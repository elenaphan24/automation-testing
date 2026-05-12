from __future__ import annotations

from typing import Any

from core.base_service import BaseService


class RestfulBookerService(BaseService):
    def _headers(self) -> dict[str, str]:
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if self.auth_token:
            headers["Cookie"] = f"token={self.auth_token}"
        return headers

    def create_token(self, username: str, password: str) -> str:
        result = self.request("POST", "/auth", {"username": username, "password": password})
        token = result.get("token")
        if not token:
            raise AssertionError(f"Restful Booker did not return a token: {result}")
        self.auth_token = token
        return token

    def attempt_create_token(self, username: str, password: str) -> dict[str, Any]:
        return self.request("POST", "/auth", {"username": username, "password": password})

    def list_booking_ids(self) -> list[dict[str, int]]:
        result = self.request("GET", "/booking")
        return result.get("data", [])

    def list_booking_ids_by_name(self, firstname: str, lastname: str) -> list[dict[str, int]]:
        result = self.request("GET", f"/booking?firstname={firstname}&lastname={lastname}")
        return result.get("data", [])

    def get_booking(self, booking_id: int) -> dict[str, Any]:
        return self.request("GET", f"/booking/{booking_id}")

    def create_booking(self, booking: dict[str, Any]) -> dict[str, Any]:
        return self.request("POST", "/booking", booking)

    def update_booking(self, booking_id: int, booking: dict[str, Any]) -> dict[str, Any]:
        return self.request("PUT", f"/booking/{booking_id}", booking)

    def partially_update_booking(self, booking_id: int, fields: dict[str, Any]) -> dict[str, Any]:
        return self.request("PATCH", f"/booking/{booking_id}", fields)

    def delete_booking(self, booking_id: int) -> dict[str, Any]:
        return self.request("DELETE", f"/booking/{booking_id}")

    def safe_delete_booking(self, booking_id: int, username: str, password: str) -> None:
        try:
            self.create_token(username, password)
            self.delete_booking(booking_id)
        except Exception as exc:
            self.logger.warning("teardown delete of booking %s failed: %s", booking_id, exc)

    def safe_delete_booking(self, booking_id: int, username: str, password: str) -> None:
        try:
            self.create_token(username, password)
        except Exception as exc:
            self.logger.warning("teardown token refresh failed: %s", exc)
            return
        try:
            self.delete_booking(booking_id)
        except Exception as exc:
            self.logger.warning("teardown delete failed: %s", exc)
