# ADR-013: Worksteal Distribution

Status: Accepted

Context: The suite mixes fast API tests with slower UI and E2E journeys.

Decision: API and infra tests use pytest-xdist with `--dist worksteal` in CI.

Consequences: Idle workers can take remaining tests from busy workers, improving utilization for mixed-duration suites.

