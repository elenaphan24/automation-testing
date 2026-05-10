# Data and Actors

## YAML Data

Runtime test data belongs under `data/yaml/`.

```yaml
- name: vip_laptop_purchase
  amount: 125
  expected_balance: 375
```

Expose data to tests through `business.data.scenarios()` so test scripts do not import from `core`.

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

