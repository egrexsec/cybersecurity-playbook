#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SIGMA_ROOT = REPO_ROOT / 'detections' / 'sigma'
GEN_SPLUNK = REPO_ROOT / 'detections' / 'generated' / 'splunk'
GEN_ELASTIC = REPO_ROOT / 'detections' / 'generated' / 'elastic'
FIXTURE_ROOT = REPO_ROOT / 'tests' / 'fixtures'
SIGMA_BIN = os.environ.get('SIGMA_BIN', 'sigma')

ALLOWED_STATUS = {'experimental', 'test', 'stable', 'deprecated', 'unsupported'}
PROHIBITED_LAB_VALUES = [
    '10.10.10.', '10.20.20.', '10.30.30.', 'mayuri.lab', 'VICTIM-MAYURI', 'DC01', 'SOC01',
]
ALLOWED_ATOMIC_MARK = {'atomic-specific', 'lab-specific'}
FIELD_RAW_MAP = {
    'ScriptBlockText': "<Data Name='ScriptBlockText'>",
    'CommandLine': "<Data Name='CommandLine'>",
    'Image': "<Data Name='Image'>",
    'ParentImage': "<Data Name='ParentImage'>",
    'User': "<Data Name='User'>",
}
BASE_SEARCH = {
    'ps_script': 'search index=main source="WinEventLog:Microsoft-Windows-PowerShell/Operational" _raw="*<EventID>4104</EventID>*"',
    'process_creation': 'search index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" _raw="*<EventID>1</EventID>*"',
}


class SigmaOpsError(RuntimeError):
    pass


@dataclass
class RuleDoc:
    path: Path
    doc: dict[str, Any]

    @property
    def relpath(self) -> str:
        return str(self.path.relative_to(REPO_ROOT))

    @property
    def rule_id(self) -> str:
        return str(self.doc.get('id', '')).strip()

    @property
    def title(self) -> str:
        return str(self.doc.get('title', '')).strip()

    @property
    def status(self) -> str:
        return str(self.doc.get('status', '')).strip()

    @property
    def technique_tags(self) -> list[str]:
        return [t for t in self.doc.get('tags', []) if str(t).startswith('attack.t')]


@dataclass
class LintIssue:
    rule: str
    severity: str
    message: str


def load_rule(path: Path) -> RuleDoc:
    return RuleDoc(path=path, doc=yaml.safe_load(path.read_text(encoding='utf-8')))


def iter_rules() -> list[RuleDoc]:
    return [load_rule(path) for path in sorted(SIGMA_ROOT.rglob('*.yml'))]


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if check and proc.returncode != 0:
        raise SigmaOpsError(proc.stderr.strip() or proc.stdout.strip() or f'command failed: {cmd}')
    return proc


def lint_rules() -> tuple[list[LintIssue], list[RuleDoc]]:
    issues: list[LintIssue] = []
    rules = iter_rules()
    seen_ids: dict[str, str] = {}
    for rule in rules:
        doc = rule.doc
        rid = rule.rule_id
        if not rid:
            issues.append(LintIssue(rule.relpath, 'error', 'missing id'))
        else:
            try:
                uuid.UUID(rid)
            except Exception:
                issues.append(LintIssue(rule.relpath, 'error', 'id is not a valid UUID'))
            if rid in seen_ids:
                issues.append(LintIssue(rule.relpath, 'error', f'duplicate id also used by {seen_ids[rid]}'))
            seen_ids[rid] = rule.relpath
        if rule.status not in ALLOWED_STATUS:
            issues.append(LintIssue(rule.relpath, 'error', f'invalid status: {rule.status}'))
        if not doc.get('falsepositives'):
            issues.append(LintIssue(rule.relpath, 'error', 'falsepositives section missing or empty'))
        if not doc.get('tags'):
            issues.append(LintIssue(rule.relpath, 'warning', 'tags missing'))
        if not doc.get('date'):
            issues.append(LintIssue(rule.relpath, 'warning', 'date missing'))
        if 'detection' not in doc or 'condition' not in doc['detection']:
            issues.append(LintIssue(rule.relpath, 'error', 'detection/condition missing'))
        text = rule.path.read_text(encoding='utf-8')
        if not any(mark in text for mark in ALLOWED_ATOMIC_MARK):
            for bad in PROHIBITED_LAB_VALUES:
                if bad in text:
                    issues.append(LintIssue(rule.relpath, 'warning', f'lab-specific value found without explicit annotation: {bad}'))
        for bad in ('Invoke-AtomicTest', 'AtomicRedTeam', 'pt-2026-00'):
            if bad in text and 'atomic-specific' not in text:
                issues.append(LintIssue(rule.relpath, 'warning', f'atomic-specific string found without annotation: {bad}'))
    return issues, rules


def ensure_dirs() -> None:
    for path in [GEN_SPLUNK / 'official', GEN_SPLUNK / 'live', GEN_ELASTIC]:
        path.mkdir(parents=True, exist_ok=True)


def official_convert(rule: RuleDoc, target: str) -> str:
    cmd = [SIGMA_BIN, 'convert', '-t', target]
    if target == 'splunk':
        cmd += ['-p', 'windows-logsources']
    elif target == 'elasticsearch':
        cmd += ['-p', 'ecs_windows']
        target = 'eql'
        cmd = [SIGMA_BIN, 'convert', '-t', target, '-p', 'ecs_windows']
    cmd.append(str(rule.path))
    proc = run(cmd, cwd=REPO_ROOT)
    return proc.stdout.strip() + ('\n' if proc.stdout and not proc.stdout.endswith('\n') else '')


def selection_expr(field: str, modifier: str | None, value: Any) -> str:
    raw_prefix = FIELD_RAW_MAP.get(field)
    if not raw_prefix:
        raise SigmaOpsError(f'unsupported field for Mayuri live SPL generation: {field}')
    values = value if isinstance(value, list) else [value]
    clauses: list[str] = []
    for item in values:
        s = str(item)
        if modifier in (None, 'contains'):
            clauses.append(f'_raw="*{raw_prefix}*{s}*"')
        elif modifier == 'contains|all':
            clauses.append(f'_raw="*{raw_prefix}*{s}*"')
        elif modifier == 'endswith':
            clauses.append(f'_raw="*{raw_prefix}*{s}*</Data>*"')
        else:
            raise SigmaOpsError(f'unsupported modifier for Mayuri live SPL generation: {modifier}')
    joiner = ' AND ' if modifier == 'contains|all' else ' OR '
    if len(clauses) == 1:
        return clauses[0]
    return '(' + joiner.join(clauses) + ')'


def split_field_modifier(key: str) -> tuple[str, str | None]:
    parts = key.split('|')
    if len(parts) == 1:
        return key, None
    return parts[0], '|'.join(parts[1:])


def render_selection(selection: dict[str, Any]) -> str:
    parts: list[str] = []
    for key, value in selection.items():
        field, modifier = split_field_modifier(key)
        parts.append(selection_expr(field, modifier, value))
    return '(' + ' AND '.join(parts) + ')'


def tokenize_condition(condition: str) -> list[str]:
    return re.findall(r'\(|\)|\band\b|\bor\b|[A-Za-z0-9_]+', condition)


def render_condition(detection: dict[str, Any]) -> str:
    rendered = {k: render_selection(v) for k, v in detection.items() if k != 'condition'}
    out: list[str] = []
    for token in tokenize_condition(str(detection['condition'])):
        lowered = token.lower()
        if lowered in {'and', 'or', '(', ')'}:
            out.append(token.upper() if lowered in {'and', 'or'} else token)
        elif token in rendered:
            out.append(rendered[token])
        else:
            raise SigmaOpsError(f'unsupported condition token: {token}')
    return ' '.join(out)


def mayuri_live_spl(rule: RuleDoc) -> str:
    category = rule.doc.get('logsource', {}).get('category')
    if category not in BASE_SEARCH:
        raise SigmaOpsError(f'unsupported logsource category for Mayuri live SPL generation: {category}')
    condition = render_condition(rule.doc['detection'])
    return f"{BASE_SEARCH[category]} {condition}"


def write_generated(name: str, content: str, path: Path) -> None:
    path.write_text(content, encoding='utf-8')


def command_check(_: argparse.Namespace) -> int:
    proc = run([SIGMA_BIN, 'check', *[str(r.path) for r in iter_rules()]], cwd=REPO_ROOT, check=False)
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    return proc.returncode


def command_lint(args: argparse.Namespace) -> int:
    issues, rules = lint_rules()
    data = {
        'rule_count': len(rules),
        'issues': [issue.__dict__ for issue in issues],
    }
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        for issue in issues:
            print(f'[{issue.severity}] {issue.rule}: {issue.message}')
        print(f'Rules checked: {len(rules)}')
        print(f'Issues found: {len(issues)}')
    return 0 if not any(i.severity == 'error' for i in issues) else 2


def command_convert(args: argparse.Namespace) -> int:
    ensure_dirs()
    rules = iter_rules()
    targets = ['splunk', 'elasticsearch'] if args.target == 'all' else [args.target]
    results: list[dict[str, str]] = []
    for rule in rules:
        stem = rule.path.stem
        for target in targets:
            official = official_convert(rule, target)
            if target == 'splunk':
                out = GEN_SPLUNK / 'official' / f'{stem}.spl'
                write_generated(stem, official, out)
                live = mayuri_live_spl(rule) + '\n'
                live_out = GEN_SPLUNK / 'live' / f'{stem}.spl'
                write_generated(stem, live, live_out)
                results.append({'rule': rule.relpath, 'target': target, 'path': str(out.relative_to(REPO_ROOT))})
                results.append({'rule': rule.relpath, 'target': 'splunk-live', 'path': str(live_out.relative_to(REPO_ROOT))})
            else:
                out = GEN_ELASTIC / f'{stem}.eql'
                write_generated(stem, official, out)
                results.append({'rule': rule.relpath, 'target': target, 'path': str(out.relative_to(REPO_ROOT))})
    print(json.dumps({'generated': results}, indent=2) if args.json else yaml.safe_dump({'generated': results}, sort_keys=False))
    return 0


def rule_event_matches(rule: RuleDoc, event: dict[str, Any]) -> bool:
    detection = rule.doc['detection']
    cache: dict[str, bool] = {}
    for name, selection in detection.items():
        if name == 'condition':
            continue
        passed = True
        for key, value in selection.items():
            field, modifier = split_field_modifier(key)
            event_value = str(event.get(field, ''))
            values = value if isinstance(value, list) else [value]
            if modifier == 'contains|all':
                ok = all(str(v) in event_value for v in values)
            elif modifier == 'contains':
                ok = any(str(v) in event_value for v in values)
            elif modifier == 'endswith':
                ok = any(event_value.endswith(str(v)) for v in values)
            elif modifier is None:
                ok = any(event_value == str(v) for v in values)
            else:
                raise SigmaOpsError(f'unsupported fixture evaluation modifier: {modifier}')
            if not ok:
                passed = False
                break
        cache[name] = passed
    expr = str(detection['condition'])
    pyexpr = expr.replace(' and ', ' and ').replace(' or ', ' or ')
    for name, value in sorted(cache.items(), key=lambda item: -len(item[0])):
        pyexpr = re.sub(rf'\b{re.escape(name)}\b', str(value), pyexpr)
    return bool(eval(pyexpr, {'__builtins__': {}}, {}))


def fixture_files(rule_id: str | None = None, technique: str | None = None) -> list[Path]:
    files = sorted(FIXTURE_ROOT.rglob('*.json'))
    if technique:
        files = [f for f in files if technique in str(f)]
    if rule_id:
        filtered = []
        for f in files:
            data = json.loads(f.read_text(encoding='utf-8'))
            if data.get('rule_id') == rule_id:
                filtered.append(f)
        files = filtered
    return files


def command_test_fixtures(args: argparse.Namespace) -> int:
    rules = {r.rule_id: r for r in iter_rules()}
    results = []
    bad = 0
    for fixture_path in fixture_files(args.rule_id, args.technique):
        data = json.loads(fixture_path.read_text(encoding='utf-8'))
        if 'rule_id' not in data or 'event' not in data or 'expected_match' not in data:
            results.append({
                'fixture': str(fixture_path.relative_to(REPO_ROOT)),
                'error': 'unsupported fixture format; expected rule_id, expected_match, and event keys',
            })
            bad += 1
            continue
        rule_id = data['rule_id']
        rule = rules.get(rule_id)
        if not rule:
            results.append({'fixture': str(fixture_path.relative_to(REPO_ROOT)), 'error': f'rule not found: {rule_id}'})
            bad += 1
            continue
        actual = rule_event_matches(rule, data['event'])
        expected = bool(data['expected_match'])
        result = 'pass' if actual == expected else 'fail'
        if result == 'fail':
            bad += 1
        results.append({
            'rule_id': rule_id,
            'fixture': str(fixture_path.relative_to(REPO_ROOT)),
            'expected_match': expected,
            'actual_match': actual,
            'result': result,
            'missing_fields': sorted(set(k for sel_name, sel in rule.doc['detection'].items() if sel_name != 'condition' for k in [split_field_modifier(x)[0] for x in sel.keys()]) - set(data['event'].keys())),
            'error': None,
        })
    if args.json:
        print(json.dumps({'results': results}, indent=2))
    else:
        print(yaml.safe_dump({'results': results}, sort_keys=False))
    return 0 if bad == 0 else 2


def command_report(args: argparse.Namespace) -> int:
    issues, rules = lint_rules()
    by_rule = {r.relpath: [] for r in rules}
    for issue in issues:
        by_rule.setdefault(issue.rule, []).append({'severity': issue.severity, 'message': issue.message})
    report = []
    for rule in rules:
        report.append({
            'id': rule.rule_id,
            'title': rule.title,
            'status': rule.status,
            'path': rule.relpath,
            'techniques': rule.technique_tags,
            'issues': by_rule.get(rule.relpath, []),
        })
    if args.json:
        print(json.dumps({'rules': report}, indent=2))
    else:
        print(yaml.safe_dump({'rules': report}, sort_keys=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog='sigma-ops')
    sub = p.add_subparsers(dest='cmd', required=True)

    p_check = sub.add_parser('check')
    p_check.set_defaults(func=command_check)

    p_lint = sub.add_parser('lint')
    p_lint.add_argument('--json', action='store_true')
    p_lint.set_defaults(func=command_lint)

    p_convert = sub.add_parser('convert')
    p_convert.add_argument('--target', choices=['splunk', 'elasticsearch', 'all'], default='all')
    p_convert.add_argument('--json', action='store_true')
    p_convert.set_defaults(func=command_convert)

    p_test = sub.add_parser('test-fixtures')
    p_test.add_argument('--rule-id')
    p_test.add_argument('--technique')
    p_test.add_argument('--json', action='store_true')
    p_test.set_defaults(func=command_test_fixtures)

    p_report = sub.add_parser('report')
    p_report.add_argument('--json', action='store_true')
    p_report.set_defaults(func=command_report)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except SigmaOpsError as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
