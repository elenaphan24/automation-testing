from __future__ import annotations

from typing import Any

from core.base_page import BasePage
from core.config import get


class SauceDemoLoginPage(BasePage):
    path = "/"

    def __init__(self, page: Any) -> None:
        super().__init__(page)
        self.base_url = get("urls.saucedemo_base_url")

    def open(self) -> None:
        self.goto(self.path)

    def login(self, username: str, password: str) -> None:
        self.logger.info("login SauceDemo user %s", username)
        self.page.get_by_placeholder("Username").fill(username)
        self.page.get_by_placeholder("Password").fill(password)
        self.page.get_by_role("button", name="Login").click()
