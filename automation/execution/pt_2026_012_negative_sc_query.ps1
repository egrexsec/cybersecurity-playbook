$ErrorActionPreference = 'Stop'
sc.exe query W32Time | Out-Host
[pscustomobject]@{ Negative='sc-query'; Completed=$true } | ConvertTo-Json -Compress
