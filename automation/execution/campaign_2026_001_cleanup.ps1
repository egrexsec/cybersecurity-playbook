$root='C:\Windows\Temp\dc1-campaign'
$ids=@(Get-Content (Join-Path $root 'process-ids.txt') -ErrorAction SilentlyContinue|Where-Object {$_ -match '^\d+$'}|ForEach-Object {[int]$_})
@(Get-CimInstance Win32_Process -ErrorAction SilentlyContinue|Where-Object {$ids -contains [int]$_.ParentProcessId}|ForEach-Object {[int]$_.ProcessId})+$ids|Sort-Object -Unique|ForEach-Object {Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue}
Remove-Item $root -Recurse -Force -ErrorAction SilentlyContinue
$remaining=@(Get-ChildItem $root -Recurse -ErrorAction SilentlyContinue)
[pscustomobject]@{RecordedProcessIds=$ids;Remaining=@($remaining|ForEach-Object FullName);Clean=($remaining.Count -eq 0)}|ConvertTo-Json -Compress
