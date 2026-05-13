# Data and Preconditions

## YAML Data

Runtime test data belongs under `data/yaml/`.

```yaml
- name: vip_laptop_purchase
  amount: 125
  expected_balance: 375
```

Expose data to tests through `business.data.scenarios()` so test scripts do not import from `core`.

## Current Precondition Pattern

The actor layer was removed in `54b7258` because the current SUTs do not expose a stable user-management API. Test preconditions now live in fixtures or in the test body, using the business service object that owns the API calls.

Use `business.services.restful_booker_service.RestfulBookerService` as the current pattern: create the record needed for the scenario, run the assertions, and clean up in `finally` so failed assertions do not leave test data behind.

```python
def test_create_booking_then_read(restful_booker_service, scenario):
    created = restful_booker_service.create_booking(scenario["booking"])
    booking_id = created["bookingid"]

    try:
        booking = restful_booker_service.get_booking(booking_id)
        assert booking["firstname"] == scenario["booking"]["firstname"]
    finally:
        restful_booker_service.safe_delete_booking(
            booking_id,
            scenario["username"],
            scenario["password"],
        )
```

When a future SUT exposes user or account management APIs, reintroduce actor abstractions from the deferred backlog only after they remove duplication across real fixtures.

## Excel Adapter

Spreadsheet files belong under `data/excel/` and are converted before runtime:

```powershell
python -c "from core.excel_adapter import excel_to_yaml; excel_to_yaml('data/excel/input.xlsx', 'data/yaml/output.yaml')"
```

## Add Preconditions

Prefer one of these patterns:

- For one-off API setup, create and clean up in the test body with `try/finally`.
- For shared setup, add a fixture in `conftest.py` that yields the prepared object and performs cleanup after the yield.
- Do not seed through UI flows unless the UI flow itself is the behavior under test.

