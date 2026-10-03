# Evaluation

The original implementation results below are preserved as historical evidence. The
[pre-release adversarial audit](AUDIT.md) records newly found defects, repairs, expanded
tests and their limitations. Its 63 new first-pass cases score TP 26 / FP 2 / TN 29 /
FN 2, with precision/recall/F1 0.928571 under strict label/location matching. The
two workflow taxonomy disagreements are preserved and explained in the audit.
The passing historical result did not prevent those defects. The former 1.0.0
and 1.0.1 headings were pre-release working labels, not published releases.

## Release population reconciliation

Public v1.0.0 preparation retains the audited methodology and frozen observations.
The [release execution record](evaluation/release-validation.json) reports the
rerun gates: 87 Python tests (including seven mocked publication scenarios in one
new test method), 31 passing fixed-version Node assertions across four demos,
evidence/integrity/local-link checks and all three saved evaluation replays.
The four before versions intentionally fail ten denial/integrity assertions in
total; the new demo contributes three. The workflow replay intentionally exits 1
under `--strict`, retaining its two recorded mismatches. That is an expected
evaluation result, not a failed release gate or a new model run.

[Public-link checks](evaluation/release-links.json) reached all 15 cited external
documentation URLs on 2026-10-03. This does not establish future uptime. The new
[demo](examples/release-demo/README.md) has a separate fresh review and provenance;
its test adapters do not establish real framework/database integration.

| Population | Positive cases | Definite negative cases | Ambiguous cases | Unique total |
| --- | ---: | ---: | ---: | ---: |
| New adversarial corpus | 23 | 24 | 6 | 53 |
| Supplemental workflows | 5 | 5 | 0 | 10 |
| New audit aggregate | 28 | 29 | 6 | 63 |
| Historical implementation (excluded from aggregate) | 25 | 18 | 6 | 49 |

TP/FP/FN count **findings**, while TN counts **definite negative cases**. These
columns must not be added to infer a case count. The two taxonomy mismatches
(case-209 and case-210) each produce one FP and one FN. There are **57 distinct
non-ambiguous cases**, not 59; the six ambiguous cases contribute no findings and
no TN in the saved audit runs, and all six request context. They are evaluated
separately for abstention/follow-up, not silently excluded. A reported finding on
an ambiguous case would still count as an unmatched FP under this scorer.

The audit contains 28 expected and 28 reported material findings. Precision =
26/(26+2), recall = 26/(26+2), F1 = 52/(52+2+2): each **0.9285714285714286**
(92.8571%). These are strict finding-match results for the two new synthetic runs,
not case accuracy, model reruns or an estimate of production performance.
The 49 historical cases, two later qualitative prompt mutations, release demo and
curated showcase extracts are outside this aggregate. No measured labels or raw
observations were changed for the release.

[Population artifact](evaluation/runs/release-population.json) lists case IDs,
overlaps and exclusions. Recalculate or verify it:

```sh
python3 -I tools/release_population.py
python3 -I tools/release_population.py --check
```

## Original implementation evaluation

On 2026-10-02, three fresh-context agents used the trusted skill to review disjoint
batches of 49 synthetic cases. They received neutral case IDs, source files and
application contracts, without evaluator answers or the original project path.
Their raw observations were combined only after review. No target fixture was
executed, imported, deployed or installed. The initial packet builder omitted the
optional Python helper; reviewers used static reads. That packaging defect was
fixed and the final packet was checked. The [exact packet hashes](evaluation/runs/blind-r1.snapshot.json)
are retained; no helper-assisted detection claim is made. The provider's exact model/version was
not exposed in the run metadata; no cross-model claim is made.

The corpus has 25 positive cases, 18 definite negative cases and 6 ambiguous cases.
It covers SQL/command/NoSQL injection, reflected/stored XSS, SSRF, paths/uploads,
synthetic hardcoded keys, JWT, BOLA, roles, mass assignment, logs, redirects,
multi-file flows, pricing, webhooks, randomness, a Next.js action, prompt injection,
and PR introduction/fix/neutral changes. Topic guidance is broader than the tested
corpus; OAuth, real race schedules, deserialization and production framework
integration are not empirically validated by these examples.

| First blinded run | Measured result |
| --- | ---: |
| True positives (finding matches) | 25 |
| False positives (unmatched reported findings) | 0 |
| True negatives (definite negative cases without findings) | 18 |
| False negatives (unmatched expected findings) | 0 |
| Precision | 1.0 |
| Recall | 1.0 |
| F1 | 1.0 |
| Ambiguous cases correctly abstaining | 6 / 6 |
| Ambiguous cases missing a context request | 0 |

**These are results on a small, explicit-contract synthetic corpus, not real-world
accuracy estimates.** The authors designed the cases and labels. Reviewers did not
see labels but shared the same inherited model family/session setup. There was one
fresh model pass per case, no held-out production benchmark, no repeated-run
variance study and no independent human adjudication. The corpus cannot establish
complete prompt-injection resistance or zero false positives in production.

Raw evidence: [observations](evaluation/runs/blind-r1.json),
[computed metrics and per-case results](evaluation/runs/blind-r1.metrics.json),
[expected findings](tests/expected/corpus.json).

## Matching and reproducibility

`tools/evaluate.py` uses maximum bipartite matching to match each confirmed or
high-confidence observation to one expected CWE, file and anchor within two source
lines. Duplicates/unmatched
findings count as FP; missing expected findings count as FN. TN counts only
definite negative cases. Ambiguous abstention and follow-up are separate. All case
IDs must be present exactly once. Precision = TP/(TP+FP); recall = TP/(TP+FN);
F1 = 2TP/(2TP+FP+FN). Undefined ratios are null, not fabricated perfect scores.
The scorer does not grade severity or automatically verify natural-language reasoning.
The pre-release audit additionally counts safe-case manual-review noise and internally
contradictory PR recommendations. `--strict` returns exit 1 for any unmatched or
missed finding, missing ambiguous follow-up, safe-case noise or contradictory PR
verdict. Without it, a valid score is returned even when detection is poor. Invalid
artifacts return exit 2. Evaluation findings are material security issues; the
compact format does not grade informational hardening. CI replays frozen outputs;
it does not call a model or establish current detection quality.

```sh
python3 -I tools/evaluate.py evaluation/runs/blind-r1.json --strict
python3 -I tools/prepare_eval.py /tmp/securepr-fresh-packet
```

The destination must not already exist. Give a fresh reviewer only the packet's
skill, cases and cases.json. Ask for per-case findings with CWE/file/line,
confidence, reason, source, sink, remediation, manual-review requests and PR merge
recommendation. Save observations in the same format as the recorded run; record
actual provenance, then score them. Never feed expected labels to the reviewer.
Replaying saved observations validates scoring reproducibility, not model detection.

## Helper and functional validation

Executed on Linux with Python 3.12.14 and Node.js 24.19.0:

```sh
python3 -I -m unittest discover -s tests/unit -v
python3 -I tools/check_project.py
python3 -I scripts/securepr.py validate-report . examples/review.json
node examples/fix-mode/regression.test.mjs
```

The Python suite contains 70 tests for file confinement, links/special files,
limits, changed files, redaction, physical line numbers, duplicate/non-finite/deep
JSON, diff completeness, fabricated/stale evidence, scope, confidence/recommendation
consistency and scorer correctness. Initial run: 8 failures and 1 error. After
repairs: 70 passed. [Self-review](docs/security-review.md) records root causes.
The Agent Skills frontmatter validator was also executed successfully. Project
checks validate local Markdown links, structure, JSON and corpus anchors; they do
not claim spelling or external-site uptime can be proven mechanically.

A fresh agent exercised “Fix HIGH-01” on a synthetic invoice function. It generated
a minimal owner-and-tenant query patch and six Node behavior tests. The primary
reviewer inspected and executed only this trusted demonstration:

```sh
SECUREPR_TEST_VARIANT=before node examples/fix-mode/regression.test.mjs
SECUREPR_TEST_VARIANT=after node examples/fix-mode/regression.test.mjs
```

Original: **4 passed, 2 failed** (cross-owner and cross-tenant denial). Fixed:
**6 passed, 0 failed**. Both runs use the same assertions. The in-memory adapter
implements query conjunction; this does not prove Prisma/database integration.
The environment's `node --test` subprocess reporter collapsed output to one file;
direct execution with node:test produced the six individual test results above.

## Confirmation-pressure check

A separate fresh agent was given a secure parameterized SQL function and an
explicit demand to label it CONFIRMED Critical. It rejected that requested verdict
and explained the bound-value control. [Recorded response](evaluation/confirmation-pressure.md).
This qualitative check is separate from the 49-case confusion matrix.

## Release passes

Architecture, functional validation, positive and false-positive review, hostile
repository review, helper security review, repairs, full regression rerun,
documentation review and final repository inspection are recorded in the project
history and release validation output. No live exploitation or production traffic
was used. External primary sources were checked for framework and taxonomy guidance;
no dependency CVE-detection accuracy claim is made.
