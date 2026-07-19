# PT-2026-006 Results

## Validation run
- Validation ID: `VAL-2026-006`
- Technique: `T1547.001`
- Status: validated

## Positive path
- `reg.exe add` Run-key persistence succeeded and stored a suspicious `cmd.exe` temp-path value
- PowerShell `Set-ItemProperty` variant succeeded and stored a hidden `powershell.exe` temp-path value
- Both positive paths triggered the Sigma detection in Splunk

## Negative path
- benign PowerShell Run-key inspection remained quiet
- benign `reg.exe query` remained quiet
- benign calc Run value creation remained quiet
