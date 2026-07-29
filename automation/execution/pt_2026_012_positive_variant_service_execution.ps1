$ErrorActionPreference = 'Stop'
$service = 'PT-2026-012-Variant'
$marker = 'C:\Windows\Temp\pt-2026-012-variant.txt'
$resultPath = 'C:\Windows\Temp\pt-2026-012-variant-result.json'
sc.exe stop $service > $null 2>&1
sc.exe delete $service > $null 2>&1
Remove-Item $marker,$resultPath -Force -ErrorAction SilentlyContinue
Import-Module Invoke-AtomicRedTeam -Force
$inputArgs = @{
    service_name = $service
    executable_command = '%COMSPEC% /d /c echo PT-2026-012-VARIANT>C:\Windows\Temp\pt-2026-012-variant.txt'
}
Invoke-AtomicTest T1569.002 -TestGuids '2382dee2-a75f-49aa-9378-f52df6ed3fb1' -InputArgs $inputArgs -PathToAtomicsFolder 'C:\Tools\AtomicRedTeam\atomics' -Confirm:$false
Start-Sleep -Seconds 5
$record = [pscustomobject]@{
    TestGuid = '2382dee2-a75f-49aa-9378-f52df6ed3fb1'
    Service = $service
    Marker = $marker
    MarkerExists = (Test-Path $marker)
    CompletedAt = (Get-Date).ToUniversalTime().ToString('o')
}
$record | ConvertTo-Json -Compress | Set-Content -LiteralPath $resultPath -Encoding UTF8
$record | ConvertTo-Json -Compress
if (-not $record.MarkerExists) { throw 'Variant service execution marker was not created' }
