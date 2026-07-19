$ErrorActionPreference = 'Stop'
$key = 'HKLM\Software\Microsoft\Windows\CurrentVersion\Run'
$name = 'PT-2026-006-Benign'
cmd.exe /c "reg delete \"HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\" /v \"PT-2026-006-Benign\" /f >nul 2>&1"
reg.exe add "$key" /v "$name" /t REG_SZ /f /d 'C:\Windows\System32\calc.exe' | Out-Host
reg.exe delete "$key" /v "$name" /f | Out-Host
'benign run key cleanup complete'
