from __future__ import annotations

import os
from pathlib import Path

import pytest

from business.data import scenarios


pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(
        os.getenv("SAUCEDEMO_LIVE") != "1",
        reason="Set SAUCEDEMO_LIVE=1 to run live SauceDemo E2E tests.",
    ),
]

SAUCEDEMO_SCENARIOS = scenarios(
    Path(__file__).resolve().parents[2] / "data/yaml/saucedemo_scenarios.yaml"
)


@pytest.mark.parametrize("scenario", SAUCEDEMO_SCENARIOS, ids=lambda item: item["name"])
def test_standard_user_can_buy_backpack(
    saucedemo_login_page,
    saucedemo_inventory_page,
    saucedemo_cart_page,
    saucedemo_checkout_page,
    scenario,
):
    checkout = scenario["checkout"]

    saucedemo_login_page.open()
    saucedemo_login_page.login(scenario["username"], scenario["password"])
    saucedemo_inventory_page.assert_opened()

    saucedemo_inventory_page.add_item_to_cart(scenario["item_name"])
    saucedemo_inventory_page.open_cart()
    saucedemo_cart_page.assert_has_item(scenario["item_name"])

    saucedemo_cart_page.checkout()
    saucedemo_checkout_page.fill_information(
        checkout["first_name"],
        checkout["last_name"],
        checkout["postal_code"],
    )
    saucedemo_checkout_page.finish()
    saucedemo_checkout_page.assert_order_complete()
