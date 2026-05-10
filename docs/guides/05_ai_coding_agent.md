# AI Coding Agent

## Context Files

AI agents should read:

- `CLAUDE.md`
- `docs/architecture/architecture.md`
- `docs/ai/quality_gate.md`

## MCP

`package.json` pins `@playwright/mcp` and `playwright`. Do not use `@latest`.

## Review Rule

AI can draft tests, page objects, and scenario data. A human reviewer owns the final merge decision and must apply the quality gate checklist.

## Failure Analysis

AI analysis reads files under `reports/failure_artifacts/{test_id}/`. It must not query live systems.
