# Authorization is an invariant

For every sensitive operation identify **actor → action → object → tenant → state**.
Locate the server-enforced policy, not the button visibility. Review reads as well
as mutations, bulk operations, exports, nested resources and alternate routes.

| Pattern | Evidence required | Counter-evidence to inspect |
| --- | --- | --- |
| BOLA/IDOR | Caller chooses object key; operation exposes/modifies another actor's restricted object | Owner/tenant-scoped query, row security, policy wrapper, deliberately public data |
| Vertical privilege escalation | Ordinary actor reaches an operation reserved by visible policy for elevated roles | Server-derived role/capability guard before operation |
| Tenant isolation | Caller can select other tenant data despite a documented/implemented tenant boundary | Tenant derived from verified membership and applied to query/write |
| Mass assignment | Untrusted object reaches update/create of protected fields | Explicit server-side field allowlist, schema stripping, service enforcement |
| Frontend-only check | Sensitive server operation remains reachable without equivalent server decision | Handler/DAL policy enforcing the same invariant |

Authentication establishes identity, not ownership. A role check can still miss
object scope. Conversely, a database predicate using verified actor/tenant values
is often the authorization control. Check how those values were derived. Do not
assume ORM methods have hidden ownership filters; inspect wrappers and schema.
Public shared resources legitimately need different policy from private records.

Prefer atomic authorized mutation predicates over check-then-write when state can
change. Check owner/tenant reassignment, bulk mixed-ownership requests, invite
roles, admin defaults and alternate HTTP methods. Do not assume unpredictability
of IDs substitutes for authorization; do not assume enumeration is necessary if
a caller can already learn an ID.

Use CWE-639 for authorization bypass through a user-controlled key when it fits;
CWE-862 for missing authorization; CWE-863 for incorrect checks; CWE-915 for unsafe
attribute modification. These are alternative root causes, not automatic stacked
findings. API1:2023 covers BOLA, API3:2023 covers object property authorization,
API5:2023 covers function level authorization.

Fix by scoping the operation to the verified actor/tenant and allowed action,
preserving intentional sharing/admin policy. Test same-owner success, other-owner
and other-tenant rejection, lower-role rejection and unchanged data on failure.
