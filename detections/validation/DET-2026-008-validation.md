# DET-2026-008 Validation

## Summary
- Rule: `76f36ef1-89af-4f11-85fc-cf54c3454941`
- Scenario: `PT-2026-008`
- Technique: `T1197`
- Validation run: `VAL-2026-008`
- Status: validated in the Mayuri lab

## Positive tests
1. Original `bitsadmin.exe /transfer` path
   - Start: `2026-07-18T19:25:44.733676Z`
   - Result: detection fired
   - Supporting telemetry: Sysmon Event ID 1 for `bitsadmin.exe` plus local BITS Operational Event ID 3 job creation
2. Modified variant using `Start-BitsTransfer`
   - Start: `2026-07-18T19:26:35.174674Z`
   - Result: detection fired
   - Supporting telemetry: Sysmon Event ID 1 for PowerShell plus local BITS Operational Event IDs 3 and 5 for job create/cancel

## Negative tests
- benign `Get-BitsTransfer`: no detection
- benign `Get-Service BITS`: no detection
- benign `bitsadmin.exe /list /allusers`: no detection

## Detection assessment
The Sigma rule is behavioral within the current lab constraints:
- detects `bitsadmin.exe` transfer/download syntax
- detects PowerShell `Start-BitsTransfer` against the local SMB source
- remains quiet on BITS inventory and service-state inspection

## Caveat
BITS transfer completion did not occur because the host reported no active network connections for BITS. This did not prevent validated job-creation telemetry through Sysmon and local BITS Operational records.
