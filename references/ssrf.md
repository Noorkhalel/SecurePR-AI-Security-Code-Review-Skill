# Server-side request destinations

Trace caller input through URL parsing, redirects, DNS and the actual outbound
client. Show control over destination, not just use of fetch. Distinguish a fixed
trusted origin plus encoded data from a fully user-chosen URL.

Inspect scheme, exact hostname/origin, port, credentials, redirects, resolution,
IP family and connection behavior. Prefix/substring URL checks are not equivalent
to parsed-origin comparisons. A public-host check alone can be invalidated by
redirects or DNS changes. For applications intentionally fetching arbitrary public
URLs, destination validation and network-level egress policy must agree at the
connection boundary; do not propose DNS preflight followed by unpinned fetch as a
complete fix. Confirm library behavior for the installed version.

Do not assert cloud metadata access, internal credentials or a reachable private
service without evidence. State unknown egress controls as context. A fixed-origin
client is a useful counterexample when caller input affects only an encoded query
parameter and redirect policy is constrained. Encoding does not validate a URL
when the encoded value is subsequently parsed as a destination.

Prefer server-owned destination IDs mapped to fixed origins. Disable or revalidate
redirects, bound timeout/response size and use an appropriately constrained client
and egress network. Tests should use a fake transport: accept an approved
identifier, reject unknown destinations, and check redirect handling without
making network requests.
