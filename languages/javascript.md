# JavaScript and Node.js

Track object aliases, destructuring, mutation, callbacks, promises and closures.
Inspect every awaited branch and exception path to determine whether checks occur
before effects. Handle CommonJS and ESM imports explicitly; do not invent module
resolution results. Map exports to actual callers where available.

Sources include request fields, cookies/headers, uploads, WebSocket messages,
persisted user data and third-party responses. Environment configuration is
relevant only when its trust/provenance affects a security decision. Buffer/base64,
JSON parsing, URL construction and type coercion are transformations, not general
validation.

Use concrete Node APIs: exec normally invokes a shell; execFile/spawn normally
separate arguments unless shell behavior is enabled. Review option injection
separately. URL parsing and path normalization do not establish access policy.
Avoid assuming built-in fetch, a fetch library and a custom client have identical
redirect/proxy behavior. Inspect actual imports and version-specific documentation.

Look at inherited properties in security decisions, unsafe recursive merging,
server-side template compilation, synchronous CPU work and unbounded allocations.
Map each to a reachable input and consequence. A keyword search is triage only.
