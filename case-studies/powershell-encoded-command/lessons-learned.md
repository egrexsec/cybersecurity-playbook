# Lessons Learned

## What worked
- controlled replay on an approved victim
- strong PowerShell operational telemetry
- fixture-backed rule testing plus live validation

## What required adjustment
- platform-specific translations matter
- raw XML matching remains a practical fallback where live field normalization is incomplete

## Production differences
In a production program, you would want:
- stronger field normalization
- durable alerts/search objects
- broader false-positive baselining
- richer investigation automation

## Next pivots
- additional persistence techniques
- stronger DFIR timelines
- broader ATT&CK coverage reporting
