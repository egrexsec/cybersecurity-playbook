# PT-2026-003 Results

## Summary
Validated low-risk WMI execution coverage on the approved Windows victim using two positive paths and two benign negatives.

## Positive paths
1. `[wmiclass]'Win32_Process'` PowerShell initiation with marker `pt-2026-003-wmic-positive.txt`
2. `Invoke-WmiMethod -Path Win32_Process -Name Create ...` with marker `pt-2026-003-invoke-wmi-positive.txt`

## Detection outcomes
- `100205` fired for the `[wmiclass]` initiation path
- `100206` fired for the `Invoke-WmiMethod` WMI-backed process creation path

## Negative outcomes
- `Get-CimInstance Win32_OperatingSystem` generated no custom PT detection
- `Get-WmiObject Win32_Service -Filter "Name='Spooler'"` generated no custom PT detection

## Telemetry notes
- Victim Sysmon recorded `cmd.exe` children with parent `WmiPrvSE.exe`
- Wazuh received the relevant PowerShell and Sysmon telemetry and produced the expected custom alerts

## Cleanup
Temporary marker files under `%TEMP%` were removed with `pt_2026_003_cleanup.ps1`.
