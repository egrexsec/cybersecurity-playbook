# PT-2026-002 Results

## Outcome
**Successful second end-to-end milestone** for a safe, victim-scoped Windows Command Shell execution scenario.

## Live execution summary
| Step | Result |
|---|---|
| Batch-script cmd execution | completed; marker file created |
| Suspicious environment-variable-based variant | completed; marker file created |
| Benign `cmd /c dir` | completed |
| Benign `cmd /c echo` | completed |
| Cleanup | completed |

## Detection summary
| Detection source | Batch positive | Suspicious variant | Negatives |
|---|---|---|---|
| Custom Wazuh PT rule | `100203` fired | `100204` fired | none |
| Relevant built-in context | not required for final pass | process-spawn context observed during tuning | none required |

## Public-safe takeaways
- Low-risk `cmd.exe` behavior can be demonstrated credibly without publishing raw Windows log exports.
- Simple custom Sysmon command-line matching was more reliable here than the earlier PowerShell path because the guest-exec transport preserved the suspicious cmd command lines directly.
- Negative tests are necessary because normal administrative `cmd.exe` usage is common; custom detections should stay tightly scoped to the validated behavior.
