#!/usr/bin/env python3
"""Source-only replay driver. Run from a release root; does not fetch certificates.

Requires the complete source/certificate release, Lean 4.34.1, its leanc compiler,
and Mathlib's pinned dependencies (`lake exe cache get` before the build).
No search engine is used. Every generated certificate is checked again by Lean.
"""
import argparse
import concurrent.futures as cf
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

FAST = ['HalfPlaneFast', 'CaptureRunFast', 'CaptureTableFast',
        'HalfPlaneCoverFast', 'CaptureSummaryFast']
FINAL = 'Sq17Lean.Square17Optimality'


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def run(cmd, log=None):
    print('RUN', ' '.join(map(str, cmd)), flush=True)
    if log:
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open('w') as f:
            result = subprocess.run(list(map(str, cmd)), stdout=f, stderr=subprocess.STDOUT)
        text = log.read_text(errors='replace')
        if result.returncode or re.search(r'error:|sorryAx|uses .sorry.', text):
            raise RuntimeError(f'Failed; inspect {log}')
    else:
        subprocess.run(list(map(str, cmd)), check=True)


def imports(p):
    # Read the actual import header, handling nested block comments and line comments.
    depth = 0
    result = []
    with p.open() as f:
        for line in f:
            visible = ''; i = 0
            while i < len(line):
                if line[i:i+2] == '/-': depth += 1; i += 2
                elif depth and line[i:i+2] == '-/': depth -= 1; i += 2
                elif depth: i += 1
                elif line[i:i+2] == '--': break
                else: visible += line[i]; i += 1
            text = visible.strip()
            if not text or text == 'prelude': continue
            m = re.fullmatch(r'(?:(?:public|meta|private)\s+)*import\s+([\w.]+)', text)
            if not m: break
            result.append(m[1])
    return result


def build(jobs, proof_jobs):
    """Build the transitive closure, bounded separately for core and Mathlib jobs."""
    lib = Path('.lake/build/lib/lean').resolve()
    ir = Path('.lake/build/ir/Sq17Lean').resolve()
    logs = Path('reproduction/logs/build')
    stamps = Path('reproduction/stamps'); stamps.mkdir(parents=True, exist_ok=True)
    ir.mkdir(parents=True, exist_ok=True); (lib / 'Sq17Lean').mkdir(parents=True, exist_ok=True)
    lean = Path(subprocess.check_output(['elan', 'which', 'lean'], text=True).strip())
    leanc = lean.with_name('leanc')
    lean_path = subprocess.check_output(['lake', 'env', 'printenv', 'LEAN_PATH'], text=True).strip()
    os.environ['LEAN_PATH'] = str(lib) + os.pathsep + lean_path
    version = subprocess.check_output([lean, '--version'], text=True).strip()
    if '4.34.1' not in version:
        raise RuntimeError(f'Unexpected Lean version: {version}')
    ext = '.dylib' if sys.platform == 'darwin' else '.so'
    native = []
    # Rebuild native libraries every invocation. No binary cache is publication input.
    for name in FAST:
        p = Path('Sq17Lean') / (name + '.lean')
        o = lib / 'Sq17Lean' / (name + '.olean')
        run([lean, p, '-o', o, '-i', o.with_suffix('.ilean'), '-c', ir / (name + '.c')], logs / (name + '.log'))
        run([leanc, '-c', ir / (name + '.c'), '-o', ir / (name + '.o'), '-O3', '-DNDEBUG', '-DLEAN_EXPORTING', '-fPIC'])
        so = lib / ('Sq17Lean_' + name + ext)
        args = [leanc, '-shared', '-o', so, ir / (name + '.o')]
        if sys.platform == 'darwin':
            tc = lean.parent.parent
            args += ['-L', tc / 'lib/lean', '-L', tc / 'lib', '-Wl,-undefined,dynamic_lookup', '-Wl,-no_fixup_chains', '-lgmp']
        run(args); native.append(so)
    files = {}; deps = {}; core = {}; active = set()
    done = {'Sq17Lean.' + name for name in FAST}
    def visit(m):
        if m in active: raise RuntimeError(f'Import cycle: {m}')
        if m in deps or m in done: return
        active.add(m)
        p = source(m); im = imports(p)
        files[m] = p; deps[m] = [d for d in im if d.startswith('Sq17Lean.')]
        for d in deps[m]: visit(d)
        core[m] = all(d.startswith('Sq17Lean.') and (d in done or core[d]) for d in im)
        active.remove(m)
    visit(FINAL)
    native_key = {str(p): sha(p) for p in native}
    configuration = {name:sha(Path(name)) for name in
                     ['lean-toolchain', 'lake-manifest.json', 'lakefile.toml', 'lakefile.lean']
                     if Path(name).exists()}
    configuration['driver'] = sha(Path(__file__))
    def one(m):
        p = files[m]; o = lib / (m.replace('.', '/') + '.olean')
        o.parent.mkdir(parents=True, exist_ok=True)
        log = logs / (m + '.log'); stamp = stamps / (m + '.json')
        key = dict(source=sha(p), imports={d:sha(lib / (d.replace('.', '/') + '.olean')) for d in deps[m]},
                   native=native_key, lean=version, configuration=configuration)
        if stamp.exists() and o.exists():
            try:
                old = json.loads(stamp.read_text())
            except (OSError, ValueError):
                old = {}
            if not isinstance(old, dict):
                old = {}
            if old.get('input') == key and old.get('olean') == sha(o): return
        o.unlink(missing_ok=True)
        stamp.unlink(missing_ok=True)
        try:
            run([lean, *['--load-dynlib=' + str(n) for n in native], p,
                 '-o', o, '-i', o.with_suffix('.ilean')], log)
        except Exception:
            o.unlink(missing_ok=True)
            o.with_suffix('.ilean').unlink(missing_ok=True)
            raise
        if not o.exists(): raise RuntimeError(f'No olean from {m}')
        tmp = stamp.with_suffix('.json.tmp')
        tmp.write_text(json.dumps(dict(input=key, olean=sha(o)), sort_keys=True) + '\n')
        tmp.replace(stamp)
    pending = set(deps); running = {}
    with cf.ThreadPoolExecutor(jobs + proof_jobs) as pool:
        while pending or running:
            for m in sorted(pending):
                if not all(d in done for d in deps[m]): continue
                count = sum(core[q] == core[m] for q in running.values())
                if count >= (jobs if core[m] else proof_jobs): continue
                running[pool.submit(one, m)] = m; pending.remove(m)
            if not running: raise RuntimeError('Unresolved imports: ' + ', '.join(sorted(pending)[:10]))
            finished, _ = cf.wait(running, return_when=cf.FIRST_COMPLETED)
            for fut in finished:
                m = running.pop(fut); fut.result(); done.add(m)
    print('REPRODUCTION_ACCEPTED', FINAL)
    print('Final statement and axiom report:', logs / (FINAL + '.log'))


def source(module):
    p = Path(module.replace('.', '/') + '.lean')
    if not p.is_file():
        raise FileNotFoundError(f'Missing source for {module}; run scripts/unpack.py first.')
    return p


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('phase', choices=['build'])
    p.add_argument('--root', type=Path, default=Path.cwd())
    p.add_argument('--jobs', type=int, default=1)
    p.add_argument('--proof-jobs', type=int, default=1)
    a = p.parse_args()
    if a.jobs < 1 or a.proof_jobs < 1: p.error('Job counts must be positive.')
    os.chdir(a.root.resolve())
    build(a.jobs, a.proof_jobs)


if __name__ == '__main__': main()
