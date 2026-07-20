#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import tempfile
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[2]
PLAYBOOK = REPO_ROOT / 'playbook'
TOKEN = os.environ.get('IR_WEBHOOK_TOKEN', '')
HOST = os.environ.get('IR_WEBHOOK_HOST', '0.0.0.0')
PORT = int(os.environ.get('IR_WEBHOOK_PORT', '8765'))


def run_playbook(args: list[str]) -> dict:
    proc = subprocess.run([str(PLAYBOOK), '--json', *args], cwd=REPO_ROOT, text=True, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or 'playbook failed')
    return json.loads(proc.stdout)


class Handler(BaseHTTPRequestHandler):
    server_version = 'IRReceiver/1.0'

    def _json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if urlparse(self.path).path != '/ir/splunk-alert':
            self._json(404, {'error': 'not found'})
            return
        if not TOKEN or self.headers.get('X-IR-Token') != TOKEN:
            self._json(403, {'error': 'forbidden'})
            return
        length = int(self.headers.get('Content-Length', '0'))
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode() or '{}')
        except Exception as exc:
            self._json(400, {'error': f'invalid json: {exc}'})
            return
        try:
            with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as fh:
                json.dump(payload, fh)
                fh.write('\n')
                alert_path = fh.name
            created = run_playbook(['ir', 'create', '--alert', alert_path])
            case_id = created['id']
            enrich = run_playbook(['ir', 'enrich', case_id])
            collect = run_playbook(['ir', 'collect', case_id])
            hunt = run_playbook(['ir', 'hunt', case_id])
            timeline = run_playbook(['ir', 'timeline', case_id])
            analyze = run_playbook(['ir', 'analyze', case_id])
            report = run_playbook(['ir', 'report', case_id])
            contain = run_playbook(['ir', 'contain', 'plan', case_id])
            self._json(200, {
                'status': 'ok',
                'case_id': case_id,
                'case_path': f'investigations/cases/{case_id}',
                'created': created,
                'enrich_summary': {'host': enrich.get('host', {}).get('hostname'), 'user': enrich.get('user', {}).get('account_name')},
                'collect_summary': {'profile': collect.get('profile'), 'target': collect.get('target')},
                'hunt_summary': {'result_count': hunt.get('result_count'), 'detection_opportunity': hunt.get('detection_opportunity')},
                'timeline_events': len(timeline.get('events', [])),
                'analysis_confidence': analyze.get('confidence'),
                'report': report,
                'containment_actions': [a.get('action') for a in contain.get('actions', [])],
            })
        except Exception as exc:
            self._json(500, {'error': str(exc)})

    def log_message(self, format: str, *args) -> None:
        print(f'{self.address_string()} - {format % args}')


if __name__ == '__main__':
    if not TOKEN:
        raise SystemExit('IR_WEBHOOK_TOKEN must be set')
    httpd = HTTPServer((HOST, PORT), Handler)
    print(f'listening on {HOST}:{PORT}')
    httpd.serve_forever()
