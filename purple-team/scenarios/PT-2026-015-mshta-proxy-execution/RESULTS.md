# PT-2026-015 Results

- Exact Atomic UUID: `8707a805-2b76-4f32-b1c0-14e558205772`.
- Exact outcome: endpoint protection prevented the inline mshta-to-PowerShell command before child-process creation. Defender recorded detection and action events; therefore the Sysmon child-process rule correctly had no event to match.
- Modified positive: a benign local HTA launched `cmd.exe` only to write a marker; the behavioral rule fired at `2026-08-03T14:36:18Z` (~1.197 s).
- Campaign corroboration: a benign downloaded HTA launched PowerShell; the rule fired at `2026-08-03T14:49:50Z` (~3.796 s).
- Negatives: command discovery, signature inspection, and a display-only local HTA remained quiet.
- Cleanup: temporary mshta processes and files were removed; repeated cleanup remained clean; no external connection remained.

## Deviation

A candidate remote-HTA Atomic was rejected after its SYSTEM/noninteractive controller path failed to honor the safe input override. Its default payload attempted an outbound external connection, and the connection failed. The run was stopped, no connection was established, all residue was removed, and that UUID is not part of the selected scenario.

## Interpretation

This scenario records two complementary controls: prevention of the exact inline Atomic and live detection of the same mshta child-process behavior through a safe modified positive and the campaign chain.
