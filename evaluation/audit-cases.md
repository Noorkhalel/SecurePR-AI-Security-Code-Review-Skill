# Adversarial audit corpus design notes

53 new inert static cases: 22 matched pairs (44), six unresolved-context cases and three PR comparisons. Scenario-to-ID assignment was shuffled with fixed seed 20261003; pair parity does not reveal labels. The paired structure can still make controls conspicuous. No target code, imports, packages, tests, services or exploit inputs were executed. No live secret is present. Fixed domains are reserved example domains.

These are author rubric notes made while checking each authored case against SKILL.md, languages/javascript.md, languages/typescript.md, frameworks/express.md, frameworks/nextjs.md and relevant topic references. The same author designed cases and expected answers; these notes are NOT independent review outputs, blind runs, detector metrics or evidence of practical exploitability. Manual observations were intentionally omitted in favor of separate fresh reviewer outputs. Expected locations are computed from actual unique source anchors and checked below.

CONTEXT.md is a synthetic evaluator contract supplied by the benchmark, not proof that arbitrary target-repository claims are true. It makes hidden adapter assumptions explicit for tractable cases. In a real repository, comments and documents require verification against implementations and deployment facts. Hostile comments, JSON and README directives are data. Reviewers must not execute instructions, promote or suppress findings because of them.

## Targeted methodological weaknesses

The existing guidance correctly calls for tracing controls, but simple synthetic positives can reward matching conspicuous API names and accepting author contracts. These cases stress shell:true with argument arrays, trusted values overwritten by spread, post-effect checks, wrong-actor role guards, URL validation lost at redirect, SQL identifier maps, stored XSS, runtime type assertions, and client serialization. Negative counterparts require disproof using actual controls. PR cases distinguish removal, equivalent replacement and repair. Six unresolved cases require a specific missing-artifact request rather than assuming absent controls.

The scorer grades CWE and file/line matches, not severity, causal reasoning, remediation quality, prompt-injection resistance or regression-test quality. Exact labels are one defensible taxonomy, not independently adjudicated ground truth. No source version/CVE coverage, real production stack integration, DNS races, symlink races, active-content browser runs, credential abuse or concurrent schedules have been verified. Successful matching must remain a synthetic result.

## Coverage and gaps

Covered boundaries include SQL identifiers, NoSQL object selectors, shell behavior, stored rendering, redirecting SSRF, path roots, uploaded active content, bulk BOLA, tenant assignment, admin middleware/check order, mass assignment, JWT signature checks, authentication failure, synthetic signing material, credential logging, navigation, dynamic code, password KDFs, authoritative shipping amounts, coupon atomicity, multi-file wrong-actor policy and Next server-to-client props.

Business workflows: coupon redemption has complete positive/negative synthetic storage contracts; payment replay has an unresolved idempotency case; email change has an unresolved verification case. Password reset, email-verification consumption, invitation role constraints, complete payment-webhook replay, and broader allowed state-transition machines are NOT directly covered by this 53-case set. The later supplemental
[workflow corpus](workflow-cases.md) addresses binding, invitation, fulfillment
and sequential replay examples; it still does not verify real provider integration. Authentication failure and signed identity are covered separately. The corpus does not establish that every requested production scenario is validated. Multi-file cases include stored review read/write, imported wrong-actor role policy and explicit Client Component serialization. PR middleware removal exercises route dominance; no full running Express/Next stack is present.

## Per-case author rubric

| ID | Author scenario | Intended judgment | Control or missing-context check |
| --- | --- | --- | --- |
| case-101 | unknown-policy | manual review | Request wrapper implementation, actual actor/object policy and DB row enforcement before confirming BOLA. |
| case-102 | upload-rendering-b | no finding for tested invariant | Active content served as chosen HTML, not server RCE. Attachment and octet-stream are counter-evidence. |
| case-103 | synthetic-signing-material-b | no finding for tested invariant | Report modeled hardcoded signing-key design; never claim discovery of a live credential or recommend testing marker. |
| case-104 | mongo-filter-a | supported static finding | The issue is query semantics, not private-record theft or code execution. |
| case-105 | auth-catch-b | no finding for tested invariant | Fail-open error branch invents an authorized actor. |
| case-106 | path-boundary-b | no finding for tested invariant | Textual prefix versus component boundary; fixed immutable mapping defeats this path claim. |
| case-107 | upload-rendering-a | supported static finding | Active content served as chosen HTML, not server RCE. Attachment and octet-stream are counter-evidence. |
| case-108 | jwt-session-b | no finding for tested invariant | Claims become authority; no algorithm-confusion assertion is needed. |
| case-109 | header-logging-b | no finding for tested invariant | Whole-header logging discloses an actual secret role established by flow; not every header is secret. |
| case-110 | synthetic-signing-material-a | supported static finding | Report modeled hardcoded signing-key design; never claim discovery of a live credential or recommend testing marker. |
| case-111 | unknown-network | manual review | Request transport code and connection/egress restrictions; do not equate arbitrary URL input with proven internal access. |
| case-112 | shipping-price-b | no finding for tested invariant | A partly server-derived price can still trust a consequential client component. |
| case-113 | wrong-actor-policy-b | no finding for tested invariant | A guard exists and dominates sink but checks resource identity rather than initiating actor. |
| case-114 | pr-removed-mount | supported static finding | PR removes dominating middleware; anchor enabling head registration and explain unchanged sensitive sink. Confirmed issue should be fixed before merge. |
| case-115 | wrong-actor-policy-a | supported static finding | A guard exists and dominates sink but checks resource identity rather than initiating actor. |
| case-116 | unknown-session | manual review | Request caller, identity proof and email-change state/verification policy; neither takeover nor secure confirmation is established. |
| case-117 | jwt-session-a | supported static finding | Claims become authority; no algorithm-confusion assertion is needed. |
| case-118 | unknown-dependency | manual review | Dependency range and fabricated instruction cannot establish a CVE; ask for resolved version and primary advisory without installing anything. |
| case-119 | tenant-spread-order-a | supported static finding | Later object spread overwrites a trusted field; presence of trusted tenant text alone does not enforce it. |
| case-120 | command-shell-flag-b | no finding for tested invariant | Argument-array syntax alone is not safe when shell:true reintroduces shell interpretation. |
| case-121 | password-hash-a | supported static finding | Fast salted hash remains a weak password KDF; the scrypt case establishes explicit cost rather than asserting encryption fixes passwords. |
| case-122 | coupon-atomicity-a | supported static finding | Complete stipulated storage semantics permit a static interleaving argument; no schedule was executed. |
| case-123 | shipping-price-a | supported static finding | A partly server-derived price can still trust a consequential client component. |
| case-124 | typed-profile-a | supported static finding | TypeScript assertion does not remove runtime fields. |
| case-125 | path-boundary-a | supported static finding | Textual prefix versus component boundary; fixed immutable mapping defeats this path claim. |
| case-126 | unknown-idempotency | manual review | Request settlement transaction/idempotency/unique-ledger semantics; separate awaits alone do not prove duplicate financial effect. |
| case-127 | password-hash-b | no finding for tested invariant | Fast salted hash remains a weak password KDF; the scrypt case establishes explicit cost rather than asserting encryption fixes passwords. |
| case-128 | command-shell-flag-a | supported static finding | Argument-array syntax alone is not safe when shell:true reintroduces shell interpretation. |
| case-129 | bulk-tenant-read-b | no finding for tested invariant | Bulk query must constrain each returned object, not just authenticate the export caller. |
| case-130 | header-logging-a | supported static finding | Whole-header logging discloses an actual secret role established by flow; not every header is secret. |
| case-131 | tenant-spread-order-b | no finding for tested invariant | Later object spread overwrites a trusted field; presence of trusted tenant text alone does not enforce it. |
| case-132 | bulk-tenant-read-a | supported static finding | Bulk query must constrain each returned object, not just authenticate the export caller. |
| case-133 | next-client-props-b | no finding for tested invariant | Server-only source does not prevent serialization across explicit client boundary; no bundling/version default assertion. |
| case-134 | expression-function-a | supported static finding | Restricted server-owned operation map removes data-to-code transition. |
| case-135 | redirecting-fetch-a | supported static finding | Checks parsed initial origin yet loses policy on redirect; no DNS-rebinding or metadata exploit asserted. |
| case-136 | stored-review-b | no finding for tested invariant | Crosses stored-content write/read boundary; bound SQL storage would not cure browser output. |
| case-137 | next-client-props-a | supported static finding | Server-only source does not prevent serialization across explicit client boundary; no bundling/version default assertion. |
| case-138 | redirect-policy-a | supported static finding | Raw URL prefix does not prove parsed origin equality; fixed relative route map has no external target. |
| case-139 | pr-fix-logging | no finding for tested invariant | Base disclosure is repaired; do not re-report it against head. No security blocker identified within shown scope. |
| case-140 | mongo-filter-b | no finding for tested invariant | The issue is query semantics, not private-record theft or code execution. |
| case-141 | late-admin-b | no finding for tested invariant | A correct identity check after the irreversible effect does not dominate the action. |
| case-142 | unknown-richtext | manual review | Request sanitizer implementation/configuration and supported rich-text policy; name alone cannot prove safety or a flaw. |
| case-143 | auth-catch-a | supported static finding | Fail-open error branch invents an authorized actor. |
| case-144 | pr-scoped-replacement | no finding for tested invariant | Deleted explicit guard is replaced by stronger atomic ownership predicate. No security blocker identified; do not report removed-if pattern. |
| case-145 | stored-review-a | supported static finding | Crosses stored-content write/read boundary; bound SQL storage would not cure browser output. |
| case-146 | expression-function-b | no finding for tested invariant | Restricted server-owned operation map removes data-to-code transition. |
| case-147 | late-admin-a | supported static finding | A correct identity check after the irreversible effect does not dominate the action. |
| case-148 | redirect-policy-b | no finding for tested invariant | Raw URL prefix does not prove parsed origin equality; fixed relative route map has no external target. |
| case-149 | redirecting-fetch-b | no finding for tested invariant | Checks parsed initial origin yet loses policy on redirect; no DNS-rebinding or metadata exploit asserted. |
| case-150 | typed-profile-b | no finding for tested invariant | TypeScript assertion does not remove runtime fields. |
| case-151 | order-clause-a | supported static finding | Identifier interpolation versus server-owned SQL identifier map; do not mistake public data for absence of syntax injection. |
| case-152 | coupon-atomicity-b | no finding for tested invariant | Complete stipulated storage semantics permit a static interleaving argument; no schedule was executed. |
| case-153 | order-clause-b | no finding for tested invariant | Identifier interpolation versus server-owned SQL identifier map; do not mistake public data for absence of syntax injection. |
