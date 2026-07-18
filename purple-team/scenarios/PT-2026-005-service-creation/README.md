# PT-2026-005 — Windows Service Creation

Validates suspicious Windows service creation on the approved victim using:
- `sc.exe create`
- PowerShell `New-Service`

The scenario is intentionally low-risk:
- services are temporary and deleted during cleanup
- marker files are limited to `C:\Windows\Temp`
- no external payload download is used
