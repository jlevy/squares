#!/usr/bin/env python3
"""Cross-checks for cur/data (2026-10-15), independent of minpoly.py's algebra:
(1) exactsolve's 80-digit Newton value of S (runs/exact-cur/<tag>/*.json, S_exact) lies in p's isolating interval;
(2) mpmath.findpoly on that value (degree <= 16, 60 digits) returns p itself or nothing (never a different polynomial);
(3) S* vs the record side printed by the store's frontier (pk.py frontier: S* <= printed, within 1e-9).
Writes cur/crosscheck.json; prints one line per n."""
import glob, gzip, json, os, re, subprocess, sys
from fractions import Fraction
import mpmath as mp
mp.mp.dps = 70
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
fr = subprocess.run([sys.executable, os.path.join(ROOT, 'search/packer/pk.py'), 'frontier'], capture_output=True, text=True).stdout
best = {int(m.group(1)): m.group(2) for m in (re.match(r'\s*(\d+)\s+([\d.]+)', l) for l in fr.split('\n')) if m}
out = []
for f in sorted(glob.glob(os.path.join(HERE, 'data', 'n-*.minpoly.json.gz')), key=lambda s: int(s.split('-')[-1].split('.')[0])):
    m = json.load(gzip.open(f)); n = int(m['n'])
    p = [int(c) for c in m['S']['poly']]                          # ascending
    lo, hi = (Fraction(x) for x in m['S']['interval'])
    st = json.load(open(os.path.join(ROOT, 'runs/exact-cur', f'n-{n}', 'status.json')))
    S = mp.mpf(st['S'])
    in_iv = mp.mpf(lo.numerator) / lo.denominator <= S <= mp.mpf(hi.numerator) / hi.denominator
    res = abs(mp.polyval(p[::-1], S)) / max(abs(c) for c in p)
    fp = None
    if len(p) - 1 <= 16:
        with mp.workdps(60):
            q = mp.findpoly(S, len(p) - 1, maxcoeff=10**40)
        fp = 'n/a' if q is None else ('agrees' if q in (p[::-1], [-c for c in p[::-1]]) else 'DIFFERS')
    d = float(mp.mpf(best[n]) - S)
    r = dict(n=n, deg=len(p) - 1, S=mp.nstr(S, 30), in_interval=bool(in_iv), rel_residual=float(res), findpoly=fp,
             printed=best[n], printed_minus_S=d)
    out.append(r); print(r, flush=True)
json.dump(out, open(os.path.join(HERE, 'crosscheck.json'), 'w'), indent=1)
