# CI/CD and Visual Regression

## Pipeline Shape

Azure Pipelines runs:

1. Static import-policy checks.
2. API and infra tests with `pytest-xdist --dist worksteal`.
3. UI and E2E tests with `pytest-split`.
4. pytest-html artifact publishing.

## Visual Baselines

Generate baselines only inside the Docker image:

```powershell
docker build -t qa-framework .
docker run --rm -e ENV=sandbox qa-framework pytest tests/ui/
```

Approve visual diffs only after reviewing CI artifacts. Production must never update baselines.

## Why Baselines Differ

If a visual baseline passes locally but fails in CI, the usual cause is operating-system rendering drift: font rasterization, browser dependencies, GPU settings, and image libraries can all differ between a laptop and the hosted build agent. Regenerate and approve baselines only inside the Docker image so the same rendering stack is used for local review and CI.

## Failure Screenshots

With the fake page object, screenshots taken through `BasePage.screenshot()` are stored on the pytest node and embedded in the pytest-html report when the test fails. When real Playwright is wired, add an autouse fixture that calls `page.screenshot()` on failure so the same failure hook can embed the captured image.


