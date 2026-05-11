import pytest

from business.actors.vip_user import VipUser
from business.data import scenarios
from business.journeys import Journey
from business.pages.checkout_page import CheckoutPage


pytestmark = pytest.mark.e2e


@pytest.fixture
def vip_actor(user_service, worker_schema):
    actor = VipUser(user_service, worker_schema)
    yield actor
    actor.teardown()


@pytest.mark.parametrize("scenario", scenarios("data/yaml/transfer_scenarios.yaml"))
def test_vip_checkout_journey(scenario, vip_actor, user_service, browser_page):
    checkout_page = CheckoutPage(browser_page)

    vip_actor.starting_balance = scenario["starting_balance"]
    journey = Journey().given(vip_actor)
    browser_page.purchase_handler = lambda amount: user_service.record_purchase(vip_actor.user["id"], amount)
    journey.when(checkout_page.buy_laptop, amount=scenario["amount"]).then(
        user_service.assert_balance,
        vip_actor.user["id"],
        scenario["expected_balance"],
    )
