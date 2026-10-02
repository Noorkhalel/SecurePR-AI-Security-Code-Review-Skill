# Next.js review

Identify installed version, App Router versus Pages Router, route handlers/API
routes, Server Actions, middleware/proxy, DAL and authentication integration.
Version-specific defaults change; do not assume behavior from latest docs applies
to an older lockfile. Missing version/context must be disclosed.

Treat reachable Server Actions as server endpoints requiring authenticated actor
and action/object authorization. A hidden button, protected layout or middleware
matcher does not prove that an action/DAL operation is authorized. Inspect checks
inside the operation or its trusted service layer. Server execution is not itself
an authorization control. Avoid claiming every exported utility is externally
callable without checking directive, build usage and framework version.

Trace route params, Request URL/search/body, cookies/headers and action arguments.
Inspect server fetch destinations and response serialization. Minimize data passed
to Client Components; server-only secrets can leak through props/returns even when
the source module is not bundled. React escaped text is a negative XSS case;
raw HTML sinks require context-specific review.

Check NEXT_PUBLIC_ values actually referenced in client code and next.config
exposure. Not every public value is secret. Inspect cache scope and identity before
claiming cross-user data leakage. Do not assume a fetch caching default across
versions. Middleware/proxy and built-in action origin checks are useful controls,
but verify their coverage rather than inventing a bypass or ignoring them.

Consult [data security](https://nextjs.org/docs/app/guides/data-security) and
[authentication](https://nextjs.org/docs/app/guides/authentication) for the
applicable release. This module contains no blanket Next.js CVE/version claims.
