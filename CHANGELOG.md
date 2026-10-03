# Changelog

## 1.0.1 — 2026-10-03

- Rejected inconsistent diff offsets/headers, malformed metadata, oversized
  coordinates and unsupported Unicode paths with bounded errors.
- Preserved embedded carriage returns in evidence; expanded best-effort masking
  of unquoted credential assignments and authorization headers.
- Replaced greedy scoring with order-independent maximum matching; added strict
  replay gates, safe-case noise and PR-verdict consistency counters.
- Clarified scenario provenance, encoded instruction handling, exact guard/value
  relationships and fix-test compatibility/concurrency limits.
- Added 63 new static cases, two hostile metadata mutations, parser regressions
  and two new in-memory red/green remediation trials; documented audit limitations.
- Retained report JSON contract version 1.0.0.

## 1.0.0 — 2026-10-02

- Added evidence-first PR, repository, snippet and targeted-fix review modes.
- Added JavaScript/TypeScript, Express and Next.js guidance plus topic references.
- Added confidence/severity rules, source-to-sink and authorization methodology,
  prompt-injection defenses, report templates and an evidence-bound JSON contract.
- Added dependency-free static helpers and a 49-case synthetic evaluation corpus.
- Recorded fresh-context review results and generated authorization regression tests.
- Hardened physical line counting, diff section completeness, JSON numeric/depth
  checks, report error handling, resource budgets and evaluation manifest validation.
- Added repeatable unit tests, project checks and constrained CI.
