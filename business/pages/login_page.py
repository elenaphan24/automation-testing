from __future__ import annotations

from core.base_page import BasePage


class LoginPage(BasePage):
    path = "/login"

    def open(self) -> None:
        self.goto(self.path)

    def login(self, email: str, password: str) -> None:
        # Real Playwright: self.page.get_by_label("Email").fill(email)
        self.fill("[data-testid=email]", email)  # FakeSUT fallback
        # Real Playwright: self.page.get_by_label("Password").fill(password)
        self.fill("[data-testid=password]", password)  # FakeSUT fallback
        # Real Playwright: self.page.get_by_role("button", name="Log in").click()
        self.click("[data-testid=login-submit]")  # FakeSUT fallback

    def assert_title_contains(self, expected: str) -> None:
        actual = self.page.title()
        self.logger.info("assert title contains %s", expected)
        assert expected in actual
