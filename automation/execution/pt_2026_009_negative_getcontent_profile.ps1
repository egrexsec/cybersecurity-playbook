$ErrorActionPreference = 'Stop'
if (Test-Path $PROFILE) { Get-Content $PROFILE -Raw | Out-Host } else { 'PROFILE_MISSING' | Out-Host }
