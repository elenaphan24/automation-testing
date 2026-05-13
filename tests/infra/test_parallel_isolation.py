import pytest


pytestmark = pytest.mark.api


def test_worker_schemas_are_independent(schema_registry, worker_schema):
    assert schema_registry.schema_exists(worker_schema)
    assert schema_registry.count_rows(worker_schema, "users") == 0

