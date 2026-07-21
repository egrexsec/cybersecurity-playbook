# Detection platform readiness

## Status boundary

This page separates repository capability from historical environment observations. It does **not** assert current lab health or authorize replay. The prior environment assessment was recorded on 2026-07-18 and must be revalidated through the private preflight process before any live action.

## Repository readiness

| Capability | Current repository status | Evidence |
|---|---|---|
| Scenario contracts | Ready | 11 schema-valid scenario definitions |
| Sigma source rules | Ready | 11 canonical Windows rules |
| Offline fixtures | Ready | 59 positive/negative fixtures passing |
| Splunk generation | Ready for conversion | Official and environment-wrapper SPL regenerated in CI |
| Elastic EQL generation | Ready for conversion | Generated EQL; no live Elastic validation claimed |
| Historical validation summaries | Ready | 11 sanitized, schema-valid summaries |
| Deterministic IR intake | Fixture tested | Unit tests cover deduplication and dry-run behavior |
| CTI enrichment contract | Fixture tested | Bounded, fail-open, advisory-only behavior |
| DFIR collection planning | Fixture tested | Fixture hashes and explicit `planned`/`fixture` statuses |
| Live DFIR collection | Not configured | Requires an external collector adapter |
| SIEM hunt execution | Not configured | Repository currently prepares query references only |
| Live scenario execution | Disabled by default | Requires private preflight, approval token, and external adapter |
| Destructive containment | Disabled | Plans require human approval; no execution path is enabled |

## Historical environment observations

Sanitized summaries indicate that an authorized lab previously produced positive, variant, negative, and cleanup outcomes for the 11 Windows scenarios. Those records:

- are historical rather than current-health checks;
- omit raw events, commands, host identities, users, addresses, VM identifiers, and credentials;
- do not prove that SIEM objects, forwarding, DNS, time, storage, snapshots, CTI, or collectors are currently healthy;
- do not establish portability to different indexes, tables, fields, sourcetypes, or data models.

## Required preflight for live work

Before a live validation, a private attestation must confirm:

1. target identity and explicit authorization;
2. DNS and name resolution;
3. time synchronization;
4. storage and retention health;
5. expected telemetry and SIEM ingestion;
6. rollback snapshot availability;
7. expected events and search window;
8. cleanup steps and timeout;
9. an unexpired approval window.

The CLI additionally requires a private mode-`0600` approval token and an executable environment-specific adapter outside the public repository.

## Readiness decision

- Safe to run offline schema, conversion, fixture, and IR unit tests: **Yes**.
- Safe to treat historical summaries as current environment health: **No**.
- Safe to execute a live scenario without a fresh private preflight: **No**.
- Safe to deploy or claim live Elastic support: **No**.
- Safe to execute destructive containment from this repository: **No**.
