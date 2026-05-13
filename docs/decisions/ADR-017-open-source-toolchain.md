# ADR-017: Open-Source Toolchain

## Status

Accepted

## Context

The automation framework needs a maintainable, inspectable toolchain with low adoption friction and no license dependency.

## Decision

Use open-source tools for the core test stack:

| Tool | Purpose |
| --- | --- |
| pytest | Test runner and fixture model |
| Playwright | Browser automation |
| pytest-xdist | Parallel execution |
| pytest-split | E2E sharding |
| pytest-html | Human-readable HTML reports |
| pytest-cov | Code coverage reporting |
| PyYAML | YAML scenario and config data |

## Rationale

The selected stack has zero license cost, broad community support, CI-friendly operation, and no vendor lock-in. It also keeps the framework easy to inspect and extend by engineers who already know Python tooling.

## Maintenance Model

Dependencies are version-bounded in `requirements.txt`. Dependency update automation such as Dependabot should propose upgrades, and each upgrade must run the offline test suite plus any enabled live smoke tests before merge.

## Risks

Open-source tools can introduce breaking changes without a commercial SLA. Version bounds, CI validation, and ADR review reduce that risk.
