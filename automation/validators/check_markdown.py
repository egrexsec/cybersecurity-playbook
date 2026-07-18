#!/usr/bin/env python3
from __future__ import annotations
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
EXCLUDE_DIRS = {'.git', '.venv', 'venv', '__pycache__', '.pytest_cache', '.mypy_cache'}
LINK_RE = re.compile(r'\[[^\]]+\]\(([^)]+)\)')
ANCHOR_RE = re.compile(r'^#+\s+(.*)$', re.M)


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r'[`*_~]', '', text)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text


def headings(path: Path) -> set[str]:
    return {slugify(m.group(1)) for m in ANCHOR_RE.finditer(path.read_text(encoding='utf-8'))}


def iter_md() -> list[Path]:
    out=[]
    for p in REPO_ROOT.rglob('*.md'):
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        out.append(p)
    return sorted(out)


def main() -> int:
    issues=[]
    for md in iter_md():
        text=md.read_text(encoding='utf-8')
        for raw in LINK_RE.findall(text):
            if raw.startswith('http://') or raw.startswith('https://') or raw.startswith('mailto:'):
                continue
            target, _, frag = raw.partition('#')
            if not target:
                if frag and slugify(frag) not in headings(md):
                    issues.append(f'{md.relative_to(REPO_ROOT)}: missing local anchor #{frag}')
                continue
            target_path = (md.parent / target).resolve()
            if not target_path.exists():
                issues.append(f'{md.relative_to(REPO_ROOT)}: missing target {raw}')
                continue
            if frag and target_path.suffix.lower()=='.md':
                if slugify(frag) not in headings(target_path):
                    issues.append(f'{md.relative_to(REPO_ROOT)}: missing anchor {raw}')
    if issues:
        print('\\n'.join(issues))
        return 2
    print('markdown links ok')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
