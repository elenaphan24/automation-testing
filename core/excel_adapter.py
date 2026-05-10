from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml


def excel_to_yaml(excel_path: str | Path, output_path: str | Path) -> None:
    source = Path(excel_path)
    target = Path(output_path)
    if not source.exists():
        raise FileNotFoundError(f"Excel file not found: {source}")

    records = pd.read_excel(source).to_dict(orient="records")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(records, handle, sort_keys=False)

