import pytest


pytestmark = pytest.mark.api


def test_create_user_api_poc(user_service):
    user = user_service.create_user(email="poc-api@example.test")

    assert user["email"] == "poc-api@example.test"
    assert user["type"] == "standard"

