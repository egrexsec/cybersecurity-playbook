# Offline EVTX Detection Testing

## Current implementation state
This workflow is now documented and staged, but **Chainsaw/Hayabusa execution is not yet fully operationalized in the repository automation**. Treat this as the approved next step, not a completed capability.

## Intended workflow
1. Execute approved scenario on victim.
2. Export relevant EVTX logs:
   - `Microsoft-Windows-Sysmon/Operational`
   - `Security`
   - `Microsoft-Windows-PowerShell/Operational`
   - `Microsoft-Windows-TaskScheduler/Operational`
   - `System`
   - `Microsoft-Windows-Windows Defender/Operational`
3. Hash each EVTX export with SHA-256.
4. Store raw EVTX outside the public Git repository.
5. Commit only:
   - hash manifest
   - sanitized excerpts
   - tool versions
   - commands used
   - normalized findings JSON/CSV
6. Run offline tools when available:
   - Chainsaw against Sigma-compatible detections
   - Hayabusa for event/timeline review
7. Compare offline matches against live Splunk results.
8. Link the results to scenario, hunt, and validation records.

## Example export commands on Windows target
```powershell
wevtutil epl Microsoft-Windows-Sysmon/Operational C:\Temp\sysmon.evtx
wevtutil epl Microsoft-Windows-PowerShell/Operational C:\Temp\powershell.evtx
wevtutil epl Security C:\Temp\security.evtx
```

## Expected repository structure
- raw EVTX: out-of-repo storage only
- committed manifests / sanitized outputs:
  - `evidence/sanitized/<scenario-id>/`
  - `investigations/endpoint/<case-id>/`
  - future helper scripts under `automation/validators/`

## Current blockers
- Chainsaw binary not yet staged in this branch
- Hayabusa binary not yet staged in this branch
- No automated EVTX export/import wrapper in `playbook` yet

## Safe fallback until tooling is added
Use Splunk live validation + sanitized raw XML excerpts as the current authoritative evidence path, and treat offline EVTX as a planned enhancement rather than a completed control.
