#!/usr/bin/env python3
"""Certify all charts of one tight-tile neighbourhood (left wall, depth d0, tilt sign).
usage: run_tt.py COVER d0 sign line s_b  |  run_tt.py COVER d0 sign strip s1+ s2-
parameters (env): K=4 U0=1/4000 (so t0 = dmax = K*U0) MAXCELLS=400000 SKIP=chart,... PROGRESS=n"""
import sys, os, time, json
from fractions import Fraction as F
import ttbox as T, ttarea
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
cov, d0, sign, kind = sys.argv[1], F(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
K = F(os.environ.get('K', '4')); U0 = F(os.environ.get('U0', '1/4000')); MAXC = int(os.environ.get('MAXCELLS', '400000'))
T0 = K*U0      # line neighbourhoods |s - s_b| <= T0; strips cover the rest
def send(x):   # '4.8+' = 4.8 + T0, '4.9-' = 4.9 - T0
    return F(x[:-1]) + T0 if x.endswith('+') else F(x[:-1]) - T0 if x.endswith('-') else F(x)
segs = T.load(cov)
def cover_rect(path):
    L = open(path).read().split('\n'); i = 0
    while not L[i].split() or L[i].startswith('#') or L[i].startswith('mixed'): i += 1
    pitch = int(L[i+1]); wden = int(L[i+2]); n = int(L[i+4]); v = [int(t) for t in L[i+5+n+1].split()]
    xs = [F(a, pitch) for a in v[2::2]]; ys = [F(a, pitch) for a in v[3::2]]
    return (min(xs), min(ys), max(xs), max(ys), F(v[1], wden)/((max(xs)-min(xs))*(max(ys)-min(ys))))
U = cover_rect(cov)
def attach(ch):
    # the tile at depth d0 reaches the Lebesgue rectangle only if d0 + 1/2 + 1 > U's left edge (with room to spare)
    if d0 + 1 > U[0]: ch['area_term'] = ttarea.AreaTerm(ch, U)
    return ch
charts = T.charts_line(d0, F(sys.argv[5]), sign, K, U0) if kind == 'line' else T.charts_strip(d0, send(sys.argv[5]), send(sys.argv[6]), sign, K, U0)
allok = True
SKIP = os.environ.get('SKIP', '').split(',')
for name, ch, poly, h0 in charts:
    attach(ch)
    if name.split()[0] in SKIP: continue
    t = time.time()
    st, fails = T.run(segs, ch, [poly], h0, maxcells=MAXC, minarea=F(1, 2**60), progress=int(os.environ.get('PROGRESS', '0')) or None)
    if fails and name == 'C_u':
        # refused C_u cells at a double corner: every refused cell must lie within rho of a rational corner point
        # (kappa*, sigma*) of small denominator; that whole box x [0, h0] is then re-covered by the four-zone corner
        # charts (charts_corner3), which are certified independently.  Anything else stays a failure.
        M = F(4); groups = {}; left = []
        for f in fails:
            Q = f[0]; cand = None
            for v in Q:
                if all(F(x).limit_denominator(1000) == x and F(x).denominator <= 1000 for x in v):
                    cand = v; break
            if cand is None:
                # refused cell next to (not at) a corner: nearest point with denominators <= 1000, if within 2^-20
                c = (sum(v[0] for v in Q)/len(Q), sum(v[1] for v in Q)/len(Q))
                r_ = (c[0].limit_denominator(1000), c[1].limit_denominator(1000))
                if max(abs(c[0]-r_[0]), abs(c[1]-r_[1])) <= F(1, 2**20): cand = r_
            if cand is None or f[1] == 'maxcells': left.append(f); continue
            r_ = max(max(abs(v[0]-cand[0]), abs(v[1]-cand[1])) for v in Q)
            groups[cand] = max(groups.get(cand, F(0)), r_)
        cres = []
        for (ks, ss), r_ in groups.items():
            rho = F(1, 2**30)
            while rho < r_: rho *= 2
            if rho > M*h0: left.append(('corner too large', (ks, ss))); continue
            for cname, cch, cpoly, ch0 in T.charts_corner3(d0, F(sys.argv[5]), sign, ks, ss, rho, M, h0):
                attach(cch)
                cst, cf = T.run(segs, cch, [cpoly], ch0, maxcells=MAXC, minarea=F(1, 2**60))
                cres.append(dict(corner=[str(ks), str(ss)], rho=str(rho), chart=cname, cells=cst['cells'], fails=cst['fails']))
                if cf: left.append(('corner chart failed', (ks, ss), cname))
        print(json.dumps(dict(tile=f'd0={d0} sign={sign} {kind} {" ".join(sys.argv[5:])}', chart='C_u corners', corners=len(groups),
                              corner_cells=sum(c['cells'] for c in cres), corner_fails=sum(c['fails'] for c in cres), unresolved=len(left))), flush=True)
        for c in cres: print('  CORNER', json.dumps(c), flush=True)
        st['fails'] = len(left); fails = left
    if fails and ch.get('wedge') and ch['wedge'][0] == 1 and name.startswith('W'):
        # refused cells of a tilt-scaled wedge chart (face (p, q), h <= q/K) near a corner (p*, 0) of the face, p* rational
        # of small denominator: the box |p - p*| <= rho, 0 <= q <= rho (x [0, q/K]) is re-covered by the wedge-corner zones
        # (charts_wcorner); a refused WFAR b zone (q <= |p - p*|) is in turn re-covered by the ray-zoom zones around the
        # face line q = lam |p - p*| that its refused cells sit on.  Anything else stays a failure.
        groups = {}; left = []
        print('  .. refused', len(fails), [(float(sum(v[0] for v in f[0])/len(f[0])), float(sum(v[1] for v in f[0])/len(f[0]))) for f in fails], flush=True)
        for f in fails:
            Q = f[0]; c = (sum(v[0] for v in Q)/len(Q), sum(v[1] for v in Q)/len(Q)); ps = c[0].limit_denominator(1000)
            if f[1] == 'maxcells' or c[1] > F(1, 2**20) or abs(c[0] - ps) > F(1, 2**20): left.append(f); continue
            r_ = max(max(abs(v[0] - ps), v[1]) for v in Q)
            groups[ps] = max(groups.get(ps, F(0)), r_)
        cres = []
        for ps, r_ in groups.items():
            rho = F(1, 2**30)
            while rho < r_: rho *= 2
            for cname, cch, cpoly, ch0 in T.charts_wcorner(ch, ps, rho, K, h0):
                attach(cch)
                cst, cf = T.run(segs, cch, [cpoly], ch0, maxcells=MAXC, minarea=F(1, 2**60))
                cres.append(dict(corner=str(ps), rho=str(rho), chart=cname, cells=cst['cells'], fails=cst['fails']))
                print('  ..', json.dumps(cres[-1]), flush=True)
                if not cf: continue
                if not (cname.startswith('WFAR') and cname.endswith('b')): left.append(('wcorner chart failed', str(ps), cname)); continue
                # the ray: a rational lam of denominator <= 20 with q = lam X meeting the most refused cells (the range
                # of q/X over a convex cell with X > 0 is [min, max] over its vertices); the simplest such lam
                ivs = []
                for f in cf:
                    Q = f[0]
                    if min(v[0] for v in Q) > 0: ivs.append((min(v[1]/v[0] for v in Q), max(v[1]/v[0] for v in Q)))
                cands_ = sorted({F(a, b) for b in range(1, 21) for a in range(1, b)}, key=lambda l: (l.denominator, l))
                score = {l: sum(1 for a, b in ivs if a <= l <= b) for l in cands_}
                lam = max(cands_, key=lambda l: score[l]) if ivs else None
                print('  .. ray', str(lam), 'meets', score.get(lam, 0), 'of', len(cf), 'refused cells', flush=True)
                if lam is None or score[lam] == 0: left.append(('wcorner chart failed', str(ps), cname)); continue
                if not (0 < lam < 1): left.append(('ray outside zone', str(ps), cname, str(lam))); continue
                for rname, rch, rpoly in T.charts_rayzoom(cch, lam, rho):
                    attach(rch)
                    rst, rf = T.run(segs, rch, [rpoly], ch0, maxcells=MAXC, minarea=F(1, 2**60))
                    cres.append(dict(corner=str(ps), rho=str(rho), chart=f'{cname} / {rname} lam={lam}', cells=rst['cells'], fails=rst['fails']))
                    print('  ..', json.dumps(cres[-1]), flush=True)
                    if rf: left.append(('ray chart failed', str(ps), cname, rname))
        print(json.dumps(dict(tile=f'd0={d0} sign={sign} {kind} {" ".join(sys.argv[5:])}', chart=f'{name} corners', corners=len(groups),
                              corner_cells=sum(c['cells'] for c in cres), corner_fails=sum(c['fails'] for c in cres), unresolved=len(left))), flush=True)
        for c in cres: print('  WCORNER', json.dumps(c), flush=True)
        st['fails'] = len(left); fails = left
    allok &= st['fails'] == 0
    w = st['worst']
    print(json.dumps(dict(tile=f'd0={d0} sign={sign} {kind} {" ".join(sys.argv[5:])}', chart=name, h0=str(h0), K=str(K), ok=st['ok'], cells=st['cells'], fails=st['fails'],
                          worst=float(w[0]) if w else None, secs=round(time.time()-t))), flush=True)
    for f in fails[:5]:
        try: print('  FAIL', [(float(a), float(b)) for a, b in f[0]], f[1], {k: float(v) for k, v in f[2].items()} if len(f) > 2 and isinstance(f[2], dict) else '', flush=True)
        except Exception: print('  FAIL', f, flush=True)
# a run with SKIP certifies only some charts: it ends PARTIAL-..., never plain ALL-OK
_skip = [x for x in SKIP if x]
print(('PARTIAL-' if _skip else '') + ('ALL-OK' if allok else 'NOT-OK') + (f' (skipped {",".join(_skip)})' if _skip else ''), flush=True)
