# Investigation lifecycle

## Purpose

Use a repeatable, evidence-led process to move from an alert or question to a defensible conclusion. Detection content can initiate or improve an investigation, but a rule match is a lead rather than proof.

## Canonical 21-step lifecycle

1. **Define incident scenario** — record authorization, investigative question, target, controlled behavior, limits, cleanup, and completion criteria.
2. **Snapshot/prepare environment** — verify rollback state, time, identity, sensors, storage, collection paths, and safety gates.
3. **Generate controlled malicious behavior** — execute one bounded, approved behavior and stop on deviation.
4. **Produce an initial alert or investigative lead** — record how the activity surfaced and treat it as a lead rather than proof.
5. **Perform triage** — validate the lead, preserve short-retention evidence, and set initial severity and confidence.
6. **Establish incident scope** — identify affected identities, hosts, processes, resources, and time bounds.
7. **Acquire evidence** — collect proportionately using the [forensic acquisition workflow](forensic-acquisition.md), with integrity and handling metadata.
8. **Create timeline** — normalize and correlate relevant events using the [timeline workflow](timeline-analysis.md) while retaining source timestamps and provenance.
9. **Analyze endpoint evidence** — examine relevant processes, logs, files, registry, services, tasks, PowerShell, Defender, and execution artifacts.
10. **Analyze identity evidence** — examine authentication, accounts, groups, privileges, tickets, directory changes, and administrative activity.
11. **Analyze network evidence where relevant** — examine connections, DNS, flow, packet, firewall, or proxy evidence available to the case.
12. **Determine root cause** — state the best-supported initiating condition and causal chain, including confidence and alternatives.
13. **Determine persistence** — establish whether persistence was attempted or achieved and cite supporting or missing evidence.
14. **Determine lateral movement** — establish whether activity crossed systems or identities and reconstruct the path where supported.
15. **Determine data/resource access** — identify files, shares, directory objects, services, credentials, or cloud resources accessed or targeted.
16. **Develop containment recommendations** — propose proportionate actions that preserve evidence and account for operational impact.
17. **Develop remediation recommendations** — address root cause, affected state, credential exposure, persistence, and recovery validation.
18. **Identify telemetry gaps** — record missing, delayed, inaccessible, malformed, or insufficient evidence.
19. **Identify detection opportunities** — derive candidate searches, alerts, data improvements, and negative tests without claiming validation prematurely.
20. **Produce sanitized investigation report** — publish only reviewable findings, methods, limitations, and non-sensitive provenance.
21. **Restore/clean environment** — remove simulation artifacts and temporary access, restore the approved baseline, verify health, and close the case.

## Minimum completion record

- investigation identifier and maturity status
- authorization and scope
- evidence ledger with hashes or stable source references
- acquisition notes and tool versions
- timestamp-normalized timeline
- hypotheses and pivot log
- findings with citations to evidence identifiers
- alternative explanations and limitations
- containment or escalation decisions
- detection opportunities, if any
- sanitization review for public artifacts

Use [the investigation template](../../templates/investigation-template.md) for case documentation.
