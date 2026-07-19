# DFIR-2026-008

## Scope
BITS job creation on the approved Windows victim for `PT-2026-008`.

## Key findings
- Local BITS Operational logs confirmed job creation for the original and variant paths.
- Sysmon process creation captured `bitsadmin.exe` and `Start-BitsTransfer` activity.
- Benign BITS inventory and service checks did not trigger the Sigma rule.
- Cleanup reset BITS jobs and removed temporary destination files.

## Time anchors
- Original positive start: `2026-07-18T19:25:44.733676Z`
- Variant positive start: `2026-07-18T19:26:35.174674Z`
