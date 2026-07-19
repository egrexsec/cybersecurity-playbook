$ErrorActionPreference = 'Stop'
$key = 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Run'
foreach ($name in @('PT-2026-006-Original','PT-2026-006-Variant','PT-2026-006-Benign')) {
  Remove-ItemProperty -Path $key -Name $name -Force -ErrorAction SilentlyContinue
}
Remove-Item 'C:\Windows\Temp\pt-2026-006-original.txt','C:\Windows\Temp\pt-2026-006-variant.txt' -Force -ErrorAction SilentlyContinue
'cleanup complete'
