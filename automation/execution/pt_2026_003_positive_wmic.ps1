$marker = Join-Path $env:TEMP 'pt-2026-003-wmic-positive.txt'
if (Test-Path $marker) { Remove-Item $marker -Force }
$null = ([wmiclass]'Win32_Process').Create('cmd.exe /c echo PT-2026-003-WMIC>%TEMP%\pt-2026-003-wmic-positive.txt')
Start-Sleep -Seconds 3
Get-Item $marker | Select-Object FullName,Length,LastWriteTime | Format-List
