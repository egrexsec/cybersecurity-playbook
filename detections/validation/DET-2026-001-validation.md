# DET-2026-001 Validation Record

## Detection set
- Sigma: `detections/sigma/windows/process_creation/suspicious_powershell_execution.yml`
- Wazuh test-scope translation: `detections/wazuh/windows/powershell/DET-2026-001-local_rules.xml`
- Supporting built-ins observed during replay:
  - `92041` Value added to registry key has Base64-like pattern
  - `91809` Powershell script may be using Base64 decoding method

## Validation status
**Pass with platform-specific implementation note**

The portable Sigma rule stays process-creation focused for portability.
The live Wazuh test-scope rule was implemented as a **hybrid translation** chained from existing high-signal Wazuh rules because the guest-exec delivery path heavily base64-encodes the PowerShell process command line, making direct command-line-only matching less reliable than script-block and registry-derived signals.

## Live replay results

| Test | Expected | Observed | Result |
|---|---|---|---|
| Original Atomic registry-backed execution | alert | custom `100201` fired | pass |
| Modified base64 + `Invoke-Expression` variant | alert | custom `100202` fired | pass |
| Benign `Get-Date` | no custom alert | no custom alert | pass |
| Benign `Get-Process` | no custom alert | no custom alert | pass |

## Custom rule behavior

| Rule ID | Purpose | Trigger source |
|---|---|---|
| `100201` | confirm the original approved Atomic registry-backed test | chained from built-in `92041` plus Atomic-specific registry value pattern |
| `100202` | detect suspicious PowerShell decode-and-execute behavior | chained from built-in `91809` plus `Invoke-Expression` / `iex` requirement |

## Important findings
1. The approved Atomic test produced a strong registry + base64 signal in Wazuh even before the custom rule.
2. The modified variant produced a strong PowerShell script-block signal via built-in `91809`.
3. Broad built-in alerts such as `92205` still fire on benign script runs that create files under Windows temp/root-adjacent paths, so they should not be used alone as success criteria for this scenario.
4. Low-severity built-ins such as `91815` and `91816` can legitimately appear during benign negative tests; the custom rules avoided escalating those tests.

## Evidence files
- `evidence/sanitized/PT-2026-001/positive_atomic_validation.json`
- `evidence/sanitized/PT-2026-001/positive_variant_validation.json`
- `evidence/sanitized/PT-2026-001/negative_get_date_validation2.json`
- `evidence/sanitized/PT-2026-001/negative_get_process_validation.json`

## Follow-up improvements
- Add a cleaner Wazuh rule path that does not depend on built-in SIDs.
- Reduce noisy dependence on `92205` for file-creation side effects.
- Add a repo-side parser that extracts sanitized event excerpts from Windows event logs into stable fixtures.
