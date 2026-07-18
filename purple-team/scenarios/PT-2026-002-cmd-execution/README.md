# PT-2026-002 — Windows Command Shell Execution

This is the second planned Mayuri scenario and extends the public-safe workflow
from PowerShell into `cmd.exe` / Windows Command Shell behavior.

## Planned focus
- low-risk command-shell execution on the approved Windows victim
- process creation telemetry validation
- file-write side effects from batch or echo-based execution
- hunt development for suspicious `cmd.exe` invocation patterns
- portable detection design plus Wazuh test-scope translation

## Public-safe constraints
- no destructive commands
- no persistence changes required for the first pass
- no internet callbacks
- no raw evidence dumps committed
