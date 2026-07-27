from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "automation" / "build_powershell_lifecycle_pack.py"
MANIFEST = ROOT / "detections" / "packs" / "validated-powershell-lifecycle-v1" / "manifest.json"
SOURCE = ROOT / "detections" / "sigma" / "windows" / "process_creation" / "suspicious_powershell_execution.yml"


class PowershellLifecyclePackTests(unittest.TestCase):
    def test_builder_emits_deterministic_traceable_pack(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)

        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["pack_version"], "1.0.0")
        self.assertEqual(manifest["scenario_id"], "PT-2026-001")
        self.assertEqual(manifest["attack_techniques"], ["T1059.001", "T1027"])
        self.assertEqual(
            manifest["source"]["sha256"],
            hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        )
        self.assertEqual(len(manifest["fixtures"]["positive"]), 4)
        self.assertEqual(len(manifest["fixtures"]["negative"]), 5)
        self.assertEqual(
            {artifact["backend"] for artifact in manifest["generated_artifacts"]},
            {"splunk-official", "splunk-mayuri-live", "elastic-eql"},
        )
        for group in ("positive", "negative"):
            for fixture in manifest["fixtures"][group]:
                self.assertTrue((ROOT / fixture["path"]).is_file())
                self.assertRegex(fixture["sha256"], r"^[a-f0-9]{64}$")
        for artifact in manifest["generated_artifacts"]:
            self.assertTrue((ROOT / artifact["path"]).is_file())
            self.assertRegex(artifact["sha256"], r"^[a-f0-9]{64}$")

        serialized = MANIFEST.read_text(encoding="utf-8")
        for prohibited in ("10.10.10.", "mayuri.lab", "VICTIM-MAYURI", "webhook"):
            self.assertNotIn(prohibited, serialized)


if __name__ == "__main__":
    unittest.main()
