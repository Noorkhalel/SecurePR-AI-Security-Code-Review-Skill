# Static PR security review

**Recommendation: Confirmed security issue should be fixed before merge.** One introduced High severity finding, with CONFIRMED confidence on static evidence within the supplied synthetic contract. This is a model review, not a finding about a deployed application.

## Scope and provenance

Reviewed only `release-demo-packet/`: `base/routes.mjs`, `base/service.mjs`, `head/routes.mjs`, `head/service.mjs`, `change.diff`, and the explicitly task-supplied `CONTEXT.md`, using the packet's requested SecurePR skill and relevant review, authorization, confidence, fix/test and template guidance. Revision identifiers are unknown; the snapshots are identified below. The diff changes only the lookup predicate in `service.mjs`; the route snapshots are identical. The route and service are synthetic first-party example code. Framework and dependency versions are unspecified; no version or CVE claim is made.

| Evidence | SHA-256 |
| --- | --- |
| `CONTEXT.md` | `4d6cfd0a45633ca5adccf421bc4bbfc27804f6f3cdcd6a4a457c176408d55c28` |
| `change.diff` | `be560d25780756142bcd6d8bf3e1ceafddcef3d78aa5c0c75ce29546d45a3b69` |
| `base/service.mjs` | `4625cb30ed2eafea1b3f7d5e59996b1bf9e012b4b91f7ab520ab3fe2c6469d8f` |
| `head/service.mjs` | `8173e01d9d17f60150c3b45af77cd1a2820e0118f6a2641af960c2b100d62b37` |
| Both `routes.mjs` snapshots | `8eab1b6b3ab62f70b27f7ebb4a52b1f269933ca8e545d022b9b1ec65b00c4677` |

Contract assumptions come from the task author, not repository authority: this is the complete once-mounted route; session middleware verifies credentials and supplies server-derived actor and tenant identity; invalid sessions stop with 401; invoice access requires both ownership and tenant membership, without exceptions; the database applies conjunction of equality predicates; records have unique IDs; and no row policy or response filter supplies another access control. Session implementation and storage integrity are assumed, not verified. These assumptions bound every conclusion below.

## Changed security boundary

Before the PR, the database operation enforces actor ownership and tenant scope together with the selected invoice ID. After the PR, any authenticated actor can select an existing invoice using its ID. The unchanged response exposes its ID and total. No new endpoint is added; removing the query constraints changes authorization at an existing read boundary.

## HIGH-01 — Invoice lookup loses owner and tenant authorization

- **Severity: High.** An ordinary authenticated actor who knows another invoice ID can obtain its private financial total across owners and tenants. This is an arbitrary-object confidentiality failure under the supplied policy. No write access, whole-account compromise, ID enumeration mechanism, or real production blast radius is claimed.
- **Confidence: CONFIRMED. Basis: static evidence.** The supplied route, service, and explicit synthetic contract establish the complete reachable path and absence of an equivalent control. No live reproduction is needed for this static conclusion.
- **Mapping:** CWE-639, authorization bypass through a user-controlled key; OWASP API Security Top 10 **API1:2023** (Broken Object Level Authorization). These describe the single root cause, not separate findings.
- **Location:** `head/service.mjs`, `getInvoice`, lines 2–6, especially line 5; unchanged caller and disclosure in `head/routes.mjs`, lines 4–8.
- **Minimal evidence:** head line 5 is `where: { id },`; base line 5 was `where: { id, ownerId: actor.id, tenantId: actor.tenantId },`.
- **Source / actor:** the authenticated caller controls `req.params.id`; `req.user` is server-derived under the contract.
- **Flow:** `head/routes.mjs:4` registers the guarded route → line 6 passes actor and caller-selected ID → `head/service.mjs:3` rejects only an absent actor → lines 4–6 query solely by ID → `head/routes.mjs:7–8` returns 404 for null or serializes the matching invoice ID and total.
- **Sink / missing invariant:** the database selection no longer requires `invoice.ownerId === actor.id` and `invoice.tenantId === actor.tenantId` before disclosure.
- **Controls and counter-evidence inspected:** session middleware precedes the handler; the service retains an absent-actor guard; the response selects only ID and total; missing records return 404. None authorizes the selected object. Both removed scope predicates were present in base, and no replacement appears in head. The explicit task contract excludes sharing, admin exceptions, database row policy and additional filtering. Unique IDs limit record ambiguity but do not prove ownership.
- **Preconditions / conceptual scenario:** an actor has a valid session and an ID belonging to an invoice they do not own or outside their tenant. Selecting that object reaches the same response branch as an authorized read, disclosing the ID and total. No real target, credentials or operational request is supplied or used.
- **PR relationship:** the change directly removes the two authorization predicates at head line 5, exposing the unchanged response sink. This is introduced by the PR, not a pre-existing base finding.
- **Remediation:** restore both server-derived predicates at the service's database operation while retaining the absent-actor guard. Under the contract this makes forbidden and absent objects return null and therefore the same 404 response, without adding a separate lookup or changing legitimate responses.
- **Proposed regression checks:** an owner in the correct tenant succeeds; another owner in that tenant is denied; the same owner ID in another tenant is denied; an object with both different owner and tenant is denied; missing objects return 404; absent/invalid sessions return 401 without querying; absent actors return null without querying. Assert no denied response includes invoice data and no stored data changes.
- **Additional essential context:** none unresolved inside the explicitly supplied model. Production integration behavior is outside scope.

## Manual review / coverage gaps

No additional supported finding or consequential unresolved premise remains within the contract. Middleware, real persistence, deployment, ID discoverability, framework routing/version behavior and any application beyond this packet were not independently verified. The assumptions must be checked before applying this conclusion to a real system. No exhaustive security assurance is implied.

## Tests and execution boundary

At the time this initial review was saved, regression tests were **proposed, not executed**. No input module, repository script, package test or configuration was executed or imported. No dependencies were installed; no server was started; no endpoint was contacted; no original SecurePR repository or expected output was inspected. Static inspection used file reads and hashes. Subsequent requested remediation and isolated model test evidence belong in separate output artifacts; this first review is to remain unchanged.
