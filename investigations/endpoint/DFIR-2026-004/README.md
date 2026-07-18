# DFIR-2026-004

## Scope
Scheduled task creation and execution on the approved Windows victim for `PT-2026-004`.

## Key findings
- Task Scheduler operational records confirmed registration, queueing, launch, action execution, and task completion for the original and variant tasks.
- Sysmon process creation captured both `schtasks.exe /Create` and the PowerShell `Register-ScheduledTask` path.
- Benign inventory and benign notepad task activity did not trigger the Sigma rule.
- Cleanup removed the created tasks and markers.

## Time anchors
- Original positive start: `2026-07-18T15:27:41.462415Z`
- Variant positive start: `2026-07-18T15:28:05.675870Z`
