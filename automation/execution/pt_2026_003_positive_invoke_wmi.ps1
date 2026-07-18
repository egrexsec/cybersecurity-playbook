$marker = Join-Path $env:TEMP 'pt-2026-003-invoke-wmi-positive.txt'
if (Test-Path $marker) { Remove-Item $marker -Force }
Invoke-WmiMethod -Path Win32_Process -Name Create -ArgumentList 'cmd.exe /c echo PT-2026-003-INVOKE-WMI>%TEMP%\pt-2026-003-invoke-wmi-positive.txt' | Out-Null
Start-Sleep -Seconds 3
Get-Item $marker | Select-Object FullName,Length,LastWriteTime | Format-List
