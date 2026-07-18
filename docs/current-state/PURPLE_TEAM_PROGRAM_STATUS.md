# Purple Team Program Status

## Milestone matrix
| Capability | Status | Evidence | Blocking Issue | Next Action |
|---|---|---|---|---|
| Lab readiness | Partially ready | `DETECTION_PLATFORM_READINESS.md`, `PROJECT_TIMELINE_ASSESSMENT.md` | limited to current Mayuri lab assumptions | keep evidence-scoped and public-safe |
| Windows telemetry | Ready | Sysmon + PowerShell + Splunk evidence in live validation JSON | field normalization incomplete | improve normalized field model |
| Splunk ingestion | Ready | generated Splunk queries + `VAL-2026-001..003` | raw XML matching still used in places | normalize fields where practical |
| Atomic scenario 1 | Validated | `VAL-2026-001-PT-2026-001.json` | latency not yet standardized | add numeric latency fields |
| Atomic scenario 2 | Validated | `VAL-2026-002-PT-2026-002.json` | still lab-tuned | broaden behavioral coverage carefully |
| Atomic scenario 3 | Validated | `VAL-2026-003-PT-2026-003.json` | broader ATT&CK coverage still limited | add next scenarios over time |
| Threat hunts | Partially ready | `HUNT-2026-001..003` | could be broader and more standardized | expand hunt packs |
| Forensics | Partially ready | `investigations/endpoint/DFIR-2026-001..003/` | not yet full DFIR suite | enrich case studies and artifacts |
| Sigma source rules | Ready | `detections/sigma/windows/process_creation/` | only three canonical rules on main | add more validated rules incrementally |
| Splunk conversions | Ready | `detections/generated/splunk/official/` and `live/` | live path still partly XML-backed | improve normalization |
| Offline EVTX testing | Staged | `docs/workflows/OFFLINE_EVTX_DETECTION_TESTING.md` | tooling not yet fully operationalized | add Chainsaw/Hayabusa workflow |
| Positive fixtures | Ready | `tests/fixtures/` | coverage still limited to current techniques | expand with each new scenario |
| Negative fixtures | Ready | `tests/fixtures/` | same as above | expand with each new scenario |
| Live detection validation | Ready | `detections/validation/live/` | currently three scenarios on main | continue scenario-by-scenario growth |
| GitHub CI | Ready | `.github/workflows/detection-validation.yml` | live Mayuri connectivity intentionally excluded | keep CI offline-focused |
| Elastic readiness | Deferred | `ELASTIC_READINESS_DECISION.md` | no live backend deployment | keep conversion-only for now |
| Elastic deployment | Not started | none | intentionally deferred | revisit only after stronger maturity |

## Current verified maturity level
**Level 4 — Detection as Code**

### Why this level is supported
- telemetry-backed scenarios exist
- authored Sigma rules exist
- backend conversions exist
- offline fixture tests exist
- live validation records exist
- CI validates content structure and generated artifacts

### Why it is not yet Level 5 or 6
- live validated coverage is still narrow
- field normalization remains incomplete in Splunk
- offline EVTX workflow is documented but not fully operationalized
- Elastic conversion exists, but no live Elastic backend validation is present
