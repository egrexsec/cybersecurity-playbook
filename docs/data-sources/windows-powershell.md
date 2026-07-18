# Windows PowerShell Data Sources

## Scope
This page documents the PowerShell telemetry used for the first Mayuri purple-team milestone.

## Confirmed Sources

| Source | System | Collection Method | Destination | Parsing Status |
|---|---|---|---|---|
| Microsoft-Windows-PowerShell/Operational | Windows victim | Windows event log | Wazuh agent / local collection | Confirmed live |
| PowerShell Script Block Logging (4104) | Windows victim | Policy-enabled PowerShell logging | Windows event log / Wazuh path | Confirmed enabled |
| PowerShell Module Logging (4103) | Windows victim | Policy-enabled PowerShell logging | Windows event log / Wazuh path | Confirmed enabled |

## Relevant Event IDs
- `4103` Module logging
- `4104` Script block logging
- `400` / `403` engine lifecycle where relevant

## Collection Notes
- Script Block Logging is enabled.
- Module Logging is enabled with wildcard module coverage.
- PowerShell transcription is not currently enabled and is a known gap.

## ATT&CK Mapping
- `T1059.001` PowerShell
- `T1027` Obfuscated / encoded execution when decode patterns are present
- `T1105` may appear as adjacent behavior when download cradles are involved

## Known Gaps
- No transcription artifacts yet
- No repo-managed parser normalization yet
- No long-term retention policy documented in this repo yet

## Example Hunt Questions
- Which PowerShell blocks used `FromBase64String`?
- Which parent process launched PowerShell?
- Which script blocks also correlate with process creation and file writes?
