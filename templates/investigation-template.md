# Investigation Report: [Case ID] — [Title]

## Case metadata

| Field | Value |
|---|---|
| Case ID | `MAY-IR-###` |
| Status | Planned / Installed / Verified / Live validated |
| Lead analyst | [Name or role] |
| Opened / closed | [ISO 8601 timestamps with timezone] |
| Investigation domain | Endpoint / Identity / Network / Cloud |
| Authorization | [Private approval reference] |
| Public handling | Sanitized derivative; raw evidence remains private |

> Capability maturity statuses in this report do not replace Sigma-native rule lifecycle values.

## Executive summary

State the investigative question, material findings, affected scope, confidence, and outcome. Separate confirmed facts from assessment.

## Scope and constraints

- Systems, identities, services, and time range in scope
- Explicit exclusions
- Collection or business-impact constraints
- Stop conditions and escalation path
- Known telemetry, retention, clock, or access limitations

## Initial alert or question

Document what initiated the investigation, who supplied it, when it was received, and what was known before analysis. A detection match is a lead, not proof.

## Hypotheses

| ID | Hypothesis | Evidence that would support it | Evidence that would refute it | State |
|---|---|---|---|---|
| H1 | [Primary explanation] | [Expected observations] | [Contradictory observations] | Open |
| H2 | [Benign or alternate explanation] | [Expected observations] | [Contradictory observations] | Open |

## Evidence ledger

Raw evidence, credentials, full acquisitions, and sensitive infrastructure data remain in approved private storage.

| Evidence ID | Description | Source | Acquisition time and timezone | Method / tool / version | Integrity reference | Public derivative |
|---|---|---|---|---|---|---|
| EV-001 | [Artifact or export] | [System or sensor] | [Timestamp] | [Method] | [Hash or private ledger reference] | [Sanitized file or none] |

## Acquisition record

- Collector and authorization reference
- Commands, filters, collection windows, and tool versions
- Source system time, timezone, and known drift
- Original and working-copy custody locations
- Hash verification after collection and transfer
- Failures, partial results, and artifacts not collected

## Triage and pivot log

| Time | Analyst action or query | Reason | Result | Evidence / next pivot |
|---|---|---|---|---|
| [Timestamp] | [Action] | [Hypothesis tested] | [Neutral result] | [Evidence IDs] |

## Timeline

Retain original timestamps and add normalized UTC values. Label inference and uncertainty.

| Normalized time | Original time / timezone | Evidence ID | Host / identity | Observed activity | Interpretation | Confidence |
|---|---|---|---|---|---|---|
| [UTC] | [Source value] | EV-001 | [Entity] | [Observation] | [Assessment] | High / Medium / Low |

## Analysis by domain

### Endpoint

Document process, persistence, file, registry, event-log, and execution-artifact analysis.

### Identity

Document authentication, account, group, role, session, and privilege analysis.

### Network

Document DNS, connection, flow, protocol, and cross-host correlation.

### Cloud

Document principal, role, policy, control-plane, data-plane, and service-log analysis. Omit when not applicable; no AWS provisioning is implied.

## Findings

For each finding, include:

1. a concise statement
2. supporting evidence IDs
3. analysis method or query
4. confidence and rationale
5. relevant contradictory or missing evidence

## Root cause and attack path

State the best-supported sequence and enabling conditions. If root cause cannot be established, say so and identify the evidence required to resolve it.

## MITRE ATT&CK mapping

| Technique | Observed behavior | Evidence IDs | Mapping confidence |
|---|---|---|---|
| [Tactic / technique] | [What was observed] | [EV-###] | [Rationale] |

ATT&CK mapping describes observed behavior; it does not prove actor identity or intent.

## Containment, eradication, and recovery

- Actions taken, owner, and timestamp
- Evidence preserved before action
- Verification that the action had the intended effect
- Residual risk and monitoring requirements

## Detection and telemetry opportunities

- Existing analytics that helped
- Blind spots, missing fields, and retention gaps
- Proposed Sigma or platform analytics
- Positive, variant, and negative validation requirements
- Ownership and priority

Detection work is a supporting output of the investigation, not a substitute for evidence.

## AI assistance disclosure

| Tool / model | Sanitized task | Output used | Independent validation |
|---|---|---|---|
| [If applicable] | [Prompt purpose, not sensitive input] | [Query idea, summary, none] | [How source evidence or deterministic tooling verified it] |

AI output is not evidence. Do not cite it as the basis for findings, timeline events, indicators, attribution, or response decisions.

## Conclusions

Answer the original question, state confidence, identify affected scope, and distinguish confirmed findings from unresolved assessment.

## Limitations and unresolved questions

- Missing or unavailable evidence
- Clock, retention, collection, or parsing limitations
- Competing explanations not fully resolved
- Follow-up owners and acceptance criteria

## Lessons learned

Record improvements to acquisition, evidence handling, analysis, detection, lab design, and documentation.

## Public sanitization review

- [ ] Raw evidence and full acquisitions are not committed
- [ ] Credentials, tokens, personal data, and sensitive infrastructure details are removed
- [ ] Public derivatives preserve the meaning of cited observations
- [ ] Links resolve and evidence identifiers are consistent
- [ ] AI-generated statements are independently validated or excluded
- [ ] Status is supported by completed acceptance criteria
