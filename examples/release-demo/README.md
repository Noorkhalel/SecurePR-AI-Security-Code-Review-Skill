# Three-minute demo: invoice PR review

An authenticated invoice endpoint looks unchanged, but a service refactor removes
object-level authorization. SecurePR's recorded review identifies the removed
owner and tenant constraints and recommends restoring them at the query.

This is a **synthetic Express-compatible route**, not a deployed application.
Session validity, private-invoice policy and database equality semantics are an
explicit [task-supplied contract](CONTEXT.md). No framework version is assumed.

## 1. Read the PR

[Base service](base/service.mjs) → [diff](change.diff) → [head service](head/service.mjs).
The unchanged [route](head/routes.mjs) reads `req.params.id`, calls the service
with the verified actor and returns the invoice ID and total.

```diff
-    where: { id, ownerId: actor.id, tenantId: actor.tenantId },
+    where: { id },
```

## 2. Read the actual review

[The complete, unchanged reviewer output](review.md) records **HIGH-01**, High
severity / CONFIRMED by static evidence within this model, CWE-639 / API1:2023.
It traces `req.params.id` → `getInvoice` → the unscoped query → invoice disclosure.
The session guard establishes identity; it does not constrain the selected object.
The PR removes both controls and supplies no replacement under the contract.

The reviewer recommends: **Confirmed security issue should be fixed before merge.**
This paragraph is an editorial summary; the linked review is the actual output.
It was produced by a fresh-context agent using the audited skill without expected
answers or the original repository. [Provenance and input hashes](provenance.json)
are retained. This single demonstration is excluded from audit metrics.

## 3. Inspect the fix and generated regression

[Fixed service](fixed/service.mjs) restores the owner and tenant predicates using
verified session identity. Forbidden and absent invoices return the same null/404;
authorized responses retain their shape. There are no sharing/admin exceptions
under this model. No migration or dependency change is needed.

The reviewer generated [eight behavior tests](generated-regression.txt). The
[runnable adaptation](regression.test.mjs) keeps those assertions and tests the
actual authored head/fixed service and route modules with in-memory session,
request/response and storage adapters. No listener or external dependency is used.
The tests include legitimate success, separate owner and tenant denials, both
denials together, missing records and absent/invalid sessions with no query.

From the repository root, using Node.js 20+:

```sh
SECUREPR_TEST_VARIANT=before node examples/release-demo/regression.test.mjs
SECUREPR_TEST_VARIANT=after node examples/release-demo/regression.test.mjs
```

The first command is expected to exit 1: **5 pass / 3 fail**, precisely the three
forbidden-object response assertions. The fixed version exits 0: **8 pass / 0 fail**.
These are model-level regression results, not live security exploitation or proof
of real Express, ORM, database or authentication integration. Only this reviewed,
trusted synthetic demo is authorized for execution; inert corpus examples remain
static review inputs. Full command evidence is in the [release validation record](../../evaluation/release-validation.json).

## Reproduce the review separately

Give an agent the trusted SKILL.md plus this directory's base, head, diff and
task-supplied context. Ask: “Use SecurePR to review this PR against its base;
inspect relevant controls and state assumptions and test status.” Withhold
review.md, fixed/, generated tests and this walkthrough for an independent pass.
A new model run may differ; replaying the bundled tests does not rerun SecurePR.
