# Windows Command Shell Data Sources

## Scope
This page documents the primary telemetry planned for `cmd.exe` / Windows Command Shell validation.

## Expected Sources

| Source | System | Collection Method | Destination | Status |
|---|---|---|---|---|
| Sysmon Event ID 1 | Windows victim | Sysmon service | Wazuh / SOC | confirmed available |
| Security Event ID 4688 | Windows victim | advanced audit policy | Wazuh / SOC | confirmed available |
| Sysmon Event ID 11 | Windows victim | Sysmon service | Wazuh / SOC | available when file-write side effects occur |

## Hunt questions
- Which parent processes launched `cmd.exe`?
- Did the execution create or modify a batch file or temporary artifact?
- Did the command line use suspicious environment-variable expansion patterns?
