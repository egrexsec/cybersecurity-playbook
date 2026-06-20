# Microsoft Defender Advanced Hunting

DetLab-backed markdown detections and hunts for MDE live under `detections/`.

## Focus Areas

- DeviceProcessEvents
- DeviceNetworkEvents
- DeviceFileEvents
- DeviceRegistryEvents
- DeviceLogonEvents
- AlertInfo
- AlertEvidence

## Authoring

Use `../../templates/detlab-detection-template.md` as the base schema.

Each entry should include:

- stable `DET-####` frontmatter ID
- primary ATT&CK mapping
- executable KQL under `## Query`
- triage and investigation steps
- artifacts and response actions
- related detection graph edges
