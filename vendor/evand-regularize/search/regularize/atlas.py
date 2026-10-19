#!/usr/bin/env python3
"""Atlas of all records, right-justified triangle layout (row k = n from (k-1)^2 + 1 to k^2, perfect squares on
the right edge, as jlevy's Triangle view).  Prototype; REGULARIZE.md.

  atlas.py compute [--procs 12] [--style coincide]     regularize every n, coordinates -> runs/regularize/coords/
  atlas.py draw [--which result|source] [--out F.png]  draw the triangle from the saved coordinates

Colours: axis-parallel squares grey-green; tilted squares by tilt on a continuous hue scale (|tilt| 0..45 deg ->
hue), positive tilts lighter, negative darker, so a fan of slightly different angles reads as one family.
"""
import argparse, json, math, os, sys, colorsys
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
RUNS = os.path.join(HERE, '..', '..', 'runs', 'regularize')
COORDS = os.path.join(RUNS, 'coords')


def level_of(reg, P0, R, rep, policy):
    """0 identical / 1 rattlers only / 2 same packing (connected) / 3 alternate (not shown connected)."""
    ch = rep.get('merged_determined') or []
    free = set(P0['free'])
    moved = set(rep.get('moved') or [])
    angle_changed = {i for i in range(P0['n']) if abs(reg.fold(R['T'][i] - P0['T'][i])) > 1e-12} if rep['g'] == 0 else None
    if not moved and not ch and not rep.get('merged'):
        return 0, 'identical (orientation aside)'
    touched = moved | (angle_changed or set())
    if touched and touched <= free:
        return 1, 'differs from the source only in rattlers (force-free squares)'
    if policy == 'conservative' or not any(c[0] == 'determined-merge' for c in ch):
        return 2, 'same packing: traversable without expansion (angle moves path-checked; slides by construction)'
    # fewest with merges of determined angles: joint path test from the source angles
    P1 = dict(P0); T_to = list(P0['T'])
    Pm, _ = reg.merge_angles(P0, P0['free'], lambda *a: None)
    Pd, _ = reg.merge_determined(Pm, policy='fewest', log=lambda *a: None)
    ok, sb, _ = reg.path_ok(P0, Pd['T'])
    if ok:
        return 2, 'same packing: traversable without expansion (joint angle path checked)'
    return 3, f'alternate packing at the record side: not shown connected to the source (path blocked at s = {sb:.2f})'


def compute_one(args):
    n, style, policy = args
    import reg, mpmath as mpm
    cdir = COORDS if policy == 'free' else os.path.join(COORDS, policy)
    os.makedirs(cdir, exist_ok=True)
    out = os.path.join(cdir, f'n-{n}.json')
    try:
        P, R, rep = reg.regularize(n, style=style, angle_policy=policy, log=lambda *a: None)
        js = lambda Q: dict(S=float(Q['S']), sq=[[float(x), float(y), float(t)] for x, y, t in zip(Q['X'], Q['Y'], Q['T'])])
        src = reg.load(n)
        poster = os.path.join(RUNS, 'poster', policy); os.makedirs(poster, exist_ok=True)
        lev, levtext = level_of(reg, reg.load(n), d4inv(reg, R, rep['g']), rep, policy)
        cert_ok, Sp = reg.write_cert(R, os.path.join(poster, f'n-{n:03d}.cert'))
        hp = lambda Q: dict(S=mpm.nstr(Q['S'], 50), sq=[[mpm.nstr(x, 50), mpm.nstr(y, 50), mpm.nstr(t, 50)]
                                                       for x, y, t in zip(Q['X'], Q['Y'], Q['T'])])
        json.dump(dict(n=n, S_exact=mpm.nstr(R['S'], 60), S_cert=str(Sp), cert_valid=cert_ok,
                       verify_80=rep['verify'], input=reg.refreshed(n) or 'search/exact/batch', by=rep['by'],
                       orientation_g=rep['g'], symmetry=rep.get('sym_imposed'), shape=rep.get('shape', {}).get('kind'),
                       groups_before=rep['groups_before'], groups_after=rep['groups_after'],
                       angle_changes=rep.get('merged_determined'), packing=hp(R),
                       policy=policy, level=lev, level_text=levtext,
                       note='regularized display view of a certified packing at the same side; not a new bound'),
                  open(os.path.join(poster, f'n-{n:03d}.json'), 'w'), default=str)
        json.dump(dict(n=n, ok=bool(rep['verify']['ok']) and cert_ok, g=rep['g'], kind=rep.get('shape', {}).get('kind'),
                       groups_before=rep['groups_before'], groups_after=rep['groups_after'],
                       min_gap=rep['verify']['min_gap'], seconds=None,
                       sym=rep.get('sym_imposed'), by=rep['by'], source=js(src), result=js(R)), open(out, 'w'))
        return n, rep['verify']['ok']
    except Exception as e:
        return n, f'{type(e).__name__}: {e}'


def d4inv(reg, R, g):
    """R mapped back to the source frame (undo container symmetry g) so it can be compared square by square."""
    for h in range(8):
        Q = reg.d4(R, h)
        Qg = reg.d4(Q, g)
        if all(abs(float(a - b)) < 1e-9 for a, b in zip(Qg['X'], R['X'])) and all(abs(float(a - b)) < 1e-9 for a, b in zip(Qg['Y'], R['Y'])):
            Q['g'] = 0
            return Q
    return R


def tile_color(t):
    if abs(t) < 1e-9:
        return (0.80, 0.86, 0.78)
    a = min(abs(t), 45.0) / 45.0
    h = (0.02 + 0.80 * a) % 1.0                     # small tilt: orange/red ... 45: violet
    l = 0.60 if t > 0 else 0.42
    return colorsys.hls_to_rgb(h, l, 0.65)


BEST = {}
GROUP_PALETTE = ['#e6194b', '#3cb44b', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#469990',
                 '#9a6324', '#800000', '#808000', '#000075', '#fabed4', '#ffd8b1', '#dcbeff', '#aaffc3', '#a9a9a9']


def group_ids(thetas):
    """Rotation group of each square by exact equality of the 50-digit angles (mod 90, to 1e-30): 0 = axis,
    1.. = tilted groups by decreasing size."""
    from mpmath import mp, mpf
    mp.dps = 60
    T = [mpf(t) for t in thetas]
    fold = lambda a: a - 90 * mp.floor((a + 45) / 90)
    reps, mem = [], []
    for i, t in enumerate(T):
        for k, r in enumerate(reps):
            if abs(fold(t - r)) < mpf('1e-30'):
                mem[k].append(i); break
        else:
            reps.append(t); mem.append([i])
    order = sorted(range(len(reps)), key=lambda k: (abs(fold(reps[k])) > mpf('1e-30'), -len(mem[k])))
    gid = [0] * len(T)
    nxt = 1
    for k in order:
        g = 0 if abs(fold(reps[k])) < mpf('1e-30') else nxt
        if g:
            nxt += 1
        for i in mem[k]:
            gid[i] = g
    return gid


def group_color(g):
    return (0.80, 0.86, 0.78) if g == 0 else GROUP_PALETTE[(g - 1) % len(GROUP_PALETTE)]


def draw(which, out, size=0.55, label=True, colour='angle'):
    if which == 'best':
        BEST.update({r['n']: r for r in json.load(open(os.path.join(HERE, 'lists', 'best.json')))})
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon
    K = 18
    ncol = 2 * K - 1
    fig = plt.figure(figsize=(ncol * size, K * size * 1.18))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, ncol); ax.set_ylim(0, K * 1.18); ax.axis('off')
    for k in range(1, K + 1):
        for n in range((k - 1) ** 2 + 1, k * k + 1):
            col = ncol - 1 - (k * k - n)               # right-justified: k^2 in the last column
            row = K - k
            if which == 'best':
                pol = BEST[n]['variant']
                d = json.load(open(os.path.join(RUNS, 'poster', pol, f'n-{n:03d}.json')))['packing']
                Q = dict(S=float(d['S']), sq=[[float(x), float(y), float(t)] for x, y, t in d['sq']])
                Q['group'] = group_ids([t for _, _, t in d['sq']])
            else:
                f = os.path.join(COORDS, f'n-{n}.json')
                if not os.path.exists(f):
                    continue
                d = json.load(open(f))
                Q = d[which]
            S = Q['S']; sc = 0.86 / S
            x0, y0 = col + 0.07, row * 1.18 + 0.22
            ax.add_patch(Polygon([(x0, y0), (x0 + S * sc, y0), (x0 + S * sc, y0 + S * sc), (x0, y0 + S * sc)],
                                 closed=True, fc='white', ec='k', lw=0.4))
            for q, (x, y, t) in enumerate(Q['sq']):
                c, s = math.cos(math.radians(t)), math.sin(math.radians(t))
                pts = [(x0 + sc * (x + 0.5 * (c * a - s * b)), y0 + sc * (y + 0.5 * (s * a + c * b)))
                       for a, b in ((1, 1), (-1, 1), (-1, -1), (1, -1))]
                fc = group_color(Q['group'][q]) if colour == 'group' and 'group' in Q else tile_color(t)
                ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=(0.3, 0.3, 0.3), lw=0.12))
            if label:
                ax.text(col + 0.5, row * 1.18 + 0.08, str(n), ha='center', va='center', fontsize=3.2,
                        color='k' if int(math.isqrt(n)) ** 2 != n else (0.7, 0, 0))
    fig.savefig(out, dpi=220)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['compute', 'draw'])
    ap.add_argument('--procs', type=int, default=12)
    ap.add_argument('--style', default='coincide')
    ap.add_argument('--which', default='best', choices=['best', 'result', 'source'])
    ap.add_argument('--out', default=None)
    ap.add_argument('--colour', default='angle', choices=['angle', 'group'])
    ap.add_argument('--n', default='1-324')
    ap.add_argument('--ns', default=None, help='comma list (overrides --n)')
    ap.add_argument('--refreshed', action='store_true', help='only n with a refreshed input')
    ap.add_argument('--policy', default='free', choices=['free', 'conservative', 'fewest'])
    a = ap.parse_args()
    if a.cmd == 'compute':
        os.makedirs(COORDS, exist_ok=True)
        lo, hi = map(int, a.n.split('-'))
        ns = list(range(hi, lo - 1, -1))
        if a.ns:
            ns = [int(x) for x in a.ns.split(',')]
        if a.refreshed:
            import reg
            ns = [n for n in ns if reg.refreshed(n)]
        print('computing', len(ns), flush=True)
        with Pool(a.procs) as pool:
            for n, st in pool.imap_unordered(compute_one, [(n, a.style, a.policy) for n in sorted(ns, reverse=True)]):
                if st is not True:
                    print(n, st, flush=True)
    else:
        draw(a.which, a.out or os.path.join(RUNS, ('atlas-result' if a.which == 'best' else f'atlas-{a.which}') + ('-groups' if a.colour == 'group' else '') + '.png'), colour=a.colour)


if __name__ == '__main__':
    main()
