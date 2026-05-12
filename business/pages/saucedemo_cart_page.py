from __future__ import annotations

from typing import Any

from core.base_page import BasePage
from core.config import get


class SauceDemoCartPage(BasePage):
    path = "/cart.html"

    def __init__(self, page: Any) -> None:
        super().__init__(page)
        self.base_url = get("urls.saucedemo_base_url")

    def assert_has_item(self, item_name: str) -> None:
        self.logger.info("assert cart has item %s", item_name)
        self.page.locator(".cart_item").filter(has_text=item_name).wait_for()

    def checkout(self) -> None:
        self.logger.info("start checkout")
        self.page.get_by_role("button", name="Checkout").click()
