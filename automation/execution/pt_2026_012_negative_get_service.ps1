$ErrorActionPreference = 'Stop'
Get-Service -Name W32Time | Select-Object Name,Status,StartType | ConvertTo-Json -Compress
