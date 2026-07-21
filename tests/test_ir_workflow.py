from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

from automation.controller import ir_ops


SAMPLE_ALERT = {
    "alert_name": "Suspicious PowerShell Execution",
    "alert_id": "splunk-alert-fixture-001",
    "rule_id": "DET-2026-001",
    "severity": "high",
    "host": "AUTHORIZED-ENDPOINT",
    "user": "LAB\\analyst",
    "process": "powershell.exe",
    "parent_process": "winword.exe",
    "command_line": "powershell.exe -EncodedCommand SAFE_FIXTURE",
    "event_time": "2026-07-20T12:00:00Z",
    "technique_id": "T1059.001",
    "event_id": "1",
    "splunk_index": "fixture-index",
    "splunk_sourcetype": "fixture-sourcetype",
    "search_reference": "fixture://saved-search/powershell",
    "indicators": [{"type": "domain", "value": "indicator.example.invalid"}],
}


class IRWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.cases = self.root / "cases"
        self.manifests = self.root / "manifests"
        self.audit = self.root / "audit.jsonl"
        self.alert = self.root / "alert.json"
        self.alert.write_text(json.dumps(SAMPLE_ALERT), encoding="utf-8")
        self.assets = self.root / "assets.yaml"
        self.assets.write_text(
            yaml.safe_dump(
                {
                    "assets": [
                        {
                            "id": "LAB-ENDPOINT",
                            "name": "AUTHORIZED-ENDPOINT",
                            "role": "authorized-lab-endpoint",
                            "network": "approved-management-segment",
                            "approved_target": True,
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        self.patches = [
            mock.patch.object(ir_ops, "CASES", self.cases),
            mock.patch.object(ir_ops, "EVIDENCE_MANIFESTS", self.manifests),
            mock.patch.object(ir_ops, "AUDIT_LOG", self.audit),
            mock.patch.object(ir_ops, "ASSETS", self.assets),
        ]
        for patcher in self.patches:
            patcher.start()
            self.addCleanup(patcher.stop)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_duplicate_alert_reuses_deterministic_case(self) -> None:
        first = ir_ops.create_case_from_alert(str(self.alert))
        second = ir_ops.create_case_from_alert(str(self.alert))

        self.assertEqual(first["id"], second["id"])
        self.assertRegex(first["id"], r"^IR-2026-[A-F0-9]{12}$")
        self.assertEqual(second["intake"]["duplicate_count"], 1)
        self.assertEqual(len(list(self.cases.iterdir())), 1)

    def test_dry_run_does_not_create_case_or_audit_log(self) -> None:
        result = ir_ops.create_case_from_alert(str(self.alert), dry_run=True)

        self.assertEqual(result["operation"], "create")
        self.assertTrue(result["dry_run"])
        self.assertFalse(self.cases.exists())
        self.assertFalse(self.audit.exists())

    def test_cti_enrichment_fails_open_with_structured_status(self) -> None:
        case = ir_ops.create_case_from_alert(str(self.alert))

        seen: list[tuple[str, float]] = []

        def unavailable(indicator: str, timeout: float) -> dict:
            seen.append((indicator, timeout))
            raise TimeoutError("provider deadline exceeded")

        result = ir_ops.enrich_case(case["id"], cti_lookup=unavailable, cti_timeout=0.01)

        cti = result["cti"]
        self.assertEqual(seen, [("indicator.example.invalid", 0.01)])
        self.assertEqual(cti["lookup_status"], "error")
        self.assertTrue(cti["timeout_status"])
        self.assertEqual(cti["errors"], ["provider-timeout"])
        self.assertEqual(cti["confidence"], "unknown")
        self.assertIn("timestamp", cti)
        self.assertTrue(ir_ops.load_case(case["id"])["automation"]["enrichment_complete"])

    def test_planned_collection_is_not_claimed_as_completed(self) -> None:
        case = ir_ops.create_case_from_alert(str(self.alert))
        collection = ir_ops.collect_case(case["id"])

        self.assertEqual(collection["status"], "planned")
        self.assertFalse(ir_ops.load_case(case["id"])["automation"]["collection_complete"])
        self.assertEqual(collection["artifacts"][0]["status"], "not-collected")

    def test_fixture_collection_hashes_artifacts_and_marks_fixture_only(self) -> None:
        case = ir_ops.create_case_from_alert(str(self.alert))
        fixture = self.root / "fixture.evtx.txt"
        fixture.write_text("safe synthetic event fixture", encoding="utf-8")

        collection = ir_ops.collect_case(case["id"], fixture_paths=[fixture])

        self.assertEqual(collection["status"], "fixture-collected")
        self.assertEqual(collection["evidence_class"], "fixture")
        self.assertEqual(collection["artifacts"][0]["status"], "collected")
        self.assertEqual(len(collection["artifacts"][0]["sha256"]), 64)
        self.assertFalse(ir_ops.load_case(case["id"])["automation"]["collection_complete"])

    def test_fixture_workflow_reaches_sanitized_report_without_live_claims(self) -> None:
        case = ir_ops.create_case_from_alert(str(self.alert))
        ir_ops.enrich_case(case["id"])
        fixture = self.root / "synthetic-events.jsonl"
        fixture.write_text('{"event":"synthetic"}\n', encoding="utf-8")
        collection = ir_ops.collect_case(case["id"], fixture_paths=[fixture])
        hunt = ir_ops.hunt_case(case["id"])
        timeline = ir_ops.build_timeline(case["id"])
        findings = ir_ops.analyze_case(case["id"])
        report = ir_ops.report_case(case["id"])

        state = ir_ops.load_case(case["id"])
        self.assertEqual(collection["status"], "fixture-collected")
        self.assertEqual(hunt["execution_status"], "not-executed")
        self.assertEqual(hunt["result_count"], 0)
        self.assertEqual(state["automation"]["hunting_status"], "planned")
        self.assertFalse(state["automation"]["hunting_complete"])
        self.assertEqual(len(timeline), 2)
        self.assertEqual(findings["confidence"], "low")
        self.assertTrue((self.cases / case["id"] / "investigation.md").exists())
        self.assertEqual(report["case_id"], case["id"])
        self.assertIn("No current endpoint or SIEM state was verified", findings["executive_summary"])

    def test_cleanup_dry_run_preserves_files_then_cleanup_resets_derived_outputs(self) -> None:
        case = ir_ops.create_case_from_alert(str(self.alert))
        ir_ops.enrich_case(case["id"])
        case_path = self.cases / case["id"]
        self.assertNotEqual(json.loads((case_path / "enrichment.json").read_text()), {})

        preview = ir_ops.cleanup_case(case["id"], dry_run=True)
        self.assertTrue(preview["dry_run"])
        self.assertNotEqual(json.loads((case_path / "enrichment.json").read_text()), {})

        result = ir_ops.cleanup_case(case["id"])
        self.assertEqual(result["status"], "cleaned")
        self.assertEqual(json.loads((case_path / "enrichment.json").read_text()), {})
        self.assertTrue((case_path / "alert.json").exists())
        self.assertFalse(ir_ops.load_case(case["id"])["automation"]["enrichment_complete"])

    def test_audit_log_records_mutating_steps_without_sensitive_payloads(self) -> None:
        case = ir_ops.create_case_from_alert(str(self.alert))
        ir_ops.enrich_case(case["id"])

        events = [json.loads(line) for line in self.audit.read_text().splitlines()]
        self.assertEqual([event["operation"] for event in events], ["ir.create", "ir.enrich"])
        self.assertTrue(all("command_line" not in event for event in events))
        self.assertTrue(all(event["case_id"] == case["id"] for event in events))


if __name__ == "__main__":
    unittest.main()
