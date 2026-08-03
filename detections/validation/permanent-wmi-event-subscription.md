# Permanent WMI Event Subscription Detection Validation

- Scenario: `PT-2026-013`
- Validation: `VAL-2026-013`
- Technique: `T1546.003`
- Atomic UUID: `3c64f177-28e2-49eb-a799-d767b24dd1e0`
- Result: **passed live validation**

## Assertions
- Exact Atomic `CommandLineEventConsumer` subscription: detected.
- Modified non-triggering permanent subscription: detected.
- Read-only CIM operating-system inventory: not detected.
- Read-only permanent-subscription inventory: not detected.
- Transient in-process indication subscription: not detected.
- Explicit association cleanup and postflight health: passed.

The live Mayuri query uses raw Sysmon XML because equivalent normalized WMI fields are not yet verified in Splunk. The canonical Sigma rule remains field-based and backend-neutral.

See the [live JSON record](live/VAL-2026-013-PT-2026-013.json), [scenario results](../../purple-team/scenarios/PT-2026-013-wmi-event-subscription/RESULTS.md), and [sanitized evidence](../../evidence/sanitized/PT-2026-013/README.md).
