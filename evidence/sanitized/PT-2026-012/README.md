# PT-2026-012 sanitized evidence

## Summary
On 2026-07-29 UTC, the approved Windows victim executed Atomic Red Team `T1569.002-1` using exact test UUID `2382dee2-a75f-49aa-9378-f52df6ed3fb1`.

## Correlated telemetry
| Path | UTC event | Sysmon lineage | SCM evidence | Detection |
|---|---|---|---|---|
| Original | 16:55:23 | `services.exe -> cmd.exe -> powershell.exe` | 7045, 7009, 7000 | Fired |
| Variant | 16:58:32 | `services.exe -> cmd.exe` | 7045, 7009, 7000 | Fired |
| Query control | 16:59:27-16:59:38 | No service-launched shell | None required | Quiet |
| PowerShell query control | 16:59:38-16:59:49 | No service-launched shell | None required | Quiet |
| Create-without-start control | 16:59:49 | No service-launched shell | 7045 | Quiet |

The create-without-start control is significant: service installation telemetry existed, but the process-lineage rule correctly remained quiet.

## Cleanup
Final validation found zero remaining test services and zero remaining marker/completion artifacts. Endpoint sensors, the domain secure channel, Splunk ingestion, and domain-controller health remained operational.

Raw credentials, addresses, management commands, process identifiers, and private infrastructure details are intentionally omitted.
