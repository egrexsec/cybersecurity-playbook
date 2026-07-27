#!/usr/bin/env python3
"""Adapters for DetLab Detection Content Specification v1."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Mapping

SPEC_VERSION = "1.0.0"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _as_authors(value: Any) -> list[str]:
    values = value if isinstance(value, list) else [value]
    return [str(item).strip() for item in values if str(item).strip()]


def normalize_sigma_rule(rule: Mapping[str, Any], source_path: Path | str, source_bytes: bytes) -> dict[str, Any]:
    detection = dict(rule.get("detection") or {})
    condition = str(detection.pop("condition", "")).strip()
    logsource = {key: str(value) for key, value in (rule.get("logsource") or {}).items() if key in {"product", "category", "service"} and value}
    tags = [str(tag).lower() for tag in (rule.get("tags") or [])]
    techniques = sorted({tag.removeprefix("attack.").upper() for tag in tags if tag.startswith("attack.t")})
    tactics = sorted({tag.removeprefix("attack.").replace("_", "-") for tag in tags if tag.startswith("attack.") and not tag.startswith("attack.t")})
    product = str(logsource.get("product", "unknown")).lower().replace(" ", "-")
    return {
        "spec_version": SPEC_VERSION,
        "kind": "detection",
        "id": str(rule.get("id", "")).strip(),
        "title": str(rule.get("title", "")).strip(),
        "description": str(rule.get("description", "")).strip(),
        "status": str(rule.get("status", "draft")).lower(),
        "severity": str(rule.get("level", "unknown")).lower(),
        "authors": _as_authors(rule.get("author", "unknown")),
        "platforms": [product],
        "attack": {"techniques": techniques, "tactics": tactics},
        "logsource": logsource,
        "logic": {"format": "sigma", "body": detection, "condition": condition},
        "source": {
            "format": "sigma",
            "path": Path(source_path).as_posix(),
            "sha256": _sha256(source_bytes),
            "canonical": True,
        },
    }


def build_generated_artifact(
    normalized: Mapping[str, Any],
    *,
    target: str,
    language: str,
    content: str,
    converter: Mapping[str, str],
) -> dict[str, Any]:
    return {
        "target": target,
        "language": language,
        "content": content,
        "content_sha256": _sha256(content.encode("utf-8")),
        "provenance": {
            "source_sha256": str(normalized["source"]["sha256"]),
            "spec_version": SPEC_VERSION,
            "converter": {"name": str(converter["name"]), "version": str(converter["version"])},
        },
    }


def generated_artifact_is_stale(normalized: Mapping[str, Any], artifact: Mapping[str, Any]) -> bool:
    provenance = artifact.get("provenance") or {}
    return (
        provenance.get("source_sha256") != normalized.get("source", {}).get("sha256")
        or provenance.get("spec_version") != SPEC_VERSION
    )
