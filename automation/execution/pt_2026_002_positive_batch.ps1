$ErrorActionPreference = 'Stop'
$scriptPath = Join-Path $env:TEMP 'pt-2026-002-positive.cmd'
$markerPath = Join-Path $env:SystemRoot 'Temp\pt-2026-002-positive.txt'
@"
@echo off
echo PT-2026-002 batch positive>"%SystemRoot%\Temp\pt-2026-002-positive.txt"
type "%SystemRoot%\Temp\pt-2026-002-positive.txt"
"@ | Set-Content -Path $scriptPath -Encoding ascii
cmd.exe /c $scriptPath
Get-Item $markerPath | Select-Object FullName,Length,LastWriteTime | Format-List
