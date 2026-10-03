# Synthetic evaluation contract

Inert source-review fixture; do not execute.

An authenticated user invokes verifyEmail with an unguessable token identifier and a requested email. Tokens are delivered to token.email and bound to token.userId. All tokens here have email-verification purpose. Only that bound address may be marked verified. The synchronous server-owned Maps are the whole persistence model. actor comes from a verified session; account IDs are unique. No hidden guards exist.
