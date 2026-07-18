# Detection Engineering

## Initial logic
The first objective was to detect suspicious PowerShell decode-and-execute behavior rather than just one exact command line.

## Canonical rule
- `detections/sigma/windows/process_creation/suspicious_powershell_execution.yml`

## Conversion path
- generated Splunk SPL under `detections/generated/splunk/official/`
- generated Elastic output under `detections/generated/elastic/`
- live-lab Splunk query under `detections/generated/splunk/live/`

## False-positive considerations
The repository explicitly tests benign PowerShell activity so the rule is not validated on a single alert alone.

## Tuning outcome
The canonical Sigma stays portable while the repo documents platform-specific live-validation constraints for the current lab.
