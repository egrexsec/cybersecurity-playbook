---
id: DET-3103
name: Suspicious Rundll32
content_kind: hunt
status: testing
severity: high
author: mell0wx
domain:
  - endpoint
platforms:
  - windows
  - mde
logsource:
  product: mde
  service: advanced_hunting
attack:
  technique: T1218.011
  tactic: defense-evasion
attack_context:
  - technique: T1105
    tactic: command-and-control
    name: Ingress Tool Transfer
    coverage: related
    rationale: Rundll32 frequently loads remotely delivered or recently dropped payloads.
  - technique: T1059.001
    tactic: execution
    name: PowerShell
    coverage: related
    rationale: Script interpreters commonly stage DLL payloads before rundll32 execution.
  - technique: T1547
    tactic: persistence
    name: Boot or Logon Autostart Execution
    coverage: gap
    rationale: The same DLL may later be reused for persistence paths not directly covered here.
data_sources:
  - name: DeviceProcessEvents
    kind: process
    provider: mde
  - name: DeviceImageLoadEvents
    kind: file
    provider: mde
triage_steps:
  - step: Confirm the DLL path, export name, and whether the command line references user-writable locations or remote shares.
    priority: high
  - step: Review the parent process for script hosts, Office, browsers, or remote admin tools.
    priority: high
investigation_steps:
  - step: Collect the DLL and compare compile time, signature state, prevalence, and recent drop history.
    priority: high
  - step: Review network callbacks and persistence creation linked to the same device and user.
    priority: high
falsepositives:
  - Vendor software installers using rundll32 from signed paths.
artifacts:
  - name: DLL path and signer information
    category: file
    path: DeviceFileEvents
  - name: Module load telemetry
    category: process
    path: DeviceImageLoadEvents
velociraptor_artifacts:
  - Windows.Forensics.Prefetch
  - Windows.Detection.Amcache
related_detections:
  - detection_id: DET-3101
    relationship: prerequisite
    rationale: Encoded PowerShell often stages the DLL or launch command.
  - detection_id: DET-3104
    relationship: investigate_next
    rationale: Attackers may register scheduled tasks to rerun the same DLL payload.
response_actions:
  - title: Contain the host and preserve the DLL before cleanup if the module is unsigned or low prevalence.
    priority: high
references:
  - https://attack.mitre.org/techniques/T1218/011/
tests:
  - name: Analyst validation
    source: markdown-curation
    test_id: suspicious-rundll32-v1
---

# Suspicious Rundll32

Highlights unusual `rundll32.exe` execution patterns so analysts can separate benign control-panel style use from proxy execution of attacker-controlled DLLs.

## Query

```kusto
DeviceProcessEvents
| where FileName =~ "rundll32.exe"
| where ProcessCommandLine has_any ("AppData", "Temp", "\\\\", ".dat", ".jpg", ".png")
| project Timestamp, DeviceName, InitiatingProcessFileName, ProcessCommandLine, AccountName, SHA1
```

## Triage Guidance

- Check whether the DLL resides in a signed system path or a user-writable staging location.
- Determine whether the export name and arguments align with known software behavior.

## Investigation Steps

- Retrieve the module for static review and prevalence checks.
- Pivot into the same user's script execution, network connections, and persistence actions.

## False Positives

- Rare but legitimate vendor software using rundll32 with nonstandard export names.

## Artifacts

- Amcache / Shimcache references to the DLL
- Prefetch for rundll32 and the loaded module
- EDR image-load telemetry

## Response Actions

- Block the DLL hash if malicious and search for the same path pattern across peers.
