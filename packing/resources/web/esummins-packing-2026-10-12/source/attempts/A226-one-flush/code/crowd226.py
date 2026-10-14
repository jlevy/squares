"""A226 CROWD -- explicit teleport-stuck (four-crowd) packings ABOVE the record side, from corner dominoes.
Construction (one corner, BL frame, floor variant): the flush corner square A = [0,1]^2 slides UP the wall by eps
(A' = [0,1] x [eps, 1+eps]); its flush floor neighbour B = [1,2] x [0,1] is tilted CLOCKWISE by th = eps/2, raised to
y_b = (sin th + eps)/2 and shifted LEFT by eta = 0.9 (eps - y_b) tan th, so that its bottom-left vertex pokes into the
strip (0,1) x (0, eps) under A' (heights y_b - eta tan th .. y_b + eta cot th < eps) while its lowest vertex stays
above the floor (y_b >= sin th).  The wall variant is the mirror in the diagonal.  The rest of the packing (the CORE)
is translated by (w/2, w/2) into the container of side S = s + w, which leaves room eps/2 beside B' and eps above A'
for eps = w/2 at every corner.  Result: a packing at side S with every corner box met by two squares.
    python crowd226.py            -> results/crowd226.jsonl, crowd226.md   (every survey packing with 4 dominoes)
    python crowd226.py --ring11   -> results/ring11_226.jsonl               (n = 11: the 8-ring + 3 interior squares?)
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
try:
    import psutil
    psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    psutil.Process().cpu_affinity(list(range(16)))
except Exception:
    pass
from svg226 import verify_packing  # noqa: E402
from survey226 import corner_status, CORNERS, frame  # noqa: E402

ATT = os.path.abspath(os.path.join(HERE, '..'))
SURVEY = os.path.join(ATT, 'results', 'survey226.jsonl')
OUT = os.path.join(ATT, 'results', 'crowd226.jsonl')
MD = os.path.join(ATT, 'results', 'crowd226.md')
RING = os.path.join(ATT, 'results', 'ring11_226.jsonl')


def to_container(c, S, u, v, th):
    """corner-frame pose (u, v, th) -> container pose; reflections negate the tilt."""
    if c == 'BL':
        return (u, v, th)
    if c == 'BR':
        return (S - u, v, -th)
    if c == 'TR':
        return (S - u, S - v, th)
    return (u, S - v, -th)


def crowd_pair(eps, variant='floor'):
    """BL-frame poses (u, v, th) of A' and B' for the floor variant (B along the floor) or the wall variant."""
    th = eps / 2
    yb = (math.sin(th) + eps) / 2
    eta = 0.9 * (eps - yb) * math.tan(th)
    p = (1 - eta, yb)                                   # bottom-left vertex of B' (tilt -th)
    cB = (p[0] + (math.cos(th) + math.sin(th)) / 2, p[1] + (math.cos(th) - math.sin(th)) / 2)
    A = (0.5, 0.5 + eps, 0.0)
    B = (cB[0], cB[1], -th)
    if variant == 'wall':                                # mirror in the diagonal u <-> v
        A = (A[1], A[0], 0.0)
        B = (B[1], B[0], th)
    return A, B


def dominoes(sq, s):
    """per corner: (index of the flush corner square, index of a flush neighbour, variant) or None."""
    out = {}
    for c in CORNERS:
        iA = iF = iW = None
        for i, (x, y, th) in enumerate(sq):
            tilt = min(th % (math.pi / 2), math.pi / 2 - th % (math.pi / 2))
            if tilt > 1e-7:
                continue
            u, v = frame(c, s, np.array([[x, y]]))[0]
            if abs(u - .5) < 1e-7 and abs(v - .5) < 1e-7:
                iA = i
            elif abs(u - 1.5) < 1e-7 and abs(v - .5) < 1e-7:
                iF = i
            elif abs(u - .5) < 1e-7 and abs(v - 1.5) < 1e-7:
                iW = i
        if iA is not None and iF is not None:
            out[c] = (iA, iF, 'floor')
        elif iA is not None and iW is not None:
            out[c] = (iA, iW, 'wall')
        else:
            out[c] = None
    return out


def build_crowd(sq, s, w, corners=CORNERS):
    """the four-crowd at side S = s + w from a packing sq at side s with dominoes at the given corners."""
    S = s + w
    eps = w / 2
    dom = dominoes(sq, s)
    used = set()
    new = []
    for c in corners:
        if dom[c] is None:
            raise ValueError('no domino at ' + c)
        iA, iB, var = dom[c]
        used |= {iA, iB}
        A, B = crowd_pair(eps, var)
        new.append(to_container(c, S, *A))
        new.append(to_container(c, S, *B))
    core = [(x + w / 2, y + w / 2, th) for i, (x, y, th) in enumerate(sq) if i not in used]
    return new + core, S, dom, eps


def run_survey_crowds():
    rows = []
    for line in open(SURVEY, encoding='utf-8'):
        r = json.loads(line)
        if r['label'] == 'trump_cert':
            continue
        sq, s, n = [tuple(q) for q in r['squares']], r['side'], r['n']
        k = r['ceil_sqrt']
        dom = dominoes(sq, s)
        have = [c for c in CORNERS if dom[c] is not None]
        row = {'n': n, 'label': r['label'], 'side': s, 'ceil_sqrt': k, 'dominoes': {c: dom[c] for c in CORNERS},
               'n_dominoes': len(have)}
        if len(have) == 4:
            w = (k - s) / 2                              # half the slack: S is strictly below ceil(sqrt n)
            P, S, _, eps = build_crowd(sq, s, w)
            gap = verify_packing(P, S)
            cs = corner_status(P, S)
            row.update({'S': S, 'w': w, 'eps': eps, 'min_pair_gap': float(gap),
                        'pattern': ' '.join(str(cs[c]['n_meet']) for c in CORNERS),
                        'all_doubly_met': all(cs[c]['n_meet'] >= 2 for c in CORNERS),
                        'corners': {c: {'n_meet': cs[c]['n_meet'], 'depths': [m['depth'] for m in cs[c]['meeters']]}
                                    for c in CORNERS},
                        'squares': [[round(x, 12), round(y, 12), round(t, 12)] for (x, y, t) in P]})
        rows.append(row)
        print(n, len(have), row.get('S'), row.get('pattern'), row.get('min_pair_gap'))
    with open(OUT, 'w', encoding='utf-8') as fh:
        for r in rows:
            fh.write(json.dumps(r) + '\n')
    with open(MD, 'w', encoding='utf-8') as fh:
        fh.write('# A226 four-crowds above the record side (Proposition CROWD-ABOVE)\n\n')
        fh.write('| n | record side | ceil | dominoes | S = s + w | eps | pattern (meeters BL BR TR TL) | '
                 'min pair gap | verified packing |\n|---|---|---|---|---|---|---|---|---|\n')
        for r in rows:
            if 'S' in r:
                fh.write('| %d | %.6f | %d | %d | %.6f | %.4f | %s | %.2e | %s |\n' % (
                    r['n'], r['side'], r['ceil_sqrt'], r['n_dominoes'], r['S'], r['eps'], r['pattern'],
                    r['min_pair_gap'], 'yes' if r['all_doubly_met'] else 'NO'))
            else:
                fh.write('| %d | %.6f | %d | %d (%s) | -- | -- | -- | -- | no construction |\n' % (
                    r['n'], r['side'], r['ceil_sqrt'], r['n_dominoes'],
                    ' '.join(c for c in CORNERS if r['dominoes'][c] is None) + ' lack a domino'))
    print('wrote', OUT, MD)


def ring11():
    """n = 11: the eight-square crowd ring at side S < 4 (alternating floor / wall variants so the dominoes do not
    collide), then A222's region search for three more squares in the free region."""
    sys.path.insert(0, os.path.join(ATT, '..', 'A222-ring-swap', 'code'))
    import region222 as RG
    rows = []
    for S in (3.90, 3.95, 3.99):
        for eps in (0.02, 0.05, 0.10):
            ring = []
            for c, var in zip(CORNERS, ('floor', 'wall', 'floor', 'wall')):
                A, B = crowd_pair(eps, var)
                ring.append(to_container(c, S, *A))
                ring.append(to_container(c, S, *B))
            gap = verify_packing(ring, S)
            cs = corner_status(ring, S)
            res = RG.place(ring, S, 3, restarts=40, rng=np.random.default_rng(1))
            row = {'S': S, 'eps': eps, 'ring_gap': float(gap), 'ring_pattern': ' '.join(str(cs[c]['n_meet']) for c in CORNERS),
                   'found3': bool(res['found']), 'method': res.get('method'), 'k_max_greedy': res.get('k_max_greedy'),
                   'best_penalty': res.get('best_penalty'), 'poses': res.get('poses'), 'ring': ring}
            if res['found']:
                P = ring + [tuple(p) for p in res['poses']]
                row['full_gap'] = float(verify_packing(P, S))
                row['full_pattern'] = ' '.join(str(corner_status(P, S)[c]['n_meet']) for c in CORNERS)
            rows.append(row)
            print(S, eps, row['ring_pattern'], 'found3' if res['found'] else 'NOT found', res.get('k_max_greedy'),
                  res.get('best_penalty'), flush=True)
    with open(RING, 'w', encoding='utf-8') as fh:
        for r in rows:
            fh.write(json.dumps(r) + '\n')
    print('wrote', RING)


if __name__ == '__main__':
    if '--ring11' in sys.argv:
        ring11()
    else:
        run_survey_crowds()
