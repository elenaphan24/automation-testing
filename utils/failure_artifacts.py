from __future__ import annotations

import json
import re
import traceback
from pathlib import Path
from typing import Any

from core.config import get


def _safe_nodeid(nodeid: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", nodeid).strip("_")


def export_failure_artifact(node: Any) -> Path:
    base_dir = Path(get("logging.artifact_dir", "reports/failure_artifacts"))
    artifact_dir = base_dir / _safe_nodeid(node.nodeid)
    artifact_dir.mkdir(parents=True, exist_ok=True)

    report = getattr(node, "rep_call", None)
    longrepr = str(getattr(report, "longrepr", "")) if report else ""
    (artifact_dir / "stack_trace.txt").write_text(longrepr or traceback.format_exc(), encoding="utf-8")

    api_log = {
        "test_id": node.nodeid,
        "layer": "UNKNOWN",
        "source": "pytest failure artifact hook",
        "note": "Replace with structured API request/response log when real transport is integrated.",
    }
    (artifact_dir / "api_log.json").write_text(json.dumps(api_log, indent=2), encoding="utf-8")

    # Replace with real page.screenshot() and context.tracing.stop() when Playwright is wired.
    (artifact_dir / "ui_screenshot.png").write_bytes(b"")
    (artifact_dir / "playwright_trace.zip").write_bytes(b"")

    (artifact_dir / "README.txt").write_text(
        "Failure artifacts are intentionally file-based. AI analysis reads these files only.\n",
        encoding="utf-8",
    )
    return artifact_dir
