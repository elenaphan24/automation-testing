# Risk Register

| Risk | Probability | Impact | Owner | Mitigation |
| --- | --- | --- | --- | --- |
| JWT injection blocked by app security | High | High | TAE Lead | Phase 1 spike, ADR-001 fallback to cached UI login |
| `@playwright/mcp` spec breaking changes | High | Medium | AI Engineer | Pin version, Dependabot/Renovate alerts |
| MCP agent output quality too low | High | Medium | AI Engineer | Human review gate for all AI-generated code |
| Parallel tests causing data conflicts | Medium | High | TAE Lead | Per-worker schemas and conflict detection tests |
| Visual baseline instability in CI | Medium | Medium | CI Engineer | Docker-only baselines and documented approval flow |
| Excel files breaking Git workflows | Medium | Low | All | `.gitattributes` binary marking and no runtime Excel reads |
| Phase overrun consuming doc weeks | Low | High | PM | Weeks 9-10 locked in governance checklist |

