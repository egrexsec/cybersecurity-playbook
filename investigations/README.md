# Investigations

This directory is the investigation-led center of the portfolio. It organizes defensible technical analysis by investigative domain while preserving detection engineering and purple-team validation as supporting capabilities.

## Capability maturity

Investigation and DFIR capabilities use these statuses:

- **Planned** — scope and acceptance criteria exist, but no implementation evidence is published.
- **Installed** — required tooling or collection capability is available, but the workflow is not yet verified end to end.
- **Verified** — the workflow has been exercised successfully with reviewable evidence.
- **Live validated** — the workflow has been exercised against approved live lab activity with sanitized, traceable results.

These statuses describe investigation capability maturity. They do not replace Sigma-native rule lifecycle values or the validation statuses used by detection content.

## Domains

| Domain | Current maturity | Scope |
|---|---|---|
| [Endpoint](endpoint/README.md) | **Installed** | Existing scenario-linked notes are present, but complete 21-step investigation cases remain Planned |
| [Identity](identity/README.md) | **Planned** | Credential abuse, lateral movement, and Active Directory privilege investigations |
| [Network](network/README.md) | **Planned** | Connection, DNS, and cross-host investigative pivots |
| [Cloud](cloud/README.md) | **Planned** | AWS-first cloud investigation methods; no cloud range is provisioned |

## Investigation workflows

- [Investigation lifecycle](../docs/workflows/investigation-lifecycle.md)
- [Evidence handling](../docs/workflows/evidence-handling.md)
- [Forensic acquisition](../docs/workflows/forensic-acquisition.md)
- [Timeline analysis](../docs/workflows/timeline-analysis.md)
- [Memory triage](../docs/workflows/memory-triage.md)
- [AI-assisted investigations](../docs/workflows/ai-assisted-investigations.md)

## Publication boundary

Raw evidence, full acquisitions, credentials, and sensitive infrastructure details remain private. Only sanitized excerpts, hashes, derived timelines, reproducible queries, and conclusions suitable for public review belong in this repository. AI output may assist analysis, but it is not evidence and cannot establish a finding without validation against source artifacts.
