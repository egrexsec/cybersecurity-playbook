# DET-2026-011 Validation

## Summary
- Rule: `5ab2ae3a-08af-4873-bd89-40fd84b79a7e`
- Scenario: `PT-2026-011`
- Technique: `T1218.010`
- Validation run: `VAL-2026-011`
- Status: validated in the Mayuri lab

## Positive tests
1. Local non-DLL-extension registration target (`shell32.jpg`)
   - Start: `2026-07-18T20:55:27.041956Z`
   - Result: detection fired
   - Supporting telemetry: Sysmon Event ID 1 for `regsvr32.exe` and image-load of `.jpg` target
2. Local SCT/scrobj path
   - Start: `2026-07-18T20:55:39.225647Z`
   - Result: detection fired
   - Supporting telemetry: Sysmon Event ID 1 for `regsvr32.exe` with `scrobj.dll` and `.sct`

## Negative tests
- benign `regsvr32.exe /s C:\Windows\System32\shell32.dll`: no detection
- benign `regsvr32.exe /?`: no detection
- benign `reg.exe query HKLM\Software\Microsoft\Windows\CurrentVersion\Run`: no detection

## Detection assessment
The Sigma rule is behavioral within the current lab constraints:
- detects regsvr32 local SCT/scrobj usage
- detects regsvr32 targeting a non-DLL extension such as `.jpg`
- remains quiet on standard DLL registration and unrelated registry query activity
