"""A226 SURVEY -- corner status of every best-known packing that beats ceil(sqrt n) (Ellsworth's page, SVGs in
../data/ellsworth/, fetched 2026-09-14) plus Trump from certs/trump11_certificate.json as a cross-check.
Per corner (BL, BR, TR, TL): the squares whose interior meets the OPEN unit corner box, whether the corner is FLUSH
(the slot square is in the packing), the meeters' tilts and depths.  Writes results/survey226.jsonl, survey226.md.
    python survey226.py
"""
import glob
import json
import math
import os
import sys
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
try:
    import psutil
    psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    psutil.Process().cpu_affinity(list(range(16)))
except Exception:
    pass
from svg226 import load_svg, verify_packing, square_corners, sat_overlap  # noqa: E402

ATT = os.path.abspath(os.path.join(HERE, '..'))
REPO = os.path.abspath(os.path.join(ATT, '..', '..'))
DATA = os.path.join(ATT, 'data', 'ellsworth')
OUT = os.path.join(ATT, 'results', 'survey226.jsonl')
MD = os.path.join(ATT, 'results', 'survey226.md')
CORNERS = ('BL', 'BR', 'TR', 'TL')
SOURCE = {5: 'Goebel 1979 (proved: Goebel)', 10: 'Goebel 1979 (proved: Stromquist 2003)', 11: 'Trump 1979 (rigid)',
          17: 'Bidwell 1998', 18: 'Hamalainen 1980 / Gustafsson 1981 variant pictured', 19: 'Wainwright 1979 (Cottingham)',
          26: 'Friedman 1997 (26b)', 27: 'Goebel 1979', 28: 'Ellsworth Dec 2025 (rigid)', 29: 'Schadt / Ellsworth Dec 2025',
          37: 'Cantrell 2002', 38: 'Goebel 1979', 39: 'Schadt / Ellsworth Jan 2026', 40: 'Goebel 1979 (rigid)',
          41: 'Schadt / Ellsworth Jan 2026', 50: 'Schadt / Ellsworth Dec 2025', 51: 'Schadt / Ellsworth 2026',
          52: 'Goebel 1979', 53: 'Cantrell 2002 / Ellsworth 2026', 54: 'Cantrell 2005 / DeVincentis 2014',
          55: 'Schadt / Ellsworth 2026'}


def frame(c, s, P):
    """container points -> corner frame (u, v) = distances from the corner's two walls."""
    x, y = P[:, 0], P[:, 1]
    u = x if c in ('BL', 'TL') else s - x
    v = y if c in ('BL', 'BR') else s - y
    return np.stack([u, v], 1)


def depth(F):
    """d = 1 - min over the square of max(u, v) (sampled on the boundary; the min of a convex function)."""
    best = math.inf
    for i in range(4):
        a, b = F[i], F[(i + 1) % 4]
        for t in np.linspace(0, 1, 401):
            p = a + t * (b - a)
            best = min(best, max(p[0], p[1]))
    return 1 - best


def corner_status(sq, s, tol=1e-9):
    box = np.array([(0, 0), (1, 0), (1, 1), (0, 1)], float)
    out = {}
    for c in CORNERS:
        meet = []
        flush = False
        for i, (x, y, th) in enumerate(sq):
            F = frame(c, s, square_corners(x, y, th))
            if sat_overlap(F, box) > tol:
                cen = F.mean(0)
                tilt = math.degrees(th % (math.pi / 2))
                tilt = min(tilt, 90 - tilt)
                fl = bool(tilt < 1e-7 and abs(cen[0] - .5) < 1e-7 and abs(cen[1] - .5) < 1e-7)
                flush = flush or fl
                meet.append({'i': i, 'tilt_deg': round(tilt, 4), 'depth': round(depth(F), 5),
                             'centre': [round(float(cen[0]), 5), round(float(cen[1]), 5)], 'flush': fl})
        out[c] = {'n_meet': len(meet), 'flush': flush, 'meeters': meet}
    return out


def load_trump():
    t = json.load(open(os.path.join(REPO, 'certs', 'trump11_certificate.json'), encoding='utf-8'))
    sq = [(float(Fraction(q['cx'])), float(Fraction(q['cy'])), 2 * math.atan(float(Fraction(q['t']))))
          for q in t['squares']]
    return sq, float(Fraction(t['container_side']))


def wall_touchers(sq, s, tol=1e-9):
    cnt = {'floor': 0, 'right': 0, 'ceil': 0, 'left': 0}
    for q in sq:
        C = square_corners(*q)
        cnt['floor'] += C[:, 1].min() < tol
        cnt['left'] += C[:, 0].min() < tol
        cnt['ceil'] += C[:, 1].max() > s - tol
        cnt['right'] += C[:, 0].max() > s - tol
    return {k: int(v) for k, v in cnt.items()}


def analyse(label, sq, s, source):
    n = len(sq)
    k = math.ceil(math.sqrt(n) - 1e-12)
    gap = verify_packing(sq, s)
    cs = corner_status(sq, s)
    row = {'label': label, 'n': n, 'side': s, 'ceil_sqrt': k, 'slack': k - s, 'min_pair_gap': float(gap),
           'n_tilted': int(sum(1 for q in sq if min(math.degrees(q[2] % (math.pi / 2)) % 90,
                                                 90 - math.degrees(q[2] % (math.pi / 2)) % 90) > 1e-7)),
           'flush_corners': int(sum(cs[c]['flush'] for c in CORNERS)),
           'singly_met': int(sum(cs[c]['n_meet'] <= 1 for c in CORNERS)),
           'doubly_met': int(sum(cs[c]['n_meet'] >= 2 for c in CORNERS)),
           'pattern': ' '.join(('F' if cs[c]['flush'] else str(cs[c]['n_meet'])) for c in CORNERS),
           'walls': wall_touchers(sq, s), 'corners': cs, 'source': source,
           'squares': [[round(x, 12), round(y, 12), round(th, 12)] for (x, y, th) in sq]}
    return row


def main():
    rows = []
    files = sorted(glob.glob(os.path.join(DATA, 'square-*.svg')),
                   key=lambda f: int(''.join(ch for ch in os.path.basename(f)[7:-4] if ch.isdigit())))
    for f in files:
        sq, s, _ = load_svg(f)
        lab = os.path.basename(f)[:-4]
        n = len(sq)
        rows.append(analyse(lab, sq, s, SOURCE.get(n, '?')))
        print(lab, n, round(s, 6), rows[-1]['pattern'])
    sq, s = load_trump()
    rows.append(analyse('trump_cert', sq, s, 'certs/trump11_certificate.json (s0 = 969271/250000)'))
    print('trump_cert', len(sq), round(s, 6), rows[-1]['pattern'])
    with open(OUT, 'w', encoding='utf-8') as fh:
        for r in rows:
            fh.write(json.dumps(r) + '\n')
    with open(MD, 'w', encoding='utf-8') as fh:
        fh.write('# A226 survey -- corner status of the record packings below ceil(sqrt n)\n\n')
        fh.write('Pattern = corners BL BR TR TL: F = flush (slot square present), k = number of squares meeting the open '
                 'unit corner box.  Depth = 1 - min over the square of max(u, v) in the corner frame.\n\n')
        fh.write('| n | side | ceil | slack | tilted | flush corners | singly met | doubly met | pattern | '
                 'wall touchers F/R/C/L | source |\n|---|---|---|---|---|---|---|---|---|---|---|\n')
        for r in rows:
            w = r['walls']
            fh.write('| %d | %.6f | %d | %.4f | %d | %d | %d | %d | %s | %d/%d/%d/%d | %s (%s) |\n' % (
                r['n'], r['side'], r['ceil_sqrt'], r['slack'], r['n_tilted'], r['flush_corners'], r['singly_met'],
                r['doubly_met'], r['pattern'], w['floor'], w['right'], w['ceil'], w['left'], r['source'], r['label']))
        fh.write('\n## Doubly-met corners (meeters: index, tilt deg mod 90 folded to [0, 45], depth, frame centre)\n\n')
        for r in rows:
            for c in CORNERS:
                cs = r['corners'][c]
                if cs['n_meet'] >= 2:
                    ms = '; '.join('#%d tilt %.3f depth %.4f centre (%.3f, %.3f)' % (
                        m['i'], m['tilt_deg'], m['depth'], m['centre'][0], m['centre'][1]) for m in cs['meeters'])
                    fh.write('- n = %d (%s) %s: %s\n' % (r['n'], r['label'], c, ms))
    print('wrote', OUT, MD)


if __name__ == '__main__':
    main()
