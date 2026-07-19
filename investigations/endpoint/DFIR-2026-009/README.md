# DFIR-2026-009

## Scope
PowerShell profile persistence on the approved Windows victim for `PT-2026-009`.

## Key findings
- The system profile file was created and modified with staged execution lines.
- Subsequent `powershell.exe -Command exit` caused the staged lines to execute and create marker files.
- Sysmon process creation captured the modification path and the follow-on PowerShell execution.
- Benign profile checks and note append did not trigger the Sigma rule.
- Cleanup restored the profile contents and removed marker files.

## Time anchors
- Original positive start: `2026-07-18T20:00:07.403277Z`
- Variant positive start: `2026-07-18T20:00:19.813637Z`
