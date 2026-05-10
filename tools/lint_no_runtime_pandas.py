from __future__ import annotations

import ast
from pathlib import Path

ALLOWED = {Path("core/excel_adapter.py")}
SCAN_DIRS = [Path("business"), Path("core"), Path("tests")]


def imports_pandas(path: Path) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "pandas" for alias in node.names):
                return True
        if isinstance(node, ast.ImportFrom) and node.module == "pandas":
            return True
    return False


def main() -> int:
    violations: list[Path] = []
    for directory in SCAN_DIRS:
        for path in directory.rglob("*.py"):
            if path in ALLOWED:
                continue
            if imports_pandas(path):
                violations.append(path)

    if violations:
        print("Runtime pandas imports are forbidden outside core/excel_adapter.py:")
        for path in violations:
            print(f"- {path}")
        return 1
    print("No runtime pandas imports found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

