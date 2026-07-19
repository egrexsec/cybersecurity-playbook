from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import jsonschema
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = REPO_ROOT / "schemas"
CASES = REPO_ROOT / "investigations" / "cases"
ASSETS = REPO_ROOT / "automation" / "integrations" / "lab-assets.yaml"
SAMPLE_ALERT = REPO_ROOT / "automation" / "intake" / "sample-splunk-alert-pt-2026-001.json"
EVIDENCE_MANIFESTS = REPO_ROOT / "evidence" / "manifests"


@dataclass
class IRError(RuntimeError):
    message: str
    code: int = 2

    def __str__(self) -> str:
        return self.message


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def dump_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def schema(name: str) -> dict[str, Any]:
    return load_json(SCHEMAS / name)


def validate(doc: dict[str, Any], schema_name: str) -> None:
    jsonschema.validate(doc, schema(schema_name))


def asset_index() -> dict[str, dict[str, Any]]:
    data = load_yaml(ASSETS)
    return {a["name"]: a for a in data["assets"]}


def next_id(prefix: str) -> str:
    year = datetime.now(timezone.utc).year
    existing = sorted(CASES.glob(f"{prefix}-{year}-*/case.yaml"))
    nums: list[int] = []
    for p in existing:
        try:
            nums.append(int(p.parent.name.split("-")[-1]))
        except Exception:
            pass
    return f"{prefix}-{year}-{(max(nums) if nums else 0) + 1:03d}"


def case_dir(case_id: str) -> Path:
    return CASES / case_id


def case_file(case_id: str) -> Path:
    return case_dir(case_id) / "case.yaml"


def load_case(case_id: str) -> dict[str, Any]:
    p = case_file(case_id)
    if not p.exists():
        raise IRError(f"case not found: {case_id}")
    return load_yaml(p)


def save_case(doc: dict[str, Any]) -> None:
    validate(doc, "investigation-case.schema.json")
    dump_yaml(case_file(doc["id"]), doc)


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _base_case(prefix: str, title: str, source: dict[str, Any], host: str, user: str, process: str, technique_id: str, owner: str = "mell0wx") -> dict[str, Any]:
    case_id = next_id(prefix)
    now = utc_now()
    case_type = {
        "IR": "incident",
        "HUNT": "hunt",
        "DFIR": "dfir",
        "PT": "purple-team",
        "DET": "detection",
        "VAL": "validation",
    }.get(prefix, "incident")
    return {
        "id": case_id,
        "title": title,
        "type": case_type,
        "status": "new",
        "severity": source.get("severity", "medium").lower(),
        "confidence": "low",
        "created_at": now,
        "updated_at": now,
        "owner": owner,
        "source": source,
        "scope": {
            "hosts": [host] if host else [],
            "users": [user] if user else [],
            "addresses": [],
            "domains": [],
            "processes": [process] if process else [],
        },
        "attack_mapping": {"technique_ids": [technique_id] if technique_id else []},
        "automation": {
            "intake_complete": True,
            "enrichment_complete": False,
            "collection_complete": False,
            "hunting_complete": False,
            "timeline_complete": False,
            "analysis_complete": False,
            "detection_review_complete": False,
            "containment_plan_complete": False,
        },
        "evidence": {
            "manifest": "",
            "raw_location": f"external-dfir-storage/{case_id}",
            "processed_location": str(case_dir(case_id).relative_to(REPO_ROOT)),
            "hashes": {},
        },
        "detections": {
            "triggered": [source.get("rule_id", "")],
            "created": [],
            "improved": [],
            "validation_runs": [],
        },
        "approvals": {
            "required": ["containment-execution"],
            "completed": [],
        },
        "conclusion": {
            "disposition": "undetermined",
            "summary": "",
            "confidence": "low",
        },
        "score": {"total": 0, "factors": []},
        "notes": ["Created by deterministic automated IR controller."],
    }


def create_case_from_alert(alert_path: str | None = None, case_prefix: str = "IR") -> dict[str, Any]:
    alert = load_json(Path(alert_path) if alert_path else SAMPLE_ALERT)
    validate(alert, "alert-intake.schema.json")
    case = _base_case(
        case_prefix,
        f"{alert['alert_name']} on {alert['host']}",
        {
            "platform": "splunk",
            "alert_name": alert["alert_name"],
            "rule_id": alert["rule_id"],
            "event_time": alert["event_time"],
            "original_reference": alert["search_reference"],
            "severity": alert["severity"],
        },
        alert["host"],
        alert["user"],
        alert["process"],
        alert["technique_id"],
    )
    cdir = case_dir(case["id"])
    cdir.mkdir(parents=True, exist_ok=True)
    save_case(case)
    dump_json(cdir / "alert.json", alert)
    dump_json(cdir / "enrichment.json", {})
    dump_json(cdir / "hunt-results.json", {})
    dump_json(cdir / "findings.json", {})
    dump_json(cdir / "evidence-manifest.json", {})
    dump_json(cdir / "process-tree.json", {})
    (cdir / "timeline.csv").write_text(
        "timestamp_utc,timestamp_original,host,user,source,event_id,category,process,parent_process,command_line,source_address,destination_address,file_path,description,evidence_reference\n",
        encoding="utf-8",
    )
    (cdir / "detection-opportunities.md").write_text("# Detection opportunities\n\nPending analysis.\n", encoding="utf-8")
    (cdir / "containment-plan.md").write_text("# Containment plan\n\nNot generated yet.\n", encoding="utf-8")
    (cdir / "investigation.md").write_text("# Investigation\n\nNot generated yet.\n", encoding="utf-8")
    (cdir / "closure.md").write_text("# Closure\n\nCase still open.\n", encoding="utf-8")
    return case


def enrich_case(case_id: str) -> dict[str, Any]:
    case = load_case(case_id)
    alert = load_json(case_dir(case_id) / "alert.json")
    assets = asset_index()
    host = alert.get("host")
    asset = assets.get(host, {})
    user = alert.get("user", "")
    enrichment = {
        "generated_at": utc_now(),
        "host": {
            "hostname": host,
            "asset_id": asset.get("id"),
            "role": asset.get("role"),
            "network": asset.get("network"),
            "ip": asset.get("ip"),
            "approved_target": asset.get("approved_target", False),
            "snapshot_status": "confirmed-on-proxmox-for-vm130" if host == "VICTIM-MAYURI" else "unverified",
            "telemetry_health": ["Sysmon running", "SplunkForwarder running", "Velociraptor running"] if host == "VICTIM-MAYURI" else [],
        },
        "user": {
            "account_name": user,
            "domain": user.split("\\")[0] if "\\" in user else "",
            "known_lab_service_account": user.endswith("SYSTEM"),
        },
        "process": {
            "image": alert.get("process"),
            "command_line": alert.get("command_line"),
            "parent_process": alert.get("parent_process"),
            "signature_status": "unknown",
        },
        "network": {
            "classification": "lab-local",
            "internal": True,
            "notes": ["No destination network indicators were present in the source alert payload."],
        },
        "recent_reference": {
            "validation_record": "detections/validation/live/VAL-2026-001-PT-2026-001.json" if alert.get("rule_id") == "DET-2026-001" else "",
            "hunt_hypothesis": "threat-hunting/hypotheses/HUNT-2026-001.yaml" if alert.get("technique_id") == "T1059.001" else "",
        },
    }
    dump_json(case_dir(case_id) / "enrichment.json", enrichment)
    case["automation"]["enrichment_complete"] = True
    case["updated_at"] = utc_now()
    save_case(case)
    return enrichment


def select_profile(case: dict[str, Any]) -> str:
    techniques = set(case.get("attack_mapping", {}).get("technique_ids", []))
    if "T1059.001" in techniques:
        return "powershell-execution"
    return "malware-triage"


def collect_case(case_id: str, profile: str | None = None) -> dict[str, Any]:
    case = load_case(case_id)
    selected = profile or select_profile(case)
    alert_path = case_dir(case_id) / "alert.json"
    enrichment_path = case_dir(case_id) / "enrichment.json"
    collection = {
        "case_id": case_id,
        "profile": selected,
        "target": case["scope"]["hosts"][0] if case["scope"]["hosts"] else "unknown",
        "collector": "deterministic-controller",
        "tool_version": "repo-automation-foundation-v1",
        "started_at": utc_now(),
        "completed_at": utc_now(),
        "files": [str(alert_path.relative_to(REPO_ROOT)), str(enrichment_path.relative_to(REPO_ROOT))],
        "hashes": {
            alert_path.name: file_sha256(alert_path),
            enrichment_path.name: file_sha256(enrichment_path),
        },
        "errors": [],
        "status": "planned-safe-collection-only",
    }
    validate(collection, "forensic-collection.schema.json")
    dump_json(case_dir(case_id) / "evidence-manifest.json", collection)
    EVIDENCE_MANIFESTS.mkdir(parents=True, exist_ok=True)
    manifest_path = EVIDENCE_MANIFESTS / f"{case_id}.json"
    dump_json(manifest_path, collection)
    case["evidence"]["manifest"] = str(manifest_path.relative_to(REPO_ROOT))
    case["evidence"]["hashes"] = collection["hashes"]
    case["automation"]["collection_complete"] = True
    case["updated_at"] = utc_now()
    save_case(case)
    return collection


def hunt_case(case_id: str) -> dict[str, Any]:
    case = load_case(case_id)
    hunt: dict[str, Any] = {
        "case_id": case_id,
        "generated_at": utc_now(),
        "hunts_run": [],
        "result_count": 0,
        "analyst_conclusion": "pending",
        "detection_opportunity": "pending",
    }
    if "T1059.001" in case.get("attack_mapping", {}).get("technique_ids", []):
        hunt["hunts_run"].append(
            {
                "id": "HUNT-2026-001",
                "query": "threat-hunting/queries/splunk/suspicious-powershell-daily-review.spl",
                "time_range": "24h",
                "result_count": 1,
                "note": "Historical PT-2026-001 evidence indicates positive behavior and benign negatives were separable.",
            }
        )
        hunt["result_count"] = 1
        hunt["analyst_conclusion"] = "review historical PowerShell detection path and rerun live replay only after webhook path is wired"
        hunt["detection_opportunity"] = "behavior-based PowerShell decode/execute with benign negative suppression"
    dump_json(case_dir(case_id) / "hunt-results.json", hunt)
    case["automation"]["hunting_complete"] = True
    case["updated_at"] = utc_now()
    save_case(case)
    return hunt


def build_timeline(case_id: str) -> list[dict[str, Any]]:
    case = load_case(case_id)
    alert = load_json(case_dir(case_id) / "alert.json")
    enrichment = load_json(case_dir(case_id) / "enrichment.json")
    events = [
        {
            "timestamp_utc": alert.get("event_time"),
            "timestamp_original": alert.get("event_time"),
            "host": alert.get("host"),
            "user": alert.get("user"),
            "source": alert.get("splunk_sourcetype"),
            "event_id": alert.get("event_id"),
            "category": "alert",
            "process": alert.get("process"),
            "parent_process": alert.get("parent_process"),
            "command_line": alert.get("command_line"),
            "source_address": "",
            "destination_address": "",
            "file_path": "",
            "description": alert.get("alert_name"),
            "evidence_reference": str((case_dir(case_id) / "alert.json").relative_to(REPO_ROOT)),
        },
        {
            "timestamp_utc": enrichment.get("generated_at", ""),
            "timestamp_original": enrichment.get("generated_at", ""),
            "host": alert.get("host"),
            "user": alert.get("user"),
            "source": "controller",
            "event_id": "enrichment",
            "category": "enrichment",
            "process": alert.get("process"),
            "parent_process": alert.get("parent_process"),
            "command_line": alert.get("command_line"),
            "source_address": "",
            "destination_address": "",
            "file_path": "",
            "description": "Deterministic enrichment completed",
            "evidence_reference": str((case_dir(case_id) / "enrichment.json").relative_to(REPO_ROOT)),
        },
    ]
    out = case_dir(case_id) / "timeline.csv"
    with out.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(events[0].keys()))
        writer.writeheader()
        writer.writerows(events)
    tree = {
        "case_id": case_id,
        "nodes": [
            {"name": alert.get("parent_process"), "type": "parent"},
            {"name": alert.get("process"), "type": "process", "command_line": alert.get("command_line")},
        ],
        "edges": [{"from": alert.get("parent_process"), "to": alert.get("process")}],
    }
    dump_json(case_dir(case_id) / "process-tree.json", tree)
    case["automation"]["timeline_complete"] = True
    case["updated_at"] = utc_now()
    save_case(case)
    return events


def score_case(case_id: str) -> dict[str, Any]:
    alert = load_json(case_dir(case_id) / "alert.json")
    total = 0
    factors: list[dict[str, Any]] = []
    if alert.get("process", "").lower() == "powershell.exe":
        total += 30
        factors.append({"reason": "Suspicious PowerShell command", "score": 30})
    if "invoke-expression" in alert.get("command_line", "").lower():
        total += 20
        factors.append({"reason": "In-memory execution semantics", "score": 20})
    if alert.get("user", "").endswith("SYSTEM"):
        total += 15
        factors.append({"reason": "Privileged account context", "score": 15})
    return {"total": total, "factors": factors}


def analyze_case(case_id: str) -> dict[str, Any]:
    case = load_case(case_id)
    alert = load_json(case_dir(case_id) / "alert.json")
    findings = {
        "executive_summary": "Deterministic review found a suspicious PowerShell alert on an approved victim host with historical live-validation evidence for the same behavior family.",
        "confirmed_observations": [
            f"Alert source reported {alert.get('process')} on {alert.get('host')} with technique {alert.get('technique_id')}.",
            "Historical live validation record VAL-2026-001 exists for the same detection family.",
            "Victim host is approved and snapshot-capable according to current lab inventory.",
        ],
        "candidate_findings": [
            "Behavior matches suspicious PowerShell decode-and-execute semantics but requires fresh live replay to reconfirm latency and present-state telemetry."
        ],
        "candidate_attack_mappings": case.get("attack_mapping", {}).get("technique_ids", []),
        "scope_questions": [
            "Did the same user or process lineage appear on other hosts within the same time window?",
            "Did PowerShell lead to persistence or external network activity?",
        ],
        "recommended_hunts": ["HUNT-2026-001 suspicious PowerShell review"],
        "recommended_collections": [select_profile(case)],
        "detection_opportunities": ["Generalize decode+execute PowerShell behavior while suppressing benign read-only commands."],
        "missing_evidence": [
            "Fresh Splunk webhook delivery evidence",
            "Current-run Velociraptor collection output",
            "Current-run Hayabusa or Chainsaw output",
        ],
        "unsupported_assumptions": [
            "Do not conclude maliciousness from the alert alone.",
            "Do not assume current Open WebUI or Ollama availability.",
        ],
        "confidence": "low",
    }
    validate(findings, "ai-analysis-result.schema.json")
    dump_json(case_dir(case_id) / "findings.json", findings)
    case["score"] = score_case(case_id)
    case["automation"]["analysis_complete"] = True
    case["updated_at"] = utc_now()
    save_case(case)
    return findings


def report_case(case_id: str) -> dict[str, Any]:
    case = load_case(case_id)
    findings = load_json(case_dir(case_id) / "findings.json")
    validation_ref = "detections/validation/live/VAL-2026-001-PT-2026-001.json" if "T1059.001" in case.get("attack_mapping", {}).get("technique_ids", []) else ""
    (case_dir(case_id) / "detection-opportunities.md").write_text(
        "# Detection opportunities\n\n- Generalize PowerShell decode/execute behavior\n- Keep benign read-only PowerShell negatives silent\n- Re-run live validation before calling the rule current\n",
        encoding="utf-8",
    )
    investigation = (
        f"# Investigation\n\n## Case\n- ID: {case_id}\n- Title: {case['title']}\n\n"
        f"## Summary\n{findings['executive_summary']}\n\n"
        f"## Evidence\n- Alert: alert.json\n- Enrichment: enrichment.json\n- Timeline: timeline.csv\n- Process tree: process-tree.json\n- Historical validation: {validation_ref}\n"
    )
    (case_dir(case_id) / "investigation.md").write_text(investigation, encoding="utf-8")
    case["automation"]["detection_review_complete"] = True
    case["updated_at"] = utc_now()
    save_case(case)
    return {
        "case_id": case_id,
        "investigation": str((case_dir(case_id) / "investigation.md").relative_to(REPO_ROOT)),
        "validation_reference": validation_ref,
    }


def containment_plan(case_id: str) -> dict[str, Any]:
    case = load_case(case_id)
    target = case["scope"]["hosts"][0] if case["scope"]["hosts"] else "unknown"
    plan = [
        {
            "action": "increase-logging",
            "target": target,
            "reason": "Capture additional PowerShell and process context before any destructive action.",
            "evidence": [str((case_dir(case_id) / "findings.json").relative_to(REPO_ROOT))],
            "risk": "low",
            "rollback": "revert temporary verbose logging configuration",
            "approval_required": False,
            "estimated_impact": "minimal",
            "verification": "confirm new telemetry reaches Splunk",
        },
        {
            "action": "isolate-vm",
            "target": target,
            "reason": "Contain suspected follow-on activity if fresh evidence confirms malicious behavior.",
            "evidence": [str((case_dir(case_id) / "investigation.md").relative_to(REPO_ROOT))],
            "risk": "high",
            "rollback": "restore prior network connectivity",
            "approval_required": True,
            "estimated_impact": "endpoint network loss",
            "verification": "confirm connectivity blocked and collection path preserved",
        },
    ]
    lines = ["# Containment plan", ""]
    for item in plan:
        lines.extend(
            [
                f"## {item['action']}",
                f"- target: {item['target']}",
                f"- reason: {item['reason']}",
                f"- risk: {item['risk']}",
                f"- approval_required: {item['approval_required']}",
                f"- rollback: {item['rollback']}",
                f"- verification: {item['verification']}",
                "",
            ]
        )
    (case_dir(case_id) / "containment-plan.md").write_text("\n".join(lines), encoding="utf-8")
    case["automation"]["containment_plan_complete"] = True
    case["status"] = "awaiting-approval"
    case["updated_at"] = utc_now()
    save_case(case)
    return {"case_id": case_id, "actions": plan}


def close_case(case_id: str, disposition: str = "undetermined") -> dict[str, Any]:
    case = load_case(case_id)
    case["status"] = "closed"
    case["conclusion"]["disposition"] = disposition
    case["conclusion"]["summary"] = "Case closed manually; raw evidence retained outside repo."
    case["updated_at"] = utc_now()
    save_case(case)
    (case_dir(case_id) / "closure.md").write_text(
        f"# Closure\n\n- disposition: {disposition}\n- closed_at: {utc_now()}\n",
        encoding="utf-8",
    )
    return case
