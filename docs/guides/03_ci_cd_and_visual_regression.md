# CI/CD and Visual Regression

## Pipeline Shape

Azure Pipelines runs:

1. Static import-policy checks.
2. API and infra tests with `pytest-xdist --dist worksteal`.
3. UI and E2E tests with `pytest-split`.
4. Allure artifact publishing.

## Visual Baselines

Generate baselines only inside the Docker image:

```powershell
docker build -t qa-framework .
docker run --rm -e ENV=sandbox qa-framework pytest tests/ui/
```

Approve visual diffs only after reviewing CI artifacts. Production must never update baselines.

