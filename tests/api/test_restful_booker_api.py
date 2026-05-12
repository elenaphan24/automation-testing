from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pytest

from business.data import scenarios


pytestmark = [
    pytest.mark.api,
    pytest.mark.skipif(
        os.getenv("RESTFUL_BOOKER_LIVE") != "1",
        reason="Set RESTFUL_BOOKER_LIVE=1 to run live Restful Booker API tests.",
    ),
]

RESTFUL_BOOKER_SCENARIOS = scenarios(
    Path(__file__).resolve().parents[2] / "data/yaml/restful_booker_scenarios.yaml"
)


@pytest.mark.parametrize("scenario", RESTFUL_BOOKER_SCENARIOS, ids=lambda item: item["name"])
def test_create_token_with_valid_admin_credentials(restful_booker_service, scenario):
    token = restful_booker_service.create_token(scenario["username"], scenario["password"])

    assert token


@pytest.mark.parametrize("scenario", RESTFUL_BOOKER_SCENARIOS, ids=lambda item: item["name"])
def test_create_token_rejects_invalid_credentials(restful_booker_service, scenario):
    result = restful_booker_service.attempt_create_token(
        scenario["invalid_username"],
        scenario["invalid_password"],
    )

    assert result["reason"] == "Bad credentials"


def _assert_booking_matches(actual: dict[str, Any], expected: dict[str, Any]) -> None:
    for key, value in expected.items():
        assert actual.get(key) == value, (
            f"booking[{key!r}] mismatch: expected {value!r}, got {actual.get(key)!r}"
        )


@pytest.mark.parametrize("scenario", RESTFUL_BOOKER_SCENARIOS, ids=lambda item: item["name"])
def test_list_booking_ids_includes_created_booking(restful_booker_service, scenario):
    created = restful_booker_service.create_booking(scenario["booking"])
    booking_id = created["bookingid"]

    try:
        booking_ids = restful_booker_service.list_booking_ids()
        assert {"bookingid": booking_id} in booking_ids

        booking = restful_booker_service.get_booking(booking_id)
        _assert_booking_matches(booking, scenario["booking"])
    finally:
        restful_booker_service.safe_delete_booking(
            booking_id, scenario["username"], scenario["password"]
        )


@pytest.mark.parametrize("scenario", RESTFUL_BOOKER_SCENARIOS, ids=lambda item: item["name"])
def test_create_booking_then_read_and_filter_by_name(restful_booker_service, scenario):
    created = restful_booker_service.create_booking(scenario["booking"])
    booking_id = created["bookingid"]

    try:
        booking = restful_booker_service.get_booking(booking_id)
        filtered_ids = restful_booker_service.list_booking_ids_by_name(
            scenario["booking"]["firstname"],
            scenario["booking"]["lastname"],
        )

        _assert_booking_matches(booking, scenario["booking"])
        assert {"bookingid": booking_id} in filtered_ids
    finally:
        restful_booker_service.safe_delete_booking(
            booking_id, scenario["username"], scenario["password"]
        )


@pytest.mark.parametrize("scenario", RESTFUL_BOOKER_SCENARIOS, ids=lambda item: item["name"])
def test_update_patch_and_delete_booking(restful_booker_service, scenario):
    created = restful_booker_service.create_booking(scenario["booking"])
    booking_id = created["bookingid"]
    restful_booker_service.create_token(scenario["username"], scenario["password"])
    deleted: dict[str, Any] | None = None

    try:
        updated = restful_booker_service.update_booking(booking_id, scenario["updated_booking"])
        patched = restful_booker_service.partially_update_booking(
            booking_id, scenario["partial_update"]
        )
        deleted = restful_booker_service.delete_booking(booking_id)

        _assert_booking_matches(updated, scenario["updated_booking"])
        _assert_booking_matches(patched, scenario["partial_update"])
        assert deleted.get("data") == "Created"
    finally:
        if deleted is None:
            restful_booker_service.safe_delete_booking(
                booking_id, scenario["username"], scenario["password"]
            )
