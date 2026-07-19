# Case Management

## ID families
- `IR-YYYY-NNN` — incident-response cases
- `HUNT-YYYY-NNN` — scheduled or analyst hunt cases
- `DFIR-YYYY-NNN` — forensic collection / deep-dive cases
- `PT-YYYY-NNN` — purple-team execution cases
- `DET-YYYY-NNN` — detection-engineering work items
- `VAL-YYYY-NNN` — validation runs

## Case directory template

```text
investigations/cases/<case-id>/
├── case.yaml
├── alert.json
├── enrichment.json
├── hunt-results.json
├── findings.json
├── evidence-manifest.json
├── timeline.csv
├── process-tree.json
├── detection-opportunities.md
├── containment-plan.md
├── investigation.md
└── closure.md
```

## Workflow rules
1. Every workflow creates or updates a case.
2. Cases are schema-validated before update.
3. Case operations use a local lock file to avoid concurrent corruption.
4. Containment execution is blocked unless approval requirements are satisfied.
5. Closing a case does not delete evidence.

## Required fields
The canonical structure is enforced by `schemas/investigation-case.schema.json`.
