# Capability Matrix

| Domain | Capability | Status | Evidence / Notes |
|---|---|---|---|
| Endpoint | Windows execution and persistence detection validation | **Live validated (historical)** | 12 Mayuri-backed scenarios; environment retired October 2026 |
| Endpoint | Complete investigation-led Windows case workflow | **Installed / developing** | scenario-linked notes exist; deeper DFIR cases remain in progress |
| DFIR | Public-safe evidence handling and sanitization | **Verified** | documented workflow and sanitized artifacts |
| DFIR | Targeted acquisition | **Planned** | no completed evidence-backed case yet |
| DFIR | Timeline generation | **Planned** | next-stage capability |
| Identity | Credential-abuse investigation | **Planned** | future endpoint/identity and cloud cases |
| Cloud | CloudTrail local analysis with PowerShell + jq | **Verified** | Flaws2.cloud Defender track |
| Cloud | AWS CLI identity/profile pivots | **Verified** | Flaws2.cloud Defender track |
| Cloud | IAM / STS investigation pivots | **Verified** | Flaws2.cloud Defender track |
| Cloud | AWS resource-policy review | **Verified** | ECR policy analysis in Flaws2.cloud Defender track |
| Cloud | Athena investigation workflow | **Conceptually reviewed** | workflow understood; not reproduced in personal account |
| Threat Hunting | Hypothesis-driven Windows hunts | **Historically live validated / fixture-backed** | linked to existing PT scenarios |
| Detection Engineering | Sigma authoring + backend conversion | **Verified** | current repository tooling |
| Detection Engineering | Live SIEM deployment | **Historical only** | Mayuri Splunk environment no longer exists |
