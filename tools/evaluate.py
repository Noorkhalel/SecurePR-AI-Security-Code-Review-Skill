#!/usr/bin/env python3
"""Score independently recorded observations. This program is not a detector."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('securepr', ROOT / 'scripts/securepr.py')
securepr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(securepr)


def score(manifest, observations):
    if not isinstance(manifest, dict) or manifest.get('version') != '1.0.0' or not isinstance(manifest.get('cases'), list) or not 1 <= len(manifest['cases']) <= 1000:
        raise securepr.Rejected('invalid evaluation manifest')
    expected = {}
    for case in manifest['cases']:
        if not isinstance(case, dict) or not isinstance(case.get('id'), str) or not case['id'] or case['id'] in expected:
            raise securepr.Rejected('invalid or duplicate manifest case ID')
        if case.get('mode') not in ('full', 'pr', 'snippet') or type(case.get('manual_review_required')) is not bool:
            raise securepr.Rejected('invalid manifest case mode or ambiguity flag')
        if not isinstance(case.get('expected'), list) or len(case['expected']) > 100:
            raise securepr.Rejected('invalid manifest expected findings')
        for finding in case['expected']:
            if not isinstance(finding, dict) or not isinstance(finding.get('cwe'), str) or type(finding.get('line')) is not int or finding['line'] < 1:
                raise securepr.Rejected('invalid expected finding')
            securepr.relpath(finding.get('file'))
        expected[case['id']] = case
    if not isinstance(observations, dict) or set(observations) != {'run', 'cases'}:
        raise securepr.Rejected('observations must contain run metadata and cases')
    metadata = observations['run']
    if not isinstance(metadata, dict) or set(metadata) != {'id', 'kind', 'reviewer', 'skill_revision', 'date', 'notes'}:
        raise securepr.Rejected('missing run provenance')
    for value in metadata.values():
        securepr._text(value, 'run metadata')
    if metadata['kind'] not in {'blinded-agent', 'manual', 'harness-self-test'}:
        raise securepr.Rejected('unknown run kind')
    actual = observations['cases']
    if not isinstance(actual, list) or len(actual) > 1000:
        raise securepr.Rejected('invalid observations')
    ids = [c.get('id') for c in actual if isinstance(c, dict)]
    if any(not isinstance(i, str) for i in ids) or len(ids) != len(actual) or len(set(ids)) != len(ids) or set(ids) != set(expected):
        raise securepr.Rejected('case set must match exactly; missing/duplicate/extra cases cannot be hidden')
    tp = fp = fn = tn = ambiguous_abstentions = manual_missed = 0
    rows = []
    for case in actual:
        securepr._object(case, {'id', 'findings', 'manual_review', 'recommendation'}, 'case observation')
        if not isinstance(case['findings'], list) or len(case['findings']) > 100:
            raise securepr.Rejected('invalid observation findings')
        securepr._strings(case['manual_review'], 'manual review')
        gold = expected[case['id']]
        if gold['mode'] == 'pr':
            if case['recommendation'] not in securepr.RECOMMENDATIONS:
                raise securepr.Rejected('PR observation needs merge recommendation')
        elif case['recommendation'] is not None:
            raise securepr.Rejected('non-PR recommendation must be null')
        used, case_fp = set(), 0
        for finding in case['findings']:
            securepr._object(finding, {'cwe', 'file', 'line', 'confidence', 'reason', 'source', 'sink', 'remediation'}, 'observation finding')
            for field in ('cwe', 'file', 'confidence', 'reason', 'source', 'sink', 'remediation'):
                securepr._text(finding[field], field)
            if finding['confidence'] not in securepr.CONFIDENCES[:2]:
                raise securepr.Rejected('uncertain candidates must be placed in manual_review')
            securepr.relpath(finding['file'])
            if type(finding['line']) is not int or finding['line'] < 1:
                raise securepr.Rejected('finding line must be a positive integer')
            # Match CWE + actual file + exact sink/decision anchor, allowing a small
            # source-range shift. A wrong CWE/location is an unmatched finding.
            matches = [i for i, item in enumerate(gold['expected']) if i not in used
                       and finding['cwe'] == item['cwe'] and finding['file'] == item['file']
                       and abs(finding['line'] - item['line']) <= 2]
            if matches:
                used.add(matches[0]); tp += 1
            else:
                fp += 1; case_fp += 1
        missed = len(gold['expected']) - len(used)
        fn += missed
        if not gold['expected'] and not gold['manual_review_required'] and not case['findings']:
            tn += 1
        if gold['manual_review_required']:
            if not case['findings']:
                ambiguous_abstentions += 1
            if not case['manual_review']:
                manual_missed += 1
        rows.append({'id': case['id'], 'tp': len(used), 'fp': case_fp, 'fn': missed,
                     'manual_review': bool(case['manual_review']),
                     'recommendation': case['recommendation']})
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    f1 = 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else None
    return {'run': metadata, 'cases': len(actual), 'true_positives': tp, 'false_positives': fp,
            'true_negatives': tn, 'false_negatives': fn, 'precision': precision,
            'recall': recall, 'f1': f1, 'ambiguous_abstentions': ambiguous_abstentions,
            'ambiguous_missing_followup': manual_missed, 'details': rows,
            'limits': 'Finding matching measures this synthetic corpus only; severity, reasoning quality and test execution require separate review.'}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('observations');p.add_argument('--manifest', default=str(ROOT / 'tests/expected/corpus.json'))
    args = p.parse_args(argv)
    try:
        result = score(securepr.load_json(securepr.read_external(args.manifest)),
                       securepr.load_json(securepr.read_external(args.observations)))
        print(json.dumps(result, indent=2, ensure_ascii=True, allow_nan=False))
        return 0
    except (securepr.Rejected, OSError, TypeError, KeyError) as exc:
        message = str(exc) if isinstance(exc, securepr.Rejected) else 'invalid evaluation artifact'
        print(json.dumps({'error': message}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
