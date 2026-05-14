from __future__ import annotations

import uuid
from typing import Any


def _uid() -> str:
    return uuid.uuid4().hex[:8]


def booking_payload(
    *,
    firstname: str | None = None,
    lastname: str | None = None,
    totalprice: int = 100,
    depositpaid: bool = True,
    checkin: str = "2026-06-01",
    checkout: str = "2026-06-05",
    additionalneeds: str = "None",
) -> dict[str, Any]:
    """Returns a unique booking payload safe for parallel execution.

    Names are auto-generated with a UUID suffix when omitted, preventing
    firstname/lastname filter collisions between concurrent tests.
    """
    uid = _uid()
    return {
        "firstname": firstname or f"Test{uid}",
        "lastname": lastname or f"User{uid}",
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": {
            "checkin": checkin,
            "checkout": checkout,
        },
        "additionalneeds": additionalneeds,
    }


def saucedemo_user(
    *,
    username: str = "standard_user",
    password: str = "secret_sauce",
) -> dict[str, str]:
    """Returns SauceDemo credentials. Override for locked/problem user variants."""
    return {"username": username, "password": password}
