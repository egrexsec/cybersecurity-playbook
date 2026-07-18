$ErrorActionPreference = 'Stop'
$task = 'PT-2026-004-Variant'
$marker = 'C:\Windows\Temp\pt-2026-004-variant.txt'
if (Get-ScheduledTask -TaskName $task -ErrorAction SilentlyContinue) {
  Unregister-ScheduledTask -TaskName $task -Confirm:$false
}
if (Test-Path $marker) { Remove-Item $marker -Force }
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-NoProfile -Command "Set-Content -Path C:\Windows\Temp\pt-2026-004-variant.txt -Value PT-2026-004-VARIANT"'
$trigger = New-ScheduledTaskTrigger -Once -At ((Get-Date).AddMinutes(5))
$principal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName $task -Action $action -Trigger $trigger -Principal $principal | Out-Host
Start-ScheduledTask -TaskName $task
Start-Sleep -Seconds 8
Get-Item $marker | Select-Object FullName,Length,LastWriteTime | Format-List
