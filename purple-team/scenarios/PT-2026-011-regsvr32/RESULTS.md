# PT-2026-011 Results

## Validation run
- Validation ID: `VAL-2026-011`
- Technique: `T1218.010`
- Status: validated

## Positive path
- `regsvr32.exe /s C:\Windows\Temp\pt-2026-011-shell32.jpg` generated suspicious regsvr32 telemetry and non-DLL image-load evidence
- `regsvr32.exe /s /u /i:C:\Windows\Temp\pt-2026-011\empty.sct scrobj.dll` generated suspicious regsvr32 SCT telemetry
- both positive paths triggered the Sigma detection in Splunk

## Negative path
- benign DLL registration remained quiet
- benign regsvr32 help invocation remained quiet
- benign registry query remained quiet
