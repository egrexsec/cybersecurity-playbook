$ErrorActionPreference = 'Continue'
$names = 'AtomicRedTeam-WMIPersistence-CommandLineEventConsumer-Example','PT-2026-013-Variant'
$namespace = 'root/subscription'
$bindingResidue = @()

function Get-NamedBindings {
    param([string]$ObjectName)
    $found = @()
    $consumers = @(Get-WmiObject -Namespace $namespace -Class CommandLineEventConsumer -Filter "Name = '$ObjectName'" -ErrorAction SilentlyContinue)
    foreach ($consumer in $consumers) {
        $found += @(Get-WmiObject -Namespace $namespace -Query "REFERENCES OF {$($consumer.__RELPATH)} WHERE ResultClass = __FilterToConsumerBinding" -ErrorAction SilentlyContinue)
    }
    $filters = @(Get-WmiObject -Namespace $namespace -Class __EventFilter -Filter "Name = '$ObjectName'" -ErrorAction SilentlyContinue)
    foreach ($filter in $filters) {
        $found += @(Get-WmiObject -Namespace $namespace -Query "REFERENCES OF {$($filter.__RELPATH)} WHERE ResultClass = __FilterToConsumerBinding" -ErrorAction SilentlyContinue)
    }
    @($found | Sort-Object -Property __PATH -Unique)
}

foreach ($name in $names) {
    @(Get-NamedBindings -ObjectName $name) | Remove-WmiObject -ErrorAction SilentlyContinue
    Start-Sleep -Milliseconds 250
    $remainingBindings = @(Get-NamedBindings -ObjectName $name)
    if ($remainingBindings.Count -eq 0) {
        @(Get-WmiObject -Namespace $namespace -Class CommandLineEventConsumer -Filter "Name = '$name'" -ErrorAction SilentlyContinue) |
            Remove-WmiObject -ErrorAction SilentlyContinue
        @(Get-WmiObject -Namespace $namespace -Class __EventFilter -Filter "Name = '$name'" -ErrorAction SilentlyContinue) |
            Remove-WmiObject -ErrorAction SilentlyContinue
    } else {
        $bindingResidue += "binding:$name"
    }
}
Remove-Item 'C:\Windows\Temp\pt-2026-013-original-completion.json','C:\Windows\Temp\pt-2026-013-variant-completion.json' -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
$remaining = foreach ($name in $names) {
    if (Get-WmiObject -Namespace $namespace -Class __EventFilter -Filter "Name = '$name'" -ErrorAction SilentlyContinue) { "filter:$name" }
    if (Get-WmiObject -Namespace $namespace -Class CommandLineEventConsumer -Filter "Name = '$name'" -ErrorAction SilentlyContinue) { "consumer:$name" }
}
$remaining = @($bindingResidue) + @($remaining)
$completionFiles = @(
    'C:\Windows\Temp\pt-2026-013-original-completion.json',
    'C:\Windows\Temp\pt-2026-013-variant-completion.json'
) | Where-Object { Test-Path $_ }
[pscustomobject]@{ Remaining=@($remaining); CompletionFiles=@($completionFiles); Clean=(@($remaining).Count -eq 0 -and @($completionFiles).Count -eq 0) } | ConvertTo-Json -Compress
if (@($remaining).Count -ne 0 -or @($completionFiles).Count -ne 0) { throw 'WMI subscription cleanup residue remains' }
