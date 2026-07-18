Get-Date | Out-File -FilePath "$env:TEMP\pt-2026-001-negative-date.txt" -Encoding utf8
Get-Item "$env:TEMP\pt-2026-001-negative-date.txt" | Select-Object FullName,Length,LastWriteTime | Format-List
