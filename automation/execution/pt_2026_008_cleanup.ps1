$ErrorActionPreference = 'Stop'
Get-BitsTransfer -AllUsers -ErrorAction SilentlyContinue | Remove-BitsTransfer -Confirm:$false -ErrorAction SilentlyContinue
cmd.exe /c "bitsadmin.exe /reset /allusers"
Remove-Item "$env:TEMP\pt-2026-008-original.txt","$env:TEMP\pt-2026-008-variant.txt" -Force -ErrorAction SilentlyContinue
'cleanup complete'
