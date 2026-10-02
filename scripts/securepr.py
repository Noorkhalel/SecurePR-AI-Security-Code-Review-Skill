#!/usr/bin/env python3
"""SecurePR static artifact helpers. No target execution, Git, network or plugins."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys

VERSION = '1.0.0'
MAX_FILE = 1024 * 1024
MAX_JSON = 4 * 1024 * 1024
MAX_DIFF = 2 * 1024 * 1024
MAX_ENTRIES = 10000
MAX_DEPTH = 32
MAX_EXCERPT_LINES = 200
MAX_LINE = 16384
MAX_EVIDENCE = 500
MAX_REVIEW_BYTES = 16 * 1024 * 1024
MAX_JSON_DEPTH = 64
EXCLUDED = {'.git', '.hg', '.svn', 'node_modules', '.next', '.venv', 'vendor',
            'dist', 'build', 'coverage', '__pycache__'}
EXTENSIONS = {'.js', '.jsx', '.mjs', '.cjs', '.ts', '.tsx', '.json', '.md',
              '.yaml', '.yml', '.sql', '.html', '.ejs', '.hbs', '.graphql'}
SEVERITIES = ['Critical', 'High', 'Medium', 'Low', 'Informational']
CONFIDENCES = ['CONFIRMED', 'HIGH CONFIDENCE', 'MEDIUM CONFIDENCE',
               'LOW CONFIDENCE / NEEDS MANUAL REVIEW']
RECOMMENDATIONS = ['No security blocker identified',
                   'Security issue should be reviewed before merge',
                   'Confirmed security issue should be fixed before merge']
SENSITIVE = re.compile(r'(?i)(?:secret|password|passwd|token|api[_-]?key|private[_-]?key|authorization|cookie)[\w\s\'".-]{0,128}[:=]\s*[\'"`]')
TOKEN = re.compile(r'(?:-----BEGIN .*PRIVATE KEY-----|\b(?:gh[pousr]_|github_pat_|AKIA|sk_live_)[A-Za-z0-9_]{8,}|\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)')


class Rejected(ValueError):
    """An artifact is invalid, unsupported or outside explicit limits."""


def relpath(value: str) -> tuple[str, ...]:
    if not isinstance(value, str) or not value or len(value) > 4096:
        raise Rejected('invalid relative path')
    if any(ord(c) < 32 or ord(c) == 127 for c in value) or '\\' in value or ':' in value:
        raise Rejected('path contains unsupported characters')
    parts = value.split('/')
    if value.startswith('/') or any(p in ('', '.', '..') for p in parts):
        raise Rejected('path must be a normalized relative POSIX path')
    return tuple(parts)


def excluded(parts: tuple[str, ...]) -> bool:
    return any(p in EXCLUDED or p.startswith('.env') or p in {'.ssh', '.aws', '.npmrc', '.netrc'}
               or p.lower().endswith(('.pem', '.key', '.p12', '.pfx', '.keystore')) for p in parts)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode(data: bytes) -> str:
    if b'\x00' in data:
        raise Rejected('binary/NUL content is unsupported')
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise Rejected('content must be UTF-8') from exc
    if any(len(line) > MAX_LINE for line in source_lines(text)):
        raise Rejected('line length exceeds limit')
    return text


def source_lines(text: str) -> list[str]:
    """Git/editor physical lines: LF with optional CR, never Unicode separators."""
    lines = text.split('\n')
    if lines[-1] == '':
        lines.pop()
    return [line[:-1] if line.endswith('\r') else line for line in lines]


def redacted_line(line: str) -> str:
    if SENSITIVE.search(line) or TOKEN.search(line):
        return '[REDACTED: potentially sensitive line]'
    # Escape invisible terminal controls without changing ordinary source text.
    return ''.join(c if (c in '\t' or (ord(c) >= 32 and ord(c) != 127
                    and not 0x202A <= ord(c) <= 0x202E
                    and not 0x2066 <= ord(c) <= 0x2069))
                   else f'\\u{ord(c):04x}' for c in line)


def safe_quote(text: str) -> str:
    out, private = [], False
    for line in source_lines(text):
        if re.search(r'-----BEGIN .*PRIVATE KEY-----', line):
            private = True
        out.append('[REDACTED: private key material]' if private else redacted_line(line))
        if private and re.search(r'-----END .*PRIVATE KEY-----', line):
            private = False
    return '\n'.join(out)


class SafeTree:
    """Descriptor-relative POSIX reads; never follow symlinks or open devices."""

    def __init__(self, root: str | Path):
        if os.name != 'posix' or not hasattr(os, 'O_NOFOLLOW'):
            raise Rejected('helpers require POSIX O_NOFOLLOW; use static host readers elsewhere')
        absolute = Path(os.path.abspath(root))
        fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
        try:
            for part in absolute.parts[1:]:
                nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                os.close(fd)
                fd = nxt
        except OSError as exc:
            os.close(fd)
            raise Rejected('root must be an accessible directory without symlink components') from exc
        self.fd = fd

    def __enter__(self):
        return self

    def __exit__(self, *args):
        os.close(self.fd)

    def _parent(self, parts: tuple[str, ...]) -> int:
        fd = os.dup(self.fd)
        try:
            for part in parts[:-1]:
                nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                os.close(fd)
                fd = nxt
            return fd
        except OSError:
            os.close(fd)
            raise

    def read(self, name: str, limit: int = MAX_FILE, *, allow_excluded: bool = False) -> bytes:
        if type(limit) is not int or not 0 < limit <= MAX_JSON:
            raise Rejected('invalid file byte budget')
        parts = relpath(name)
        if excluded(parts) and not allow_excluded:
            raise Rejected('path excluded by static-reading policy')
        parent = self._parent(parts)
        try:
            fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
        except OSError as exc:
            raise Rejected('file is inaccessible or is a symlink') from exc
        finally:
            os.close(parent)
        try:
            before = os.fstat(fd)
            if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
                raise Rejected('only regular files with one hard link are accepted')
            if before.st_size > limit:
                raise Rejected('file exceeds byte limit')
            chunks, count = [], 0
            while True:
                chunk = os.read(fd, min(65536, limit + 1 - count))
                if not chunk:
                    break
                count += len(chunk)
                if count > limit:
                    raise Rejected('file exceeds byte limit')
                chunks.append(chunk)
            after = os.fstat(fd)
            if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                raise Rejected('file changed during inspection; use an immutable snapshot')
            return b''.join(chunks)
        finally:
            os.close(fd)

    def inventory(self, max_entries: int = MAX_ENTRIES) -> dict:
        records, omissions, count = [], [], 0
        truncated = False

        def walk(fd: int, prefix: str, depth: int):
            nonlocal count, truncated
            if depth > MAX_DEPTH:
                omissions.append({'path': prefix, 'reason': 'depth limit'})
                return
            with os.scandir(fd) as entries:
                for entry in entries:
                    count += 1
                    if count > max_entries:
                        truncated = True
                        return
                    name = prefix + entry.name
                    try:
                        parts = relpath(name)
                        if excluded(parts):
                            omissions.append({'path': name, 'reason': 'excluded'})
                            continue
                        info = entry.stat(follow_symlinks=False)
                        if stat.S_ISDIR(info.st_mode):
                            child = os.open(entry.name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                            try:
                                walk(child, name + '/', depth + 1)
                            finally:
                                os.close(child)
                            if truncated:
                                return
                        elif stat.S_ISREG(info.st_mode) and info.st_nlink == 1:
                            suffix = PurePosixPath(name).suffix.lower()
                            if suffix not in EXTENSIONS and entry.name not in {'Dockerfile', 'Makefile'}:
                                omissions.append({'path': name, 'reason': 'unsupported extension'})
                            elif info.st_size > MAX_FILE:
                                omissions.append({'path': name, 'reason': 'byte limit'})
                            else:
                                records.append({'path': name, 'bytes': info.st_size})
                        else:
                            omissions.append({'path': name, 'reason': 'symlink, hard link or special file'})
                    except (OSError, Rejected):
                        omissions.append({'path': name, 'reason': 'unreadable or unsupported path'})
        walk(self.fd, '', 0)
        return {'files': sorted(records, key=lambda r: r['path']),
                'omissions': sorted(omissions, key=lambda r: r['path']),
                'truncated': truncated, 'entries_seen': min(count, max_entries),
                'notice': 'Metadata only; this is not a vulnerability scan. Content may still be unreadable.'}


def read_external(path: str | Path, limit: int = MAX_JSON) -> bytes:
    absolute = Path(os.path.abspath(path))
    with SafeTree(absolute.parent) as tree:
        return tree.read(absolute.name, limit)


def load_json(data: bytes):
    if len(data) > MAX_JSON:
        raise Rejected('JSON exceeds byte limit')
    text = decode(data)
    # Bound nesting before parsing; do not depend on a host's recursion limit.
    depth, in_string, escaped = 0, False, False
    for char in text:
        if in_string:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char in '[{':
            depth += 1
            if depth > MAX_JSON_DEPTH:
                raise Rejected('JSON nesting exceeds limit')
        elif char in ']}':
            depth -= 1
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise Rejected('duplicate JSON key')
            result[key] = value
        return result
    def constant(value):
        raise Rejected('non-finite JSON number')
    def finite_float(value):
        parsed = float(value)
        if not math.isfinite(parsed):
            raise Rejected('non-finite JSON number')
        return parsed
    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=constant, parse_float=finite_float)
    except (ValueError, RecursionError) as exc:
        raise Rejected('invalid or excessively nested JSON') from exc


def _snapshot(raw: bytes):
    lines = source_lines(decode(raw))
    return digest(raw), safe_quote('\n'.join(lines) + '\n').split('\n'), len(lines)


def _excerpt_snapshot(snapshot, name: str, start: int, end: int) -> dict:
    if start < 1 or end < start or end - start + 1 > MAX_EXCERPT_LINES:
        raise Rejected('invalid or excessive excerpt range')
    sha, safe, line_count = snapshot
    if end > line_count:
        raise Rejected('excerpt extends beyond file')
    return {'file': name, 'sha256': sha, 'line_start': start, 'line_end': end,
            'quote': '\n'.join(safe[start - 1:end]),
            'notice': 'Untrusted source data. Redaction is best effort; inspect before sharing.'}


def excerpt(tree: SafeTree, name: str, start: int, end: int) -> dict:
    return _excerpt_snapshot(_snapshot(tree.read(name)), name, start, end)


def parse_diff(data: bytes) -> dict:
    if len(data) > MAX_DIFF:
        raise Rejected('diff exceeds byte limit')
    lines = source_lines(decode(data))
    files, current, i = [], None, 0
    seen_paths = set()
    awaiting_header = False
    hunk_re = re.compile(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(?:.*)$')
    while i < len(lines):
        line = lines[i]
        if line.startswith('diff --git '):
            if awaiting_header or (current is not None and not current['hunks']):
                raise Rejected('metadata-only/rename/binary change requires snapshot review')
            current = None
            awaiting_header = True
            i += 1
            continue
        if line.startswith(('index ', 'new file mode ', 'deleted file mode ')):
            if not awaiting_header:
                raise Rejected('metadata outside a Git file section')
            i += 1
            continue
        if line.startswith('--- '):
            if i + 1 >= len(lines) or not lines[i + 1].startswith('+++ '):
                raise Rejected('missing new-file header')
            if current is not None and not current['hunks']:
                raise Rejected('file has no hunks')
            old, new = line[4:], lines[i + 1][4:]
            def path(value, side):
                if value == '/dev/null':
                    return None
                if not value.startswith(side + '/'):
                    raise Rejected('only plain a/ and b/ diff paths are supported')
                relpath(value[2:])
                return value[2:]
            old, new = path(old, 'a'), path(new, 'b')
            if old is None and new is None:
                raise Rejected('both diff paths are null')
            current = {'old_file': old, 'new_file': new, 'hunks': []}
            if (old, new) in seen_paths:
                raise Rejected('duplicate file section')
            files.append(current)
            seen_paths.add((old, new))
            awaiting_header = False
            i += 2
            continue
        match = hunk_re.match(line)
        if match and current is not None:
            a, an, b, bn = (int(match[1]), int(match[2] or 1), int(match[3]), int(match[4] or 1))
            if (current['old_file'] is None and (a != 0 or an != 0)) or (current['new_file'] is None and (b != 0 or bn != 0)):
                raise Rejected('null-file header contradicts hunk coordinates')
            if a > 10**9 or b > 10**9 or an > 100000 or bn > 100000 or (an and a < 1) or (bn and b < 1):
                raise Rejected('invalid hunk coordinates')
            if current['hunks']:
                prior = current['hunks'][-1]
                if a < prior['old_start'] + prior['old_count'] or b < prior['new_start'] + prior['new_count']:
                    raise Rejected('overlapping/out-of-order hunks')
            old_n = new_n = 0
            added, removed = [], []
            i += 1
            while i < len(lines) and (old_n < an or new_n < bn):
                body = lines[i]
                if body == '\\ No newline at end of file':
                    i += 1
                    continue
                if not body or body[0] not in ' +-':
                    raise Rejected('truncated or malformed hunk')
                if body[0] == '+':
                    added.append(b + new_n)
                    new_n += 1
                elif body[0] == '-':
                    removed.append(a + old_n)
                    old_n += 1
                else:
                    old_n += 1
                    new_n += 1
                if old_n > an or new_n > bn:
                    raise Rejected('hunk count mismatch')
                i += 1
            if (old_n, new_n) != (an, bn):
                raise Rejected('truncated hunk')
            current['hunks'].append({'old_start': a, 'old_count': an, 'new_start': b,
                                     'new_count': bn, 'added_lines': added, 'removed_lines': removed})
            continue
        if line == '\\ No newline at end of file' and current and current['hunks']:
            i += 1
            continue
        if not line and not files:
            i += 1
            continue
        raise Rejected('unsupported or malformed diff; inspect snapshots and connector metadata')
    if awaiting_header or (current is not None and not current['hunks']):
        raise Rejected('file has no hunks')
    if not files and lines:
        raise Rejected('diff contains no supported changes')
    return {'files': files, 'notice': 'Coordinates only; context, binary and metadata changes require separate review.'}


def _object(value, keys, label):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise Rejected(f'{label}: unexpected or missing fields')


def _text(value, label):
    if not isinstance(value, str) or not value.strip() or len(value) > 20000:
        raise Rejected(f'{label}: expected bounded nonempty text')


def _strings(value, label, nonempty=False):
    if not isinstance(value, list) or len(value) > 200 or (nonempty and not value):
        raise Rejected(f'{label}: expected bounded list')
    for v in value:
        _text(v, label)


def validate_evidence(tree, evidence, scope, cache, budget):
    if not isinstance(evidence, list) or not 1 <= len(evidence) <= 30:
        raise Rejected('finding needs bounded evidence')
    for e in evidence:
        _object(e, {'file', 'line_start', 'line_end', 'sha256', 'quote'}, 'evidence')
        if not isinstance(e['file'], str) or e['file'] not in scope:
            raise Rejected('evidence file is outside declared reviewed scope')
        if type(e['line_start']) is not int or type(e['line_end']) is not int:
            raise Rejected('evidence line numbers must be integers')
        if e['file'] not in cache:
            raw = tree.read(e['file'])
            budget[0] += len(raw)
            if budget[0] > MAX_REVIEW_BYTES:
                raise Rejected('aggregate evidence byte budget exceeded; split the review')
            cache[e['file']] = _snapshot(raw)
        actual = _excerpt_snapshot(cache[e['file']], e['file'], e['line_start'], e['line_end'])
        for k in ('sha256', 'quote'):
            if e[k] != actual[k]:
                raise Rejected('evidence quote/hash mismatch or unredacted evidence')


def validate_report(tree: SafeTree, report: dict) -> dict:
    _object(report, {'version', 'mode', 'revision', 'scope', 'summary', 'findings',
                     'manual_review', 'coverage_gaps', 'recommendation'}, 'report')
    if report['version'] != VERSION or report['mode'] not in ('pr', 'full', 'snippet'):
        raise Rejected('unsupported report version/mode')
    _text(report['revision'], 'revision')
    _text(report['summary'], 'summary')
    _strings(report['scope'], 'scope', True)
    if len(set(report['scope'])) != len(report['scope']):
        raise Rejected('duplicate scope path')
    for p in report['scope']:
        relpath(p)
    _strings(report['coverage_gaps'], 'coverage_gaps')
    for name in ('findings', 'manual_review'):
        if not isinstance(report[name], list) or len(report[name]) > 200:
            raise Rejected('invalid finding/manual-review list')
    evidence_count = sum(len(f.get('evidence', [])) for f in report['findings']
                         if isinstance(f, dict) and isinstance(f.get('evidence'), list))
    if evidence_count > MAX_EVIDENCE:
        raise Rejected('aggregate evidence count budget exceeded; split the review')
    cache, budget = {}, [0]
    ids = set()
    for f in report['findings']:
        keys = {'id', 'title', 'severity', 'severity_rationale', 'confidence', 'confidence_rationale',
                'cwe', 'owasp', 'function', 'evidence', 'source', 'data_flow', 'sink',
                'missing_control', 'controls_checked', 'preconditions', 'attack_scenario',
                'impact', 'remediation', 'regression_test', 'context_required', 'introduced_by', 'basis'}
        _object(f, keys, 'finding')
        if not isinstance(f['id'], str) or not re.fullmatch(r'(?:CRITICAL|HIGH|MEDIUM|LOW|INFO)-[0-9]{2,4}', f['id']) or f['id'] in ids:
            raise Rejected('invalid or duplicate finding ID')
        ids.add(f['id'])
        if f['severity'] not in SEVERITIES or f['confidence'] not in CONFIDENCES[:2] or f['basis'] != 'static':
            raise Rejected('invalid severity/confidence/basis; uncertain issues belong in manual_review')
        for key in ('title', 'severity_rationale', 'confidence_rationale', 'source', 'sink',
                    'missing_control', 'attack_scenario', 'impact', 'remediation', 'regression_test'):
            _text(f[key], key)
        for key in ('data_flow', 'controls_checked', 'preconditions'):
            _strings(f[key], key, True)
        _strings(f['context_required'], 'context_required')
        if f['confidence'] == 'CONFIRMED' and f['context_required']:
            raise Rejected('confirmed finding cannot have essential missing context')
        if f['confidence'] == 'HIGH CONFIDENCE' and not f['context_required']:
            raise Rejected('high-confidence finding must name its unresolved premise')
        if f['cwe'] is not None and (not isinstance(f['cwe'], str) or not re.fullmatch(r'CWE-[1-9][0-9]{0,4}', f['cwe'])):
            raise Rejected('invalid CWE syntax')
        for key in ('owasp', 'function'):
            if f[key] is not None:
                _text(f[key], key)
        if report['mode'] == 'pr':
            _text(f['introduced_by'], 'PR causal change relationship')
        elif f['introduced_by'] is not None:
            raise Rejected('introduced_by only applies in PR mode')
        validate_evidence(tree, f['evidence'], report['scope'], cache, budget)
    for item in report['manual_review']:
        _object(item, {'title', 'confidence', 'reason', 'context_required'}, 'manual review')
        _text(item['title'], 'title')
        _text(item['reason'], 'reason')
        if item['confidence'] not in CONFIDENCES[2:]:
            raise Rejected('manual-review confidence must be medium or low')
        _strings(item['context_required'], 'context_required', True)
    recommendation = report['recommendation']
    if report['mode'] != 'pr':
        if recommendation is not None:
            raise Rejected('merge recommendation is PR-only')
    else:
        if recommendation not in RECOMMENDATIONS:
            raise Rejected('invalid merge recommendation')
        material = [f for f in report['findings'] if f['severity'] != 'Informational']
        confirmed = any(f['confidence'] == 'CONFIRMED' for f in material)
        if confirmed and recommendation != RECOMMENDATIONS[2]:
            raise Rejected('confirmed PR finding contradicts merge recommendation')
        if not confirmed and recommendation == RECOMMENDATIONS[2]:
            raise Rejected('merge blocker claims confirmation without a confirmed material finding')
        if (material or report['coverage_gaps'] or report['manual_review']) and recommendation == RECOMMENDATIONS[0]:
            raise Rejected('unresolved PR evidence/context cannot produce a clean automated recommendation')
    return {'valid': True, 'findings': len(report['findings']),
            'notice': 'Structure and quoted evidence verified. Reasoning, CWE semantics, completeness and revision identity need human/agent review.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version', version=VERSION)
    sub = parser.add_subparsers(dest='command', required=True)
    inv = sub.add_parser('inventory', help='bounded metadata inventory; no detection')
    inv.add_argument('root')
    exc = sub.add_parser('excerpt', help='redacted, hashed source excerpt')
    exc.add_argument('root'); exc.add_argument('file')
    exc.add_argument('--start', type=int, required=True); exc.add_argument('--end', type=int, required=True)
    diff = sub.add_parser('diff', help='parse a supplied plain unified patch')
    diff.add_argument('patch')
    report = sub.add_parser('validate-report', help='check structure and quote/hash evidence')
    report.add_argument('root'); report.add_argument('report')
    args = parser.parse_args(argv)
    try:
        if args.command == 'diff':
            result = parse_diff(read_external(args.patch, MAX_DIFF))
        else:
            with SafeTree(args.root) as tree:
                if args.command == 'inventory':
                    result = tree.inventory()
                elif args.command == 'excerpt':
                    result = excerpt(tree, args.file, args.start, args.end)
                else:
                    result = validate_report(tree, load_json(read_external(args.report)))
        print(json.dumps(result, ensure_ascii=True, indent=2, allow_nan=False))
        return 0
    except (Rejected, OSError, RecursionError, TypeError) as exc:
        # Do not echo arbitrary source or OS error paths into diagnostics.
        message = str(exc) if isinstance(exc, Rejected) else 'artifact inaccessible or exceeds safe processing limits'
        print(json.dumps({'error': message}, ensure_ascii=True), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
