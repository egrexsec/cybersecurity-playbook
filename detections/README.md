# detections/

Contains canonical detection logic, generated backend queries, platform translations, and validation records.

## Layout
- `sigma/` — canonical authored Sigma rules
- `generated/` — generated Splunk and Elastic output
- `validation/` — human-readable validation records and live JSON evidence
- `wazuh/` — platform-specific Wazuh translations or test-scope rules

## Authoring rule
Edit canonical logic in `sigma/` first.
Do not hand-edit generated output under `generated/`.
