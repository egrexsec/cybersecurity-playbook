# PT-2026-013 sanitized evidence

## Summary
On 2026-08-03 UTC, the approved Windows victim executed Atomic Red Team `T1546.003-1` using exact test UUID `3c64f177-28e2-49eb-a799-d767b24dd1e0`. A modified local, non-triggering permanent subscription provided a second positive path.

## Correlated telemetry
| Path | UTC event/window | Sysmon evidence | Detection |
|---|---|---|---|
| Exact Atomic | 01:47:05 | Three creation events; event types included WMI filter and consumer | Fired; 4.486 s |
| Modified variant | 01:48:47 | Events 19, 20, and 21; filter, consumer, and binding creation | Fired; 0.994 s |
| CIM inventory control | 01:49:52-01:49:55 | No permanent-subscription creation | Quiet |
| Subscription inventory control | 01:50:34-01:50:37 | No permanent-subscription creation | Quiet |
| Transient subscription control | 01:51:16-01:51:22 | No permanent `root/subscription` objects | Quiet |

Boot-time evidence placed the exact Atomic run outside its 240–324 second trigger interval. A bounded Splunk search returned zero `notepad.exe` Sysmon process-creation matches during the exact positive window.

## Cleanup
Final validation found zero remaining test filters, consumers, bindings, and completion files. A later idempotence recheck again returned empty residue sets and `Clean=true`. Endpoint sensors, the domain secure channel, Splunk ingestion, and domain-controller health remained operational.

Raw event XML, credentials, private addresses, management commands, process identifiers, and private infrastructure details are intentionally omitted.
