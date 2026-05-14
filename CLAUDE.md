# QA Framework Conventions for AI Agents

## Architecture Rules

- Four layers: Core Libraries -> Business Logic -> Flows -> Test Scripts.
- Test Scripts never import from Core Libraries directly.
- Test Scripts never import from Business Logic directly; they go through Flows or Fixtures.
- All UI actions go through `BasePage` subclasses in `business/pages/`.
- All API calls go through `BaseService` subclasses in `business/services/`.
- Multi-step business workflows (Given/When/Then sequences) belong in `flows/`; tests call flows, not raw service/page methods.
- All test fixtures (actors, preconditions, data injection) live in `fixtures/`; `conftest.py` imports and registers them — it does not define them.

## Generating New Code

- New page object: create in `business/pages/` and inherit from `BasePage`.
- New API service: create in `business/services/` and inherit from `BaseService`.
- New flow (multi-step workflow): create in `flows/` and compose page objects and services as plain functions.
- New fixture (actor, seeded data, cleanup): create in `fixtures/` as a dedicated module; register it in `conftest.py` via `pytest_plugins`.
- New test: create in `tests/e2e/`, `tests/api/`, `tests/ui/`, or `tests/smoke/`.
- Log meaningful actions through the `[UI]` / `[API]` / `[TAF]` logger; step-level tracking is logger-driven (no decorator-based step framework).
- Logs must use `[UI]`, `[API]`, or `[TAF]` layer tags through `get_logger`.

## Locator Priority

1. `getByRole()`
2. `getByLabel()` or `getByPlaceholder()`
3. `getByTestId()`
4. CSS selectors only as a last resort

## Test Data

- Runtime data lives in YAML or JSON under `data/yaml/`.
- Dynamic or parallel-safe data must use `utils/data_factory.py` (UUID-based generators).
- Do not hardcode test values when a scenario file or factory is appropriate.
- Excel files are import-time only and must be converted before test execution.

## Environment Config

- Use `core.config.get()` from Core or business-layer wrappers.
- Never hardcode URLs or secrets.
- `ENV` controls the active environment and defaults to `sandbox`.
- Use `npx playwright` for Playwright CLI commands; the old standalone `playwright-cli` package is deprecated.

## AI Review Gate

- Does the change follow the four-layer rule (Core -> Business -> Flows -> Tests)?
- Are fixtures defined in `fixtures/` and only registered in `conftest.py`?
- Are multi-step workflows in `flows/` rather than inlined in tests?
- Does it use resilient locators before CSS selectors?
- Are log statements layer-tagged?
- Is test data in YAML/JSON or generated via `data_factory` instead of hardcoded in tests?
- Does each business action emit a layer-tagged logger call?
- Does the PR say `AI-generated - reviewed by <name>` when applicable?
