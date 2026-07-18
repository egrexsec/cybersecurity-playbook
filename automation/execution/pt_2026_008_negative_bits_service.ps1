$ErrorActionPreference = 'Stop'
Get-Service BITS | Select-Object Name,Status,StartType | Format-List
