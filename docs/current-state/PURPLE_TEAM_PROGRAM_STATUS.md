# Purple Team Program Status

## Milestone matrix
| Capability | Status | Evidence | Blocking Issue | Next Action |
|---|---|---|---|---|
| Lab readiness | Partially ready | `PROJECT_TIMELINE_ASSESSMENT.md`, `DETECTION_PLATFORM_READINESS.md` | host capacity margin is not ideal | keep changes small and reversible |
| Windows telemetry | Ready | victim/DC01 service checks, Splunk counts, live validation JSON files | field normalization incomplete | normalize XML fields later |
| Splunk ingestion | Ready | listeners `8000/8089/9997`; 24h counts for victim/DC01 | CIM/field extraction not normalized | maintain Splunk as primary backend |
| Atomic scenario 1 | Validated | `VAL-2026-001-PT-2026-001.json` | latency not numerically computed | compute ingestion/detection latency later |
| Atomic scenario 2 | Validated | `VAL-2026-002-PT-2026-002.json` | rule is lab-tuned rather than universal | broaden behavioral rule carefully |
| Atomic scenario 3 | Validated | `VAL-2026-003-PT-2026-003.json` | forensic refresh still partial | add fuller case pack |
| Threat hunts | Partially ready | HUNT-2026-001/002/003 files exist | not yet reworked into broader behavioral hunt packs | expand hunt queries |
| Forensics | Partially ready | historical DFIR README files exist | fresh replay focused on telemetry, not full evidence packs | add refreshed investigation artifacts |
| Sigma source rules | Ready | `detections/sigma/windows/process_creation/` | none for current three scenarios | add next scenario when ready |
| Splunk conversions | Ready | `detections/generated/splunk/official/` | official SPL is not yet the live execution path | normalize fields |
| Offline EVTX testing | Missing / staged | `OFFLINE_EVTX_DETECTION_TESTING.md` | tools not operationalized | add Chainsaw/Hayabusa |
| Positive fixtures | Ready | `tests/fixtures/T1059.001`, `T1059.003`, `T1047` | none | maintain with every new rule |
| Negative fixtures | Ready | same fixture directories | none | expand with future scenarios |
| Live detection validation | Ready | `detections/validation/live/VAL-2026-001...003.json` | latency values uncomputed | add numeric latency extraction |
| GitHub CI | Missing | no `.github/workflows` verified | no enforced PR gate | add workflow next |
| Elastic readiness | Deferred | `ELASTIC_READINESS_DECISION.md` | normalization/capacity/CI gaps | revisit after Splunk hardening |
| Elastic deployment | Not started | none | intentionally deferred | none until readiness gate passes |

## Current verified maturity level
**Level 4 — Detection as Code**

### Why not lower
- Telemetry is collected and searchable.
- The three approved attacks replay reliably and clean up successfully.
- Sigma rules, conversions, fixtures, and live validation artifacts now exist.

### Why not higher yet
- Threat hunting and forensic workflows are not yet revalidated to the same standard across all three scenarios.
- Offline EVTX testing is documented but not operational.
- GitHub CI enforcement is still missing.
- Splunk live detections rely on raw XML matching rather than normalized field extraction.
