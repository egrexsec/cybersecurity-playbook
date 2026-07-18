# PT-2026-009 Results

## Validation run
- Validation ID: `VAL-2026-009`
- Technique: `T1546.013`
- Status: validated

## Positive path
- profile modification using `Add-Content` succeeded and wrote `pt-2026-009-original.txt`
- profile append variant succeeded and wrote `pt-2026-009-variant.txt`
- both positive paths triggered the Sigma detection in Splunk

## Negative path
- benign profile existence checks remained quiet
- benign profile content reads remained quiet
- benign profile note append remained quiet
