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
OUTPUT_DIR = REPO_ROOT / 'detections' / 'validation' / 'live'


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_z(dt: datetime) -> str:
    return dt.isoformat().replace('+00:00', 'Z')


def run_shell(command: str, timeout: int = 240) -> str:
    proc = subprocess.run(command, shell=True, text=True, capture_output=True, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or command)
    return proc.stdout


def guest_ps(vm: int, script: str, timeout: int = 240) -> str:
    inner = f"sudo -n qm guest exec {vm} -- powershell.exe -NoProfile -ExecutionPolicy Bypass -Command {shlex.quote(script)} 2>&1"
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
    if marker not in raw:
        raise RuntimeError(f'unexpected Splunk export wrapper: {raw[:500]}')
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


def query_with_window(query_path: Path, earliest_epoch: int) -> str:
    base = query_path.read_text(encoding='utf-8').strip()
    return f"{base} earliest={earliest_epoch} latest=now | table _time host source sourcetype _raw"


def marker_query(base: str, earliest_epoch: int) -> str:
    return f"{base} earliest={earliest_epoch} latest=now | table _time host source sourcetype _raw"


def extract_results(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row['result'] for row in rows if 'result' in row]


def run_test(vm: int, command: str, query_path: Path, marker_search: str | None = None, wait_seconds: int = 8) -> dict[str, Any]:
    start = utc_now()
    exec_output = guest_ps(vm, command)
    end = utc_now()
    time.sleep(wait_seconds)
    earliest = int(start.timestamp()) - 2
    detection_rows = extract_results(splunk_export(query_with_window(query_path, earliest)))
    marker_rows = extract_results(splunk_export(marker_query(marker_search, earliest))) if marker_search else []
    return {
        'start_time_utc': iso_z(start),
        'end_time_utc': iso_z(end),
        'exec_output': exec_output,
        'detection_results': detection_rows,
        'marker_results': marker_rows,
        'detection_fired': len(detection_rows) > 0,
        'marker_found': len(marker_rows) > 0 if marker_search else None,
        'detection_latency_seconds': None if not detection_rows else 'uncomputed-search-window',
    }


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    scenarios = [
        {
            'scenario_id': 'PT-2026-001',
            'validation_run_id': 'VAL-2026-001',
            'technique_id': 'T1059.001',
            'query': REPO_ROOT / 'detections' / 'generated' / 'splunk' / 'live' / 'suspicious_powershell_execution.spl',
            'original': "$ErrorActionPreference='Stop'; $encoded='U2V0LUNvbnRlbnQgLXBhdGggIiRlbnY6U3lzdGVtUm9vdC9UZW1wL2FydC1tYXJrZXIudHh0IiAtdmFsdWUgIkhlbGxvIGZyb20gdGhlIEF0b21pYyBSZWQgVGVhbSI='; reg.exe add \"HKEY_CURRENT_USER\\Software\\Classes\\AtomicRedTeam\" /v ART /t REG_SZ /d $encoded /f; Invoke-Expression ([Text.Encoding]::ASCII.GetString([Convert]::FromBase64String((Get-ItemProperty 'HKCU:\\Software\\Classes\\AtomicRedTeam').ART))); Get-Item \"$env:SystemRoot\\Temp\\art-marker.txt\" | Select-Object FullName,Length,LastWriteTime | Format-List",
            'variant': "$ErrorActionPreference='Stop'; $bytes=[Text.Encoding]::Unicode.GetBytes('Set-Content -Path \"$env:SystemRoot\\Temp\\variant-marker.txt\" -Value \"Hello from modified variant\"'); $b64=[Convert]::ToBase64String($bytes); Invoke-Expression ([Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($b64))); Get-Item \"$env:SystemRoot\\Temp\\variant-marker.txt\" | Select-Object FullName,Length,LastWriteTime | Format-List",
            'negatives': [
                'Get-Date | Out-File -FilePath "$env:TEMP\\pt-2026-001-negative-date.txt" -Encoding utf8; Get-Item "$env:TEMP\\pt-2026-001-negative-date.txt" | Select-Object FullName,Length,LastWriteTime | Format-List',
                'Get-Process | Select-Object -First 5 Name,Id | Out-File -FilePath "$env:TEMP\\pt-2026-001-negative-process.txt" -Encoding utf8; Get-Item "$env:TEMP\\pt-2026-001-negative-process.txt" | Select-Object FullName,Length,LastWriteTime | Format-List',
                'Get-Service | Select-Object -First 5 Name,Status | Out-File -FilePath "$env:TEMP\\pt-2026-001-negative-service.txt" -Encoding utf8; Get-Item "$env:TEMP\\pt-2026-001-negative-service.txt" | Select-Object FullName,Length,LastWriteTime | Format-List',
            ],
            'marker_searches': [
                'search index=main host="VICTIM-MAYURI" source="WinEventLog:Microsoft-Windows-PowerShell/Operational" ("art-marker.txt" OR "AtomicRedTeam")',
                'search index=main host="VICTIM-MAYURI" source="WinEventLog:Microsoft-Windows-PowerShell/Operational" "variant-marker.txt"',
            ],
            'cleanup': 'Remove-Item -Path "$env:SystemRoot\\Temp\\art-marker.txt","$env:SystemRoot\\Temp\\variant-marker.txt","$env:TEMP\\pt-2026-001-negative-date.txt","$env:TEMP\\pt-2026-001-negative-process.txt","$env:TEMP\\pt-2026-001-negative-service.txt" -Force -ErrorAction SilentlyContinue; Remove-Item "HKCU:\\Software\\Classes\\AtomicRedTeam" -Force -ErrorAction SilentlyContinue; "cleanup complete"',
        },
        {
            'scenario_id': 'PT-2026-002',
            'validation_run_id': 'VAL-2026-002',
            'technique_id': 'T1059.003',
            'query': REPO_ROOT / 'detections' / 'generated' / 'splunk' / 'live' / 'suspicious_cmd_execution.spl',
            'original': '$ErrorActionPreference="Stop"; $scriptPath = Join-Path $env:TEMP "pt-2026-002-positive.cmd"; $markerPath = Join-Path $env:SystemRoot "Temp\\pt-2026-002-positive.txt"; @"\n@echo off\necho PT-2026-002 batch positive>"%SystemRoot%\\Temp\\pt-2026-002-positive.txt"\ntype "%SystemRoot%\\Temp\\pt-2026-002-positive.txt"\n"@ | Set-Content -Path $scriptPath -Encoding ascii; cmd.exe /c $scriptPath; Get-Item $markerPath | Select-Object FullName,Length,LastWriteTime | Format-List',
            'variant': '$ErrorActionPreference="Stop"; $markerPath = Join-Path $env:SystemRoot "Temp\\pt-2026-002-variant.txt"; cmd.exe /c "%LOCALAPPDATA:~-3,1%md /c echo PT-2026-002 suspicious variant > %SystemRoot%\\Temp\\pt-2026-002-variant.txt & type %SystemRoot%\\Temp\\pt-2026-002-variant.txt"; Get-Item $markerPath | Select-Object FullName,Length,LastWriteTime | Format-List',
            'negatives': [
                'cmd.exe /c dir C:\\Windows > "$env:TEMP\\pt-2026-002-negative-dir.txt"; Get-Item "$env:TEMP\\pt-2026-002-negative-dir.txt" | Select-Object FullName,Length,LastWriteTime | Format-List',
                'cmd.exe /c echo benign > "$env:TEMP\\pt-2026-002-negative-echo.txt"; Get-Item "$env:TEMP\\pt-2026-002-negative-echo.txt" | Select-Object FullName,Length,LastWriteTime | Format-List',
                'cmd.exe /c whoami /all > "$env:TEMP\\pt-2026-002-negative-whoami.txt"; Get-Item "$env:TEMP\\pt-2026-002-negative-whoami.txt" | Select-Object FullName,Length,LastWriteTime | Format-List',
            ],
            'marker_searches': [
                'search index=main host="VICTIM-MAYURI" source="WinEventLog:Microsoft-Windows-Sysmon/Operational" ("pt-2026-002-positive.cmd" OR "pt-2026-002-positive.txt")',
                'search index=main host="VICTIM-MAYURI" source="WinEventLog:Microsoft-Windows-Sysmon/Operational" ("pt-2026-002-variant.txt" OR ":~-")',
            ],
            'cleanup': 'Remove-Item -Path "$env:TEMP\\pt-2026-002-positive.cmd","$env:SystemRoot\\Temp\\pt-2026-002-positive.txt","$env:SystemRoot\\Temp\\pt-2026-002-variant.txt","$env:TEMP\\pt-2026-002-negative-dir.txt","$env:TEMP\\pt-2026-002-negative-echo.txt","$env:TEMP\\pt-2026-002-negative-whoami.txt" -Force -ErrorAction SilentlyContinue; "cleanup complete"',
        },
        {
            'scenario_id': 'PT-2026-003',
            'validation_run_id': 'VAL-2026-003',
            'technique_id': 'T1047',
            'query': REPO_ROOT / 'detections' / 'generated' / 'splunk' / 'live' / 'suspicious_wmi_process_creation_powershell.spl',
            'original': '$marker = Join-Path $env:TEMP "pt-2026-003-wmic-positive.txt"; if (Test-Path $marker) { Remove-Item $marker -Force }; $null = ([wmiclass]"Win32_Process").Create("cmd.exe /c echo PT-2026-003-WMIC>%TEMP%\\pt-2026-003-wmic-positive.txt"); Start-Sleep -Seconds 3; Get-Item $marker | Select-Object FullName,Length,LastWriteTime | Format-List',
            'variant': '$marker = Join-Path $env:TEMP "pt-2026-003-invoke-wmi-positive.txt"; if (Test-Path $marker) { Remove-Item $marker -Force }; Invoke-WmiMethod -Path Win32_Process -Name Create -ArgumentList "cmd.exe /c echo PT-2026-003-INVOKE-WMI>%TEMP%\\pt-2026-003-invoke-wmi-positive.txt" | Out-Null; Start-Sleep -Seconds 3; Get-Item $marker | Select-Object FullName,Length,LastWriteTime | Format-List',
            'negatives': [
                'Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version | Format-List',
                'Get-WmiObject Win32_Service -Filter "Name=\'Spooler\'" | Select-Object Name,State,StartMode | Format-List',
                'Get-WmiObject Win32_OperatingSystem | Select-Object CSName,Caption,Version | Format-List',
            ],
            'marker_searches': [
                'search index=main host="VICTIM-MAYURI" source="WinEventLog:Microsoft-Windows-PowerShell/Operational" ("pt-2026-003-wmic-positive.txt" OR "[wmiclass]" OR "Win32_Process")',
                'search index=main host="VICTIM-MAYURI" source="WinEventLog:Microsoft-Windows-PowerShell/Operational" ("pt-2026-003-invoke-wmi-positive.txt" OR "Invoke-WmiMethod" OR "Win32_Process")',
            ],
            'cleanup': 'Remove-Item -Path "$env:TEMP\\pt-2026-003-wmic-positive.txt","$env:TEMP\\pt-2026-003-invoke-wmi-positive.txt" -Force -ErrorAction SilentlyContinue; "cleanup complete"',
        },
    ]

    for scenario in scenarios:
        data: dict[str, Any] = {
            'scenario_id': scenario['scenario_id'],
            'validation_run_id': scenario['validation_run_id'],
            'technique_id': scenario['technique_id'],
        }
        data['original'] = run_test(130, scenario['original'], scenario['query'], scenario['marker_searches'][0])
        data['variant'] = run_test(130, scenario['variant'], scenario['query'], scenario['marker_searches'][1])
        negatives = []
        for negative in scenario['negatives']:
            negatives.append(run_test(130, negative, scenario['query'], None, wait_seconds=5))
        data['negatives'] = negatives
        cleanup_start = utc_now()
        cleanup_output = guest_ps(130, scenario['cleanup'])
        cleanup_end = utc_now()
        data['cleanup'] = {
            'start_time_utc': iso_z(cleanup_start),
            'end_time_utc': iso_z(cleanup_end),
            'exec_output': cleanup_output,
        }
        out_path = OUTPUT_DIR / f"{scenario['validation_run_id']}-{scenario['scenario_id']}.json"
        out_path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
        print(out_path.relative_to(REPO_ROOT))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
