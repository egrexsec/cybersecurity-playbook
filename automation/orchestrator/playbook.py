from __future__ import annotations

import argparse
import ipaddress
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import jsonschema
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = REPO_ROOT / 'schemas'
ASSET_FILE = REPO_ROOT / 'automation' / 'integrations' / 'lab-assets.yaml'
SCENARIO_ROOT = REPO_ROOT / 'purple-team' / 'scenarios'


class PlaybookError(RuntimeError):
    pass


def load_yaml(path: Path) -> Any:
    with path.open('r', encoding='utf-8') as fh:
        return yaml.safe_load(fh)


def dump(data: Any, as_json: bool) -> None:
    if as_json:
        print(json.dumps(data, indent=2))
        return
    if isinstance(data, (dict, list)):
        print(yaml.safe_dump(data, sort_keys=False))
    else:
        print(data)


def resolve_scenario(value: str) -> Path:
    candidate = Path(value)
    if candidate.exists():
        return candidate.resolve()
    for path in SCENARIO_ROOT.glob('*/scenario.yaml'):
        doc = load_yaml(path)
        if doc.get('id') == value:
            return path.resolve()
    raise PlaybookError(f'scenario not found: {value}')


def schema_path(name: str) -> Path:
    return SCHEMA_DIR / name


def validate_schema(doc: dict, schema_name: str) -> None:
    schema = json.loads(schema_path(schema_name).read_text(encoding='utf-8'))
    jsonschema.validate(doc, schema)


def list_assets() -> dict[str, Any]:
    return load_yaml(ASSET_FILE)


def scenario_validate(args: argparse.Namespace) -> int:
    path = resolve_scenario(args.scenario)
    doc = load_yaml(path)
    validate_schema(doc, 'purple-team-scenario.schema.json')
    dump({'status': 'ok', 'scenario': str(path), 'id': doc['id']}, args.json)
    return 0


def scenario_plan(args: argparse.Namespace) -> int:
    path = resolve_scenario(args.scenario)
    doc = load_yaml(path)
    plan = {
        'id': doc['id'],
        'title': doc['title'],
        'approved_hosts': doc['targets']['approved_hosts'],
        'techniques': doc['attack']['technique_ids'],
        'tests': doc['attack']['test_ids'],
        'baseline_queries': doc['baseline']['queries'],
        'collections_before': doc['collection']['before'],
        'collections_after': doc['collection']['after'],
        'expected_rules': doc['detections']['expected_rules'],
    }
    dump(plan, args.json)
    return 0


def _asset_index() -> dict[str, dict[str, Any]]:
    assets = list_assets()['assets']
    return {a['name']: a for a in assets}


def _check_command(command: str) -> tuple[int, str, str]:
    proc = subprocess.run(command, shell=True, text=True, capture_output=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def scenario_preflight(args: argparse.Namespace) -> int:
    path = resolve_scenario(args.scenario)
    doc = load_yaml(path)
    assets = _asset_index()
    approved_networks = [ipaddress.ip_network(n) for n in list_assets()['approved_networks']]
    target = doc['targets']['approved_hosts'][0]
    asset = assets.get(target)
    if not asset:
        raise PlaybookError(f'target asset missing from inventory: {target}')
    if not asset.get('approved_target'):
        raise PlaybookError(f'target not approved: {target}')
    ip = ipaddress.ip_address(asset['ip'])
    if not any(ip in net for net in approved_networks):
        raise PlaybookError(f'target ip outside approved networks: {ip}')

    snapshot_name = doc.get('safety', {}).get('required_snapshot_name', '')
    snapshot_ok = False
    snapshot_raw = ''
    if snapshot_name:
        vmid = asset['id'].split('-')[-1]
        cmd = (
            "ssh -i /root/.ssh/hermes-home-server-ed25519 -o BatchMode=yes hermes@mayuri "
            f"'sudo -n qm listsnapshot {vmid}'"
        )
        rc, out, err = _check_command(cmd)
        snapshot_raw = out or err
        snapshot_ok = rc == 0 and snapshot_name in snapshot_raw
    else:
        snapshot_ok = True

    required = {
        'target': target,
        'target_ip': asset['ip'],
        'risk_level': doc['safety']['risk_level'],
        'snapshot_required': doc['safety']['snapshot_required'],
        'snapshot_check': snapshot_ok,
        'cleanup_required': doc['safety']['cleanup_required'],
        'timeout_seconds': doc['safety']['timeout_seconds'],
    }
    dump(required, args.json)
    return 0 if snapshot_ok else 2


def inventory(args: argparse.Namespace) -> int:
    dump(list_assets(), args.json)
    return 0


def validate_repo(args: argparse.Namespace) -> int:
    checked: list[str] = []
    for path in REPO_ROOT.glob('purple-team/scenarios/*/scenario.yaml'):
        validate_schema(load_yaml(path), 'purple-team-scenario.schema.json')
        checked.append(str(path.relative_to(REPO_ROOT)))
    for path in REPO_ROOT.glob('threat-hunting/hypotheses/*.yaml'):
        validate_schema(load_yaml(path), 'threat-hunt-hypothesis.schema.json')
        checked.append(str(path.relative_to(REPO_ROOT)))
    dump({'status': 'ok', 'validated_files': checked}, args.json)
    return 0


def report(args: argparse.Namespace) -> int:
    path = resolve_scenario(args.scenario)
    doc = load_yaml(path)
    dump({'scenario': doc['id'], 'reporting': doc['reporting']}, args.json)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='playbook')
    parser.add_argument('--json', action='store_true', help='emit JSON')
    sub = parser.add_subparsers(dest='command', required=True)

    p_inventory = sub.add_parser('inventory')
    p_inventory.set_defaults(func=inventory)

    p_preflight = sub.add_parser('preflight')
    p_preflight.add_argument('scenario')
    p_preflight.set_defaults(func=scenario_preflight)

    p_scenario = sub.add_parser('scenario')
    sc = p_scenario.add_subparsers(dest='scenario_cmd', required=True)
    p_validate = sc.add_parser('validate')
    p_validate.add_argument('scenario')
    p_validate.set_defaults(func=scenario_validate)
    p_plan = sc.add_parser('plan')
    p_plan.add_argument('scenario')
    p_plan.set_defaults(func=scenario_plan)

    p_report = sub.add_parser('report')
    p_report.add_argument('scenario')
    p_report.set_defaults(func=report)

    p_validate_repo = sub.add_parser('validate')
    p_validate_repo.set_defaults(func=validate_repo)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except PlaybookError as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    except jsonschema.ValidationError as exc:
        print(f'SCHEMA ERROR: {exc.message}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
