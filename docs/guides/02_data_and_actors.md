# Data and Actors

## YAML Data

Runtime test data belongs under `data/yaml/`.

```yaml
- name: vip_laptop_purchase
  amount: 125
  expected_balance: 375
```

Expose data to tests through `business.data.scenarios()` so test scripts do not import from `core`.

## Worked Example: Adding a PremiumUser Actor

Walk through every layer for a new Actor that gets a higher starting balance and an extra perk credit. This is a reference pattern for teams wiring a real user-management service behind `BaseActor`.

1. Add YAML scenario data at `data/yaml/premium_scenarios.yaml`:

```yaml
- name: premium_perk_purchase
  starting_balance: 1000
  perk_credit: 50
  amount: 200
  expected_balance: 850
```

2. Create `business/actors/premium_user.py`:

```python
from business.actors.base_actor import BaseActor


class PremiumUser(BaseActor):
    starting_balance = 1000
    perk_credit = 50

    @property
    def role(self) -> str:
        return "PremiumUser"

    def seed(self):
        self.user = self.api.create_user(
            user_type="premium",
            balance=self.starting_balance + self.perk_credit,
        )
        self.credentials = {
            "email": self.user["email"],
            "password": self.user["password"],
        }
        return self.credentials

    def teardown(self):
        if self.credentials:
            self.api.delete_user_by_email(self.credentials["email"])
```

3. Add a fixture in your test file or `conftest.py`:

```python
@pytest.fixture
def premium_actor(api_service, worker_schema):
    actor = PremiumUser(api_service, worker_schema)
    yield actor
    actor.teardown()
```

4. Add a journey test at `tests/e2e/test_premium_journey.py`:

```python
@pytest.mark.parametrize(
    "scenario",
    scenarios("data/yaml/premium_scenarios.yaml"),
)
def test_premium_perk_purchase(scenario, premium_actor, checkout_flow, api_service):
    premium_actor.starting_balance = scenario["starting_balance"]
    premium_actor.perk_credit = scenario["perk_credit"]
    journey = Journey().given(premium_actor)
    journey.when(checkout_flow.buy_laptop, amount=scenario["amount"]).then(
        api_service.assert_balance,
        premium_actor.user["id"],
        scenario["expected_balance"],
    )
```

5. Run the focused journey:

```powershell
pytest tests/e2e/test_premium_journey.py -q
```

`checkout_flow` is the team's real business-layer checkout facade. The same five-step pattern applies to any new Actor: data, actor class, fixture, test, run.

## Excel Adapter

Spreadsheet files belong under `data/excel/` and are converted before runtime:

```powershell
python -c "from core.excel_adapter import excel_to_yaml; excel_to_yaml('data/excel/input.xlsx', 'data/yaml/output.yaml')"
```

## Add an Actor

Create a class under `business/actors/` that inherits `BaseActor` and implements:

- `role`
- `seed()`
- `teardown()`

Use API services for setup and cleanup. Do not seed through UI flows.

