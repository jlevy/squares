#!/usr/bin/env python3
"""s(183) hunt (10-18 evening; Evan: "182 has too much slack, 183 should pack sub-grid").  s(183) = 14 (grid) in the
register; s(182) = 13.97409 (Couzo), the largest end-of-column margin k - s(k^2 - c) for k = 8..18.

  seeds:   one square inserted into distinct sub-14 182 packings from the store (chain.seed_job k = -1: dilate 0.2-1.2 %,
           one of the 12 best pose holes, fq quench), two into 181 packings (k = -2).  Arms: 'record' (the 182 record
           only, many seeds), 'diverse182' (stratified distinct 182s), 'diverse181'.
  explore: explorer runs per arm from the seeds below --smax-seed (not grid), equal minutes per run.
  report:  seed side distribution per arm; explorer best per run; every sub-14 183 found.

  h183.py seeds   [--donors 120 --per 4 --tries 4 --procs 15]
  h183.py explore [--runs-per-arm 4 --procs-per 2 --minutes 40]
  h183.py report
"""
import argparse, collections, glob, json, os, random, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = f'{HERE}/runs/h183'
K = 14.0


def _seed(j):
    import chain
    chain.TRIES = j[-1]
    return chain.seed_job(j[:-1])


def pick(st, n, m, smax, rng):
    """the best m // 2 distinct sides + m // 2 stratified by (side band, tilted count) over the rest below smax"""
    rows = st.db.execute('SELECT id, s, ntilted FROM packing WHERE n=? AND s < ? ORDER BY s', (n, smax)).fetchall()
    seen, D = set(), []
    for pid, s, t in rows:
        k = round(s, 7)
        if k in seen:
            continue
        seen.add(k); D.append((pid, s, t or 0))
    out = D[:m // 2]
    rest = D[m // 2:]
    strata = collections.defaultdict(list)
    if rest:
        lo, hi = rest[0][1], smax
        for d in rest:
            strata[(min(4, int(5 * (d[1] - lo) / (hi - lo + 1e-12))), d[2] // 6)].append(d)
    keys = sorted(strata)
    while len(out) < m and any(strata.values()):
        for k in keys:
            if strata[k] and len(out) < m:
                out.append(strata[k].pop(rng.randrange(len(strata[k]))))
    return out


def seeds(a):
    from pk.store import Store
    from pk import manifest
    from jobpool import run_jobs
    import scratch
    scratch.scope('h183')
    os.makedirs(ROOT, exist_ok=True)
    man = manifest.start(ROOT, 'h183-seeds', seed=a.seed, args=vars(a), procs=a.procs, fname='manifest_seeds.json')
    st = Store(); rng = random.Random(a.seed)
    for d in ('donors', 'seeds'):
        os.makedirs(f'{ROOT}/{d}', exist_ok=True)
    rec = st.db.execute('SELECT id FROM packing WHERE n=182 ORDER BY s LIMIT 1').fetchone()[0]
    d182 = [x for x in pick(st, 182, a.donors + 1, a.smax182, rng) if x[0] != rec][:a.donors]
    d181 = pick(st, 181, a.donors181, a.smax181, rng)
    J, meta = [], []
    st.get(rec).write(f'{ROOT}/donors/d{rec}.txt')
    for q in range(a.per_record):
        J.append((f'{ROOT}/donors/d{rec}.txt', -1, 183, f'{ROOT}/seeds/r{rec}_{q}.txt', rng.randrange(10 ** 9), a.tries))
        meta.append(dict(arm='record', src=rec, q=q))
    for arm, D, k in (('diverse182', d182, -1), ('diverse181', d181, -2)):
        for pid, s, t in D:
            st.get(pid).write(f'{ROOT}/donors/d{pid}.txt')
            for q in range(a.per):
                J.append((f'{ROOT}/donors/d{pid}.txt', k, 183, f'{ROOT}/seeds/{arm[-3:]}_{pid}_{q}.txt', rng.randrange(10 ** 9), a.tries))
                meta.append(dict(arm=arm, src=pid, src_s=s, src_tilt=t, q=q))
    t0 = time.time()
    R = run_jobs(_seed, J, procs=a.procs, timeout=1800)
    with open(f'{ROOT}/seeds.jsonl', 'w') as fo:
        for j, m, r in zip(J, meta, R):
            m.update(path=j[3], s=r if isinstance(r, float) else None)
            fo.write(json.dumps(m) + '\n')
    summary(meta)
    print(f'seeds done [{time.time() - t0:.0f}s]')
    man.finish()


def summary(meta):
    for arm in ('record', 'diverse182', 'diverse181'):
        S = [m['s'] for m in meta if m['arm'] == arm]
        ok = sorted(s for s in S if s is not None)
        if not ok:
            print(f'{arm}: none feasible'); continue
        print(f'{arm}: {len(S)} seeds, {len(ok)} feasible; <14: {sum(s < K - 1e-9 for s in ok)}, grid: '
              f'{sum(abs(s - K) < 1e-9 for s in ok)}, 14-14.01: {sum(K + 1e-9 < s < K + .01 for s in ok)}, '
              f'14.01-14.02: {sum(K + .01 <= s < K + .02 for s in ok)}, 14.02-14.05: {sum(K + .02 <= s < K + .05 for s in ok)}, '
              f'above: {sum(s >= K + .05 for s in ok)}; best {ok[:3]}', flush=True)


def explore(a):
    from pk import manifest
    from layout import full_lines
    M = [json.loads(l) for l in open(f'{ROOT}/seeds.jsonl')]
    M = [m for m in M if m['s'] is not None and full_lines(m['path'], int(K)) == 0]   # grid-blocked seeds can't go below 14
    man = manifest.start(ROOT, 'h183-explore', args=vars(a), procs=a.runs_per_arm * 3 * a.procs_per, fname='manifest_explore.json')
    P = []
    i = 0
    for arm in ('record', 'diverse182', 'diverse181'):
        use = sorted((m for m in M if m['arm'] == arm and m['s'] is not None and m['s'] < a.smax_seed and abs(m['s'] - K) > 1e-9),
                     key=lambda m: m['s'])
        # distinct sides, best first, at most --starts-per-run per run, round-robin so every run gets good and worse starts
        seen, U = set(), []
        for m in use:
            if round(m['s'], 8) not in seen:
                seen.add(round(m['s'], 8)); U.append(m)
        U = U[:a.runs_per_arm * a.starts_per_run]
        if not U:
            print(f'{arm}: no seeds below {a.smax_seed}'); continue
        for r in range(a.runs_per_arm):
            R = U[r::a.runs_per_arm]
            if not R:
                continue
            out = f'{ROOT}/x{i}_{arm}'; i += 1
            os.makedirs(out, exist_ok=True)
            json.dump(R, open(f'{out}/starts.json', 'w'))
            cmd = [sys.executable, f'{HERE}/explore.py', '--n', '183', '--starts', *[m['path'] for m in R], '--minutes',
                   str(a.minutes), '--procs', str(a.procs_per), '--seed', str(700 + i), '--adapt', '--smax', str(K + 0.06),
                   '--frontier-s', str(K), '--final-polish', '8', '--out', out]
            P.append(subprocess.Popen(cmd, stdout=open(f'{out}/log.txt', 'w'), stderr=subprocess.STDOUT))
    for p in P:
        p.wait()
    man.finish()
    report(a)


def report(a):
    M = [json.loads(l) for l in open(f'{ROOT}/seeds.jsonl')]
    summary(M)
    allbest = []
    for d in sorted(glob.glob(f'{ROOT}/x*')):
        best = None
        for f in glob.glob(f'{d}/**/*.txt', recursive=True):
            try:
                h = open(f).readline().split()
                if len(h) == 2 and h[0] == '183':
                    s = float(h[1])
                    if best is None or s < best[0]:
                        best = (s, f)
            except Exception:
                pass
        print(f'{os.path.basename(d)}: best {best}')
        if best:
            allbest.append(best)
    sub = sorted(b for b in allbest if b[0] < K - 1e-9)
    print(f'sub-14 run bests: {len(sub)}', sub[:5])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    p = sp.add_parser('seeds')
    p.add_argument('--donors', type=int, default=120); p.add_argument('--donors181', type=int, default=30)
    p.add_argument('--per', type=int, default=4); p.add_argument('--per-record', type=int, default=120)
    p.add_argument('--tries', type=int, default=4); p.add_argument('--procs', type=int, default=15)
    p.add_argument('--smax182', type=float, default=13.995); p.add_argument('--smax181', type=float, default=13.97)
    p.add_argument('--seed', type=int, default=183)
    p = sp.add_parser('explore')
    p.add_argument('--runs-per-arm', type=int, default=4); p.add_argument('--procs-per', type=int, default=1)
    p.add_argument('--starts-per-run', type=int, default=6); p.add_argument('--minutes', type=float, default=40)
    p.add_argument('--smax-seed', type=float, default=14.04)
    p = sp.add_parser('report')
    a = ap.parse_args()
    {'seeds': seeds, 'explore': explore, 'report': report}[a.cmd](a)
