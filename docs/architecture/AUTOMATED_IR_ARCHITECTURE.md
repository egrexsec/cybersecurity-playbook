# Automated IR Architecture

## Purpose
Build a **safe, case-driven automation platform** around the existing Mayuri cyber lab and `cybersecurity-playbook` repository without replacing proven components.

## Component responsibilities

| Component | Responsibility |
|---|---|
| Splunk | primary alerting, investigation searches, live validation evidence, historical pivots |
| Wazuh | supplemental endpoint alerts and alternate hunt pivots |
| Sysmon | detailed endpoint process/file/network telemetry |
| Velociraptor | targeted triage and forensic collection |
| Hayabusa | EVTX timeline generation when installed |
| Chainsaw | offline Sigma matching against EVTX when installed |
| sigma-cli / repo validators | rule linting, conversion, fixture tests, validation support |
| n8n | orchestration, intake, scheduling, analyst notifications, approval routing |
| Ollama / Open WebUI | candidate findings, summary drafting, missing-evidence prompts only |
| GitHub | workflow-as-code, hunts, detections, issues, PRs, validation evidence |
| OPNsense | future approval-based containment and network-state enrichment |
| Proxmox | VM inventory, snapshots, guest-exec, lifecycle safety checks |
| SOC VM | Splunk and future automation-side SIEM integrations |
| DFIR VM | Velociraptor and offline evidence processing |
| Victim VM | approved Windows alert/IR/purple-team target |

## High-level flow

```text
Splunk alert / hunt result / PT scenario
        ↓
Structured intake payload
        ↓
Case creation + deduplication
        ↓
Deterministic enrichment
        ↓
Forensic profile selection
        ↓
Evidence manifest + collection request
        ↓
Automated hunt execution
        ↓
Timeline + process-tree generation
        ↓
Optional EVTX / Velociraptor / local-AI analysis
        ↓
Detection opportunity review
        ↓
Fixture + live validation workflow
        ↓
Report, issue, PR, containment plan
```

## Trust boundaries

### Trusted control planes
- Proxmox host `mayuri`
- GitHub repository and CI
- homelab n8n instance behind Authentik
- DFIR-hosted Velociraptor server

### Semi-trusted data sources
- Splunk event results
- Wazuh alerts
- PowerShell / Sysmon / Security logs
- Velociraptor collected metadata

### Restricted components
- Ollama/Open WebUI analysis output
- generated containment actions
- any destructive response action

AI output is **advisory only** and cannot directly mutate targets, close investigations, or deploy detections.

## Approval boundaries

### Auto-permitted
- read-only enrichment
- case creation/update
- evidence manifest generation
- hashing
- timeline generation
- hunt execution
- sanitized GitHub issue / draft PR generation
- safe notifications

### Approval required
- account disablement
- firewall or network isolation
- process termination
- service stop/removal
- persistence deletion
- snapshot revert
- production detection deployment
- case closure with malicious/benign disposition

## Network and API dependencies

| Flow | Direction | Current state |
|---|---|---|
| Splunk alert -> n8n webhook | SOC/homelab -> n8n | design ready; live webhook config pending |
| n8n -> repo controller | n8n -> local/VPS runner | supported via HTTP/CLI wrapper design |
| Controller -> GitHub | VPS -> GitHub | confirmed |
| Controller -> Proxmox guest exec | VPS -> Proxmox | confirmed |
| Controller -> Velociraptor API | VPS/DFIR | not yet wired |
| Controller -> Ollama/Open WebUI | VPS -> local AI | endpoint unconfirmed |
| Future containment -> OPNsense API | controller -> firewall | blocked until OPNsense returns |

## Credentials required
- GitHub token / `gh` auth
- Splunk API auth or service credential
- n8n webhook secret / credential mapping
- Velociraptor API client config
- optional local-AI API token/endpoint
- future OPNsense API key/secret

## Data handling model
- raw evidence remains outside the public repo
- processed and sanitized evidence may be committed
- every collected artifact gets SHA-256 tracking
- UTC is the internal time base
- case records link to raw and processed evidence locations, not inline raw data
