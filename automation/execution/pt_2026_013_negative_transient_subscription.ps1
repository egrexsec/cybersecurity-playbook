$ErrorActionPreference = 'Stop'
$id = 'PT-2026-013-Transient'
Register-CimIndicationEvent -Query "SELECT * FROM Win32_ProcessStartTrace WHERE ProcessName='definitely-not-created-pt-2026-013.exe'" -SourceIdentifier $id | Out-Null
Start-Sleep -Seconds 1
Unregister-Event -SourceIdentifier $id
Get-Job -Name $id -ErrorAction SilentlyContinue | Remove-Job -Force
[pscustomobject]@{ SourceIdentifier=$id; Permanent=$false } | ConvertTo-Json -Compress
