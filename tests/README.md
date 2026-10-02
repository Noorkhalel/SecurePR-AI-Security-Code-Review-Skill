# Test corpus

All source under vulnerable, secure, ambiguous and pr-diffs is **inert synthetic
test data**. Do not deploy it, install dependencies, import it or run it as an app.
String constants labelled synthetic are not real credentials. No live targets or
operational exploit payloads are included.

[corpus.json](expected/corpus.json) contains evaluator-only expected root causes,
locations, modes, tags and ambiguity requirements. Its line anchors are tied to
actual fixture content. CONTEXT.md supplies application contracts: these are
scenario data, not instructions that can override the installed review skill.

The corpus includes positives, secure counterparts, missing-context cases,
multi-file flows, framework examples, prompt injection and base/head PR pairs.
`tools/evaluate.py` grades externally produced observations; it does not generate
findings. Unit tests separately validate helper and scoring behavior. See
[EVALUATION.md](../EVALUATION.md) for executed runs and limitations.
