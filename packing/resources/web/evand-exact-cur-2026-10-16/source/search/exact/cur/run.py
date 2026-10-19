#!/usr/bin/env python3
"""Exact forms for current records (2026-10-15; TODO "Exact forms for current records without one").

Per n (or n:REF for a specific store packing): pk.py get -> exactsolve (-> slp2 polish -> exactsolve, as in
search/regularize/refresh.py) -> minpoly.py -> verify_exact.py (the last two via ../env.sh: msolve, flint).
Outputs runs/exact-cur/<tag>/; status line per job in runs/exact-cur/status.jsonl.  Nothing published is touched.

  run.py N[:REF] ... [--procs 12] [--tmo 900] [--mem 12G]
"""
import argparse, json, os, subprocess, sys, time
from decimal import Decimal, getcontext
from multiprocessing import Pool
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '1')
EX = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.abspath(os.path.join(EX, '..', '..'))
PK = os.path.join(ROOT, 'search', 'packer')
OUT = os.path.join(ROOT, 'runs', 'exact-cur')
PY = sys.executable
A = None


def sh(args, timeout, log, cwd=None):
    t = time.time()
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout, cwd=cwd)
        out, rc = r.stdout + r.stderr, r.returncode
    except subprocess.TimeoutExpired:
        out, rc = f'TIMEOUT after {timeout}s', 'timeout'
    with open(log, 'a') as f:
        f.write(f'$ {" ".join(args)}  ({time.time() - t:.0f}s, rc {rc})\n{out[-4000:]}\n')
    return rc, out


def job(spec):
    n, _, ref = spec.partition(':')
    ref = ref or f'best:{n}'
    tag = f'n-{n}' if ref == f'best:{n}' else f'n-{n}-' + ref.replace(':', '_').replace('/', '_')
    d = os.path.join(OUT, tag); os.makedirs(d, exist_ok=True)
    log = os.path.join(d, 'log.txt'); open(log, 'w').close()
    t0 = time.time()

    def done(stage, **kw):
        r = dict(n=int(n), ref=ref, tag=tag, stage=stage, secs=round(time.time() - t0), **kw)
        json.dump(r, open(os.path.join(d, 'status.json'), 'w'))
        return r

    inp = os.path.join(d, 'in.txt')
    sh([PY, os.path.join(PK, 'pk.py'), 'get', ref, '--fmt', 'ours', '-o', inp], 300, log, cwd=PK)
    if not os.path.exists(inp):
        return done('get failed')
    tmo = 1800 if int(n) < 200 else 3600

    def exact(path):
        sh([PY, os.path.join(EX, 'exactsolve.py'), path, '--out', d, '-q'], tmo, log)
        p = path[:-4] + '.json'
        return json.load(open(p)) if os.path.exists(p) else None

    base = os.path.join(d, 'in')
    r = exact(inp)
    if not (r and r.get('cert_valid') and r.get('newton_converged')):
        L = open(inp).read().split('\n'); nn, side = L[0].split()[:2]
        if '/' in side:
            getcontext().prec = 40; a, b = side.split('/'); side = str(Decimal(a) / Decimal(b))
        open(os.path.join(d, 'in_dec.txt'), 'w').write('\n'.join([f'{nn} {side}'] + L[1:]))
        pol = os.path.join(d, 'pol.txt')
        sh([PY, os.path.join(PK, 'slp2.py'), os.path.join(d, 'in_dec.txt'), pol, '--R', '1e-4'], tmo, log)
        if not os.path.exists(pol):
            return done('polish failed')
        r = exact(pol); base = os.path.join(d, 'pol')
        if not (r and r.get('cert_valid')):
            return done('not certified')
    S = r.get('S_exact')
    rc, out = sh(['systemd-run', '--user', '--scope', '-q', '-p', f'MemoryMax={A.mem}', '-p', 'MemorySwapMax=0',
                  os.path.join(EX, 'env.sh'), 'timeout', str(A.tmo), 'python3', 'minpoly.py', base], A.tmo + 600, log, cwd=EX)
    open(os.path.join(d, 'minpoly.log'), 'w').write(out)
    if not os.path.exists(base + '.minpoly.json'):
        last = [l for l in out.strip().split('\n') if l][-1:] or ['']
        return done('minpoly failed', S=S, why=last[0][-300:], rc=rc)
    rc, out = sh([os.path.join(EX, 'env.sh'), 'timeout', '3600', 'python3', 'verify_exact.py', base + '.minpoly.json'],
                 4000, log, cwd=EX)
    open(os.path.join(d, 'verify.txt'), 'w').write(out)
    m = json.load(open(base + '.minpoly.json'))
    return done('VALID' if 'VALID' in out and 'INVALID' not in out else 'verify failed', S=S,
                S_deg=len(m['S']['poly']) - 1, field_deg=len(m['field']['f']) - 1)


def main():
    global A
    ap = argparse.ArgumentParser()
    ap.add_argument('specs', nargs='+'); ap.add_argument('--procs', type=int, default=12)
    ap.add_argument('--tmo', type=int, default=900); ap.add_argument('--mem', default='12G')
    A = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    with Pool(A.procs) as pool, open(os.path.join(OUT, 'status.jsonl'), 'a') as st:
        for r in pool.imap_unordered(job, sorted(A.specs, key=lambda s: -int(s.split(':')[0]))):
            print(json.dumps(r), flush=True); st.write(json.dumps(r) + '\n'); st.flush()


if __name__ == '__main__':
    main()
