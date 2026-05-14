from __future__ import annotations

import base64
import os
from typing import Any

import pytest

from core.config import load_config, validate_required_keys
from core.logging_util import get_logger

logger = get_logger("taf.conftest", "TAF")

pytest_plugins = [
    "fixtures.infra_fixtures",
    "fixtures.browser_fixtures",
    "fixtures.page_fixtures",
    "fixtures.service_fixtures",
]


def pytest_configure(config: pytest.Config) -> None:
    try:
        cfg = load_config()
        missing = validate_required_keys()
        if missing:
            raise ValueError(f"Missing required config keys: {missing}")
        logger.info("Active environment: %s", cfg.get("env", "unknown").upper())
    except Exception as exc:
        pytest.exit(f"[CONFIG ERROR] {exc}", returncode=1)


def pytest_xdist_auto_num_workers(config: pytest.Config) -> int:
    if os.getenv("CI") or os.getenv("TF_BUILD"):
        return int(os.getenv("CI_WORKER_COUNT", "4"))
    return int(os.getenv("LOCAL_WORKER_COUNT", "2"))


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if os.getenv("ENV", "sandbox").lower() != "production":
        return
    non_smoke = [item.nodeid for item in items if "smoke" not in item.keywords]
    if non_smoke:
        sample = "\n".join(non_smoke[:5])
        pytest.exit(
            "ENV=production only allows tests marked with 'smoke'. "
            f"Non-smoke tests were collected:\n{sample}",
            returncode=1,
        )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[Any]):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    try:
        from pytest_html import extras as html_extras

        extra = getattr(report, "extras", [])

        # Embed captured log for every test phase that produced output
        for section_name, section_content in report.sections:
            if "log" in section_name.lower() and section_content.strip():
                lines = section_content.strip().split("\n")
                rows = "".join(
                    f"<tr><td style='white-space:pre;font-family:monospace;"
                    f"font-size:12px;padding:2px 6px'>{line}</td></tr>"
                    for line in lines
                )
                table = (
                    f"<table style='width:100%;border-collapse:collapse;margin-top:4px'>"
                    f"<thead><tr><th style='text-align:left;background:#dce8f5;"
                    f"padding:4px 6px'>{section_name}</th></tr></thead>"
                    f"<tbody>{rows}</tbody></table>"
                )
                extra.append(html_extras.html(table))

        # Failure screenshot
        if report.when == "call" and report.failed:
            screenshot = getattr(item, "_screenshot", None)
            if screenshot:
                encoded = base64.b64encode(screenshot).decode("ascii")
                extra.append(html_extras.png(encoded, name="failure-screenshot"))

        report.extras = extra
    except ImportError:
        logger.warning("pytest-html not installed; extras not embedded")
