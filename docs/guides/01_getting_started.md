# Getting Started

## Setup

```powershell
pip install -r requirements.txt
$env:ENV = "sandbox"
pytest tests/
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

