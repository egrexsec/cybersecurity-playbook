# Automated IR Platform Assessment

- **Assessment timestamp (UTC):** 2026-07-19T20:05:00Z
- **Operator:** Hermes Agent
- **Repository:** `egrexsec/cybersecurity-playbook`
- **Branch during assessment:** `feat/automated-ir-powershell-foundation`
- **Scope rule:** read-only discovery first; no destructive response automation enabled

## Executive summary

The Mayuri environment is now strong enough to support a **case-driven suspicious-PowerShell alert-to-investigation workflow** built on the existing purple-team and detection-engineering repository.

The strongest confirmed building blocks are:
- Proxmox host access and VM inventory
- approved victim snapshots
- Splunk on the SOC VM with active listeners on `8000`, `8089`, and `9997`
- live victim and DC forwarders, Sysmon, and Velociraptor agents
- Velociraptor server listeners on DFIR (`8000`, `8001`, `8889`)
- existing PT-2026-001 PowerShell live-validation evidence in the repo
- authenticated GitHub repo access
- authenticated and healthy homelab `n8n` behind Authentik

The biggest confirmed gaps for the requested end-state are:
- no current repo-native automated IR/case-management controller
- no current Splunk alert webhook payload contract in-repo
- no current immutable evidence-handling runbook in-repo
- Hayabusa not present on DFIR
- Chainsaw not confirmed on DFIR during this assessment
- Open WebUI endpoint not confirmed from the assessed FQDN
- no verified local Ollama API endpoint from this execution environment
- no approval-token execution path yet for destructive containment actions

## Component status matrix

| Component | Status | Evidence | Notes |
|---|---|---|---|
| Proxmox host `mayuri` | Ready | `pve-manager/9.2.4`, NTP synced, `qm list` works over SSH with sudo | management-only, never a target |
| VM inventory | Ready | `qm list` shows 100/110/120/130/140/150/160 | matches documented lab roles |
| Victim VM 130 | Ready | `qm status 130: running`, guest exec works, domain joined, Sysmon/SplunkForwarder/Velociraptor running | primary approved target |
| SOC VM 140 | Ready | `qm status 140: running`, Splunk listeners on `8000/8089/9997`, `splunkd` running | main live detection node |
| DFIR VM 160 | Partially ready | `qm status 160: running`, Velociraptor listeners on `8000/8001/8889`, binary present | workflow-ready but offline EVTX tooling incomplete |
| DC01 VM 120 | Partially ready | domain joined, Sysmon/SplunkForwarder/Velociraptor running, Security events visible | keep usage low-risk |
| Kali VM 150 | Deferred | `qm status 150: stopped` | not required for first workflow |
| OPNsense VM 110 | Blocked | `qm status 110: stopped` | containment integration cannot be validated live |
| Snapshots on victim | Ready | snapshot chain ends at `current`; pre-atomic/pre-splunk lineage confirmed | sufficient for guarded replay |
| Snapshots on SOC | Ready | snapshot chain ends at `current` | useful for SIEM-side rollback |
| Splunk ingestion path | Ready | listeners active, prior live validation records present, forwarders active on victim/DC | saved alerts not yet inventory-backed here |
| Splunk webhook intake | Missing | no in-repo webhook contract or workflow found | implemented in this branch as repo scaffolding only |
| Sysmon on victim | Ready | guest query: `Sysmon64` status `4` | process telemetry source confirmed |
| PowerShell logging on victim | Ready | recent PowerShell Operational events, `ProcessCreationIncludeCmdLine_Enabled=1` | transcription still unverified here |
| Wazuh in current IR workflow | Partially ready | prior docs confirm Wazuh; current workflow still Splunk-first | supplemental only in this milestone |
| Velociraptor server | Ready | ports `8000/8001/8889` reachable on DFIR guest | collection integration can be staged |
| Hayabusa | Missing | DFIR probe returned `HAYABUSA_MISSING` | prevents full DFIR EVTX automation validation |
| Chainsaw | Unconfirmed | no path returned during DFIR probe | treat as missing until validated |
| sigma-cli / repo conversions | Ready | existing `sigma_ops.py`, generated SPL/EQL, fixture tests in repo | mature enough for detection workflow |
| Existing case schema | Partially ready | minimal `investigation-case.schema.json` existed | expanded in this branch |
| Existing automation controller | Partially ready | `playbook` supports validation/reporting/sigma/test | expanded in this branch for IR/case workflows |
| Existing PowerShell scenario | Ready | `PT-2026-001`, `HUNT-2026-001`, `VAL-2026-001-PT-2026-001.json` | used as first end-to-end case model |
| GitHub auth and repo access | Ready | `gh auth status` success | feature-branch + PR workflow supported |
| Homelab n8n runtime | Ready | container up, `n8n --version` = `2.29.7`, `/healthz` returns `{"status":"ok"}` | ingress protected by Authentik |
| n8n external ingress | Ready | `https://n8n.lab.mell0wx.tech/` returns Authentik `302` | healthy protected entrypoint |
| Open WebUI FQDN | Misconfigured or unconfirmed | `https://openwebui.lab.mell0wx.tech/` returned `404` | repo integration must tolerate model unavailability |
| Ollama endpoint | Unconfirmed | not directly reachable/validated from this environment | local-AI wrapper must degrade safely |

## Evidence excerpts

### Proxmox
- `qm list` showed `120`, `130`, `140`, `160` running; `110`, `150` stopped.
- `qm listsnapshot 130` and `qm listsnapshot 140` returned valid snapshot chains ending at `current`.
- `timedatectl show -p NTPSynchronized --value` returned `yes`.

### Victim and DC guest-state checks
- Victim guest query returned:
  - `Name=VICTIM-MAYURI`
  - `Domain=mayuri.lab`
  - `PartOfDomain=true`
  - services `SplunkForwarder`, `Sysmon64`, `Velociraptor` all status `4`
  - `ProcessCreationIncludeCmdLine_Enabled=1`
  - recent `Microsoft-Windows-PowerShell/Operational` events present
- DC guest query returned:
  - `Name=DC01`
  - `Domain=mayuri.lab`
  - services `SplunkForwarder`, `Sysmon64`, `Velociraptor` all status `4`
  - recent Security log events `4673`, `4688`

### Splunk and DFIR
- SOC guest query showed listeners on:
  - `0.0.0.0:8000`
  - `0.0.0.0:8089`
  - `0.0.0.0:9997`
- `/opt/splunk/bin/splunk status` reported `splunkd is running`.
- DFIR guest query confirmed:
  - `*:8000`
  - `127.0.0.1:8001`
  - `127.0.0.1:8889`
  - `velociraptor` binary present
  - `hayabusa` missing

## Readiness decision

### Ready now
- repository-side case management foundation
- deterministic alert intake and case generation from structured JSON
- evidence manifest generation and hashing for repo-side artifacts
- suspicious-PowerShell investigation flow using current PT-2026-001 evidence model
- GitHub issue/PR-safe output generation
- n8n workflow export authoring
- approval-gated containment plan generation

### Partially ready now
- live Splunk alert intake end-to-end (controller side yes; webhook/config side still manual)
- Velociraptor collection orchestration (manifest/profile side yes; authenticated API execution still manual)
- local AI-assisted analysis (schema/wrapper side yes; endpoint still unconfirmed)
- offline EVTX enrichment (workflow docs and placeholders yes; Hayabusa/Chainsaw validation incomplete)

### Not ready / blocked
- destructive containment execution
- OPNsense-backed isolation or firewall changes
- automated account disablement
- production detection deployment
- validated scheduled-hunt production rollout
