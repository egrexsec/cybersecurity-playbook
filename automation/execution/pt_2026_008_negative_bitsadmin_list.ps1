$ErrorActionPreference = 'Stop'
cmd.exe /c "bitsadmin.exe /list /allusers" | Out-Host
