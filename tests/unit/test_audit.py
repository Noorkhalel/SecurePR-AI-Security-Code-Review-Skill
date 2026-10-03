"""Adversarial release audit regressions; no target code execution."""
import copy
import contextlib
import difflib
import random
import io
import json
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
s = load('audit_securepr', 'scripts/securepr.py')
e = load('audit_evaluate', 'tools/evaluate.py')
p = load('audit_packet', 'tools/prepare_eval.py')

class AuditRuntime(unittest.TestCase):
    def test_surrogate_path_rejected(self):
        with self.assertRaises(s.Rejected): s.relpath('\ud800.js')

    def test_embedded_carriage_return_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, 'a.js').write_bytes(b'left\r\r\nright\n')
            with s.SafeTree(directory) as tree:
                self.assertEqual(s.excerpt(tree, 'a.js', 1, 1)['quote'], 'left\\u000d')

    def test_final_carriage_return_is_data(self):
        self.assertEqual(s.safe_quote('left\r'), 'left\\u000d')
        self.assertEqual(s.safe_quote('left\r\n'), 'left')

    def test_common_unquoted_credentials_redacted(self):
        for line in ['api_key: SYNTHETIC_ONLY', 'Authorization: Bearer SYNTHETIC_ONLY']:
            self.assertIn('REDACTED', s.safe_quote(line))

    def test_excessive_coordinates_rejected(self):
        patch = '--- a/a.js\n+++ b/a.js\n@@ -' + '9'*5000 + ' +1 @@\n-a\n+b\n'
        with self.assertRaises(s.Rejected): s.parse_diff(patch.encode())

    def test_cli_rejects_huge_coordinate_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            patch = Path(directory, 'change.diff')
            patch.write_text('--- a/a.js\n+++ b/a.js\n@@ -' + '9'*5000 + ' +1 @@\n-a\n+b\n')
            output = io.StringIO()
            with contextlib.redirect_stderr(output):
                self.assertEqual(s.main(['diff', str(patch)]), 2)
            self.assertEqual(json.loads(output.getvalue()), {'error': 'invalid hunk coordinates'})

    def test_inconsistent_offsets_rejected(self):
        for body in ['@@ -1 +100 @@\n-a\n+b\n',
                     '@@ -1 +1,2 @@\n-a\n+b\n+c\n@@ -5 +5 @@\n-d\n+e\n',
                     '@@ -1,0 +1,0 @@\n', '@@ -1 +1 @@\n a\n']:
            with self.subTest(body=body), self.assertRaises(s.Rejected):
                s.parse_diff(('--- a/a.js\n+++ b/a.js\n'+body).encode())

    def test_valid_zero_context_offsets(self):
        for body in ['@@ -0,0 +1 @@\n+b\n', '@@ -3,0 +4 @@\n+b\n',
                     '@@ -4 +3,0 @@\n-a\n',
                     '@@ -1 +1,2 @@\n-a\n+b\n+c\n@@ -5 +6 @@\n-d\n+e\n']:
            with self.subTest(body=body):
                self.assertTrue(s.parse_diff(('--- a/a.js\n+++ b/a.js\n'+body).encode())['files'])

    def test_mismatched_git_header_rejected(self):
        patch = b'diff --git a/other.js b/other.js\n--- a/a.js\n+++ b/a.js\n@@ -1 +1 @@\n-a\n+b\n'
        with self.assertRaises(s.Rejected): s.parse_diff(patch)

    def test_malformed_metadata_rejected(self):
        patch = b'diff --git a/a.js b/a.js\nindex fabricated\n--- a/a.js\n+++ b/a.js\n@@ -1 +1 @@\n-a\n+b\n'
        with self.assertRaises(s.Rejected): s.parse_diff(patch)

    def test_generated_valid_diff_coordinates(self):
        rng = random.Random(1729)
        for index in range(150):
            old = [f'row-{i}\n' for i in range(rng.randrange(0, 20))]
            new = old.copy()
            for _ in range(rng.randrange(1, 6)):
                at = rng.randrange(len(new) + 1)
                new[at:at + rng.randrange(0, 3)] = [f'changed-{index}-{at}\n'] * rng.randrange(0, 3)
            patch = ''.join(difflib.unified_diff(old, new, 'a/a.js', 'b/a.js', n=rng.randrange(0, 4)))
            parsed = s.parse_diff(patch.encode())
            if old != new:
                hunks = parsed['files'][0]['hunks']
                observed_add = [line for h in hunks for line in h['added_lines']]
                observed_remove = [line for h in hunks for line in h['removed_lines']]
                expected_add, expected_remove = [], []
                for tag, a, b, c, d in difflib.SequenceMatcher(None, old, new).get_opcodes():
                    if tag in ('replace', 'delete'): expected_remove.extend(range(a + 1, b + 1))
                    if tag in ('replace', 'insert'): expected_add.extend(range(c + 1, d + 1))
                self.assertEqual(observed_add, expected_add)
                self.assertEqual(observed_remove, expected_remove)

class AuditScoring(unittest.TestCase):
    def setup_pair(self):
        manifest = {'version':'1.0.0','cases':[{'id':'x','mode':'full','manual_review_required':False,
            'expected':[{'cwe':'CWE-89','file':'a.js','line':3}, {'cwe':'CWE-89','file':'a.js','line':6}]}]}
        finding = {'cwe':'CWE-89','file':'a.js','line':4,'confidence':'CONFIRMED',
            'reason':'binding missing','source':'request query','sink':'SQL query','remediation':'bind value'}
        second = dict(finding, line=2)
        observations = {'run':dict(id='unit',kind='harness-self-test',reviewer='unit',skill_revision='test',date='2026-10-03',notes='Scorer test only'),
            'cases':[{'id':'x','findings':[finding,second],'manual_review':[],'recommendation':None}]}
        return manifest, observations

    def test_matching_is_order_independent(self):
        manifest, observations = self.setup_pair()
        one = e.score(manifest, observations)
        observations['cases'][0]['findings'].reverse()
        two = e.score(manifest, observations)
        self.assertEqual(one['true_positives'], 2)
        self.assertEqual(one['true_positives'], two['true_positives'])

    def test_duplicate_gold_rejected(self):
        manifest, observations = self.setup_pair()
        manifest['cases'][0]['expected'][1] = copy.deepcopy(manifest['cases'][0]['expected'][0])
        with self.assertRaises(e.securepr.Rejected): e.score(manifest, observations)

    def test_noise_and_contradictory_recommendation_visible(self):
        manifest, observations = self.setup_pair()
        manifest['cases'][0].update(mode='pr', expected=[])
        observations['cases'][0].update(findings=[],manual_review=['unnecessary suspicion'],recommendation=s.RECOMMENDATIONS[0])
        result = e.score(manifest, observations)
        self.assertEqual(result['safe_manual_review_cases'], 1)
        self.assertEqual(result['recommendation_conflicts'], 1)

    def test_strict_exit_status(self):
        manifest, observations = self.setup_pair()
        with tempfile.TemporaryDirectory() as directory:
            gold, observed = Path(directory, 'manifest.json'), Path(directory, 'observed.json')
            gold.write_text(json.dumps(manifest))
            observed.write_text(json.dumps(observations))
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(e.main([str(observed), '--manifest', str(gold), '--strict']), 0)
            observations['cases'][0]['findings'] = []
            observed.write_text(json.dumps(observations))
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(e.main([str(observed), '--manifest', str(gold)]), 0)
                self.assertEqual(e.main([str(observed), '--manifest', str(gold), '--strict']), 1)

class AuditPacket(unittest.TestCase):
    def test_custom_manifest_answer_free_packet(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory, 'installed')
            root.mkdir()
            (root / 'scripts').mkdir()
            (root / 'scripts/securepr.py').write_text('# trusted helper')
            (root / 'SKILL.md').write_text('trusted skill')
            (root / 'fixtures').mkdir()
            (root / 'fixtures/app.js').write_text('const x = 1;')
            manifest = {'cases': [{'id': 'case-101', 'mode': 'snippet',
                'path': 'fixtures', 'files': ['app.js'], 'expected': ['ANSWER_MARKER']}]}
            (root / 'custom.json').write_text(json.dumps(manifest))
            original = p.ROOT
            try:
                p.ROOT = root
                dest = Path(directory, 'packet')
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(p.main([str(dest), '--manifest', 'custom.json']), 0)
                self.assertEqual((dest / 'cases/case-101/app.js').read_text(), 'const x = 1;')
                self.assertTrue((dest / 'skill/scripts/securepr.py').is_file())
                self.assertFalse((dest / 'custom.json').exists())
                self.assertNotIn('ANSWER_MARKER', (dest / 'cases.json').read_text())
            finally:
                p.ROOT = original
