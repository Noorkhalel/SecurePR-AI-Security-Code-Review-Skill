"""Defensive helper tests using synthetic files; never execute corpus source."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('securepr_test', ROOT / 'scripts/securepr.py')
s = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(s)


def report_for(tree, mode='full'):
    ev=s.excerpt(tree,'app.js',1,1);ev.pop('notice')
    finding={'id':'HIGH-01','title':'Unsafe catalog query','severity':'High',
             'severity_rationale':'Query syntax is caller-controlled.',
             'confidence':'CONFIRMED','confidence_rationale':'Complete static flow supplied.',
             'cwe':'CWE-89','owasp':'A05:2025 Injection','function':'search','evidence':[ev],
             'source':'req.query.term','data_flow':['req.query.term -> db.query'],
             'sink':'db.query','missing_control':'No parameter binding.',
             'controls_checked':['Complete handler; no guards or binding.'],
             'preconditions':['Public route; standard query driver.'],
             'attack_scenario':'Caller changes query syntax.','impact':'Unauthorized query results.',
             'remediation':'Bind the term as a query parameter.',
             'regression_test':'Verify literal text matching and valid search.',
             'context_required':[],'introduced_by':'Replaced binding with interpolation.' if mode=='pr' else None,'basis':'static'}
    return {'version':'1.0.0','mode':mode,'revision':'synthetic-working-tree','scope':['app.js'],
            'summary':'One statically evidenced issue.','findings':[finding],'manual_review':[],
            'coverage_gaps':[],'recommendation':s.RECOMMENDATIONS[2] if mode=='pr' else None}


class FileSafety(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        (self.root/'app.js').write_text('const value = 1;\n')
        self.tree=s.SafeTree(self.root)
    def tearDown(self):
        self.tree.__exit__();self.tmp.cleanup()
    def test_regular_read(self): self.assertEqual(self.tree.read('app.js'),b'const value = 1;\n')
    def test_path_rejections(self):
        for name in ['../x','a/../x','/etc/passwd','a//b','a/./b','C:\\x','a\x00b','a\nb','']:
            with self.subTest(name=name),self.assertRaises(s.Rejected): self.tree.read(name)
    def test_symlink_file(self):
        (self.root/'link.js').symlink_to(self.root/'app.js')
        with self.assertRaises(s.Rejected): self.tree.read('link.js')
    def test_symlink_directory(self):
        (self.root/'dir').symlink_to(self.root,target_is_directory=True)
        with self.assertRaises((s.Rejected,OSError)): self.tree.read('dir/app.js')
    def test_symlink_root(self):
        (self.root/'dir').symlink_to(self.root,target_is_directory=True)
        with self.assertRaises(s.Rejected): s.SafeTree(self.root/'dir')
    def test_hardlink(self):
        os.link(self.root/'app.js',self.root/'hard.js')
        with self.assertRaises(s.Rejected): self.tree.read('hard.js')
    def test_fifo(self):
        os.mkfifo(self.root/'pipe.js')
        with self.assertRaises(s.Rejected): self.tree.read('pipe.js')
    def test_directory_not_file(self):
        (self.root/'dir').mkdir()
        with self.assertRaises(s.Rejected): self.tree.read('dir')
    def test_secret_path_excluded(self):
        (self.root/'.env').write_text('SECRET=synthetic')
        with self.assertRaises(s.Rejected): self.tree.read('.env')
    def test_size_limit(self):
        with self.assertRaises(s.Rejected): self.tree.read('app.js',3)
    def test_changed_file_rejected(self):
        original=os.fstat;calls=[]
        def changing(fd):
            obj=original(fd);calls.append(1)
            if len(calls)==2:
                return mock.Mock(st_size=obj.st_size,st_mtime_ns=obj.st_mtime_ns+1,st_ctime_ns=obj.st_ctime_ns)
            return obj
        with mock.patch.object(s.os,'fstat',side_effect=changing),self.assertRaises(s.Rejected): self.tree.read('app.js')
    def test_inventory_no_code_execution(self):
        (self.root/'package.json').write_text('{"scripts":{"postinstall":"DO_NOT_EXECUTE"}}')
        inv=self.tree.inventory()
        self.assertEqual([x['path'] for x in inv['files']],['app.js','package.json'])
        self.assertFalse(inv['truncated'])
    def test_inventory_exclusions(self):
        (self.root/'node_modules').mkdir();(self.root/'node_modules'/'x.js').write_text('x')
        (self.root/'link').symlink_to('/etc')
        inv=self.tree.inventory()
        self.assertEqual(len(inv['files']),1)
        self.assertEqual(len(inv['omissions']),2)
    def test_inventory_entry_budget(self):
        for i in range(8): (self.root/f'f{i}.js').write_text('x')
        inv=self.tree.inventory(max_entries=3)
        self.assertTrue(inv['truncated']);self.assertEqual(len(inv['files']),3)
    def test_invalid_encoding(self):
        with self.assertRaises(s.Rejected): s.decode(b'\xff')
    def test_binary(self):
        with self.assertRaises(s.Rejected): s.decode(b'x\x00y')
    def test_line_budget(self):
        with self.assertRaises(s.Rejected): s.decode(b'x'*(s.MAX_LINE+1))
    def test_excerpt_range(self):
        for start,end in [(0,1),(2,1),(1,2),(1,202)]:
            with self.subTest(start=start,end=end),self.assertRaises(s.Rejected): s.excerpt(self.tree,'app.js',start,end)
    def test_excerpt_hash(self):
        actual=s.excerpt(self.tree,'app.js',1,1)
        self.assertEqual(actual['sha256'],s.digest((self.root/'app.js').read_bytes()))
    def test_credential_redaction(self):
        (self.root/'app.js').write_text("const signingSecret = 'SYNTHETIC_NOT_REAL';\n")
        self.assertNotIn('SYNTHETIC_NOT_REAL',s.excerpt(self.tree,'app.js',1,1)['quote'])
    def test_private_key_partial_excerpt(self):
        (self.root/'app.js').write_text('-----BEGIN PRIVATE KEY-----\nSYNTHETIC BODY\n-----END PRIVATE KEY-----\n')
        self.assertNotIn('SYNTHETIC BODY',s.excerpt(self.tree,'app.js',2,2)['quote'])
    def test_crlf(self):
        (self.root/'app.js').write_bytes(b'first\r\nsecond\r\n')
        self.assertEqual(s.excerpt(self.tree,'app.js',2,2)['quote'],'second')
    def test_control_character_does_not_shift_line(self):
        (self.root/'app.js').write_bytes(b'first\x1esecond\nthird\n')
        self.assertEqual(s.excerpt(self.tree,'app.js',2,2)['quote'],'third')
    def test_trailing_blank_excerpt(self):
        (self.root/'app.js').write_text('first\n\n')
        self.assertEqual(s.excerpt(self.tree,'app.js',2,2)['quote'],'')
    def test_json_duplicate(self):
        with self.assertRaises(s.Rejected): s.load_json(b'{"x":1,"x":2}')
    def test_json_nan(self):
        with self.assertRaises(s.Rejected): s.load_json(b'{"x":NaN}')
    def test_json_exponent_overflow(self):
        with self.assertRaises(s.Rejected): s.load_json(b'{"x":1e999}')
    def test_json_deep(self):
        with self.assertRaises(s.Rejected): s.load_json(b'['*2000+b'0'+b']'*2000)


class DiffSafety(unittest.TestCase):
    patch=b'--- a/app.js\n+++ b/app.js\n@@ -1,2 +1,2 @@\n keep\n-old\n+new\n'
    def test_valid(self):
        f=s.parse_diff(self.patch)['files'][0]
        self.assertEqual(f['hunks'][0]['added_lines'],[2]);self.assertEqual(f['hunks'][0]['removed_lines'],[2])
    def test_empty(self): self.assertEqual(s.parse_diff(b'')['files'],[])
    def test_new_file(self):
        self.assertIsNone(s.parse_diff(b'--- /dev/null\n+++ b/x.js\n@@ -0,0 +1 @@\n+x\n')['files'][0]['old_file'])
    def test_deleted(self):
        self.assertIsNone(s.parse_diff(b'--- a/x.js\n+++ /dev/null\n@@ -1 +0,0 @@\n-x\n')['files'][0]['new_file'])
    def test_truncation(self):
        with self.assertRaises(s.Rejected):s.parse_diff(self.patch.replace(b'+new\n',b''))
    def test_unsupported_binary(self):
        with self.assertRaises(s.Rejected):s.parse_diff(b'diff --git a/x b/x\nBinary files a/x and b/x differ\n')
    def test_traversal(self):
        with self.assertRaises(s.Rejected):s.parse_diff(self.patch.replace(b'a/app.js',b'a/../app.js'))
    def test_quoted_paths(self):
        with self.assertRaises(s.Rejected):s.parse_diff(self.patch.replace(b'a/app.js',b'"a/app.js"'))
    def test_overlapping(self):
        with self.assertRaises(s.Rejected):s.parse_diff(self.patch+b'@@ -1 +1 @@\n-x\n+y\n')
    def test_trailing_empty_metadata_change(self):
        with self.assertRaises(s.Rejected):s.parse_diff(self.patch+b'diff --git a/empty.js b/empty.js\nnew file mode 100644\nindex 0000000..e69de29\n')
    def test_control_bytes_not_new_hunk_line(self):
        with self.assertRaises(s.Rejected):s.parse_diff(b'--- a/x\n+++ b/x\n@@ -1,2 +1,2 @@\n first\x1e second\n')
    def test_null_header_coordinate_consistency(self):
        with self.assertRaises(s.Rejected):s.parse_diff(b'--- /dev/null\n+++ b/x\n@@ -1 +1 @@\n-x\n+y\n')


class ReportSafety(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        (self.root/'app.js').write_text('return db.query(req.query.term);\n')
        self.tree=s.SafeTree(self.root);self.report=report_for(self.tree)
    def tearDown(self):self.tree.__exit__();self.tmp.cleanup()
    def test_valid(self): self.assertTrue(s.validate_report(self.tree,self.report)['valid'])
    def test_fabricated_line(self):
        self.report['findings'][0]['evidence'][0]['line_start']=900
        with self.assertRaises(s.Rejected):s.validate_report(self.tree,self.report)
    def test_fabricated_quote(self):
        self.report['findings'][0]['evidence'][0]['quote']='invented'
        with self.assertRaises(s.Rejected):s.validate_report(self.tree,self.report)
    def test_stale_hash(self):
        (self.root/'app.js').write_text('changed\n')
        with self.assertRaises(s.Rejected):s.validate_report(self.tree,self.report)
    def test_scope_escape(self):
        self.report['findings'][0]['evidence'][0]['file']='elsewhere.js'
        with self.assertRaises(s.Rejected):s.validate_report(self.tree,self.report)
    def test_boolean_line(self):
        self.report['findings'][0]['evidence'][0]['line_start']=True
        with self.assertRaises(s.Rejected):s.validate_report(self.tree,self.report)
    def test_confirmed_unknown_context(self):
        self.report['findings'][0]['context_required']=['unknown guard']
        with self.assertRaises(s.Rejected):s.validate_report(self.tree,self.report)
    def test_high_missing_premise(self):
        self.report['findings'][0]['confidence']='HIGH CONFIDENCE'
        with self.assertRaises(s.Rejected):s.validate_report(self.tree,self.report)
    def test_medium_in_findings(self):
        self.report['findings'][0]['confidence']='MEDIUM CONFIDENCE'
        with self.assertRaises(s.Rejected):s.validate_report(self.tree,self.report)
    def test_duplicate_ids(self):
        self.report['findings'].append(copy.deepcopy(self.report['findings'][0]))
        with self.assertRaises(s.Rejected):s.validate_report(self.tree,self.report)
    def test_unknown_field(self):
        self.report['shell_command']='do not run'
        with self.assertRaises(s.Rejected):s.validate_report(self.tree,self.report)
    def test_malformed_mode(self):
        self.report['mode']=[]
        with self.assertRaises(s.Rejected):s.validate_report(self.tree,self.report)
    def test_pr_contradiction(self):
        report=report_for(self.tree,'pr');report['recommendation']=s.RECOMMENDATIONS[0]
        with self.assertRaises(s.Rejected):s.validate_report(self.tree,report)
    def test_pr_missing_change(self):
        report=report_for(self.tree,'pr');report['findings'][0]['introduced_by']=None
        with self.assertRaises(s.Rejected):s.validate_report(self.tree,report)
    def test_pr_fake_confirmation(self):
        report=report_for(self.tree,'pr');report['findings']=[]
        with self.assertRaises(s.Rejected):s.validate_report(self.tree,report)
    def test_pr_coverage_blocks_clean_automation(self):
        report=report_for(self.tree,'pr');report['findings']=[];report['coverage_gaps']=['missing base']
        report['recommendation']=s.RECOMMENDATIONS[0]
        with self.assertRaises(s.Rejected):s.validate_report(self.tree,report)
    def test_high_confidence_allowed(self):
        self.report['findings'][0]['confidence']='HIGH CONFIDENCE'
        self.report['findings'][0]['context_required']=['confirm this route is deployed']
        self.assertTrue(s.validate_report(self.tree,self.report)['valid'])
    def test_manual_followup_required(self):
        self.report['manual_review']=[{'title':'policy','confidence':'MEDIUM CONFIDENCE','reason':'wrapper missing','context_required':[]}]
        with self.assertRaises(s.Rejected):s.validate_report(self.tree,self.report)
    def test_evidence_work_budget(self):
        ev=self.report['findings'][0]['evidence'][0]
        self.report['findings'][0]['evidence']=[copy.deepcopy(ev)]*30
        self.report['findings']=[dict(copy.deepcopy(self.report['findings'][0]),id=f'HIGH-{i:03}') for i in range(1,201)]
        with self.assertRaises(s.Rejected):s.validate_report(self.tree,self.report)


if __name__=='__main__':unittest.main()
