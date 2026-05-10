# Environment Configuration

## Active Environment

`ENV` selects the active config file from `config/envs/`.

```powershell
$env:ENV = "sandbox"
pytest tests/
```

Valid values:

- `sandbox`
- `staging`
- `production`

## Secrets

YAML files store environment variable names, not secret values. Inject actual secrets through Azure Key Vault or local environment variables.

## Production Guard

When `ENV=production`, pytest exits unless collected tests are marked `smoke`.

