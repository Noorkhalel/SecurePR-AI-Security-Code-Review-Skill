# SecurePR v1.0.0

First public release of the evidence-first AI security code-review skill for
JavaScript/TypeScript, Node.js, Express, Next.js and REST APIs.

- Includes PR/diff, repository and snippet review, plus scoped fix guidance and
  security regression-test generation.
- Provides source-to-sink and authorization/BOLA methodology, separate confidence
  and severity rules, prompt-injection defenses and safe static defaults.
- Ships topic/framework references, report templates and dependency-free Python
  helpers for inventory, evidence excerpts, diffs and report validation.
- Incorporates the pre-release parser, evidence-fidelity and evaluation hardening.
- Reconciles audit counts without changing raw observations: 63 unique new cases
  = 28 positive + 29 negative + 6 ambiguous. TP 26 / FP 2 / TN 29 / FN 2 mixes
  finding counts (TP/FP/FN) and negative-case counts (TN); two positive cases each
  contribute FP and FN. Finding precision, recall and F1 are each 0.928571.
- Adds a small recorded BOLA PR review with fix and runnable synthetic regression,
  plus exact historical BOLA, SQL, safe-code and missing-context output extracts.
- Includes marketplace text and a proposed Community/Pro model; Pro is not shipping.

Results cover explicit-contract synthetic cases, not production accuracy. Helpers
are not vulnerability detectors. No target code is executed by static review;
the selected AI host still processes supplied source. Prompt-injection resistance,
complete detection and real application patch compatibility are not guaranteed.

Start with [installation](installation.md), the [demo](../examples/release-demo/README.md)
and [evaluation](../EVALUATION.md). Existing MIT license and report JSON contract
1.0.0 remain unchanged. Earlier changelog version labels were pre-release working
milestones; their details remain in [CHANGELOG.md](../CHANGELOG.md).
