from __future__ import annotations

from core.allure_compat import allure
from core.base_page import BasePage


class LoginPage(BasePage):
    path = "/login"

    @allure.step("Open login page")
    def open(self) -> None:
        self.goto(self.path)

    @allure.step("Login through UI")
    def login(self, email: str, password: str) -> None:
        self.fill("[data-testid=email]", email)
        self.fill("[data-testid=password]", password)
        self.click("[data-testid=login-submit]")

    @allure.step("Verify login page title")
    def assert_title_contains(self, expected: str) -> None:
        actual = self.page.title()
        self.logger.info("assert title contains %s", expected)
        assert expected in actual

