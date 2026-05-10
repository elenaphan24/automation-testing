# QA Automation Framework

Pytest framework scaffold for multi-environment UI, API, and E2E automation.

## Quick Start

```powershell
pip install -r requirements.txt
$env:ENV = "sandbox"
pytest tests/
```

The default environment is `sandbox`. Configuration lives in `config/envs/` and is loaded through `core.config`.

Follow ISTQB CTAL-TAE aligned 
