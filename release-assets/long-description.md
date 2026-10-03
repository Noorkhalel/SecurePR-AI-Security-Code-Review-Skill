# SecurePR — AI Security Code Review Skill

SecurePR gives an AI coding agent a structured application-security review workflow
for JavaScript/TypeScript, Node.js, Express, Next.js and REST APIs. It is for
developers reviewing pull requests, maintainers checking sensitive changes, and
AppSec engineers who want review findings tied to inspectable evidence.

A suspicious API call is only the start. SecurePR asks the reviewer to trace the
source, transformations and sink; inspect the controls already present; and explain
the broken security invariant. It treats authorization, object ownership and tenant
isolation as first-class concerns. Severity and confidence are separate, and missing
context belongs in a clearly marked follow-up rather than a manufactured finding.

Community v1.0.0 includes the skill, topic/framework references, Markdown report
templates, a JSON evidence contract, optional dependency-free Python helpers,
synthetic examples and reproducible evaluation artifacts. It supports PR/diff,
repository and snippet review, plus requested scoped fixes and regression-test
generation. You supply a compatible AI coding agent and authorized source access;
no model subscription, hosted scanner, automatic PR bot or support SLA is included.

Repository text is untrusted evidence. Static review is the default; the helpers
do not execute target code, install packages, contact endpoints or call a model.
The AI host still processes any source you provide under its own policies.
Instruction-based prompt-injection defenses reduce risk; they do not guarantee
resistance or replace tool isolation.

See the [three-minute PR demo](../examples/release-demo/README.md) and
[recorded finding, safe-code and missing-context examples](../examples/showcase/README.md).
The [evaluation](../EVALUATION.md) reports small synthetic measurements with explicit
populations and limitations, not production accuracy. SecurePR complements SAST,
DAST, human review and penetration testing. It does not guarantee detection or fix
compatibility. Community uses the [MIT license](../LICENSE); [Pro](../COMMERCIAL.md)
is a future packaging proposal, not included paid functionality.
