# DFIR-2026-006

## Scope
Registry Run-key persistence on the approved Windows victim for `PT-2026-006`.

## Key findings
- HKLM Run values were created for both positive paths and confirmed locally.
- Sysmon process creation captured both the `reg.exe add` path and the PowerShell `Set-ItemProperty` path.
- The PowerShell variant also generated Sysmon registry set telemetry for the Run key.
- Benign Run-key inspection and benign calc startup value creation did not trigger the Sigma rule.
- Cleanup removed the created Run values and marker files.

## Time anchors
- Original positive start: `2026-07-18T18:35:03.008078Z`
- Variant positive start: `2026-07-18T18:35:16.165972Z`
