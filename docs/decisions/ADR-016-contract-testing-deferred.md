# ADR-016: Contract Testing Deferred

## Status

Deferred

## Context

ISTQB CT-TAS section 3.1.1 expects the automation strategy to consider contract testing between service consumers and providers. The current framework exercises public demonstration systems only:

- Restful Booker is a public API with no provider-side Pact broker available to this project.
- SauceDemo is a public UI application with no API layer available to contract against.

Without ownership of both consumer and provider, contract tests would become shallow schema checks rather than executable consumer-provider agreements.

## Decision

Contract testing is not implemented in the current scope.

When an internal microservice SUT is onboarded, add Pact Python and create `tests/contract/` for consumer contracts. Restful Booker API tests remain functional API validation in the meantime.

## Consequences

API schema drift and integration defects are caught at the API test level, not at contract verification time. This is acceptable for the current public-API-only scope, but it must be revisited before the framework is used for owned service ecosystems.
