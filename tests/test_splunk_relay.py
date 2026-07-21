from __future__ import annotations

import os
import unittest
from unittest import mock

with mock.patch.dict(os.environ, {"RELAY_TOKEN": "expected"}, clear=False):
    from automation.relays import splunk_n8n_relay as relay


class SplunkRelaySecurityTests(unittest.TestCase):
    def test_public_defaults_are_loopback_and_non_environment_specific(self) -> None:
        self.assertEqual(relay.DEFAULT_LISTEN_HOST, "127.0.0.1")
        self.assertEqual(relay.DEFAULT_ALLOWED_SOURCE, "127.0.0.1")
        self.assertTrue(relay.DEFAULT_UPSTREAM.endswith(".invalid/webhook/splunk-alert-to-case"))

    def test_token_is_header_authenticated(self) -> None:
        self.assertTrue(relay.authorized("expected", "expected"))
        self.assertFalse(relay.authorized("expected", "wrong"))
        self.assertFalse(relay.authorized("", "anything"))

    def test_log_path_does_not_include_query_or_secret_components(self) -> None:
        self.assertEqual(relay.safe_log_path("/splunk-alert?token=secret"), "/splunk-alert")
        self.assertEqual(
            relay.safe_upstream_label("https://orchestrator.example.invalid/hook?token=secret"),
            "https://orchestrator.example.invalid/hook",
        )

    def test_upstream_rejects_non_http_and_embedded_credentials(self) -> None:
        with self.assertRaises(ValueError):
            relay.validate_upstream("file:///tmp/payload")
        with self.assertRaises(ValueError):
            relay.validate_upstream("https://user:secret@example.invalid/hook")
        self.assertEqual(
            relay.validate_upstream("https://example.invalid/hook"),
            "https://example.invalid/hook",
        )


if __name__ == "__main__":
    unittest.main()
