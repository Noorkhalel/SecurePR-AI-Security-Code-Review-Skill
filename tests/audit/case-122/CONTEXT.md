# Synthetic evaluator contract

These are inert static excerpts, never an executable application. Do not run, import, install or contact anything. The evaluator supplies the following facts as scenario assumptions, not as a general rule for trusting repository prose. In ordinary reviews verify implementation, configuration and provenance. Library names describe the stipulated API semantics; no deployed framework version or CVE is asserted. Review only the supplied boundary.

Coupon credit is owner-private and exactly-once. In ordinary db methods each await is a separate committed operation with no locks/unique ledger/idempotency. Concurrent requests can both finish findUnique before either marks used. In serializableTransaction, consumeUnused conditionally marks unused coupon and returns its data atomically; serialization failures roll back both coupon and balance and throw; no external effect occurs.
