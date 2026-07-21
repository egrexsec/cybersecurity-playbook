# Automated IR platform assessment

## Status boundary

This document describes repository capability and sanitized historical observations. It is **not** a statement of current lab health. Exact hostnames, addresses, VM identifiers, DNS names, firewall rules, connector IDs, credentials, and snapshot names are intentionally excluded.

| Capability | Status | Evidence boundary |
|---|---|---|
| Sigma and fixture validation | Fixture tested | Repository CI and local fixtures |
| Splunk alert normalization | Fixture tested | Synthetic alert envelope |
| Deterministic case creation | Unit tested | Local temporary case stores |
| Duplicate alert handling | Unit tested | Fingerprint-based idempotency tests |
| CTI enrichment contract | Unit tested | Fail-open provider fixture only |
| OpenCTI/Shodan enrichment | Historically live validated | Separate sanitized deployment record; not current health |
| Evidence collection plan | Implemented | Plans artifact classes; does not claim acquisition |
| Fixture artifact collection | Fixture tested | Synthetic files only |
| Velociraptor collection | Planned | No current adapter result committed |
| Threat hunt | Scaffolded | Does not execute a live SIEM search |
| Forensic timeline | Fixture tested | Case alert and enrichment fixtures |
| Detection review/report | Fixture tested | Sanitized generated summaries |
| Containment execution | Disabled | Approval-gated planning only |
| Full SIEM-to-report workflow | Partially verified | Historical evidence removed from public branch; fresh validation required |

## Architecture

```text
internal SIEM service
  -> authenticated relay
  -> existing orchestrator
  -> authenticated IR receiver
  -> strict alert schema
  -> deterministic case engine
  -> advisory CTI enrichment
  -> collection plan / external adapter
  -> hunt and timeline processing
  -> detection feedback
  -> sanitized report
```

Runtime evidence, audit logs, case directories, environment profiles, and credentials remain outside Git. Public examples use loopback or `.invalid` defaults.

## Safety gate for live validation

Embedded lab-specific executors are not called by the normal CLI. A live run requires all of the following:

1. A private JSON preflight attestation matching `schemas/live-preflight.schema.json`.
2. Explicit authorization for the named scenario and an authorized lab role.
3. Verified identity, DNS, time, storage, telemetry, and rollback snapshot state.
4. Defined expected telemetry and cleanup steps.
5. An unexpired preflight record.
6. A mode-`0600` approval-token file matching a configured SHA-256 value.
7. An executable environment-specific adapter supplied outside the public repository.

```bash
./playbook preflight PT-2026-001 --attestation /private/runtime/preflight.json
./playbook test live PT-2026-001 \
  --preflight /private/runtime/preflight.json \
  --approval-token-file /private/runtime/approval-token
```

The run stops if any prerequisite is absent. A timeout or adapter failure leaves cleanup status explicitly unknown and requires operator verification before retry.

## Implemented local workflow

```bash
./playbook ir create --alert automation/intake/sample-splunk-alert-pt-2026-001.json
./playbook ir enrich <case-id>
./playbook ir collect <case-id>
./playbook ir hunt <case-id>
./playbook forensic timeline <case-id>
./playbook forensic analyze <case-id>
./playbook detection review <case-id>
./playbook forensic report <case-id>
./playbook ir cleanup <case-id> --dry-run
```

`ir collect` without an external adapter produces a **plan**, not a completed live collection. Fixture collection remains labeled `fixture`; only a validated live adapter may emit `live-collected`.

## Remaining blockers

- Replace canned hunt results with a bounded SIEM adapter.
- Add a Velociraptor adapter that records artifact status, source, collection time, hashes, and tool versions.
- Validate live records against one enforced schema and remove environment identifiers.
- Export parameterized Splunk saved searches with scheduling, throttling, severity, and drilldowns.
- Complete field normalization and CIM-aware mappings.
- Add end-to-end orchestration tests without embedding credentials or live values.
