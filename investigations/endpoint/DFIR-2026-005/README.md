# DFIR-2026-005

## Scope
Windows service creation and execution on the approved Windows victim for `PT-2026-005`.

## Key findings
- System 7045 service installation events confirmed both positive paths.
- System 7000/7009 documented expected service start failures when the configured binary was not a real service host.
- Sysmon captured the service-creation command lines used for both positives.
- Benign inspection and benign notepad service creation did not trigger the Sigma detection.
- Cleanup removed the created services and markers.

## Time anchors
- Original positive start: `2026-07-18T16:38:32.050452Z`
- Variant positive start: `2026-07-18T16:38:48.714894Z`
