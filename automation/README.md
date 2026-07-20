# automation/

Repository-local orchestration and validation helpers.

## Subdirectories
- `orchestrator/` — `playbook` command implementation
- `validators/` — Sigma, fixture, live-record, and documentation validation helpers
- `execution/` — scenario execution and cleanup scripts
- `collectors/` — supporting collection scripts
- `integrations/` — lab asset metadata
- `opencti/` — credential-free OpenCTI and Shodan lab deployment template

## Role
Automation in this repo validates content and evidence; it does not deploy a production SIEM stack.
