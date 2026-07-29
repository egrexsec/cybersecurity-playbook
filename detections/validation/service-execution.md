# Service Execution Detection Validation

- Scenario: `PT-2026-012`
- Validation: `VAL-2026-012`
- Technique: `T1569.002`
- Atomic UUID: `2382dee2-a75f-49aa-9378-f52df6ed3fb1`
- Result: **passed live validation**

## Assertions
- Original service-launched PowerShell marker path: detected.
- Modified service-launched command-shell path: detected.
- `sc.exe query`: not detected.
- `Get-Service`: not detected.
- Service create/delete without start: not detected.
- Cleanup and postflight health: passed.

See the [live JSON record](live/VAL-2026-012-PT-2026-012.json), [scenario results](../../purple-team/scenarios/PT-2026-012-service-execution/RESULTS.md), and [sanitized evidence](../../evidence/sanitized/PT-2026-012/README.md).
