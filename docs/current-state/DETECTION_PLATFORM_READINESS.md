# Detection Platform Readiness

## Summary
Critical telemetry prerequisites are currently sufficient to replay and validate the current fifteen Windows scenarios represented in the repository.

## Proxmox and VM state
| Component | Status | Evidence | Notes |
|---|---|---|---|
| Virtualization host reachable | Ready | private management-plane inventory | management-only; never target |
| Approved Windows victim | Ready | private management-plane inventory and live validation | domain joined and reachable |
| Directory-services role | Ready | private inventory and service checks | critical / non-destructive only |
| SIEM role | Ready | private inventory, service ports, Sigma tooling | active monitoring node |
| DFIR role | Partially ready | private management-plane inventory | not exercised in this validation cycle |
| Attack-simulation role | Partially ready | private management-plane inventory | not required for current validation |
| Snapshot capability | Ready | victim rollback snapshot verified; identifier retained privately | snapshots supplement but do not replace cleanup |
| Host disk capacity | Partially ready | local storage 77% used; local LVM thin pool 72% used | enough for current work, not ideal for Elastic |
| Host memory headroom | Partially ready | 62Gi total / ~1Gi free / 24Gi cache available | Elastic on SOC would be risky |

## Windows target telemetry
| Capability | Status | Evidence | Notes |
|---|---|---|---|
| Approved endpoint domain membership | Ready | private endpoint and directory-domain identifiers; `PartOfDomain=true` | direct guest query |
| Sysmon on approved endpoint | Ready | `Sysmon64` service status `4` | running |
| SplunkForwarder on approved endpoint | Ready | `SplunkForwarder` service status `4` | running |
| Velociraptor on approved endpoint | Ready | `Velociraptor` service status `4` | running |
| Sysmon on directory-services role | Ready | `Sysmon64` service status `4` | running |
| SplunkForwarder on directory-services role | Ready | `SplunkForwarder` service status `4` | running |
| PowerShell Operational log | Ready | present on victim; recent 4104 events in live validations | primary source for PT-001/PT-003 |
| Sysmon Operational log | Ready | present on victim; recent Event ID 1 and 11 events | primary source for PT-002 |
| Task Scheduler Operational log | Ready | present on victim (last seen event ID 332) | scenario not yet implemented |
| Defender Operational log | Ready | exact mshta prevention recorded with detection/action events during PT-2026-015 | prevention telemetry is evidence, not yet a canonical Sigma rule |
| Security log | Ready | present on victim | current Sigma live path does not yet normalize 4688 fields |
| Sysmon WMI subscription events | Ready | live events 19, 20, and 21 validated during PT-2026-013 | primary source for permanent WMI subscription detection |
| Time alignment | Ready | fresh replays searchable in Splunk immediately after execution | numeric latency recorded for PT-2026-013; older records remain inconsistent |

## Splunk readiness
| Capability | Status | Evidence | Notes |
|---|---|---|---|
| Splunk installed on SIEM role | Ready | expected service listeners present | live check |
| Splunk web/API/forwarding | Ready | ports listening | current primary SIEM |
| Victim telemetry ingestion | Ready | 24h counts for Application / PowerShell / Sysmon / Security / System | live query |
| Directory-services telemetry ingestion | Ready | 24h counts for Application / PowerShell / Sysmon / Security / System | live query |
| Required sources | Ready | `WinEventLog:*` sources visible | raw XML ingestion confirmed |
| Searchability during replay | Ready | `VAL-2026-001..015` | positive and negative windows validated |
| Field normalization | Partially ready | official Sigma conversion returns field-based SPL, but live environment lacks equivalent extracted fields | current lab-live pipeline uses raw XML `_raw` matching |
| Existing alerts/saved searches | Missing | no durable Splunk alert objects were verified in this cycle | validation currently query-driven |
| Retention sufficiency | Partially ready | at least 24h historical queries succeeded | formal retention policy not audited |

## Sigma tooling readiness
| Capability | Status | Evidence | Notes |
|---|---|---|---|
| SIEM-local Sigma binary | Partially ready | `sigma 3.1.0` exists on the SIEM role | plugin list failed because the SIEM role could not resolve the upstream source |
| Controller-side Sigma environment | Ready | private controller environment with working `sigma check/convert` | current authoritative build environment |
| Splunk backend conversion | Ready | generated official and lab-live SPL files | repository-local |
| Elastic conversion | Ready (conversion only) | generated EQL files | no live Elastic backend |
| Fixture harness | Ready | `automation/validators/sigma_ops.py test-fixtures` passing | 15 rules / 79 fixtures |

## Readiness decision
- Critical telemetry for PT-2026-001 through PT-2026-015: **Ready**
- Critical telemetry for the current Windows-safe execution/persistence set: **Ready with existing field-normalization caveats**
- Safe to replay the fifteen documented scenarios after fresh preflight and scenario-specific safety review: **Yes**
- Safe to deploy Elastic now: **No**
