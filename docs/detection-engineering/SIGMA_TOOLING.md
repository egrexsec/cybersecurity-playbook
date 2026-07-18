# Sigma Tooling

## Current authoritative build environment
Because SOC01 currently has `sigma` installed but cannot resolve the online plugin directory, the **automation controller** is the current authoritative Sigma build system.

- Python version: system Python 3.13 on controller
- Virtual environment path: `/root/.venvs/sigma-platform`
- sigma-cli version: `3.1.0`
- pySigma version: `1.4.0`
- Command used:
  ```bash
  source /root/.venvs/sigma-platform/bin/activate
  SIGMA_BIN=sigma python3 automation/validators/sigma_ops.py lint --json
  SIGMA_BIN=sigma python3 automation/validators/sigma_ops.py convert --target all --json
  ```

## SOC01 state
- `sigma --version` on SOC01: `3.1.0`
- `sigma plugin list` on SOC01: failed because `raw.githubusercontent.com` could not be resolved
- `sigma list targets` / `sigma list pipelines` on SOC01 before plugin install: no backends / no pipelines
- Conclusion: SOC01 is useful as an analyst node, but not yet the authoritative conversion host

## Installed plugins in controller venv
- `splunk`
- `elasticsearch`
- `windows`
- `sysmon`

## Supported targets verified
- Splunk: `splunk`, `splunk_spl2`
- Elastic: `lucene`, `eql`, `esql`, `elastalert`

## Supported pipelines verified
- `windows-logsources`
- `windows-audit`
- `sysmon`
- `splunk_windows`
- `splunk_sysmon_acceleration`
- `splunk_cim`
- `ecs_windows`
- `ecs_windows_old`

## Update procedure
```bash
sudo -n apt-get install -y python3-venv
python3 -m venv /root/.venvs/sigma-platform
source /root/.venvs/sigma-platform/bin/activate
python -m pip install --upgrade pip sigma-cli
sigma plugin install splunk elasticsearch windows sysmon
```

## Validation commands
```bash
source /root/.venvs/sigma-platform/bin/activate
cd /root/work/github-readme-audit/cybersecurity-playbook
SIGMA_BIN=sigma python3 automation/validators/sigma_ops.py lint --json
SIGMA_BIN=sigma python3 automation/validators/sigma_ops.py check
SIGMA_BIN=sigma python3 automation/validators/sigma_ops.py convert --target all --json
SIGMA_BIN=sigma python3 automation/validators/sigma_ops.py test-fixtures --json
```

## Generated outputs
- Official Splunk conversions: `detections/generated/splunk/official/`
- Mayuri live Splunk queries: `detections/generated/splunk/live/`
- Elastic EQL conversions: `detections/generated/elastic/`

## Known limitations
1. Official field-based Splunk conversion succeeds syntactically, but the live Splunk deployment does not yet expose equivalent extracted fields for direct use.
2. Current live Splunk validation therefore uses a Mayuri raw-XML wrapper query generator.
3. Elastic conversion is syntax-only right now; no live Elastic backend exists in the lab.
