#!/usr/bin/env python3
"""Refresh regularizer inputs from the packing store (prototype; REGULARIZE.md, round 5).

For each n: the best known packing (`pk.py get best:N`, register + pending + ours) -> exactsolve; if that does
not certify, slp2 polish -> exactsolve.  Outputs in runs/regularize/exact/n-N/ ({input,polished}.exact.txt, .json);
reg.load() prefers these over search/exact/batch/work/ when they exist.  The published exact batch is not touched.

  refresh.py N... [--procs 12]
  refresh.py --stale [--procs 12]     every n whose batch input is worse than the store's best, or not a KKT point
"""
import argparse, json, os, re, subprocess, sys, time
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '1')
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
PK = os.path.join(ROOT, 'search', 'packer')
EX = os.path.join(ROOT, 'search', 'exact')
OUT = os.path.join(ROOT, 'runs', 'regularize', 'exact')
PY = sys.executable


def sh(args, timeout, log, cwd=None):
    t = time.time()
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout, cwd=cwd)
        out = r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        out = f'TIMEOUT after {timeout}s'
    with open(log, 'a') as f:
        f.write(f'$ {" ".join(args)}  ({time.time() - t:.0f}s)\n{out}\n')
    return out


def job(n):
    d = os.path.join(OUT, f'n-{n}')
    os.makedirs(d, exist_ok=True)
    log = os.path.join(d, 'log.txt')
    inp = os.path.join(d, 'input.txt')
    sh([PY, os.path.join(PK, 'pk.py'), 'get', f'best:{n}', '--fmt', 'ours', '-o', inp], 300, log, cwd=PK)
    if not os.path.exists(inp):
        return n, 'export failed'
    tmo = 1800 if n < 200 else 3600

    def exact(path):
        sh([PY, os.path.join(EX, 'exactsolve.py'), path, '--out', d, '-q'], tmo, log)
        p = os.path.join(d, os.path.basename(path)[:-4] + '.json')
        return json.load(open(p)) if os.path.exists(p) else None

    r = exact(inp)
    if r and r.get('cert_valid') and r.get('newton_converged'):
        return n, ('input', r.get('S_exact'))
    pol = os.path.join(d, 'polished.txt')
    # slp2 reads a decimal side only (the store writes an exact fraction when it has one)
    L = open(inp).read().split('\n')
    nn, side = L[0].split()[:2]
    if '/' in side:
        a, b = side.split('/')
        from decimal import Decimal, getcontext
        getcontext().prec = 40
        side = str(Decimal(a) / Decimal(b))
    inp_f = os.path.join(d, 'input_dec.txt')
    open(inp_f, 'w').write('\n'.join([f'{nn} {side}'] + L[1:]))
    sh([PY, os.path.join(PK, 'slp2.py'), inp_f, pol, '--R', '1e-4'], tmo, log)
    if not os.path.exists(pol):
        return n, 'polish failed'
    r2 = exact(pol)
    if r2 and r2.get('cert_valid'):
        return n, ('polished', r2.get('S_exact'))
    return n, 'not certified'


def stale():
    out = subprocess.run([PY, os.path.join(PK, 'pk.py'), 'frontier', '--lo', '1', '--hi', '324'], capture_output=True,
                         text=True, cwd=PK).stdout
    res = {r['n']: r for r in json.load(open(os.path.join(EX, 'batch', 'results.json')))}
    ns = []
    for line in out.split('\n'):
        m = re.match(r'\s*(\d+)\s+([\d.]+)', line)
        if m:
            n, best = int(m.group(1)), float(m.group(2))
            if best < float(res[n]['S_exact']) - 1e-9 or res[n]['status'] != 'KKT local min':
                ns.append(n)
    return ns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('n', type=int, nargs='*')
    ap.add_argument('--stale', action='store_true')
    ap.add_argument('--procs', type=int, default=12)
    a = ap.parse_args()
    ns = stale() if a.stale else a.n
    print('refreshing', len(ns), ns, flush=True)
    with Pool(a.procs) as pool:
        for n, st in pool.imap_unordered(job, sorted(ns, reverse=True)):
            print(n, st, flush=True)


if __name__ == '__main__':
    main()
