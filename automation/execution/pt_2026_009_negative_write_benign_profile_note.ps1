$ErrorActionPreference = 'Stop'
$profilePath = $PROFILE
New-Item -ItemType Directory -Force -Path (Split-Path $profilePath) | Out-Null
if (!(Test-Path $profilePath)) { New-Item -ItemType File -Path $profilePath -Force | Out-Null }
Add-Content $profilePath -Value "# benign note"
(Get-Item $profilePath).FullName | Out-Host
