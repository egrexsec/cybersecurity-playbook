$ErrorActionPreference = 'Stop'
Set-ExecutionPolicy -Scope Process Bypass -Force
$testGuid = '3c64f177-28e2-49eb-a799-d767b24dd1e0'
$name = 'AtomicRedTeam-WMIPersistence-CommandLineEventConsumer-Example'
Import-Module Invoke-AtomicRedTeam -Force
Invoke-AtomicTest T1546.003 -TestGuids $testGuid -PathToAtomicsFolder 'C:\Tools\AtomicRedTeam\atomics' -Confirm:$false
$deadline = (Get-Date).AddSeconds(30)
do {
    $filter = Get-WmiObject -Namespace root/subscription -Class __EventFilter -Filter "Name = '$name'" -ErrorAction SilentlyContinue
    $consumer = Get-WmiObject -Namespace root/subscription -Class CommandLineEventConsumer -Filter "Name = '$name'" -ErrorAction SilentlyContinue
    $binding = if ($consumer) {
        Get-WmiObject -Namespace root/subscription -Query "REFERENCES OF {$($consumer.__RELPATH)} WHERE ResultClass = __FilterToConsumerBinding" -ErrorAction SilentlyContinue
    }
    if ($filter -and $consumer -and $binding) { break }
    Start-Sleep -Seconds 1
} while ((Get-Date) -lt $deadline)
$result = [pscustomobject]@{
    TestGuid = $testGuid
    FilterPresent = [bool]$filter
    ConsumerPresent = [bool]$consumer
    BindingPresent = [bool]$binding
    CompletedAt = (Get-Date).ToUniversalTime().ToString('o')
}
if (-not ($result.FilterPresent -and $result.ConsumerPresent -and $result.BindingPresent)) { throw 'Atomic WMI subscription was not fully created' }
$completionPath = 'C:\Windows\Temp\pt-2026-013-original-completion.json'
$result | ConvertTo-Json -Compress | Set-Content -Path $completionPath -Encoding UTF8
$result | ConvertTo-Json -Compress
