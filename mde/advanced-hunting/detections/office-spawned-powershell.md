---
id: DET-3102
name: Office Spawned PowerShell
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
  - technique: T1204.002
    tactic: execution
    name: Malicious File
    coverage: related
    rationale: Office-to-PowerShell often begins with user execution of a phishing attachment.
  - technique: T1027
    tactic: defense-evasion
    name: Obfuscated Files or Information
    coverage: partial
    rationale: Malicious macro and child PowerShell content are frequently obfuscated.
  - technique: T1105
    tactic: command-and-control
    name: Ingress Tool Transfer
    coverage: related
    rationale: Scripted payload retrieval is a common next step.
data_sources:
  - name: DeviceProcessEvents
    kind: process
    provider: mde
  - name: AlertEvidence
    kind: endpoint
    provider: mde
triage_steps:
  - step: Identify the originating Office application and document path that launched PowerShell.
    priority: high
  - step: Review user context and whether macro execution or child process creation was expected.
    priority: high
investigation_steps:
  - step: Pivot into the source document, email, download origin, and user interaction history.
    priority: high
  - step: Review subsequent network, registry, and scheduled-task activity on the same endpoint.
    priority: high
falsepositives:
  - Internal automation that uses Office as a launcher during testing.
artifacts:
  - name: Document hash and file path
    category: file
    path: DeviceFileEvents
  - name: Parent-child process ancestry
    category: process
    path: DeviceProcessEvents
velociraptor_artifacts:
  - Windows.Forensics.Lnk
  - Windows.Registry.RecentDocs
related_detections:
  - detection_id: DET-3101
    relationship: child
    rationale: Encoded PowerShell is a common descendant of Office-launched scripting.
  - detection_id: DET-3103
    relationship: investigate_next
    rationale: Rundll32 can follow script-based staging or proxy execution.
  - detection_id: DET-3104
    relationship: follow_on
    rationale: Scheduled tasks are a likely persistence mechanism after successful execution.
response_actions:
  - title: Quarantine the document and isolate the endpoint if the launch was not expected.
    priority: high
  - title: Block or retract the source message or file share if the document was delivered broadly.
    priority: high
references:
  - https://attack.mitre.org/techniques/T1059/001/
  - https://attack.mitre.org/techniques/T1204/002/
tests:
  - name: Analyst validation
    source: markdown-curation
    test_id: office-spawned-powershell-v1
---

# Office Spawned PowerShell

Surfaces Office applications launching PowerShell so analysts can quickly determine whether a document-based intrusion has moved from user execution into script-based payload delivery.

## Query

```kusto
DeviceProcessEvents
| where InitiatingProcessFileName in~ ("WINWORD.EXE", "EXCEL.EXE", "POWERPNT.EXE", "OUTLOOK.EXE")
| where FileName in~ ("powershell.exe", "pwsh.exe")
| project Timestamp, DeviceName, InitiatingProcessFileName, FileName, ProcessCommandLine, AccountName
```

## Triage Guidance

- Validate whether the parent Office process opened an external attachment, internet-downloaded file, or embedded template.
- Check whether Protected View, Mark-of-the-Web, or mail-delivery context exists for the source document.

## Investigation Steps

- Collect the source file, user mailbox context, and any related browser download history.
- Review for follow-on encoded commands, download cradles, or persistence creation within the same session.

## False Positives

- Highly unusual internal testing workflows that intentionally use Office child scripting.

## Artifacts

- RecentDocs and Jump Lists
- Office trust records and attachment metadata
- EDR process ancestry

## Response Actions

- Block the document hash and sender path if malicious.
- Hunt for the same parent-child pattern across the tenant.
