# Paths, uploads and archives

Identify who controls path segments, original filenames, storage roots and archive
entry names. Trace normalization/decoding and the filesystem operation. path.join,
path.normalize, basename or a string prefix check is not a universal confinement
mechanism. Check path component boundaries, absolute paths, platform separators,
symlinks and check/use races. A lexical check does not prevent symlink escape.

For a confirmed flaw, establish a reachable input path and intended storage
boundary. Do not claim arbitrary root access when process permissions and storage
layout are unknown. A server-generated identifier mapped to a private file is
counter-evidence; authorization still needs separate inspection.

Uploads: inspect size/count, content-type detection, extension/format policy,
server-generated name, collision behavior, storage outside executable/public
paths, download headers and access control. Client MIME and extensions are weak
alone. A complete image decoding/re-encoding policy can be useful but must use a
maintained parser with resource limits. Malware scanning is not proof of safety.
Do not call every upload an RCE; show server execution or active-content serving.

Archives: validate each entry and link before extraction, enforce uncompressed
size/count limits, and avoid following links. Reading archive metadata does not
require extracting or executing it.

Patch the actual storage boundary; prefer object IDs or descriptor-relative
operations with no-follow semantics on a stable tree. Regression tests should
verify rejected out-of-policy paths, authorized valid access, bounded uploads and
no write on rejection. Use disposable local files only when execution is requested.
