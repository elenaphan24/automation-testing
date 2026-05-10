# AI Log Analysis Contract

AI analysis reads exported failure files only. It must not query live databases, APIs, browsers, or production systems.

## Input Directory

`reports/failure_artifacts/{test_id}/`

Expected files:

- `api_log.json`
- `stack_trace.txt`
- `ui_screenshot.png` when available
- `playwright_trace.zip` when available

## Output Format

```json
{
  "hypotheses": [
    {
      "cause": "Payment API returned 500",
      "evidence": "api_log.json line 147: http_status=500",
      "layer": "API",
      "confidence": 0.92
    }
  ]
}
```

## Rules

- Each hypothesis must cite file-based evidence.
- Confidence must be between 0 and 1.
- The TAE owns the final diagnosis and fix decision.

