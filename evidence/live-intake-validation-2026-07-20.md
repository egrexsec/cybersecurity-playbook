# Live Splunk → n8n → IR validation — 2026-07-20

## Result
**Fully validated end to end.**

A live PT-2026-001 PowerShell replay on the approved Windows victim generated PowerShell 4104 telemetry, triggered the scheduled Splunk detection, crossed a source-restricted Mayuri relay, entered the live homelab n8n workflow, and created a complete deterministic IR case on the VPS.

## Validated path

```text
VICTIM-MAYURI
  → Splunk Universal Forwarder
  → SOC Splunk saved search DET-2026-001-live-webhook
  → Mayuri relay 10.10.10.250:8766
  → n8n production webhook /webhook/splunk-alert-to-case
  → VPS receiver 100.90.16.73:8765
  → playbook IR controller
  → investigations/cases/IR-2026-006
```

## Live components

### Splunk SOC
- saved search: `DET-2026-001-live-webhook`
- schedule: every minute
- lookback: five minutes
- alert action: `webhook`
- duplicate suppression: `rule_id,host` for ten minutes
- relay URL contains a random path token; the token is not committed

### Mayuri relay
- host address: `10.10.10.250/24` on `vmbr10`
- listener: `10.10.10.250:8766`
- permitted source: `10.10.10.20` only
- upstream: live n8n HTTPS webhook
- service: `splunk-n8n-relay.service`
- address and service persist across reboot

### n8n
- live workflow: `Splunk Alert to Case`
- production path: `/webhook/splunk-alert-to-case`
- normalizes Splunk's webhook payload to the repository intake schema
- forwards to the VPS receiver with the shared receiver token
- Traefik bypass is limited to the exact webhook path; the editor remains behind Authentik

### VPS receiver
- listener: `100.90.16.73:8765` on Tailscale only
- service: `cybersecurity-playbook-ir-receiver.service`
- validates `X-IR-Token`
- runs the deterministic IR pipeline through containment planning
- does not execute containment

## Definitive replay evidence

### Victim execution
- PT scenario: `PT-2026-001`
- event time: `2026-07-20T16:17:34.2643622Z`
- victim: `VICTIM-MAYURI`
- telemetry: PowerShell Operational event 4104
- script block contained:
  - `FromBase64String`
  - `Invoke-Expression`
  - a benign marker write under `C:\Windows\Temp`

### Splunk scheduler
At `2026-07-20T16:22:02Z`, `scheduler.log` recorded:
- `result_count=1`
- `alert_actions="webhook"`
- `fired=1`
- `suppressed=0`

Subsequent matching runs recorded `suppressed=1`, confirming duplicate suppression worked.

### Relay
Mayuri journal recorded a POST from the SOC source:
- source: `10.10.10.20`
- response: HTTP `200`

### Created case
- case: `IR-2026-006`
- title: `Suspicious PowerShell Execution on VICTIM-MAYURI`
- severity: `high`
- rule: `DET-2026-001`
- ATT&CK: `T1059.001`
- state: `awaiting-approval`
- score: `50`
- original Splunk SID and results link preserved
- full 4104 XML/script block preserved in `alert.json`
- controller completed intake, enrichment, collection, hunting, timeline, analysis, detection review, and containment planning

## Security controls
- n8n editor/UI remains protected by Authentik
- unauthenticated n8n exposure is limited to one exact webhook path
- Mayuri relay binds only to the isolated enterprise bridge
- relay accepts only the SOC IP and a random path token
- relay enforces JSON object payloads and a 1 MiB maximum body
- VPS receiver binds only to its Tailscale address and requires a token header
- secrets live in root-readable environment files and are excluded from repository templates
- no containment action is executed automatically

## Repository artifacts
- `automation/n8n/splunk-alert-to-case.json`
- `automation/orchestrator/ir_receiver.py`
- `automation/relays/splunk_n8n_relay.py`
- `automation/systemd/splunk-n8n-relay.service`
- `automation/systemd/splunk-n8n-relay.env.example`
- `automation/systemd/cybersecurity-playbook-ir-receiver.service`
- `automation/systemd/cybersecurity-playbook-ir-receiver.env.example`
- `investigations/cases/IR-2026-006/`
- `evidence/manifests/IR-2026-006.json`

## Status
- implementation: **complete**
- manual relay validation: **passed**
- live n8n validation: **passed**
- fresh PT replay: **passed**
- automatic Splunk-originated case creation: **passed**
- duplicate suppression: **passed**
