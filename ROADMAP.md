# Roadmap

## Direction

Evolve this repository as an investigation-led technical portfolio centered on repeatable incident-response, DFIR, threat-hunting, and cloud-investigation methods.

Detection engineering, purple-team validation, and automation remain supporting capabilities. Historical Mayuri validation evidence is preserved as provenance, but Mayuri is no longer an active lab dependency.

## Status model

Investigation and DFIR capability maturity uses:

- **Planned** — scope and acceptance criteria exist; implementation is not evidence-backed.
- **Installed** — required tooling or collection capability is available but not verified end to end.
- **Verified** — the workflow has been exercised successfully with reviewable evidence or an approved bounded dataset.
- **Live validated** — the workflow has been exercised against approved live lab activity with sanitized, traceable results.

Historical Mayuri live-validation records retain their original status after decommissioning.

## Current evidence-backed foundation

- twelve Windows purple-team scenarios retain historical live-validation status
- endpoint investigation notes exist for PT-2026-001 through PT-2026-012
- Sigma linting, conversion, fixture testing, and validation-record workflows remain operational
- public-safe evidence-handling and case-study material demonstrate traceability
- the Flaws2.cloud Defender track provides a verified AWS CloudTrail investigation workflow
- raw evidence remains private; the repository stores sanitized derivatives and documentation

## Investigation roadmap

### Endpoint

- Windows execution investigation — **Installed**
- persistence investigation — **Installed**
- reusable endpoint timeline reconstruction — **Planned**
- targeted forensic acquisition — **Planned**
- execution-artifact and filesystem analysis — **Planned**

### Identity

- authentication and session correlation — **Planned**
- credential-abuse investigation workflow — **Planned**
- privilege and group-change reconstruction — **Planned**
- endpoint and identity timeline correlation — **Planned**

### Network

- DNS and connection pivots supporting endpoint cases — **Planned**
- packet or flow evidence-handling boundary — **Planned**
- cross-host timeline correlation — **Planned**

### Cloud

AWS is an active investigation domain, but this repository does not maintain a standing AWS lab.

- CloudTrail local-analysis workflow with PowerShell and jq — **Verified**
- AWS CLI profile and identity-pivot workflow — **Verified**
- IAM / STS investigation workflow — **Verified**
- AWS resource-policy review workflow — **Verified**
- Athena-at-scale investigation workflow — **Conceptually reviewed**
- first polished AWS case study — **Verified** through Flaws2.cloud Defender
- additional AWS investigations using bounded training datasets — **Planned**
- Azure and GCP investigation content — **Planned**

## DFIR capability roadmap

- targeted forensic acquisition — **Planned**
- reusable Windows timeline workflow — **Planned**
- disk and execution-artifact analysis — **Planned**
- memory acquisition and triage — **Planned**
- public sanitization and public-safe derivation — **Verified**
- end-to-end private evidence handling — **Installed**

## Detection engineering as a supporting capability

Preserve and continue:

- field normalization improvements
- durable SIEM saved searches and alerts where an approved environment exists
- detection quality scoring
- ATT&CK coverage reporting
- rule versioning and regression tests
- generated-versus-canonical content separation
- fixture-driven testing

The repository should not imply that historical Mayuri live detections can still be replayed against that retired environment.

## Learning-lab strategy

Training platforms are inputs to the portfolio, not the portfolio itself.

Use `learning-labs/` for concise notes from:

- CyberDefenders
- TryHackMe
- Hack The Box / HTB Academy
- other bounded training datasets

Promote only stronger investigations into `case-studies/` when they include a defensible investigative question, evidence, timeline, analysis, findings, response considerations, and lessons learned.

## Portfolio acceptance goals

- a visitor can identify the investigative question, evidence, timeline, reasoning, and outcome of each completed case
- every material conclusion traces to an evidence identifier or sanitized source artifact
- historical lab evidence is clearly labeled as historical
- raw evidence, credentials, acquisitions, and sensitive infrastructure details remain private
- AI output is independently validated and never treated as evidence
- completed learning labs do not automatically become portfolio case studies
- Planned work is not presented as implemented, verified, or live validated
