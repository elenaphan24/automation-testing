import pytest

from business.actors.vip_user import VipUser
from business.data import scenarios
from business.journeys import Journey
from business.pages.checkout_page import CheckoutPage


pytestmark = pytest.mark.e2e


@pytest.mark.parametrize("scenario", scenarios("data/yaml/transfer_scenarios.yaml"))
def test_vip_checkout_journey(scenario, user_service, worker_schema, browser_page):
    actor = VipUser(user_service, worker_schema)
    checkout_page = CheckoutPage(browser_page)

    try:
        journey = Journey().given(actor)
        browser_page.purchase_handler = lambda amount: user_service.record_purchase(actor.user["id"], amount)
        journey.when(checkout_page.buy_laptop, amount=scenario["amount"]).then(
            user_service.assert_balance,
            actor.user["id"],
            scenario["expected_balance"],
        )
    finally:
        actor.teardown()
