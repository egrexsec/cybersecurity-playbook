$ErrorActionPreference = 'Stop'
Remove-Item -Path "$env:SystemRoot\Temp\art-marker.txt" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$env:SystemRoot\Temp\variant-marker.txt" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$env:TEMP\pt-2026-001-negative-date.txt" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$env:TEMP\pt-2026-001-negative-process.txt" -Force -ErrorAction SilentlyContinue
Remove-Item 'HKCU:\Software\Classes\AtomicRedTeam' -Force -ErrorAction SilentlyContinue
'cleanup complete'
