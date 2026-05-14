from __future__ import annotations

from business.pages.saucedemo_cart_page import SauceDemoCartPage
from business.pages.saucedemo_checkout_page import SauceDemoCheckoutPage
from business.pages.saucedemo_inventory_page import SauceDemoInventoryPage
from business.pages.saucedemo_login_page import SauceDemoLoginPage

_LOCKED_OUT_ERROR = "Epic sadface: Sorry, this user has been locked out."


def locked_out_login_flow(
    login_page: SauceDemoLoginPage,
    *,
    username: str,
    password: str,
) -> None:
    """Attempts login with locked-out credentials and asserts the error banner appears."""
    login_page.open()
    login_page.login(username, password)
    login_page.assert_login_error(_LOCKED_OUT_ERROR)


def login_to_inventory(
    login_page: SauceDemoLoginPage,
    inventory_page: SauceDemoInventoryPage,
    *,
    username: str,
    password: str,
) -> None:
    """Logs in and asserts the inventory page is open."""
    login_page.open()
    login_page.login(username, password)
    inventory_page.assert_opened()


def purchase_item(
    login_page: SauceDemoLoginPage,
    inventory_page: SauceDemoInventoryPage,
    cart_page: SauceDemoCartPage,
    checkout_page: SauceDemoCheckoutPage,
    *,
    username: str,
    password: str,
    item_name: str,
    first_name: str,
    last_name: str,
    postal_code: str,
) -> None:
    """Full SauceDemo purchase flow: login → add to cart → checkout → confirm."""
    login_page.open()
    login_page.login(username, password)
    inventory_page.assert_opened()

    inventory_page.add_item_to_cart(item_name)
    inventory_page.open_cart()
    cart_page.assert_has_item(item_name)

    cart_page.checkout()
    checkout_page.fill_information(first_name, last_name, postal_code)
    checkout_page.finish()
    checkout_page.assert_order_complete()
