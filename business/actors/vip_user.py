from __future__ import annotations

from typing import Any

from business.actors.base_actor import BaseActor


class VipUser(BaseActor):
    starting_balance = 500

    @property
    def role(self) -> str:
        return "VipUser"

    def seed(self) -> dict[str, Any]:
        self.user = self.api.create_user(user_type="standard", balance=self.starting_balance)
        self.user = self.api.promote_to_vip(self.user["id"])
        self.credentials = {"email": self.user["email"], "password": self.user["password"]}
        return self.credentials

    def teardown(self) -> None:
        if self.credentials:
            self.api.delete_user_by_email(self.credentials["email"])

