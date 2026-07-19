# Automated IR Program Status

| Capability | Status | Evidence | Blocking Issue | Next Action |
|---|---|---|---|---|
| Splunk alert intake | Implemented | `schemas/alert-intake.schema.json`, `automation/controller/ir_ops.py`, `automation/n8n/splunk-alert-to-case.json` | live Splunk alert object not yet configured | wire webhook in Splunk and n8n |
| Deduplication | Implemented | case grouping logic in `ir_ops.py` using rule+host+user+window | no production event volume tested | exercise against repeated alerts |
| Case management | Implemented | expanded `investigation-case.schema.json`, case template, `playbook ir create/close` | needs multi-case live use | run additional cases |
| Host enrichment | Implemented | `playbook ir enrich`, normalized enrichment output | currently deterministic/repo-backed | add live VM query module later |
| User enrichment | Implemented | case enrichment includes account and scope fields | no AD API integration yet | add DC-safe identity pivots |
| Process enrichment | Implemented | process context fields stored from alert + derived context | relies on alert payload unless live integrations added | enrich from Splunk export next |
| Network enrichment | Implemented | network fields and classification in case model | no OPNsense API execution yet | add safe network enrichment adapter |
| Velociraptor collection | Partially tested | profile selection and collection manifest generation | API auth/execution not wired | add DFIR API client config |
| Evidence hashing | Implemented | evidence manifest generation with SHA-256 | only repo-side artifacts hashed in this branch | extend to raw DFIR exports |
| Hayabusa processing | Blocked | workflow/documentation added | tool missing on DFIR | install/validate Hayabusa |
| Chainsaw analysis | Blocked | workflow/documentation added | binary unconfirmed on DFIR | install/validate Chainsaw |
| Unified timeline | Implemented | `automation/forensics/build_timeline.py`, `playbook ir timeline` | needs broader source feeds | merge EVTX/Velociraptor later |
| Process tree | Implemented | `process-tree.json` generated from case/process context | shallow for now | extend with Splunk/EVTX parents |
| Automated hunts | Implemented | hunt library + `playbook ir hunt` | only PowerShell-first hunt modeled fully | add more hunt packs |
| Scheduled hunts | Implemented | schedule-ready manifests + n8n workflow export | not production-scheduled | connect to n8n cron |
| Ollama analysis | Partially tested | schema + safe wrapper + fallback analysis path | endpoint unconfirmed | validate local model endpoint |
| Containment planning | Implemented | `playbook ir contain --plan`, containment docs | execution intentionally blocked | add audited approval token path |
| Detection generation | Implemented | detection-opportunity workflow docs and report generation | no new rule authored in this branch | connect to detection build helper |
| Live detection testing | Partially tested | existing `VAL-2026-001` evidence referenced, `playbook detection validate-live` wired to existing validators | fresh live rerun not performed in this branch | rerun PT-2026-001 with confirmed credentials |
| n8n orchestration | Implemented | workflow JSON exports under `automation/n8n/` | not yet imported | import and test in homelab n8n |
| GitHub integration | Implemented | issue templates, PR template, feature branch workflow | no PR opened yet in this branch | push and open draft PR |
| GitHub Actions | Partially tested | existing CI remains green baseline; new schema/controller paths added | workflow not yet expanded for every requested check | extend `detection-validation.yml` |
| PowerShell workflow | Partially tested | PT-2026-001 scenario/hunt/live validation exists; new IR case flow added | fresh live alert-to-case not yet rerun | wire Splunk webhook and rerun |
| Scheduled-task workflow | Planned | existing PT-2026-004 assets provide baseline | no IR pipeline integration yet | map PT-2026-004 into case workflow |
| Service workflow | Planned | existing PT-2026-005 assets provide baseline | no IR pipeline integration yet | map PT-2026-005 into case workflow |
