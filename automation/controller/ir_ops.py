from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import jsonschema
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = REPO_ROOT / "schemas"
CASES = REPO_ROOT / "investigations" / "cases"
ASSETS = REPO_ROOT / "automation" / "integrations" / "lab-assets.yaml"
SAMPLE_ALERT = REPO_ROOT / "automation" / "intake" / "sample-splunk-alert-pt-2026-001.json"
EVIDENCE_MANIFESTS = REPO_ROOT / "evidence" / "manifests"
AUDIT_LOG = REPO_ROOT / ".runtime" / "audit" / "ir-audit.jsonl"


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


def alert_fingerprint(alert: dict[str, Any]) -> str:
    """Return a stable fingerprint without persisting raw alert values in the index."""
    stable = {
        key: alert.get(key, "")
        for key in (
            "alert_id",
            "rule_id",
            "host",
            "user",
            "process",
            "command_line",
            "event_time",
            "event_id",
            "search_reference",
        )
    }
    return hashlib.sha256(
        json.dumps(stable, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def deterministic_case_id(prefix: str, alert: dict[str, Any]) -> str:
    event_time = str(alert.get("event_time", ""))
    year = (
        event_time[:4]
        if len(event_time) >= 4 and event_time[:4].isdigit()
        else str(datetime.now(timezone.utc).year)
    )
    return f"{prefix}-{year}-{alert_fingerprint(alert)[:12].upper()}"


def audit(operation: str, case_id: str, status: str, **metadata: Any) -> None:
    event = {
        "timestamp": utc_now(),
        "operation": operation,
        "case_id": case_id,
        "status": status,
        "metadata": metadata,
    }
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, sort_keys=True) + "\n")


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


def repository_reference(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return path.name


def _base_case(
    prefix: str,
    case_id: str,
    title: str,
    source: dict[str, Any],
    host: str,
    user: str,
    process: str,
    technique_id: str,
    fingerprint: str,
    owner: str = "mell0wx",
) -> dict[str, Any]:
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
        "intake": {
            "fingerprint": fingerprint,
            "duplicate_count": 0,
            "last_received_at": now,
        },
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
            "hunting_status": "not-run",
            "timeline_complete": False,
            "analysis_complete": False,
            "detection_review_complete": False,
            "containment_plan_complete": False,
        },
        "evidence": {
            "manifest": "",
            "raw_location": f"external-dfir-storage/{case_id}",
            "processed_location": repository_reference(case_dir(case_id)),
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


def create_case_from_alert(
    alert_path: str | None = None,
    case_prefix: str = "IR",
    dry_run: bool = False,
) -> dict[str, Any]:
    alert = load_json(Path(alert_path) if alert_path else SAMPLE_ALERT)
    validate(alert, "alert-intake.schema.json")
    fingerprint = alert_fingerprint(alert)
    case_id = deterministic_case_id(case_prefix, alert)
    if dry_run:
        return {
            "operation": "create",
            "dry_run": True,
            "case_id": case_id,
            "fingerprint": fingerprint,
        }
    if case_file(case_id).exists():
        existing = load_case(case_id)
        existing["intake"]["duplicate_count"] += 1
        existing["intake"]["last_received_at"] = utc_now()
        existing["updated_at"] = utc_now()
        existing["notes"].append("Duplicate alert received; existing case reused.")
        save_case(existing)
        audit(
            "ir.create",
            case_id,
            "duplicate",
            duplicate_count=existing["intake"]["duplicate_count"],
        )
        return existing
    case = _base_case(
        case_prefix,
        case_id,
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
        fingerprint,
    )
    cdir = case_dir(case["id"])
    cdir.mkdir(parents=True, exist_ok=False)
    save_case(case)
    dump_json(cdir / "alert.json", alert)
    for name in (
        "enrichment.json",
        "hunt-results.json",
        "findings.json",
        "evidence-manifest.json",
        "process-tree.json",
    ):
        dump_json(cdir / name, {})
    (cdir / "timeline.csv").write_text(
        "timestamp_utc,timestamp_original,host,user,source,event_id,category,process,parent_process,command_line,source_address,destination_address,file_path,description,evidence_reference\n",
        encoding="utf-8",
    )
    (cdir / "detection-opportunities.md").write_text(
        "# Detection opportunities\n\nPending analysis.\n", encoding="utf-8"
    )
    (cdir / "containment-plan.md").write_text(
        "# Containment plan\n\nNot generated yet.\n", encoding="utf-8"
    )
    (cdir / "investigation.md").write_text(
        "# Investigation\n\nNot generated yet.\n", encoding="utf-8"
    )
    (cdir / "closure.md").write_text(
        "# Closure\n\nCase still open.\n", encoding="utf-8"
    )
    audit("ir.create", case_id, "created", fingerprint=fingerprint)
    return case


def enrich_case(
    case_id: str,
    cti_lookup: Callable[[str, float], dict[str, Any]] | None = None,
    cti_timeout: float = 3.0,
    dry_run: bool = False,
) -> dict[str, Any]:
    case = load_case(case_id)
    alert = load_json(case_dir(case_id) / "alert.json")
    assets = asset_index()
    host = alert.get("host")
    asset = assets.get(host, {})
    user = alert.get("user", "")
    indicators = alert.get("indicators", [])
    primary_indicator = indicators[0] if indicators else None
    cti: dict[str, Any] = {
        "source": "configured-cti-provider" if cti_lookup else "none",
        "confidence": "unknown",
        "timestamp": utc_now(),
        "lookup_status": "not-requested",
        "timeout_status": False,
        "errors": [],
        "result": {},
        "indicator": primary_indicator,
        "advisory_only": True,
    }
    if cti_lookup and primary_indicator:
        try:
            result = cti_lookup(str(primary_indicator["value"]), cti_timeout)
            cti.update(
                {
                    "lookup_status": "completed",
                    "result": result,
                    "confidence": str(result.get("confidence", "unknown")),
                }
            )
        except Exception as exc:
            is_timeout = isinstance(exc, TimeoutError)
            cti.update(
                {
                    "lookup_status": "error",
                    "timeout_status": is_timeout,
                    "errors": ["provider-timeout" if is_timeout else "provider-error"],
                }
            )
    elif cti_lookup:
        cti["lookup_status"] = "no-indicators"
    enrichment = {
        "generated_at": utc_now(),
        "host": {
            "hostname": host,
            "asset_id": asset.get("id"),
            "role": asset.get("role"),
            "network": asset.get("network"),
            "approved_target": asset.get("approved_target", False),
            "snapshot_status": "not-checked-by-repository-workflow",
            "telemetry_health": [],
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
            "classification": "not-assessed",
            "internal": None,
            "notes": [
                "No destination network indicators were present in the source alert payload."
            ],
        },
        "cti": cti,
        "recent_reference": {
            "validation_record": "detections/validation/live/VAL-2026-001-PT-2026-001.json"
            if alert.get("rule_id") == "DET-2026-001"
            else "",
            "hunt_hypothesis": "threat-hunting/hypotheses/HUNT-2026-001.yaml"
            if alert.get("technique_id") == "T1059.001"
            else "",
        },
    }
    if dry_run:
        return {
            "operation": "enrich",
            "dry_run": True,
            "case_id": case_id,
            "result": enrichment,
        }
    dump_json(case_dir(case_id) / "enrichment.json", enrichment)
    case["automation"]["enrichment_complete"] = True
    case["updated_at"] = utc_now()
    save_case(case)
    audit(
        "ir.enrich",
        case_id,
        "completed-with-errors" if cti["errors"] else "completed",
        cti_status=cti["lookup_status"],
    )
    return enrichment


def select_profile(case: dict[str, Any]) -> str:
    techniques = set(case.get("attack_mapping", {}).get("technique_ids", []))
    if "T1059.001" in techniques:
        return "powershell-execution"
    return "malware-triage"


def collect_case(
    case_id: str,
    profile: str | None = None,
    fixture_paths: list[Path] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    case = load_case(case_id)
    selected = profile or select_profile(case)
    alert_path = case_dir(case_id) / "alert.json"
    enrichment_path = case_dir(case_id) / "enrichment.json"
    artifacts: list[dict[str, Any]] = []
    if fixture_paths:
        for path in fixture_paths:
            if path.exists() and path.is_file():
                artifacts.append(
                    {
                        "path": path.name,
                        "status": "collected",
                        "sha256": file_sha256(path),
                        "error": "",
                    }
                )
            else:
                artifacts.append(
                    {
                        "path": path.name,
                        "status": "collection-failed",
                        "sha256": "",
                        "error": "fixture path not found",
                    }
                )
    else:
        artifacts = [
            {
                "name": name,
                "status": "not-collected",
                "sha256": "",
                "error": "live collector not configured",
            }
            for name in (
                "Windows event logs",
                "Sysmon",
                "PowerShell Operational",
                "PowerShell history",
                "Prefetch",
                "Amcache",
                "Shimcache",
                "scheduled tasks",
                "services",
                "registry persistence",
                "process telemetry",
                "network telemetry",
                "Velociraptor triage",
            )
        ]
    evidence_class = "fixture" if fixture_paths else "plan"
    status = (
        "fixture-collected"
        if fixture_paths and all(item["status"] == "collected" for item in artifacts)
        else "planned"
    )
    collection = {
        "case_id": case_id,
        "profile": selected,
        "target": case["scope"]["hosts"][0]
        if case["scope"]["hosts"]
        else "unknown",
        "collector": "deterministic-controller",
        "tool_version": "repo-automation-foundation-v2",
        "started_at": utc_now(),
        "completed_at": utc_now(),
        "files": [
            repository_reference(alert_path),
            repository_reference(enrichment_path),
        ],
        "hashes": {
            alert_path.name: file_sha256(alert_path),
            enrichment_path.name: file_sha256(enrichment_path),
        },
        "errors": [
            item["error"]
            for item in artifacts
            if item.get("error") and item["status"] == "collection-failed"
        ],
        "status": status,
        "evidence_class": evidence_class,
        "artifacts": artifacts,
    }
    if dry_run:
        return {
            "operation": "collect",
            "dry_run": True,
            "case_id": case_id,
            "result": collection,
        }
    validate(collection, "forensic-collection.schema.json")
    dump_json(case_dir(case_id) / "evidence-manifest.json", collection)
    EVIDENCE_MANIFESTS.mkdir(parents=True, exist_ok=True)
    manifest_path = EVIDENCE_MANIFESTS / f"{case_id}.json"
    dump_json(manifest_path, collection)
    case["evidence"]["manifest"] = repository_reference(manifest_path)
    case["evidence"]["hashes"] = collection["hashes"]
    case["automation"]["collection_complete"] = status == "live-collected"
    case["updated_at"] = utc_now()
    save_case(case)
    audit("ir.collect", case_id, status, evidence_class=evidence_class)
    return collection


def hunt_case(case_id: str) -> dict[str, Any]:
    case = load_case(case_id)
    hunt: dict[str, Any] = {
        "case_id": case_id,
        "generated_at": utc_now(),
        "hunts_run": [],
        "result_count": 0,
        "execution_status": "not-executed",
        "analyst_conclusion": "No SIEM query was executed by the repository workflow.",
        "detection_opportunity": "pending analyst review",
    }
    if "T1059.001" in case.get("attack_mapping", {}).get("technique_ids", []):
        hunt["hunts_run"].append(
            {
                "id": "HUNT-2026-001",
                "query": "threat-hunting/queries/splunk/suspicious-powershell-daily-review.spl",
                "time_range": "24h",
                "result_count": 0,
                "execution_status": "reference-only",
                "note": "Query reference prepared; run it through an authorized bounded SIEM adapter before drawing conclusions.",
            }
        )
        hunt["analyst_conclusion"] = "Historical validation may guide review but does not establish current activity."
        hunt["detection_opportunity"] = "behavior-based PowerShell decode/execute with benign negative suppression"
    dump_json(case_dir(case_id) / "hunt-results.json", hunt)
    case["automation"]["hunting_complete"] = False
    case["automation"]["hunting_status"] = "planned"
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
            "evidence_reference": repository_reference(case_dir(case_id) / "alert.json"),
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
            "evidence_reference": repository_reference(case_dir(case_id) / "enrichment.json"),
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
        "executive_summary": "Deterministic review found a reported suspicious PowerShell alert and a sanitized historical validation summary for the same behavior family. No current endpoint or SIEM state was verified.",
        "confirmed_observations": [
            f"Alert source reported {alert.get('process')} on {alert.get('host')} with technique {alert.get('technique_id')}.",
            "A sanitized historical validation summary exists for the same detection family.",
            "Current target identity, authorization, snapshot state, telemetry, and scope remain unverified.",
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
            "Do not infer current lab, SIEM, CTI, collector, or model availability from historical records.",
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
        "investigation": repository_reference(case_dir(case_id) / "investigation.md"),
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


def cleanup_case(case_id: str, dry_run: bool = False) -> dict[str, Any]:
    case = load_case(case_id)
    generated_json = (
        "enrichment.json",
        "hunt-results.json",
        "findings.json",
        "evidence-manifest.json",
        "process-tree.json",
    )
    generated_text = {
        "timeline.csv": "timestamp_utc,timestamp_original,host,user,source,event_id,category,process,parent_process,command_line,source_address,destination_address,file_path,description,evidence_reference\n",
        "detection-opportunities.md": "# Detection opportunities\n\nPending analysis.\n",
        "containment-plan.md": "# Containment plan\n\nNot generated yet.\n",
        "investigation.md": "# Investigation\n\nNot generated yet.\n",
    }
    affected = [*generated_json, *generated_text]
    if dry_run:
        return {
            "case_id": case_id,
            "status": "planned",
            "dry_run": True,
            "affected": affected,
        }
    for name in generated_json:
        dump_json(case_dir(case_id) / name, {})
    for name, content in generated_text.items():
        (case_dir(case_id) / name).write_text(content, encoding="utf-8")
    manifest = EVIDENCE_MANIFESTS / f"{case_id}.json"
    if manifest.exists():
        manifest.unlink()
    for key in (
        "enrichment_complete",
        "collection_complete",
        "hunting_complete",
        "timeline_complete",
        "analysis_complete",
        "detection_review_complete",
        "containment_plan_complete",
    ):
        case["automation"][key] = False
    case["automation"]["hunting_status"] = "not-run"
    case["evidence"]["manifest"] = ""
    case["evidence"]["hashes"] = {}
    case["status"] = "triage"
    case["updated_at"] = utc_now()
    save_case(case)
    audit("ir.cleanup", case_id, "cleaned", affected_count=len(affected))
    return {
        "case_id": case_id,
        "status": "cleaned",
        "dry_run": False,
        "affected": affected,
    }


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
