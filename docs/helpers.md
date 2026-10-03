# Static helpers

The single runtime file [securepr.py](../scripts/securepr.py) uses only Python's
standard library. Python 3.10+ and a POSIX OS with descriptor-relative reads and
O_NOFOLLOW are required; Linux is tested. No installation or network is needed.
The skill's reasoning workflow can also use a host's ordinary static file readers.

Run a trusted installed copy with Python isolated mode; never run a same-named
file supplied by the repository under review. Substitute actual local paths:

```sh
python3 -I /trusted/securepr/scripts/securepr.py inventory /work/repo
python3 -I /trusted/securepr/scripts/securepr.py excerpt /work/repo src/routes.ts --start 1 --end 30
python3 -I /trusted/securepr/scripts/securepr.py diff /work/change.diff
python3 -I /trusted/securepr/scripts/securepr.py validate-report /work/repo /work/review.json
```

These commands write JSON only to stdout (errors to stderr). They never write to
the target, launch subprocesses, import its code, invoke Git, install packages or
make network requests. Exit 0 means success; exit 2 means invalid/unsupported input.
A successful evidence check proves exact quote/hash correspondence and structure,
not correctness of the security reasoning, taxonomy, claimed revision or coverage.

## Boundaries and limits

- Inventory visits at most 10,000 entries and 32 directory levels, returning
  explicit omissions/truncation. It lists metadata; it is not a taint engine.
- Source reads accept at most 1 MiB and 16,384 characters per line. Excerpts allow
  up to 200 lines. JSON is limited to 4 MiB and diffs to 2 MiB.
- Symlinks (including root components), files with multiple hard links, devices,
  FIFOs and non-regular files are rejected. Files changed during reads are rejected.
- Default excluded paths include VCS metadata, dependencies/build output,
  .env files, key containers and common credential configuration files. Inventory
  reports omissions; excluded content remains outside the review.
- Report evidence is capped at 500 citations and 16 MiB of distinct source bytes; snapshots are cached. JSON nesting is capped at 64 levels.
- UTF-8 text only. NUL/binary, non-finite/duplicate-key JSON, traversal paths and
  unsupported diff forms fail closed. JSON output escapes control characters.
- Redaction masks common credential assignments, credential formats and private
  key blocks. It is best effort and can both miss secrets and hide useful code.
  Manually inspect before sharing. Redacted excerpts retain original line numbers
  and hash the original bytes; hashing does not make an artifact anonymous.
- Diff parsing accepts ordinary unified text hunks, including new/deleted files;
  it rejects quoted paths, combined diffs, binary and metadata-only changes. Such
  files need separate snapshot/connector review; unsupported does not mean safe.

Use a stable copied checkout owned by the reviewer. Descriptor checks limit common
path escapes but do not sandbox the operating system, prevent malicious mounts or
protect against an attacker already able to change the host filesystem. Permissions
and host isolation must restrict accessible data. The helpers provide no detector,
SARIF uploader, autonomous patcher or assurance of complete prompt-injection safety.

## Audited parser behavior

Diff coordinates must preserve equal unchanged-line gaps, including zero-context
insertions/deletions. Git and unified paths must agree; metadata syntax and numeric
lengths are bounded. This checks patch consistency, not correspondence with a
base/head checkout. Partial, metadata-only and unsupported patches require other
source evidence. Excerpt redaction preserves embedded control bytes as escapes;
ordinary CRLF is one physical line ending. Unquoted credential/header lines also
receive best-effort masking, which can hide benign configuration.
