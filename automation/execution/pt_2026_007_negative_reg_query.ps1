$ErrorActionPreference = 'Stop'
cmd.exe /c "reg unload HKU\PT2026007 >nul 2>&1"
cmd.exe /c "reg load HKU\PT2026007 C:\Users\mell0wx\NTUSER.DAT" | Out-Host
reg.exe query "HKU\PT2026007\Environment" | Out-Host
cmd.exe /c "reg unload HKU\PT2026007" | Out-Host
