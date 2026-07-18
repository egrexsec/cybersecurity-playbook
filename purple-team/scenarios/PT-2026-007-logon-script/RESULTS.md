# PT-2026-007 Results

## Validation run
- Validation ID: `VAL-2026-007`
- Technique: `T1037.001`
- Status: validated

## Positive path
- `reg.exe add` UserInitMprLogonScript persistence succeeded against the safely loaded user hive and wrote `C:\Windows\Temp\pt-2026-007-original.txt`
- PowerShell `Set-ItemProperty` variant succeeded against the safely loaded user hive and wrote `C:\Windows\Temp\pt-2026-007-variant.txt`
- Both positive paths triggered the Sigma detection in Splunk

## Negative path
- benign environment inspection remained quiet
- benign `reg.exe query` remained quiet
- benign calc environment value creation remained quiet
