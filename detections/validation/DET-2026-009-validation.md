# DET-2026-009 Validation

## Summary
- Rule: `86cd3d91-3ef6-4c72-99ab-1db6a4f74f29`
- Scenario: `PT-2026-009`
- Technique: `T1546.013`
- Validation run: `VAL-2026-009`
- Status: validated in the Mayuri lab

## Positive tests
1. Original `Add-Content` profile modification path
   - Start: `2026-07-18T20:00:07.403277Z`
   - Result: detection fired
   - Supporting telemetry: Sysmon Event ID 1 for PowerShell profile modification and subsequent profile execution marker
2. Variant profile append path
   - Start: `2026-07-18T20:00:19.813637Z`
   - Result: detection fired
   - Supporting telemetry: Sysmon Event ID 1 for PowerShell profile modification and subsequent profile execution marker

## Negative tests
- benign `Test-Path $PROFILE`: no detection
- benign `Get-Content $PROFILE -Raw`: no detection
- benign note append to profile: no detection

## Detection assessment
The Sigma rule is behavioral within the current lab constraints:
- detects PowerShell profile persistence when `Add-Content` is used to stage temp-path execution content into the profile
- remains quiet on profile existence checks, profile reads, and benign profile annotation
