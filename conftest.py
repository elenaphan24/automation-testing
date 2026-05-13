from __future__ import annotations

import base64
import os
import uuid
from typing import Any

import pytest

from business.pages.saucedemo_cart_page import SauceDemoCartPage
from business.pages.saucedemo_checkout_page import SauceDemoCheckoutPage
from business.pages.saucedemo_inventory_page import SauceDemoInventoryPage
from business.pages.saucedemo_login_page import SauceDemoLoginPage
from business.services.restful_booker_service import RestfulBookerService
from core.config import get as config_get, load_config, validate_required_keys
from core.failure_artifacts import export_failure_artifact
from core.http_transport import UrlLibTransport
from core.logging_util import get_logger

logger = get_logger("taf.conftest", "TAF")


class SchemaRegistry:
    def __init__(self) -> None:
        self.schemas: dict[str, dict[str, list[Any]]] = {}

    def create_schema(self, schema: str) -> None:
        self.schemas[schema] = {"users": []}

    def drop_schema(self, schema: str) -> None:
        self.schemas.pop(schema, None)

    def schema_exists(self, schema: str) -> bool:
        return schema in self.schemas

    def count_rows(self, schema: str, table: str) -> int:
        return len(self.schemas[schema][table])


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


@pytest.fixture(autouse=True)
def capture_artifacts_on_failure(request: pytest.FixtureRequest):
    yield
    report = getattr(request.node, "rep_call", None)
    if report and report.failed:
        artifact_dir = export_failure_artifact(request.node)
        logger.info("exported failure artifacts to %s", artifact_dir)


@pytest.fixture(scope="session")
def worker_id(request: pytest.FixtureRequest) -> str:
    return getattr(request.config, "workerinput", {}).get("workerid", "master")


@pytest.fixture(scope="session")
def schema_registry() -> SchemaRegistry:
    return SchemaRegistry()


@pytest.fixture(scope="session")
def worker_schema(worker_id: str, schema_registry: SchemaRegistry) -> str:
    prefix = load_config().get("database", {}).get("schema_prefix", "test")
    schema = f"{prefix}_{worker_id}_{uuid.uuid4().hex[:6]}"
    schema_registry.create_schema(schema)
    yield schema
    schema_registry.drop_schema(schema)


@pytest.fixture
def restful_booker_service() -> RestfulBookerService:
    return RestfulBookerService(
        UrlLibTransport(config_get("urls.restful_booker_base_url"), timeout_seconds=30)
    )


@pytest.fixture(scope="session")
def live_browser():
    pytest.importorskip("playwright.sync_api")
    from playwright.sync_api import sync_playwright

    headless = os.getenv("LIVE_HEADLESS", "1") != "0"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        try:
            yield browser
        finally:
            browser.close()


@pytest.fixture
def live_browser_page(live_browser):
    context = live_browser.new_context()
    try:
        yield context.new_page()
    finally:
        context.close()


@pytest.fixture
def saucedemo_login_page(live_browser_page) -> SauceDemoLoginPage:
    return SauceDemoLoginPage(live_browser_page)


@pytest.fixture
def saucedemo_inventory_page(live_browser_page) -> SauceDemoInventoryPage:
    return SauceDemoInventoryPage(live_browser_page)


@pytest.fixture
def saucedemo_cart_page(live_browser_page) -> SauceDemoCartPage:
    return SauceDemoCartPage(live_browser_page)


@pytest.fixture
def saucedemo_checkout_page(live_browser_page) -> SauceDemoCheckoutPage:
    return SauceDemoCheckoutPage(live_browser_page)
