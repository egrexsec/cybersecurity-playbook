$ErrorActionPreference = 'Stop'
@(Get-CimInstance -Namespace root/subscription -ClassName __EventFilter | Select-Object -ExpandProperty Name) | ConvertTo-Json -Compress
