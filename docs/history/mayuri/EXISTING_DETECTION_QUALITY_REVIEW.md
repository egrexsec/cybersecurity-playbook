# Existing Detection Quality Review

## Historical Wazuh detections

| rule_id | title | source_format | target_platform | scenario | technique | assessment | exact_atomic_strings | behavioral_coverage | variant_detected | recommended_status |
|---|---|---|---|---|---|---|---|---|---|---|
| 100201 | PT-2026-001 original Atomic registry-backed PowerShell execution | Wazuh XML | Wazuh | PT-2026-001 | T1059.001 | Atomic-specific | `AtomicRedTeam`, `/v ART` | Low | N/A | atomic-specific |
| 100202 | PT-2026-001 suspicious PowerShell decode-and-execute behavior | Wazuh XML | Wazuh | PT-2026-001 | T1059.001 | Semi-behavioral but broad | none exact to Atomic in the rule body | Medium | historically yes | test |
| 100203 | PT-2026-002 batch-script cmd execution detected | Wazuh XML | Wazuh | PT-2026-002 | T1059.003 | Exact-command detection | `pt-2026-002-positive.cmd` | Low | no | atomic-specific |
| 100204 | PT-2026-002 env-var based cmd execution detected | Wazuh XML | Wazuh | PT-2026-002 | T1059.003 | Narrow tool-pattern detection | `LOCALAPPDATA:~-3,1.*md /c` | Medium | yes for the specific variant | test |
| 100205 | PT-2026-003 [wmiclass] PowerShell detected | Wazuh XML | Wazuh | PT-2026-003 | T1047 | Exact-marker detection | `pt-2026-003-wmic-positive.txt` | Low | no | atomic-specific |
| 100206 | PT-2026-003 Invoke-WmiMethod local process creation | Wazuh XML | Wazuh | PT-2026-003 | T1047 | Tool/path-specific | `pt-2026-003-invoke-wmi-positive.txt` | Medium | partially | atomic-specific |

## Current Sigma detections

| rule_id | title | source_format | target_platform | scenario | technique | assessment | exact_atomic_strings | behavioral_coverage | variant_detected | negative_matches | recommended_status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `0b77858e-3f9f-4a0e-bc4c-8f0ac4b2b0d1` | Suspicious PowerShell Decode And Execute Behavior | Sigma | Splunk / Elastic conversion | PT-2026-001 | T1059.001 | Behavioral within PowerShell script-block scope | No exact Atomic markers | High for decode+execute behavior | Yes | 0/5 in fixtures, 0/3 in live negatives | validated-for-lab / candidate validated |
| `6e90d85e-4476-4a9f-ac12-9f983cadc5c1` | Suspicious Windows Command Shell Execution From Temporary Or Obfuscated Context | Sigma | Splunk / Elastic conversion | PT-2026-002 | T1059.003 | Behavioral but still tuned to current lab tradecraft | No exact filename requirement in rule | Medium | Yes | 0/3 live negatives | validated-for-lab |
| `497cb8cc-c62d-4a90-b2ae-69b33b8048f7` | Suspicious PowerShell WMI Process Creation Behavior | Sigma | Splunk / Elastic conversion | PT-2026-003 | T1047 | Behavioral within PowerShell-WMI process creation scope | No exact marker required | High | Yes | 0/3 live negatives | validated-for-lab |

## Key findings
- The historical Wazuh layer is useful as scenario evidence, but most rules remain **atomic-specific** or **marker-specific**.
- The new Sigma layer is materially better for portability and repeatability, but current Splunk live execution still depends on a Mayuri raw-XML search wrapper because the SIEM is ingesting XML without equivalent field normalization/CIM extraction.
- None of the current rules should be described as universal enterprise detections. They are **validated for the Mayuri lab** under the documented telemetry conditions.

## Required follow-up
1. Normalize Splunk XML fields so official field-based Sigma SPL can become the live query path.
2. Add scheduled-task and service-creation scenarios before claiming broader ATT&CK coverage.
3. Replace remaining historical Wazuh marker-specific rules if the intent is reusable detection engineering rather than lab visibility.
