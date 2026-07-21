#!/usr/bin/env python3
from __future__ import annotations

import hmac
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
HOST = os.environ.get('IR_WEBHOOK_HOST', '127.0.0.1')
PORT = int(os.environ.get('IR_WEBHOOK_PORT', '8765'))
MAX_BODY_BYTES = min(int(os.environ.get('IR_WEBHOOK_MAX_BODY_BYTES', '262144')), 1048576)
WORKFLOW_TIMEOUT_SECONDS = min(int(os.environ.get('IR_WORKFLOW_TIMEOUT_SECONDS', '60')), 300)


def parse_content_length(value: str | None) -> int:
    if not value:
        raise ValueError('content length required')
    try:
        length = int(value)
    except ValueError as exc:
        raise ValueError('invalid content length') from exc
    if length < 1 or length > MAX_BODY_BYTES:
        raise ValueError('payload size outside allowed range')
    return length


def authorized(expected: str, provided: str | None) -> bool:
    return bool(expected and provided and hmac.compare_digest(expected, provided))


def run_playbook(args: list[str]) -> dict:
    proc = subprocess.run(
        [str(PLAYBOOK), '--json', *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        timeout=WORKFLOW_TIMEOUT_SECONDS,
    )
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
        if not authorized(TOKEN, self.headers.get('X-IR-Token')):
            self._json(403, {'error': 'forbidden'})
            return
        if self.headers.get_content_type() != 'application/json':
            self._json(415, {'error': 'content type must be application/json'})
            return
        try:
            length = parse_content_length(self.headers.get('Content-Length'))
        except ValueError as exc:
            self._json(413, {'error': str(exc)})
            return
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode() or '{}')
        except Exception as exc:
            self._json(400, {'error': f'invalid json: {exc}'})
            return
        alert_path = ''
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
        except subprocess.TimeoutExpired:
            self._json(504, {'error': 'workflow timeout', 'status': 'failed'})
        except Exception:
            self._json(500, {'error': 'workflow failed', 'status': 'failed'})
        finally:
            if alert_path:
                Path(alert_path).unlink(missing_ok=True)

    def log_message(self, format: str, *args) -> None:
        print(f'{self.address_string()} - {format % args}')


if __name__ == '__main__':
    if not TOKEN:
        raise SystemExit('IR_WEBHOOK_TOKEN must be set')
    httpd = HTTPServer((HOST, PORT), Handler)
    print(f'listening on {HOST}:{PORT}')
    httpd.serve_forever()
