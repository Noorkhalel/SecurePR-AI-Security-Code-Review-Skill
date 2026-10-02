# Finding template

Use one instance per root cause. Replace field descriptions with observed facts;
use unknown/null for unavailable exact evidence. Redact sensitive literals.

- **ID / Title:** stable severity-prefixed ID and specific broken invariant.
- **Severity / rationale:** supported consequence, affected assets and prerequisites.
- **Confidence / rationale:** exact confidence label and evidence completeness.
- **Basis:** static evidence; separately record any authorized runtime validation.
- **CWE / OWASP:** justified root cause; include OWASP edition or omit the mapping.
- **Location:** file, function if named, exact source range or explicit unknown.
- **Evidence:** minimal excerpt; reviewed revision or file hash; redact secrets.
- **Source / actor:** caller-controlled value or identity/state transition.
- **Flow:** cited source → transformation → call → sink/decision.
- **Sink / missing control:** specific operation and failed security invariant.
- **Controls inspected:** relevant safeguards and counter-evidence checked.
- **Preconditions:** actor access, data/state assumptions and reachability.
- **Scenario / impact:** conceptual unauthorized behavior and bounded consequence.
- **Remediation:** smallest safe change at the authoritative layer.
- **Regression test:** rejected abuse + valid success + no unintended mutation.
- **Additional context:** essential unresolved premises; empty for CONFIRMED.
- **PR relationship:** changed enabling/control line and head evidence, if applicable.

Do not fill this template by inventing absent fields. Exact-machine output uses
[the JSON contract](../schemas/review.schema.json); narrative output can explicitly
state that exact lines are unavailable. Machine validation requires exact evidence.
