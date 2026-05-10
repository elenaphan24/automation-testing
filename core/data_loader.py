from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def load_test_data(file_path: str | Path) -> list[dict[str, Any]]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Test data file not found: {path}")

    with path.open(encoding="utf-8") as handle:
        if path.suffix.lower() == ".json":
            data = json.load(handle)
        else:
            data = yaml.safe_load(handle)

    if not isinstance(data, list):
        raise ValueError(f"Expected a list of scenarios in {path}")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError(f"Every scenario in {path} must be a mapping")
    return data

