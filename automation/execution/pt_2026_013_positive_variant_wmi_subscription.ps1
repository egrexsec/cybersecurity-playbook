$ErrorActionPreference = 'Stop'
$name = 'PT-2026-013-Variant'
$namespace = 'root/subscription'
$filterArgs = @{
    Name = $name
    EventNameSpace = 'root\CimV2'
    QueryLanguage = 'WQL'
    Query = "SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System' AND TargetInstance.SystemUpTime > 99999999"
}
$consumerArgs = @{
    Name = $name
    CommandLineTemplate = "$env:SystemRoot\System32\cmd.exe /c exit 0"
}
$filter = New-CimInstance -Namespace $namespace -ClassName __EventFilter -Property $filterArgs
$consumer = New-CimInstance -Namespace $namespace -ClassName CommandLineEventConsumer -Property $consumerArgs
$binding = New-CimInstance -Namespace $namespace -ClassName __FilterToConsumerBinding -Property @{ Filter=[Ref]$filter; Consumer=[Ref]$consumer }
$deadline = (Get-Date).AddSeconds(30)
do {
    $persistedFilter = Get-WmiObject -Namespace $namespace -Class __EventFilter -Filter "Name = '$name'" -ErrorAction SilentlyContinue
    $persistedConsumer = Get-WmiObject -Namespace $namespace -Class CommandLineEventConsumer -Filter "Name = '$name'" -ErrorAction SilentlyContinue
    $persistedBinding = if ($persistedConsumer) {
        Get-WmiObject -Namespace $namespace -Query "REFERENCES OF {$($persistedConsumer.__RELPATH)} WHERE ResultClass = __FilterToConsumerBinding" -ErrorAction SilentlyContinue
    }
    $filterPresent = [bool]$persistedFilter
    $consumerPresent = [bool]$persistedConsumer
    $bindingPresent = [bool]$persistedBinding
    if ($filterPresent -and $consumerPresent -and $bindingPresent) { break }
    Start-Sleep -Seconds 1
} while ((Get-Date) -lt $deadline)
$result = [pscustomobject]@{
    FilterPresent = $filterPresent
    ConsumerPresent = $consumerPresent
    BindingPresent = $bindingPresent
    CompletedAt = (Get-Date).ToUniversalTime().ToString('o')
}
if (-not ($result.FilterPresent -and $result.ConsumerPresent -and $result.BindingPresent)) { throw 'Variant WMI subscription was not fully created' }
$completionPath = 'C:\Windows\Temp\pt-2026-013-variant-completion.json'
$result | ConvertTo-Json -Compress | Set-Content -Path $completionPath -Encoding UTF8
$result | ConvertTo-Json -Compress
