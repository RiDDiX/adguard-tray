"""
Persistent configuration stored as JSON at ~/.config/adguard-tray/config.json.
Unknown keys from disk are silently ignored (forward-compatible).
"""

import json
import logging
from dataclasses import asdict, dataclass, fields
from pathlib import Path

logger = logging.getLogger(__name__)

CONFIG_DIR = Path.home() / ".config" / "adguard-tray"
CONFIG_FILE = CONFIG_DIR / "config.json"


@dataclass
class Config:
    refresh_interval: int = 30          # seconds between auto-refresh
    notifications_enabled: bool = True  # desktop notifications on status change
    log_level: str = "INFO"             # DEBUG | INFO | WARNING | ERROR
    adguard_cli_path: str = ""          # empty = auto-detect via PATH


def load_config() -> Config:
    if not CONFIG_FILE.exists():
        return Config()
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        valid = {f.name for f in fields(Config)}
        filtered = {k: v for k, v in data.items() if k in valid}
        return Config(**filtered)
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        logger.warning("Config load failed, using defaults: %s", exc)
        return Config()


def save_config(config: Config) -> None:
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(
            json.dumps(asdict(config), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        logger.debug("Config saved to %s", CONFIG_FILE)
    except OSError as exc:
        logger.error("Config save failed: %s", exc)
