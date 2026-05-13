import pytest


pytestmark = pytest.mark.api


def test_worker_schemas_are_independent(schema_registry, worker_schema):
    schema_registry.schemas[worker_schema]["users"].append({"id": 1})
    assert schema_registry.schema_exists(worker_schema)
    assert schema_registry.count_rows(worker_schema, "users") == 1


def test_separate_schema_starts_empty(schema_registry):
    import uuid

    other = f"test_other_{uuid.uuid4().hex[:6]}"
    schema_registry.create_schema(other)
    try:
        assert schema_registry.count_rows(other, "users") == 0
    finally:
        schema_registry.drop_schema(other)

