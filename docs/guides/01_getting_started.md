# Getting Started

## Setup

```powershell
pip install -r requirements.txt
$env:ENV = "sandbox"
pytest tests/
```

## Fixture Dependency Flow

```text
pytest test
  |
  +-- restful_booker_service
  |     |
  |     +-- UrlLibTransport
  |
  +-- saucedemo_login_page
        |
        +-- live_browser_page
```

## Add a First API Test

Create a test under `tests/api/` and request a business-layer fixture such as `restful_booker_service`.

```python
def test_list_bookings(restful_booker_service):
    bookings = restful_booker_service.list_booking_ids()
    assert isinstance(bookings, list)
```

## Run Reports

pytest writes `reports/html_report.html` (single self-contained file) and `reports/junit.xml`. Open the HTML file in any browser.

## Troubleshooting

`ENV` not set:
The framework defaults to `sandbox`, so local runs do not require an `ENV` variable. Set `$env:ENV = "staging"` or `$env:ENV = "production"` only when intentionally switching environments.

`worker_id` fixture error:
The framework provides a `worker_id` fallback for non-xdist runs. If you see a fixture error, confirm `conftest.py` is being discovered from the repository root and run `pytest tests/` from the project directory.

