# ADR-002: YAML Primary, Excel Adapter Only

Status: Accepted

Context: Test data must be readable in reviews and safe for parallel runtime execution.

Decision: YAML and JSON are the runtime data formats. Excel is supported only through an import-time adapter that converts spreadsheets into YAML.

Consequences: Tests can be reviewed with normal diffs. Stakeholders can still provide spreadsheet data, but CI blocks runtime pandas imports outside the adapter.

