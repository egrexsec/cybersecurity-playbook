$ErrorActionPreference = 'Stop'
Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,LastBootUpTime | ConvertTo-Json -Compress
