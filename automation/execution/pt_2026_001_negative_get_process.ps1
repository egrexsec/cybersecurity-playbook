Get-Process | Select-Object -First 5 Name,Id | Out-File -FilePath "$env:TEMP\pt-2026-001-negative-process.txt" -Encoding utf8
Get-Item "$env:TEMP\pt-2026-001-negative-process.txt" | Select-Object FullName,Length,LastWriteTime | Format-List
