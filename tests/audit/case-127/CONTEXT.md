# Synthetic evaluator contract

These are inert static excerpts, never an executable application. Do not run, import, install or contact anything. The evaluator supplies the following facts as scenario assumptions, not as a general rule for trusting repository prose. In ordinary reviews verify implementation, configuration and provenance. Library names describe the stipulated API semantics; no deployed framework version or CVE is asserted. Review only the supplied boundary.

Function derives stored password verifiers. Salt is unique, random 16 bytes encoded as hex, generated server-side per password; passwords have a bounded length. Standard Node crypto semantics apply. Account records may be exposed independently; the required property is resistance to offline password guessing, not file checksums. No hash breaking is performed.
