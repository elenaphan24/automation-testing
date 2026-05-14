from __future__ import annotations

import pytest

from business.services.restful_booker_service import RestfulBookerService
from core.config import get as config_get
from core.http_transport import UrlLibTransport
from utils.data_factory import booking_payload


@pytest.fixture
def restful_booker_service() -> RestfulBookerService:
    return RestfulBookerService(
        UrlLibTransport(config_get("urls.restful_booker_base_url"), timeout_seconds=30)
    )


@pytest.fixture
def unique_booking() -> dict:
    """Parallel-safe booking payload with UUID-suffixed names."""
    return booking_payload()


@pytest.fixture
def created_booking(restful_booker_service: RestfulBookerService, unique_booking: dict):
    """Creates a booking before the test and guarantees deletion after.

    Yields (booking_id: int, payload: dict).
    """
    created = restful_booker_service.create_booking(unique_booking)
    booking_id: int = created["bookingid"]

    yield booking_id, unique_booking

    admin_username = config_get("restful_booker.admin_username")
    admin_password = config_get("restful_booker.admin_password")
    restful_booker_service.safe_delete_booking(booking_id, admin_username, admin_password)
