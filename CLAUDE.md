# QA Framework Conventions for AI Agents

## Architecture Rules

- Three layers: Core Libraries -> Business Logic -> Test Scripts.
- Test Scripts never import from Core Libraries directly.
- All UI actions go through `BasePage` subclasses in `business/pages/`.
- All API calls go through `BaseService` subclasses in `business/services/`.

## Generating New Code

- New page object: create in `business/pages/` and inherit from `BasePage`.
- New API service: create in `business/services/` and inherit from `BaseService`.
- New test: create in `tests/e2e/`, `tests/api/`, `tests/ui/`, or `tests/smoke/`.
- New Actor: inherit from `BaseActor`, implement `seed()`, `teardown()`, and `role`.
- Log meaningful actions through the `[UI]` / `[API]` / `[TAF]` logger; step-level tracking is logger-driven (no decorator-based step framework).
- Logs must use `[UI]`, `[API]`, or `[TAF]` layer tags through `get_logger`.

## Locator Priority

1. `getByRole()`
2. `getByLabel()` or `getByPlaceholder()`
3. `getByTestId()`
4. CSS selectors only as a last resort

## Test Data

- Runtime data lives in YAML or JSON under `data/yaml/`.
- Do not hardcode test values when a scenario file is appropriate.
- Excel files are import-time only and must be converted before test execution.

## Environment Config

- Use `core.config.get()` from Core or business-layer wrappers.
- Never hardcode URLs or secrets.
- `ENV` controls the active environment and defaults to `sandbox`.
- Use `npx playwright` for Playwright CLI commands; the old standalone `playwright-cli` package is deprecated.

## AI Review Gate

- Does the change follow the three-layer rule?
- Does it use resilient locators before CSS selectors?
- Are log statements layer-tagged?
- Is test data in YAML/JSON instead of hardcoded in tests?
- Does each business action emit a layer-tagged logger call?
- Does the PR say `AI-generated - reviewed by <name>` when applicable?
