# DET-2026-002 Validation Record

## Detection set
- Sigma: `detections/sigma/windows/process_creation/suspicious_cmd_execution.yml`
- Wazuh test-scope translation: `detections/wazuh/windows/cmd/DET-2026-002-local_rules.xml`

## Validation status
**Pass**

## Live replay results

| Test | Expected | Observed | Result |
|---|---|---|---|
| Batch-script execution | alert | custom `100203` fired | pass |
| Suspicious environment-variable-based cmd execution | alert | custom `100204` fired | pass |
| Benign `cmd /c dir` | no custom alert | no custom alert | pass |
| Benign `cmd /c echo` | no custom alert | no custom alert | pass |

## Custom rule behavior

| Rule ID | Purpose |
|---|---|
| `100203` | detect the approved batch-script execution path used in PT-2026-002 |
| `100204` | detect suspicious cmd invocation using environment-variable-based indirection |

## Platform notes
1. The suspicious variant was also visible through built-in Wazuh process-spawn context during initial replay, but the validated custom signal for this scenario is `100204`.
2. The guest-exec delivery path preserved the unusual command line well enough for direct Sysmon command-line matching in this cmd.exe scenario.
3. A malformed intermediate rules update briefly broke Wazuh manager startup during tuning; the final committed rule file was corrected and the manager was restored to active state before continuing validation.

## Evidence files
- `evidence/sanitized/PT-2026-002/positive_batch_validation.json`
- `evidence/sanitized/PT-2026-002/positive_variant_validation.json`
- `evidence/sanitized/PT-2026-002/negative_dir_validation.json`
- `evidence/sanitized/PT-2026-002/negative_echo_validation.json`
