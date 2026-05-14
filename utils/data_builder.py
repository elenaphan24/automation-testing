from __future__ import annotations

from typing import Any

from utils.data_factory import booking_payload


class BookingBuilder:
    """Fluent builder for booking payloads.

    Example::
        payload = (
            BookingBuilder()
            .with_name("Alice", "Smith")
            .with_dates("2026-09-01", "2026-09-05")
            .with_price(250)
            .build()
        )
    """

    def __init__(self) -> None:
        self._firstname: str | None = None
        self._lastname: str | None = None
        self._totalprice: int = 100
        self._depositpaid: bool = True
        self._checkin: str = "2026-06-01"
        self._checkout: str = "2026-06-05"
        self._additionalneeds: str = "None"

    def with_name(self, firstname: str, lastname: str) -> "BookingBuilder":
        self._firstname = firstname
        self._lastname = lastname
        return self

    def with_dates(self, checkin: str, checkout: str) -> "BookingBuilder":
        self._checkin = checkin
        self._checkout = checkout
        return self

    def with_price(self, totalprice: int) -> "BookingBuilder":
        self._totalprice = totalprice
        return self

    def with_deposit(self, depositpaid: bool) -> "BookingBuilder":
        self._depositpaid = depositpaid
        return self

    def with_additional_needs(self, additionalneeds: str) -> "BookingBuilder":
        self._additionalneeds = additionalneeds
        return self

    def build(self) -> dict[str, Any]:
        return booking_payload(
            firstname=self._firstname,
            lastname=self._lastname,
            totalprice=self._totalprice,
            depositpaid=self._depositpaid,
            checkin=self._checkin,
            checkout=self._checkout,
            additionalneeds=self._additionalneeds,
        )
