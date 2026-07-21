# Purple-team program status

## Milestone matrix

| Capability | Current status | Evidence | Boundary / blocker | Next action |
|---|---|---|---|---|
| Repository validation | Ready | schema, Markdown, public-safety, and unit checks | offline only | keep CI green |
| Windows detection content | Fixture tested | 11 Sigma rules and 59 fixtures | Windows-centric | expand only with fixtures |
| Generated Splunk content | Conversion supported | official and environment-wrapper SPL | deployment not verified | add backend registry and deployment profiles |
| Generated Elastic content | Conversion supported | EQL output | no live Elastic backend validation | retain conversion-only label |
| Historical live summaries | Historical evidence | 11 sanitized records dated 2026-07-18 | not current-health evidence | require fresh preflight for replay |
| Threat hunts | Planned / reference-only | 11 hunt definitions | no bounded SIEM adapter | implement adapter and result contract |
| IR intake and case workflow | Fixture tested | deterministic intake, enrichment, collection plan, timeline, analysis, report | no fresh webhook replay | test via approved adapter when authorized |
| CTI enrichment | Fixture tested contract | timeout, fail-open, advisory-only tests | no current provider health claim | add private provider adapter |
| DFIR collection | Fixture tested / planned | artifact hashes and explicit status model | no live collector adapter | implement Velociraptor contract externally |
| Containment | Intentionally disabled | approval-aware plans | destructive execution prohibited | retain human approval gate |
| GitHub CI | Ready locally; pending branch CI | workflow includes unit and public-safety checks | new commit not yet pushed | verify PR checks |
| Shared DetLab contract | Not started | assessment complete | cross-repository schema required | implement specification v1 |

## Current maturity

**Functional detection-engineering MVP / early Detection-as-Code platform.**

Supported by:

- canonical Sigma source rules;
- positive and negative fixtures;
- reproducible generated queries;
- schema-valid scenarios and sanitized historical summaries;
- deterministic IR workflow tests;
- public-safety and secret-scanning gates.

Not yet a higher-maturity operational platform because:

- live SIEM, endpoint, CTI, and DFIR adapters are not configured in the public repository;
- current deployment and telemetry health are not asserted;
- field normalization remains incomplete;
- durable SIEM saved-search deployment is not verified;
- Elastic support remains conversion-only;
- destructive response remains disabled.
