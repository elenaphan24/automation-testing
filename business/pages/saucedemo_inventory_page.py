from __future__ import annotations

from typing import Any

from core.base_page import BasePage
from core.config import get


class SauceDemoInventoryPage(BasePage):
    path = "/inventory.html"

    def __init__(self, page: Any) -> None:
        super().__init__(page)
        self.base_url = get("urls.saucedemo_base_url")

    def assert_opened(self) -> None:
        self.logger.info("assert SauceDemo inventory opened")
        self.page.wait_for_url("**/inventory.html")

    def assert_item_visible(self, item_name: str) -> None:
        self.logger.info("assert inventory item visible %s", item_name)
        self.page.locator(".inventory_item").filter(has_text=item_name).wait_for()

    def add_item_to_cart(self, item_name: str) -> None:
        self.logger.info("add inventory item to cart %s", item_name)
        item = self.page.locator(".inventory_item").filter(has_text=item_name)
        item.get_by_role("button", name="Add to cart").click()

    def open_cart(self) -> None:
        self.logger.info("open cart")
        self.page.locator(".shopping_cart_link").click()
