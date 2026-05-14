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
    if report.when == "call" and report.failed:
        screenshot = getattr(item, "_screenshot", None)
        if screenshot:
            try:
                from pytest_html import extras

                encoded = base64.b64encode(screenshot).decode("ascii")
                extra = getattr(report, "extras", [])
                extra.append(extras.png(encoded, name="failure-screenshot"))
                report.extras = extra
            except ImportError:
                logger.warning("pytest-html not installed; screenshot not embedded")
