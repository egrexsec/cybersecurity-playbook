# DET-2026-005 Validation

## Summary
- Rule: `b5bf95a5-e28f-48d3-aa87-d6fb6ad11d88`
- Scenario: `PT-2026-005`
- Technique: `T1543.003`
- Validation run: `VAL-2026-005`
- Status: validated in the Mayuri lab

## Positive tests
1. Original `sc.exe create` service path
   - Start: `2026-07-18T16:38:32.050452Z`
   - Result: detection fired
   - Supporting telemetry: Sysmon Event ID 1 and System 7045/7000/7009
2. Modified variant using PowerShell `New-Service`
   - Start: `2026-07-18T16:38:48.714894Z`
   - Result: detection fired
   - Supporting telemetry: Sysmon Event ID 1 and System 7045/7000/7009

## Negative tests
- `sc.exe qc BITS`: no detection
- `Get-Service BITS`: no detection
- benign `sc.exe create` using `notepad.exe`: no detection

## Detection assessment
The Sigma rule is behavioral within the current lab constraints:
- detects `sc.exe create` when the configured service ImagePath launches `cmd.exe` and writes to a temp path
- detects PowerShell `New-Service` when the configured service binary is another PowerShell interpreter targeting a temp path
- remains quiet on service inspection and a benign non-script service create path
