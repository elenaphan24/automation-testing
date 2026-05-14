from __future__ import annotations

import os
from pathlib import Path

import pytest

from utils.data_loader import scenarios
from flows.saucedemo_checkout_flow import purchase_item


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
    purchase_item(
        saucedemo_login_page,
        saucedemo_inventory_page,
        saucedemo_cart_page,
        saucedemo_checkout_page,
        username=scenario["username"],
        password=scenario["password"],
        item_name=scenario["item_name"],
        first_name=checkout["first_name"],
        last_name=checkout["last_name"],
        postal_code=checkout["postal_code"],
    )
