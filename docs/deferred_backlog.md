# Deferred Backlog

| Item | Reason | Owner |
| --- | --- | --- |
| Real JWT injection spike | Requires live sandbox SUT | TAE Lead |
| Auto-capture screenshot on assertion failure | Requires real Playwright page fixture with autouse failure hook | QA Automation Engineer |
| Real DB schema adapter | Current scaffold uses fake DB | TAE Lead |
| Real Playwright browser fixtures | Current UI PoCs use fake page object | QA Automation Engineer |
| Visual regression implementation | Baseline process documented, suite pending real UI | CI Engineer |
| Jira integration | Test management target not available in scaffold | QA Lead |
| Actor layer (BaseActor, seed/teardown/role pattern) | Removed in 54b7258; real SUT has no user management API yet | TAE Lead |
| Journey runner tests | Removed with actors; journey_runner.py still exists but unused | TAE Lead |

