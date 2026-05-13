# Test Suitability Criteria

Use this checklist before automating a manual test.

| Question | Yes/No | Notes |
| --- | --- | --- |
| Is the scenario repeated in every regression cycle? |  |  |
| Is it technically possible without OS-level restrictions or lengthy time dependencies? |  |  |
| Does automation provide ROI within the project timeline? |  |  |
| Is the flow stable enough that locators and APIs will not change every sprint? |  |  |
| Is there shared test data that avoids duplication? |  |  |

## Decision Tree

```text
YES to every question -> automate the test.
Any NO answer -> document the reason and keep the scenario manual for now.
```

Review deferred manual scenarios each sprint. A scenario can become automatable when product stability, tooling, or data access improves.
