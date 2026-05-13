# Test Pyramid Strategy

## Current State: Umbrella

The current suite leans on external UI and API systems because no internal SUT is available for component testing.

```text
        UI/E2E: 2 tests
      API/live: 5 tests
   Smoke/infra: 3 tests
Component/unit: 7 tests
```

Most business confidence still comes from tests that require live public systems. The unit tests cover framework configuration, but they do not yet represent the product behavior of an internal application.

## Target State: Hourglass

The target shape is an hourglass: strong component tests for framework and owned service logic, strong API tests for service behavior, and a small UI layer for happy-path E2E coverage.

```text
        UI/E2E: capped smoke journeys
      API/live: broad service behavior
   Contract/API: consumer-provider checks
Component/unit: broad core and business logic
```

## Counts Today

| Level | Current tests | Notes |
| --- | ---: | --- |
| Component/unit | 7 | `tests/unit/test_config.py` covers config behavior. |
| Infra | 2 | Worker schema isolation tests use the in-memory registry. |
| Smoke | 3 | Two offline config checks and one optional live API health check. |
| API | 5 | Restful Booker functional API tests, skipped unless live testing is enabled. |
| UI | 1 | SauceDemo login/inventory flow, skipped unless live testing is enabled. |
| E2E | 1 | SauceDemo purchase journey, skipped unless live testing is enabled. |

## Roadmap

1. Add component tests for `core/` modules beyond configuration: data loading, HTTP transport, logging, failure artifacts, and journey failure attribution.
2. Grow API coverage around owned services when an internal SUT is available.
3. Add contract tests when both service consumer and provider can participate.
4. Keep UI and E2E coverage focused on stable happy paths and do not grow it beyond the current role without an explicit risk decision.

## Why Not a Classic Pyramid Yet

A classic pyramid depends on an internal system where behavior can be tested below the UI. This repo currently targets public demo systems, so it cannot create meaningful service doubles, component tests, or provider-side contracts for the real product domain. Until an internal SUT exists, the framework documents the intended shape and keeps public-system tests clearly marked as live checks.
