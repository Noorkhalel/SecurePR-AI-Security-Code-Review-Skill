# SecurePR self-review

Reviewed the skill, helpers, evaluator, packet builder, test corpus and release
workflow on 2026-10-02. An independent reviewer inspected helper code without
seeing corpus answers. The primary reviewer reproduced defects with unit tests,
repaired them and reran the suite. This is an internal review, not an external audit.

| Defect found | Repair and verification |
| --- | --- |
| A later metadata-only diff section could disappear from successful output | Track pending sections and reject incomplete/unsupported sections; regression covers trailing empty-file metadata |
| Unicode/control separators could shift source and diff line numbers | Use LF/CRLF physical lines and escape other controls; regression checks exact line attribution |
| Packet inventory omitted the Python helper | Explicitly include the trusted runtime; packet creation and file existence verified |
| Exponent overflow accepted non-finite JSON | Reject non-finite float conversion; add explicit nesting/byte limits independent of host recursion settings |
| Malformed report mode caused an uncaught TypeError | Use safe enum checking and normalized CLI errors; malformed-mode regression |
| Repeated evidence caused excessive reads and redaction work | Cap total citations and source bytes; cache each redacted source snapshot; bound the credential regex suffix; use a set for duplicate diff paths |
| Duplicate manifest IDs silently collapsed evaluation cases | Validate manifest fields, uniqueness and expected anchors before building the scoring map |
| Null diff headers allowed contradictory coordinates | Reject inconsistent new/deleted-file hunk coordinates |
| Packet case IDs were not constrained as output path components | Restrict to case-NNN and validate source-relative paths; require a new destination in a trusted parent |

The initial 70-test run had 8 failures and 1 error. An intermediate run retained
one scorer failure; the repaired suite passes all 70. No ordinary symlink/hardlink
escape, target execution, network client or credential leak was demonstrated under
the documented stable-tree assumptions. There are no runtime third-party dependencies.

## Adversarial critique and residual risks

An AppSec engineer may disagree with policy assumptions, severity or CWE choice;
evidence matching is not semantic proof. Source snapshots must include the real
policy/config layers. Helpers do not verify that a claimed revision matches Git.
The schema is a structural contract; runtime validation adds stricter requirements.

Prompt instructions cannot guarantee resistance to all adaptive attacks. The
corpus tests suppression, false sanitization, spoofed findings, hostile README,
YAML/JSON metadata and misleading identifiers, but is small and public. Host
permissions and isolation remain the practical boundary.

Redaction is best effort; multiline/nonstandard secret formats can be missed and
useful lines can be hidden. Large/unsupported files, excluded credential files,
opaque infrastructure, race semantics and version-dependent framework behavior
remain coverage limits. A host able to change filesystem mounts or the output
parent concurrently is outside the trusted snapshot/parent contract.

Scoring uses one-to-one CWE/file/near-line matches. The bundled corpus has one
expected finding per positive case; the 1.0.1 audit replaced order-dependent
matching with maximum bipartite matching and an overlapping-anchor regression.
Scores do not measure severity calibration, complete
report quality, production reachability or fix integration. The synthetic fix test
models query conjunction, not a real database/session stack.

The subsequent [adversarial release audit](../AUDIT.md) records additional parser,
evidence-fidelity and evaluator defects that this initial review missed.
