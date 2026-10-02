# Fix mode and behavior-based tests

On “Fix finding HIGH-01”, locate the actual finding and re-read the current code.
If the finding or code is unavailable, ask for that specific artifact; do not
invent a patch. If the premise has changed, explain before modifying anything.

1. Explain root cause and the invariant to restore.
2. Patch the narrowest authoritative layer. Preserve intended sharing, admin,
   tenant, transaction and retry behavior. Do not silently refactor unrelated code.
3. Explain why the source cannot reach the unsafe decision under the patch.
4. Identify migration, compatibility and failure-mode effects.
5. Add a regression test plus a legitimate success case in the existing test style.
6. Separate required correction from optional defense-in-depth.

User authorization to patch is not permission to execute target code. Prepare
tests statically; run them only when explicitly requested in an isolated mode.
Name any adapter/test helper whose implementation is unknown instead of inventing
a passing test. Label illustrative tests and proposed commands clearly.

Test observable behavior: authorized success, unauthorized rejection and no state
change; literal binding; text-safe output; allowed destination and rejected policy;
valid signature and tamper rejection. Avoid tests that merely check a guard was
called, search a source string or mirror the same flawed implementation.

Red/green claims require actual execution of the same meaningful assertion against
both original and patched logic. A mock proves only its model; record integration
coverage still needed. Do not create weaponized payloads, contact production,
install target dependencies or expose secrets as part of a regression.
