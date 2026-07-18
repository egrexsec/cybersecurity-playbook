cmd.exe /c "dir %SystemRoot%\Temp > %TEMP%\pt-2026-002-negative-dir.txt"
Get-Item "$env:TEMP\pt-2026-002-negative-dir.txt" | Select-Object FullName,Length,LastWriteTime | Format-List
