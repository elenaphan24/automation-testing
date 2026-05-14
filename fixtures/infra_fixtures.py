from __future__ import annotations

import uuid
from typing import Any

import pytest

from core.config import load_config
from utils.failure_artifacts import export_failure_artifact
from core.logging_util import get_logger

logger = get_logger("taf.fixtures.infra", "TAF")


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
