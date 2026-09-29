# Roadmap

## Direction

Evolve the repository into an investigation-led technical portfolio. Detection engineering, purple-team validation, threat hunting, and automation remain intact as supporting capabilities that produce leads, test hypotheses, and improve coverage after evidence-led analysis.

## Status model

Investigation and DFIR capability maturity uses only:

- **Planned** — scope and acceptance criteria exist; implementation is not evidence-backed.
- **Installed** — required tooling or collection capability is available but not verified end to end.
- **Verified** — the workflow has been exercised successfully with reviewable evidence.
- **Live validated** — the workflow has been exercised against approved live lab activity with sanitized, traceable results.

This model does not change Sigma-native lifecycle values or existing detection validation statuses.

## Current evidence-backed foundation

- twelve existing Windows purple-team scenarios have published live-validation status
- endpoint investigation notes exist for PT-2026-001 through PT-2026-012
- Sigma linting, conversion, fixture testing, and Splunk live-validation workflows remain operational
- public-safe validation records and case-study material demonstrate evidence traceability
- raw evidence remains private; the repository stores sanitized derivatives and documentation

## Investigation case roadmap

Every case below remains **Planned** until its stated acceptance criteria are complete and backed by traceable evidence. A scenario, installed tool, draft narrative, or AI-generated analysis does not advance the status by itself.

### MAY-IR-001 PowerShell

**Status: Planned**

Acceptance criteria:
- define a scoped investigative question and competing hypotheses
- create an evidence ledger referencing approved private sources
- correlate PowerShell, process, persistence, and SIEM evidence
- publish a timestamp-normalized sanitized timeline
- distinguish observed facts, interpretation, and limitations
- document response and detection-improvement opportunities

Existing PT-2026-001 and DFIR-2026-001 material may support this case, but the MAY-IR case is not complete until the investigation-led record meets these criteria.

### MAY-IR-002 Scheduled Task

**Status: Planned**

Acceptance criteria:
- reconstruct Scheduled Task creation, execution, modification, and cleanup where evidenced
- correlate task metadata with process and event-log records
- test malicious and benign administrative explanations
- publish sanitized findings and a source-cited timeline
- derive and validate detection opportunities without treating a rule match as proof

### MAY-IR-003 credential abuse/lateral movement

**Status: Planned**

Acceptance criteria:
- use bounded, approved lab activity without real credentials or secret exposure
- correlate authentication, endpoint, identity, and available network evidence
- distinguish credential use, account compromise, and administrator activity
- document affected scope, containment logic, and unresolved visibility gaps
- publish only sanitized derivatives; raw authentication evidence remains private

### MAY-IR-004 AD privilege escalation

**Status: Planned**

Acceptance criteria:
- document a controlled directory privilege change or escalation path
- preserve authoritative identity and directory-change sources
- correlate principal, session, group or role, host, and timestamp context
- evaluate benign change-control explanations
- publish a defensible attack-path narrative and detection recommendations

### MAY-IR-005 full Windows DFIR

**Status: Planned**

Acceptance criteria:
- document authorization, scope, acquisition decisions, custody, and integrity checks
- perform targeted endpoint acquisition using a repeatable workflow
- produce a multi-source normalized timeline
- analyze relevant event, registry, file-system, execution, persistence, and identity artifacts
- include memory triage only if the capability has reached the required maturity and collection is justified
- state root cause or explain why evidence cannot establish it
- publish a complete sanitized case study with response and prevention recommendations

## Capability roadmap

### Endpoint DFIR

- targeted forensic acquisition — **Planned**
- reusable Windows timeline workflow — **Planned**
- disk and execution-artifact analysis — **Planned**
- memory acquisition and triage — **Planned**
- public sanitization and public-safe derivation — **Verified**
- end-to-end private evidence handling — **Installed** pending a completed case that verifies ledger, integrity, lineage, and source/working-copy controls

### Identity and Active Directory

- authentication and session correlation — **Planned**
- credential-abuse investigation workflow — **Planned**
- privilege and group-change reconstruction — **Planned**
- endpoint and identity timeline correlation — **Planned**

### Network

- DNS and connection pivots supporting endpoint cases — **Planned**
- documented packet or flow collection boundary — **Planned**
- cross-host timeline correlation — **Planned**

### Cloud

AWS is an adjacent future cloud range. No AWS provisioning is included or implied in the current work.

- approved cloud evidence dataset and custody model — **Planned**
- CloudTrail and IAM investigation workflow — **Planned**
- first evidence-backed AWS case study — **Planned**
- Azure and GCP investigation content — **Planned**

## Detection engineering as a supporting capability

Preserve and continue the existing detection program:

- field normalization improvements
- durable Splunk saved searches and alerts
- standardized validation latency
- detection quality scoring
- ATT&CK coverage reporting
- rule versioning and regression tests
- generated-versus-canonical content separation

Detection acceptance continues to use the repository's existing rule, fixture, conversion, and live-validation controls. Investigation maturity statuses do not replace those controls.

## Portfolio acceptance goals

- a visitor can identify the investigative question, evidence, timeline, reasoning, and outcome of each completed case
- every material conclusion traces to an evidence identifier or sanitized source artifact
- raw evidence, credentials, acquisitions, and sensitive infrastructure details remain private
- AI output is disclosed when material, independently validated, and never treated as evidence
- a detection engineer can still trace scenario -> rule -> query -> fixture -> live evidence
- existing detection, purple-team, automation, and URL structure remain intact
- Planned work is not presented as implemented, verified, or live validated
