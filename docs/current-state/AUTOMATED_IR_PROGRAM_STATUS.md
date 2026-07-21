# Automated IR program status

| Capability | Current status | Evidence | Boundary / blocker | Next action |
|---|---|---|---|---|
| Alert intake | Fixture tested | strict alert schema, receiver tests, sample payload | durable SIEM alert object not verified | add approved SIEM adapter |
| Deduplication | Fixture tested | deterministic fingerprint and duplicate-count tests | production event volume not tested | load-test separately |
| Case management | Fixture tested | create, enrich, collect, hunt-plan, timeline, analyze, report, cleanup tests | no fresh live case asserted | keep runtime cases outside Git |
| CTI enrichment | Fixture tested | typed indicators, timeout, fail-open result, advisory-only behavior | no current provider health assertion | add private provider adapter |
| Asset enrichment | Repository backed | sanitized role inventory | not a live CMDB or hypervisor query | keep role metadata separate from runtime discovery |
| Evidence collection planning | Implemented | explicit artifact classes and `planned` status | no live acquisition occurs | add external collector adapter |
| Fixture collection | Tested | SHA-256 artifact manifests | fixtures are not live evidence | retain explicit `fixture-collected` label |
| Live DFIR collection | Not configured | adapter boundary documented | authorization and collector credentials required | implement externally |
| Unified timeline | Fixture tested | deterministic alert/enrichment timeline | broader source feeds absent | add bounded parsers |
| Process context | Fixture tested | alert-derived process context | not a complete endpoint process tree | integrate collector data later |
| Threat hunting | Reference-only | hunt query artifact and `planned` state | no SIEM query adapter | do not claim result counts |
| Analysis/reporting | Fixture tested | sanitized findings and report test | no current host/SIEM verification | preserve evidence limitations |
| Containment planning | Implemented | human-review plan generation | execution intentionally disabled | retain approval boundary |
| Live validation | Disabled by default | preflight schema, approval-token check, external adapter contract | no public embedded executor | run only after private authorization |
| n8n orchestration | Sanitized template | importable workflow JSON | deployment/import not verified | validate in an authorized environment |
| GitHub Actions | Implemented on branch | unit, content, generated-output, and public-safety checks | branch CI pending push | watch PR checks |

## Operational boundary

The repository can validate its contracts and exercise the IR lifecycle against fixtures. It does not currently prove live SIEM alerting, endpoint collection, CTI availability, snapshot readiness, or containment execution.
