#!/usr/bin/env python3
"""Offline release integrity checks for this trusted project, not target code."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('securepr',ROOT/'scripts/securepr.py')
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
REQUIRED=['SKILL.md','README.md','LICENSE','SECURITY.md','CONTRIBUTING.md','CHANGELOG.md',
          'EVALUATION.md','languages/javascript.md','languages/typescript.md',
          'frameworks/express.md','frameworks/nextjs.md','references/confidence-model.md',
          'references/authorization.md','references/authentication.md','references/business-logic.md',
          'references/prompt-injection.md','schemas/review.schema.json','examples/review.json']


def check():
    errors=[];count=links=0
    for name in REQUIRED:
        if not (ROOT/name).is_file() or (ROOT/name).stat().st_size==0:errors.append('missing/empty '+name)
    for path in ROOT.rglob('*'):
        relative=path.relative_to(ROOT)
        if any(p in {'.git','__pycache__','.venv','node_modules'} for p in relative.parts):continue
        if path.is_symlink():errors.append('symlink '+str(relative));continue
        if not path.is_file():continue
        count+=1
        data=path.read_bytes()
        if b'\x00' in data:errors.append('binary '+str(relative));continue
        text=data.decode('utf-8')
        if re.search(r'^(<<<<<<< |=======\s*$|>>>>>>> )',text,re.M):errors.append('merge marker '+str(relative))
        if path.suffix=='.md':
            if sum(line.startswith('```') for line in text.splitlines())%2:errors.append('unclosed fence '+str(relative))
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
                if target.startswith(('https://','http://','mailto:','#')):continue
                target=unquote(target.split('#')[0])
                if not (path.parent/target).is_file():errors.append('broken link '+str(relative)+' -> '+target)
                links+=1
        elif path.suffix=='.json':
            try:s.load_json(data)
            except s.Rejected:errors.append('invalid JSON '+str(relative))
        elif path.suffix=='.py':
            ast.parse(text,filename=str(relative))
    skill=(ROOT/'SKILL.md').read_text()
    if not skill.startswith('---\nname: securepr\ndescription: ') or len(skill.splitlines())>500:errors.append('invalid skill frontmatter/size')
    if len(skill.splitlines()[2].removeprefix('description: '))>1024:errors.append('description too long')
    ids=set()
    for manifest_path in sorted((ROOT/'tests/expected').glob('*.json')):
        manifest=s.load_json(manifest_path.read_bytes())
        for case in manifest['cases']:
            if case['id'] in ids:errors.append('duplicate case '+case['id'])
            ids.add(case['id'])
            s.relpath(case['path'])
            for name in case['files']:
                s.relpath(name)
                if not (ROOT/case['path']/name).is_file():errors.append('missing fixture '+name)
            for finding in case['expected']:
                if finding['file'] not in case['files']:errors.append('unlisted evidence '+case['id'])
                lines=(ROOT/case['path']/finding['file']).read_text().splitlines()
                if finding['anchor'] not in lines[finding['line']-1]:errors.append('stale anchor '+case['id'])
            if case['mode']=='pr':s.parse_diff((ROOT/case['path']/'change.diff').read_bytes())
    evaluation_spec=importlib.util.spec_from_file_location('evaluation_integrity',ROOT/'tools/evaluate.py')
    evaluator=importlib.util.module_from_spec(evaluation_spec);evaluation_spec.loader.exec_module(evaluator)
    for name, manifest_name in [('audit-r1','audit'),('workflows-r1','workflows')]:
        manifest_bytes=(ROOT/f'tests/expected/{manifest_name}.json').read_bytes()
        manifest=s.load_json(manifest_bytes)
        observations=s.load_json((ROOT/f'evaluation/runs/{name}.json').read_bytes())
        recorded=s.load_json((ROOT/f'evaluation/runs/{name}.metrics.json').read_bytes())
        if evaluator.score(manifest,observations)!=recorded:errors.append('stale metrics '+name)
        snapshot=s.load_json((ROOT/f'evaluation/runs/{name}.snapshot.json').read_bytes())
        if hashlib.sha256(manifest_bytes).hexdigest()!=snapshot['expected_manifest_sha256']:
            errors.append('changed expected labels after review '+name)
        for case in manifest['cases']:
            for filename in case['files']:
                key='cases/'+case['id']+'/'+filename
                actual=hashlib.sha256((ROOT/case['path']/filename).read_bytes()).hexdigest()
                if actual!=snapshot['files'].get(key):errors.append('changed reviewed fixture '+key)
    module=ast.parse((ROOT/'scripts/securepr.py').read_text())
    for node in ast.walk(module):
        if isinstance(node,ast.Import) and any(n.name.split('.')[0] in {'subprocess','socket','requests','http','urllib'} for n in node.names):errors.append('unsafe runtime import')
        if isinstance(node,ast.ImportFrom) and (node.module or '').split('.')[0] in {'subprocess','socket','requests','http','urllib'}:errors.append('unsafe runtime import')
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in {'eval','exec','compile','__import__'}:errors.append('dynamic runtime execution')
    with s.SafeTree(ROOT) as tree:s.validate_report(tree,s.load_json((ROOT/'examples/review.json').read_bytes()))
    return {'valid':not errors,'files_checked':count,'local_markdown_links_checked':links,'corpus_cases':len(ids),'errors':errors}


if __name__=='__main__':
    try:
        result=check();print(json.dumps(result,indent=2));raise SystemExit(0 if result['valid'] else 1)
    except (OSError,ValueError,SyntaxError,KeyError,IndexError) as exc:
        print(json.dumps({'valid':False,'error':type(exc).__name__}),file=sys.stderr);raise SystemExit(1)
