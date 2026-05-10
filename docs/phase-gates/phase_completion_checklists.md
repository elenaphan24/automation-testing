# Phase Completion Checklists

Every phase closes only after review, tests, and documentation updates are complete.

## Phase 0

- Architecture document merged.
- Test data strategy documented.
- Risk register populated with owners.
- `config/envs/` contains sandbox, staging, and production stubs.
- `core/config.py` loads and validates active environment config.
- Weeks 9-10 are reserved for documentation and sign-off.
- Phase done criteria exist for all later phases.

## Phase 1

- Three-layer folder structure is present.
- BasePage, BaseService, and structured logger are implemented.
- Allure output directory is configured from day one.
- JWT spike outcome is documented in ADR-001.
- Three PoC tests are present for API, UI, and E2E.
- Worker count is controlled through environment variables or pytest hook.

## Phase 2

- YAML/JSON data loader supports pytest parametrization.
- Excel adapter converts spreadsheets to YAML outside runtime tests.
- BaseActor contract enforces seed, teardown, and role.
- NewUser, VipUser, and Admin actors seed through API service objects.
- Journey runner attributes GIVEN, WHEN, THEN failures to layers.
- A complete Journey test runs from data to actor to assertion.

## Phase 3

- Parallel execution strategy is documented.
- Worker schema isolation is verified.
- Dockerfile builds a Playwright-capable test image.
- Azure Pipeline runs API before E2E and publishes Allure artifacts.
- Visual regression baseline process is documented.

## Phase 4

- `@playwright/mcp` and the Playwright CLI package are version-pinned.
- `CLAUDE.md` or equivalent agent instruction file is committed.
- AI quality gate checklist is present.
- Failure artifacts are exported after test failures.
- AI log analysis contract is documented with example input and output.

## Phase 5

- Five handoff guides are committed under `docs/guides/`.
- Independence test instructions are documented.
- Stakeholder demo narrative and report format are documented.
- Deferred backlog and sign-off checklist are recorded.
