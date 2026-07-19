$ErrorActionPreference = 'Stop'
$job = 'PT-2026-008-Original'
$src = '\\127.0.0.1\C$\Windows\win.ini'
$dst = "$env:TEMP\pt-2026-008-original.txt"
Remove-Item $dst -ErrorAction SilentlyContinue -Force
cmd.exe /c "bitsadmin.exe /reset /allusers"
cmd.exe /c "bitsadmin.exe /transfer $job /download /priority foreground $src $dst" | Out-Host
$exists = Test-Path $dst
[pscustomobject]@{ JobName=$job; DstExists=$exists } | ConvertTo-Json -Compress | Out-Host
