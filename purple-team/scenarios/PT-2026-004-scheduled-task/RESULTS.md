# PT-2026-004 Results

## Validation run
- Validation ID: `VAL-2026-004`
- Technique: `T1053.005`
- Status: validated

## Positive path
- Original scheduled-task creation via `schtasks.exe /Create` succeeded and wrote `C:\Windows\Temp\pt-2026-004-original.txt`
- Modified variant via `Register-ScheduledTask` succeeded and wrote `C:\Windows\Temp\pt-2026-004-variant.txt`
- Both paths generated local Task Scheduler execution records and Splunk-visible Sysmon process creation telemetry

## Negative path
- Benign task query, benign task inventory, and benign scheduled task creation launching `notepad.exe` did not trigger the Sigma detection

## Notes
- During historical validation, the authorized lab endpoint temporarily lost telemetry connectivity. Private addressing and forwarding configuration were restored, after which validation succeeded.
