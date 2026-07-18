# DFIR-2026-002 — Endpoint Investigation Summary

## Scope
Investigate a low-risk Windows Command Shell execution scenario on the approved Windows victim and document a public-safe forensic workflow.

## Investigated scenario
- Scenario: `PT-2026-002`
- Technique: `T1059.003` Windows Command Shell
- Endpoint role: approved Windows victim

## What was validated
1. A batch-script execution path completed and created the expected marker file.
2. A suspicious environment-variable-based `cmd.exe` invocation completed and created the expected marker file.
3. Sysmon process creation telemetry was sufficient to support precise scenario-scoped detection.
4. Benign `cmd.exe` negative tests did not trigger the custom PT-specific rules.

## Evidence sources used
- Sysmon process creation telemetry forwarded into Wazuh
- Wazuh alert stream on SOC
- Sanitized validation records committed under `evidence/sanitized/PT-2026-002/`

## High-value artifacts observed
- `C:\Windows\Temp\pt-2026-002-positive.txt`
- `C:\Windows\Temp\pt-2026-002-variant.txt`
- `C:\Windows\Temp\pt-2026-002-negative-dir.txt`
- `C:\Windows\Temp\pt-2026-002-negative-echo.txt`
- `cmd.exe` command lines referencing `pt-2026-002-positive.cmd`
- `cmd.exe` command line containing `LOCALAPPDATA:~-3,1` indirection

## Forensic reconstruction notes
- The validated suspicious variant is a good example of cmd-based obfuscation/indirection that remains visible in process creation telemetry.
- This scenario did not require raw event export to demonstrate the engineering workflow in a public repo.
- A temporary malformed local rules update interrupted Wazuh manager startup during rule tuning, but the service was restored and the final rule set validated before completion.
