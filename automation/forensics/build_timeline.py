#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('case_dir')
    args = parser.parse_args()
    case_dir = Path(args.case_dir)
    alert = json.loads((case_dir / 'alert.json').read_text(encoding='utf-8'))
    rows = [{
        'timestamp_utc': alert.get('event_time',''),
        'timestamp_original': alert.get('event_time',''),
        'host': alert.get('host',''),
        'user': alert.get('user',''),
        'source': alert.get('splunk_sourcetype',''),
        'event_id': alert.get('event_id',''),
        'category': 'alert',
        'process': alert.get('process',''),
        'parent_process': alert.get('parent_process',''),
        'command_line': alert.get('command_line',''),
        'source_address': '',
        'destination_address': '',
        'file_path': '',
        'description': alert.get('alert_name',''),
        'evidence_reference': 'alert.json',
    }]
    out = case_dir / 'timeline.csv'
    with out.open('w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)
    print(out)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
