$ErrorActionPreference = 'Stop'
$profilePath = $PROFILE
$marker = 'C:\Windows\Temp\pt-2026-009-variant.txt'
New-Item -ItemType Directory -Force -Path (Split-Path $profilePath) | Out-Null
if (!(Test-Path $profilePath)) { New-Item -ItemType File -Path $profilePath -Force | Out-Null }
$payload = "`nSet-Content -Path 'C:\Windows\Temp\pt-2026-009-variant.txt' -Value 'PT-2026-009-VARIANT'"
$payload | Add-Content -Path $profilePath
powershell.exe -Command exit
Get-Item $marker | Select-Object FullName,Length,LastWriteTime | Format-List
