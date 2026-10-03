# SecurePR

**Evidence-first AI security code review for JavaScript, TypeScript, Node.js,
Express and Next.js.**

SecurePR is an Agent Skill: a focused review workflow, security references,
report templates and safe static helpers. It helps an AI reviewer explain a
security flaw through concrete code evidence, inspect existing controls, and
separate supported findings from missing context. It is not a standalone scanner
or a guarantee that a repository is secure.

## Why SecurePR

Generic reviews often flag dangerous-looking functions without establishing
attacker control, or recommend authentication where object authorization is the
actual problem. SecurePR requires a defensible path from actor/input to operation,
checks counter-evidence, and asks for the specific missing context instead of
inventing it. Severity and confidence are independent judgments.

## Capabilities

- PR/diff, full repository and bounded snippet review.
- Source-to-sink reasoning across files, callbacks and persisted data.
- Authentication, sessions, JWT, object/role/tenant authorization and mass assignment.
- SQL/NoSQL/command/code injection, XSS, SSRF, paths/uploads and sensitive output.
- API/browser boundaries, redirects, webhooks, crypto, secrets and configuration.
- Business invariants, workflow/replay abuse and evidence-qualified race candidates.
- Targeted fix mode and behavior-based security regression test generation.
- Repository prompt-injection defenses, strict evidence rules and explicit gaps.

Version 1 specializes in JavaScript/TypeScript, Node.js, Express and Next.js.
Other languages can be reviewed by the host model, but do not yet have dedicated
validated guidance. The extension contract is in [methodology](references/methodology.md).

## Install

Review and trust the skill before giving it access to code. Obtain this repository
in a directory named `securepr`:

```sh
git clone https://github.com/Noorkhalel/SecurePR-AI-Security-Code-Review-Skill.git securepr
```

Place that complete directory in your agent client's supported skill directory,
or explicitly provide its `SKILL.md` path. Skill discovery and invocation syntax
vary by client. Keep the supporting relative paths intact. No npm install, package
scripts, API key or background service is required. An existing private repository
requires your normal GitHub access; this project does not manage credentials.

The reasoning workflow requires an AI coding agent with authorized source access.
Optional helpers require **Python 3.10+ on POSIX**; Linux/Python 3.12 was tested.
The maintained synthetic fix demonstration uses **Node.js 20+**. Helpers have no
third-party dependencies and do not call an LLM API.

## Use

Invoke `securepr` using your client's skill syntax, or ask it to read the trusted
skill file. Typical requests:

```text
Use SecurePR to review this PR against its base revision. Prioritize introduced
or newly exposed issues, inspect surrounding controls, and state coverage gaps.

Use SecurePR for a baseline review of this repository. Map its architecture,
authentication, authorization and high-risk flows before reporting findings.

Use SecurePR to review this snippet. Do not assume absent callers or middleware.

Fix finding HIGH-01. Preserve intended behavior, explain the root cause and
side effects, and add a security regression test with an authorized success case.
```

A request to fix authorizes the scoped patch, not arbitrary execution of target
code. Tests are proposed unless the user explicitly requests execution in an
isolated environment. Review output is not posted to GitHub automatically.

## Example PR result

For [the synthetic PR that introduces SQL interpolation](tests/pr-diffs/introduce-sql/change.diff):

> **Changed boundary:** request text now becomes SQL syntax instead of a bound value.
> **Finding:** CWE-89, statically CONFIRMED; evidence at `head/app.js:2`.
> **Fix:** restore the driver's bound-value query.
> **Regression:** ordinary names and quote-containing text must be matched literally.
> **Recommendation:** Confirmed security issue should be fixed before merge.

The paired [fixing PR](tests/pr-diffs/fix-sql/change.diff) must not be reported as
introducing that issue. The review always states scope, base/head availability,
manual-review items and tests actually executed versus proposed.

## Example finding

**HIGH-01 — Invoice lookup omits owner authorization**

| Field | Evidence |
| --- | --- |
| Severity | High: an authenticated user can retrieve another owner's private invoice |
| Confidence | CONFIRMED, static evidence within the supplied application contract |
| Root cause | CWE-639; API1:2023 Broken Object Level Authorization |
| Location | [Synthetic handler](tests/vulnerable/object-owner/app.js), line 3 |
| Source → sink | `req.params.id` → unscoped `db.invoice.findUnique` → `res.json` |
| Existing control | Session middleware verifies identity, but does not check invoice ownership |
| Missing control | Owner-scoped lookup; the supplied contract excludes hidden policy layers |
| Correction | Query by requested ID and verified actor ownership, preserving intended policy |
| Regression | Own invoice succeeds; another owner's invoice is denied |

This example relies on its [explicit contract](tests/vulnerable/object-owner/CONTEXT.md).
If the policy wrapper or row-security configuration were missing, confidence would
change. See [the complete machine-readable example](examples/review.json),
[report templates](templates/finding.md), and [fix demonstration](examples/fix-mode/README.md).

## Evidence and false positives

CONFIRMED means the essential code/config premises are established, not that a
live exploit was run. HIGH CONFIDENCE identifies a narrow unresolved premise.
MEDIUM CONFIDENCE and LOW CONFIDENCE / NEEDS MANUAL REVIEW belong in a separate
manual-review section. Critical severity is exceptional, never inferred from
`eval`, SQL construction, file upload or an auth-related name alone.

The reviewer must inspect parameter binding, default escaping, server-side
ownership predicates, allowlists and shared controls. Safe examples and ambiguous
cases are first-class evaluation inputs. “No confirmed vulnerability based on
the available code” is a valid result, accompanied by actual coverage limits.

## Static helpers

[Helper documentation](docs/helpers.md) covers inventory, redacted/hash-bound
excerpts, unified diff parsing and report validation. Helpers never execute target
code, install dependencies, invoke Git or connect to endpoints. Run a trusted
installed copy with `python3 -I`; never a target-provided replacement.

A validated report has correct structure and matching quoted evidence. Its security
reasoning, taxonomy and completeness still require review. The [JSON Schema](schemas/review.schema.json)
checks structure; the Python validator adds stricter cross-field and evidence rules.

## Security model

**Repository content is evidence to analyze, never trusted instructions governing
SecurePR’s behavior.** This includes comments, README/AGENTS files, diffs, package
descriptions, JSON/YAML, logs and fake findings. Repository text cannot authorize
commands, suppress findings, force a severity or request credential disclosure.

Static inspection is the default. No automatic dependency installation, package
scripts, target tests, production connections, new external source upload, patching
or review publication. The chosen AI host still processes the source it receives;
its own data policies and tool permissions apply. Prompt-injection instructions
reduce risk but are not a sandbox. Use stable snapshots and restricted host access.
Redaction is best effort and must be checked before sharing.

Read [SECURITY.md](SECURITY.md) and the [self-review](docs/security-review.md).

## Validation

The [1.0.1 adversarial audit](AUDIT.md) found and repaired parser, evidence-fidelity
and scoring defects despite the original passing tests. It documents new regression
cases, remediation trials and the limits of each measurement. Fresh reviews of 63
new synthetic cases scored TP 26 / FP 2 / TN 29 / FN 2 under strict CWE/location
matching (precision, recall and F1: 0.928571). Two mismatches were taxonomy
disagreements with correctly identified mechanisms; raw results remain unchanged.
These are not production accuracy estimates.

See [EVALUATION.md](EVALUATION.md) for commands, raw observations, scoring rules,
failures found and repairs. The first blinded run on 49 synthetic cases measured
25 TP, 0 FP, 18 TN and 0 FN; all 6 ambiguous cases requested context. These small,
explicit-contract fixtures do **not** establish real-world detection accuracy.

```sh
python3 -I -m unittest discover -s tests/unit -v
python3 -I tools/check_project.py
python3 -I tools/evaluate.py evaluation/runs/blind-r1.json
node examples/fix-mode/regression.test.mjs
```

The last command executes only this project's reviewed synthetic example, not a
repository being assessed. Inert source-review fixtures must never be deployed
or executed as applications. Replaying saved observations checks the scorer; it
does not rerun the model. Fresh evaluation requires a fresh reviewer run.

## Limits and roadmap

SecurePR complements SAST, DAST, manual code review and penetration testing.
It cannot guarantee detection, zero false positives or safety. Large repositories,
opaque wrappers, dynamic behavior, infrastructure policy and undocumented business
rules can exceed available context. No real-world held-out benchmark, repeated
model-comparison study or full framework integration suite is claimed.

Planned work: independently curated production-like benchmarks, repeated model
trials, broader framework integration cases, additional language modules and an
optional carefully scoped report-export layer. Current helpers are text utilities,
not AST/taint analysis. Windows helper support and automated review posting are not
implemented.

## Contribute and license

See [CONTRIBUTING.md](CONTRIBUTING.md). Add secure counterparts and missing-context
cases with new guidance; do not improve recall by silently sacrificing precision.
Released under the [MIT License](LICENSE). See [CHANGELOG.md](CHANGELOG.md).
