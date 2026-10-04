$client=New-Object System.Net.WebClient;[pscustomobject]@{Type=$client.GetType().FullName;NoTransfer=$true}|ConvertTo-Json -Compress;$client.Dispose()
