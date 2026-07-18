# PT-2026-008 Results

## Validation run
- Validation ID: `VAL-2026-008`
- Technique: `T1197`
- Status: validated

## Positive path
- `bitsadmin.exe /transfer` created a BITS job named `PT-2026-008-Original`
- `Start-BitsTransfer` created a BITS job visible in local BITS Operational logs
- Both positive paths triggered the Sigma detection in Splunk process-creation telemetry

## Negative path
- benign `Get-BitsTransfer` remained quiet
- benign `Get-Service BITS` remained quiet
- benign `bitsadmin.exe /list /allusers` remained quiet
