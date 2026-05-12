from __future__ import annotations

from typing import Any

from core.base_page import BasePage
from core.config import get


class SauceDemoCheckoutPage(BasePage):
    path = "/checkout-step-one.html"

    def __init__(self, page: Any) -> None:
        super().__init__(page)
        self.base_url = get("urls.saucedemo_base_url")

    def fill_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.logger.info("fill checkout information")
        self.page.get_by_placeholder("First Name").fill(first_name)
        self.page.get_by_placeholder("Last Name").fill(last_name)
        self.page.get_by_placeholder("Zip/Postal Code").fill(postal_code)
        self.page.get_by_role("button", name="Continue").click()

    def finish(self) -> None:
        self.logger.info("finish checkout")
        self.page.get_by_role("button", name="Finish").click()

    def assert_order_complete(self) -> None:
        self.logger.info("assert order complete")
        self.page.get_by_role("heading", name="Thank you for your order!").wait_for()
