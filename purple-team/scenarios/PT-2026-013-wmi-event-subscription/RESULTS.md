# PT-2026-013 Results

## Validation run
- Validation ID: `VAL-2026-013`
- Technique: `T1546.003` WMI Event Subscription
- Exact Atomic test: `3c64f177-28e2-49eb-a799-d767b24dd1e0` (`T1546.003-1`)
- Status: **live validated** on 2026-08-03 UTC
- Target: approved Windows victim only
- Rollback snapshot: verified; exact identifier retained in private evidence

## Scope and safety
The scenario validated creation of a permanent WMI event filter, `CommandLineEventConsumer`, and filter-to-consumer binding. Boot-time evidence showed that the victim's uptime exceeded the upstream Atomic's 240–324 second trigger window, and a bounded Splunk search found zero `notepad.exe` Sysmon process-creation matches during the exact positive window. The modified variant used an intentionally unreachable uptime condition and an inert local command. No test-triggered payload execution was observed.

The ActiveScriptEventConsumer and MOFComp Atomic tests were excluded. No domain-controller execution, remote target, credential access, lateral movement, reboot, or network payload was permitted.

## Positive paths
1. The exact upstream Atomic UUID created the permanent filter, consumer, and binding.
   - A durable completion record verified all three objects.
   - The behavioral Splunk rule matched three Sysmon creation events at `2026-08-03T01:47:05Z`.
   - Observed event types included `WmiFilterEvent` and `WmiConsumerEvent`.
   - Detection latency was 4.486 seconds.
2. A modified local `CommandLineEventConsumer` variant used a deliberately non-triggering WQL condition.
   - A durable completion record verified all three objects.
   - The same rule matched Sysmon events 19, 20, and 21 at `2026-08-03T01:48:47Z`.
   - Detection latency was 0.994 seconds.

The detection is behavioral: it matches permanent WMI subscription creation fields, not scenario object names or Atomic-specific strings.

## Negative paths
The rule remained quiet for:
- read-only CIM operating-system inventory;
- read-only inventory of existing permanent WMI subscriptions;
- a transient in-process CIM indication subscription that did not write to `root/subscription`.

## Deviation and correction
The first validation harness compared CIM association references as ordinary strings. The Atomic created the subscription, but the harness could not reliably confirm or remove the binding, so no successful completion record was accepted. A later controlled attempt proved that a longer polling delay did not solve the representation problem.

Execution was stopped after each failed proof. Cleanup and verification were changed to the upstream-style WMI `REFERENCES OF` association query, regression assertions were added, and filter, consumer, binding, and completion-file counts were verified as zero before the successful replay. Only the final clean positive windows above are used as validation evidence.

## Cleanup and postflight
At `2026-08-03T01:52:21.487320Z`:
- no test filters, consumers, or bindings remained;
- no completion files remained;
- the victim domain secure channel passed;
- Sysmon, Splunk Forwarder, Velociraptor, Wazuh, and Defender were running;
- fresh victim telemetry remained searchable in Splunk;
- the domain controller remained healthy and `dcdiag /q` was quiet.

An idempotence recheck reran the corrected cleanup against the clean victim and again returned no remaining objects or completion files with `Clean=true`.
