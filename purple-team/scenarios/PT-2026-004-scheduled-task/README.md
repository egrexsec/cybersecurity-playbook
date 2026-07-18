# PT-2026-004 — Scheduled Task Creation

Validates suspicious scheduled task creation on the approved Windows victim using:
- `schtasks.exe /Create`
- PowerShell `Register-ScheduledTask`

The scenario is intentionally low-risk:
- tasks run once under `SYSTEM`
- only marker files under `C:\Windows\Temp` are created
- cleanup removes tasks and markers immediately after validation
