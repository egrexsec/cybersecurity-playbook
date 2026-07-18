$ErrorActionPreference = 'Stop'
$tasks = @('PT-2026-004-Original', 'PT-2026-004-Variant', 'PT-2026-004-Benign')
foreach ($task in $tasks) {
  if (Get-ScheduledTask -TaskName $task -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $task -Confirm:$false -ErrorAction SilentlyContinue | Out-Null
  }
}
$markers = @(
  'C:\Windows\Temp\pt-2026-004-original.txt',
  'C:\Windows\Temp\pt-2026-004-variant.txt'
)
foreach ($marker in $markers) {
  Remove-Item $marker -Force -ErrorAction SilentlyContinue
}
'cleanup complete'
