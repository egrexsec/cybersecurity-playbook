#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

LISTEN_HOST = os.environ.get("RELAY_LISTEN_HOST", "10.10.10.250")
LISTEN_PORT = int(os.environ.get("RELAY_LISTEN_PORT", "8766"))
ALLOWED_SOURCE = os.environ.get("RELAY_ALLOWED_SOURCE", "10.10.10.20")
TOKEN = os.environ["RELAY_TOKEN"]
UPSTREAM = os.environ.get(
    "RELAY_UPSTREAM",
    "https://n8n.lab.mell0wx.tech/webhook/splunk-alert-to-case",
)
MAX_BODY = 1024 * 1024


class RelayHandler(BaseHTTPRequestHandler):
    server_version = "splunk-n8n-relay/1.0"

    def _reply(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if self.client_address[0] != ALLOWED_SOURCE:
            self._reply(403, {"error": "source_not_allowed"})
            return
        if self.path != f"/splunk/{TOKEN}":
            self._reply(404, {"error": "not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._reply(400, {"error": "invalid_content_length"})
            return
        if length <= 0 or length > MAX_BODY:
            self._reply(413, {"error": "invalid_body_size"})
            return
        body = self.rfile.read(length)
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            self._reply(400, {"error": "invalid_json"})
            return
        if not isinstance(parsed, dict):
            self._reply(400, {"error": "json_object_required"})
            return

        request = urllib.request.Request(
            UPSTREAM,
            data=json.dumps(parsed, separators=(",", ":")).encode(),
            headers={
                "Content-Type": "application/json",
                "User-Agent": "mayuri-splunk-n8n-relay/1.0",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                upstream_body = response.read(MAX_BODY)
                self.send_response(response.status)
                self.send_header(
                    "Content-Type",
                    response.headers.get("Content-Type", "application/json"),
                )
                self.send_header("Content-Length", str(len(upstream_body)))
                self.end_headers()
                self.wfile.write(upstream_body)
        except urllib.error.HTTPError as exc:
            detail = exc.read(4096).decode(errors="replace")
            self._reply(
                502,
                {
                    "error": "upstream_http_error",
                    "status": exc.code,
                    "detail": detail,
                },
            )
        except Exception as exc:
            self._reply(502, {"error": "upstream_unreachable", "detail": str(exc)})

    def do_GET(self) -> None:
        if self.path == "/health" and self.client_address[0] == ALLOWED_SOURCE:
            self._reply(200, {"status": "ok"})
            return
        self._reply(404, {"error": "not_found"})

    def log_message(self, format: str, *args) -> None:
        print(f"{self.client_address[0]} - {format % args}", flush=True)


if __name__ == "__main__":
    server = ThreadingHTTPServer((LISTEN_HOST, LISTEN_PORT), RelayHandler)
    print(
        f"listening on {LISTEN_HOST}:{LISTEN_PORT}; "
        f"allowed_source={ALLOWED_SOURCE}; upstream={UPSTREAM}",
        flush=True,
    )
    server.serve_forever()
