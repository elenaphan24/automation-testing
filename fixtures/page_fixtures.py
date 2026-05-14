from __future__ import annotations

import pytest

from business.pages.saucedemo_cart_page import SauceDemoCartPage
from business.pages.saucedemo_checkout_page import SauceDemoCheckoutPage
from business.pages.saucedemo_inventory_page import SauceDemoInventoryPage
from business.pages.saucedemo_login_page import SauceDemoLoginPage
from utils.data_factory import saucedemo_user


@pytest.fixture
def saucedemo_login_page(live_browser_page) -> SauceDemoLoginPage:
    return SauceDemoLoginPage(live_browser_page)


@pytest.fixture
def saucedemo_inventory_page(live_browser_page) -> SauceDemoInventoryPage:
    return SauceDemoInventoryPage(live_browser_page)


@pytest.fixture
def saucedemo_cart_page(live_browser_page) -> SauceDemoCartPage:
    return SauceDemoCartPage(live_browser_page)


@pytest.fixture
def saucedemo_checkout_page(live_browser_page) -> SauceDemoCheckoutPage:
    return SauceDemoCheckoutPage(live_browser_page)


@pytest.fixture
def locked_out_credentials() -> dict[str, str]:
    """Credentials for the SauceDemo locked-out user variant."""
    return saucedemo_user(username="locked_out_user")
