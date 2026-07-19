$ErrorActionPreference = 'Stop'
$service = 'PT-2026-005-Variant'
$marker = 'C:\Windows\Temp\pt-2026-005-variant.txt'
if (Get-Service $service -ErrorAction SilentlyContinue) {
  sc.exe delete $service > $null 2>&1
  Start-Sleep -Seconds 1
}
if (Test-Path $marker) { Remove-Item $marker -Force }
New-Service -Name $service -BinaryPathName 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -Command "Set-Content -Path C:\Windows\Temp\pt-2026-005-variant.txt -Value PT-2026-005-VARIANT"' -StartupType Manual | Out-Host
Start-Sleep -Seconds 1
Start-Service -Name $service -ErrorAction SilentlyContinue | Out-Null
Start-Sleep -Seconds 3
$exists = Test-Path $marker
[pscustomobject]@{ MarkerExists=$exists } | ConvertTo-Json -Compress | Out-Host
