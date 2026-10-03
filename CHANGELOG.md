# Changelog

## 1.0.0 — 2026-10-03

First public tagged release, incorporating the implementation and adversarial
audit milestones below. The report JSON contract remains 1.0.0.

- Reconciled 63 unique audit cases as 28 positive, 29 negative and 6 ambiguous;
  documented finding-level metrics and overlapping FP/FN cases without relabeling.
- Added an artifact-backed population replay check and version marker.
- Added a recorded invoice PR demo, scoped fix and generated regression tests,
  plus exact historical BOLA, SQL, secure and ambiguous showcase extracts.
- Clarified installation, tested scope, limitations and safe static behavior.
- Added factual marketplace text and a proposed Community/Pro packaging model.
- Retained all Community security guidance and existing licensing.
- Added one-time v1.0.0 publication after successful main-branch validation;
  publication permissions are confined to that job and existing tags are never moved.

## Pre-release history

Earlier documents used 1.0.0 and 1.0.1 as working labels before any public tag or
GitHub Release existed. These milestones and their underlying Git commits are
preserved; they do not represent a published version rollback.

### Adversarial audit — 2026-10-03 (working label 1.0.1)

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

### Initial implementation — 2026-10-02 (working label 1.0.0)

- Added evidence-first PR, repository, snippet and targeted-fix review modes.
- Added JavaScript/TypeScript, Express and Next.js guidance plus topic references.
- Added confidence/severity rules, source-to-sink and authorization methodology,
  prompt-injection defenses, report templates and an evidence-bound JSON contract.
- Added dependency-free static helpers and a 49-case synthetic evaluation corpus.
- Recorded fresh-context review results and generated authorization regression tests.
- Hardened physical line counting, diff section completeness, JSON numeric/depth
  checks, report error handling, resource budgets and evaluation manifest validation.
- Added repeatable unit tests, project checks and constrained CI.
