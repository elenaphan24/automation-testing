from __future__ import annotations

from core.allure_compat import allure
from core.base_page import BasePage


class CheckoutPage(BasePage):
    path = "/checkout"

    @allure.step("Buy laptop through UI")
    def buy_laptop(self, amount: int) -> dict[str, int | str]:
        self.goto(self.path)
        # Real Playwright: self.page.get_by_label("Amount").fill(str(amount))
        self.fill("[data-testid=amount]", str(amount))  # FakeSUT fallback
        # Real Playwright: self.page.get_by_role("button", name="Buy laptop").click()
        self.click("[data-testid=buy-laptop]")  # FakeSUT fallback
        if callable(getattr(self.page, "purchase_handler", None)):
            self.page.purchase_handler(amount)
        return {"item": "laptop", "amount": amount}
