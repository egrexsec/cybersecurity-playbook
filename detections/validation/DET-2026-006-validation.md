# DET-2026-006 Validation

## Summary
- Rule: `3f9d4c53-a7cb-4e6a-82a2-0b57a6ef58bb`
- Scenario: `PT-2026-006`
- Technique: `T1547.001`
- Validation run: `VAL-2026-006`
- Status: validated in the Mayuri lab

## Positive tests
1. Original `reg.exe add` Run-key path
   - Start: `2026-07-18T18:35:03.008078Z`
   - Result: detection fired
   - Supporting telemetry: Sysmon Event ID 1 for `reg.exe add` plus local HKLM Run value confirmation
2. Modified variant using PowerShell `Set-ItemProperty`
   - Start: `2026-07-18T18:35:16.165972Z`
   - Result: detection fired
   - Supporting telemetry: Sysmon Event ID 1 plus Sysmon registry set evidence and local HKLM Run value confirmation

## Negative tests
- benign `Get-ItemProperty` Run-key inspection: no detection
- benign `reg.exe query` Run-key inspection: no detection
- benign `calc.exe` Run value creation: no detection

## Detection assessment
The Sigma rule is behavioral within the current lab constraints:
- detects `reg.exe add` when the Run value launches `cmd.exe` and points to temp-path activity
- detects PowerShell `Set-ItemProperty` when the Run value launches hidden PowerShell against a temp path
- remains quiet on Run-key inspection and a benign calc startup value
