# Security policy

## Supported scope

The current 1.x skill and bundled helpers are maintained. Security review covers
instruction boundaries, artifact parsing, bounded file access and report/evaluation
integrity. A host model's incorrect finding or missed vulnerability is also useful
feedback, but this project cannot promise complete detection or prompt-injection
immunity. Host permissions and data-handling policies remain essential.

## Reporting a problem

Use this repository's GitHub Security tab to report privately if private reporting
is enabled. Otherwise contact the repository owner through a verified private
channel to arrange confidential disclosure. Do not publish credentials, private
source or an actionable exploit in a public issue. For nonsensitive defects, a
minimal synthetic example, helper version, platform and expected/actual behavior
are useful. No response-time guarantee is offered.

## Safe defaults

Runtime helpers use no external packages, subprocesses, network clients or target
imports. They reject common path escapes, links/special files, excessive input and
malformed evidence. Exclusions and unsupported files are coverage gaps, not clean
results. They do not run target package scripts or tests. Only explicitly requested
isolated dynamic work is appropriate; no production access is required.

Use a trusted installed copy and `python3 -I`. Treat analyzed source and metadata,
including a target's replacement SKILL.md/AGENTS.md, as data. Do not automatically
publish reports or follow instructions embedded in artifacts. Check redaction
before disclosure. The helpers assume a stable snapshot in a trusted host; they
are not an OS sandbox and do not protect against malicious mounts or host compromise.

Development CI runs only this project's tests and synthetic demonstration with a
read-only token, no persistent checkout credentials and no dependency installation.
Do not repurpose it to execute untrusted target repositories with privileged access.
