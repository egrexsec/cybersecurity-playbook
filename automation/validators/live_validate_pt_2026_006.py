#!/usr/bin/env python3
from __future__ import annotations

import json
import shlex
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
SSH = "ssh -i /root/.ssh/hermes-home-server-ed25519 -o BatchMode=yes hermes@mayuri"
SPLUNK_PASS_FILE = '/root/.splunk_admin_pass'
OUTPUT = REPO_ROOT / 'detections' / 'validation' / 'live' / 'VAL-2026-006-PT-2026-006.json'
QUERY = REPO_ROOT / 'detections' / 'generated' / 'splunk' / 'live' / 'suspicious_registry_runkey_persistence.spl'
VM = 130


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_z(dt: datetime) -> str:
    return dt.isoformat().replace('+00:00', 'Z')


def run_shell(command: str, timeout: int = 240) -> str:
    proc = subprocess.run(command, shell=True, text=True, capture_output=True, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or command)
    return proc.stdout


def guest_ps(script: str, timeout: int = 240) -> str:
    inner = f"sudo -n qm guest exec {VM} -- powershell.exe -NoProfile -ExecutionPolicy Bypass -Command {shlex.quote(script)} 2>&1"
    return run_shell(f"{SSH} {shlex.quote(inner)}", timeout=timeout)


def splunk_export(search: str, timeout: int = 240) -> list[dict[str, Any]]:
    inner = (
        f"PASS=$(<{SPLUNK_PASS_FILE}); "
        "curl -sk -u admin:$PASS https://127.0.0.1:8089/services/search/jobs/export "
        "-d output_mode=json --data-urlencode search=" + shlex.quote(search)
    )
    outer = f"{SSH} {shlex.quote('sudo -n qm guest exec 140 -- bash -lc ' + shlex.quote(inner))}"
    raw = run_shell(outer, timeout=timeout)
    marker = '"out-data" : "'
    wrapped = raw.split(marker, 1)[1].rsplit('"', 1)[0]
    text = bytes(wrapped, 'utf-8').decode('unicode_escape')
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def query_with_window(earliest_epoch: int) -> str:
    base = QUERY.read_text(encoding='utf-8').strip()
    return f"{base} earliest={earliest_epoch} latest=now | table _time host source sourcetype _raw"


def extract_results(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row['result'] for row in rows if 'result' in row]


def local_registry_query(name: str) -> str:
    return (
        "$key='HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run'; "
        f"Get-ItemProperty -Path $key -Name '{name}' -ErrorAction SilentlyContinue | ConvertTo-Json -Compress"
    )


def run_test(script: str, reg_name: str | None = None, wait_seconds: int = 5) -> dict[str, Any]:
    start = utc_now()
    exec_output = guest_ps(script)
    end = utc_now()
    time.sleep(wait_seconds)
    earliest = int(start.timestamp()) - 2
    detection_results = extract_results(splunk_export(query_with_window(earliest)))
    local_registry = guest_ps(local_registry_query(reg_name)) if reg_name else ''
    return {
        'start_time_utc': iso_z(start),
        'end_time_utc': iso_z(end),
        'exec_output': exec_output,
        'detection_results': detection_results,
        'local_registry_state': local_registry,
        'detection_fired': len(detection_results) > 0,
        'detection_latency_seconds': None if not detection_results else 'uncomputed-search-window',
    }


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    original = (REPO_ROOT / 'automation' / 'execution' / 'pt_2026_006_positive_reg_add_run.ps1').read_text(encoding='utf-8')
    variant = (REPO_ROOT / 'automation' / 'execution' / 'pt_2026_006_positive_powershell_run.ps1').read_text(encoding='utf-8')
    negatives = [
        (REPO_ROOT / 'automation' / 'execution' / 'pt_2026_006_negative_query_run.ps1').read_text(encoding='utf-8'),
        (REPO_ROOT / 'automation' / 'execution' / 'pt_2026_006_negative_reg_query.ps1').read_text(encoding='utf-8'),
        (REPO_ROOT / 'automation' / 'execution' / 'pt_2026_006_negative_benign_runvalue.ps1').read_text(encoding='utf-8'),
    ]
    cleanup = (REPO_ROOT / 'automation' / 'execution' / 'pt_2026_006_cleanup.ps1').read_text(encoding='utf-8')
    result = {
        'scenario_id': 'PT-2026-006',
        'validation_run_id': 'VAL-2026-006',
        'technique_id': 'T1547.001',
        'original': run_test(original, 'PT-2026-006-Original'),
        'variant': run_test(variant, 'PT-2026-006-Variant'),
        'negatives': [
            run_test(negatives[0], None, 3),
            run_test(negatives[1], None, 3),
            run_test(negatives[2], None, 3),
        ],
        'cleanup': {
            'start_time_utc': iso_z(utc_now()),
            'exec_output': guest_ps(cleanup),
        },
    }
    result['cleanup']['end_time_utc'] = iso_z(utc_now())
    OUTPUT.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(str(OUTPUT.relative_to(REPO_ROOT)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
