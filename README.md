# cybersecurity-playbook

[![Detection validation](https://github.com/egrexsec/cybersecurity-playbook/actions/workflows/detection-validation.yml/badge.svg)](https://github.com/egrexsec/cybersecurity-playbook/actions/workflows/detection-validation.yml)

An **investigation-led cybersecurity portfolio** focused on incident response, DFIR, threat hunting, cloud investigation, and evidence-backed detection engineering.

The repository preserves repeatable investigation methods, sanitized case material, Sigma detections, generated SIEM queries, validation fixtures, threat-hunting hypotheses, and historical live-validation evidence.

> **Current direction:** build portable investigation capability without depending on a permanent lab. The former Mayuri environment was decommissioned in October 2026; its validated evidence remains preserved as historical provenance.

## Portfolio at a glance

| Area | Current state |
|---|---|
| Windows detection validation | **15 historically live-validated scenarios** |
| Sigma content | **15 canonical rules** |
| Test coverage | **79 fixtures** — 32 positive / 47 negative |
| Threat hunting | **16 hypotheses**, including 3 completed Detection Cycle 1 hunts |
| AWS Cloud IR | **Verified** through the Flaws2.cloud Defender workflow |
| SIEM portability | Generated **Splunk SPL** and **Elastic EQL** |
| DFIR | Investigation framework and evidence-handling foundation; deeper acquisition/timeline work in progress |

See [Portfolio Metrics](docs/current-state/PORTFOLIO_METRICS.md) and the [Capability Matrix](docs/current-state/CAPABILITY_MATRIX.md) for the current evidence-backed state.

## Featured work

### AWS Cloud Incident Response — Flaws2.cloud Defender

A Windows-first CloudTrail investigation workflow using **AWS CLI, PowerShell, and jq**.

Skills exercised:

- AWS CLI identity and named-profile usage
- CloudTrail retrieval from S3
- recursive log parsing with PowerShell and `jq`
- chronological timeline construction
- principal, source IP, event, and user-agent correlation
- credential-theft investigation
- IAM / STS pivots
- ECR resource-policy analysis
- Athena as a scalable CloudTrail-querying model

[Read the Flaws2.cloud Defender case study](case-studies/aws/flaws2-defender/README.md)

### Validated PowerShell Detection Lifecycle

An end-to-end example that traces controlled behavior through:

```text
scenario
  → telemetry
  → investigation
  → Sigma rule
  → generated SIEM queries
  → positive / negative fixtures
  → validation evidence
```

[Read the Validated PowerShell Detection Lifecycle v1](detections/packs/validated-powershell-lifecycle-v1/README.md)

### Detection Cycle 1

The final Mayuri-era threat-informed cycle added:

- **PT-2026-014 — T1105** PowerShell web ingress transfer
- **PT-2026-015 — T1218.005** mshta child-process proxy execution
- three completed threat hunts
- a bounded benign campaign correlating download-to-execution behavior

The program-state documentation is retained under the [Mayuri historical archive](docs/history/mayuri/README.md).

## Investigation model

The repository uses a canonical [21-step investigation lifecycle](docs/workflows/investigation-lifecycle.md) covering:

```text
scope
  → triage
  → evidence acquisition
  → timeline reconstruction
  → endpoint / identity / network / cloud analysis
  → root cause
  → persistence / lateral movement / resource access
  → response recommendations
  → detection lessons
  → sanitized reporting
```

Supporting workflows include:

- [Evidence handling](docs/workflows/evidence-handling.md)
- [Forensic acquisition](docs/workflows/forensic-acquisition.md)
- [Timeline analysis](docs/workflows/timeline-analysis.md)
- [Memory triage](docs/workflows/memory-triage.md)
- [AI-assisted investigations](docs/workflows/ai-assisted-investigations.md)

Raw evidence, credentials, full acquisitions, and sensitive infrastructure details remain outside the public repository. Public artifacts are sanitized derivatives with enough provenance to review the method and reasoning.

## Validation model

The repository distinguishes capability maturity from detection-rule lifecycle.

- **Live validated** — exercised against approved live lab activity with positive/negative evidence and cleanup confirmation. Mayuri-backed records retain this status as historical evidence.
- **Verified** — exercised successfully against an approved dataset or bounded workflow with reviewable evidence.
- **Fixture tested** — validated offline against sanitized positive and negative fixtures.
- **Conversion supported** — canonical Sigma successfully converts to a target backend, without implying live backend validation.
- **Planned / Installed** — scoped or available, but not yet supported by complete evidence.

Historical live-validation records cover these ATT&CK techniques:

`T1037.001`, `T1047`, `T1053.005`, `T1059.001`, `T1059.003`, `T1105`, `T1197`, `T1218.005`, `T1218.010`, `T1218.011`, `T1543.003`, `T1546.003`, `T1546.013`, `T1547.001`, `T1569.002`.

## Repository map

| Path | Purpose |
|---|---|
| `investigations/` | Domain-organized endpoint, identity, network, and cloud investigation material |
| `dfir/` | Reusable acquisition, timeline, memory, and evidence-handling methods |
| `case-studies/` | Portfolio-ready end-to-end technical investigations |
| `learning-labs/` | Concise CyberDefenders, TryHackMe, HTB, and other training notes |
| `threat-hunting/` | Hunt hypotheses and investigation pivots |
| `purple-team/` | Historical scenario and campaign definitions |
| `detections/sigma/` | Canonical authored Sigma rules |
| `detections/generated/` | Generated Splunk and Elastic queries |
| `detections/validation/` | Human-readable and structured validation records |
| `tests/fixtures/` | Positive and negative rule fixtures |
| `automation/` | Validation and content-processing tooling |
| `docs/workflows/` | Investigation and validation operating workflows |
| `docs/current-state/` | Current portfolio status, metrics, and capability maturity |
| `docs/history/mayuri/` | Historical Mayuri infrastructure and validation-program records |
| `templates/` | Investigation, hunt, and detection authoring templates |
| `schemas/` | Structured content validation schemas |

## Detection engineering

Detection engineering remains a supporting capability rather than the sole purpose of the repository.

The portable workflow is:

```text
investigative lead
  → behavioral hypothesis
  → telemetry review
  → Sigma authoring
  → Splunk / Elastic conversion
  → fixture testing
  → evidence-backed validation
```

Existing live SIEM evidence is historical. The Mayuri Splunk environment no longer exists, and Elastic remains **conversion supported**, not live deployed.

## Quick-start repository validation

From the repository root:

```bash
python3 playbook validate
python3 playbook --json sigma lint
python3 playbook --json sigma convert --target all
python3 playbook --json test fixtures
python3 playbook --json validate previous-scenarios
python3 playbook --json status
python3 playbook --json timeline
python3 playbook --json metrics
python3 automation/validators/check_markdown.py
```

## Current priorities

The next stages of the portfolio focus on:

1. deeper endpoint DFIR and Windows timeline reconstruction
2. identity and authentication investigations
3. additional AWS incident investigations using bounded datasets
4. practical CyberDefenders investigations
5. targeted TryHackMe and HTB Academy material where it strengthens IR/DFIR capability
6. promoting only the strongest learning exercises into polished case studies

## Boundaries and limitations

- Mayuri is **decommissioned**; live-validation claims refer to historical evidence.
- No standing AWS investigation range is provisioned by this repository.
- AWS CloudTrail / IAM investigation capability is **Verified** through the Flaws2.cloud Defender dataset and workflow.
- Elastic output is generated but has **not** been live validated against an Elastic deployment.
- Historical Splunk validation includes raw-XML matching where field normalization was incomplete.
- Durable production SIEM alerts and saved searches are not claimed as deployed.
- Full forensic acquisition, memory analysis, identity correlation, and network-forensics capability remain active development areas.
- This repository is a technical portfolio and investigation-content library, **not a production security platform**.
- AI-assisted analysis may support workflow development, but AI output is never treated as evidence without validation against source artifacts.

## Documentation

- [Roadmap](ROADMAP.md)
- [Current Portfolio Status](docs/current-state/PORTFOLIO_STATUS.md)
- [Capability Matrix](docs/current-state/CAPABILITY_MATRIX.md)
- [Portfolio Metrics](docs/current-state/PORTFOLIO_METRICS.md)
- [Investigations](investigations/README.md)
- [DFIR Capability Library](dfir/README.md)
- [AWS Case Studies](case-studies/aws/README.md)
- [Learning Labs](learning-labs/README.md)
- [Mayuri Historical Archive](docs/history/mayuri/README.md)
- [Detection Content Specification v1](docs/detection-content-spec-v1.md)
- [Contributing](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
