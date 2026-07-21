# Automated Threat Hunting

## Scheduling model
- deterministic schedule only
- baseline query + current-window query
- explicit thresholds
- known-lab suppression
- case creation only when thresholds are met

## Initial hunt set
- daily suspicious PowerShell review
- daily scheduled-task review
- daily service-creation review
- daily privileged-logon review
- daily security-tool-tampering review
- weekly lateral-movement review

## Current branch scope
Only the suspicious-PowerShell hunt is fully modeled into the new case workflow. Other hunt families are scaffolded for later extension.
