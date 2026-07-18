# Validation Results

## Positive fixtures
The repo contains positive PowerShell fixtures under `tests/fixtures/T1059.001/positive/`.

## Negative fixtures
The repo contains negative PowerShell fixtures under `tests/fixtures/T1059.001/negative/`.

## Live execution result
Source of truth:
- `detections/validation/live/VAL-2026-001-PT-2026-001.json`
- `detections/validation/DET-2026-001-validation.md`

## Detection result
PT-2026-001 is represented in the repo as a live-validated execution scenario with positive and negative evidence.

## Cleanup outcome
Cleanup is explicitly captured in the validation record and scenario result notes.

## Known gaps
- live latency is not yet computed numerically in all records
- field normalization in Splunk is still incomplete
