# Microsoft Defender Advanced Hunting

Repository-backed markdown detections and hunts for MDE live under `detections/`.

## Focus Areas

- DeviceProcessEvents
- DeviceNetworkEvents
- DeviceFileEvents
- DeviceRegistryEvents
- DeviceLogonEvents
- AlertInfo
- AlertEvidence

## Authoring

Use `../../templates/detlab-detection-template.md` as the locally maintained base schema. The historical filename is retained for compatibility and does not require the retired DetLab-DAC repository.

Each entry should include:

- stable `DET-####` frontmatter ID
- primary ATT&CK mapping
- executable KQL under `## Query`
- triage and investigation steps
- artifacts and response actions
- related detection graph edges
