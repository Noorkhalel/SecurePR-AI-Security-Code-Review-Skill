First public release of SecurePR Community: evidence-first AI security code review
for JavaScript/TypeScript, Node.js, Express, Next.js and REST APIs.

### Included

- PR/diff, repository and snippet review methodology, with source-to-sink and
  authorization/BOLA reasoning, evidence requirements and confidence classification.
- Requested scoped fixes and security regression-test generation.
- Framework/topic references, report templates and optional dependency-free Python
  helpers for static inventory, evidence excerpts, diffs and report validation.
- Prompt-injection defenses and safe static defaults.
- A recorded invoice PR review and fix, runnable synthetic regression, and selected
  actual outputs for BOLA, SQL injection, safe SQL and missing-context restraint.
- Marketplace copy and a Community/Pro proposal. Pro is not a shipping entitlement.

### Evaluation and validation

The audit's 63 distinct new cases are 28 positive, 29 negative and 6 ambiguous.
Strict matching yields TP 26 / FP 2 / TN 29 / FN 2. TP/FP/FN count findings; TN counts
negative cases. Two positive cases each contribute FP and FN because of CWE label
mismatches. Adding these columns is not a case count. All six ambiguous cases
requested context and contribute none of the four counts in the recorded runs.
Finding-level precision, recall and F1 are each 26/28 = 0.9285714285714286.

These are saved first-pass results on explicit-contract synthetic cases, not
production accuracy or new model measurements. Historical cases and release
examples are excluded from that aggregate. Raw observations remain unchanged.

Local release gates passed 87 Python tests and 31 fixed-version Node assertions.
The four before-version demonstrations failed ten expected security assertions
collectively; the release demo alone changed from 5 pass / 3 fail to 8 pass / 0 fail.
Evidence validation, integrity/local-link checks and evaluation replays passed
their specified outcomes. The workflow replay still exits 1 in strict mode because
its two recorded mismatches are retained.

### Start here

- [Installation and usage](https://github.com/Noorkhalel/SecurePR-AI-Security-Code-Review-Skill/blob/v1.0.0/README.md)
- [Three-minute PR demo](https://github.com/Noorkhalel/SecurePR-AI-Security-Code-Review-Skill/blob/v1.0.0/examples/release-demo/README.md)
- [Evaluation populations and limitations](https://github.com/Noorkhalel/SecurePR-AI-Security-Code-Review-Skill/blob/v1.0.0/EVALUATION.md)
- [Release validation record](https://github.com/Noorkhalel/SecurePR-AI-Security-Code-Review-Skill/blob/v1.0.0/evaluation/release-validation.json)

SecurePR is a skill for an AI agent, not a standalone scanner or automated customer
PR bot. Helpers do not execute target code or call a model. The selected AI host
still processes supplied source under its own policies. Prompt-injection resistance,
complete detection and application patch compatibility are not guaranteed. Use it
alongside established security testing and human review.

Existing MIT license and report JSON contract 1.0.0 are unchanged. The source
archives contain the complete repository; rename the extracted top-level folder
to `securepr` when installing. Earlier changelog labels were pre-release milestones,
not earlier public releases. No paid service, model credits or support SLA is included.
