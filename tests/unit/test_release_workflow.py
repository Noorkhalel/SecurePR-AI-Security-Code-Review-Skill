"""Exercise the publication shell with a fake gh client; no network or credentials."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
FAKE_GH = r'''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
args = sys.argv[1:]
scenario = os.environ['SCENARIO']
if scenario == 'api-error':
    sys.exit(1)
with Path('calls.jsonl').open('a') as f:
    f.write(json.dumps(args) + '\n')
if args[:3] == ['api', '--method', 'POST'] or args[:2] == ['release', 'create']:
    print('{}')
elif args[0] == 'api' and '/releases?' in args[1]:
    print(1 if scenario == 'published' else 0)
elif args[0] == 'api' and args[1].endswith('/git/ref/heads/main'):
    print('b' * 40 if scenario == 'stale' else os.environ['RELEASE_SHA'])
elif args[0] == 'api' and '/git/matching-refs/tags/' in args[1]:
    print(1 if scenario in ['tag-conflict', 'resume'] else 0)
elif args[0] == 'api' and '/git/ref/tags/' in args[1]:
    print('b' * 40 if scenario == 'tag-conflict' else os.environ['RELEASE_SHA'])
else:
    sys.exit('unexpected mocked API request')
'''


class ReleaseWorkflowTest(unittest.TestCase):
    def test_publication_fails_closed_and_is_idempotent(self):
        workflow = (ROOT / '.github/workflows/ci.yml').read_text()
        # The last run block is deliberately the publication shell. Execute only
        # that authored script, in a disposable directory with the fake client.
        script = '\n'.join(line[10:] for line in workflow.rsplit('        run: |\n', 1)[1].splitlines())
        scenarios = [('fresh', 0, 1, 1), ('resume', 0, 0, 1),
                     ('published', 0, 0, 0), ('other-version', 0, 0, 0),
                     ('stale', 1, 0, 0), ('tag-conflict', 1, 0, 0),
                     ('api-error', 1, 0, 0)]
        for scenario, exit_code, tags, releases in scenarios:
            with self.subTest(scenario=scenario), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp)
                (path / 'gh').write_text(FAKE_GH)
                (path / 'gh').chmod(0o700)
                (path / 'VERSION').write_text('1.0.1\n' if scenario == 'other-version' else '1.0.0\n')
                env = {'PATH': tmp + os.pathsep + '/usr/bin:/bin', 'SCENARIO': scenario,
                       'GH_REPO': 'Noorkhalel/SecurePR-AI-Security-Code-Review-Skill',
                       'RELEASE_SHA': 'a' * 40}
                result = subprocess.run(['bash', '-c', script], cwd=tmp, env=env,
                                        capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, exit_code, result.stderr)
                log = path / 'calls.jsonl'
                calls = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
                writes = [c for c in calls if c[:3] == ['api', '--method', 'POST']]
                publications = [c for c in calls if c[:2] == ['release', 'create']]
                self.assertEqual(len(writes), tags)
                self.assertEqual(len(publications), releases)
                for call in writes:
                    self.assertIn('ref=refs/tags/v1.0.0', call)
                    self.assertIn('sha=' + 'a' * 40, call)
                for call in publications:
                    self.assertIn('--verify-tag', call)


if __name__ == '__main__':
    unittest.main()
