$ErrorActionPreference = 'Stop'
$key = 'HKLM\Software\Microsoft\Windows\CurrentVersion\Run'
$name = 'PT-2026-006-Original'
$marker = 'C:\Windows\Temp\pt-2026-006-original.txt'
cmd.exe /c "reg delete \"HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\" /v \"PT-2026-006-Original\" /f >nul 2>&1"
Remove-Item $marker -Force -ErrorAction SilentlyContinue
reg.exe add "$key" /v "$name" /t REG_SZ /f /d 'cmd.exe /c echo PT-2026-006-ORIGINAL > C:\Windows\Temp\pt-2026-006-original.txt' | Out-Host
& cmd.exe /c echo PT-2026-006-ORIGINAL > C:\Windows\Temp\pt-2026-006-original.txt
Get-ItemProperty -Path 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Run' -Name $name | ConvertTo-Json -Compress | Out-Host
Get-Item $marker | Select-Object FullName,Length,LastWriteTime | Format-List
