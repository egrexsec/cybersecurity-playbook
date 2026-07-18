# DFIR-2026-001 — Endpoint Investigation Summary

## Scope
Investigate the first approved PowerShell-execution scenario on the Windows victim and document the minimum viable forensic workflow for a public-safe repository.

## Investigated scenario
- Scenario: `PT-2026-001`
- Technique: `T1059.001` PowerShell
- Endpoint role: approved Windows victim
- Execution path: local QEMU guest exec into the isolated lab endpoint

## What was validated
1. The approved Atomic registry-backed execution completed and created the expected marker file.
2. The modified variant completed and created its expected marker file.
3. PowerShell script-block telemetry existed and was sufficiently rich to support live detection logic.
4. Wazuh built-ins and custom test-scope rules both observed relevant behavior.
5. Benign negative tests did not trigger the custom PT-specific rules.

## Evidence sources used
- Windows PowerShell Operational events (`4104` observed live)
- Sysmon process creation events (`1` observed live)
- Wazuh alert stream on SOC
- Sanitized execution records committed under `evidence/sanitized/PT-2026-001/`

## High-value artifacts observed
- Registry-backed base64 value under `HKCU\Software\Classes\AtomicRedTeam`
- Marker file `C:\Windows\Temp\art-marker.txt`
- Marker file `C:\Windows\Temp\variant-marker.txt`
- Script block showing `FromBase64String` + `Invoke-Expression`

## Forensic reconstruction notes
- The most reliable platform signal for the modified variant was **PowerShell script-block logging**, not the encoded PowerShell process command line.
- The original Atomic test was best confirmed via a **registry + base64** signal on the `reg.exe` step and the expected cleanup-capable marker-file outcome.
- The guest-exec transport means some PowerShell process command lines are heavily base64 wrapped, so raw process-creation-only analytics can miss decoded execution intent unless paired with script-block logging.

## Gaps and constraints
- The lightweight collector used during this run produced sparse time-window exports because log ingestion timing was tighter than the collection windows.
- Velociraptor remained available in the lab, but this milestone relied primarily on Windows event and Wazuh evidence to keep the first scenario small and public-safe.
- PowerShell transcription is still not enabled, which limits full content reconstruction beyond script-block logs.

## Recommended next DFIR increment
- Add a dedicated sanitized event-excerpt exporter.
- Add a small Velociraptor collection profile for recent PowerShell script blocks or process inventory.
- Extend the investigation template with timeline and pivot sections for parent/child process analysis.
