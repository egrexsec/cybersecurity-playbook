$ErrorActionPreference = 'Stop'
Get-ScheduledTask -TaskName 'Registration' -TaskPath '\Microsoft\Windows\PushToInstall\' | Select-Object TaskName,TaskPath,State | Format-List
