$ErrorActionPreference = 'Stop'
$service = 'PT-2026-005-Original'
$marker = 'C:\Windows\Temp\pt-2026-005-original.txt'
sc.exe delete $service > $null 2>&1
if (Test-Path $marker) { Remove-Item $marker -Force }
sc.exe create $service binPath= "C:\Windows\System32\cmd.exe /c echo PT-2026-005-ORIGINAL > C:\Windows\Temp\pt-2026-005-original.txt" start= demand | Out-Host
Start-Sleep -Seconds 1
sc.exe start $service | Out-Host
Start-Sleep -Seconds 3
$exists = Test-Path $marker
[pscustomobject]@{ MarkerExists=$exists } | ConvertTo-Json -Compress | Out-Host
