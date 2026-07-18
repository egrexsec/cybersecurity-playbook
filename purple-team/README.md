# purple-team/

Contains canonical purple-team scenario definitions and per-scenario results.

## What belongs here
- `scenario.yaml` — canonical scenario definition
- `README.md` — human summary of the scenario
- `RESULTS.md` — sanitized outcome summary

## Naming
- scenario directories use `PT-YYYY-NNN-description`
- scenario IDs should match the directory stem and linked validation artifacts

## Validation relationship
Each scenario should map to:
- a hunt hypothesis
- at least one detection
- fixture tests where applicable
- a live validation record when the scenario is marked live validated
