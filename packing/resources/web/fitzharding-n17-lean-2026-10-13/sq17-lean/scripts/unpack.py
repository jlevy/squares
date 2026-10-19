#!/usr/bin/env python3
"""Authenticate the source release and safely extract its listed Lean modules."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import tarfile
import tempfile


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def destination(root, name):
    p = PurePosixPath(name)
    if not name or '\\' in name or p.is_absolute() or any(s in ('', '.', '..') for s in name.split('/')):
        raise ValueError(f'Unsafe path: {name!r}')
    dest = root.joinpath(*p.parts)
    for part in [dest, *dest.parents]:
        if part == root: break
        if part.is_symlink(): raise ValueError(f'Symlink destination: {name}')
    if not dest.resolve().is_relative_to(root):
        raise ValueError(f'Destination outside release: {name}')
    return dest


def verify_file(root, name, info):
    p = destination(root, name)
    if not p.is_file() or p.stat().st_size != info['bytes'] or sha(p) != info['sha256']:
        raise ValueError(f'File checksum mismatch or missing file: {name}')


def consume(root, name, info, stream, verify_only):
    dest = destination(root, name)
    if not name.startswith('Sq17Lean/') or not name.endswith('.lean'):
        raise ValueError(f'Archive member is not a Lean module: {name}')
    temp = None
    try:
        if not verify_only:
            dest.parent.mkdir(parents=True, exist_ok=True)
            temp = tempfile.NamedTemporaryFile(mode='wb', prefix='.source-', dir=dest.parent, delete=False)
        h = hashlib.sha256(); size = 0
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            size += len(chunk)
            if size > info['bytes']: raise ValueError(f'Excess data in {name}')
            h.update(chunk)
            if temp: temp.write(chunk)
        if size != info['bytes'] or h.hexdigest() != info['sha256']:
            raise ValueError(f'Archived source checksum mismatch: {name}')
        if temp:
            temp.close()
            os.replace(temp.name, dest)
    finally:
        if temp:
            temp.close()
            Path(temp.name).unlink(missing_ok=True)


def verify_archive(root, name, info, sources, verify_only):
    verify_file(root, name, info)
    expected = {p:s for p,s in sources.items() if s.get('archive') == name}
    if len(expected) != info['members']:
        raise ValueError(f'Manifest member count mismatch: {name}')
    seen = set()
    def member(path, size, regular, stream):
        if path not in expected or path in seen or not regular:
            raise ValueError(f'Unexpected, repeated or nonregular archive member: {path}')
        if size != expected[path]['bytes']:
            raise ValueError(f'Archive member size mismatch: {path}')
        seen.add(path)
        consume(root, path, expected[path], stream, verify_only)
    archive = destination(root, name)
    if info['format'] in ('tar.gz', 'tar.xz'):
        with tarfile.open(archive, 'r|gz' if info['format'] == 'tar.gz' else 'r|xz') as tf:
            for m in tf:
                if not m.isfile(): raise ValueError(f'Nonregular tar member: {m.name}')
                with tf.extractfile(m) as f: member(m.name, m.size, m.isfile(), f)
    else:
        raise ValueError(f'Unknown archive format: {info["format"]}')
    if seen != set(expected): raise ValueError(f'Missing archive members: {name}')
    print(f'VERIFIED {name}: {len(seen)} source modules', flush=True)


def verify(root, verify_only=False, allow_incomplete=False):
    root = root.resolve()
    manifest = json.loads((root / 'manifest.json').read_text())
    if manifest['schema'] != 'sq17-source-release-v1': raise ValueError('Unknown manifest schema')
    if allow_incomplete and not verify_only: raise ValueError('Incomplete releases may only be inspected, not extracted')
    pending = [p for p,s in manifest['sources'].items() if s['status'] != 'ready']
    if (pending or manifest['status'] != 'complete') and not allow_incomplete:
        raise ValueError(f'Incomplete release: {len(pending)} source modules still pending')
    modules = {s['module'] for s in manifest['sources'].values()}
    if manifest['entry'] not in modules: raise ValueError('Missing entry module')
    for name, info in manifest['sources'].items():
        if name != info['module'].replace('.', '/') + '.lean':
            raise ValueError(f'Noncanonical module path: {name}')
        for imported in info['imports']:
            if imported.startswith('Sq17Lean.') and imported not in modules:
                raise ValueError(f'Missing imported source: {imported}')
            if not imported.startswith('Sq17Lean.') and imported not in manifest['external_imports']:
                raise ValueError(f'Unlisted external import: {imported}')
    for name, info in manifest['files'].items(): verify_file(root, name, info)
    for name, info in manifest['sources'].items():
        destination(root, name)
        if info['status'] == 'ready' and info['archive'] is None: verify_file(root, name, info)
    for name, info in manifest['archives'].items():
        if info['status'] == 'ready':
            verify_archive(root, name, info, manifest['sources'], verify_only)
        elif not allow_incomplete:
            raise ValueError(f'Archive still pending: {name}')
    if pending:
        print(f'PARTIAL_SOURCE_VERIFICATION: {len(pending)} source modules pending; release is not complete')
    else:
        print(f'SOURCE_RELEASE_VERIFIED: {len(manifest["sources"])} source modules')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent)
    p.add_argument('--verify-only', action='store_true')
    p.add_argument('--allow-incomplete', action='store_true', help='verification-only inventory check during release assembly')
    a = p.parse_args()
    verify(a.root, a.verify_only, a.allow_incomplete)


if __name__ == '__main__': main()
