# DET-2026-010 Validation

## Summary
- Rule: `68f76492-b7f9-4cb4-8482-2410b0cf0a59`
- Scenario: `PT-2026-010`
- Technique: `T1218.011`
- Validation run: `VAL-2026-010`
- Status: validated in the Mayuri lab

## Positive tests
1. Original `url.dll,FileProtocolHandler` path
   - Start: `2026-07-18T20:20:13.440558Z`
   - Result: detection fired
   - Supporting telemetry: Sysmon Event ID 1 for `rundll32.exe` plus marker confirmation
2. Variant `pcwutl.dll,LaunchApplication` path
   - Start: `2026-07-18T20:20:29.357623Z`
   - Result: detection fired
   - Supporting telemetry: Sysmon Event ID 1 for `rundll32.exe` plus marker confirmation

## Negative tests
- benign `rundll32 shell32.dll,Control_RunDLL appwiz.cpl`: no detection
- benign `cmd.exe /c rundll32 shell32.dll,Control_RunDLL appwiz.cpl`: no detection
- benign `control.exe appwiz.cpl`: no detection

## Detection assessment
The Sigma rule is behavioral within the current lab constraints:
- detects suspicious `rundll32.exe` proxy execution through `url.dll,FileProtocolHandler` and `pcwutl.dll,LaunchApplication`
- remains quiet on standard control panel invocation patterns
