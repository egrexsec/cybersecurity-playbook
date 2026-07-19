# IR Data Source Matrix

| Source | Purpose | Confirmed status | Notes |
|---|---|---|---|
| Splunk `XmlWinEventLog:Microsoft-Windows-PowerShell/Operational` | PowerShell execution, script block review | Ready | strong source for PT-2026-001 |
| Splunk `XmlWinEventLog:Microsoft-Windows-Sysmon/Operational` | process creation, file, network telemetry | Ready | existing validations rely on it |
| Splunk Security log | auth/process context | Partially ready | present, field normalization incomplete |
| Velociraptor client data | targeted triage, collection | Partially ready | server reachable; API not yet wired |
| Wazuh alerts | supplemental alerting and hunts | Partially ready | not primary in this first workflow |
| OPNsense logs | containment + network pivots | Blocked | firewall VM stopped |
| Hayabusa EVTX output | offline timeline enrichment | Blocked | tool missing |
| Chainsaw output | offline Sigma matching | Blocked | tool unconfirmed |
| Local AI analysis | structured narrative assistance | Unconfirmed | endpoint not validated |
