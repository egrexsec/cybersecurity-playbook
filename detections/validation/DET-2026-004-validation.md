# DET-2026-004 Validation

## Summary
- Rule: `3dbcf00c-6ff4-45b3-b16c-f2f5c8678c9a`
- Scenario: `PT-2026-004`
- Technique: `T1053.005`
- Validation run: `VAL-2026-004`
- Status: validated in the Mayuri lab

## Positive tests
1. Original `schtasks.exe /Create` task creation
   - Start: `2026-07-18T15:27:41.462415Z`
   - Result: detection fired
   - Supporting telemetry: Sysmon Event ID 1 and local Task Scheduler 106/110/129/200/201/102
2. Modified variant using `Register-ScheduledTask`
   - Start: `2026-07-18T15:28:05.675870Z`
   - Result: detection fired
   - Supporting telemetry: Sysmon Event ID 1 and local Task Scheduler 106/110/129/200/201/102

## Negative tests
- `schtasks.exe /Query` against an existing Microsoft task: no detection
- `Get-ScheduledTask` inventory query: no detection
- benign scheduled task creation launching `notepad.exe`: no detection

## Detection assessment
The Sigma rule is behavioral within the current lab constraints:
- detects `schtasks.exe /Create` when the action points to `cmd.exe` under a temporary path
- detects PowerShell `Register-ScheduledTask` usage when the action is another PowerShell interpreter writing to a temporary path
- does not trigger on read-only scheduled-task inventory or a benign task launching a standard binary

## Caveat
This remains a lab-validated rule, not a universal enterprise detection. Broader legitimate automation that creates tasks through script interpreters in temporary staging directories could still require environment-specific tuning.
