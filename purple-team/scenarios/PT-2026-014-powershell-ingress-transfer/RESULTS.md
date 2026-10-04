# PT-2026-014 Results

- Exact Atomic UUID: `42dc4460-9aa6-45d3-b1a6-3955d34e1fe8`.
- Exact positive: benign loopback transfer completed; source and destination hashes matched; detection fired at `2026-08-03T14:34:40Z` (~7.711 s from start).
- Modified positive: `Invoke-WebRequest -OutFile` transfer completed; hashes matched; detection fired at `2026-08-03T14:35:40Z` (~0.502 s).
- Negatives: WebClient object construction, bounded HEAD request without `OutFile`, and command discovery remained quiet.
- Cleanup: first and idempotent second passes both returned `Clean=true` with zero residue.
- Limitation: current live detection depends on PowerShell script-block telemetry; process-only sources are insufficient.
