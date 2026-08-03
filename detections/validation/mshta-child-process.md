# Mshta Child-Process Validation

DET-2026-015 detects command shells and script interpreters whose direct parent is `mshta.exe`. Endpoint protection prevented the exact inline Atomic before child creation. A modified benign local HTA and the multi-stage campaign both produced the intended lineage and matched; three controls stayed quiet. Prevention telemetry and child-process detection remain separate controls.
