# DFIR-2026-007

## Scope
Windows logon-script registry persistence on the approved Windows victim for `PT-2026-007`.

## Key findings
- The `UserInitMprLogonScript` value was written into a safely loaded user hive and confirmed locally.
- Sysmon process creation captured both the `reg.exe add` path and the PowerShell `Set-ItemProperty` path.
- Both positive paths executed their temporary batch files and produced marker artifacts.
- Benign environment inspection and benign calc environment value creation did not trigger the Sigma rule.
- Cleanup removed the loaded-hive values and temporary batch/marker files.

## Time anchors
- Original positive start: `2026-07-18T19:11:27.258486Z`
- Variant positive start: `2026-07-18T19:11:39.708081Z`
