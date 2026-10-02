# API and browser boundaries

Apply object, property and function authorization independently. Trace field
selection both into writes and out of serializers; a safe write schema does not
prevent returning sensitive columns. Check pagination and bounds on expensive
operations, but distinguish a reachable resource-exhaustion mechanism from a
missing visible rate limiter that could exist at the gateway.

CSRF: establish ambient credentials, cross-site request feasibility, a state
change and absent/ineffective verification. Bearer tokens explicitly placed in
headers behave differently from cookies. SameSite and Origin/Referer checks depend
on routes, methods and deployment; framework protections must be checked by
version. CORS is not authentication and does not prevent all cross-site requests.

CORS: show attacker origin acceptance plus a readable sensitive response and
credential behavior where needed. A literal wildcard with credentials does not
by itself prove browsers permit credentialed reads. Public non-sensitive APIs
may intentionally allow all origins. Inspect dynamic origin reflection and
preflight behavior in the actual library.

Redirects: show attacker control over an external navigation destination and
where victims receive it. Prefer server-side route identifiers or parsed allowed
origins; URL prefix checks and protocol-relative paths require attention. Do not
assume an OAuth token is leaked without the surrounding flow.

Webhooks: verify provider signatures over the correct raw bytes before parsing or
mutating state. Inspect timestamp tolerance, event ID replay handling, unique
constraints, retries and account/order binding. A verified signature proves origin
and integrity, not permission for an arbitrary object or unlimited replay.

DoS: assess attacker-controlled size, allocation, recursion, regex complexity,
synchronous CPU, fan-out and parsing depth. Bound the impact and costs; do not
execute stress traffic. Recommend time/size/count budgets and behavior tests with
small benign inputs. Do not count every unbounded loop as an exploitable outage.
