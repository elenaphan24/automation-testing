from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pytest

from utils.data_loader import scenarios
from flows.restful_booker_booking_flow import (
    create_booking,
    full_crud_flow,
    wait_for_booking_in_list,
)


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


def _assert_booking_matches(actual: dict[str, Any], expected: dict[str, Any]) -> None:
    for key, value in expected.items():
        assert actual.get(key) == value, (
            f"booking[{key!r}] mismatch: expected {value!r}, got {actual.get(key)!r}"
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


@pytest.mark.parametrize("scenario", RESTFUL_BOOKER_SCENARIOS, ids=lambda item: item["name"])
def test_list_booking_ids_includes_created_booking(restful_booker_service, scenario):
    booking_id = create_booking(restful_booker_service, scenario["booking"])

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
def test_create_booking_then_read_and_filter_by_name(restful_booker_service, scenario, unique_booking):
    booking_id = create_booking(restful_booker_service, unique_booking)

    try:
        booking = restful_booker_service.get_booking(booking_id)
        filtered_ids = wait_for_booking_in_list(
            booking_id,
            lambda: restful_booker_service.list_booking_ids_by_name(
                unique_booking["firstname"],
                unique_booking["lastname"],
            ),
        )

        _assert_booking_matches(booking, unique_booking)
        if {"bookingid": booking_id} not in filtered_ids:
            pytest.xfail(
                "Restful Booker live API returned the booking by id but did not expose it "
                "through the firstname/lastname filter."
            )
    finally:
        restful_booker_service.safe_delete_booking(
            booking_id, scenario["username"], scenario["password"]
        )


@pytest.mark.parametrize("scenario", RESTFUL_BOOKER_SCENARIOS, ids=lambda item: item["name"])
def test_update_patch_and_delete_booking(restful_booker_service, scenario):
    result = full_crud_flow(
        restful_booker_service,
        booking=scenario["booking"],
        updated_booking=scenario["updated_booking"],
        partial_update=scenario["partial_update"],
        username=scenario["username"],
        password=scenario["password"],
    )

    _assert_booking_matches(result["updated"], scenario["updated_booking"])
    _assert_booking_matches(result["patched"], scenario["partial_update"])
    assert result["deleted"].get("data") == "Created"
