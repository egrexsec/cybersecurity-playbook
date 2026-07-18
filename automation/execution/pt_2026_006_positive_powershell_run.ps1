$ErrorActionPreference = 'Stop'
$key = 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Run'
$name = 'PT-2026-006-Variant'
$marker = 'C:\Windows\Temp\pt-2026-006-variant.txt'
Remove-ItemProperty -Path $key -Name $name -Force -ErrorAction SilentlyContinue
if (Test-Path $marker) { Remove-Item $marker -Force }
Set-ItemProperty -Path $key -Name $name -Value 'powershell.exe -NoProfile -WindowStyle Hidden -Command "Set-Content -Path C:\Windows\Temp\pt-2026-006-variant.txt -Value PT-2026-006-VARIANT"'
Set-Content -Path $marker -Value 'PT-2026-006-VARIANT'
Get-ItemProperty -Path $key -Name $name | ConvertTo-Json -Compress | Out-Host
Get-Item $marker | Select-Object FullName,Length,LastWriteTime | Format-List
