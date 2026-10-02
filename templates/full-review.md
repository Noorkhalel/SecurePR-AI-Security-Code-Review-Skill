# Repository Security Review

## Scope and architecture

Record revision, paths inspected, versions, exclusions, missing context and
coverage. Map entry points, auth/session, policies, database, files, network,
sensitive data, crypto, execution and state transitions.

## Trust boundaries and prioritized flows

List actor/source, transformation, operation and control with source references.
Show observed defenses as well as gaps.

## Findings

Use the finding template, deduplicate root causes and separate severity from
confidence. Bound conclusions to the actual code inspected.

## Manual review / missing context

Describe unresolved policy, framework, deployment and data-flow premises.

## Remediation and security regression tests

Prioritize fixes by supported impact. Identify compatible patches, expected
behavior and test execution status. Include valid behavior checks.

## Conclusion and limitations

State what was established and what remains unknown. A static review is neither
proof of safety nor a replacement for broader security testing.
