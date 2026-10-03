# Supplied synthetic application contract

These are benchmark assumptions provided by the task author, not claims to trust
in a repository under review. This small application model is not deployed.

The PR simplifies invoice lookup; only service.mjs changes. Base and head are
complete for this route. mountInvoiceRoutes is mounted once. requireSession
verifies the session and sets req.user to a server-derived { id, tenantId };
an absent/invalid session returns 401 without invoking the handler. Callers can
choose req.params.id. Each invoice is private to its owner within its tenant;
there are no sharing/admin exceptions. db.invoice.findFirst applies conjunction
of supplied equality predicates and returns a matching record or null. There is
no row-level policy or additional response filter. Each stored record has a
unique id, ownerId, tenantId and total. Storage integrity and session middleware
are assumed by contract, not implemented here. No dependencies or network services
are needed for static review. Framework version is unspecified; do not infer
version-specific behavior or CVEs.
