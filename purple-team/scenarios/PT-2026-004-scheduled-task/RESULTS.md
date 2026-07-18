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
- During validation, the victim temporarily lost its enterprise IPv4 address and the Splunk Universal Forwarder stopped sending to SOC01. The address was restored to `10.10.10.101/24`, connectivity to `10.10.10.20:9997` was re-established, and live Splunk validation then succeeded.
