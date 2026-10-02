# Business-logic review

Write the business invariant first and cite where it is established. Examples:
price derives from the server catalog; a payment settles the correct order once;
an invite grants no more privilege than the inviter possesses; a reset token is
consumed once; a workflow transition has an allowed prior state.

Map actor, resource, state and authoritative values across endpoints/jobs/webhooks.
Look for client-selected totals/discounts, missing quantity bounds, repeated
redemption, payment-state updates before verification, out-of-order transitions,
account linking, duplicate effects and security checks after the mutation.

Do not invent commercial policy. A client-provided amount may be valid for a
pay-what-you-want product. A duplicate request may be intentionally idempotent.
A suspicious field is not a finding without the code-visible decision/contract.
When essential product rules are absent, request them under manual review.

Race analysis: identify shared state, two competing actors/requests, a check/use
gap and the missing atomic constraint. Inspect database transactions, isolation,
conditional updates, uniqueness, locks and idempotency. await is an indicator of
possible interleaving, not proof. A transaction is not always enough if its
isolation/constraints permit the invalid schedule. If storage semantics are
missing, classify as a candidate and specify exactly what resolves it.

Fix the invariant where it is authoritative, ideally in an atomic operation or
constraint. Preserve retry semantics and recovery. Tests should assert valid flows
succeed, forbidden transitions fail, replays cause one effect and concurrent
requests cannot violate the invariant. Propose a controlled concurrent test only
when its storage contract is known; do not manufacture successful execution.
