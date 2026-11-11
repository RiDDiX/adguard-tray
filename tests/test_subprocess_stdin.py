import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent.parent / "adguard_tray"
SPAWNERS = {"run", "Popen", "check_output", "call"}


def inheriting_calls(source: str) -> list[int]:
    lines = []
    for node in ast.walk(ast.parse(source)):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess"
                and node.func.attr in SPAWNERS
                and not {kw.arg for kw in node.keywords
                         if not (isinstance(kw.value, ast.Constant) and kw.value.value is None)} & {"stdin", "input"}):
            lines.append(node.lineno)
    return lines


def test_no_subprocess_inherits_the_trays_stdin():
    found = {path.name: inheriting_calls(path.read_text(encoding="utf-8"))
             for path in sorted(PACKAGE.glob("*.py"))}
    assert {name: lines for name, lines in found.items() if lines} == {}


def test_stdin_none_counts_as_inheriting():
    source = "import subprocess\nsubprocess.run(['x'], stdin=None)\nsubprocess.run(['x'], stdin=subprocess.DEVNULL)\n"
    assert inheriting_calls(source) == [2]
