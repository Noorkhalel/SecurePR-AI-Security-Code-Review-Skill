# Authentication, sessions and tokens

Trace credential receipt → verification → session issuance → session lookup →
handler identity. Inspect actual middleware and every exposed sensitive handler.
A variable named user is not proof of a verified actor. A test stub is not a
production authentication mechanism.

JWT: decoding is not verification. Establish whether decoded claims authorize a
request. Check signature verification, trusted key source, allowed algorithm,
issuer, audience, expiry and application token purpose according to the library
and token contract. Do not assert every absent optional claim is a vulnerability.
Do not claim algorithm confusion without key/algorithm behavior evidence.

Session: review identifier generation, rotation after login/privilege changes,
logout/revocation, expiry, cookie transport/access flags and storage. Cookie
settings depend on deployment TLS and cross-site requirements; SameSite is not
a complete CSRF strategy. Look for fail-open error paths and authentication that
runs after a handler.

Reset/invite/email-change: trace token entropy, binding to user and purpose,
expiry, single use, storage and atomic consumption. Identify takeover only when
the flow grants an attacker the necessary identity. Uniform failure behavior and
rate controls can matter, but unknown infrastructure limits are missing context.

OAuth/OIDC: distinguish OAuth authorization from OIDC identity. Verify state and
transaction binding, PKCE where appropriate, redirect URI policy, issuer/audience,
nonce when required and account-linking identity proof. Do not call a missing
visible state field a confirmed issue if the trusted SDK maintains it elsewhere.

Remediation: use the existing vetted verification/session API with explicit
application constraints. Preserve legitimate refresh/revocation flows. Tests
should reject absent, expired, tampered and wrong-purpose tokens while accepting
a valid intended token. Never log or paste real tokens into the report.
