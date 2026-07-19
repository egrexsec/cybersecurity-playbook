# DET-2026-007 Validation

## Summary
- Rule: `22da6a1c-f0f2-4a4d-a322-c2da4c8ba2a5`
- Scenario: `PT-2026-007`
- Technique: `T1037.001`
- Validation run: `VAL-2026-007`
- Status: validated in the Mayuri lab

## Positive tests
1. Original `reg.exe add` UserInitMprLogonScript path
   - Start: `2026-07-18T19:11:27.258486Z`
   - Result: detection fired
   - Supporting telemetry: Sysmon Event ID 1 plus loaded-hive value confirmation under `HKEY_USERS\PT2026007\Environment`
2. Modified variant using PowerShell `Set-ItemProperty`
   - Start: `2026-07-18T19:11:39.708081Z`
   - Result: detection fired
   - Supporting telemetry: Sysmon Event ID 1 plus loaded-hive value confirmation under `HKEY_USERS\PT2026007\Environment`

## Negative tests
- benign loaded-hive environment query: no detection
- benign `reg.exe query` of the environment hive: no detection
- benign calc environment value creation: no detection

## Detection assessment
The Sigma rule is behavioral within the current lab constraints:
- detects `reg.exe add` when `UserInitMprLogonScript` is set to a temp-path batch file
- detects PowerShell `Set-ItemProperty` when `UserInitMprLogonScript` is set to a temp-path batch file
- remains quiet on environment inspection and benign non-logon-script values
