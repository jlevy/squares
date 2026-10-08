#!/usr/bin/env python3
"""Check the local import graph, exact admissions, and portable source layout."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
from native_certificates import (load_native_manifest, validate_native_source,
                                 restore_kernel_source)
from native_data_compatibility import load_manifest as load_native_data_manifest, upstream_bytes
from split_indexed_data import reconstruct_inputs as reconstruct_indexed_data
from t07_proof_shape import check_row_block_proof

ROOT = Path(__file__).resolve().parents[1]
_IMPORT_CACHE = {}
_CODE_DELIMITER = re.compile(r'/-|--|"')
_COMMENT_DELIMITER = re.compile(r'/-|-/')
_STRING_DELIMITER = re.compile(r'\\[\s\S]?|"')
_NON_NEWLINES = re.compile(r'[^\n]+')
_HEADER_PREFIX = re.compile(r'\s*(?:module\s+)?(?:prelude\s+)?')
_IMPORT_DECL = re.compile(
    r'\s*(?:public\s+)?(?:meta\s+)?import\s+(?:all\s+)?((?:[^\s«»]|«[^»]*»)+)')


def _blank(text):
    return _NON_NEWLINES.sub(lambda match: ' ' * (match.end() - match.start()), text)


def code_only(text):
    """Blank nested Lean comments and strings while preserving line numbers."""
    # Search whole code spans in C instead of storing one Python list entry per
    # character: generated numeric certificate files contain very few delimiters.
    out = []
    i = 0
    while match := _CODE_DELIMITER.search(text, i):
        start = match.start()
        out.append(text[i:start])
        delimiter = match.group()
        i = match.end()
        if delimiter == '--':
            end = text.find('\n', i)
            end = len(text) if end < 0 else end
            out.append(' ' * (end - start))
            i = end
        elif delimiter == '/-':
            depth = 1
            while depth:
                match = _COMMENT_DELIMITER.search(text, i)
                if match is None:
                    raise ValueError('Unterminated comment or string')
                depth += 1 if match.group() == '/-' else -1
                i = match.end()
            out.append(_blank(text[start:i]))
        else:
            out.append(' ')
            while True:
                match = _STRING_DELIMITER.search(text, i)
                if match is None:
                    raise ValueError('Unterminated comment or string')
                out.append(_blank(text[i:match.start()]))
                # Preserve the old scanner's escape handling, including its
                # replacement of an escaped newline with a space.
                out.append(' ' * (match.end() - match.start()))
                i = match.end()
                if match.group() == '"':
                    break
    out.append(text[i:])
    return ''.join(out)


def import_names(code):
    """Read the Lean 4.34 header from comment/string-masked source code."""
    # Header whitespace is not restricted to newlines or column zero. Each
    # declaration imports one name; subsequent imports can share the same line.
    i = _HEADER_PREFIX.match(code).end()
    names = []
    while match := _IMPORT_DECL.match(code, i):
        names.append(match[1].replace('«', '').replace('»', ''))
        i = match.end()
    return names


def imports(path):
    if path not in _IMPORT_CACHE:
        _IMPORT_CACHE[path] = import_names(code_only(path.read_text(encoding='utf-8')))
    return _IMPORT_CACHE[path]


def check(use_cache=False):
    # The standalone audit and --fresh always rescan. Resumed compilations may
    # reuse lexical results only when both the scanner and source bytes match.
    cache_path = ROOT / '.verification/source-scan.json'
    native_manifest = load_native_manifest(ROOT)
    # Authenticate the exact inverse of compilation-sized indexed data helpers.
    # This checks literals and row order against the original source receipt.
    reconstruct_indexed_data(ROOT)
    native_data = load_native_data_manifest(ROOT)
    for rel, entry in native_data.items():
        path = ROOT / rel
        if (not path.is_file() or any((ROOT / Path(*Path(rel).parts[:i])).is_symlink()
                                    for i in range(1, len(Path(rel).parts) + 1))):
            raise ValueError('Missing or nonregular native data source: ' + rel)
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != entry['sha256']:
            raise ValueError('Native data source hash mismatch: ' + rel)
        upstream_bytes(rel, raw, entry['upstream_sha256'], root=ROOT)
    # Native permissions are source-bound. A policy change must also invalidate
    # a cached lexical scan even when no Lean source changed.
    scanner = hashlib.sha256(Path(__file__).read_bytes() +
        Path(__file__).with_name('native_certificates.py').read_bytes() +
        Path(__file__).with_name('native_data_compatibility.py').read_bytes() +
        Path(__file__).with_name('t07_proof_shape.py').read_bytes() +
        json.dumps(native_manifest, sort_keys=True).encode() +
        json.dumps(native_data, sort_keys=True).encode()).hexdigest()
    cache = {}
    if use_cache and cache_path.is_file():
        try:
            saved = json.loads(cache_path.read_text(encoding='utf-8'))
            if saved.get('scanner') == scanner:
                cache = saved.get('files', {})
        except (ValueError, OSError):
            pass
    next_cache = {}
    files = sorted((ROOT / 'ElevenSquare').rglob('*.lean')) + sorted((ROOT / 'Sqpack').rglob('*.lean')) + [ROOT / 'ElevenSquare.lean', ROOT / 'Sqpack.lean']
    modules = {'.'.join(p.relative_to(ROOT).with_suffix('').parts): p for p in files}
    found = []
    for p in files:
        rel = p.relative_to(ROOT).as_posix()
        data = p.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        info = cache.get(rel, {})
        if info.get('sha256') != digest:
            code = code_only(data.decode())
            # Catch the known generated exact-block sequencing error before
            # starting the long Lean replay. This is not a general proof check.
            check_row_block_proof(rel, code)
            for word in ['axiom', 'admit', 'sorryAx']:
                if word in code and re.search(r'\b' + word + r'\b', code):
                    raise ValueError('Forbidden local proof form in ' + rel + ': ' + word)
            native = validate_native_source(rel, data, native_manifest)
            # A recorded pre-migration hash is a checked inverse, not merely
            # provenance text. Revalidate when sources or policy change.
            if 'kernel_sha256' in native_manifest['files'].get(rel, {}):
                restore_kernel_source(rel, data, native_manifest)
            info = {'sha256': digest,
                    'imports': import_names(code),
                    'native_declarations': native,
                    'admissions': [code.count('\n', 0, m.start()) + 1
                                   for m in re.finditer(r'\bsorry\b', code)] if 'sorry' in code else []}
        _IMPORT_CACHE[p] = info['imports']
        next_cache[rel] = info
        found.extend({'path': rel, 'line': line} for line in info['admissions'])
        for dep in imports(p):
            if dep.startswith(('ElevenSquare', 'Sqpack')) and dep not in modules:
                raise ValueError('Missing local import: ' + dep)
    expected = json.loads((ROOT / 'verification/admissions.json').read_text(encoding='utf-8'))['sites']
    missing_native = set(native_manifest.get('files', {})) - set(next_cache)
    if missing_native:
        raise ValueError('Missing inventoried native certificate sources: ' +
                         ', '.join(sorted(missing_native)))
    sort = lambda xs: sorted(xs, key=lambda x: (x['path'], x['line']))
    if sort(found) != sort(expected):
        raise ValueError('Admission inventory changed; review and update MISSING.md and admissions.json.')
    active = set(); done = set()
    def visit(name):
        if name in done: return
        if name in active: raise ValueError('Local import cycle: ' + name)
        active.add(name)
        for dep in imports(modules[name]):
            if dep in modules: visit(dep)
        active.remove(name); done.add(name)
    for name in modules: visit(name)
    if use_cache:
        cache_path.parent.mkdir(exist_ok=True)
        temporary = cache_path.with_name(cache_path.name + f'.{os.getpid()}.tmp')
        temporary.write_text(json.dumps({'scanner': scanner, 'files': next_cache}), encoding='utf-8')
        temporary.replace(cache_path)
    return {'status': 'SOURCE_ASSEMBLY_PASS', 'local_modules': len(modules),
            'explicit_admissions': len(found),
            'native_certificate_declarations': sum(len(info.get('native_declarations', []))
                                                   for info in next_cache.values()),
            'global_optimality_proved': False}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
