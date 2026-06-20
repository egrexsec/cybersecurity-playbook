# Cybersecurity Playbook

Detection-first markdown knowledge base for threat hunting, DFIR, cloud investigations, and response workflows.

## DetLab Markdown Schema

DetLab can ingest curated markdown directly when entries follow this structure.

### Required frontmatter

```yaml
---
id: DET-3101
name: Encoded PowerShell
content_kind: hunt
status: validated
severity: high
author: mell0wx
domain: [endpoint]
platforms: [windows, mde]
logsource:
  product: mde
  service: advanced_hunting
attack:
  technique: T1059.001
  tactic: execution
data_sources:
  - name: DeviceProcessEvents
    kind: process
    provider: mde
tests:
  - name: Analyst validation
    source: markdown-curation
    test_id: encoded-powershell-v1
---
```

### Supported frontmatter fields

- `id`: stable DetLab ID, `DET-####`
- `name` or `title`
- `content_kind`: `hunt`, `investigation`, or `artifact`
- `status`: `draft`, `experimental`, `testing`, `validated`, `stable`, `production`, `deprecated`
- `severity`: `low`, `medium`, `high`, `critical`
- `author`
- `domain`: one or more of `endpoint`, `identity`, `cloud`, `network`, `email`
- `platforms`
- `logsource.product`, `logsource.service`
- `attack.technique`, `attack.tactic`
- `attack_context[]`
- `data_sources[]`
- `triage_steps[]`
- `investigation_steps[]`
- `falsepositives[]`
- `artifacts[]`
- `velociraptor_artifacts[]`
- `cloud_telemetry[]`
- `related_detections[]`
- `response_actions[]`
- `references[]`
- `tests[]`

### Recommended sections

- `## Query`
- `## Triage Guidance`
- `## Investigation Steps`
- `## False Positives`
- `## Artifacts`
- `## Response Actions`
- `## Related Hunts`
- `## Notes`

### Authoring rules

- Put the primary ATT&CK mapping in frontmatter.
- Use `attack_context` for partial coverage, adjacent techniques, and likely follow-on activity.
- Use explicit `related_detections` for relationship graph edges.
- Put the executable hunt logic in a fenced code block under `## Query`.
- Use stable `DET-####` IDs so graph links remain deterministic.

## Templates

- `templates/detlab-detection-template.md`
- `templates/kql-template.md`
- `templates/hunt-template.md`
- `templates/investigation-template.md`
- `templates/velociraptor-template.md`
