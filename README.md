# QA Automation Framework

Pytest framework scaffold for multi-environment UI, API, and E2E automation. ISTQB CTAL-TAE aligned.

---

## Setup

```powershell
pip install -r requirements.txt
playwright install chromium
$env:ENV = "sandbox"
```

---

## Run Tests Locally

### All tests

```powershell
pytest tests/
```

### By folder/layer

```powershell
pytest tests/api/       # API tests
pytest tests/ui/        # UI / browser tests
pytest tests/e2e/       # E2E journey tests
pytest tests/smoke/     # Smoke tests
pytest tests/infra/     # Parallel isolation infra tests
pytest tests/unit/      # Unit tests
```

### By marker

```powershell
pytest -m smoke                       # smoke tests only
pytest -m api                         # API-marked tests
pytest -m ui                          # UI-marked tests
pytest -m e2e                         # E2E-marked tests
pytest -m regression                  # full regression suite
pytest -m "smoke and not quarantine"  # mirrors PR gate filter
```

### Switch environment

```powershell
$env:ENV = "staging"      # or "production" — default is sandbox
pytest tests/
```

### Parallel — API/infra (xdist)

```powershell
pytest tests/api/ tests/infra/ -n 4 --dist worksteal
```

### Parallel — UI/E2E (sharding)

```powershell
# Run shard 1 of 4
pytest tests/e2e/ tests/ui/ --splits 4 --group 1 --reruns 1 --reruns-delay 2
```

---

## Opt-In Live Tests

### Restful Booker API

```powershell
$env:RESTFUL_BOOKER_LIVE = "1"
python -m pytest tests/api/test_restful_booker_api.py
```

API docs: https://restful-booker.herokuapp.com/apidoc/index.html#api-Auth

Live tests create temporary bookings and delete them during cleanup.

### SauceDemo UI / E2E

```powershell
$env:SAUCEDEMO_LIVE = "1"
python -m pytest tests/ui/test_saucedemo_ui.py
python -m pytest tests/e2e/test_saucedemo_e2e.py
```

Watch the browser (non-headless):

```powershell
$env:LIVE_HEADLESS = "0"
```

---

## Reports

After any run, output is written to:

| Path | Format |
|---|---|
| `reports/html_report.html` | Self-contained HTML (open in browser) |
| `reports/junit.xml` | JUnit XML |
| `reports/coverage/` | HTML coverage report |

---

## CI/CD Pipeline (`azure-pipelines.yml`)

### Triggers

| Trigger | Condition |
|---|---|
| PR gate | Any PR targeting `main` (excludes `*.md`, `docs/**`) |
| Push | Push to `main` |
| Nightly | Mon–Fri 02:00 UTC (`0 2 * * 1-5`) |

### Stage order

```
StaticChecks → APITests → E2ETests
```

### Stage 1 — StaticChecks

```bash
python tools/lint_no_runtime_pandas.py   # enforce Excel adapter boundary
```

### Stage 2 — APITests

Runs after StaticChecks. On PR, filter is `smoke and not quarantine`.

```bash
pytest tests/api/ tests/infra/ \
  -x -n 4 --dist worksteal \
  --cov=core --cov=business \
  --cov-fail-under=55 \
  --cov-report=xml:coverage.xml \
  --html=report.html --self-contained-html \
  --junitxml=junit-api.xml
```

Quality gates: coverage >= 55%, pass rate >= 90%.

### Stage 3 — E2ETests

Runs after APITests. Splits across 4 parallel shards. On PR, filter is `smoke and not quarantine`.

```bash
# Per shard (SHARD_GROUP = 1..4)
pytest tests/e2e/ tests/ui/ \
  --splits 4 --group $SHARD_GROUP \
  --reruns 1 --reruns-delay 2 \
  --html=report.html --self-contained-html \
  --junitxml=junit-e2e-$SHARD_GROUP.xml
```

### Key pipeline variables

| Variable | Default |
|---|---|
| `ENV` | `sandbox` |
| `CI_WORKER_COUNT` | `4` |
| `SHARD_COUNT` | `4` |

---

## Visual Baselines (Docker)

Generate and approve baselines only inside the Docker image to avoid OS rendering drift:

```powershell
docker build -t qa-framework .
docker run --rm -e ENV=sandbox qa-framework pytest tests/ui/
```

Never regenerate baselines against production.
