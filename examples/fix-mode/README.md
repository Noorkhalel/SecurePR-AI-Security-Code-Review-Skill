# HIGH-01: invoice authorization fix

Scope: supplied synthetic snippet and stated policy; working-tree revision unknown.

Root cause: `before.mjs` authenticates only by testing whether an actor exists,
then passes the caller-selected invoice ID to `findFirst` without owner or tenant
constraints. Given the supplied policy and conjunctive Prisma semantics, static
evidence confirms that the original function can return another owner's or
tenant's private invoice. No runtime validation or live exploitation was performed.

Patch: `after.mjs` adds `ownerId: actor.id` and `tenantId: actor.tenantId` to the
same query predicate. Both identity values come from the verified session under
the supplied contract. A returned invoice must match its ID, owner, and tenant.
There are no sharing or administrative exceptions. The original file is intact.

Side effects: previously unauthorized reads now return null, matching nonexistent
records and unauthenticated requests. Authorized reads retain their returned
record shape. The function performs no writes and requires no schema migration,
dependency, or API signature change. Database errors continue to propagate.
Production query performance and database integration were not assessed.

Test status: executed by the primary reviewer after inspecting this synthetic demonstration. The original produced 4 passes and 2 failures; the fixed version produced 6 passes and 0 failures. `regression.test.mjs` uses Node built-ins,
synthetic in-memory records, and a small equality-conjunction adapter. It covers
authorized success, independent owner and tenant denials, absent invoices,
unauthenticated denial, unchanged records/session identity, and absence of database
access for unauthenticated callers. The environment selector accepts only literal
`before` and `after` variants and defaults to `after`.

The original violated the cross-owner and cross-tenant assertions; the patch satisfied all six scenarios in actual local execution. The adapter models only the stated conjunction
contract; it does not prove actual Prisma/database integration or session integrity.
