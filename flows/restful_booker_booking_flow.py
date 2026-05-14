from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from business.services.restful_booker_service import RestfulBookerService


def create_booking(service: RestfulBookerService, payload: dict[str, Any]) -> int:
    """Creates a booking and returns its ID."""
    created = service.create_booking(payload)
    return created["bookingid"]


def wait_for_booking_in_list(
    booking_id: int,
    list_fn: Callable[[], list[dict[str, int]]],
    *,
    attempts: int = 5,
    delay_seconds: float = 1.0,
) -> list[dict[str, int]]:
    """Polls list_fn until booking_id appears or attempts are exhausted."""
    booking_ref = {"bookingid": booking_id}
    result: list[dict[str, int]] = []

    for attempt in range(attempts):
        result = list_fn()
        if booking_ref in result:
            return result
        if attempt < attempts - 1:
            time.sleep(delay_seconds)

    return result


def full_crud_flow(
    service: RestfulBookerService,
    *,
    booking: dict[str, Any],
    updated_booking: dict[str, Any],
    partial_update: dict[str, Any],
    username: str,
    password: str,
) -> dict[str, Any]:
    """Runs the full booking lifecycle: create → update → patch → delete.

    Guarantees cleanup via safe_delete_booking if delete never executes.
    Returns a dict with the booking_id and the response of each mutation.
    """
    booking_id = create_booking(service, booking)
    service.create_token(username, password)
    deleted: dict[str, Any] | None = None

    try:
        updated = service.update_booking(booking_id, updated_booking)
        patched = service.partially_update_booking(booking_id, partial_update)
        deleted = service.delete_booking(booking_id)
    finally:
        if deleted is None:
            service.safe_delete_booking(booking_id, username, password)

    return {
        "booking_id": booking_id,
        "updated": updated,
        "patched": patched,
        "deleted": deleted,
    }
