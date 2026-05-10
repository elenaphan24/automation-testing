# ADR-001: JWT Injection Spike

Status: Proposed fallback documented

## Context

The plan requires a controllability spike before E2E journeys depend on session injection. This scaffold has no real SUT yet, so the spike cannot validate browser storage, CSRF behavior, token TTL, or session binding against a live app.

## Decision

Use fast UI login as the default Phase 1 fallback in the scaffold. When the sandbox SUT is available, run `spike/jwt_injection_spike.py` to replace this placeholder with a real result:

- `WORKS`: inject JWT into Playwright BrowserContext.
- `PARTIAL`: inject where supported and use UI login elsewhere.
- `BLOCKED`: keep cached-credential UI login as the primary path.

## Consequences

E2E PoC tests remain valid because they exercise API-created users, UI login behavior, and API session verification through business-layer objects.

