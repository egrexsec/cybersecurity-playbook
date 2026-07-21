#!/usr/bin/env python3
from __future__ import annotations

import json
import hmac
import os
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

DEFAULT_LISTEN_HOST = "127.0.0.1"
DEFAULT_ALLOWED_SOURCE = "127.0.0.1"
DEFAULT_UPSTREAM = "https://orchestrator.example.invalid/webhook/splunk-alert-to-case"
LISTEN_HOST = os.environ.get("RELAY_LISTEN_HOST", DEFAULT_LISTEN_HOST)
LISTEN_PORT = int(os.environ.get("RELAY_LISTEN_PORT", "8766"))
ALLOWED_SOURCE = os.environ.get("RELAY_ALLOWED_SOURCE", DEFAULT_ALLOWED_SOURCE)
TOKEN = os.environ.get("RELAY_TOKEN", "")
MAX_BODY = min(int(os.environ.get("RELAY_MAX_BODY_BYTES", "262144")), 1048576)


def authorized(expected: str, provided: str | None) -> bool:
    return bool(expected and provided and hmac.compare_digest(expected, provided))


def safe_log_path(value: str) -> str:
    return urlsplit(value).path


def validate_upstream(value: str) -> str:
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("RELAY_UPSTREAM must be an absolute HTTP(S) URL")
    if parsed.username or parsed.password:
        raise ValueError("RELAY_UPSTREAM must not contain user information")
    return value


def safe_upstream_label(value: str) -> str:
    parsed = urlsplit(value)
    host = parsed.hostname or "invalid"
    port = f":{parsed.port}" if parsed.port else ""
    return f"{parsed.scheme}://{host}{port}{parsed.path}"


UPSTREAM = validate_upstream(os.environ.get("RELAY_UPSTREAM", DEFAULT_UPSTREAM))


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
        if safe_log_path(self.path) != "/splunk-alert":
            self._reply(404, {"error": "not_found"})
            return
        if not authorized(TOKEN, self.headers.get("X-Relay-Token")):
            self._reply(403, {"error": "forbidden"})
            return
        if self.headers.get_content_type() != "application/json":
            self._reply(415, {"error": "json_content_type_required"})
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
                "User-Agent": "security-playbook-splunk-relay/2.0",
            },
            method="POST",
        )
        try:
            # UPSTREAM is validated at startup as an absolute HTTP(S) URL without userinfo.
            with urllib.request.urlopen(request, timeout=30) as response:  # nosec B310
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
            self._reply(
                502,
                {
                    "error": "upstream_http_error",
                    "status": exc.code,
                },
            )
        except Exception:
            self._reply(502, {"error": "upstream_unreachable"})

    def do_GET(self) -> None:
        if self.path == "/health" and self.client_address[0] == ALLOWED_SOURCE:
            self._reply(200, {"status": "ok"})
            return
        self._reply(404, {"error": "not_found"})

    def log_message(self, format: str, *args) -> None:
        print(f"{self.client_address[0]} - {self.command} {safe_log_path(self.path)}", flush=True)


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("RELAY_TOKEN must be set")
    server = ThreadingHTTPServer((LISTEN_HOST, LISTEN_PORT), RelayHandler)
    print(
        f"listening on {LISTEN_HOST}:{LISTEN_PORT}; "
        f"allowed_source={ALLOWED_SOURCE}; upstream={safe_upstream_label(UPSTREAM)}",
        flush=True,
    )
    server.serve_forever()
