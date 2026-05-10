import pytest


pytestmark = pytest.mark.api


def test_worker_schemas_are_independent(fake_db, worker_schema):
    assert fake_db.schema_exists(worker_schema)
    assert fake_db.count_rows(worker_schema, "users") == 0

