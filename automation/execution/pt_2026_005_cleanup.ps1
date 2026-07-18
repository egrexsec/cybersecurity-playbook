$ErrorActionPreference = 'Stop'
$services = @('PT-2026-005-Original','PT-2026-005-Variant','PT-2026-005-Benign')
foreach ($service in $services) { sc.exe delete $service > $null 2>&1 }
Remove-Item 'C:\Windows\Temp\pt-2026-005-original.txt','C:\Windows\Temp\pt-2026-005-variant.txt' -Force -ErrorAction SilentlyContinue
'cleanup complete'
