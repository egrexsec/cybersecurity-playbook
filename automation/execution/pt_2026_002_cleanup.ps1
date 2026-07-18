$ErrorActionPreference = 'SilentlyContinue'
$paths = @(
  (Join-Path $env:TEMP 'pt-2026-002-positive.cmd'),
  (Join-Path $env:SystemRoot 'Temp\pt-2026-002-positive.txt'),
  (Join-Path $env:SystemRoot 'Temp\pt-2026-002-variant.txt'),
  (Join-Path $env:TEMP 'pt-2026-002-negative-dir.txt'),
  (Join-Path $env:TEMP 'pt-2026-002-negative-echo.txt')
)
foreach ($path in $paths) {
  Remove-Item $path -Force -ErrorAction SilentlyContinue
}
'cleanup complete'
