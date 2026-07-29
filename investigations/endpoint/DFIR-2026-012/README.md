# DFIR-2026-012 — Service execution investigation

## Question
Did a command interpreter execute as a child of the Windows Service Control Manager, and was the behavior caused by controlled validation or unauthorized activity?

## Evidence sequence
1. Review Sysmon process creation for `ParentImage = services.exe` and child `cmd.exe` or PowerShell.
2. Correlate the command line and user context; this scenario executed as `NT AUTHORITY\\SYSTEM`.
3. Pivot to Windows System events `7045`, `7009`, and `7000` for service installation and start behavior.
4. Determine whether the service was started. Creation without a resulting `services.exe` child is not sufficient for this behavioral rule.
5. Confirm service deletion and inspect for residual binaries, scripts, marker files, or continued child processes.

## Validated observations
- Both controlled positives created the expected service-launched command-shell lineage and fired in Splunk.
- The benign create/delete control generated event `7045` but did not fire because it was never started.
- Query-only controls remained quiet.
- Final cleanup found no remaining services or files.

## Disposition
Expected lab activity for validation `VAL-2026-012`. Outside an approved exercise, the same lineage warrants escalation because arbitrary command interpreters launched directly by `services.exe` are uncommon and can indicate service-based execution.
