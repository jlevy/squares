#!/usr/bin/env python3
"""Coverage check: every box zmx2 left uncertified in the tight-tile roots must lie inside a region certified by
ttbox (exact rational comparisons).  Certified region for depth d0, tilt sign sg, left-wall frame:
    |cx - d0| <= DMAX,  cy in RANGES[d0],  0 <= u <= U0  (u = tan(theta/2); u = 0 is the theta = 0 case, done by zmx2
    cert0 / Lemma Z),  both signs certified.
zmx2 boxes (x, y, u) with u >= 0 near x = d0 are left-wall tiles with sign +1; near y = d0 they are bottom-wall tiles,
which the transpose (x <-> y, orientation reversed) maps to left-wall tiles with sign -1 and s = x.
usage: cov_check.py cov/   (files r<id>.out from run_cov.sh)"""
import sys, os, re, glob
from fractions import Fraction as F
U0 = F(1, 4000); DMAX = 4*U0
R = {F(3, 2): [(14, 17), (24, 27), (33, 55)], F(5, 2): [(14, 17), (23, 27), (33, 37), (38, 55)],
     F(7, 2): [(14, 17), (23, 27), (33, 37), (41, 45)]}
RANGES = {d: [(F(a, 10), F(b, 10)) for a, b in rs] for d, rs in R.items()}
# extra regions certified with u0 = 1/2000, dmax = 1/500 (run_u2000.sh): (d0, frame, s_lo, s_hi); frame 'left' = sign +1
# jobs, 'bottom' = sign -1 jobs (transpose).  Used only if every listed job in out_u2000/ is ALL-OK.  Each range includes
# its end lines s = a, b, whose line charts cover |s - s_b| <= t0 = DMAXb, so the range extends by DMAXb at both ends.
EXTRA = [(F(3, 2), 'left', F(42, 10), F(43, 10)), (F(3, 2), 'left', F(45, 10), F(46, 10)), (F(3, 2), 'bottom', F(54, 10), F(55, 10)),
         (F(3, 2), 'bottom', F(38, 10), F(39, 10)), (F(5, 2), 'bottom', F(44, 10), F(45, 10))]
U0b = F(1, 2000); DMAXb = 4*U0b
# ---- jobs-complete check (strict) ----
# Every job must have a finished run_tt.py output in which EVERY expected chart (the chart names that charts_line /
# charts_strip produce for that job) reports 0 refused cells, with h0 equal to the job's u0 and a matching tile string.
# A rerun in <dir>_fix/<same name> (e.g. with the wedge-corner / ray-zoom zones, possibly SKIP=... so PARTIAL-...)
# overrides exactly the charts it reports.  Main jobs: make_jobs.py, u0 = 1/4000, outputs in out/ (a stray name suffix
# from an old launcher is tolerated: such line runs carried one extra ignored argument).  u0 = 1/2000 jobs: the list in
# run_u2000.sh, outputs in out_u2000/.  An appended hand supplement is NOT accepted.
import glob as _g, os as _o, json as _json, subprocess as _sp
_here = _o.path.dirname(_o.path.abspath(__file__))
sys.path.insert(0, _here)
import ttbox as _T
def _expected(d0, sign, kind, args, u0, K=F(4)):
    t0 = K*u0
    sendf = lambda x: F(x[:-1]) + t0 if x.endswith('+') else F(x[:-1]) - t0 if x.endswith('-') else F(x)
    ch = _T.charts_line(F(d0), F(args[0]), int(sign), K, u0) if kind == 'line' else _T.charts_strip(F(d0), sendf(args[0]), sendf(args[1]), int(sign), K, u0)
    return [c[0] for c in ch]
def _read(fn, final_ok):
    """(last line, {chart: (fails, h0, tile)}) of a finished run_tt.py output, or None"""
    t = [l for l in open(fn).read().split('\n') if l.strip()]
    if not t or not any(t[-1].startswith(x) for x in final_ok): return None
    r = {}
    for line in t:
        if line.startswith('{'):
            d = _json.loads(line)
            if 'fails' in d: r[d['chart']] = (d['fails'], d.get('h0'), d.get('tile', ''), d.get('K', '4'))
    return t[-1], r
def check_jobs(jobs, outdir, u0):
    bad = []
    for j in jobs:
        d0, sign, kind, args = j[0], j[1], j[2], j[3:]
        n = 'd%s_s%s_%s_%s' % (d0, sign, kind, '_'.join(args))
        main = [_o.path.join(_here, outdir, n + '.out')] + sorted(_g.glob(_o.path.join(_here, outdir, _g.escape(n) + '_*.out')))
        main = [c for c in main if _o.path.exists(c)]
        if len(main) != 1: bad.append((n, f'{len(main)} output files')); continue
        rr = _read(main[0], ('ALL-OK', 'NOT-OK'))
        if rr is None: bad.append((n, 'unfinished')); continue
        txt = open(main[0]).read()
        r = rr[1]; rf = None
        fx = _o.path.join(_here, outdir + '_fix' if outdir != 'out' else 'out_fix', n + '.out')
        if _o.path.exists(fx):
            rf = _read(fx, ('ALL-OK', 'NOT-OK', 'PARTIAL-ALL-OK', 'PARTIAL-NOT-OK'))
            if rf is None: bad.append((n, 'fix run unfinished')); continue
            r.update(rf[1])
        # an appended hand supplement (corner_supp.py) is never accepted: the chart it patched (C_u) must be re-run
        if ('SUPPLEMENT' in txt or 'supplement' in txt) and not (rf and 'C_u' in rf[1]):
            bad.append((n, 'C_u closed only by an appended hand supplement: re-run C_u into ' + _o.path.basename(_o.path.dirname(fx)) + '/')); continue
        exp = _expected(d0, sign, kind, args, u0)
        tile = f'd0={F(d0)} sign={sign} {kind} {" ".join(args)}'
        miss = [c for c in exp if c not in r]
        extra = [c for c in r if c not in exp]
        wrong = [c for c in exp if c in r and (r[c][0] != 0 or r[c][1] != str(u0) or r[c][3] != '4'
                                              or not (r[c][2] == tile or (kind == 'line' and r[c][2].startswith(tile + ' '))))]
        if miss or extra or wrong: bad.append((n, f'missing {miss} extra {extra} failed/mismatched {wrong}'))
    return bad
_jobs = [j.split() for j in _sp.run([sys.executable, _o.path.join(_here, 'make_jobs.py')], capture_output=True, text=True).stdout.split('\n') if j.strip()]
_ub = open(_o.path.join(_here, 'run_u2000.sh')).read()
_ujobs = [l.split() for l in _ub.split('\n') if re.match(r'^\d+(\.\d+)? -?1 (line|strip) ', l)]
jobs_bad = check_jobs(_jobs, 'out', U0)
ujobs_bad = check_jobs(_ujobs, 'out_u2000', U0b)
JOBS_OK = len(_jobs) == 308 and not jobs_bad
EXTRA_OK = len(_ujobs) == 15 and not ujobs_bad
print(f'tight-tile jobs (u0 = 1/4000): {len(_jobs)}; not certified: {len(jobs_bad)}', *[f'\n  {n}: {st}' for n, st in jobs_bad[:20]])
print(f'u0 = 1/2000 jobs: {len(_ujobs)}; not certified: {len(ujobs_bad)}', *[f'\n  {n}: {st}' for n, st in ujobs_bad[:20]])
# each extra region needs exactly its own jobs: lines a and b and the strip between them, d0 and sign (left = +1)
_ubad = {n for n, _ in ujobs_bad}
def _region_ok(d0, fr, a, b):
    sg = '1' if fr == 'left' else '-1'; d = str(float(d0))
    need = [f'd{d}_s{sg}_line_{float(a):.1f}', f'd{d}_s{sg}_strip_{float(a):.1f}+_{float(b):.1f}-', f'd{d}_s{sg}_line_{float(b):.1f}']
    have = {'d%s_s%s_%s_%s' % (j[0], j[1], j[2], '_'.join(j[3:])) for j in _ujobs}
    return all(x in have and x not in _ubad for x in need)
EXTRA = [e for e in EXTRA if len(_ujobs) == 15 and _region_ok(*e)]
print(f'extra u0 = 1/2000 regions used: {len(EXTRA)} of 5')
def inside(lo, hi, ranges): return any(a <= lo and hi <= b for a, b in ranges)
pat = re.compile(r'^UNCERT (\d+) pass \d+ box (\S+) ')
tot = bad = 0; files = 0; done = 0; badlist = []
for f in sorted(glob.glob(os.path.join(sys.argv[1], 'r*.out'))):
    files += 1; txt = open(f).read()
    if '\ndone in' in txt or txt.startswith('done in'): done += 1
    for line in txt.split('\n'):
        m = pat.match(line)
        if not m: continue
        x0, x1, y0, y1, u0, u1 = (F(t) for t in m.group(2).split(','))
        tot += 1; ok = False
        if u1 <= U0:
            for d0, rg in RANGES.items():
                if d0 - DMAX <= x0 and x1 <= d0 + DMAX and inside(y0, y1, rg): ok = True; break
                if d0 - DMAX <= y0 and y1 <= d0 + DMAX and inside(x0, x1, rg): ok = True; break
        if not ok and u1 <= U0b:
            for d0, fr, a, b in EXTRA:
                if fr == 'left' and d0 - DMAXb <= x0 and x1 <= d0 + DMAXb and a - DMAXb <= y0 and y1 <= b + DMAXb: ok = True; break
                if fr == 'bottom' and d0 - DMAXb <= y0 and y1 <= d0 + DMAXb and a - DMAXb <= x0 and x1 <= b + DMAXb: ok = True; break
        if not ok:
            bad += 1
            if len(badlist) < 20: badlist.append((m.group(1), [float(v) for v in (x0, x1, y0, y1, u0, u1)]))
print(f'files {files} (finished {done}); uncertified boxes {tot}; inside certified tight-tile regions {tot-bad}; OUTSIDE {bad}')
for b in badlist: print('  outside:', b)
print('COVERAGE-OK' if bad == 0 and done == files and files == 75 and JOBS_OK else 'COVERAGE-NOT-OK')
