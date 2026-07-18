$ErrorActionPreference = 'Stop'
$service = 'PT-2026-005-Benign'
sc.exe delete $service > $null 2>&1
sc.exe create $service binPath= "C:\Windows\System32\notepad.exe" start= demand | Out-Host
Start-Sleep -Seconds 1
sc.exe delete $service | Out-Host
'benign service create cleanup complete'
