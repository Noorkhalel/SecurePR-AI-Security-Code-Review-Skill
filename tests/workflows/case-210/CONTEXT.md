# Synthetic evaluation contract

Inert source-review fixture; do not execute.

This is the public forgotten-password recovery completion operation. Tokens are unguessable, issued to an account through a verified channel, stored in server-owned state, and expire. Only the account bound to a token may change its password. The digest argument is a correctly derived password hash of caller-chosen new credentials from a trusted KDF adapter; its derivation is outside scope. All state is private to this single-process synchronous model. There are no additional policy layers.
