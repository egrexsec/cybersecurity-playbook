# Windows WMI Process Execution Data Source Notes

## Primary signals
- Sysmon Event ID 1 for process creation
- command lines referencing `wmic.exe`, `Invoke-WmiMethod`, or WMI-backed local process creation
- WMI provider host (`WmiPrvSE.exe`) context where relevant
- Security Event ID 4688 where command line capture is available

## Validation goal
Distinguish local WMI-backed process creation from benign read-only WMI inventory/query activity.
