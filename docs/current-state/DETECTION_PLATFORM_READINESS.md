# Detection Platform Readiness

## Summary
Critical telemetry prerequisites are currently sufficient to replay and validate the current eleven live-validated Windows scenarios represented on main.

## Proxmox and VM state
| Component | Status | Evidence | Notes |
|---|---|---|---|
| Proxmox host `mayuri` reachable | Ready | live SSH + `qm list` | host remains management-only; never target |
| victim VM 130 | Ready | `qm list`, live validation runs | domain joined and reachable |
| DC01 VM 120 | Ready | `qm list`, service checks | treat as critical / non-destructive only |
| SOC01 VM 140 | Ready | `qm list`, Splunk ports, sigma present | active SIEM node |
| DFIR01 VM 160 | Partially ready | running in `qm list` | not exercised in this validation cycle |
| KALI VM 150 | Partially ready | stopped in `qm list` | not required for current validation |
| Snapshot capability | Ready | victim and SOC snapshot chains present | latest branches end at `pre-splunk-*`; no new rollback taken in this cycle |
| Host disk capacity | Partially ready | `/` 80% used, ~19G free | enough for current work, not ideal for Elastic |
| Host memory headroom | Partially ready | 62Gi total / ~1Gi free / 24Gi cache available | Elastic on SOC would be risky |

## Windows target telemetry
| Capability | Status | Evidence | Notes |
|---|---|---|---|
| victim domain membership | Ready | `VICTIM-MAYURI`, `mayuri.lab`, `PartOfDomain=true` | direct guest query |
| Sysmon installed on victim | Ready | `Sysmon64` service status `4` | running |
| SplunkForwarder on victim | Ready | `SplunkForwarder` service status `4` | running |
| Velociraptor on victim | Ready | `Velociraptor` service status `4` | running |
| Sysmon installed on DC01 | Ready | `Sysmon64` service status `4` | running |
| SplunkForwarder on DC01 | Ready | `SplunkForwarder` service status `4` | running |
| PowerShell Operational log | Ready | present on victim; recent 4104 events in live validations | primary source for PT-001/PT-003 |
| Sysmon Operational log | Ready | present on victim; recent Event ID 1 and 11 events | primary source for PT-002 |
| Task Scheduler Operational log | Ready | present on victim (last seen event ID 332) | scenario not yet implemented |
| Defender Operational log | Ready | present on victim (last seen event ID 5007) | not yet integrated into current detections |
| Security log | Ready | present on victim | current Sigma live path does not yet normalize 4688 fields |
| Time alignment | Ready | fresh replays searchable in Splunk immediately after execution | manual latency still uncomputed |

## Splunk readiness
| Capability | Status | Evidence | Notes |
|---|---|---|---|
| Splunk installed on SOC01 | Ready | listeners on `8000`, `8089`, `9997` | live check |
| Splunk web/API/forwarding | Ready | ports listening | current primary SIEM |
| Victim telemetry ingestion | Ready | 24h counts for Application / PowerShell / Sysmon / Security / System | live query |
| DC01 telemetry ingestion | Ready | 24h counts for Application / PowerShell / Sysmon / Security / System | live query |
| Required sourcetypes | Ready | `XmlWinEventLog:*` sources visible | raw XML ingestion confirmed |
| Searchability during replay | Ready | `VAL-2026-001/002/003` | positive and negative windows validated |
| Field normalization | Partially ready | official Sigma conversion returns field-based SPL, but live environment lacks equivalent extracted fields | current Mayuri live pipeline uses raw XML `_raw` matching |
| Existing alerts/saved searches | Missing | no durable Splunk alert objects were verified in this cycle | validation currently query-driven |
| Retention sufficiency | Partially ready | at least 24h historical queries succeeded | formal retention policy not audited |

## Sigma tooling readiness
| Capability | Status | Evidence | Notes |
|---|---|---|---|
| SOC-local sigma binary | Partially ready | `sigma 3.1.0` exists on SOC01 | plugin list failed because SOC01 could not resolve `raw.githubusercontent.com` |
| Controller-side sigma venv | Ready | `/root/.venvs/sigma-platform` with working `sigma check/convert` | current authoritative build environment |
| Splunk backend conversion | Ready | generated official + Mayuri live SPL files | repository-local |
| Elastic conversion | Ready (conversion only) | generated EQL files | no live Elastic backend |
| Fixture harness | Ready | `automation/validators/sigma_ops.py test-fixtures` passing | 11 rules / 59 fixtures |

## Readiness decision
- Critical telemetry for PT-2026-001 through PT-2026-011: **Ready**
- Critical telemetry for the current Windows-safe execution/persistence set: **Ready with existing field-normalization caveats**
- Safe to replay the eleven verified scenarios now: **Yes**
- Safe to deploy Elastic now: **No**
