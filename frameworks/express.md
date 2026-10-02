# Express review

Map app/router mounting and middleware order, not isolated handlers. Determine
whether a guard runs before every relevant route, whether next/error branches fail
closed and whether nested routers inherit the intended identity. Inspect HTTP
method and alternate path registration. Version 4/5 routing and error behavior
can differ; consult the project's actual version.

Review body-parser limits and ordering, raw-body signature verification, query
parser behavior, cookie/session configuration, upload storage, static mounts,
redirect destinations and error serialization. req.body/req.query are untrusted;
do not assume scalar strings or validated fields.

For trust proxy, map deployment hops and whether proxies overwrite forwarded
headers. The setting affects client IP/protocol/hostname interpretation; do not
claim bypass from a boolean alone without identifying a security decision that
trusts the resulting value and a reachable spoofing path. Cookie secure behavior,
IP rate controls and URL construction may depend on this configuration.

Check authorization at the operation, including owner/tenant-scoped queries. CORS
middleware does not authorize API access. res.json is not HTML rendering;
res.send of interpolated HTML is a separate context. Centralized error handling
can prevent leakage even if a route throws a detailed error.

References: [Express security](https://expressjs.com/en/advanced/best-practice-security/),
[proxy behavior](https://expressjs.com/en/guide/behind-proxies/).
