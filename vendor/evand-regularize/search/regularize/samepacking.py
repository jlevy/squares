#!/usr/bin/env python3
"""Is the regularized packing the same packing as the source?  (Evan 10-10; REGULARIZE.md.)

Per record with angle changes:
  path   rotate the changed squares from their source angles to their final angles together (linear in angle, steps
         <= STEP_DEG), re-solving translations at S* at every step (LP, trust region from the previous step).  All
         steps feasible = connected at S*: no size increase on the way (sufficient, not necessary: only translations
         and this one angle path are tried).
  kkt    exactsolve on the regularized output: is it itself a KKT local minimum at S* (or can S go down from it)?
         Criterion as search/exact/batch/summarize.py.
Usage:  samepacking.py [N ...] [--procs 8] [--min-deg 1e-3] [--no-kkt]
Writes runs/regularize/samepacking.jsonl.
"""
import argparse, glob, json, math, os, subprocess, sys, tempfile, time
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '1')
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
POSTER = os.path.join(ROOT, 'runs', 'regularize', 'poster')
STEP_DEG = 0.01


def path_test(n, near_gap=None):
    import reg
    from mpmath import mpf
    if near_gap is not None:          # NEAR_GAP keeps nearly-equal distinct angles apart; on a path that converges to
        reg.NEAR_GAP = near_gap       # equal angles it blocks the last steps artificially
    P0 = reg.load(n)
    P1, _ = reg.merge_angles(P0, P0['free'], lambda *a: None)
    P2, ch = reg.merge_determined(P1, log=lambda *a: None)
    T0, T2 = P0['T'], P2['T']
    d = [float(reg.fold(T2[i] - T0[i])) for i in range(n)]
    changed = [i for i in range(n) if abs(d[i]) > 1e-12]
    if not changed:
        return dict(changed=0)
    big = max(abs(d[i]) for i in changed)
    steps = max(2, int(math.ceil(big / STEP_DEG)))
    Q = dict(P0)
    blocked = None
    for k in range(1, steps + 1):
        s = k / steps
        T = list(T0)
        for i in changed:
            T[i] = reg.fold(T0[i] + mpf(d[i]) * s)
        Q = dict(Q); Q['T'] = T
        X, Y, st, _ = reg.place(Q, None, feas_only=True, trust=0.25)
        if st != 'ok':
            # a few full iterations before calling it blocked
            X, Y, st, _ = reg.place(Q, [(0.0, 0.0)] * n, trust=0.25, iters=8)
        if st == 'infeasible':
            blocked = s
            break
        Q['X'] = [mpf(float(v)) for v in X]; Q['Y'] = [mpf(float(v)) for v in Y]
    return dict(changed=len(changed), max_deg=big, steps=steps, connected=blocked is None, blocked_at=blocked,
                free=sum(1 for i in changed if i in P0['free']))


def kkt_test(n):
    d = json.load(open(os.path.join(POSTER, f'n-{n:03d}.json')))
    pk = d['packing']
    tmp = tempfile.mkdtemp(prefix=f'reg{n}-', dir=os.path.join(ROOT, 'runs', 'regularize'))
    inp = os.path.join(tmp, 'reg.txt')
    with open(inp, 'w') as f:
        f.write(f"{n} {pk['S']}\n" + ''.join(f'{x} {y} {t}\n' for x, y, t in pk['sq']))
    t = time.time()
    try:
        subprocess.run([sys.executable, os.path.join(ROOT, 'search', 'exact', 'exactsolve.py'), inp, '--out', tmp, '-q'],
                       capture_output=True, text=True, timeout=3600 if n > 200 else 1800)
    except subprocess.TimeoutExpired:
        return dict(kkt='timeout')
    p = os.path.join(tmp, 'reg.json')
    if not os.path.exists(p):
        return dict(kkt='no output')
    r = json.load(open(p))
    so = (r.get('second_order') or {}).get('status', '') or ''
    lam = r.get('lambda_A_maxmin')
    kkt = (lam is not None and lam > 0 and (r.get('equilibrium_residual_exact') or 0) < 1e-30
           and so.startswith(('local minimum', 'PD', 'rigid')) and (r.get('vv_milp_dS') or 0) > -1e-9)
    from mpmath import mpf, mp
    mp.dps = 80
    dS = float(mpf(r['S_exact']) - mpf(d['S_exact'])) if r.get('S_exact') else None
    return dict(kkt=bool(kkt), S_reg_exact_minus_Sstar=dS, second=so[:60], lam=lam, vv=r.get('vv_milp_dS'),
                free=len(r.get('free_squares') or []), cert=r.get('cert_valid'), dir=os.path.relpath(tmp, ROOT),
                seconds=round(time.time() - t))


def one(args):
    n, do_kkt = args
    out = dict(n=n)
    try:
        out['path'] = path_test(n, near_gap=float(os.environ.get('SP_NEAR_GAP', '1e-8')))
    except Exception as e:
        out['path'] = dict(error=f'{type(e).__name__}: {e}')
    if do_kkt:
        try:
            out['kkt'] = kkt_test(n)
        except Exception as e:
            out['kkt'] = dict(error=f'{type(e).__name__}: {e}')
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('n', type=int, nargs='*')
    ap.add_argument('--procs', type=int, default=8)
    ap.add_argument('--min-deg', type=float, default=1e-3)
    ap.add_argument('--no-kkt', action='store_true')
    a = ap.parse_args()
    ns = a.n
    if not ns:
        for f in sorted(glob.glob(os.path.join(POSTER, 'n-*.json'))):
            d = json.load(open(f))
            if any(c[0] == 'free-angle' and abs(((c[2] - c[1]) + 45) % 90 - 45) > a.min_deg
                   for c in d.get('angle_changes') or []):
                ns.append(d['n'])
    print('records', len(ns), ns, flush=True)
    out = os.path.join(ROOT, 'runs', 'regularize', 'samepacking.jsonl')
    with Pool(a.procs) as pool, open(out, 'a') as f:
        for r in pool.imap_unordered(one, [(n, not a.no_kkt) for n in sorted(ns, reverse=True)]):
            f.write(json.dumps(r, default=str) + '\n'); f.flush()
            print(json.dumps(r, default=str), flush=True)


if __name__ == '__main__':
    main()
