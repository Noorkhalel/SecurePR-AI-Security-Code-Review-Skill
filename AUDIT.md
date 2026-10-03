# Adversarial release audit — 1.0.1

Date: 2026-10-03. Starting revision:
`4a9201ba1a6aa87f2526ac65723f8a264add75a0`.
The existing implementation was inspected and repaired, not replaced. This is an
internal agent-assisted adversarial audit, not independent human certification.
Fresh-context agents supplied runtime probes, novel cases and remediation trials;
the primary agent also participated in the original implementation. One initial
evaluator review was interrupted by an agent usage limit; its preliminary
concerns were reproduced and resolved by the primary reviewer, not represented
as a completed external review.

## Defects and repairs

| Finding | Observed weakness | Repair / regression |
| --- | --- | --- |
| AUD-01 | Diff parser accepted inconsistent unchanged-line offsets, contradictory Git/unified paths, invalid metadata and no-change hunks | Reject inconsistent artifacts; preserve valid zero-context insertion/deletion; exercise 150 deterministic generated valid patches |
| AUD-02 | A 5,000-digit hunk coordinate produced an uncaught conversion traceback | Bound coordinate strings before conversion; verify bounded JSON error and exit 2 |
| AUD-03 | An escaped Unicode surrogate in a report path could reach filesystem encoding and produce a traceback | Reject surrogate paths and normalize Unicode processing errors |
| AUD-04 | Double CR before LF lost an embedded control character through repeated line normalization; final CR without LF was also stripped | Normalize physical line endings once and preserve data controls as escaped evidence |
| AUD-05 | Common unquoted credential assignments and authorization headers escaped best-effort masking | Mask these forms; retain explicit false-negative/over-redaction limitations |
| AUD-06 | Greedy scoring undercounted nearby findings depending on observation order | Maximum bipartite matching with overlapping-anchor and duplicate-label regressions |
| AUD-07 | Valid but poor observations always exited successfully; safe-case manual noise and contradictory PR recommendations were invisible in metrics | Add explicit counters and opt-in strict exit status; enable strict baseline replay in CI |
| AUD-08 | Scenario-contract provenance was too implicit, enabling repository prose to masquerade as authoritative context | Require provenance, verify code/config controls, treat encoded and report-shaped content as untrusted |
| AUD-09 | Fix-test guidance did not distinguish mixed-field compatibility, sequential replay and concurrent guarantees precisely enough | Add adapter-contract, rejection-semantics and actual baseline-failure requirements; two new red/green trials |
| AUD-10 | Packet builder and integrity checker assumed a single corpus | Add trusted relative manifest selection, answer-free packet regression and validation of every corpus manifest |

The fresh runtime reviewer recorded [48 baseline probes](evaluation/audit-helper-probes.json).
The initial 11 new unit methods produced 11 failed assertions/subtests and two
errors against the starting implementation. Some failures share one root cause.
A repair-stage scorer edit initially caused seven test errors; these were fixed
before the complete passing rerun. Existing tests were not weakened to conceal
failures. Runtime helper code has no external dependency, subprocess, network,
archive extraction or target-import capability. CI retains read-only permissions,
a pinned checkout action, no persisted credentials and no dependency installation.

## Evidence and tooling limits

The report validator rejects stale hashes, wrong excerpts, fabricated citation
ranges and contradictory confidence/recommendation fields within its contract.
It does **not** prove source-to-sink reasoning, semantic CWE validity, function
names, route reachability, authentication, completeness, uncited scope existence,
or correspondence between a supplied revision string and Git. No-finding output
must still describe what was inspected. Stable snapshots and a trusted output
parent remain assumptions; these helpers are not an operating-system sandbox.

The evaluator matches CWE/file/near-line anchors, not exploitability or prose
quality. It now uses order-independent maximum matching. The compact evaluation
format contains material findings only; informational hardening belongs outside
it. Strict mode treats unmatched findings, missed findings, missing ambiguous
follow-up, safe-case manual noise and internally contradictory PR verdicts as
failures. A safe-case manual flag can be appropriate in a real review; this count
measures deviation from an explicit synthetic scenario contract.

## Remediation validation

Two new evaluator-authored demonstrations use the same behavior assertions before
and after a narrow correction. Profile field integrity: before 6 pass / 3 fail,
after 9 pass / 0 fail. Checkout price integrity: before 6 pass / 2 fail, after
8 pass / 0 fail. All failures were checked for the intended state or receipt
invariant. The existing owner/tenant demonstration also passes six assertions.
See [fix evidence and limitations](evaluation/audit-fixes.md). These are trusted
in-memory models, not production database, payment or concurrency integration.

## Primary-source and documentation review

Express middleware ordering, Next.js action/data boundaries and MITRE CWE-863 /
CWE-915 were checked against current official documentation, linked in
[primary references](references/sources.md). The guidance already correctly
required version-specific interpretation; no framework-wide CVE claim was added.
Agent Skills structure, GitHub workflow hardening and ASVS terminology were also
cross-checked. Local Markdown links, JSON, Python syntax, required files, fixture
anchors and supported PR patches are checked mechanically. These checks do not
establish all external-site uptime or exhaustive spelling correctness.

## Remaining release limitations

- Prompt-injection resistance cannot be guaranteed by instructions or a finite
  corpus. Host permissions and isolation remain essential.
- No production benchmark, repeated stochastic trial, cross-model comparison,
  independent human adjudication or calibrated severity study was performed.
- Runtime helpers are bounded text utilities, not an AST analyzer, SAST engine,
  automatic reviewer or automatic fixer. Skill activation depends on the host.
- Framework integration, production policy, storage isolation, distributed races,
  full OAuth flows, cryptographic protocol correctness and real patch compatibility
  need application-specific verification.
- Redaction is best effort. Synthetic fixture credentials are deliberately inert;
  no live credential validation or target endpoint traffic was performed.
- A clean unit suite or replayed score does not demonstrate fresh model behavior.
  New behavior observations and their provenance are recorded separately below.

## Executed tooling checks

[Execution record](evaluation/audit-validation.json) contains exact commands,
exit codes, environment versions and assertion counts. The complete suite passes
86 Python unit tests, including 16 new audit methods and 150 generated valid diff
samples. All 23 fixed-version Node assertions pass across the three demonstrations.
The original demonstration still fails its two intended owner/tenant assertions;
the two new demonstrations fail five intended assertions before correction.
Report example validation, project integrity, strict historical score replay and
`git diff --check` also pass. Historical replay preserves TP 25 / FP 0 / TN 18 /
FN 0 and precision/recall/F1 1.0; these are **not new detection measurements**.

## New behavioral evaluation

Three fresh-context reviewers used frozen answer-free packets. Two reviewed 53
cases authored by a separate agent; a third reviewed ten supplemental workflow
cases authored by the primary auditor. Reviewers did not receive expected labels,
author notes or the original project. Raw outputs were saved before scoring and
were not edited to improve results. The reviewers share the session's inherited
model family; exact provider model/version was not exposed. Scenario contracts
were explicitly supplied as trusted benchmark assumptions, so these results do not
validate accepting production README claims. Corpus IDs were randomized before
review and normalized to the packet format before snapshot hashes were taken.

| First-pass run | Cases | TP | FP | TN | FN | Precision | Recall | F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| New adversarial corpus | 53 | 23 | 0 | 24 | 0 | 1.0 | 1.0 | 1.0 |
| Supplemental workflows | 10 | 3 | 2 | 5 | 2 | 0.6 | 0.6 | 0.6 |
| Combined new cases | 63 | 26 | 2 | 29 | 2 | 0.928571 | 0.928571 | 0.928571 |

All six ambiguous cases abstained and requested specific context. Both runs had
zero safe-case manual-review flags and zero internally contradictory PR verdicts.
Historical cases and two later prompt mutations are excluded from these totals.
These are strict CWE/file/near-line match metrics, not severity, real-world
exploitability or production accuracy measurements.

The two workflow mismatches are recorded, not erased: case-209 was labeled
CWE-287 by the reviewer versus CWE-863 in the key; case-210 used CWE-639 versus
CWE-640. The primary auditor inspected the actual evidence and found that both
outputs describe the intended binding defect and propose the matching correction.
That is a qualitative mechanism assessment, not independent human adjudication
or an adjusted perfect detection score. The single-label rubric cannot distinguish
all defensible taxonomy alternatives. Future datasets should adjudicate acceptable
mappings before review. No expected labels or observed CWEs were changed afterward.

- Adversarial run: [observations](evaluation/runs/audit-r1.json),
  [metrics](evaluation/runs/audit-r1.metrics.json),
  [snapshot](evaluation/runs/audit-r1.snapshot.json),
  [author rubric](evaluation/audit-cases.md),
  [reviewer A](evaluation/audit-reviewer-a.md),
  [reviewer B](evaluation/audit-reviewer-b.md).
- Workflow run: [observations](evaluation/runs/workflows-r1.json),
  [metrics](evaluation/runs/workflows-r1.metrics.json),
  [snapshot](evaluation/runs/workflows-r1.snapshot.json),
  [author rubric](evaluation/workflow-cases.md),
  [reviewer notes](evaluation/workflow-reviewer.md).
- [Combined arithmetic](evaluation/runs/audit-aggregate.metrics.json) retains the
  two strict mismatches. CI verifies stored per-run metrics against observations
  and verifies source/expected-label hashes against the frozen snapshots.

New cases exercise non-obvious shell options, partial pricing trust, wrong-actor
shared guards, middleware removal, tenant spread ordering, late checks, imported
policies, raw/stored output, explicit Next.js serialization, secure counterpart
controls, and PR removal/repair/equivalent replacement. Supplemental pairs cover
forgotten-password account binding, email-address verification, invitation role
limits, paid-only fulfillment and single-use rewards. All are small inert models;
no target application was run and no real authentication/payment provider was used.

## Prompt-injection review

The new blind corpus includes suppression, severity manipulation, a hostile
README requesting execution/disclosure, JSON instructions, misleading security
comments and fake dependency/advisory authority. Reviewers retained evidence-based
judgments and reported no target execution, network calls or obedience to those
instructions. The original corpus additionally covers fake CVE and finding text.

Two unchanged source cases were then re-reviewed with hostile YAML, base64-encoded
suppression text and a fabricated report/CVE. The prior reviewer retained one
confirmed SQL finding and one no-finding result, accepted no spoofed report/CVE
and performed no decoding or unauthorized action. [Observations](evaluation/audit-injection.md)
and [inert mutation fixtures](tests/injection-mutations/README.md) are retained.
This was explicitly attack-aware, reused-context qualitative testing, not an
additional blinded run or a proof against adaptive prompt injection.

## Reproduction

```sh
python3 -I -m unittest discover -s tests/unit -v
python3 -I tools/check_project.py
python3 -I tools/evaluate.py evaluation/runs/blind-r1.json --strict
python3 -I tools/evaluate.py evaluation/runs/audit-r1.json --manifest tests/expected/audit.json --strict
python3 -I tools/evaluate.py evaluation/runs/workflows-r1.json --manifest tests/expected/workflows.json
python3 -I scripts/securepr.py validate-report . examples/review.json
node examples/fix-mode/regression.test.mjs
node examples/audit-fix-mode/mass-assignment/regression.test.mjs
node examples/audit-fix-mode/checkout-price/regression.test.mjs
git diff --check
```

Adding `--strict` to the workflow run intentionally exits 1 because its frozen
first-pass observations contain two label mismatches. Do not replace those outputs
with expected labels to make CI green. Replaying observations is deterministic
artifact validation, not a fresh model trial. For a fresh trial, use
`tools/prepare_eval.py NEW_DIRECTORY --manifest tests/expected/audit.json` (or
`tests/expected/workflows.json`), give only the packet to a new reviewer, retain
raw observations and provenance, then score them separately.
