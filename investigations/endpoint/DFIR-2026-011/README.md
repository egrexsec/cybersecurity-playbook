# DFIR-2026-011

## Scope
Regsvr32 proxy execution on the approved Windows victim for `PT-2026-011`.

## Key findings
- Sysmon process creation captured regsvr32 with both the non-DLL target and SCT/scrobj path.
- Image-load telemetry showed regsvr32 loading the `.jpg` target and `scrobj.dll`.
- Benign DLL registration and help output did not trigger the Sigma rule.
- Cleanup removed temp artifacts and residual regsvr32 processes.

## Time anchors
- Original positive start: `2026-07-18T20:55:27.041956Z`
- Variant positive start: `2026-07-18T20:55:39.225647Z`
