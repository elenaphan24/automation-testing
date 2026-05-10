from __future__ import annotations

from typing import Any

from business.actors.base_actor import BaseActor


class NewUser(BaseActor):
    @property
    def role(self) -> str:
        return "NewUser"

    def seed(self) -> dict[str, Any]:
        self.user = self.api.create_user(user_type="standard", balance=100)
        self.credentials = {"email": self.user["email"], "password": self.user["password"]}
        return self.credentials

    def teardown(self) -> None:
        if self.credentials:
            self.api.delete_user_by_email(self.credentials["email"])

