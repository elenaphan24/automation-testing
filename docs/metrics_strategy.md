# Metrics Strategy

The framework tracks metrics that can be derived from JUnit XML, CI artifacts, and lightweight manual classification.

| Metric | Collection source | Reviewer | Action trigger |
| --- | --- | --- | --- |
| Pass-fail ratio per stage per sprint | JUnit XML from API and E2E stages | QA Lead | Investigate when pass rate drops below 90%. |
| Test execution time trend | JUnit XML duration plus CI stage timing | CI Engineer | Optimize or shard when trend exceeds the sprint baseline by 20%. |
| Ratio of failures to unique defects | Failed test count mapped to confirmed defect IDs | QA Lead | Reduce flaky or duplicate failures when ratio stays above 2:1. |
| Functional coverage percent | Manual scenario count compared with YAML-backed automated scenarios | TAE Lead | Add or defer tests when automated coverage misses committed regression scope. |
| Code coverage percent | `pytest-cov` reports for `core/` and `business/` | TAE Lead | Raise targeted unit coverage when coverage falls below the current threshold. |

## Review Cadence

Metrics are reviewed once per sprint during quality review. The CI Engineer owns artifact availability, the TAE Lead owns interpretation for automation health, and the QA Lead owns stakeholder communication.

## Incremental Targets

The initial CI thresholds are intentionally conservative: 60% code coverage for the covered layers and 90% pass rate for API/infra stage tests. Raise these thresholds only after the suite is stable for at least one sprint.
