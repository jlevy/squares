#!/usr/bin/env python3
"""Run the regularizer over the register and flag records where tie-breaks matter (prototype; REGULARIZE.md).

Per record: variants yx / xy / sum (gravity order), nosym (if the rigid part has a symmetry), o1 (runner-up
orientation, if the orientation score ties).  "Tie-break matters" = two variants' results differ by > 1e-6 in some
square's position (same orientation), or the orientation ties.
Usage:  census.py [--procs 6] [--n 1-324] [--out runs/regularize/census.jsonl]
"""
import argparse, json, os, sys, time, traceback
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reg

KEEP = ('g', 'orient_tie', 'orient_topright', 'orient_scores', 'groups_before', 'groups_after', 'merged', 'rigid_sym', 'sym_imposed',
        'sym_dropped', 'place', 'face_spread', 'moved', 'max_move', 'refine', 'verify', 'contacts_before', 'free', 'by', 'status')


def diff(R1, R2):
    return max(max(abs(float(a) - float(b)) for a, b in zip(R1['X'], R2['X'])),
               max(abs(float(a) - float(b)) for a, b in zip(R1['Y'], R2['Y'])))


STYLE = os.environ.get('REG_STYLE', 'gravity')


def one_pretty(n):
    t0 = time.time()
    out = dict(n=n)
    try:
        P, R, rep = reg.regularize(n, style=STYLE, log=lambda *a: None)
        out.update({k: rep.get(k) for k in KEEP + ('sym_candidates', 'align_pairs', 'align_total', 'align_dropped', 'coincident', 'coinc_sym', 'coinc_nosym', 'sym_dropped_for_coincidence', 'coinc_replace', 'orient_source')})
        out['verify_all'] = rep['verify']['ok']
        out['tiebreak'] = (['face'] if (rep.get('face_spread') or 0) > 1e-6 else []) + \
            (['orient'] if rep['orient_tie'] else []) + (['topright'] if rep['orient_topright'] else [])
    except Exception as e:
        out['error'] = f'{type(e).__name__}: {e}'
        out['trace'] = traceback.format_exc()[-800:]
    out['seconds'] = round(time.time() - t0, 1)
    return out


def one(n):
    if STYLE in ('pretty', 'coincide'):
        return one_pretty(n)
    t0 = time.time()
    out = dict(n=n)
    try:
        res = {}
        for v, kw in (('yx', dict(gravity='yx')), ('xy', dict(gravity='xy')), ('sum', dict(gravity='sum'))):
            P, R, rep = reg.regularize(n, **kw, log=lambda *a: None)
            res[v] = (R, rep)
        out.update({k: res['yx'][1].get(k) for k in KEEP})
        out['verify_all'] = all(r[1]['verify']['ok'] for r in res.values())
        out['d_xy'] = diff(res['yx'][0], res['xy'][0])
        out['d_sum'] = diff(res['yx'][0], res['sum'][0])
        if res['yx'][1]['rigid_sym']:
            P, R, rep = reg.regularize(n, gravity='yx', sym='off')
            out['d_nosym'] = diff(res['yx'][0], R)
            out['verify_all'] &= rep['verify']['ok']
        out['tiebreak'] = sorted(k for k in ('d_xy', 'd_sum', 'd_nosym') if out.get(k, 0) > 1e-6) + \
            (['face'] if (out.get('face_spread') or 0) > 1e-6 else []) + (['orient'] if out['orient_tie'] else []) + (['topright'] if out['orient_topright'] else [])
    except Exception as e:
        out['error'] = f'{type(e).__name__}: {e}'
        out['trace'] = traceback.format_exc()[-800:]
    out['seconds'] = round(time.time() - t0, 1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--procs', type=int, default=6)
    ap.add_argument('--n', default='1-324')
    ap.add_argument('--out', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'runs',
                                                  'regularize', 'census.jsonl'))
    a = ap.parse_args()
    lo, hi = map(int, a.n.split('-')) if '-' in a.n else (int(a.n), int(a.n))
    ns = list(range(lo, hi + 1))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with Pool(a.procs) as pool, open(a.out, 'w') as f:
        # big n first so the pool finishes evenly
        for r in pool.imap_unordered(one, sorted(ns, reverse=True)):
            f.write(json.dumps(r, default=str) + '\n'); f.flush()
            print(r['n'], r.get('error', ''), r.get('tiebreak'), r['seconds'], flush=True)


if __name__ == '__main__':
    main()
