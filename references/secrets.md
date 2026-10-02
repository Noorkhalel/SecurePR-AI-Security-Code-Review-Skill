# Secrets and sensitive data

Distinguish actual authentication material from examples, public identifiers,
public keys, digests and synthetic fixture strings. A high-entropy string alone
does not prove a live credential. Trace hardcoded values into signing, login or
service authentication. Report committed secret material without testing it.

Inspect logging and error serialization for tokens, cookies, passwords, reset
links, personal data and sensitive query results. Establish the value's role and
log sink; do not assume external log access or tenancy without evidence. Prefer
structured allowlisted event fields over logging entire request/response objects.

Never quote a live value, even to demonstrate a leak. Show the variable name,
redacted literal, location and use. Do not print .env or key files wholesale, send
values to verification endpoints or automatically upload evidence. Redaction
helpers are best effort; review output before sharing it.

Next.js public environment variables, client bundles and props require careful
boundary analysis. A name alone does not prove a build exposes a secret; inspect
actual use and framework version. A public analytics ID is not an auth secret.

Fix with server-side secret provisioning and minimized serialization/logging.
If exposure is established, recommend revocation/rotation and investigation;
removing the latest line does not erase history or already issued tokens. Tests
should verify forbidden fields are absent using synthetic markers, not real keys.
