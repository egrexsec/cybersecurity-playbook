$ErrorActionPreference='SilentlyContinue'
Get-Process calc -ErrorAction SilentlyContinue | Stop-Process -Force
Get-Process rundll32 -ErrorAction SilentlyContinue | Stop-Process -Force
Remove-Item 'C:\Windows\Temp\pt-2026-010-url.txt','C:\Windows\Temp\pt-2026-010-pcwu.txt' -Force -ErrorAction SilentlyContinue
'cleanup complete'
