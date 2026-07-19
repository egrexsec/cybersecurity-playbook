# Containment plan

## increase-logging
- target: VICTIM-MAYURI
- reason: Capture additional PowerShell and process context before any destructive action.
- risk: low
- approval_required: False
- rollback: revert temporary verbose logging configuration
- verification: confirm new telemetry reaches Splunk

## isolate-vm
- target: VICTIM-MAYURI
- reason: Contain suspected follow-on activity if fresh evidence confirms malicious behavior.
- risk: high
- approval_required: True
- rollback: restore prior network connectivity
- verification: confirm connectivity blocked and collection path preserved
