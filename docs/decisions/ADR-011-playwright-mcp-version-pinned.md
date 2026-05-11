# ADR-011: Playwright MCP Version Pinned

Status: Accepted

Context: MCP packages can change behavior between releases.

Decision: `@playwright/mcp` is pinned in `package.json` and `.mcp.json`. Production workflows must not use `@latest`.

Consequences: Updates are deliberate and reviewed through dependency PRs, with release notes checked before bumping versions.

