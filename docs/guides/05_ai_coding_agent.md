# AI Coding Agent

## Context Files

AI agents should read:

- `CLAUDE.md`
- `docs/architecture/architecture.md`
- `docs/ai/quality_gate.md`

## MCP

`package.json` pins `@playwright/mcp`, `@playwright/cli`, and `playwright`. `.mcp.json` pins the MCP server command. Do not use `@latest`.

## MCP Version Updates

1. Read the `@playwright/mcp` and Playwright release notes.
2. Update the pins in `package.json` and `.mcp.json` together.
3. Run API, UI, and E2E smoke checks locally or in CI.
4. Review generated page objects or tests for locator quality and framework-layer compliance.
5. Merge only after the AI quality gate passes.

## Review Rule

AI can draft tests, page objects, and scenario data. A human reviewer owns the final merge decision and must apply the quality gate checklist.

## Failure Analysis

AI analysis reads files under `reports/failure_artifacts/{test_id}/`. It must not query live systems.

## Known Limitations

- AI cannot know business logic it has not seen in code, docs, or test data.
- AI must not receive live database, production API, or production browser access during analysis.
- AI output is not guaranteed correct; the TAE owns validation and final diagnosis.
- AI can suggest locator improvements, but a human reviewer must confirm the selectors are stable and accessible.
