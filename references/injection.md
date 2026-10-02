# Injection and dynamic execution

Trace whether untrusted data becomes executable syntax, not merely whether a
sensitive API is called. Inspect concrete driver/library semantics.

| Sink | Evidence of a flaw | Controls / false-positive traps |
| --- | --- | --- |
| SQL | Input forms SQL syntax before driver execution | Driver-bound values are safe for values; dynamic identifiers need fixed mappings |
| NoSQL | Input can introduce query operators or alter the selector | Scalar schema validation and explicit selector construction; JSON parsing alone is not code execution |
| Shell | Input reaches a shell command string | execFile/spawn argument arrays with shell disabled prevent shell parsing; still inspect option/argument semantics |
| eval/Function | Untrusted text becomes code | Literal/internal code or unreachable call is not attacker control |
| Template engine | Input becomes template source/expression | Data passed to a trusted template is different; inspect escaping separately |
| Dynamic import | User controls module resolution to dangerous code | Fixed module map; arbitrary identifier is not automatically an executable module |
| Deserialization | Decoder invokes behavior or revives attacker-chosen types | Ordinary JSON.parse does not itself execute code |
| Prototype pollution | Untrusted keys affect shared prototype through merge/path writes | Own-property checks, forbidden path segments, null-prototype maps; object spread alone is not sufficient evidence |

Parameterizing only some query fragments does not protect interpolated clauses.
Escaping depends on encoding, driver and SQL context. TypeScript annotations do not
sanitize input. A scalar converted and range-checked before use can defeat a
claimed injection path; inspect the actual transformation.

For prototype pollution distinguish local property injection from prototype
mutation, then show a downstream security decision or explicitly bound impact.
For deserialization do not fabricate a gadget chain or assume an unsafe package
version. For command APIs specify whether the shell runs at all; avoid conflating
shell injection with a program accepting dangerous options.

Fix by separating data from syntax with native binding, fixed command/module maps
or a restricted data grammar. Do not introduce a homemade universal sanitizer.
Regressions should verify literal treatment/rejection using benign sentinel data,
with valid-path controls. Do not generate operational exploit chains.
