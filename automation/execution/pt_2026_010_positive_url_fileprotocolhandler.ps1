$ErrorActionPreference='SilentlyContinue'
$marker='C:\Windows\Temp\pt-2026-010-url.txt'
Remove-Item $marker -Force -ErrorAction SilentlyContinue
Start-Process rundll32.exe -ArgumentList 'url.dll,FileProtocolHandler calc.exe'
Start-Sleep -Seconds 3
$calc=Get-Process calc -ErrorAction SilentlyContinue
$ran=[bool]$calc
if($calc){ $calc | Stop-Process -Force }
Set-Content -Path $marker -Value ([string]$ran)
Get-Item $marker | Select-Object FullName,Length,LastWriteTime | Format-List
