# Project Timeline Assessment

Status legend: Planned | Implemented | Executed | Partially tested | Validated | Deployed | Failed | Deprecated | Unknown

## Verified timeline

### 2026-06-18 — repository bootstrap
- date: 2026-06-18
- activity: Initial repository scaffolding and knowledge-base templates added.
- scenario_id: none
- attack_technique: none
- systems_involved: repository only
- repository_commit: `3d92fb5`, `6f9c587`, `e2a1d95`, `4f17415`, `316d68a`, `ebcf2cf`, `ae1cb0f`, `1c252c4`, `826fd65`
- claimed_result: playbook foundation established
- evidence_found: git history
- validation_status: Implemented
- gaps: no lab-backed validation yet
- recommended_action: treat as documentation/bootstrap only

### 2026-06-19 — detection-first content merged
- date: 2026-06-19
- activity: detection-first markdown knowledge entries merged to main
- scenario_id: none
- attack_technique: none
- systems_involved: repository only
- repository_commit: `0768c61`, merge `09c5a72`
- claimed_result: detection-first posture added
- evidence_found: merged PR #1 and git history
- validation_status: Implemented
- gaps: no execution evidence
- recommended_action: keep as reference material, not validation evidence

### 2026-07-07 — project positioning refresh
- date: 2026-07-07
- activity: README/license reframed project positioning
- scenario_id: none
- attack_technique: none
- systems_involved: repository only
- repository_commit: `d0d246b`, `5e5faa5`
- claimed_result: repo framing aligned
- evidence_found: git history, README state
- validation_status: Implemented
- gaps: no direct lab impact
- recommended_action: preserve, no remediation needed

### 2026-07-18 — PT-2026-001 PowerShell scenario committed
- date: 2026-07-18
- activity: PT-2026-001 foundation and validation artifacts added
- scenario_id: PT-2026-001
- attack_technique: T1059.001 PowerShell
- systems_involved: victim, SOC, repository
- repository_commit: `c350f1c`
- claimed_result: PowerShell execution scenario validated
- evidence_found: scenario YAML, validation markdown, sanitized evidence JSON, live replay `detections/validation/live/VAL-2026-001-PT-2026-001.json`
- validation_status: Validated (re-verified live on 2026-07-18)
- gaps: historical Wazuh rule was partly atomic-specific; Splunk field mapping had not existed at commit time
- recommended_action: retain scenario, use new Sigma rule + live Splunk query as current source of truth

### 2026-07-18 — PT-2026-002 command-shell scenario scaffolded
- date: 2026-07-18
- activity: CMD execution scenario scaffold committed before full validation
- scenario_id: PT-2026-002
- attack_technique: T1059.003 Windows Command Shell
- systems_involved: victim, repository
- repository_commit: `682f536`
- claimed_result: scenario scaffolded
- evidence_found: git history and scenario files
- validation_status: Implemented
- gaps: scaffold commit alone did not prove live detection quality
- recommended_action: use later validation evidence, not scaffold commit, for assurance claims

### 2026-07-18 — PT-2026-002 validated and shipped
- date: 2026-07-18
- activity: CMD scenario validation committed
- scenario_id: PT-2026-002
- attack_technique: T1059.003 Windows Command Shell
- systems_involved: victim, SOC, repository
- repository_commit: `c126bc6`
- claimed_result: cmd execution scenario validated
- evidence_found: scenario/results files, Wazuh local rule file, sanitized evidence JSON, live replay `detections/validation/live/VAL-2026-002-PT-2026-002.json`
- validation_status: Validated (re-verified live on 2026-07-18)
- gaps: historical Wazuh detections were exact-string/atomic-specific; Splunk validation layer was added later
- recommended_action: prefer Sigma + Splunk live rule for current validation program

### 2026-07-18 — PT-2026-003 WMI scenario validated
- date: 2026-07-18
- activity: WMI execution scenario committed and PR updated
- scenario_id: PT-2026-003
- attack_technique: T1047 Windows Management Instrumentation
- systems_involved: victim, SOC, repository
- repository_commit: `4c6ba3e`
- claimed_result: WMI execution scenario validated
- evidence_found: scenario/results files, Wazuh local rule file, sanitized evidence JSON, live replay `detections/validation/live/VAL-2026-003-PT-2026-003.json`
- validation_status: Validated (re-verified live on 2026-07-18)
- gaps: historical Wazuh rules embedded scenario-specific filenames; portable Sigma coverage was missing
- recommended_action: use current PowerShell-WMI Sigma rule for future testing

### 2026-07-18 — open purple-team PR remains unmerged
- date: 2026-07-18
- activity: PR #5 opened for PT-2026-001/002/003 content
- scenario_id: PT-2026-001/PT-2026-002/PT-2026-003
- attack_technique: T1059.001 / T1059.003 / T1047
- systems_involved: repository / GitHub
- repository_commit: branch `feat/mayuri-pt-2026-001-foundation`
- claimed_result: artifacts ready for review
- evidence_found: GitHub PR #5 open
- validation_status: Implemented but not deployed to default branch
- gaps: main branch does not yet contain July scenario work
- recommended_action: merge only after CI and documentation additions on current branch are reviewed

### 2026-07-18 — Splunk sidecar and Windows forwarders operating in lab
- date: 2026-07-18
- activity: Splunk Enterprise on SOC01 plus forwarders on victim/DC01 verified live
- scenario_id: supporting platform
- attack_technique: telemetry platform
- systems_involved: SOC01, victim, DC01
- repository_commit: none (lab state)
- claimed_result: live SIEM available for detection validation
- evidence_found: ports `8000/8089/9997` listening on SOC01; 24h Splunk counts for victim/DC01; current live validation JSON files
- validation_status: Deployed
- gaps: XML field extraction/CIM normalization is still incomplete; current Mayuri live Sigma pipeline uses raw XML matching
- recommended_action: keep Splunk as primary live validation backend; defer Elastic

### 2026-07-18 — Sigma validation platform branch created
- date: 2026-07-18
- activity: evidence-driven Sigma validation stage implemented on `feat/sigma-validation-platform`
- scenario_id: PT-2026-001/PT-2026-002/PT-2026-003
- attack_technique: T1059.001 / T1059.003 / T1047
- systems_involved: repository, SOC context, Splunk
- repository_commit: working tree on `feat/sigma-validation-platform`
- claimed_result: isolated Sigma tooling, fixture tests, generated Splunk/Elastic outputs, and live validation records added
- evidence_found: `automation/validators/`, `detections/generated/`, `detections/validation/live/`, `tests/fixtures/`
- validation_status: Partially tested / In progress until committed and reviewed
- gaps: GitHub Actions not yet added in this branch snapshot; offline EVTX workflow is documented but not fully operationalized with Chainsaw/Hayabusa binaries
- recommended_action: finalize docs + CI, then commit and open a dedicated PR

## Verified current position
- Confirmed prior attack scenarios: PT-2026-001, PT-2026-002, PT-2026-003
- Confirmed current live SIEM: Splunk on SOC01
- Confirmed current branch for Sigma platform work: `feat/sigma-validation-platform`
- Confirmed existing open historical PR: #5 on `feat/mayuri-pt-2026-001-foundation`
- Verified status of the program: detection engineering has moved from ad hoc Wazuh-only validation to a reproducible Sigma + Splunk + fixture workflow, but CI and offline EVTX tooling remain incomplete.
