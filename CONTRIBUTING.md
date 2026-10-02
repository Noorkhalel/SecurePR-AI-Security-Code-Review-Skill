# Contributing

Keep SecurePR useful to a developer reading a pull request. Describe the invariant,
code evidence, counter-evidence and precise repair. Avoid generic checklists that
produce unsupported findings. Keep SKILL.md compact and put topic details in
linked references.

For a new language/framework, follow the extension contract in
[methodology](references/methodology.md). Include a vulnerable case, a secure
counterpart, missing-context behavior and a multi-file or PR example where relevant.
Use synthetic values and inert fixtures, not real secrets or operational payloads.
Check CWE root causes and edition-qualified OWASP mappings against primary sources.

Run the commands in [EVALUATION.md](EVALUATION.md). Do not claim model metrics from
format checks or replayed gold labels. For fresh agent trials, create an answer-free
packet with `tools/prepare_eval.py`, use a fresh context, keep expected results out
of that context, save raw observations, then score them separately. Report model
identity only when actually exposed by the provider. Disclose changes to fixtures,
matching rules, scope or exclusions.

Helper changes need tests for hostile input and failure behavior. Use standard
library APIs, fail closed on unsupported artifacts, avoid target execution and
network access, and preserve documented resource limits. Never weaken a failing
test merely to improve a score. Preserve failed-run evidence and explain repairs.

Small focused commits are preferred. Review Markdown links, examples, report
schema consistency and security terminology before submitting. Security-sensitive
reports should follow [SECURITY.md](SECURITY.md).
