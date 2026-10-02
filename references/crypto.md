# Cryptographic use

Ask what security property is required: password resistance, integrity,
confidentiality, token unpredictability or non-security checksum. A hash algorithm
used for a cache key is not the same as one used for password storage.

Inspect password KDF parameters, salts, verification API and migration needs.
Inspect encryption mode, nonce/IV uniqueness, authenticated data and key lifetime.
Do not recommend encryption as a substitute for authorization. Encoding/base64 is
not encryption; a signed token need not be confidential unless it carries secrets.

Trace Math.random or predictable values into reset tokens, sessions or other
security decisions before reporting weak randomness. Use cryptographically secure
randomness with sufficient entropy for security tokens. A random UI color is a
negative case, not CWE-338.

MAC/signature verification needs the correct bytes, trusted keys, compatible
encoding, expected algorithm and failure handling. Timing-safe comparison APIs
have length/type preconditions and do not by themselves prove a protocol is safe.
Inspect replay/expiry and event identity separately.

Prefer vetted libraries already in the stack; specify the security property and
parameter constraints. Avoid inventing a protocol or claiming cryptographic
strength from key length alone. Regression tests should prove tampering/wrong
purpose rejection and valid operation using local synthetic keys.
