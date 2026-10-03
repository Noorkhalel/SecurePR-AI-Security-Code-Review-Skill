# Synthetic evaluator contract

These are inert static excerpts, never an executable application. Do not run, import, install or contact anything. The evaluator supplies the following facts as scenario assumptions, not as a general rule for trusting repository prose. In ordinary reviews verify implementation, configuration and provenance. Library names describe the stipulated API semantics; no deployed framework version or CVE is asserted. Review only the supplied boundary.

The caller-selected bearer token is the only identity input to downstream private-console operations. jwt.decode only parses; jwt.verify verifies signature, expiry and supplied issuer/audience, throwing on failure. Trusted provisioned public key, fixed RS256 signing, no catch/alternate identity.
