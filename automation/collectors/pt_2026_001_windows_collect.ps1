param(
  [Parameter(Mandatory=$true)][string]$StartUtc,
  [Parameter(Mandatory=$true)][string]$EndUtc
)
$ErrorActionPreference = 'Stop'
$start = [DateTime]::Parse($StartUtc).ToUniversalTime()
$end = [DateTime]::Parse($EndUtc).ToUniversalTime()
$procEvents = Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Sysmon/Operational'; Id=1; StartTime=$start; EndTime=$end} -ErrorAction SilentlyContinue |
  Where-Object { $_.Message -match 'powershell.exe|pwsh.exe|reg.exe' } |
  Select-Object TimeCreated, Id, ProviderName, RecordId, Message
$psEvents = Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-PowerShell/Operational'; StartTime=$start; EndTime=$end} -ErrorAction SilentlyContinue |
  Where-Object { $_.Id -in 4103,4104 } |
  Select-Object TimeCreated, Id, ProviderName, RecordId, Message
$secEvents = Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4688; StartTime=$start; EndTime=$end} -ErrorAction SilentlyContinue |
  Where-Object { $_.Message -match 'powershell.exe|pwsh.exe|reg.exe' } |
  Select-Object TimeCreated, Id, ProviderName, RecordId, Message
[ordered]@{
  collected_at_utc = (Get-Date).ToUniversalTime().ToString('o')
  start_utc = $start.ToString('o')
  end_utc = $end.ToString('o')
  hostname = $env:COMPUTERNAME
  sysmon_process_events = $procEvents
  powershell_events = $psEvents
  security_process_events = $secEvents
} | ConvertTo-Json -Depth 6
