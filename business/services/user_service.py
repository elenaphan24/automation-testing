from __future__ import annotations

from typing import Any

from core.allure_compat import allure
from core.base_service import BaseService


class UserService(BaseService):
    @allure.step("Create user through API")
    def create_user(self, user_type: str = "standard", **overrides: Any) -> dict[str, Any]:
        payload = {"type": user_type, **overrides}
        return self.request("POST", "/users", payload)

    @allure.step("Promote user to VIP")
    def promote_to_vip(self, user_id: str) -> dict[str, Any]:
        return self.request("PATCH", f"/users/{user_id}/promote", {"tier": "vip"})

    @allure.step("Create API session")
    def create_session(self, email: str, password: str) -> dict[str, Any]:
        return self.request("POST", "/sessions", {"email": email, "password": password})

    @allure.step("Verify API session")
    def verify_session(self, token: str) -> None:
        session = self.request("GET", f"/sessions/{token}")
        self.assert_field(session, "active", True)

    @allure.step("Get user through API")
    def get_user(self, user_id: str) -> dict[str, Any]:
        return self.request("GET", f"/users/{user_id}")

    @allure.step("Record purchase through API")
    def record_purchase(self, user_id: str, amount: int) -> dict[str, Any]:
        return self.request("POST", f"/users/{user_id}/purchases", {"amount": amount})

    @allure.step("Assert user balance")
    def assert_balance(self, user_id: str, expected: int) -> None:
        user = self.get_user(user_id)
        self.assert_field(user, "balance", expected)

    @allure.step("Delete user through API")
    def delete_user_by_email(self, email: str) -> None:
        self.request("DELETE", f"/users/{email}")
