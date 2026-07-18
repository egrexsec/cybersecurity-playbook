# PT-2026-010 Results

## Validation run
- Validation ID: `VAL-2026-010`
- Technique: `T1218.011`
- Status: validated

## Positive path
- `rundll32.exe url.dll,FileProtocolHandler calc.exe` generated suspicious rundll32 process telemetry and marker confirmation
- `rundll32.exe pcwutl.dll,LaunchApplication calc.exe` generated suspicious rundll32 process telemetry and marker confirmation
- both positive paths triggered the Sigma detection in Splunk

## Negative path
- benign `Control_RunDLL` style rundll32 usage remained quiet
- benign control.exe launch remained quiet
