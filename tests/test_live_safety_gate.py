from __future__ import annotations

import hashlib
import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

from automation.orchestrator import playbook


class LiveSafetyGateTests(unittest.TestCase):
    def valid_preflight(self) -> dict:
        now = datetime.now(timezone.utc)
        return {
            "schema_version": "1.0.0",
            "scenario_id": "PT-2026-001",
            "target_role": "authorized lab endpoint",
            "authorized": True,
            "identity_verified": True,
            "dns_healthy": True,
            "time_synchronized": True,
            "storage_healthy": True,
            "telemetry_healthy": True,
            "rollback_snapshot_confirmed": True,
            "expected_telemetry": ["process creation telemetry"],
            "cleanup_steps": ["remove the benign validation marker"],
            "validated_at": now.isoformat().replace("+00:00", "Z"),
            "expires_at": (now + timedelta(minutes=30)).isoformat().replace("+00:00", "Z"),
        }

    def test_valid_preflight_is_accepted(self) -> None:
        doc = self.valid_preflight()
        playbook.validate_live_preflight(doc, "PT-2026-001")

    def test_mismatched_or_expired_preflight_fails_closed(self) -> None:
        mismatch = self.valid_preflight()
        with self.assertRaises(playbook.PlaybookError):
            playbook.validate_live_preflight(mismatch, "PT-2026-999")
        expired = self.valid_preflight()
        expired["expires_at"] = "2020-01-01T00:00:00Z"
        with self.assertRaises(playbook.PlaybookError):
            playbook.validate_live_preflight(expired, "PT-2026-001")

    def test_approval_token_requires_private_file_and_matching_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            token = Path(tmp) / "approval"
            token.write_text("approved-value\n", encoding="utf-8")
            token.chmod(0o600)
            expected = hashlib.sha256(b"approved-value").hexdigest()
            with mock.patch.dict(os.environ, {"PLAYBOOK_LIVE_APPROVAL_TOKEN_SHA256": expected}):
                playbook.verify_approval_token(token)
            token.chmod(0o644)
            with mock.patch.dict(os.environ, {"PLAYBOOK_LIVE_APPROVAL_TOKEN_SHA256": expected}):
                with self.assertRaises(playbook.PlaybookError):
                    playbook.verify_approval_token(token)


if __name__ == "__main__":
    unittest.main()
