#!/usr/bin/env python3
"""Build the deterministic PT-2026-001 portfolio pack manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "detections" / "packs" / "validated-powershell-lifecycle-v1" / "manifest.json"
SOURCE = "detections/sigma/windows/process_creation/suspicious_powershell_execution.yml"
FIXTURE_ROOT = Path("tests/fixtures/T1059.001")
ARTIFACTS = (
    ("splunk-official", "detections/generated/splunk/official/suspicious_powershell_execution.spl"),
    ("splunk-mayuri-live", "detections/generated/splunk/live/suspicious_powershell_execution.spl"),
    ("elastic-eql", "detections/generated/elastic/suspicious_powershell_execution.eql"),
)


def file_record(relative_path: str | Path) -> dict[str, str]:
    relative = Path(relative_path)
    path = ROOT / relative
    if not path.is_file():
        raise FileNotFoundError(f"required pack input is missing: {relative.as_posix()}")
    return {
        "path": relative.as_posix(),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def fixture_records(kind: str) -> list[dict[str, str]]:
    directory = ROOT / FIXTURE_ROOT / kind
    return [file_record(path.relative_to(ROOT)) for path in sorted(directory.glob("*.json"))]


def build_manifest() -> dict[str, Any]:
    artifacts = []
    for backend, path in ARTIFACTS:
        record = file_record(path)
        record["backend"] = backend
        artifacts.append(record)

    return {
        "pack_version": "1.0.0",
        "title": "Validated PowerShell Detection Lifecycle v1",
        "scenario_id": "PT-2026-001",
        "detection_id": "0b77858e-3f9f-4a0e-bc4c-8f0ac4b2b0d1",
        "attack_techniques": ["T1059.001", "T1027"],
        "validation_status": "live-validated",
        "validation_date": "2026-07-18",
        "source": file_record(SOURCE),
        "fixtures": {
            "positive": fixture_records("positive"),
            "negative": fixture_records("negative"),
        },
        "generated_artifacts": artifacts,
        "provenance": {
            "contract": "schemas/detlab-detection-content-v1.schema.json",
            "generator": "automation/build_powershell_lifecycle_pack.py",
            "query_generator": "automation/validators/sigma_ops.py",
            "validation_record": "detections/validation/DET-2026-001-validation.md",
            "sanitized_evidence_root": "evidence/sanitized/PT-2026-001",
            "case_study": "case-studies/powershell-encoded-command/README.md",
        },
        "external_evidence": {
            "repository": "egrexsec/mayuri-purple-team-lab",
            "path": "evidence/powershell-detection-to-case.md",
            "result": "PASS — live validated",
        },
        "detlab_workflow": {
            "input": SOURCE,
            "targets": ["splunk", "elastic-eql", "microsoft-kusto"],
            "export": "markdown detection pack with source hash and converter provenance",
        },
        "sanitization": "Manifest contains public artifact paths and hashes only; raw telemetry is excluded.",
    }


def serialize(manifest: dict[str, Any]) -> str:
    return json.dumps(manifest, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if the committed manifest is stale")
    args = parser.parse_args()
    expected = serialize(build_manifest())
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != expected:
            print(f"stale or missing lifecycle manifest: {OUTPUT.relative_to(ROOT)}")
            return 1
        print(f"lifecycle manifest is current: {OUTPUT.relative_to(ROOT)}")
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(expected, encoding="utf-8")
    print(OUTPUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
