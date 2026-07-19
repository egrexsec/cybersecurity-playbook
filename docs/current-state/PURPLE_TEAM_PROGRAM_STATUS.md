# Purple Team Program Status

## Milestone matrix
| Capability | Status | Evidence | Blocking Issue | Next Action |
|---|---|---|---|---|
| Lab readiness | Partially ready | `DETECTION_PLATFORM_READINESS.md`, `PROJECT_TIMELINE_ASSESSMENT.md` | limited to current Mayuri lab assumptions | keep evidence-scoped and public-safe |
| Windows telemetry | Ready | Sysmon + PowerShell + Splunk evidence in live validation JSON | field normalization incomplete | improve normalized field model |
| Splunk ingestion | Ready | generated Splunk queries + `VAL-2026-001..011` | raw XML matching still used in places | normalize fields where practical |
| Atomic execution foundation | Validated | `VAL-2026-001..004` | latency not yet standardized | add numeric latency fields |
| Windows persistence expansion | Validated | `VAL-2026-005..011` | coverage is broader but still Windows-centric | continue expanding safely |
| Threat hunts | Partially ready | `HUNT-2026-001..011` | could be broader and more standardized | expand hunt packs |
| Forensics | Partially ready | `investigations/endpoint/DFIR-2026-001..011/` | not yet full DFIR suite | enrich case studies and artifacts |
| Sigma source rules | Ready | `detections/sigma/windows/process_creation/` | 11 canonical rules are live on main | add more validated rules incrementally |
| Splunk conversions | Ready | `detections/generated/splunk/official/` and `live/` | live path still partly XML-backed | improve normalization |
| Offline EVTX testing | Staged | `docs/workflows/OFFLINE_EVTX_DETECTION_TESTING.md` | tooling not yet fully operationalized | add Chainsaw/Hayabusa workflow |
| Positive fixtures | Ready | `tests/fixtures/` | coverage is solid for current Windows scenarios | expand with each new scenario |
| Negative fixtures | Ready | `tests/fixtures/` | same as above | expand with each new scenario |
| Live detection validation | Ready | `detections/validation/live/` | 11 scenarios are live validated on main | continue scenario-by-scenario growth |
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
- live validated coverage is still narrower than the long-term roadmap, but no longer limited to the original three scenarios
- field normalization remains incomplete in Splunk
- offline EVTX workflow is documented but not fully operationalized
- Elastic conversion exists, but no live Elastic backend validation is present
