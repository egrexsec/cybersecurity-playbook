$ErrorActionPreference = 'Stop'
[ordered]@{
  hostname = $env:COMPUTERNAME
  timestamp_utc = (Get-Date).ToUniversalTime().ToString('o')
  secure_channel = (Test-ComputerSecureChannel)
  sysmon_service = (Get-Service Sysmon64 -ErrorAction SilentlyContinue | Select-Object Name,Status)
  wazuh_service = (Get-Service WazuhSvc -ErrorAction SilentlyContinue | Select-Object Name,Status)
  powershell_log_records = ((wevtutil gli Microsoft-Windows-PowerShell/Operational | Select-String 'numberOfLogRecords').ToString())
} | ConvertTo-Json -Depth 4
