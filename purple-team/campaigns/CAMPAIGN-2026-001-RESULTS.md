# CAMPAIGN-2026-001 Results

A benign loopback-only chain completed on the approved Windows victim:

1. PowerShell retrieved an HTA to a local file.
2. `mshta.exe` opened the staged HTA.
3. The HTA launched a benign PowerShell child that wrote a marker.

Source and staged hashes matched. DET-2026-014 fired at `2026-08-03T14:49:47Z`; DET-2026-015 fired three seconds later at `2026-08-03T14:49:50Z`. The marker was verified, cleanup returned zero residue, and the second cleanup pass was also clean. No external C2, credentials, lateral movement, or persistence were used.
