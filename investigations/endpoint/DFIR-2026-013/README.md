# DFIR-2026-013 — Permanent WMI event subscription investigation

## Question
Was a permanent WMI event filter, consumer, or filter-to-consumer binding created, and was the behavior approved administration or unauthorized event-triggered persistence?

## Evidence sequence
1. Review Sysmon events 19, 20, and 21 for `WmiFilterEvent`, `WmiConsumerEvent`, and `WmiBindingEvent` creation.
2. Correlate the filter namespace and WQL query with the consumer class and destination command.
3. Confirm the binding relationship; a filter or consumer alone may be incomplete or orphaned rather than functional persistence.
4. Pivot to adjacent PowerShell and WMI Activity telemetry to identify the creating account, process, and execution window.
5. Inventory `root/subscription` directly and compare object names and consumers with approved endpoint-management and monitoring baselines.
6. Remove the binding before its consumer and filter, then verify all three object classes are clean.

## Validated observations
- Both controlled positives created a filter, `CommandLineEventConsumer`, and binding and fired in Splunk.
- The modified positive produced Sysmon events 19, 20, and 21.
- Read-only inventory and transient in-process subscription controls remained quiet.
- Final cleanup found no test objects or completion artifacts.

## Disposition
Expected lab activity for validation `VAL-2026-013`. Outside an approved exercise or software deployment, permanent WMI subscription creation warrants escalation because it can provide stealthy event-triggered persistence. Validate legitimate management tooling before containment, but preserve the filter, consumer, and binding relationship as evidence.
