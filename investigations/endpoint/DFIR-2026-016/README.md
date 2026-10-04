# DFIR-2026-016 — Download-to-Execution Chain

## Investigation question

Did a PowerShell web retrieval produce a staged HTA that was subsequently opened by `mshta.exe` and used to launch a script interpreter on the same endpoint?

## Timeline pivots

1. Start with PowerShell script-block events containing web retrieval plus file output behavior.
2. Identify the destination path and hash; pivot to file-creation telemetry when available.
3. Search a bounded interval for `mshta.exe` referencing the staged content.
4. Reconstruct direct child lineage from `mshta.exe` to PowerShell, cmd, wscript, or cscript.
5. Compare user, integrity level, process identifiers, and adjacent network/file activity.
6. Determine whether endpoint prevention acted before process creation.

## Containment and evidence

Preserve raw telemetry and active observables privately. Public reporting should retain only role labels, aggregate counts, bounded timestamps, behavioral conclusions, and sanitized hashes needed for controlled-test provenance.
