# Test & CI/CD Command Reference

## 1. Setup

```powershell
pip install -r requirements.txt
playwright install chromium
```

---

## 2. Environment Variables

| Variable | Values | Default | Notes |
|---|---|---|---|
| `ENV` | `sandbox` / `staging` / `production` | `sandbox` | Controls config from `config/envs/` |
| `RESTFUL_BOOKER_LIVE` | `1` | off | Opt-in: runs live Restful Booker API tests |
| `SAUCEDEMO_LIVE` | `1` | off | Opt-in: runs live SauceDemo UI/E2E tests |
| `LIVE_HEADLESS` | `0` | `1` | Set to `0` to watch the browser run |

```powershell
$env:ENV = "sandbox"       # default — not required locally
$env:ENV = "staging"       # QA lead / CI only
$env:ENV = "production"    # CI only; enforces smoke-only guard
```

---

## 3. Run All Tests

```powershell
pytest tests/
```

---

## 4. Run by Test Suite (folder)

```powershell
pytest tests/api/           # API service tests
pytest tests/ui/            # Browser / page-object tests
pytest tests/e2e/           # Hybrid UI+API journey tests
pytest tests/smoke/         # Production-safe read-only smoke tests
pytest tests/infra/         # Parallel isolation / infrastructure checks
pytest tests/unit/          # Unit tests (config, utilities)
```

---

## 5. Run by Marker

```powershell
pytest tests/ -m smoke
pytest tests/ -m api
pytest tests/ -m ui
pytest tests/ -m e2e
pytest tests/ -m regression
pytest tests/ -m "smoke and not quarantine"   # CI PR filter
```

> Quarantined tests (known-unstable) are excluded from the main CI run via `not quarantine`.

---

## 6. Run Specific Test Files

```powershell
python -m pytest tests/api/test_restful_booker_api.py
python -m pytest tests/ui/test_saucedemo_ui.py
python -m pytest tests/e2e/test_saucedemo_e2e.py
```

---

## 7. Opt-in Live Tests

### Restful Booker (creates + deletes real bookings)
```powershell
$env:RESTFUL_BOOKER_LIVE = "1"
python -m pytest tests/api/test_restful_booker_api.py
```

### SauceDemo UI + E2E
```powershell
$env:SAUCEDEMO_LIVE = "1"
python -m pytest tests/ui/test_saucedemo_ui.py
python -m pytest tests/e2e/test_saucedemo_e2e.py
```

### Watch the browser (non-headless)
```powershell
$env:LIVE_HEADLESS = "0"
```

---

## 8. Parallel Execution (local)

### API / infra — xdist worksteal
```powershell
pytest tests/api/ tests/infra/ -n 4 --dist worksteal
```

### UI / E2E — sharded (4 shards example)
```powershell
pytest tests/e2e/ tests/ui/ --splits 4 --group 1   # run shard 1
pytest tests/e2e/ tests/ui/ --splits 4 --group 2   # run shard 2
# ...repeat for groups 3 and 4
```

---

## 9. Coverage

```powershell
# Coverage report is generated automatically via pytest.ini addopts.
# Outputs: reports/coverage/ (HTML) and terminal missing-lines summary.
# CI enforces --cov-fail-under=55
pytest tests/api/ tests/infra/ --cov=core --cov=business --cov-fail-under=55
```

---

## 10. Static Checks

```powershell
# Enforces Excel/pandas import-boundary rule (no runtime pandas imports)
python tools/lint_no_runtime_pandas.py
```

---

## 11. Reports

After any `pytest` run:

| Report | Path |
|---|---|
| HTML report | `reports/html_report.html` |
| JUnit XML | `reports/junit.xml` |
| Coverage HTML | `reports/coverage/` |

Open `reports/html_report.html` in any browser.

---

## 12. Docker — Visual Baselines (CI-consistent rendering)

```powershell
docker build -t qa-framework .
docker run --rm -e ENV=sandbox qa-framework pytest tests/ui/
```

> Always regenerate and approve visual baselines inside Docker to avoid OS rendering drift between laptop and CI agent.

---

## 13. CI/CD — Azure Pipelines (`azure-pipelines.yml`)

### Triggers

| Event | Branch | Condition |
|---|---|---|
| Push | `main` | Always (excludes `*.md`, `docs/**`) |
| Pull Request | `main` | Always (excludes `*.md`, `docs/**`) |
| Nightly schedule | `main` | Mon–Fri at 02:00 UTC (`0 2 * * 1-5`) |

### Pipeline Stages (sequential)

```
StaticChecks  →  APITests  →  E2ETests
```

#### Stage 1 — StaticChecks
```bash
pip install -r requirements.txt
python tools/lint_no_runtime_pandas.py
```

#### Stage 2 — APITests (xdist, 4 workers)
```bash
# Full run (push / nightly):
pytest tests/api/ tests/infra/ \
  -x -n 4 --dist worksteal \
  --cov=core --cov=business --cov-fail-under=55 \
  --cov-report=xml:coverage.xml \
  --html=report.html --self-contained-html \
  --junitxml=junit-api.xml

# PR run (smoke only):
pytest tests/api/ tests/infra/ ... -m "smoke and not quarantine"
```
Quality gate: pass rate must be **≥ 90%** (inline Python check post-run).

#### Stage 3 — E2ETests (4 parallel shards × 1 rerun)
```bash
# Each shard runs independently (matrix: shard_1..shard_4):
playwright install chromium
pytest tests/e2e/ tests/ui/ \
  --splits 4 --group <SHARD_GROUP> \
  --reruns 1 --reruns-delay 2 \
  --html=report.html --self-contained-html \
  --junitxml=junit-e2e-<SHARD_GROUP>.xml

# PR run (smoke only):
pytest tests/e2e/ tests/ui/ ... -m "smoke and not quarantine"
```

### CI Environment Constraints

| Environment | Who | Test scope | Max workers |
|---|---|---|---|
| `sandbox` | All team | Full suite | 8 |
| `staging` | CI / QA lead | Full suite | 4 |
| `production` | CI only | `smoke` only | 1 (sequential) |

### CI Artifacts Published

| Artifact | Content |
|---|---|
| `html-api` | HTML report from API stage |
| `html-e2e-1..4` | HTML report from each E2E shard |
| JUnit XML | Test results (shown in Azure Pipelines Tests tab) |
| Coverage XML | Code coverage summary |
