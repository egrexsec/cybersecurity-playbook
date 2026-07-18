$paths = @(
  (Join-Path $env:TEMP 'pt-2026-003-wmic-positive.txt'),
  (Join-Path $env:TEMP 'pt-2026-003-invoke-wmi-positive.txt')
)
foreach ($path in $paths) {
  if (Test-Path $path) { Remove-Item $path -Force }
}
Get-ChildItem $env:TEMP -Filter 'pt-2026-003-*' -ErrorAction SilentlyContinue | Select-Object FullName,Length,LastWriteTime
