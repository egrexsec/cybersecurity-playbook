$ErrorActionPreference = 'Continue'
$services = 'PT-2026-012-Original','PT-2026-012-Variant','PT-2026-012-Benign'
foreach ($service in $services) {
    sc.exe stop $service > $null 2>&1
    sc.exe delete $service > $null 2>&1
}
$artifacts = @(
    'C:\Windows\Temp\pt-2026-012-original.txt',
    'C:\Windows\Temp\pt-2026-012-variant.txt',
    'C:\Windows\Temp\pt-2026-012-original-result.json',
    'C:\Windows\Temp\pt-2026-012-variant-result.json',
    'C:\art-marker.txt'
)
foreach ($artifact in $artifacts) { Remove-Item $artifact -Force -ErrorAction SilentlyContinue }
Start-Sleep -Seconds 2
[pscustomobject]@{
  ServicesRemaining=@($services | Where-Object { Get-Service $_ -ErrorAction SilentlyContinue })
  ArtifactsRemaining=@($artifacts | Where-Object { Test-Path $_ })
} | ConvertTo-Json -Compress
