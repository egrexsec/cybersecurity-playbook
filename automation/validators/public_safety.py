#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

PATTERNS = {
    "rfc1918-address": re.compile(
        r"(?<![0-9])(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})(?![0-9])"
    ),
    "cgnat-address": re.compile(
        r"(?<![0-9])100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])(?:\.\d{1,3}){2}(?![0-9])"
    ),
    "internal-lab-domain": re.compile(r"\b[a-z0-9-]+\.lab\b", re.IGNORECASE),
    "environment-host-identifier": re.compile(
        r"\b(?:VICTIM-MAYURI|DC01-MAYURI|SOC-MAYURI|mayuri-(?:osint|dfir))\b",
        re.IGNORECASE,
    ),
    "environment-public-dns": re.compile(
        r"\b[a-z0-9-]+\.lab\.mell0wx\.tech\b", re.IGNORECASE
    ),
    "private-key-material": re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
    ),
    "likely-secret-assignment": re.compile(
        r"(?im)^\s*(?:password|token|api[_-]?key|secret)\s*[:=]\s*(?!replace-|todo_|\$\{|<)[^\s#]{12,}\s*$"
    ),
}

RUNTIME_PREFIXES = (
    "evidence/raw/",
    "investigations/cases/",
    ".runtime/",
)
RUNTIME_EXCEPTIONS = {
    "investigations/cases/.gitkeep",
}
MANIFEST_PREFIX = "evidence/manifests/"
MANIFEST_EXCEPTIONS = {"evidence/manifests/.gitkeep"}
LIVE_VALIDATION_PREFIX = "detections/validation/live/"
RAW_LIVE_KEYS = re.compile(r'"(?:_raw|exec_output|detection_results|marker_results)"\s*:')


def tracked_files() -> list[str]:
    proc = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
    )
    return [item.decode() for item in proc.stdout.split(b"\0") if item]


def scan() -> list[str]:
    issues: list[str] = []
    for relative in tracked_files():
        if relative == "automation/validators/public_safety.py":
            continue
        if relative in RUNTIME_EXCEPTIONS or relative in MANIFEST_EXCEPTIONS:
            continue
        if relative.startswith(RUNTIME_PREFIXES):
            issues.append(f"{relative}: tracked runtime evidence is prohibited")
            continue
        if relative.startswith(MANIFEST_PREFIX):
            issues.append(f"{relative}: tracked runtime manifest is prohibited")
            continue
        path = REPO_ROOT / relative
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for name, pattern in PATTERNS.items():
            if name == "likely-secret-assignment" and path.suffix.lower() not in {
                ".env", ".example", ".yaml", ".yml", ".json", ".toml", ".ini"
            }:
                continue
            if pattern.search(text):
                issues.append(f"{relative}: {name}")
        if relative.startswith(LIVE_VALIDATION_PREFIX) and RAW_LIVE_KEYS.search(text):
            issues.append(f"{relative}: raw live evidence fields are prohibited")
    return sorted(set(issues))


def main() -> int:
    issues = scan()
    if issues:
        print("public-safety scan failed:", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1
    print("public-safety scan passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
