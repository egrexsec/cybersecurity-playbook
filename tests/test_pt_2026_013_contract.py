from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCENARIO = ROOT / "purple-team/scenarios/PT-2026-013-wmi-event-subscription/scenario.yaml"
RULE = ROOT / "detections/sigma/windows/wmi_event/suspicious_permanent_wmi_subscription.yml"
ATOMIC_GUID = "3c64f177-28e2-49eb-a799-d767b24dd1e0"
SNAPSHOT = "private-rollback-reference"
RULE_ID = "45742e29-7c43-4a65-bd91-b04fa7a8d9dc"


class PT2026013ContractTests(unittest.TestCase):
    def test_scenario_records_exact_atomic_and_rollback_snapshot(self) -> None:
        scenario = yaml.safe_load(SCENARIO.read_text(encoding="utf-8"))
        self.assertEqual(scenario["id"], "PT-2026-013")
        self.assertEqual(scenario["attack"]["technique_ids"], ["T1546.003"])
        self.assertEqual(scenario["attack"]["test_ids"], [ATOMIC_GUID])
        self.assertEqual(scenario["safety"]["required_snapshot_name"], SNAPSHOT)
        self.assertTrue(scenario["safety"]["cleanup_required"])
        self.assertEqual(scenario["targets"]["approved_hosts"], ["approved-windows-victim"])
        self.assertIn("ActiveScriptEventConsumer", scenario["safety"]["excluded_tests"])
        self.assertIn("MOFComp", scenario["safety"]["excluded_tests"])

    def test_positive_original_invokes_only_exact_atomic_guid(self) -> None:
        script = (ROOT / "automation/execution/pt_2026_013_positive_atomic_wmi_subscription.ps1").read_text(encoding="utf-8")
        self.assertIn("Invoke-AtomicTest T1546.003", script)
        self.assertIn(ATOMIC_GUID, script)
        self.assertIn("-TestGuids $testGuid", script)
        self.assertNotIn("-TestNumbers 2", script)
        self.assertNotIn("mofcomp", script.lower())

    def test_variant_is_local_non_triggering_and_cleanup_is_explicit(self) -> None:
        original = (ROOT / "automation/execution/pt_2026_013_positive_atomic_wmi_subscription.ps1").read_text(encoding="utf-8")
        variant = (ROOT / "automation/execution/pt_2026_013_positive_variant_wmi_subscription.ps1").read_text(encoding="utf-8")
        self.assertIn("CommandLineEventConsumer", variant)
        self.assertIn("SystemUpTime > 99999999", variant)
        self.assertNotIn("Invoke-WebRequest", variant)
        self.assertIn("pt-2026-013-original-completion.json", original)
        self.assertIn("pt-2026-013-variant-completion.json", variant)
        self.assertIn("ConvertTo-Json", original)
        self.assertIn("ConvertTo-Json", variant)
        self.assertIn("AddSeconds(30)", original)
        self.assertIn("AddSeconds(30)", variant)
        self.assertIn("REFERENCES OF", original)
        self.assertIn("REFERENCES OF", variant)
        cleanup = (ROOT / "automation/execution/pt_2026_013_cleanup.ps1").read_text(encoding="utf-8")
        for name in ("AtomicRedTeam-WMIPersistence-CommandLineEventConsumer-Example", "PT-2026-013-Variant"):
            self.assertIn(name, cleanup)
        self.assertIn("__FilterToConsumerBinding", cleanup)
        self.assertIn("CommandLineEventConsumer", cleanup)
        self.assertIn("__EventFilter", cleanup)
        self.assertIn("pt-2026-013-original-completion.json", cleanup)
        self.assertIn("pt-2026-013-variant-completion.json", cleanup)
        self.assertIn("REFERENCES OF", cleanup)
        self.assertIn("Remove-WmiObject", cleanup)
        self.assertIn("Get-NamedBindings", cleanup)
        self.assertNotIn('"$($_.Filter)" -like', cleanup)
        self.assertNotIn('"$($_.Consumer)" -like', cleanup)
        binding_delete = cleanup.index("@(Get-NamedBindings -ObjectName $name) | Remove-WmiObject")
        binding_recheck = cleanup.index("$remainingBindings = @(Get-NamedBindings -ObjectName $name)")
        endpoint_gate = cleanup.index("if ($remainingBindings.Count -eq 0)")
        consumer_delete = cleanup.index(
            "@(Get-WmiObject -Namespace $namespace -Class CommandLineEventConsumer",
            endpoint_gate,
        )
        self.assertLess(binding_delete, binding_recheck)
        self.assertLess(binding_recheck, endpoint_gate)
        self.assertLess(endpoint_gate, consumer_delete)

    def test_detection_is_behavioral_and_not_scenario_coupled(self) -> None:
        rule = yaml.safe_load(RULE.read_text(encoding="utf-8"))
        self.assertEqual(rule["id"], RULE_ID)
        self.assertEqual(rule["logsource"]["category"], "wmi_event")
        self.assertIn("attack.t1546.003", rule["tags"])
        serialized = json.dumps(rule["detection"])
        for event_type in ("WmiFilterEvent", "WmiConsumerEvent", "WmiBindingEvent"):
            self.assertIn(event_type, serialized)
        self.assertIn("Created", serialized)
        self.assertNotIn("PT-2026-013", serialized)
        self.assertNotIn("AtomicRedTeam", serialized)

    def test_live_spl_generator_supports_wmi_event_fields(self) -> None:
        from automation.validators import sigma_ops

        self.assertIn("wmi_event", sigma_ops.BASE_SEARCH)
        self.assertIn("EventType", sigma_ops.FIELD_RAW_MAP)
        self.assertIn("Operation", sigma_ops.FIELD_RAW_MAP)

    def test_fixture_contract_has_two_positive_and_three_negative_cases(self) -> None:
        root = ROOT / "tests/fixtures/T1546.003"
        positive = sorted((root / "positive").glob("*.json"))
        negative = sorted((root / "negative").glob("*.json"))
        self.assertEqual(len(positive), 2)
        self.assertEqual(len(negative), 3)
        for path, expected in [(p, True) for p in positive] + [(p, False) for p in negative]:
            fixture = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(fixture["rule_id"], RULE_ID)
            self.assertEqual(fixture["technique_id"], "T1546.003")
            self.assertEqual(fixture["scenario_id"], "PT-2026-013")
            self.assertIs(fixture["expected_match"], expected)


if __name__ == "__main__":
    unittest.main()
