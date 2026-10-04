# CYBER LAB ASSESSMENT

> Historical snapshot: this document captures the initial Mayuri assessment at the start of the purple-team buildout. For the current repository-facing state, use `DETECTION_PLATFORM_READINESS.md`, `PROJECT_TIMELINE_ASSESSMENT.md`, and `PURPLE_TEAM_PROGRAM_STATUS.md`.

- **Assessment timestamp (UTC):** 2026-07-18T01:18:00Z
- **Operator:** Hermes Agent
- **Repository:** `egrexsec/cybersecurity-playbook`
- **Branch during assessment start:** `main`
- **Implementation branch:** `feat/mayuri-pt-2026-001-foundation`

## Executive Summary

The Mayuri lab is far enough along to support a **safe first purple-team / detection-engineering scenario on the Windows victim** using the current stack of **Wazuh + Sysmon + Windows audit logging + PowerShell logging + Velociraptor**.

The environment is **not yet ready for unattended continuous automation** across the full requested lifecycle. The main blockers are:

1. the repository is still a small markdown knowledge base, not an automation repo
2. there are **no schemas, workflows, issue templates, or execution controller** yet
3. the current DFIR-to-enterprise Velociraptor path depends on a **temporary dual-homed DFIR workaround**
4. the OPNsense VM is currently reported as **stopped** from Proxmox, so firewall/logging state is not presently validated from the live appliance
5. PowerShell transcription is **not enabled** on the victim
6. no in-repo validation harness or detection test scope exists yet
7. `n8n`, `Ollama`, and `Open WebUI` are **not confirmed inside the accessible lab scope**

Despite those gaps, the lab does support a controlled **PT-2026-001 / T1059.001** milestone on VM `130` if execution remains narrowly scoped and reversible.

---

## Confirmed Systems

### Proxmox host
- **Hostname:** `mayuri`
- **FQDN:** _redacted from public repo; internal lab FQDN confirmed during assessment_
- **Platform:** `Proxmox VE 9.2.4`
- **Time sync:** host clock synchronized, NTP active
- **Storage:**
  - `local` ~24 GiB available
  - `local-lvm` ~131 GiB available

### VM inventory from Proxmox
| VMID | Name | Status | Notes |
|---|---|---:|---|
| 100 | daily | stopped | explicitly out of scope as attack target |
| 110 | firewall | stopped | critical architecture concern; live firewall/logging state not currently validated |
| 120 | DC01-enterprise | running | AD / DNS / Wazuh / Sysmon / Velociraptor client confirmed |
| 130 | victim | running | domain joined, Sysmon + Wazuh + PowerShell logging + Velociraptor client confirmed |
| 140 | soc | running | Wazuh + Suricata + sigma-cli confirmed |
| 150 | kali | stopped | available for future approved attacker-side scenarios |
| 160 | dfir | running | Velociraptor server confirmed; dual-homed ingress workaround active |

### Active Directory and identity plane
- **Domain:** `mayuri.lab`
- **Domain controller:** `DC01`
- Victim remains domain joined and secure channel check returns `True`
- DC time source is `10.10.10.1`
- Victim time source is `DC01.mayuri.lab`
- `repadmin /replsummary` completed without replication failures in current single-DC layout
- `dcdiag /q` returned no visible failures in the current read-only check

### Victim (VM 130)
- **Hostname:** `VICTIM-MAYURI`
- **Primary IP:** `10.10.10.101`
- **Domain:** `mayuri.lab`
- **Secure channel:** `True`
- **Time sync:** healthy against `DC01`
- **Sysmon:** running
- **Wazuh agent:** running
- **PowerShell Operational log:** enabled and receiving new events (`4103`, `4104` observed)
- **Process command-line auditing:** enabled (`ProcessCreationIncludeCmdLine_Enabled = 1`)
- **PowerShell script block logging:** enabled
- **PowerShell module logging:** enabled with wildcard module names
- **WMI-Activity / TaskScheduler / Defender operational logs:** present and writable
- **PowerShell transcription:** **missing / not enabled**

### Domain controller (VM 120)
- **Hostname:** `DC01`
- **Primary IP:** `10.10.10.10`
- **Time sync:** healthy
- **Sysmon:** running
- **Wazuh agent:** running
- Recent Wazuh ingestion confirms DC Security events (`4624`, `4634`, `4688`) are reaching SOC

### SOC (VM 140)
- **Hostname:** `soc-mayuri`
- **Primary IP:** `10.10.10.20`
- **Time sync:** healthy
- **Confirmed active services:**
  - `wazuh-manager`
  - `wazuh-indexer`
  - `wazuh-dashboard`
  - `filebeat`
  - `suricata`
- **Confirmed listening services:**
  - `1514/tcp` Wazuh remoted
  - `1515/tcp` Wazuh authd
  - `55000/tcp` Wazuh API
  - `9200/tcp` loopback indexer
- **sigma-cli:** installed (`3.1.0`)
- **Local custom Wazuh rules path exists:** `/var/ossec/etc/rules/local_rules.xml`
- **Local custom Wazuh decoder path exists:** `/var/ossec/etc/decoders/local_decoder.xml`
- Wazuh recent alerts confirm ingestion from both `DC01` and `VICTIM-MAYURI`

### DFIR (VM 160)
- **Hostname:** `mayuri-dfir`
- **IPs:**
  - `10.30.30.10` on `ens18`
  - `10.10.10.30` on `ens19`
- **Time sync:** healthy
- **Velociraptor server:** active
- **Confirmed listeners:**
  - `*:8000` client frontend
  - `127.0.0.1:8001` API
  - `127.0.0.1:8889` GUI
- **Confirmed enrolled clients:**
  - `VICTIM-MAYURI`
  - `DC01`

### GitHub / repository state
- Repo path in current environment:
  - _local working clone; host-specific path intentionally omitted from public repo_
- Remote:
  - `https://github.com/egrexsec/cybersecurity-playbook.git`
- GitHub access during implementation:
  - authenticated maintainer access confirmed locally
- Current repo characteristics:
  - markdown-first content repository
  - no CI workflows
  - no issue templates / PR template
  - no schemas
  - no controller
  - no automation layout matching the requested operating model

---

## Missing Systems / Unconfirmed Components

These were requested or mentioned in the design brief but are **not confirmed as available in the currently accessible lab scope**:

- `n8n` inside the accessible lab VMs
- `Ollama` inside the accessible lab VMs
- `Open WebUI` inside the accessible lab VMs
- Splunk in the current Mayuri lab scope
- Elastic in the current Mayuri lab scope
- Zeek in the current Mayuri lab scope
- live OPNsense firewall logging from the running appliance
- public GitHub Actions workflows for this repository
- existing repo-side detection validation harness

Where these may exist elsewhere in the broader environment, they were **not assumed operational for this implementation**.

---

## Partially Configured Systems

### DFIR / Velociraptor routing
Velociraptor is operational, but current enterprise access relies on a **temporary dual-homed design**:
- DFIR is reachable on `10.10.10.30:8000`
- access is restricted with guest-local `iptables`
- this is safe enough for the current milestone, but it is **not the final target architecture**

### Wazuh custom-rule pipeline
- custom rules and decoder files exist
- `wazuh-logtest` is present
- however, there is **no current repo-backed detection-as-code pipeline** tying Sigma → Wazuh → validation records → PR workflow

### Repository content model
The repo already contains useful content:
- markdown templates
- MDE hunting examples
- AWS FLAWS2 examples
- Velociraptor notes

But it does **not** yet support:
- execution manifests
- forensic evidence manifests
- validation records
- automation controller runs
- scenario-specific artifacts
- GitHub validation workflows

---

## Telemetry Gaps

### Endpoint telemetry gaps on victim
1. **PowerShell transcription not enabled**
2. No confirmed in-repo baseline for:
   - Task Scheduler operational hunt queries
   - WMI operational hunt queries
   - Defender operational query pack
3. No repo-managed ATT&CK-to-data-source map yet
4. No normalized fixture set for positive/negative PowerShell detections yet

### Identity telemetry gaps
1. DC telemetry is present, but current milestone should remain **victim-focused** to avoid unnecessary AD risk
2. No dedicated identity-hunt automation manifests exist yet
3. No domain-controller-specific approval gating is implemented in code yet

### Network telemetry gaps
1. OPNsense VM status is currently reported as **stopped** from Proxmox
2. therefore live firewall / DNS / DHCP / inter-zone log validation is incomplete
3. no Zeek deployment confirmed
4. no repo-managed network-evidence collection flow yet

### Platform / process gaps
1. no stable run manifest format in-repo yet
2. no schema validation workflows yet
3. no structured evidence hashing workflow yet
4. no PR templates for scenarios / hunts / detections / investigations
5. no AI task guardrail schema or pipeline in repo yet

---

## Security Risks and Architectural Concerns

1. **Firewall VM reported stopped**
   - This is the largest unresolved infrastructure concern because it blocks confidence in live network-policy assumptions and firewall-log collection.

2. **Dual-homed DFIR workaround**
   - Currently acceptable for controlled validation, but it increases architectural complexity and should be replaced by a narrowly scoped firewall rule later.

3. **Duplicate LVM VG warning on Proxmox (`ubuntu-vg`)**
   - Continues to present operational risk during offline guest work and snapshots.

4. **Thin-pool overcommit warnings**
   - Snapshot-heavy workflows can amplify storage risk.

5. **No transcription on victim**
   - Reduces completeness of PowerShell forensic reconstruction.

6. **No current CI / secret-scanning / evidence-path controls in repo**
   - Increases risk of unsafe commits once raw evidence starts accumulating.

7. **Kali and firewall are stopped**
   - Not a blocker for the first victim-only PowerShell scenario, but a blocker for broader purple-team automation.

---

## Automation Opportunities

1. Add a deterministic `playbook` controller for:
   - inventory
   - preflight
   - scenario validation
   - scenario planning
   - reporting

2. Standardize schemas for:
   - scenario manifests
   - hunts
   - investigations
   - evidence manifests
   - detection validation records
   - run records

3. Build a first safe path around **PT-2026-001 / T1059.001** using:
   - victim
   - SOC / Wazuh
   - DFIR / Velociraptor
   - GitHub feature-branch workflow

4. Use Wazuh as the first active SIEM target for detection validation because it is the only currently confirmed platform with live ingest and writable custom-rule support.

5. Use Velociraptor selectively for post-execution collection instead of full broad-scope forensic acquisition.

---

## Blocking Issues

### Critical blockers for fully unattended continuous automation
- missing repo automation/controller foundation
- missing schema/validation workflows
- OPNsense live state not currently validated
- no CI guardrails
- no stable detection deployment/test workflow

### Non-blocking for the first victim-only PowerShell milestone
- Kali stopped
- n8n unconfirmed in lab scope
- Ollama/Open WebUI unconfirmed in lab scope
- Splunk/Elastic absent or unconfirmed

---

## Recommended Implementation Order

1. **Restructure the repository safely** without destroying current markdown content.
2. **Add schemas** for scenarios, hunts, investigations, evidence, validation, campaigns, and lab assets.
3. **Add a minimal controller** that can perform inventory, scenario validation, and preflight checks.
4. **Document current data sources** for Windows process creation and PowerShell telemetry.
5. **Define and approve PT-2026-001** as a low-risk victim-only T1059.001 scenario.
6. **Collect baseline telemetry** from victim and SOC.
7. **Execute one approved Atomic Red Team PowerShell test** with explicit cleanup.
8. **Collect evidence** via Wazuh + endpoint logs + Velociraptor.
9. **Build one portable Sigma detection** plus one **Wazuh test-scope rule**.
10. **Replay positive + modified + negative tests** and capture validation results.
11. **Commit on feature branch** and open a reviewable PR.
12. After that succeeds, move to **scheduled task persistence** only after the first scenario is reproducible.

---

## Assessment Conclusion

The current lab is **ready for one controlled end-to-end T1059.001 milestone on the Windows victim**.

It is **not yet ready for broad autonomous purple-team orchestration across the full lab**, especially anything that depends on live OPNsense validation, internet-dependent atomics, unattended lateral movement, or domain-controller attack workflows.

The correct next step is to implement the minimum foundation inside this repository, then complete and validate **PT-2026-001** before expanding to additional scenarios.
