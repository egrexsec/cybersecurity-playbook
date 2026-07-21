# Environment-specific live validation adapter

The public repository intentionally contains no lab addresses, credentials, host mappings, VM identifiers, snapshot names, SIEM connection details, or executable environment profile.

`./playbook test live` invokes an operator-supplied executable from the absolute path in `PLAYBOOK_LIVE_VALIDATION_ADAPTER`. The adapter is maintained outside this repository and receives one positional argument: the scenario ID.

Before invocation, the CLI verifies:

- a schema-valid, unexpired authorization/preflight attestation;
- scenario identity matching;
- identity, DNS, time, storage, telemetry, rollback, expected-telemetry, and cleanup confirmations;
- a private mode-`0600` approval-token file whose SHA-256 matches `PLAYBOOK_LIVE_APPROVAL_TOKEN_SHA256`.

The adapter must:

1. Revalidate target identity and authorization immediately before execution.
2. Run only the requested scenario against the authorized target role.
3. Enforce the scenario timeout.
4. Capture raw logs and evidence only in approved external DFIR storage.
5. Execute cleanup even when validation fails.
6. Return one JSON object on stdout matching `schemas/live-validation-adapter-result.schema.json`.
7. Write diagnostics to private operator logs, not stdout.

Example output shape:

```json
{
  "schema_version": "1.0.0",
  "scenario_id": "PT-2026-001",
  "status": "completed",
  "positive_detection_fired": true,
  "negative_tests_quiet": true,
  "cleanup_status": "confirmed",
  "evidence_location": "external-dfir-storage/case-reference",
  "limitations": [
    "Result applies only to the authorized environment and observed telemetry window."
  ]
}
```

The external evidence path is a logical reference; it must not expose an internal hostname, mount path, URL, token, or storage credential.
