# Previous Atomic Scenarios

## Determination
The three previously implemented scenarios were **not** Scheduled Task / Service Creation scenarios. Repository history, historical validation artifacts, and fresh live replay show the implemented set was:
1. PT-2026-001 — PowerShell execution (`T1059.001`)
2. PT-2026-002 — Windows command shell execution (`T1059.003`)
3. PT-2026-003 — WMI execution (`T1047`)

## PT-2026-001
- Scenario ID: PT-2026-001
- ATT&CK technique: T1059.001
- Atomic test number: historical files indicate Atomic Red Team-driven PowerShell execution path; exact upstream Atomic test UUID was not preserved in live telemetry, but scenario YAML and execution script match the registry-backed encoded PowerShell pattern used in lab
- Target host: victim / `VICTIM-MAYURI`
- Execution command: registry-backed PowerShell decode + `Invoke-Expression` writing `art-marker.txt`
- Historical execution timestamp: evidence files around `2026-07-18T01:44Z` and fresh replay at `2026-07-18T13:19:28Z`
- Exit status: success in fresh replay
- Cleanup command: remove marker files and `HKCU:\Software\Classes\AtomicRedTeam`
- Cleanup status: verified in `VAL-2026-001-PT-2026-001.json`
- Required telemetry: PowerShell Operational 4104/4103, optionally Sysmon process creation
- Telemetry found: yes
- Threat hunt performed: hypothesis file exists; historical hunt was present but not yet reworked into a broader behavioral query set
- Forensic collection performed: historical DFIR README exists; fresh replay focused on telemetry validation rather than a new full forensic case pack
- Detection created: yes
- Detection platform: historical Wazuh + current Sigma/Splunk
- Validation evidence: `detections/validation/live/VAL-2026-001-PT-2026-001.json`
- Current confidence: High
- Outstanding gaps: exact upstream Atomic UUID not preserved in current live record; detection latency not yet numerically computed

## PT-2026-002
- Scenario ID: PT-2026-002
- ATT&CK technique: T1059.003
- Atomic test number: historical scenario is tied to the lab-authored batch/obfuscated variant workflow rather than a preserved upstream Atomic UUID in current evidence
- Target host: victim / `VICTIM-MAYURI`
- Execution command: temporary `.cmd` launch and obfuscated `%LOCALAPPDATA:~-3,1%md /c` variant
- Historical execution timestamp: historical repository validation on 2026-07-18; fresh replay at `2026-07-18T13:20:27Z` and `2026-07-18T13:20:41Z`
- Exit status: success in fresh replay
- Cleanup command: remove temp batch, positive marker, variant marker, negative test outputs
- Cleanup status: verified in `VAL-2026-002-PT-2026-002.json`
- Required telemetry: Sysmon Event ID 1 and file creation support
- Telemetry found: yes
- Threat hunt performed: hypothesis file exists; current broad hunt coverage still needs refinement
- Forensic collection performed: historical README exists; fresh replay confirmed Sysmon artifacts and Splunk capture
- Detection created: yes
- Detection platform: historical Wazuh + current Sigma/Splunk
- Validation evidence: `detections/validation/live/VAL-2026-002-PT-2026-002.json`
- Current confidence: High
- Outstanding gaps: historical Wazuh rules were atomic-specific; current Splunk live query uses raw XML matching due missing field normalization

## PT-2026-003
- Scenario ID: PT-2026-003
- ATT&CK technique: T1047
- Atomic test number: repository history shows WMI execution scenario validated through safe PowerShell WMI creation methods; exact upstream Atomic UUID is not preserved in the refreshed live validation record
- Target host: victim / `VICTIM-MAYURI`
- Execution command: `[wmiclass]"Win32_Process".Create(...)` and `Invoke-WmiMethod -Path Win32_Process -Name Create ...`
- Historical execution timestamp: historical repository validation on 2026-07-18; fresh replay at `2026-07-18T13:21:25Z` and `2026-07-18T13:21:45Z`
- Exit status: success in fresh replay
- Cleanup command: remove WMI marker files
- Cleanup status: verified in `VAL-2026-003-PT-2026-003.json`
- Required telemetry: PowerShell Operational 4104/4103; optional Sysmon process creation from WmiPrvSE lineage
- Telemetry found: yes
- Threat hunt performed: hypothesis file exists but remains narrower than desired for long-term behavioral hunting
- Forensic collection performed: historical README exists; fresh replay focused on telemetry confirmation
- Detection created: yes
- Detection platform: historical Wazuh + current Sigma/Splunk
- Validation evidence: `detections/validation/live/VAL-2026-003-PT-2026-003.json`
- Current confidence: High
- Outstanding gaps: historical Wazuh detection used marker filenames; live Splunk latency not yet numerically measured

## Missing / unverified expected scenarios
- T1053.005 Scheduled Task/Job: **unconfirmed / not implemented in current repository evidence**
- T1543.003 Windows Service Creation: **unconfirmed / not implemented in current repository evidence**
