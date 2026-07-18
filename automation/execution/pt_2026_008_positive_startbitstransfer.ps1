$ErrorActionPreference = 'Stop'
$src = '\\127.0.0.1\C$\Windows\win.ini'
$dst = "$env:TEMP\pt-2026-008-variant.txt"
Remove-Item $dst -ErrorAction SilentlyContinue -Force
try { Start-BitsTransfer -Priority foreground -Source $src -Destination $dst -ErrorAction Stop } catch { Write-Output $_.Exception.Message }
$exists = Test-Path $dst
[pscustomobject]@{ DstExists=$exists } | ConvertTo-Json -Compress | Out-Host
