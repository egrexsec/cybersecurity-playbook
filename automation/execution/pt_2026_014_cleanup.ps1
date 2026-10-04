$root='C:\Windows\Temp\dc1-t1105'
Remove-Item $root -Recurse -Force -ErrorAction SilentlyContinue
$remaining=@(Get-ChildItem $root -Recurse -ErrorAction SilentlyContinue)
[pscustomobject]@{Remaining=@($remaining|ForEach-Object FullName);Clean=($remaining.Count -eq 0)}|ConvertTo-Json -Compress
