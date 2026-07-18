$ErrorActionPreference = 'Stop'
$task = 'PT-2026-004-Original'
$marker = 'C:\Windows\Temp\pt-2026-004-original.txt'
if (Get-ScheduledTask -TaskName $task -ErrorAction SilentlyContinue) {
  Unregister-ScheduledTask -TaskName $task -Confirm:$false
}
if (Test-Path $marker) { Remove-Item $marker -Force }
$start = (Get-Date).AddMinutes(5).ToString('HH:mm')
schtasks.exe /Create /SC ONCE /TN $task /TR 'cmd.exe /c echo PT-2026-004-ORIGINAL> C:\Windows\Temp\pt-2026-004-original.txt' /ST $start /RU SYSTEM /F | Out-Host
schtasks.exe /Run /TN $task | Out-Host
Start-Sleep -Seconds 8
Get-Item $marker | Select-Object FullName,Length,LastWriteTime | Format-List
