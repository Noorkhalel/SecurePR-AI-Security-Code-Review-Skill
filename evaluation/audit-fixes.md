# Independent fix-mode evaluation

Executed on 2026-10-03 with Node v24.19.0 in the supplied working tree. Scope was
limited to newly authored, inspected examples under `examples/audit-fix-mode/`.
No target application, existing vulnerability fixtures, package scripts, network
endpoints, installed dependencies, production data, or credentials were used.

The method under evaluation was `references/fix-and-test.md`: state the root cause
and invariant, patch the authoritative layer narrowly, preserve legitimate flows,
document compatibility, and execute the same observable assertions against both
versions. These are evaluator-authored demonstrations, not blinded model trials
or evidence that SecurePR automatically produces correct application patches.

## Results

| Case | Before passed | Before failed | After passed | After failed | Exit codes before / after |
| --- | ---: | ---: | ---: | ---: | --- |
| Profile field integrity | 6 | 3 | 9 | 0 | 1 / 0 |
| Checkout price integrity | 6 | 2 | 8 | 0 | 1 / 0 |
| Total | 12 | 5 | 17 | 0 | — |

Actual before failures were behavioral assertion failures, not import or syntax
failures:

- Profile: each of the role, tenant, and credit inputs changed persistent state
  and applied the display-name change. The invariant required full rejection.
- Checkout: the receipt used 1 cent instead of the committed 4200-cent quote;
  a second scenario completed a cart whose invalid zero-cent server quote should
  have prevented any cart change or receipt.

The after variant passed the identical assertions. No tests were skipped,
cancelled, or marked todo. Commands and their exact literal variant selection are
documented in [`examples/audit-fix-mode/README.md`](../examples/audit-fix-mode/README.md).
Initial `node --test` invocations reported only file-level pass/fail in this
environment. Direct invocation of the same `node:test` files exposed the individual
assertion results above; counts are from those observed direct runs.

## Evidence and corrective decisions

### FIX-AUDIT-01 — client fields reach protected profile state

Confidence: **CONFIRMED**, bounded to static evidence in the authored example,
with the stated behavior also exercised locally. CWE-915 is appropriate to the
unrestricted field update. Severity is not assigned to this invented product:
real impact depends on consumers of the protected fields.

Evidence: `mass-assignment/before.mjs:updateProfile` checks the actor and record
owner/tenant, validates `displayName`, then passes `{ ...profile, ...body }` to
`store.replace`. Authentication and object scoping do not constrain which fields
are persisted. The request-body properties reach the write without an allowlist.

The correction rejects extra fields and explicitly builds the only permitted
update. Rejection precedes the storage write, so a mixed valid/invalid body has no
partial effect. Tests observe complete stored records and write count, preserve
the legitimate name update, independently deny foreign owners and tenants, handle
missing profiles and invalid names, and prohibit unauthenticated storage access.
The tests do not merely assert that a guard was invoked or match source strings.

### FIX-AUDIT-02 — client amount overrides the authoritative cart quote

Confidence: **CONFIRMED**, bounded to static evidence in the authored example,
with the stated behavior also exercised locally. Severity is not assigned without
a real payment and fulfillment integration.

Evidence: `checkout-price/before.mjs:checkout` verifies owner, tenant, and open
state, then selects `body.totalCents ?? cart.totalCents` for the recorded order.
The amount check validates the substituted value instead of the authoritative
quote. The missing invariant is source integrity, not numeric validation.

The correction selects `cart.totalCents` exclusively. Tests observe persisted
receipts and cart state; they preserve a valid purchase and sequential repeat
denial, independently deny foreign owners and tenants, reject missing carts and
unauthenticated callers, and require an invalid stored quote to leave no order
or state transition. The amount assertion is a fixed contractual expectation,
not a second copy of the application's amount-selection logic.

## What this does and does not establish

The guidance was sufficient to structure two narrow corrections and meaningful
red/green tests. Denial checks include persistent-state invariants, so an error
return after a write would not satisfy these tests. Existing success and denial
behavior passes on both versions where the policy was unchanged.

The storage models prove only their synchronous, in-memory contracts. Remaining
integration work includes real session derivation, JSON parsing and schema
validation, all routes and privileged flows, database update semantics and
constraints, persistence failures and rollback, concurrent updates/checkouts,
quote creation and modification controls, and payment/fulfillment idempotency.
The sequential repeat test is not a race test or a proof of distributed replay
resistance. No production transaction guarantees are implied. A passing synthetic
suite does not establish comprehensive vulnerability coverage or real-world fix
accuracy.

## Guidance improvements identified

The existing guidance correctly requires observed red/green behavior and warns
about mock limits. These refinements would make its application less ambiguous:

1. Ask authors to state the test adapter's contract and identify which security
   decisions remain in production logic. A fake that enforces the desired policy
   itself can produce a misleading pass.
2. Make the mixed-valid/invalid update policy explicit: reject the entire request
   or ignore extra fields according to the application's contract. Field
   allowlisting alone does not decide compatibility or partial-update behavior.
3. Distinguish sequential replay tests from concurrent execution. Require named
   atomicity/rollback integration coverage before claiming race or transactional
   correctness; the brief instruction to preserve transactions/retries is not a
   test specification.
4. Require checking why the baseline failed, not just its exit code, before
   calling a run red/green. Load errors and harness failures are not evidence that
   a security assertion caught the old behavior.

These are refinements to an otherwise useful methodology, not confirmed flaws in
the review helpers or claims of an exploitable target application.
