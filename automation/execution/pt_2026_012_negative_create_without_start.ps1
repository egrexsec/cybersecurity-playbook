$ErrorActionPreference = 'Stop'
$service = 'PT-2026-012-Benign'
sc.exe delete $service > $null 2>&1
sc.exe create $service binPath= 'C:\Windows\System32\svchost.exe -k LocalService' start= demand | Out-Host
Start-Sleep -Seconds 1
sc.exe delete $service | Out-Host
[pscustomobject]@{ Negative='service-create-without-start'; Completed=$true } | ConvertTo-Json -Compress
