$ErrorActionPreference = 'Stop'
$profilePath = $PROFILE
if (Test-Path $profilePath) {
  $lines = Get-Content $profilePath
  $filtered = $lines | Where-Object { $_ -notmatch 'PT-2026-009-(ORIGINAL|VARIANT)|benign note' }
  Set-Content -Path $profilePath -Value $filtered
}
Remove-Item 'C:\Windows\Temp\pt-2026-009-original.txt','C:\Windows\Temp\pt-2026-009-variant.txt' -Force -ErrorAction SilentlyContinue
'cleanup complete'
