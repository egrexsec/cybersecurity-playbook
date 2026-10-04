import json, unittest
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
class DetectionCycle1ContractTests(unittest.TestCase):
 def test_exact_atomic_guids_and_public_scope(self):
  expected={'PT-2026-014-powershell-ingress-transfer':('T1105','42dc4460-9aa6-45d3-b1a6-3955d34e1fe8'),'PT-2026-015-mshta-proxy-execution':('T1218.005','8707a805-2b76-4f32-b1c0-14e558205772')}
  for d,(tech,guid) in expected.items():
   s=yaml.safe_load((ROOT/'purple-team/scenarios'/d/'scenario.yaml').read_text())
   self.assertEqual(s['attack']['technique_ids'],[tech]);self.assertEqual(s['attack']['test_ids'],[guid]);self.assertEqual(s['targets']['approved_hosts'],['approved-windows-victim']);self.assertEqual(s['safety']['required_snapshot_name'],'private-rollback-reference')
 def test_scripts_pin_only_approved_guids(self):
  a=(ROOT/'automation/execution/pt_2026_014_positive_atomic_webclient.ps1').read_text();m=(ROOT/'automation/execution/pt_2026_015_positive_atomic_mshta.ps1').read_text()
  self.assertIn('42dc4460-9aa6-45d3-b1a6-3955d34e1fe8',a);self.assertIn('8707a805-2b76-4f32-b1c0-14e558205772',m);self.assertIn('-TestGuids',a);self.assertIn('PreventiveEvents',m)
 def test_fixture_contract(self):
  for tech,sc,rid in [('T1105','PT-2026-014','4f18fcd8-8a39-4aa2-a71d-9b247d3ea475'),('T1218.005','PT-2026-015','8b36d6e2-16e6-4ae2-b86a-d396aac273c1')]:
   root=ROOT/'tests/fixtures'/tech;pos=list((root/'positive').glob('*.json'));neg=list((root/'negative').glob('*.json'));self.assertEqual(len(pos),2);self.assertEqual(len(neg),3)
   for p,e in [(x,True) for x in pos]+[(x,False) for x in neg]:
    f=json.loads(p.read_text());self.assertEqual((f['scenario_id'],f['rule_id'],f['technique_id']),(sc,rid,tech));self.assertIs(f['expected_match'],e)
 def test_campaign_contract_is_bounded_and_ordered(self):
  c=yaml.safe_load((ROOT/'purple-team/campaigns/CAMPAIGN-2026-001.yaml').read_text())
  self.assertEqual(c['scenario_ids'],['PT-2026-014','PT-2026-015'])
  self.assertEqual([s['order'] for s in c['sequence']],[1,2,3])
  self.assertEqual([s['technique_id'] for s in c['sequence']],['T1105','T1218.005','T1059.001'])
  self.assertTrue(c['safety']['loopback_only']);self.assertTrue(c['safety']['benign_content_only'])
  for key in ('external_c2','credential_access','lateral_movement','persistence','destructive_actions'):
   self.assertFalse(c['safety'][key])
  self.assertTrue(c['cleanup']['first_pass_clean']);self.assertTrue(c['cleanup']['idempotent_recheck_clean'])
 def test_cleanup_removes_roots_and_reports_clean(self):
  for n in ('014','015'):
   t=(ROOT/f'automation/execution/pt_2026_{n}_cleanup.ps1').read_text();self.assertIn('Remove-Item $root -Recurse -Force',t);self.assertIn('Clean=',t)
  mshta=(ROOT/'automation/execution/pt_2026_015_cleanup.ps1').read_text();campaign=(ROOT/'automation/execution/campaign_2026_001_cleanup.ps1').read_text()
  for t in (mshta,campaign):
   self.assertIn('process-ids',t);self.assertIn('Stop-Process -Id',t);self.assertNotIn('Get-Process mshta',t)
 def test_cycle_excludes_active_iocs_and_internal_ids(self):
  roots=[ROOT/'README.md',ROOT/'docs/current-state/DETECTION_CYCLE_1.md',ROOT/'docs/current-state/DETECTION_CYCLE_1_COVERAGE.md',ROOT/'docs/current-state/DETECTION_PLATFORM_READINESS.md',ROOT/'docs/current-state/PROJECT_TIMELINE_ASSESSMENT.md',ROOT/'docs/current-state/PURPLE_TEAM_PROGRAM_STATUS.md',ROOT/'automation/execution',ROOT/'purple-team/campaigns',ROOT/'purple-team/scenarios/PT-2026-014-powershell-ingress-transfer',ROOT/'purple-team/scenarios/PT-2026-015-mshta-proxy-execution',ROOT/'threat-hunting/hypotheses',ROOT/'detections/sigma/windows/process_creation/suspicious_mshta_child_process.yml',ROOT/'detections/sigma/windows/ps_script/suspicious_powershell_web_download.yml',ROOT/'detections/generated',ROOT/'detections/validation/live',ROOT/'detections/validation/mshta-child-process.md',ROOT/'detections/validation/powershell-web-ingress-transfer.md',ROOT/'tests/fixtures/T1105',ROOT/'tests/fixtures/T1218.005',ROOT/'evidence/sanitized/CAMPAIGN-2026-001',ROOT/'evidence/sanitized/PT-2026-014',ROOT/'evidence/sanitized/PT-2026-015',ROOT/'investigations/endpoint/DFIR-2026-014',ROOT/'investigations/endpoint/DFIR-2026-015',ROOT/'investigations/endpoint/DFIR-2026-016']
  paths=[]
  for root in roots:
   if root.is_file(): paths.append(root)
   elif root.is_dir(): paths.extend(p for p in root.rglob('*') if p.is_file() and p.suffix in ('.md','.yaml','.yml','.json','.ps1'))
  text='\n'.join(p.read_text() for p in paths)
  self.assertNotRegex(text,r'(?<![\d.])(?:10\.(?:\d{1,3}\.){2}\d{1,3}|192\.168\.(?:\d{1,3}\.)\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})(?![\d.])')
  self.assertNotRegex(text,r'/(?:root|home)/')
  self.assertNotRegex(text,r'(?i)\b(?:ssh|scp)\s+[^\s]+@')
  self.assertNotRegex(text,r'(?i)\bqm\s+(?:guest|snapshot|status)\b')
if __name__=='__main__': unittest.main()
