$ErrorActionPreference='SilentlyContinue'
Remove-Item 'C:\Windows\Temp\pt-2026-011-shell32.jpg','C:\Windows\Temp\pt-2026-011-jpg.txt','C:\Windows\Temp\pt-2026-011-sct.txt' -Force -ErrorAction SilentlyContinue
Remove-Item 'C:\Windows\Temp\pt-2026-011\empty.sct' -Force -ErrorAction SilentlyContinue
Remove-Item 'C:\Windows\Temp\pt-2026-011' -Force -ErrorAction SilentlyContinue
Get-Process regsvr32 -ErrorAction SilentlyContinue | Stop-Process -Force
'cleanup complete'
