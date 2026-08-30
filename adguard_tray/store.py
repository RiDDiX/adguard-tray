"""Keep the access log's history in a small SQLite database.

adguard-cli rotates its logs itself: the emitter checks its own write position
before every line and, past 10 MiB, renames access.log to access.log.1 and
shifts the older generations down to access.log.9 (recovered by disassembling
`ag::RotatingLogToFile`; the 10 MiB and 10-file constants are compiled in, so
there is no setting to change them). Reading the tail of the live file
therefore shows a sliding window, and everything older is gone from the app's
view the moment it rotates.

This module reads the log forward instead, remembering how far it got, and
keeps two things: recent requests, pruned to a retention window, and hourly
totals that are never pruned. The totals are what makes "last 30 days" and
"all time" answerable at all, and they cost about forty bytes an hour.

Nothing here is authoritative about the proxy – it only preserves what the log
said before adguard-cli deletes it.
"""

import logging
import os
import sqlite3
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

DB_PATH = Path.home() / ".local" / "share" / "adguard-tray" / "activity.db"
SCHEMA_VERSION = 1

# Raw rows exist for the request list and for drilling into a domain; the
# hourly rollups answer everything older. Two weeks of rows is enough for the
# list to feel complete without the file growing without bound.
RETENTION_DAYS = 14
MAX_ROWS = 400_000

# One ingest pass should not stall a worker for long, so a huge backlog is
# taken in chunks; the cursor makes the next pass continue where it stopped.
MAX_INGEST_BYTES = 16 * 1024 * 1024

# Device and inode miss the case where a file is replaced in place and happens
# to end up the same length; the opening bytes of a log almost never repeat.
_HEAD_BYTES = 256

# Per-hour detail for every domain and rule would grow without bound; the
# totals do not, so "all time" stays right while the top lists have a horizon.
DETAIL_DAYS = 90

# Two ingests reading the cursor before either commits would insert the same
# lines twice, and nothing in the schema could tell the copies apart.
_INGEST_LOCK = threading.Lock()

_SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS requests (
    ts           INTEGER NOT NULL,
    host         TEXT    NOT NULL,
    url          TEXT    NOT NULL,
    rule         TEXT    NOT NULL,
    size         INTEGER NOT NULL,
    duration     INTEGER NOT NULL,
    blocked      INTEGER NOT NULL,
    modified     INTEGER NOT NULL,
    filter_id    INTEGER NOT NULL,
    protocol     TEXT    NOT NULL,
    method       TEXT    NOT NULL,
    content_type TEXT    NOT NULL,
    status       INTEGER NOT NULL,
    app          TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS requests_ts   ON requests (ts);
CREATE INDEX IF NOT EXISTS requests_host ON requests (host, ts);

CREATE TABLE IF NOT EXISTS hourly (
    hour     INTEGER PRIMARY KEY,
    total    INTEGER NOT NULL DEFAULT 0,
    blocked  INTEGER NOT NULL DEFAULT 0,
    modified INTEGER NOT NULL DEFAULT 0,
    bytes    INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS domain_hourly (
    hour    INTEGER NOT NULL,
    host    TEXT    NOT NULL,
    total   INTEGER NOT NULL DEFAULT 0,
    blocked INTEGER NOT NULL DEFAULT 0,
    bytes   INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (hour, host)
);
CREATE TABLE IF NOT EXISTS rule_hourly (
    hour  INTEGER NOT NULL,
    rule  TEXT    NOT NULL,
    hits  INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (hour, rule)
);
"""


@dataclass
class IngestResult:
    added: int = 0
    unparsed: int = 0
    rotated: bool = False
    truncated: bool = False
    error: str = ""


def _connect(path: Path | None = None) -> sqlite3.Connection:
    """A fresh connection. One per call – they are cheap and never shared.

    sqlite3 refuses to use a connection from another thread by default, and
    this database is written by a worker and read by another one, so passing
    connections around would only invite that error.
    """
    target = path or DB_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(target, timeout=10)
    connection.execute("PRAGMA journal_mode=WAL")   # readers never wait for the writer
    connection.execute("PRAGMA synchronous=NORMAL")
    connection.executescript(_SCHEMA)
    connection.execute(
        "INSERT OR IGNORE INTO meta (key, value) VALUES ('schema', ?)", (str(SCHEMA_VERSION),))
    connection.commit()
    return connection


def _meta(connection: sqlite3.Connection, key: str, default: str = "") -> str:
    row = connection.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    return row[0] if row else default


def _set_meta(connection: sqlite3.Connection, key: str, value: str) -> None:
    connection.execute(
        "INSERT INTO meta (key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value", (key, value))


def _head(path: Path) -> str:
    """The first line of a file, as hex. Empty when there is not one yet.

    A fixed-size prefix would change as a short file grows past it, which looks
    exactly like the file having been replaced. The first line stays put for as
    long as the file does, so that is what identifies it.
    """
    try:
        with path.open("rb") as handle:
            chunk = handle.read(_HEAD_BYTES)
    except OSError:
        return ""
    end = chunk.find(b"\n")
    if end >= 0:
        return chunk[:end].hex()
    # No newline yet: only a full buffer is a stable fingerprint.
    return chunk.hex() if len(chunk) == _HEAD_BYTES else ""


def _hour_of(when: datetime) -> int:
    stamp = int(when.timestamp())
    return stamp - stamp % 3600


def _read_new(path: Path, offset: int) -> tuple[list[str], int, str, str]:
    """Lines added since *offset*, the offset after them, and what was read.

    Only whole lines are consumed: the daemon may be halfway through writing
    the last one, and a partial line would be counted as unreadable and then
    never seen complete. Cutting at a newline also keeps multi-byte characters
    intact, since a newline byte cannot occur inside one.

    The identity comes from the open handle, not from a separate stat(): a
    rotation between the two would otherwise pin the new file's offset to the
    old file's identity, and the next pass would read a whole generation again.
    """
    try:
        with path.open("rb") as handle:
            info = os.fstat(handle.fileno())
            identity = f"{info.st_dev}:{info.st_ino}"
            handle.seek(offset)
            chunk = handle.read(MAX_INGEST_BYTES)
    except OSError as exc:
        return [], offset, str(exc), ""
    if not chunk:
        return [], offset, "", identity
    end = chunk.rfind(b"\n")
    if end < 0:
        if len(chunk) >= MAX_INGEST_BYTES:
            # A whole buffer with no line ending: one record longer than the
            # buffer. Waiting for its end would stall the cursor here forever,
            # so step over it and let the caller count it as unreadable.
            return [""], offset + len(chunk), "", identity
        return [], offset, "", identity           # nothing complete yet
    text = chunk[:end + 1].decode("utf-8", errors="replace")
    # split("\n"), not splitlines(): the latter also breaks on U+2028 and
    # friends, which would shred one record into two unreadable halves.
    return text[:-1].split("\n"), offset + end + 1, "", identity


def _owed_generations(path: Path, previous_ino: int) -> list[Path]:
    """The rotated files holding what we had not read yet, oldest first.

    Two rollovers between two passes push the file we were reading down to
    access.log.2, so looking only at .1 would drop a whole generation without
    a word. Everything from the one we know down to .1 is owed.
    """
    for index in range(1, 10):
        candidate = path.with_name(f"{path.name}.{index}")
        try:
            if candidate.is_file() and candidate.stat().st_ino == previous_ino:
                break
        except OSError:
            continue
    else:
        return []
    owed = []
    for step in range(index, 0, -1):
        candidate = path.with_name(f"{path.name}.{step}")
        if candidate.is_file():
            owed.append(candidate)
    return owed


def ingest(db: Path | None = None, log_path: Path | None = None) -> IngestResult:
    """Read whatever the log gained since last time. Never raises."""
    with _INGEST_LOCK:
        return _ingest(db, log_path)


def _ingest(db: Path | None, log_path: Path | None) -> IngestResult:
    from .stats import access_log_path, parse_line

    result = IngestResult()
    path = log_path or access_log_path()
    try:
        connection = _connect(db)
    except sqlite3.Error as exc:
        logger.warning("Could not open the activity database: %s", exc)
        result.error = str(exc)
        return result

    try:
        known = _meta(connection, "log_identity")
        if not known:
            # First run: the rotated generations still hold history.
            backfilled = _backfill(connection, path)
            result.added += backfilled.added
            result.unparsed += backfilled.unparsed

        try:
            info = path.stat()
        except OSError as exc:
            result.error = str(exc)
            return result

        identity = f"{info.st_dev}:{info.st_ino}"
        offset = int(_meta(connection, "log_offset", "0") or 0)
        head = _head(path)
        known_head = _meta(connection, "log_head")
        # Only comparable when both sides actually have a fingerprint.
        head_changed = bool(known) and bool(head) and bool(known_head) and head != known_head

        rows: list[str] = []
        previous_ino = int(known.split(":")[-1]) if known else 0
        # Same file, now shorter than we had read: it was emptied in place.
        # This has to be decided before the replacement check, because
        # truncation changes the opening bytes too.
        truncated_in_place = bool(known) and known == identity and offset > info.st_size
        if truncated_in_place:
            result.truncated = True
            # Emptied and refilled, or merely shortened? An unchanged first
            # line means the bytes that are left are the ones already read, so
            # starting over would count them twice.
            offset = info.st_size if (head and known_head and head == known_head) else 0
        elif known and (known != identity or head_changed):
            # The file we were reading is gone: either rotation renamed it,
            # or something replaced it in place. Its tail may still be on
            # disk, and without it up to 10 MiB of requests would be lost at
            # every rollover.
            result.rotated = True
            owed = _owed_generations(path, previous_ino)
            for position, older in enumerate(owed):
                # Only the generation we were reading has a meaningful offset;
                # any generation after it has to be read whole.
                lines, _, error, _ = _read_new(older, offset if position == 0 else 0)
                if error:
                    result.error = error
                    return result          # leave the cursor alone and retry
                rows.extend(lines)
            offset = 0

        fresh, new_offset, error, read_identity = _read_new(path, offset)
        if error:
            result.error = error
            return result
        rows.extend(fresh)

        parsed = []
        for line in rows:
            if not line.strip():
                continue
            request = parse_line(line)
            if request is None or request.when is None:
                # A request without a timestamp cannot be placed in a bucket,
                # so it would silently distort every total.
                result.unparsed += 1
                continue
            parsed.append(request)

        if parsed:
            _write(connection, parsed)
            result.added += len(parsed)
        # The identity of the file the offset actually belongs to.
        _set_meta(connection, "log_identity", read_identity or identity)
        _set_meta(connection, "log_offset", str(new_offset))
        if head:
            _set_meta(connection, "log_head", head)
        connection.commit()
        _prune(connection)
        connection.commit()
    except sqlite3.Error as exc:
        logger.warning("Activity ingest failed: %s", exc)
        result.error = str(exc)
    finally:
        connection.close()
    return result


def _backfill(connection: sqlite3.Connection, path: Path) -> IngestResult:
    """Read the rotated generations once, oldest first.

    Only on a first run, when there is no cursor yet: up to nine generations
    of history sit next to the live log, and ignoring them would start the
    store empty on a machine that has been filtering for weeks.
    """
    from .stats import parse_line

    result = IngestResult()
    for index in range(9, 0, -1):
        older = path.with_name(f"{path.name}.{index}")
        if not older.is_file():
            continue
        lines, _, error, _ = _read_new(older, 0)
        if error:
            continue
        parsed = []
        for line in lines:
            if not line.strip():
                continue
            request = parse_line(line)
            if request is None or request.when is None:
                result.unparsed += 1
            else:
                parsed.append(request)
        if parsed:
            _write(connection, parsed)
            result.added += len(parsed)
    if result.added:
        logger.info("Backfilled %d requests from rotated logs", result.added)
    return result


def _write(connection: sqlite3.Connection, requests: list) -> None:
    connection.executemany(
        "INSERT INTO requests (ts, host, url, rule, size, duration, blocked, modified,"
        " filter_id, protocol, method, content_type, status, app)"
        " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [(int(r.when.timestamp()), r.host, r.url, r.rule, max(0, r.size),
          max(0, r.duration_ms), int(r.blocked), int(r.modified), r.filter_id,
          r.protocol, r.method, r.content_type, r.status, r.app) for r in requests])

    hours: dict[int, list[int]] = {}
    domains: dict[tuple[int, str], list[int]] = {}
    rules: dict[tuple[int, str], int] = {}
    for r in requests:
        hour = _hour_of(r.when)
        size = max(0, r.size)
        slot = hours.setdefault(hour, [0, 0, 0, 0])
        slot[0] += 1
        slot[1] += int(r.blocked)
        slot[2] += int(r.modified)
        slot[3] += size
        if r.host:
            entry = domains.setdefault((hour, r.host), [0, 0, 0])
            entry[0] += 1
            entry[1] += int(r.blocked)
            entry[2] += size
        if r.rule:
            rules[(hour, r.rule)] = rules.get((hour, r.rule), 0) + 1

    connection.executemany(
        "INSERT INTO hourly (hour, total, blocked, modified, bytes) VALUES (?,?,?,?,?)"
        " ON CONFLICT(hour) DO UPDATE SET total = total + excluded.total,"
        " blocked = blocked + excluded.blocked, modified = modified + excluded.modified,"
        " bytes = bytes + excluded.bytes",
        [(hour, *counts) for hour, counts in hours.items()])
    connection.executemany(
        "INSERT INTO domain_hourly (hour, host, total, blocked, bytes) VALUES (?,?,?,?,?)"
        " ON CONFLICT(hour, host) DO UPDATE SET total = total + excluded.total,"
        " blocked = blocked + excluded.blocked, bytes = bytes + excluded.bytes",
        [(hour, host, *counts) for (hour, host), counts in domains.items()])
    connection.executemany(
        "INSERT INTO rule_hourly (hour, rule, hits) VALUES (?,?,?)"
        " ON CONFLICT(hour, rule) DO UPDATE SET hits = hits + excluded.hits",
        [(hour, rule, hits) for (hour, rule), hits in rules.items()])


def _prune(connection: sqlite3.Connection) -> None:
    """Drop what is past its horizon.

    The hourly totals are kept forever – they are four numbers an hour. The
    per-domain and per-rule detail is one row per distinct name per hour, so
    it would grow with the variety of the traffic and needs a horizon of its
    own; past it the totals remain but the top lists do not.
    """
    now = int(time.time())
    cutoff = now - RETENTION_DAYS * 86400
    connection.execute("DELETE FROM requests WHERE ts < ?", (cutoff,))
    detail_cutoff = now - DETAIL_DAYS * 86400
    connection.execute("DELETE FROM domain_hourly WHERE hour < ?", (detail_cutoff,))
    connection.execute("DELETE FROM rule_hourly WHERE hour < ?", (detail_cutoff,))
    count = connection.execute("SELECT COUNT(*) FROM requests").fetchone()[0]
    if count > MAX_ROWS:
        connection.execute(
            "DELETE FROM requests WHERE rowid IN ("
            " SELECT rowid FROM requests ORDER BY ts LIMIT ?)", (count - MAX_ROWS,))


# ── Queries ───────────────────────────────────────────────────────────────

def _range(hours: int | None) -> tuple[int, int]:
    """(from, to) in epoch seconds, aligned to the hour.

    The rollups are keyed by hour, so an unaligned start would drop the bucket
    the range begins in and the cards would disagree with the request list.
    """
    now = int(time.time())
    end = now - now % 3600 + 3600
    return (0 if hours is None else end - hours * 3600), end


def summary(hours: int | None = 24, db: Path | None = None) -> dict:
    """Totals for a range, answered from the rollups so it stays cheap."""
    start, end = _range(hours)
    connection = _connect(db)
    try:
        row = connection.execute(
            "SELECT COALESCE(SUM(total),0), COALESCE(SUM(blocked),0),"
            " COALESCE(SUM(modified),0), COALESCE(SUM(bytes),0), MIN(hour), MAX(hour)"
            " FROM hourly WHERE hour >= ? AND hour < ?", (start, end)).fetchone()
        return {
            "total": row[0], "blocked": row[1], "modified": row[2], "bytes": row[3],
            "first_hour": row[4], "last_hour": row[5],
        }
    finally:
        connection.close()


def per_hour(hours: int = 24, db: Path | None = None) -> list[tuple[datetime, int, int]]:
    """(hour, total, blocked) for the last *hours*, quiet hours included."""
    connection = _connect(db)
    try:
        if connection.execute("SELECT MAX(hour) FROM hourly").fetchone()[0] is None:
            return []
        # Anchored on the clock: a quiet proxy should show empty hours, not
        # yesterday's bars under a "last 24 hours" label.
        now = int(time.time())
        last = now - now % 3600
        rows = dict(
            (hour, (total, blocked)) for hour, total, blocked in connection.execute(
                "SELECT hour, total, blocked FROM hourly WHERE hour > ?",
                (last - hours * 3600,)))
    finally:
        connection.close()
    out = []
    for back in range(max(1, hours) - 1, -1, -1):
        hour = last - back * 3600
        total, blocked = rows.get(hour, (0, 0))
        out.append((datetime.fromtimestamp(hour), total, blocked))
    return out


def top_hosts(hours: int | None = 24, limit: int = 10, blocked_only: bool = False,
              by_bytes: bool = False, db: Path | None = None) -> list[tuple[str, int]]:
    start, end = _range(hours)
    column = "bytes" if by_bytes else ("blocked" if blocked_only else "total")
    connection = _connect(db)
    try:
        return [(host, value) for host, value in connection.execute(
            f"SELECT host, SUM({column}) AS value FROM domain_hourly"
            " WHERE hour >= ? AND hour < ? GROUP BY host HAVING value > 0"
            " ORDER BY value DESC, host LIMIT ?", (start, end, limit))]
    finally:
        connection.close()


def top_rules(hours: int | None = 24, limit: int = 10,
              db: Path | None = None) -> list[tuple[str, int]]:
    start, end = _range(hours)
    connection = _connect(db)
    try:
        return [(rule, hits) for rule, hits in connection.execute(
            "SELECT rule, SUM(hits) AS n FROM rule_hourly WHERE hour >= ? AND hour < ?"
            " GROUP BY rule ORDER BY n DESC, rule LIMIT ?", (start, end, limit))]
    finally:
        connection.close()


def recent(hours: int | None = 24, limit: int = 500, host: str = "",
           db: Path | None = None) -> list[sqlite3.Row]:
    """The newest raw requests, optionally for one domain."""
    start, end = _range(hours)
    connection = _connect(db)
    connection.row_factory = sqlite3.Row
    try:
        if host:
            return connection.execute(
                "SELECT * FROM requests WHERE ts >= ? AND ts < ? AND host = ?"
                " ORDER BY ts DESC LIMIT ?", (start, end, host, limit)).fetchall()
        return connection.execute(
            "SELECT * FROM requests WHERE ts >= ? AND ts < ?"
            " ORDER BY ts DESC LIMIT ?", (start, end, limit)).fetchall()
    finally:
        connection.close()


def dashboard(hours: int | None = 24, chart_hours: int = 24, host: str = "",
              limit: int = 10, rows: int = 500, db: Path | None = None) -> dict:
    """Everything one screen needs, from a single read of the database.

    Asking each question on its own connection would let an ingest commit
    between them, so the cards could count requests the list below does not
    show.
    """
    start, end = _range(hours)
    connection = _connect(db)
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("BEGIN")
        row = connection.execute(
            "SELECT COALESCE(SUM(total),0), COALESCE(SUM(blocked),0),"
            " COALESCE(SUM(modified),0), COALESCE(SUM(bytes),0)"
            " FROM hourly WHERE hour >= ? AND hour < ?", (start, end)).fetchone()
        data = {
            "summary": {"total": row[0], "blocked": row[1],
                        "modified": row[2], "bytes": row[3]},
            "hours": _chart(connection, chart_hours),
        }
        for key, column in (("blocked", "blocked"), ("active", "total"), ("traffic", "bytes")):
            data[key] = [(name, value) for name, value in connection.execute(
                f"SELECT host, SUM({column}) AS value FROM domain_hourly"
                " WHERE hour >= ? AND hour < ? GROUP BY host HAVING value > 0"
                " ORDER BY value DESC, host LIMIT ?", (start, end, limit))]
        data["rules"] = [(name, hits) for name, hits in connection.execute(
            "SELECT rule, SUM(hits) AS n FROM rule_hourly WHERE hour >= ? AND hour < ?"
            " GROUP BY rule ORDER BY n DESC, rule LIMIT ?", (start, end, limit))]
        if host:
            data["recent"] = connection.execute(
                "SELECT * FROM requests WHERE ts >= ? AND ts < ? AND host = ?"
                " ORDER BY ts DESC LIMIT ?", (start, end, host, rows)).fetchall()
        else:
            data["recent"] = connection.execute(
                "SELECT * FROM requests WHERE ts >= ? AND ts < ?"
                " ORDER BY ts DESC LIMIT ?", (start, end, rows)).fetchall()
        connection.commit()
        return data
    finally:
        connection.close()


def _chart(connection: sqlite3.Connection, hours: int) -> list[tuple[datetime, int, int]]:
    now = int(time.time())
    last = now - now % 3600
    rows = dict(
        (hour, (total, blocked)) for hour, total, blocked in connection.execute(
            "SELECT hour, total, blocked FROM hourly WHERE hour > ? AND hour <= ?",
            (last - hours * 3600, last)))
    if not rows and not connection.execute("SELECT 1 FROM hourly LIMIT 1").fetchone():
        return []
    out = []
    for back in range(max(1, hours) - 1, -1, -1):
        hour = last - back * 3600
        total, blocked = rows.get(hour, (0, 0))
        out.append((datetime.fromtimestamp(hour), total, blocked))
    return out


def db_size(db: Path | None = None) -> int:
    target = db or DB_PATH
    total = 0
    for suffix in ("", "-wal", "-shm"):
        try:
            total += (target.parent / (target.name + suffix)).stat().st_size
        except OSError:
            pass
    return total


def reset(db: Path | None = None) -> tuple[bool, str]:
    """Forget everything and start reading the log from scratch.

    The tables are emptied rather than the files deleted: another thread may
    still hold a connection, and unlinking the database out from under it
    would leave it writing into a file nobody will ever read again.
    """
    with _INGEST_LOCK:
        try:
            connection = _connect(db)
        except sqlite3.Error as exc:
            return False, str(exc)
        try:
            with connection:
                for table in ("requests", "hourly", "domain_hourly", "rule_hourly", "meta"):
                    connection.execute(f"DELETE FROM {table}")
            connection.execute("VACUUM")
        except sqlite3.Error as exc:
            return False, str(exc)
        finally:
            connection.close()
    return True, ""
