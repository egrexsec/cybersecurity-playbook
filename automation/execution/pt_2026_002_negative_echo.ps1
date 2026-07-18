cmd.exe /c echo PT-2026-002 benign echo>%TEMP%\pt-2026-002-negative-echo.txt
Get-Item "$env:TEMP\pt-2026-002-negative-echo.txt" | Select-Object FullName,Length,LastWriteTime | Format-List
