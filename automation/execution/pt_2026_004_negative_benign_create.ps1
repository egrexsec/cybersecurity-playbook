$ErrorActionPreference = 'Stop'
$task = 'PT-2026-004-Benign'
if (Get-ScheduledTask -TaskName $task -ErrorAction SilentlyContinue) {
  Unregister-ScheduledTask -TaskName $task -Confirm:$false
}
$start = (Get-Date).AddMinutes(5).ToString('HH:mm')
schtasks.exe /Create /SC ONCE /TN $task /TR 'notepad.exe' /ST $start /RU SYSTEM /F | Out-Host
schtasks.exe /Run /TN $task | Out-Host
Start-Sleep -Seconds 3
schtasks.exe /Delete /TN $task /F | Out-Host
'benign task create cleanup complete'
