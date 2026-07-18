# Windows Process Creation Data Sources

## Scope
Process creation telemetry is the backbone for PT-2026-001 detection and validation.

## Confirmed Sources

| Source | System | Collection Method | Destination | Parsing Status |
|---|---|---|---|---|
| Sysmon Event ID 1 | Windows victim | Sysmon service | Wazuh agent / SOC | Confirmed live |
| Security Event ID 4688 | Windows victim | Advanced audit policy + command-line auditing | Wazuh agent / SOC | Confirmed live |

## Relevant Fields
- Image / NewProcessName
- CommandLine / ProcessCommandLine
- ParentImage / Creator Process Name
- User / SubjectUserName
- Timestamp / UtcTime
- ProcessId / NewProcessId

## ATT&CK Mapping
- `T1059.001` PowerShell
- `T1053.005` Scheduled task creation follow-on
- `T1543.003` Service creation follow-on

## Known Gaps
- No current repo-side field-normalization layer
- No portable fixture corpus before this implementation

## Example Analytics
- PowerShell launched by an unusual parent
- PowerShell with base64 decoding plus invoke-expression behavior
- New persistence process shortly after PowerShell execution
