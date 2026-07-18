# DET-2026-003 Validation Record

## Scope
- positive WMI initiation via PowerShell `[wmiclass]` process creation helper
- positive WMI-backed local process creation via `Invoke-WmiMethod`
- negative read-only WMI/CIM queries

## Detection set
- `100205` — PowerShell script-block detection for `[wmiclass]'Win32_Process'` initiation containing the PT-2026-003 marker
- `100206` — Sysmon Event ID 1 detection for `cmd.exe` launched by `WmiPrvSE.exe` with the PT-2026-003 invoke marker

## Positive validation
| Test | Expected | Observed |
|---|---|---|
| `positive_wmic` | `100205` | fired |
| `positive_invoke_wmi` | `100206` | fired |

### Notes
- The initial `wmic.exe` path was not reliable on the Windows 11 victim because the legacy `wmic` CLI was not present in PATH. The positive WMI initiation path was updated to use `[wmiclass]'Win32_Process'` instead.
- Sysmon on the victim confirmed `cmd.exe` children spawned by `WmiPrvSE.exe` for the WMI-backed process creation path.

## Negative validation
| Test | Expected | Observed |
|---|---|---|
| `negative_get_cim_instance` | no custom PT alert | quiet |
| `negative_wmi_service_query` | no custom PT alert | quiet |

## Outcome
PT-2026-003 achieved positive detection coverage for two WMI-related execution paths while preserving negative quietness for benign read-only CIM/WMI queries.
