# Containment Approval

## Principle
Automation may propose containment but may not execute destructive or service-affecting response actions without explicit approval.

## Plan fields
- action
- target
- reason
- evidence
- risk
- rollback
- approval_required
- estimated_impact
- verification

## Current branch behavior
- `playbook ir contain --plan <case-id>` generates a plan
- `playbook ir contain --execute ...` is intentionally blocked unless an approval token path is implemented and verified
