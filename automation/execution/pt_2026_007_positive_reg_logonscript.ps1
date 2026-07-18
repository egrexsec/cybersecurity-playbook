$ErrorActionPreference = 'Stop'
$hive = 'HKU\PT2026007'
$key = 'Registry::HKEY_USERS\PT2026007\Environment'
$name = 'UserInitMprLogonScript'
$scriptPath = 'C:\Windows\Temp\pt-2026-007-original.bat'
$marker = 'C:\Windows\Temp\pt-2026-007-original.txt'
cmd.exe /c "reg unload HKU\PT2026007 >nul 2>&1"
cmd.exe /c "reg load HKU\PT2026007 C:\Users\mell0wx\NTUSER.DAT" | Out-Host
Remove-Item $scriptPath,$marker -Force -ErrorAction SilentlyContinue
"echo PT-2026-007-ORIGINAL > C:\Windows\Temp\pt-2026-007-original.txt" | Set-Content -Path $scriptPath -Encoding ascii
reg.exe add "$hive\Environment" /v "$name" /t REG_SZ /f /d "$scriptPath" | Out-Host
& cmd.exe /c $scriptPath
Get-ItemProperty -Path $key -Name $name | ConvertTo-Json -Compress | Out-Host
Get-Item $marker | Select-Object FullName,Length,LastWriteTime | Format-List
cmd.exe /c "reg unload HKU\PT2026007" | Out-Host
