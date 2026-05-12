from __future__ import annotations

import os
from pathlib import Path

import pytest

from business.data import scenarios


pytestmark = [
    pytest.mark.ui,
    pytest.mark.skipif(
        os.getenv("SAUCEDEMO_LIVE") != "1",
        reason="Set SAUCEDEMO_LIVE=1 to run live SauceDemo UI tests.",
    ),
]

SAUCEDEMO_SCENARIOS = scenarios(
    Path(__file__).resolve().parents[2] / "data/yaml/saucedemo_scenarios.yaml"
)


@pytest.mark.parametrize("scenario", SAUCEDEMO_SCENARIOS, ids=lambda item: item["name"])
def test_standard_user_can_login_and_view_inventory(
    saucedemo_login_page, saucedemo_inventory_page, scenario
):
    saucedemo_login_page.open()
    saucedemo_login_page.login(scenario["username"], scenario["password"])

    saucedemo_inventory_page.assert_opened()
    saucedemo_inventory_page.assert_item_visible(scenario["item_name"])
