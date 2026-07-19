# PT-2026-001 Results

## Outcome
**Successful first end-to-end milestone** for a safe, victim-scoped PowerShell execution scenario.

## Preflight
- Approved target scope validated.
- Snapshot prerequisite validated by repo preflight.
- Sysmon, Wazuh, and PowerShell logging confirmed present on the victim.

## Baseline recorded before execution
- Time recorded: `2026-07-18T01:44:26Z`
- 30-minute victim counts:
  - PowerShell `4103`: `213`
  - PowerShell `4104`: `123`
  - Security `4688` matching PowerShell: `0`
  - Sysmon `1` matching PowerShell: `16`

## Live execution summary
| Step | Result |
|---|---|
| Original Atomic registry-backed fileless execution | completed; marker file created |
| Modified base64 + `Invoke-Expression` variant | completed; marker file created |
| Benign `Get-Date` | completed |
| Benign `Get-Process` | completed |
| Cleanup | completed |

## Detection summary
| Detection source | Original Atomic | Modified variant | Negatives |
|---|---|---|---|
| Wazuh built-in | `92041` fired | `91809` fired | low-severity built-ins only |
| Custom PT rule | `100201` fired | `100202` fired | none |

## Public-safe takeaways
- A public repository can demonstrate real detection engineering value **without** publishing raw EVTX, memory images, or secrets.
- Platform-specific translation matters: the portable Sigma remained process-creation focused, while the live Wazuh rule chained from built-in script-block and registry detections for stronger validation in this environment.
- Benign tests are essential because the stock ruleset still emits lower-severity noise during normal administrative PowerShell activity.
