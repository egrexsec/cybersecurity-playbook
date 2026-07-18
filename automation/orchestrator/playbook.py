from __future__ import annotations

import argparse
import ipaddress
import json
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
SIGMA_OPS = REPO_ROOT / 'automation' / 'validators' / 'sigma_ops.py'
LIVE_VALIDATOR = REPO_ROOT / 'automation' / 'validators' / 'live_validate_previous_scenarios.py'
LIVE_VALIDATION_DIR = REPO_ROOT / 'detections' / 'validation' / 'live'
CURRENT_STATE_DIR = REPO_ROOT / 'docs' / 'current-state'


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


def _asset_index() -> dict[str, dict[str, Any]]:
    assets = list_assets()['assets']
    return {a['name']: a for a in assets}


def _check_command(command: str) -> tuple[int, str, str]:
    proc = subprocess.run(command, shell=True, text=True, capture_output=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def _run(args: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(args, cwd=REPO_ROOT, text=True, capture_output=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def _sigma_cmd_base(args: argparse.Namespace) -> list[str]:
    cmd = [sys.executable, str(SIGMA_OPS)]
    if args.sigma_cmd == 'check':
        return cmd + ['check']
    if args.sigma_cmd == 'convert':
        return cmd + ['convert', '--target', args.target]
    if args.sigma_cmd == 'lint':
        return cmd + ['lint']
    if args.sigma_cmd == 'report':
        return cmd + ['report']
    raise PlaybookError(f'unsupported sigma command: {args.sigma_cmd}')


def _validation_files() -> list[Path]:
    return sorted(LIVE_VALIDATION_DIR.glob('VAL-*.json'))


def _load_validation_summary(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding='utf-8'))
    return {
        'file': str(path.relative_to(REPO_ROOT)),
        'scenario_id': data['scenario_id'],
        'validation_run_id': data['validation_run_id'],
        'technique_id': data['technique_id'],
        'original_detection_fired': data['original']['detection_fired'],
        'variant_detection_fired': data['variant']['detection_fired'],
        'negative_detections': [n['detection_fired'] for n in data['negatives']],
        'cleanup_output': data['cleanup']['exec_output'],
    }


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
    if snapshot_name:
        vmid = asset['id'].split('-')[-1]
        cmd = (
            "ssh -i /root/.ssh/hermes-home-server-ed25519 -o BatchMode=yes hermes@mayuri "
            f"'sudo -n qm listsnapshot {vmid}'"
        )
        rc, out, err = _check_command(cmd)
        snapshot_ok = rc == 0 and snapshot_name in (out or err)
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


def validate_previous_scenarios(args: argparse.Namespace) -> int:
    files = _validation_files()
    if not files:
        raise PlaybookError('no live validation files found under detections/validation/live')
    summaries = [_load_validation_summary(path) for path in files]
    dump({'status': 'ok', 'scenarios': summaries}, args.json)
    return 0


def report_scenario(args: argparse.Namespace) -> int:
    path = resolve_scenario(args.scenario)
    doc = load_yaml(path)
    dump({'scenario': doc['id'], 'reporting': doc['reporting']}, args.json)
    return 0


def report_progress(args: argparse.Namespace) -> int:
    status_doc = CURRENT_STATE_DIR / 'PURPLE_TEAM_PROGRAM_STATUS.md'
    if not status_doc.exists():
        raise PlaybookError('status document missing')
    if args.json:
        dump({
            'status_doc': str(status_doc.relative_to(REPO_ROOT)),
            'validation_files': [str(p.relative_to(REPO_ROOT)) for p in _validation_files()],
        }, True)
    else:
        print(status_doc.read_text(encoding='utf-8'))
    return 0


def show_timeline(args: argparse.Namespace) -> int:
    path = CURRENT_STATE_DIR / 'PROJECT_TIMELINE_ASSESSMENT.md'
    if not path.exists():
        raise PlaybookError('timeline document missing')
    if args.json:
        dump({'timeline_doc': str(path.relative_to(REPO_ROOT))}, True)
    else:
        print(path.read_text(encoding='utf-8'))
    return 0


def show_status(args: argparse.Namespace) -> int:
    summary = {
        'branch': _check_command(f'git -C {REPO_ROOT} branch --show-current')[1],
        'live_validation_files': [str(p.relative_to(REPO_ROOT)) for p in _validation_files()],
        'current_state_docs': [str(p.relative_to(REPO_ROOT)) for p in sorted(CURRENT_STATE_DIR.glob('*.md'))],
        'sigma_rules': [str(p.relative_to(REPO_ROOT)) for p in sorted((REPO_ROOT / 'detections' / 'sigma').glob('**/*.yml'))],
    }
    dump(summary, args.json)
    return 0


def sigma_dispatch(args: argparse.Namespace) -> int:
    cmd = _sigma_cmd_base(args)
    if args.json:
        cmd.append('--json')
    rc, out, err = _run(cmd)
    if out:
        print(out)
    if err:
        print(err, file=sys.stderr)
    return rc


def test_dispatch(args: argparse.Namespace) -> int:
    if args.test_cmd == 'fixtures':
        cmd = [sys.executable, str(SIGMA_OPS), 'test-fixtures']
        if args.rule_id:
            cmd += ['--rule-id', args.rule_id]
        if args.technique:
            cmd += ['--technique', args.technique]
        if args.json:
            cmd.append('--json')
        rc, out, err = _run(cmd)
        if out:
            print(out)
        if err:
            print(err, file=sys.stderr)
        return rc

    if args.test_cmd == 'live':
        rc, out, err = _run([sys.executable, str(LIVE_VALIDATOR)])
        if rc != 0:
            if out:
                print(out)
            if err:
                print(err, file=sys.stderr)
            return rc
        files = _validation_files()
        if args.scenario_id:
            files = [p for p in files if args.scenario_id in p.name]
        dump({'validated': [str(p.relative_to(REPO_ROOT)) for p in files]}, args.json)
        return 0

    raise PlaybookError(f'unsupported test command: {args.test_cmd}')


def elastic_readiness(args: argparse.Namespace) -> int:
    path = CURRENT_STATE_DIR / 'ELASTIC_READINESS_DECISION.md'
    if not path.exists():
        raise PlaybookError('Elastic readiness decision doc missing')
    if args.json:
        dump({'decision_doc': str(path.relative_to(REPO_ROOT))}, True)
    else:
        print(path.read_text(encoding='utf-8'))
    return 0



def metrics(args: argparse.Namespace) -> int:
    scenarios = sorted(REPO_ROOT.glob('purple-team/scenarios/*/scenario.yaml'))
    sigma_rules = sorted((REPO_ROOT / 'detections' / 'sigma').rglob('*.yml'))
    fixture_files = sorted((REPO_ROOT / 'tests' / 'fixtures').rglob('*.json'))
    live_records = sorted((REPO_ROOT / 'detections' / 'validation' / 'live').glob('VAL-*.json'))
    techniques = set()
    for path in scenarios:
        doc = load_yaml(path)
        techniques.update(doc.get('attack', {}).get('technique_ids', []))
    positive = [p for p in fixture_files if 'positive' in p.parts]
    negative = [p for p in fixture_files if 'negative' in p.parts]
    data = {
        'scenario_count': len(scenarios),
        'sigma_rule_count': len(sigma_rules),
        'fixture_file_count': len(fixture_files),
        'positive_fixture_count': len(positive),
        'negative_fixture_count': len(negative),
        'live_validation_record_count': len(live_records),
        'attack_techniques_covered': sorted(techniques),
        'attack_technique_count': len(techniques),
        'generated_splunk_detection_count': len(list((REPO_ROOT / 'detections' / 'generated' / 'splunk' / 'official').glob('*.spl'))),
        'generated_elastic_detection_count': len(list((REPO_ROOT / 'detections' / 'generated' / 'elastic').glob('*.eql'))),
    }
    dump(data, args.json)
    return 0


def render_metrics_markdown() -> str:
    class A: json=False
    import io
    scenarios = sorted(REPO_ROOT.glob('purple-team/scenarios/*/scenario.yaml'))
    sigma_rules = sorted((REPO_ROOT / 'detections' / 'sigma').rglob('*.yml'))
    fixture_files = sorted((REPO_ROOT / 'tests' / 'fixtures').rglob('*.json'))
    live_records = sorted((REPO_ROOT / 'detections' / 'validation' / 'live').glob('VAL-*.json'))
    techniques = set()
    for path in scenarios:
        doc = load_yaml(path)
        techniques.update(doc.get('attack', {}).get('technique_ids', []))
    positive = [p for p in fixture_files if 'positive' in p.parts]
    negative = [p for p in fixture_files if 'negative' in p.parts]
    lines = [
        '# Portfolio Metrics',
        '',
        '| Metric | Value |',
        '|---|---:|',
        f'| Purple-team scenarios | {len(scenarios)} |',
        f'| Canonical Sigma rules | {len(sigma_rules)} |',
        f'| Fixture files | {len(fixture_files)} |',
        f'| Positive fixtures | {len(positive)} |',
        f'| Negative fixtures | {len(negative)} |',
        f'| Live validation records | {len(live_records)} |',
        f'| ATT&CK techniques covered | {len(techniques)} |',
        f'| Generated Splunk detections | {len(list((REPO_ROOT / "detections" / "generated" / "splunk" / "official").glob("*.spl")))} |',
        f'| Generated Elastic detections | {len(list((REPO_ROOT / "detections" / "generated" / "elastic").glob("*.eql")))} |',
        '',
        '## ATT&CK techniques currently represented',
        '',
        ', '.join(sorted(techniques)) or 'none',
        '',
        '> Generated from repository content. Rebuild with `python3 playbook metrics`.',
    ]
    return '\n'.join(lines) + '\n'


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='playbook')
    parser.add_argument('--json', action='store_true', help='emit JSON')
    sub = parser.add_subparsers(dest='command', required=True)

    p_inventory = sub.add_parser('inventory')
    p_inventory.set_defaults(func=inventory)

    p_status = sub.add_parser('status')
    p_status.set_defaults(func=show_status)

    p_timeline = sub.add_parser('timeline')
    p_timeline.set_defaults(func=show_timeline)

    p_metrics = sub.add_parser('metrics')
    p_metrics.set_defaults(func=metrics)

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
    rp = p_report.add_subparsers(dest='report_cmd', required=True)
    p_report_scenario = rp.add_parser('scenario')
    p_report_scenario.add_argument('scenario')
    p_report_scenario.set_defaults(func=report_scenario)
    p_report_progress = rp.add_parser('progress')
    p_report_progress.set_defaults(func=report_progress)

    p_validate_repo = sub.add_parser('validate')
    vr = p_validate_repo.add_subparsers(dest='validate_cmd')
    p_validate_repo.set_defaults(func=validate_repo)
    p_validate_prev = vr.add_parser('previous-scenarios')
    p_validate_prev.set_defaults(func=validate_previous_scenarios)

    p_sigma = sub.add_parser('sigma')
    sg = p_sigma.add_subparsers(dest='sigma_cmd', required=True)
    sg_check = sg.add_parser('check')
    sg_check.set_defaults(func=sigma_dispatch)
    sg_convert = sg.add_parser('convert')
    sg_convert.add_argument('--target', choices=['splunk', 'elasticsearch', 'all'], default='all')
    sg_convert.set_defaults(func=sigma_dispatch)
    sg_lint = sg.add_parser('lint')
    sg_lint.set_defaults(func=sigma_dispatch)
    sg_report = sg.add_parser('report')
    sg_report.set_defaults(func=sigma_dispatch)

    p_test = sub.add_parser('test')
    ts = p_test.add_subparsers(dest='test_cmd', required=True)
    t_fix = ts.add_parser('fixtures')
    t_fix.add_argument('--rule-id')
    t_fix.add_argument('--technique')
    t_fix.set_defaults(func=test_dispatch)
    t_live = ts.add_parser('live')
    t_live.add_argument('scenario_id', nargs='?')
    t_live.set_defaults(func=test_dispatch)

    p_elastic = sub.add_parser('elastic')
    el = p_elastic.add_subparsers(dest='elastic_cmd', required=True)
    el_ready = el.add_parser('readiness')
    el_ready.set_defaults(func=elastic_readiness)

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
