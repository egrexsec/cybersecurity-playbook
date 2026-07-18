---
id: DET-0000
name: Detection Name
content_kind: detection
status: testing
severity: medium
author: mell0wx
domain:
  - endpoint
platforms:
  - windows
logsource:
  product: mde
  service: advanced_hunting
attack:
  technique: T0000
  tactic: unknown
attack_context:
  - technique: T0000
    tactic: unknown
    name: Related Technique
    coverage: related
    rationale: Why this technique is adjacent.
data_sources:
  - name: DeviceProcessEvents
    kind: process
    provider: mde
triage_steps:
  - step: Validate alert context.
    priority: high
investigation_steps:
  - step: Scope for related activity.
    priority: high
falsepositives:
  - Expected benign case
artifacts:
  - name: Example artifact
    category: event_log
    path: Example path or table
velociraptor_artifacts:
  - Windows.EventLogs.PowerShell
cloud_telemetry:
  - provider: other
    source: ExampleCloudSource
    event_names:
      - ExampleEvent
related_detections:
  - detection_id: DET-0001
    relationship: follow_on
    rationale: Why analysts should pivot there.
response_actions:
  - title: Example response action
    priority: medium
references:
  - https://example.org
tests:
  - name: Analyst validation
    source: markdown-curation
    test_id: example-v1
---

# Detection Name

One-paragraph explanation of what this detection means and why it matters.

## Query

```kusto
// Put the primary hunt or detection logic here.
```

## Triage Guidance

- First triage step
- Second triage step

## Investigation Steps

- First investigation step
- Second investigation step

## False Positives

- Expected benign source

## Artifacts

- Artifact to review

## Response Actions

- Immediate containment or escalation action

## Related Hunts

- Optional follow-on hunt hypothesis
