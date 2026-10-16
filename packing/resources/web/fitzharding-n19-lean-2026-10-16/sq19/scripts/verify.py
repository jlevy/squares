#!/usr/bin/env python3
"""Build Sq19.square19_optimality from source and check its axioms.

    python3 scripts/verify.py [--jobs N] [--kernel-replay]

Run `bash scripts/fetch.sh` first. Linux x86-64 with elan and libgmp.
Steps:
  1. `lake exe cache get` fetches Mathlib's build cache and the pinned sq17-lean.
  2. Hand-written modules that do not depend on generated certificates are built
     by `lake build` (with the lakefile's options), including the C code of the
     six checker modules (`*Fast`), which is linked into one native library.
  3. The generated certificate modules (about 2,000) and every module above them
     are compiled with `lean`, loading that library so that `native_decide` runs
     compiled code, in dependency order and in parallel.
  4. The theorem's statement and axioms are compared with `expected/`.
  5. With --kernel-replay, every module of the import closure, Mathlib included,
     is replayed through Lean's kernel (Lean's own LeanChecker.replayFromImports).
Interrupted runs resume: modules already compiled from the same source are kept.
"""
import argparse, concurrent.futures as cf, hashlib, heapq, os, pathlib, re, subprocess, sys, threading, time

R = pathlib.Path(__file__).resolve().parents[1]
B = R / 'build/verify'; OUT = R / '.lake/build/lib/lean'; LOGS = B / 'logs'
P = R / '.lake/packages/sq17-lean'
ROOTS = {'Sq19Lean': R, 'Sq17Lean': P}
CANON = R / 's19/certificates/endgame_reduction/canonical'
ASSEM = R / 's19/certificates/endgame_reduction/assembly'
FAST = ['Sq17Lean.HalfPlaneFast', 'Sq17Lean.HalfPlaneCoverFast', 'Sq17Lean.CaptureSummaryFast',
        'Sq17Lean.CaptureRunFast', 'Sq17Lean.CaptureTableFast', 'Sq19Lean.Capture.SummaryFast']
TARGET = 'Sq19Lean.Assembly.Optimality'

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
mem_gb = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / 2**30
ap.add_argument('--jobs', type=int, default=max(1, min(os.cpu_count() or 1, int(mem_gb // 6))))
ap.add_argument('--kernel-replay', action='store_true')
a = ap.parse_args()

def say(*s): print(time.strftime('%H:%M:%S'), *s, flush=True)
def run(cmd, **kw): return subprocess.run(cmd, cwd=R, check=True, text=True, capture_output=True, **kw).stdout
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

say('lake exe cache get (Mathlib build cache, pinned dependencies)')
subprocess.run(['lake', 'exe', 'cache', 'get'], cwd=R, check=True)
LEAN = 'lean'  # elan selects the toolchain pinned in lean-toolchain
PREFIX = pathlib.Path(run([LEAN, '--print-prefix']).strip())
version = run([LEAN, '--version'])
if 'version 4.34.1' not in version: sys.exit('Lean 4.34.1 required, found: ' + version)
LEAN_PATH = run(['lake', 'env', 'printenv', 'LEAN_PATH']).strip()
base = [pathlib.Path(p) for p in LEAN_PATH.split(':') if p] + [PREFIX / 'lib/lean']
LOGS.mkdir(parents=True, exist_ok=True)
ENV = {**os.environ, 'LEAN_PATH': LEAN_PATH, 'LEAN_NUM_THREADS': '1'}
GENERATED = {l.split('  ', 1)[1].strip() for l in (R / 'expected/generated-sources.sha256').read_text().splitlines() if l.strip()}

def source(m):
    top = m.split('.')[0]
    if top in ROOTS: return ROOTS[top], ROOTS[top] / (m.replace('.', '/') + '.lean')
    if re.fullmatch(r'Shard\d+', m): return CANON, CANON / (m + '.lean')
    if re.fullmatch(r'Block\d+', m) or m == 'CertifiedHull': return ASSEM, ASSEM / (m + '.lean')
    return None, None
def external_ok(m):  # Lean's rule: first search root holding the package decides
    top = m.split('.')[0]
    for d in base:
        if (d / top).is_dir() or (d / (top + '.olean')).exists():
            return (d / (m.replace('.', '/') + '.olean')).exists()
    return False
def imports(path):
    out = []
    for line in path.read_text().splitlines():
        s = line.split('--')[0].split()
        if s[:1] == ['import']: out += s[1:]
    return out

deps, todo = {}, [TARGET, 'Sq19Lean.Assembly.FinalReport']
while todo:
    m = todo.pop()
    if m in deps: continue
    root, src = source(m)
    if src is None:
        if not external_ok(m): sys.exit(f'missing dependency object {m}: did `lake exe cache get` succeed?')
        continue
    if not src.is_file(): sys.exit(f'missing source {src}: run `bash scripts/fetch.sh` first')
    deps[m] = [d for d in imports(src) if source(d)[1] is not None]
    todo += imports(src)
gen = {m for m in deps if str(source(m)[1].relative_to(R)) in GENERATED}
above = set(gen)  # generated modules and everything that imports them
changed = True
while changed:
    changed = False
    for m, ds in deps.items():
        if m not in above and any(d in above for d in ds): above.add(m); changed = True
lake_mods = sorted(set(deps) - above)
assert not set(FAST) & above, 'checker modules must not depend on generated code'
say(f'{len(deps)} project modules: {len(lake_mods)} via lake build, {len(above)} certificate-level via lean')

LIB = B / 'checkers.so'
lock = threading.Lock(); done_count = [0]
def compile_one(m, with_lib):
    root, src = source(m)
    dst = OUT / (m.replace('.', '/') + '.olean'); dst.parent.mkdir(parents=True, exist_ok=True)
    log, ok = LOGS / (m + '.log'), LOGS / (m + '.ok')
    stamp = sha(src) + (' lib ' + sha(LIB) if with_lib else '')
    if ok.exists() and dst.exists() and ok.read_text() == stamp: return m, 0.0, True
    cmd = [LEAN] + (['--load-dynlib=' + str(LIB)] if with_lib else []) + ['-R', str(root), str(src), '-o', str(dst)]
    t = time.time()
    with log.open('w') as f: rc = subprocess.run(cmd, cwd=R, env=ENV, stdout=f, stderr=subprocess.STDOUT).returncode
    text = log.read_text()
    if rc or re.search(r'\berror:|declaration uses .sorry.|sorryAx', text):
        raise RuntimeError(f'{m} failed (exit {rc}); see {log}')
    ok.write_text(stamp)
    return m, time.time() - t, False

def build(mods, with_lib):
    mods = set(mods); waiting = {m: {d for d in deps[m] if d in mods} for m in mods}
    users = {m: [] for m in mods}
    for m, ds in waiting.items():
        for d in ds: users[d].append(m)
    ready = [(-source(m)[1].stat().st_size, m) for m, ds in waiting.items() if not ds]; heapq.heapify(ready)
    running = {}
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as pool:
        while ready or running:
            while ready and len(running) < a.jobs:
                _, m = heapq.heappop(ready); running[pool.submit(compile_one, m, with_lib)] = m
            fin, _ = cf.wait(running, return_when=cf.FIRST_COMPLETED)
            for f in fin:
                m = running.pop(f); _, secs, reused = f.result()
                done_count[0] += 1
                if not reused: say(f'[{done_count[0]}/{len(above)}] {m} {secs:.0f}s')
                for u in users[m]:
                    waiting[u].discard(m)
                    if not waiting[u]: heapq.heappush(ready, (-source(u)[1].stat().st_size, u))

say('lake build: hand-written base modules and checker C code')
subprocess.run(['lake', 'build', *['+' + m for m in lake_mods], *['+' + m + ':c' for m in FAST]], cwd=R, check=True)
(B / 'c').mkdir(parents=True, exist_ok=True); objs = []
for m in FAST:
    c, o = R / '.lake/build/ir' / (m.replace('.', '/') + '.c'), B / 'c' / (m + '.o')
    subprocess.run([PREFIX / 'bin/leanc', '-c', c, '-o', o, '-O3', '-DNDEBUG', '-DLEAN_EXPORTING', '-fPIC'], check=True)
    objs.append(o)
subprocess.run([PREFIX / 'bin/leanc', '-shared', '-o', LIB, *objs, '-L', PREFIX / 'lib/lean', '-L', PREFIX / 'lib', '-lgmp'], check=True)
say('linked native checker library', LIB.name)
build(above, True)

say('checking the final theorem')
check = B / 'Check.lean'
check.write_text(f'import {TARGET}\n#check @Sq19.square19_optimality\n#print axioms Sq19.square19_optimality\n')
out = subprocess.run([LEAN, str(check)], cwd=R, env=ENV, text=True, capture_output=True)
text = out.stdout + out.stderr
if out.returncode or re.search(r'\berror:', text): sys.exit('final check failed:\n' + text[:4000])
statement = text.split("'Sq19.square19_optimality' depends")[0].strip()
axioms = sorted(x.strip() for x in re.search(r"depends on axioms: \[([^\]]*)\]", text, re.S)[1].split(','))
want_stmt = (R / 'expected/statement.txt').read_text().strip()
want_ax = (R / 'expected/axioms.txt').read_text().split()
if ' '.join(statement.split()) != ' '.join(want_stmt.split()): sys.exit('statement differs:\n' + statement)
if axioms != sorted(want_ax): sys.exit(f'axioms differ: {sorted(set(axioms) ^ set(want_ax))[:10]}')
native = sum('native_decide' in x for x in axioms)
print(statement)
print(f'axioms: {", ".join(x for x in axioms if "native_decide" not in x)} + {native} native_decide checks')

if a.kernel_replay:
    say('kernel replay of the full import closure')
    lst = B / 'closure.txt'
    mods = run([LEAN, '--run', str(R / 'scripts/Closure.lean'), TARGET], env=ENV).split()
    def olean_size(m):  # largest first, so the biggest modules do not finish last
        top = m.split('.')[0]
        for d in base:
            if (d / top).is_dir() or (d / (top + '.olean')).exists():
                f = d / (m.replace('.', '/') + '.olean')
                return f.stat().st_size if f.exists() else 0
        return 0
    lst.write_text('\n'.join(sorted(mods, key=olean_size, reverse=True)) + '\n')
    rep = subprocess.run([LEAN, str(R / 'scripts/KernelReplay.lean')], cwd=R, text=True, capture_output=True,
                         env={**ENV, 'LEAN_NUM_THREADS': str(a.jobs), 'KCHECK_LIST': str(lst)})
    (B / 'kernel-replay.log').write_text(rep.stdout + rep.stderr)
    m = re.search(r'DONE modules=(\d+) fail=(\d+)', rep.stdout)
    if rep.returncode or not m or m[2] != '0': sys.exit('kernel replay failed; see build/verify/kernel-replay.log')
    print(f'kernel replay: {m[1]} modules, 0 failures')
print('VERIFIED')
