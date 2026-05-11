# Getting Started

## Setup

```powershell
pip install -r requirements.txt
$env:ENV = "sandbox"
pytest tests/
```

Install the Allure CLI if you want to view HTML reports locally:

```powershell
npm install -g allure-commandline
```

## Fixture Dependency Flow

```text
pytest test
  |
  +-- user_service
  |     |
  |     +-- api_transport
  |           |
  |           +-- worker_schema
  |                 |
  |                 +-- fake_db
  |
  +-- login_page
        |
        +-- browser_page
```

## Add a First API Test

Create a test under `tests/api/` and request a business-layer fixture such as `user_service`.

```python
def test_create_basic_user(user_service):
    user = user_service.create_user(email="new-user@example.test")
    assert user["email"] == "new-user@example.test"
```

## Run Reports

Allure result files are written to `reports/allure-results`. Generate the HTML report with your local Allure CLI:

```powershell
allure serve reports/allure-results
```

## Troubleshooting

`ENV` not set:
The framework defaults to `sandbox`, so local runs do not require an `ENV` variable. Set `$env:ENV = "staging"` or `$env:ENV = "production"` only when intentionally switching environments.

Missing Allure CLI:
If `allure serve reports/allure-results` is not recognized, install it with `npm install -g allure-commandline`. Pytest still writes raw Allure result files even when the CLI is missing.

`worker_id` fixture error:
The framework provides a `worker_id` fallback for non-xdist runs. If you see a fixture error, confirm `conftest.py` is being discovered from the repository root and run `pytest tests/` from the project directory.

