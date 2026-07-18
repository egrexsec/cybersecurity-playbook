$ErrorActionPreference = 'Stop'
$now = Get-Date
$start = $now.AddMinutes(-30)
$result = [ordered]@{
  collected_at_utc = (Get-Date).ToUniversalTime().ToString('o')
  window_start_utc = $start.ToUniversalTime().ToString('o')
  hostname = $env:COMPUTERNAME
  counts = [ordered]@{
    powershell_4103 = ((Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-PowerShell/Operational'; Id=4103; StartTime=$start} -ErrorAction SilentlyContinue) | Measure-Object).Count
    powershell_4104 = ((Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-PowerShell/Operational'; Id=4104; StartTime=$start} -ErrorAction SilentlyContinue) | Measure-Object).Count
    security_4688_powershell = ((Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4688; StartTime=$start} -ErrorAction SilentlyContinue | Where-Object { $_.Message -match 'powershell.exe|pwsh.exe' }) | Measure-Object).Count
    sysmon_1_powershell = ((Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Sysmon/Operational'; Id=1; StartTime=$start} -ErrorAction SilentlyContinue | Where-Object { $_.Message -match 'powershell.exe|pwsh.exe' }) | Measure-Object).Count
  }
}
$result | ConvertTo-Json -Depth 4
