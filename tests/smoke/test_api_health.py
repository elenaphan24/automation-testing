import os

import pytest


@pytest.mark.smoke
@pytest.mark.skipif(
    os.getenv("RESTFUL_BOOKER_LIVE") != "1",
    reason="Set RESTFUL_BOOKER_LIVE=1 to run live API smoke tests.",
)
def test_restful_booker_api_is_reachable(restful_booker_service):
    """Operational health: verify the API responds to auth endpoint."""
    result = restful_booker_service.attempt_create_token("admin", "password123")
    assert "token" in result or "reason" in result, f"Unexpected response: {result}"
