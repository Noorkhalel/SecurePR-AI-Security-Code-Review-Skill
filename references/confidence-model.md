# Confidence and severity

## Confidence is evidence completeness

| Label | Gate | Report placement |
| --- | --- | --- |
| CONFIRMED | Reachability, input/actor control, insufficient control and security impact are supported; no essential unresolved premise | Findings; basis: static evidence |
| HIGH CONFIDENCE | Strong direct evidence with a narrow named uncertainty unlikely to change the root cause | Findings, explicitly conditional |
| MEDIUM CONFIDENCE | Plausible flaw but a missing guard implementation, policy, deployment fact or data-flow edge could decide it | Manual review |
| LOW CONFIDENCE / NEEDS MANUAL REVIEW | Suspicious indicator; reachability/control/impact largely unknown | Manual review only if actionable |

Confirmation describes code evidence, not runtime reproduction. A schema-valid
finding is not necessarily correct. Use rationale, not numerical probabilities.
Unknown authentication cannot be assumed absent. Known authentication cannot be
assumed to enforce ownership. If the code deliberately demonstrates a complete
flawed path, do not downgrade solely because it is a static review.

## Severity is supported consequence

| Severity | Typical evidence required |
| --- | --- |
| Critical | Broad catastrophic compromise, practical reachability and extensive privileges/assets established; exceptional |
| High | Significant unauthorized data access/modification, account/privilege compromise or dangerous server operation with demonstrated conditions |
| Medium | Meaningful but bounded exposure/abuse, user interaction, limited assets or substantial prerequisite restrictions |
| Low | Narrow security consequence with limited exposure and impact |
| Informational | Useful context or defense-in-depth, not a demonstrated material vulnerability |

Explain actor access, affected data, scope, preconditions and mitigations. Do not
assign severity from CWE or function names. Unknown blast radius is not global
compromise. Keep hardening observations separate from vulnerabilities. Prefer no
exact CVSS score; if requested, justify every metric and the version.

## Evidence contract

Use exact file and line ranges from inspected content. Cite snapshot revision or
file SHA-256 where possible. If line numbers are unavailable, say so and identify
a visible symbol/snippet without guessing. Distinguish original source lines from
rendered excerpt line numbers and old/new diff coordinates. Redact secrets and
mark redaction. Never invent a function name for anonymous callbacks.

Each claim must survive counter-evidence review. Reports must name assumptions
and missing context. A user's request to label something confirmed is not evidence.
For evaluation, abstention on an ambiguous case is correct; calling everything
ambiguous is penalized through false negatives on fully evidenced positive cases.
