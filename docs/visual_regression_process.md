# Visual Regression Baseline Process

Visual baselines must be generated inside the Docker image, never from a developer desktop. This avoids operating-system rendering drift.

## Approval Flow

1. Run the visual suite in Docker against sandbox.
2. Store generated baselines in the configured Git LFS path.
3. Review diffs in the CI artifact before approval.
4. Approve only intentional UI changes.
5. Keep tolerance at or below 2 percent unless a documented exception exists.

## CI Rules

- Sandbox and staging may run visual checks.
- Production runs smoke tests only and does not update baselines.
- Failed baselines embed inline in the pytest-html report and produce Playwright traces.

