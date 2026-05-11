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

Azure Pipelines example:

```yaml
steps:
  - task: AzureKeyVault@2
    inputs:
      azureSubscription: qa-service-connection
      KeyVaultName: qa-framework-secrets
      SecretsFilter: SANDBOX_JWT_SECRET,SANDBOX_DB_URL
  - script: pytest tests/
    env:
      ENV: sandbox
      SANDBOX_JWT_SECRET: $(SANDBOX_JWT_SECRET)
      SANDBOX_DB_URL: $(SANDBOX_DB_URL)
```

## Production Guard

When `ENV=production`, pytest exits unless collected tests are marked `smoke`.

## Environment Scope Constraints

| Environment | Who can run | Test scope | Data writes | Parallel workers |
| --- | --- | --- | --- | --- |
| sandbox | All team members | Full suite | Ephemeral schemas allowed | Up to 8 |
| staging | CI pipeline and QA lead | Full suite | Ephemeral schemas allowed | Up to 4 |
| production | CI pipeline only | Smoke tests only | Read-only | 1 sequential worker |

