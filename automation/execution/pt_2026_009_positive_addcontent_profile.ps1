$ErrorActionPreference = 'Stop'
$profilePath = $PROFILE
$marker = 'C:\Windows\Temp\pt-2026-009-original.txt'
New-Item -ItemType Directory -Force -Path (Split-Path $profilePath) | Out-Null
if (!(Test-Path $profilePath)) { New-Item -ItemType File -Path $profilePath -Force | Out-Null }
$existing = Get-Content $profilePath -Raw -ErrorAction SilentlyContinue
Set-Content -Path $profilePath -Value $existing
Add-Content $profilePath -Value "Set-Content -Path 'C:\Windows\Temp\pt-2026-009-original.txt' -Value 'PT-2026-009-ORIGINAL'"
powershell.exe -Command exit
Get-Item $marker | Select-Object FullName,Length,LastWriteTime | Format-List
