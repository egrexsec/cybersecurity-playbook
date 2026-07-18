# PT-2026-004 Sanitized Evidence

Files in this directory are sanitized summaries linked to the scheduled task validation scenario.

## Primary evidence
- `detections/validation/live/VAL-2026-004-PT-2026-004.json`
- `detections/validation/DET-2026-004-validation.md`

## Highlights
- positive `schtasks.exe /Create` execution detected
- positive `Register-ScheduledTask` variant detected
- three benign negative tests remained quiet
- cleanup completed successfully
