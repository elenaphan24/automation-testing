# ADR-014: Multi-Environment Configuration

Status: Accepted

Context: The current scope is sandbox, but the framework must support staging and production without code changes.

Decision: Environment-specific values live under `config/envs/`, and the `ENV` variable selects the active file.

Consequences: Tests call the config loader instead of reading YAML directly. Production can enforce smoke-only behavior through the active environment.

