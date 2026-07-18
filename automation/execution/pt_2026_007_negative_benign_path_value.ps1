$ErrorActionPreference = 'Stop'
$hive = 'HKU\PT2026007'
$name = 'PT-2026-007-Benign'
cmd.exe /c "reg unload HKU\PT2026007 >nul 2>&1"
cmd.exe /c "reg load HKU\PT2026007 C:\Users\mell0wx\NTUSER.DAT" | Out-Host
cmd.exe /c "reg delete HKU\PT2026007\Environment /v PT-2026-007-Benign /f >nul 2>&1"
reg.exe add "$hive\Environment" /v "$name" /t REG_SZ /f /d "C:\Windows\System32\calc.exe" | Out-Host
reg.exe delete "$hive\Environment" /v "$name" /f | Out-Host
cmd.exe /c "reg unload HKU\PT2026007" | Out-Host
'benign logon-script cleanup complete'
