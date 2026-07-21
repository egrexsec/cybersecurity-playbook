# Previous Atomic scenarios

## Historical scope

This document summarizes the original three Windows execution scenarios before the repository expanded to 11 scenarios. It is a dated historical record, not current lab-health evidence. Raw commands, host identities, users, addresses, event payloads, and infrastructure identifiers are intentionally omitted.

## Original set

| Scenario | ATT&CK | Behavior | Historical evidence date | Current repository posture |
|---|---|---|---|---|
| PT-2026-001 | T1059.001 | PowerShell decode-and-execute | 2026-07-18 | fixture tested; sanitized historical summary retained |
| PT-2026-002 | T1059.003 | Windows command-shell execution | 2026-07-18 | fixture tested; sanitized historical summary retained |
| PT-2026-003 | T1047 | WMI-backed process execution | 2026-07-18 | fixture tested; sanitized historical summary retained |

## What the historical summaries establish

For each scenario, the sanitized record reports:

- an authorized positive execution previously produced expected telemetry;
- a behavioral variant previously matched;
- negative tests did not match;
- cleanup was reported as confirmed;
- the source record was hashed before sanitization.

## What they do not establish

The summaries do not prove current:

- endpoint, identity, DNS, time, or snapshot health;
- log forwarding or SIEM ingestion;
- deployed saved searches or alert objects;
- Wazuh, Splunk, CTI, or DFIR service availability;
- field normalization or detection latency;
- portability to another environment.

## Later expansion

PT-2026-004 through PT-2026-011 subsequently added scheduled-task, service, registry, logon-script, BITS, PowerShell-profile, Rundll32, and Regsvr32 behaviors. Their present public posture is also **fixture tested with dated historical summaries**, not freshly live-verified state.

Any replay requires the private preflight, approval token, rollback confirmation, and external live adapter described in `automation/validators/LIVE_ADAPTER.md`.
