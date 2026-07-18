$ErrorActionPreference = 'Stop'
Get-BitsTransfer -AllUsers | Select-Object -First 5 DisplayName,JobState | Format-List
