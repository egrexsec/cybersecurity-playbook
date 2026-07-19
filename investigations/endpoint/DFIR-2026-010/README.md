# DFIR-2026-010

## Scope
Rundll32 proxy execution on the approved Windows victim for `PT-2026-010`.

## Key findings
- Sysmon process creation captured both suspicious rundll32 argument patterns.
- Marker files confirmed both positive paths reached the intended execution checkpoint.
- Benign control-panel style invocation did not trigger the Sigma rule.
- Cleanup removed residual rundll32/calc state and marker files.

## Time anchors
- Original positive start: `2026-07-18T20:20:13.440558Z`
- Variant positive start: `2026-07-18T20:20:29.357623Z`
