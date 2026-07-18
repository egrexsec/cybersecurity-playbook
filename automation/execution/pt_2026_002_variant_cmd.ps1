$ErrorActionPreference = 'Stop'
$markerPath = Join-Path $env:SystemRoot 'Temp\pt-2026-002-variant.txt'
cmd.exe /c "%LOCALAPPDATA:~-3,1%md /c echo PT-2026-002 suspicious variant > %SystemRoot%\Temp\pt-2026-002-variant.txt & type %SystemRoot%\Temp\pt-2026-002-variant.txt"
Get-Item $markerPath | Select-Object FullName,Length,LastWriteTime | Format-List
