# AI Quality Gate

AI-generated code cannot merge until a human reviewer checks:

- The three-layer rule is preserved.
- Tests do not import from `core`.
- Page objects use resilient locators before CSS selectors.
- Test data is YAML/JSON, not hardcoded in test bodies.
- Meaningful actions emit a layer-tagged logger call (`[UI]` / `[API]` / `[TAF]`).
- Logs are layer-tagged with `[UI]`, `[API]`, or `[TAF]`.
- The PR description states `AI-generated - reviewed by <name>` when applicable.

