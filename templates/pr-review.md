# Security Review Summary

State base/head, changed and inspected files, review completeness and relevant
framework versions. Give a bounded result and the counts by confidence/severity.

## Changed security boundaries

Describe identity, ownership, tenant, state, input/output and execution boundaries
affected by the change. Include new or modified attack surface.

## Findings introduced or exposed by the PR

Use the finding template. Explain the causal change. Do not list a fixed base
issue as an introduced vulnerability. State “No confirmed vulnerability based on
the available code” when appropriate, followed by coverage limits.

## Manual review / missing context

State each consequential uncertainty, its confidence and the smallest missing
artifact. Keep speculative hardening separate.

## Suggested fixes and security regression tests

Describe precise corrections, valid-path tests and negative behavior assertions.
Label proposed versus executed tests and their outcomes.

## Merge-security recommendation

Choose the exact recommendation phrase from SKILL.md. Explain its scope and any
review gaps. This is security advice, not automatic PR approval or publication.
