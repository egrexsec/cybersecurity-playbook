---
id: DET-3104
name: Scheduled Task Creation
content_kind: hunt
status: testing
severity: medium
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
  technique: T1053.005
  tactic: persistence
attack_context:
  - technique: T1059.001
    tactic: execution
    name: PowerShell
    coverage: related
    rationale: Script-based intrusion paths frequently create tasks for persistence.
  - technique: T1547
    tactic: persistence
    name: Boot or Logon Autostart Execution
    coverage: related
    rationale: Scheduled tasks are one of several common persistence pivots.
  - technique: T1003
    tactic: credential-access
    name: OS Credential Dumping
    coverage: gap
    rationale: Credential access often occurs before or after persistence but is not directly visible here.
data_sources:
  - name: DeviceProcessEvents
    kind: process
    provider: mde
  - name: DeviceEvents
    kind: endpoint
    provider: mde
triage_steps:
  - step: Review the task name, trigger, author, and command for user-writable paths, script hosts, or suspicious DLL calls.
    priority: high
  - step: Check whether the creating process was interactive admin activity, software installation, or suspected malware.
    priority: high
investigation_steps:
  - step: Enumerate all tasks created or modified on the host during the same period.
    priority: high
  - step: Review associated binaries, scripts, network callbacks, and registry run keys for redundant persistence.
    priority: medium
falsepositives:
  - Software updaters and enterprise management tooling.
artifacts:
  - name: Scheduled task XML
    category: task
    path: C:\Windows\System32\Tasks
  - name: Task Scheduler operational log
    category: event_log
    path: Microsoft-Windows-TaskScheduler/Operational
velociraptor_artifacts:
  - Windows.System.TaskScheduler
related_detections:
  - detection_id: DET-3101
    relationship: prerequisite
    rationale: Encoded PowerShell frequently precedes task creation in hands-on-keyboard intrusions.
  - detection_id: DET-3103
    relationship: correlated
    rationale: Rundll32 persistence can be launched through scheduled tasks.
response_actions:
  - title: Disable the malicious task and preserve its XML plus referenced payload before removal.
    priority: high
  - title: Hunt for the same task name, command line, or payload path across endpoints.
    priority: medium
references:
  - https://attack.mitre.org/techniques/T1053/005/
tests:
  - name: Analyst validation
    source: markdown-curation
    test_id: scheduled-task-creation-v1
---

# Scheduled Task Creation

Tracks suspicious scheduled-task creation so analysts can quickly pivot from persistence establishment into payload review, user scoping, and broader host compromise assessment.

## Query

```kusto
DeviceProcessEvents
| where FileName in~ ("schtasks.exe", "powershell.exe", "cmd.exe")
| where ProcessCommandLine has_any ("/create", "Register-ScheduledTask", "New-ScheduledTask")
| project Timestamp, DeviceName, InitiatingProcessFileName, ProcessCommandLine, AccountName
```

## Triage Guidance

- Determine whether the task points to scripts, LOLBins, or payloads in temp or user profile paths.
- Compare the task author and execution context with expected admin activity.

## Investigation Steps

- Collect the full task definition and the payload it launches.
- Review whether the same device also showed suspicious PowerShell, rundll32, or credential-access activity.

## False Positives

- IT automation, software updates, and backup agents.

## Artifacts

- Task XML
- Task Scheduler operational log
- Referenced payload path and signer information

## Response Actions

- Disable the task only after preserving the XML and launched payload for evidence.
