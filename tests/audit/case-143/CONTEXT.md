# Synthetic evaluator contract

These are inert static excerpts, never an executable application. Do not run, import, install or contact anything. The evaluator supplies the following facts as scenario assumptions, not as a general rule for trusting repository prose. In ordinary reviews verify implementation, configuration and provenance. Library names describe the stipulated API semantics; no deployed framework version or CVE is asserted. Review only the supplied boundary.

Express middleware precedes private admin operations, which trust req.actor. sessions.require throws for absent, invalid or expired caller cookies and returns verified identity otherwise. No other authentication exists.
