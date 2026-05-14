from __future__ import annotations

import os
from pathlib import Path

import pytest

from utils.data_loader import scenarios
from flows.saucedemo_checkout_flow import locked_out_login_flow, login_to_inventory


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
    login_to_inventory(
        saucedemo_login_page,
        saucedemo_inventory_page,
        username=scenario["username"],
        password=scenario["password"],
    )
    saucedemo_inventory_page.assert_item_visible(scenario["item_name"])


def test_locked_out_user_cannot_login(saucedemo_login_page, locked_out_credentials):
    locked_out_login_flow(
        saucedemo_login_page,
        username=locked_out_credentials["username"],
        password=locked_out_credentials["password"],
    )
