$ErrorActionPreference = 'Stop'
$key = 'Registry::HKEY_USERS\PT2026007\Environment'
cmd.exe /c "reg unload HKU\PT2026007 >nul 2>&1"
cmd.exe /c "reg load HKU\PT2026007 C:\Users\mell0wx\NTUSER.DAT" | Out-Host
foreach ($name in @('UserInitMprLogonScript','PT-2026-007-Benign')) {
  Remove-ItemProperty -Path $key -Name $name -Force -ErrorAction SilentlyContinue
}
cmd.exe /c "reg unload HKU\PT2026007" | Out-Host
Remove-Item 'C:\Windows\Temp\pt-2026-007-original.bat','C:\Windows\Temp\pt-2026-007-original.txt','C:\Windows\Temp\pt-2026-007-variant.bat','C:\Windows\Temp\pt-2026-007-variant.txt' -Force -ErrorAction SilentlyContinue
'cleanup complete'
