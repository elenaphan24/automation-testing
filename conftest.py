from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Any

import pytest

from business.pages.login_page import LoginPage
from business.services.user_service import UserService
from core.config import load_config, validate_required_keys
from core.failure_artifacts import export_failure_artifact
from core.fake_sut import FakeApiTransport, FakeBrowserPage, FakeDatabase
from core.logging_util import get_logger

logger = get_logger("taf.conftest", "TAF")


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


@pytest.fixture(autouse=True)
def capture_artifacts_on_failure(request: pytest.FixtureRequest):
    yield
    report = getattr(request.node, "rep_call", None)
    if report and report.failed:
        artifact_dir = export_failure_artifact(request.node)
        logger.info("exported failure artifacts to %s", artifact_dir)
        try:
            from core.allure_compat import allure

            screenshot = getattr(request.node, "_screenshot", None)
            if screenshot:
                allure.attach(
                    screenshot,
                    name="failure-screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
        except Exception:
            pass


@pytest.fixture(scope="session")
def fake_db() -> FakeDatabase:
    return FakeDatabase()


@pytest.fixture(scope="session")
def worker_id(request: pytest.FixtureRequest) -> str:
    return getattr(request.config, "workerinput", {}).get("workerid", "master")


@pytest.fixture(scope="session")
def worker_schema(worker_id: str, fake_db: FakeDatabase) -> str:
    prefix = load_config().get("database", {}).get("schema_prefix", "test")
    schema = f"{prefix}_{worker_id}_{uuid.uuid4().hex[:6]}"
    fake_db.create_schema(schema)
    yield schema
    fake_db.drop_schema(schema)


@pytest.fixture
def api_transport(fake_db: FakeDatabase, worker_schema: str) -> FakeApiTransport:
    return FakeApiTransport(fake_db, worker_schema)


@pytest.fixture
def user_service(api_transport: FakeApiTransport) -> UserService:
    return UserService(api_transport)


@pytest.fixture
def browser_page(request: pytest.FixtureRequest) -> FakeBrowserPage:
    page = FakeBrowserPage()
    page._pytest_node = request.node
    return page


@pytest.fixture
def login_page(browser_page: FakeBrowserPage) -> LoginPage:
    return LoginPage(browser_page)
