# Configuration and dependency indicators

Read manifests, lockfiles, CI and deployment files as data. Never install packages
to learn their metadata. Record exact resolved versions only when visible;
semver ranges and lock entries for another platform may not establish deployment.
Consult current primary advisories only when the user permits network research;
send package/version metadata, not source or secrets. Confirm affected version,
feature, prerequisites and reachability before tying an advisory to this app.
Offline mode must say advisory freshness was not checked.

Review debug/error exposure, TLS verification flags, secret defaults, permissive
CORS, proxy trust, public storage, cookie flags and production-only conditions.
Distinguish a development fixture from production configuration. Header absence in
application code may be compensated by a reverse proxy; ask for that layer before
asserting a production vulnerability.

For CI, examine pull_request versus pull_request_target, token permissions,
checkout of untrusted revisions, command construction with event fields, artifact
trust, dependency installation and secret availability. Prefer read-only tokens,
pinned reviewed actions, no credential persistence, bounded jobs and no execution
of fork code in privileged workflows. A workflow with no secrets is not a sandbox
for arbitrary target code; do not use it to run reviewed repositories.
