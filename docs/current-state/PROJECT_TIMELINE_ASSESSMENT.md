# Project Timeline Assessment

Status legend: Planned | Implemented | Executed | Partially tested | Validated | Deployed | Failed | Deprecated | Unknown

## Verified timeline

### 2026-06-18 — repository bootstrap
- date: 2026-06-18
- activity: initial repository scaffolding and template content landed
- scenario_id: none
- attack_technique: none
- systems_involved: repository only
- repository_commit: `3d92fb5`, `6f9c587`, `e2a1d95`, `4f17415`, `316d68a`, `ebcf2cf`, `ae1cb0f`, `1c252c4`, `826fd65`
- claimed_result: project foundation established
- evidence_found: git history
- validation_status: Implemented
- gaps: no lab-backed validation yet
- recommended_action: treat as historical foundation only

### 2026-06-19 — detection-first content merged
- date: 2026-06-19
- activity: detection-first markdown entries merged into main
- scenario_id: none
- attack_technique: none
- systems_involved: repository only
- repository_commit: `0768c61`, merge `09c5a72`
- claimed_result: repo positioning toward detection engineering improved
- evidence_found: merged PR history and committed content
- validation_status: Implemented
- gaps: still documentation-first at this point
- recommended_action: preserve as origin story, not as proof of live validation

### 2026-07-07 — project positioning refresh
- date: 2026-07-07
- activity: README and licensing posture refreshed
- scenario_id: none
- attack_technique: none
- systems_involved: repository only
- repository_commit: `d0d246b`, `5e5faa5`
- claimed_result: cleaner repo framing
- evidence_found: git history and current docs
- validation_status: Implemented
- gaps: still pre-validation era
- recommended_action: keep, but do not let it overstate capability

### 2026-07-18 — PT-2026-001 validated
- date: 2026-07-18
- activity: first end-to-end PowerShell scenario committed and validated
- scenario_id: PT-2026-001
- attack_technique: T1059.001
- systems_involved: victim, SOC01, repository
- repository_commit: `c350f1c`
- claimed_result: PowerShell execution scenario validated
- evidence_found: scenario YAML, Sigma rule, fixtures, validation markdown, live validation JSON
- validation_status: Validated
- gaps: portable Splunk field normalization still incomplete
- recommended_action: keep as first live case study

### 2026-07-18 — PT-2026-002 validated
- date: 2026-07-18
- activity: Windows command-shell scenario validated
- scenario_id: PT-2026-002
- attack_technique: T1059.003
- systems_involved: victim, SOC01, repository
- repository_commit: `682f536`, `c126bc6`
- claimed_result: cmd execution scenario validated
- evidence_found: scenario YAML, Sigma rule, fixtures, validation markdown, live validation JSON
- validation_status: Validated
- gaps: live query path still relies on current lab-specific normalization assumptions
- recommended_action: keep as second validated scenario in showcase material

### 2026-07-18 — PT-2026-003 validated
- date: 2026-07-18
- activity: WMI execution scenario validated
- scenario_id: PT-2026-003
- attack_technique: T1047
- systems_involved: victim, SOC01, repository
- repository_commit: `4c6ba3e`
- claimed_result: WMI execution scenario validated
- evidence_found: scenario YAML, Sigma rule, fixtures, validation markdown, live validation JSON
- validation_status: Validated
- gaps: broader ATT&CK coverage still limited to three live scenarios on main
- recommended_action: keep as third validated scenario in showcase material

### 2026-07-18 — Sigma validation platform merged
- date: 2026-07-18
- activity: Sigma tooling, generated queries, live validation record format, and CI workflow merged into main
- scenario_id: PT-2026-001/PT-2026-002/PT-2026-003
- attack_technique: T1059.001 / T1059.003 / T1047
- systems_involved: repository, Splunk, Mayuri lab evidence
- repository_commit: merged state including `9a89a37`, merge commit `e7ba885`
- claimed_result: repository became a lab-validated detection-as-code content repo rather than a markdown-only library
- evidence_found: `automation/validators/`, `detections/generated/`, `.github/workflows/detection-validation.yml`, `detections/validation/live/`
- validation_status: Deployed
- gaps: CI validates offline content and evidence structure, not live Mayuri connectivity
- recommended_action: keep CI focused on offline validation and preserve live lab work as structured evidence

### 2026-07-18 to 2026-07-19 — PT-2026-004 through PT-2026-011 merged
- date: 2026-07-18 to 2026-07-19
- activity: scheduled-task, service-creation, run-key, logon-script, BITS, PowerShell-profile, rundll32, and regsvr32 scenarios were merged into main in sequence
- scenario_id: PT-2026-004 / PT-2026-005 / PT-2026-006 / PT-2026-007 / PT-2026-008 / PT-2026-009 / PT-2026-010 / PT-2026-011
- attack_technique: T1053.005 / T1543.003 / T1547.001 / T1037.001 / T1197 / T1546.013 / T1218.011 / T1218.010
- systems_involved: victim, SOC01, repository
- repository_commit: merge commits `4b7d31e`, `005bf4c`, `869c935`, `099a603`, `7a2bb10`, `3453068`, `93a6d88`, `d1b0d0f`
- claimed_result: the repository expanded from three validated execution scenarios to eleven validated Windows execution/persistence scenarios on main
- evidence_found: scenario YAML, Sigma rules, fixtures, validation markdown, live validation JSON, hunts, and investigation notes for PT-2026-004..011
- validation_status: Validated
- gaps: normalized-field maturity, durable alert objects, and broader non-Windows coverage still lag the scenario count growth
- recommended_action: treat this as the current baseline for public status/metrics rather than the earlier three-scenario snapshot

## Position recorded on 2026-07-19
- the repository supported authored Sigma, generated Splunk/Elastic queries, fixture tests, and live-validation records
- eleven scenarios had historical live-validation records on the then-current main branch
- GitHub Actions validated offline content and evidence structure
- this dated position supported a lab-validated portfolio claim at that time; current repository posture is fixture-tested content plus sanitized historical summaries, not a current lab-health assertion
