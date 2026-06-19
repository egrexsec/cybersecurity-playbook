---
id: DET-3101
name: Encoded PowerShell
content_kind: hunt
status: validated
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
  technique: T1059.001
  tactic: execution
attack_context:
  - technique: T1027
    tactic: defense-evasion
    name: Obfuscated Files or Information
    coverage: partial
    rationale: Encoded command arguments reduce analyst visibility and often accompany obfuscation.
  - technique: T1105
    tactic: command-and-control
    name: Ingress Tool Transfer
    coverage: related
    rationale: Encoded PowerShell frequently retrieves second-stage payloads.
  - technique: T1547
    tactic: persistence
    name: Boot or Logon Autostart Execution
    coverage: gap
    rationale: Persistence frequently follows successful scripted execution but is not directly seen here.
data_sources:
  - name: DeviceProcessEvents
    kind: process
    provider: mde
  - name: DeviceNetworkEvents
    kind: network
    provider: mde
triage_steps:
  - step: Validate the full PowerShell command line, initiating account, and parent process.
    priority: high
  - step: Identify whether the encoded argument was launched from Office, a script host, or remote admin tooling.
    priority: high
investigation_steps:
  - step: Scope for repeat executions from the same device or user within the last 24 hours.
    priority: high
  - step: Review child processes, outbound connections, and dropped files immediately after execution.
    priority: high
falsepositives:
  - Administrative automation that wraps scripts with -enc.
  - Security tooling that encodes short PowerShell launchers.
artifacts:
  - name: PowerShell operational logs
    category: event_log
    path: Microsoft-Windows-PowerShell/Operational
    notes: Useful for script block and engine lifecycle review.
  - name: Process command line telemetry
    category: process
    path: DeviceProcessEvents
velociraptor_artifacts:
  - Windows.EventLogs.PowerShell
  - Windows.System.Pslist
related_detections:
  - detection_id: DET-3102
    relationship: prerequisite
    rationale: Office-spawned PowerShell is a common initiating vector for encoded execution.
  - detection_id: DET-3103
    relationship: investigate_next
    rationale: Rundll32 execution can appear in the same intrusion chain after script-based staging.
  - detection_id: DET-3104
    relationship: follow_on
    rationale: Scheduled tasks are a common persistence pivot after hands-on-keyboard PowerShell use.
response_actions:
  - title: Contain the host if the encoded command cannot be tied to approved automation.
    priority: high
  - title: Reset or review affected credentials if the script accessed secrets or spawned credential tooling.
    priority: medium
references:
  - https://attack.mitre.org/techniques/T1059/001/
tests:
  - name: Analyst validation
    source: markdown-curation
    test_id: encoded-powershell-v1
---

# Encoded PowerShell

Detects PowerShell launched with encoded command arguments so analysts can quickly pivot from suspicious execution into payload retrieval, persistence, and credential-access follow-on activity.

## Query

```kusto
DeviceProcessEvents
| where FileName in~ ("powershell.exe", "pwsh.exe")
| where ProcessCommandLine has_any (" -enc", " -encodedcommand", "FromBase64String")
| project Timestamp, DeviceName, InitiatingProcessFileName, AccountName, ProcessCommandLine, SHA1
```

## Triage Guidance

- Confirm whether the parent process is Office, a browser, a script host, or remote management tooling.
- Determine whether the encoded argument resolves to admin automation, security testing, or unknown tradecraft.

## Investigation Steps

- Review nearby `DeviceNetworkEvents` for external destinations reached within five minutes of execution.
- Look for follow-on child processes such as `rundll32.exe`, `schtasks.exe`, `cmd.exe`, or credential dumping tools.
- Collect script block, module, and transcript evidence where available.

## False Positives

- Internal deployment scripts that intentionally obfuscate short bootstrap commands.
- Red-team or detection engineering validation activity.

## Artifacts

- Script block logging
- AMSI or EDR process ancestry
- Prefetch and execution history for PowerShell binaries

## Response Actions

- Isolate the host if the command launched from an untrusted parent or contacted external infrastructure.
- Preserve volatile evidence before terminating long-running child processes.
