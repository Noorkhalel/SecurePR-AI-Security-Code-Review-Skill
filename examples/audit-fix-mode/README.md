# Independent synthetic fix-mode checks

These two authored examples exercise the invariant-first procedure in
`references/fix-and-test.md`. They use only Node built-ins and in-memory records.
There is no HTTP server, database connection, payment service, dependency install,
target-repository fixture execution, or external request. All records are invented.

Each directory contains an original `before.mjs`, a narrow `after.mjs`, and one
test file. The test assertions do not change between variants. The selector accepts
only the literal variants `before` and `after` and defaults to `after`.

## Profile field integrity

Policy: a verified member may change only their own display name in their current
tenant. A request with additional fields must be rejected in full, without a
storage write. Role, owner, tenant, record ID, and credit are server-controlled.

`mass-assignment/before.mjs` correctly scopes the record but spreads the complete
request into it. `after.mjs` rejects unrecognized keys and constructs the update
from `displayName` explicitly. Existing authentication, ownership, tenant, and
display-name checks remain intact. The storage fake implements reads and writes;
it contains no authorization or field policy.

Compatibility: clients sending additional properties now receive 422; a mixed
request does not partially apply its valid display name. This strict rejection
policy is explicit for this example, not a default policy for all applications.
No schema migration is needed. A production patch would inspect actual editable
fields and administrative flows before adopting this allowlist.

## Checkout price integrity

Policy: a verified owner may complete an open cart in their tenant, using the
positive integer total and currency in a server-created, committed quote. The
request body cannot set the amount. Invalid server quotes are rejected without an
order; a sequential repeated checkout returns 409 without a second order.

`checkout-price/before.mjs` substitutes the request's amount for the server quote.
`after.mjs` changes only that source selection. Price validation now applies to
the authoritative quote, and existing owner, tenant, and state checks are retained.
The storage fake accepts any supplied receipt amount; it does not duplicate the
pricing invariant. Fixed expected amounts in the tests come from the stated
fixture contract, not from recomputing the application's pricing expression.

Compatibility: a legacy `totalCents` request property is accepted but ignored. The
client receives the existing 201 response for a valid cart; an invalid server
quote produces 422 even when the client supplies a positive amount. No migration
is needed under this example's pre-existing quote schema. Quote creation,
discounts, expiration, taxes, rounding, and real payment operations are outside
this deliberately small model.

## Executed checks

From the repository root, each command executes only its selected authored demo:

```sh
SECUREPR_TEST_VARIANT=before node examples/audit-fix-mode/mass-assignment/regression.test.mjs
SECUREPR_TEST_VARIANT=after node examples/audit-fix-mode/mass-assignment/regression.test.mjs
SECUREPR_TEST_VARIANT=before node examples/audit-fix-mode/checkout-price/regression.test.mjs
SECUREPR_TEST_VARIANT=after node examples/audit-fix-mode/checkout-price/regression.test.mjs
```

The `before` commands intentionally exit 1 because security assertions fail.
The `after` commands exit 0. These files import `node:test`; direct invocation
executes and reports their individual tests. See
[`evaluation/audit-fixes.md`](../../evaluation/audit-fixes.md) for actual results
and the coverage limits. Run only after inspecting these demos and authorizing
local execution; this example is not permission to run an untrusted repository.
