from __future__ import annotations

from pathlib import Path
from typing import Any

from core.data_loader import load_test_data as _load_test_data


def scenarios(file_path: str | Path) -> list[dict[str, Any]]:
    return _load_test_data(file_path)

