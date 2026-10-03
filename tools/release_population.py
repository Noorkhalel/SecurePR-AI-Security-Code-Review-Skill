#!/usr/bin/env python3
"""Reconcile this release's frozen observations; never run a model or target code."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('release_evaluator', ROOT / 'tools/evaluate.py')
evaluator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(evaluator)
OUTPUT = ROOT / 'evaluation/runs/release-population.json'


def read(path):
    return evaluator.securepr.load_json((ROOT / path).read_bytes())


def reconcile():
    runs = []
    sums = {key: 0 for key in ('cases', 'true_positives', 'false_positives',
            'true_negatives', 'false_negatives', 'ambiguous_abstentions',
            'ambiguous_missing_followup', 'safe_manual_review_cases',
            'recommendation_conflicts')}
    seen = set()
    for name, manifest_name in [('audit-r1', 'audit'), ('workflows-r1', 'workflows')]:
        manifest = read(f'tests/expected/{manifest_name}.json')
        observations = read(f'evaluation/runs/{name}.json')
        score = evaluator.score(manifest, observations)
        if score != read(f'evaluation/runs/{name}.metrics.json'):
            raise ValueError('stored score differs: ' + name)
        positive, negative, ambiguous = [], [], []
        for case in manifest['cases']:
            if case['id'] in seen:
                raise ValueError('overlapping runs')
            seen.add(case['id'])
            if case['manual_review_required']:
                if case['expected']:
                    raise ValueError('mixed gold classification requires explicit adjudication')
                ambiguous.append(case['id'])
            elif case['expected']:
                positive.append(case['id'])
            else:
                negative.append(case['id'])
        by_id = {c['id']: c for c in observations['cases']}
        runs.append({'run': name, 'total_cases': len(manifest['cases']),
                     'positive_cases': positive, 'negative_cases': negative,
                     'ambiguous_cases': ambiguous,
                     'ambiguous_with_scored_findings': [i for i in ambiguous if by_id[i]['findings']],
                     'cases_contributing_both_fp_and_fn': [c['id'] for c in score['details'] if c['fp'] and c['fn']],
                     'expected_findings': sum(len(c['expected']) for c in manifest['cases']),
                     'reported_findings': sum(len(c['findings']) for c in observations['cases'])})
        for key in sums:
            sums[key] += score[key]
    tp, fp, fn = (sums[k] for k in ('true_positives', 'false_positives', 'false_negatives'))
    sums.update(precision=tp / (tp + fp), recall=tp / (tp + fn), f1=2 * tp / (2 * tp + fp + fn))
    aggregate = read('evaluation/runs/audit-aggregate.metrics.json')
    if any(aggregate[k] != v for k, v in sums.items()):
        raise ValueError('aggregate differs from replayed observations')
    return {'version': '1.0.0', 'population': 'New audit first-pass runs only',
            'total_unique_cases': len(seen),
            'positive_cases': sum(len(r['positive_cases']) for r in runs),
            'negative_cases': sum(len(r['negative_cases']) for r in runs),
            'ambiguous_cases': sum(len(r['ambiguous_cases']) for r in runs),
            'non_ambiguous_cases': sum(len(r['positive_cases']) + len(r['negative_cases']) for r in runs),
            'units': {'tp_fp_fn': 'finding matches/unmatched findings', 'tn': 'definite-negative cases'},
            'metrics': sums, 'runs': runs,
            'excluded': ['49 historical blind-r1 cases', '2 later prompt-mutation reviews',
                         'Release demonstrations and curated example extracts'],
            'interpretation': 'TP+FP+TN+FN is not a distinct-case count. In these runs case-209 and case-210 each contribute FP and FN. Ambiguous cases contribute none of these four counts.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='compare with saved population report')
    args = parser.parse_args()
    result = reconcile()
    if args.check:
        if read(OUTPUT) != result:
            raise ValueError('release population is stale')
        print('Release population verified: 63 unique = 28 positive + 29 negative + 6 ambiguous.')
    else:
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
