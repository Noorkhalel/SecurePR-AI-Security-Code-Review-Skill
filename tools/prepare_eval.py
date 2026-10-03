#!/usr/bin/env python3
"""Create an answer-free evaluation packet in a NEW trusted destination directory."""
import argparse
import importlib.util
import json
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('securepr', ROOT / 'scripts/securepr.py')
s = importlib.util.module_from_spec(spec);spec.loader.exec_module(s)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', help='new directory in a trusted parent; must not already exist')
    parser.add_argument('--manifest', default='tests/expected/corpus.json', help='trusted manifest path relative to installed skill')
    args = parser.parse_args(argv)
    dest = Path(args.destination).absolute()
    # The user chooses the output location. Do not accept a symlinked parent.
    try:
        with s.SafeTree(dest.parent):
            pass
        dest.mkdir(mode=0o700)
        with s.SafeTree(ROOT) as tree:
            manifest = s.load_json(tree.read(args.manifest))
            packets = []
            for case in manifest['cases']:
                if not isinstance(case['id'], str) or not re.fullmatch(r'case-[0-9]{3}', case['id']):
                    raise s.Rejected('invalid packet case identifier')
                s.relpath(case['path'])
                for name in case['files']:
                    s.relpath(name)
                    data = tree.read(case['path'] + '/' + name)
                    target = dest / 'cases' / case['id'] / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with target.open('xb') as out:
                        out.write(data)
                packets.append({'id': case['id'], 'mode': case['mode'], 'files': case['files']})
            # No README, evaluation results, expected labels or corpus paths in skill copy.
            inventory = tree.inventory()
            if inventory['truncated']:
                raise s.Rejected('cannot prepare complete packet from truncated skill inventory')
            for record in inventory['files'] + [{'path': 'scripts/securepr.py'}]:
                name = record['path']
                if name == 'SKILL.md' or name.split('/')[0] in {'references', 'languages', 'frameworks', 'templates', 'schemas'} or name in {'scripts/securepr.py', 'docs/helpers.md'}:
                    target = dest / 'skill' / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(tree.read(name))
        (dest / 'cases.json').write_text(json.dumps(packets, indent=2)+'\n')
        print(json.dumps({'destination': str(dest), 'cases': len(packets), 'notice':'Reviewers must not access expected labels or original project.'}))
        return 0
    except (OSError, s.Rejected) as exc:
        print(json.dumps({'error': str(exc) if isinstance(exc, s.Rejected) else 'destination must be new and writable; partial packet may remain'}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
