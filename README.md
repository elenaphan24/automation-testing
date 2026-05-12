# QA Automation Framework

Pytest framework scaffold for multi-environment UI, API, and E2E automation.

## Quick Start

```powershell
pip install -r requirements.txt
$env:ENV = "sandbox"
pytest tests/
```

The default environment is `sandbox`. Configuration lives in `config/envs/` and is loaded through `core.config`.

## Restful Booker Live API Demo

The repository includes opt-in API tests for the Restful Booker spec:

- API docs: https://restful-booker.herokuapp.com/apidoc/index.html#api-Auth

```powershell
$env:RESTFUL_BOOKER_LIVE = "1"
python -m pytest tests/api/test_restful_booker_api.py
```

The live tests create temporary bookings and delete them during cleanup.

## SauceDemo Live UI/E2E Demo

The repository includes opt-in SauceDemo examples for `standard_user`:

```powershell
$env:SAUCEDEMO_LIVE = "1"
python -m pytest tests/ui/test_saucedemo_ui.py
python -m pytest tests/e2e/test_saucedemo_e2e.py
```

Set `$env:LIVE_HEADLESS = "0"` to watch the browser run.

Follow ISTQB CTAL-TAE aligned 
