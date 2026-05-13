# Manual-to-Automated Transition Plan

## Step 1: Identify Manual Regression Tests

| Test name | Execution time | Frequency | Automation candidate Y/N | Notes |
| --- | ---: | --- | --- | --- |
|  |  |  |  |  |

## Step 2: Verify the Manual Test

Run the manual test before automating it. Do not automate stale or invalid steps.

## Step 3: Identify Functional Overlap

Extract shared setup and repeated interactions into fixtures or business-layer helpers. Common examples include login, record creation, and cleanup.

## Step 4: Identify Data Sharing

Move reusable scenario data into YAML files under `data/yaml/`. Keep secrets and environment-specific values in config, not scenario files.

## Step 5: Implement Preconditions

Use `try/finally` cleanup in tests for one-off API setup. Use `conftest.py` fixtures when the same precondition is reused by multiple tests.

## Step 6: Confirm Equivalent Coverage

Run the manual and automated versions in parallel for one sprint. Compare defects found, execution time, and any missed assertions before retiring the manual version.

## Cost Note

The dual-running period increases short-term cost. Track that cost in `docs/roi_tracking.md` so the team can see when automation breaks even.
