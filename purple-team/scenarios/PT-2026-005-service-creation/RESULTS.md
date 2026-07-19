# PT-2026-005 Results

## Validation run
- Validation ID: `VAL-2026-005`
- Technique: `T1543.003`
- Status: validated

## Positive path
- `sc.exe create` service installation succeeded and produced System 7045 plus Sysmon service-creation process telemetry
- PowerShell `New-Service` variant succeeded and produced System 7045 plus Sysmon process telemetry
- Both positive paths triggered the Sigma detection in Splunk

## Negative path
- benign `sc qc`
- benign `Get-Service`
- benign service creation using `notepad.exe`

All three negative paths stayed quiet.
