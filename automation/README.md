# automation/

Repository-local orchestration and validation helpers.

## Subdirectories
- `orchestrator/` — `playbook` command implementation and authenticated IR receiver
- `validators/` — Sigma, fixture, live-record, and documentation validation helpers
- `execution/` — scenario execution and cleanup scripts
- `collectors/` — supporting collection scripts
- `integrations/` — lab asset metadata
- `n8n/` — importable workflow definitions for live orchestration
- `relays/` — narrowly scoped network relays for segmented lab integrations
- `systemd/` — hardened service and environment-file templates

## Role
Automation in this repo validates content and evidence and provides deployable integration templates. Environment-specific addresses, tokens, and credentials stay outside the repository.
