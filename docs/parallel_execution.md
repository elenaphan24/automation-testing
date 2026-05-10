# Parallel Execution Strategy

## Tooling

| Test type | Tool | Reason |
| --- | --- | --- |
| API and infra | `pytest-xdist` | Fast tests with low browser overhead |
| UI and E2E | `pytest-split` | Sharding avoids Playwright browser/context conflicts in large grids |

## Distribution

The default CI distribution mode for xdist is `--dist worksteal` because this framework mixes short API tests with longer E2E journeys.

## Fixture Scoping Audit

| Fixture | Scope | Reason |
| --- | --- | --- |
| `browser_page` | function | Fresh browser state per test |
| `worker_schema` | session | Isolated schema per worker |
| `user_service` | function | Fresh auth/service context per test |
| `fake_db` | session | Shared fake adapter behind isolated schemas |

## Conflict Detection

`tests/infra/test_parallel_isolation.py` verifies that each worker schema exists and starts with no user rows.

