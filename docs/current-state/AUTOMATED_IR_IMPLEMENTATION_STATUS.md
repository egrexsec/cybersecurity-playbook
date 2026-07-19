# Automated IR Implementation Status

## Implemented in this branch
- expanded investigation case schema for IR/HUNT/DFIR/PT/DET/VAL workflows
- added alert-intake schema and case directory template
- added deterministic IR controller module with create/enrich/collect/hunt/timeline/analyze/report/contain/close primitives
- added forensic collection profiles and threat-hunt library entries for the PowerShell-first workflow
- added PowerShell-first sample alert payload and sample case artifacts
- added n8n workflow export skeletons for Splunk intake, scheduled hunts, detection validation, PT replay, and case closure
- added GitHub issue templates and PR template for security-engineering workflows
- added evidence-handling, case-management, containment, alert-to-case, EVTX, detection-from-investigation, and automated-hunting docs
- added automated IR architecture and program-status docs

## Partially implemented
- live Splunk webhook integration: controller contract implemented, server-side alert object still manual
- Velociraptor automation: profile/manifests implemented, API execution still manual
- Ollama/Open WebUI analysis: safe wrapper and schema path implemented, endpoint validation pending
- Hayabusa/Chainsaw workflow: documented and integrated as optional stages, tooling not fully validated on DFIR

## Not implemented in this branch
- destructive containment execution against OPNsense/AD/Windows
- automatic merge to default branch
- production rule deployment into Splunk/Wazuh
- silent AI-driven final case disposition
