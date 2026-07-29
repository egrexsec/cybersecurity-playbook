from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCENARIO = ROOT / "purple-team/scenarios/PT-2026-012-service-execution/scenario.yaml"
RULE = ROOT / "detections/sigma/windows/process_creation/suspicious_service_execution.yml"
ATOMIC_GUID = "2382dee2-a75f-49aa-9378-f52df6ed3fb1"
SNAPSHOT = "pre-pt-2026-012-t1569-002-20260729"
RULE_ID = "d7bfcdf8-7f68-4bcb-8a21-11f2c00f9a12"


class PT2026012ContractTests(unittest.TestCase):
    def test_scenario_records_exact_atomic_and_rollback_snapshot(self) -> None:
        scenario = yaml.safe_load(SCENARIO.read_text(encoding="utf-8"))
        self.assertEqual(scenario["id"], "PT-2026-012")
        self.assertEqual(scenario["attack"]["technique_ids"], ["T1569.002"])
        self.assertIn(ATOMIC_GUID, scenario["attack"]["test_ids"])
        self.assertEqual(scenario["safety"]["required_snapshot_name"], SNAPSHOT)
        self.assertTrue(scenario["safety"]["cleanup_required"])
        self.assertEqual(scenario["targets"]["approved_hosts"], ["VICTIM-MAYURI"])

    def test_positive_original_invokes_exact_atomic_guid(self) -> None:
        script = (ROOT / "automation/execution/pt_2026_012_positive_atomic_service_execution.ps1").read_text(encoding="utf-8")
        self.assertIn("Invoke-AtomicTest T1569.002", script)
        self.assertIn(ATOMIC_GUID, script)
        self.assertIn("PT-2026-012-Original", script)

    def test_atomic_input_avoids_nested_quotes_and_writes_completion_record(self) -> None:
        script = (ROOT / "automation/execution/pt_2026_012_positive_atomic_service_execution.ps1").read_text(encoding="utf-8")
        self.assertNotIn('-Command "', script)
        self.assertIn("pt-2026-012-original-result.json", script)
        self.assertIn("ConvertTo-Json", script)
        self.assertIn("Set-Content -LiteralPath $resultPath", script)

    def test_cleanup_is_explicit_and_idempotent(self) -> None:
        script = (ROOT / "automation/execution/pt_2026_012_cleanup.ps1").read_text(encoding="utf-8")
        for service in ("PT-2026-012-Original", "PT-2026-012-Variant", "PT-2026-012-Benign"):
            self.assertIn(service, script)
        self.assertIn("sc.exe stop", script)
        self.assertIn("sc.exe delete", script)
        self.assertIn("Remove-Item", script)

    def test_detection_is_behavioral_service_parent_and_shell_child(self) -> None:
        rule = yaml.safe_load(RULE.read_text(encoding="utf-8"))
        self.assertEqual(rule["id"], RULE_ID)
        self.assertIn("attack.t1569.002", rule["tags"])
        serialized = json.dumps(rule["detection"])
        self.assertIn("\\\\services.exe", serialized)
        self.assertIn("\\\\cmd.exe", serialized)
        self.assertIn("\\\\powershell.exe", serialized)
        self.assertNotIn("PT-2026-012", serialized)
        self.assertNotIn("art-marker", serialized.lower())

    def test_fixture_contract_has_two_positive_and_three_negative_cases(self) -> None:
        root = ROOT / "tests/fixtures/T1569.002"
        positive = sorted((root / "positive").glob("*.json"))
        negative = sorted((root / "negative").glob("*.json"))
        self.assertEqual(len(positive), 2)
        self.assertEqual(len(negative), 3)
        for path, expected in [(p, True) for p in positive] + [(p, False) for p in negative]:
            fixture = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(fixture["rule_id"], RULE_ID)
            self.assertEqual(fixture["technique_id"], "T1569.002")
            self.assertEqual(fixture["scenario_id"], "PT-2026-012")
            self.assertIs(fixture["expected_match"], expected)


if __name__ == "__main__":
    unittest.main()
