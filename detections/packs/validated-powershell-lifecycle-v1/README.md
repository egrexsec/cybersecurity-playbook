# Validated PowerShell Detection Lifecycle v1

This is the canonical, machine-verifiable portfolio pack for `PT-2026-001` / `T1059.001`.

It connects one detection engineering lifecycle without copying raw telemetry between repositories:

1. **Author and validate:** `cybersecurity-playbook` owns the Sigma rule, positive and negative fixtures, generated queries, hashes, validation record, and sanitized evidence.
2. **Historical conversion proof:** `DetLab-DAC` produced the preserved 2026 conversion capture. Current generation and validation are self-contained in `cybersecurity-playbook` and do not require the retired repository.
3. **Execute and evidence:** `mayuri-purple-team-lab` owns the controlled execution environment and the sanitized detection-to-case result.
4. **Publish:** `mell0wx.tech` presents the case study and links back to these source artifacts.

## Verify

```bash
python3 automation/build_powershell_lifecycle_pack.py --check
python3 -m unittest tests.test_powershell_lifecycle_pack -v
python3 automation/validators/sigma_ops.py test-fixtures --technique T1059.001
```

`manifest.json` is deterministic. It records SHA-256 hashes for the canonical Sigma source, all nine fixtures, and the three checked-in query artifacts. CI should fail if any referenced artifact changes without rebuilding the manifest.

## Evidence boundary

The manifest contains public paths, hashes, dates, and validation status only. It deliberately excludes raw event XML, internal addresses, credentials, receiver locations, and case identifiers. Detailed runtime evidence remains in the designated sanitized evidence locations.

## Known limits

- The live result dates to 2026-07-18; this pack organizes and verifies that evidence rather than claiming a new execution.
- Numeric end-to-end detection latency was not preserved in the original validation record.
- The historical DetLab screenshot and public portfolio article are presentation artifacts. They are not dependencies for current validation or artifact generation.
