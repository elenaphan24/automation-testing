# ADR-015: pytest-html Replaces Allure

Status: Accepted

Context: Earlier scaffold used Allure for HTML reporting. Allure requires a separate Java-based CLI to produce HTML from JSON results, adds an npm dependency in CI, and duplicates information that the [UI]/[API]/[TAF] structured logger already records.

Decision: Use pytest-html for HTML reports and JUnit XML for Azure DevOps test result publishing. Remove the allure-pytest dependency, the @allure.step decorators, and the allure-commandline CI step.

Consequences:
- Single self-contained HTML report (no separate generate step).
- JUnit XML feeds Azure DevOps test history natively.
- Step-level annotations are now logger-driven (layer-tagged JSON).
- Failure screenshots embed inline in the HTML report via pytest-html extras instead of allure.attach.
