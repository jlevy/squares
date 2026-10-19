#!/usr/bin/env python3
"""Breadth-first basin exploration (10-07, Evan: more explore, less exploit).  Quality-diversity over basins (MAP-Elites
style): an archive of distinct polished minima binned by a content-agnostic descriptor; parents are drawn uniformly over
bins (not by quality), and within a bin favouring rarely expanded basins.  Basins up to S_MAX (above the integer k) are
kept as stepping stones; grid-obstructed states (full lines / staggered axis chains) are discarded.

Quench per proposal: fq screen (ALM + <= 8 SLP iterations, no flips, loosen drawn from 1.0/1.02/1.05).  A screened side
within `same` of a known basin counts as a return (visit, no polish); otherwise full polish (fq --no-alm) and, if new,
an archive entry.

Descriptor (search): (ntilted bin of 2, number of tilt-angle classes, below-k flag).  Evaluation only (n = 110): role
counts (L, B, axis, other) as in census_roles, and novelty against runs/known110.json (48 certified sub-11 minima).

  explore.py --n 110 --starts seeds/rec110.txt ... --minutes 60 --procs 15 --out runs/ex0
  explore.py --report runs/ex0
"""
import argparse, collections, json, math, os, random, subprocess, tempfile, time
from concurrent.futures import ProcessPoolExecutor, FIRST_COMPLETED, wait
from pk import identity as ID           # SAME_SIDE: one f64 same-side tolerance (10-11)
import mcmin, hop
from pk.engine import QOpt, SCREEN, POLISH   # the explorer's fq stages (one flag builder, 10-14)
from pk import fingerprint as FP
from pk.bandit import KindBandit, CellBandit   # moved to pk/bandit.py (10-13)

HERE = os.path.dirname(os.path.abspath(__file__))


class A:                                     # attributes mcmin's moves look up
    alpha = 2.0; reinsert = 'clear'; remove = 'uniform'; tau = 0.0


def mv_bigkick(s, sq, rng, a):
    sig = math.exp(rng.uniform(math.log(0.05), math.log(0.2)))
    return [(x + rng.gauss(0, sig), y + rng.gauss(0, sig), t + rng.gauss(0, 20 * sig)) for x, y, t in sq], f'bigkick {sig:.3f}'


ANNEAL = os.path.join(HERE, 'target/release/anneal')
UNP_TOL = 1e-5     # --polish-gate: a screened (unpolished) side is the same basin as an archive / novelty-ref side within this
                   # (screen side error: median ~7e-5 at k = 0, 2e-6 at k = 4, 1e-8 at k = 8 SLP iterations; PACKER 10-07)   # current src (10-11; was target-dev, a 10-08 build)


def melt_side(s, sq, rng, a, rad_r=(1.5, 3.5), rmax_r=(0.05, 0.2)):
    """Regional melt (anneal melt): squares within R of a random square get rounded corners (up to rmax), hard-particle MC
    at high pressure around them, then squared up again; large but local, non-destructive rearrangement.
    Returns (side, squares, desc): the NPT box changes size, so the side matters (falls back to bigkick on failure)."""
    rad, rmax = rng.uniform(*rad_r), rng.uniform(*rmax_r)
    i = rng.randrange(len(sq))
    avoid = os.environ.get('PK_MELT_AVOID')              # protected melt (Evan 10-15): centres at least rad + margin
    if avoid:                                            # from every protected point, so that segment is left alone
        pts, margin = json.load(open(avoid)), float(os.environ.get('PK_MELT_MARGIN', '1.0'))
        ok = [j for j in range(len(sq)) if all(math.hypot(sq[j][0] - x, sq[j][1] - y) > rad + margin for x, y in pts)]
        if not ok:
            rad = max(1.0, min(math.hypot(sq[j][0] - x, sq[j][1] - y) for j in range(len(sq)) for x, y in pts) - margin)
            ok = [j for j in range(len(sq)) if all(math.hypot(sq[j][0] - x, sq[j][1] - y) > rad + margin for x, y in pts)]
        if ok:
            i = ok[rng.randrange(len(ok))]
    with tempfile.TemporaryDirectory() as tmp:
        mcmin.write_deg(f'{tmp}/in.txt', s, sq)
        r = subprocess.run([ANNEAL, 'melt', '--in', f'{tmp}/in.txt', '--out', f'{tmp}/out.txt', '--cx', str(sq[i][0]), '--cy', str(sq[i][1]),
                            '--rad', f'{rad:.3f}', '--rmax', f'{rmax:.3f}', '--sweeps', '3000', '--bp', '2000',
                            '--seed', str(rng.randrange(1 << 30))], capture_output=True, text=True, timeout=300)
        if r.returncode != 0 or not os.path.exists(f'{tmp}/out.txt'):
            sq2, desc = mv_bigkick(s, sq, rng, a)
            return s, sq2, 'melt failed ' + desc
        s2, sq2 = mcmin.load_deg(f'{tmp}/out.txt')
    return s2, sq2, f'melt R{rad:.2f} r{rmax:.2f} s{s2:.5f}'


BIGMELT = dict(rad_r=(3.5, 7.0), rmax_r=(0.1, 0.25))     # TT3 arm M (10-15): melts too big for the default range
GLS_DELTA = (1e-4, 3e-3)                                 # TT3 arm L: relative shrink below min(parent, gate line), log-uniform
GLS_MS_PER_N = 2.0                                       # GLS wall budget per proposal, ms per square


# Parent value model (10-14, PACKER "Parent / move value model", analysis/parent_model.py 'full' fit on TT3 G / M / L):
# log rate of distinct new near-frontier minima per CPU-s = gap-bin term + screened / start terms
# - 0.78 log(1 + times expanded) + 0.57 log(1 + archive-new children).  Kind and n terms omitted (kind is the bandit's;
# n is constant within a run).  Pick weight = rate ** beta over every archive entry below smax.
PM_GAP = ((0.0, -0.26), (1e-4, 0.13), (1e-3, -0.80), (3e-3, -2.14), (1e-2, -2.91), (3e-2, -4.06), (1e-1, -5.00))
PM_UNP, PM_START, PM_EXP, PM_KIDS = -0.30, 0.16, -0.78, 0.57


def pm_lograte(e, front):
    g = e['s'] - front
    c = 0.0
    for lo, v in PM_GAP:
        if g >= lo:
            c = v
    return (c + PM_UNP * bool(e.get('unpolished')) + PM_START * e['kind'].startswith('start')
            + PM_EXP * math.log1p(e['expanded']) + PM_KIDS * math.log1p(e.get('children', 0)))


def pm_pick(E, front, smax, beta, rng):
    """parent drawn with weight exp(beta * pm_lograte); returns (entry, its pick probability)"""
    C = [e for e in E if e['s'] < smax] or E
    L = [beta * pm_lograte(e, front) for e in C]
    m = max(L); W = [math.exp(x - m) for x in L]; tot = sum(W)
    j = rng.choices(range(len(C)), weights=W)[0]
    return C[j], W[j] / tot


def gls_side(s, sq, rng, ref):
    """Sparrow-style GLS feasibility attempt (anneal gls, 10-15): target side min(s, ref) (1 - delta); squares beyond a
    random cut per axis slide in, then weighted-overlap relaxation + sampled relocation of colliding squares + GLS pair
    weights.  Returns (target side, squares, desc); the screen resolves any overlap left (falls back to a kick on failure)."""
    base = min(s, ref) if ref and math.isfinite(ref) else s
    dl = math.exp(rng.uniform(math.log(GLS_DELTA[0]), math.log(GLS_DELTA[1])))
    tgt = base * (1 - dl)
    with tempfile.TemporaryDirectory() as tmp:
        mcmin.write_deg(f'{tmp}/in.txt', s, sq)
        r = subprocess.run([ANNEAL, 'gls', '--in', f'{tmp}/in.txt', '--out', f'{tmp}/out.txt', '--shrink', repr(1 - tgt / s),
                            '--ms', f'{GLS_MS_PER_N * len(sq):.0f}', '--seed', str(rng.randrange(1 << 30))],
                           capture_output=True, text=True, timeout=300)
        if r.returncode != 0 or not os.path.exists(f'{tmp}/out.txt'):
            sq2, desc = mv_bigkick(s, sq, rng, a=None)
            return s, sq2, 'gls failed ' + desc
        s2, sq2 = mcmin.load_deg(f'{tmp}/out.txt')
        try:
            j = json.loads(r.stdout)
        except Exception:
            j = {}
    return s2, sq2, f'gls d{dl:.1e} feas{int(bool(j.get("feasible")))} ov{j.get("overlap", -1):.1e} st{j.get("strikes", -1)}'


def mv_melt(s, sq, rng, a):
    """melt_side without the side (2-tuple move interface for polish_replay / polish_trace / mcmin-style callers).
    Lossy: the anneal's box size is dropped.  explore.work uses melt_side."""
    _, sq2, desc = melt_side(s, sq, rng, a)
    return sq2, desc


def _axis(t, tol=3.0):
    a = t % 90
    return min(a, 90 - a) < tol


def mv_rowslide(s, sq, rng, a):
    """Slide a contiguous run of axis squares along its row (or column) by 0.2-0.6: a coordinated move kicks never make."""
    ax = [i for i, q in enumerate(sq) if _axis(q[2])]
    if not ax:
        return mv_bigkick(s, sq, rng, a)
    i0 = rng.choice(ax)
    horiz = rng.random() < 0.5
    c = 1 if horiz else 0                    # coordinate shared by the row (y for a horizontal row)
    run = [j for j in ax if abs(sq[j][c] - sq[i0][c]) < 0.35]
    run.sort(key=lambda j: sq[j][1 - c])
    # contiguous component containing i0 (gaps < 0.3 between neighbours along the row)
    k = run.index(i0); lo = hi = k
    while lo > 0 and sq[run[lo]][1 - c] - sq[run[lo - 1]][1 - c] < 1.3: lo -= 1
    while hi < len(run) - 1 and sq[run[hi + 1]][1 - c] - sq[run[hi]][1 - c] < 1.3: hi += 1
    seg = set(run[lo:hi + 1])
    if rng.random() < 0.5:                   # sometimes only part of the run (one end stays)
        seg = set(run[lo:k + 1]) if rng.random() < 0.5 else set(run[k:hi + 1])
    d = rng.choice((-1, 1)) * rng.uniform(0.2, 0.6)
    out = []
    for j, (x, y, t) in enumerate(sq):
        if j in seg:
            x, y = (x + d, y) if horiz else (x, y + d)
        out.append((x, y, t))
    return out, f'rowslide {len(seg)} {d:+.2f} {"h" if horiz else "v"}'


def mv_chainshift(s, sq, rng, a):
    """Vacancy -> hole chain shift: remove a square, move a chain of squares one step each toward the vacancy along the
    line to a clearance hole, re-insert the removed square at the hole."""
    hs = mcmin.holes(s, sq)
    if not hs:
        return mv_bigkick(s, sq, rng, a)
    hx, hy, _ = rng.choices(hs[:10], weights=[h[2] for h in hs[:10]])[0]
    near = sorted(range(len(sq)), key=lambda j: math.hypot(sq[j][0] - hx, sq[j][1] - hy))[:12]
    i = rng.choice(near[2:12]) if len(near) > 3 else near[-1]
    px, py = sq[i][0], sq[i][1]
    L = math.hypot(hx - px, hy - py) or 1.0
    ux, uy = (hx - px) / L, (hy - py) / L
    chain = []
    for j, (x, y, t) in enumerate(sq):       # squares near the segment vacancy -> hole, ordered from the vacancy
        if j == i: continue
        u = (x - px) * ux + (y - py) * uy
        w = abs(-(x - px) * uy + (y - py) * ux)
        if 0 < u < L and w < 0.6:
            chain.append((u, j))
    chain.sort()
    out = list(sq)
    prev = (px, py)
    for _, j in chain:                       # each takes its predecessor's place (keeps its own angle)
        x, y, t = sq[j]
        out[j] = (prev[0], prev[1], t)
        prev = (x, y)
    out[i] = (hx, hy, rng.choice((sq[i][2], 0.0)))
    return out, f'chainshift {len(chain)} L={L:.2f}'


def mv_mirror(s, sq, rng, a):
    """Reflect a local cluster across a horizontal, vertical or diagonal line through a random point (flips junction
    handedness; angles reflect accordingly)."""
    p = (rng.uniform(0, s), rng.uniform(0, s)); r = rng.uniform(1.2, 3.0)
    kind = rng.choice(('h', 'v', 'd'))
    out = []
    n = 0
    for x, y, t in sq:
        if math.hypot(x - p[0], y - p[1]) < r:
            n += 1
            dx, dy = x - p[0], y - p[1]
            if kind == 'h': x, y, t = x, p[1] - dy, -t
            elif kind == 'v': x, y, t = p[0] - dx, y, -t
            else: x, y, t = p[0] + dy, p[1] + dx, 90 - t
        out.append((x, y, t % 90))
    return out, f'mirror {kind} {n}'


MOVES = dict(mcmin.MOVES, melt=mv_melt, bigkick=mv_bigkick, rowslide=mv_rowslide, chainshift=mv_chainshift, mirror=mv_mirror)
CROSS_P, CROSS_K, CROSS_CANDS = 5, 3, 30
CROSS2_VARIANTS = ('field', 'softfield', 'half', 'bestfit:2')   # battery mix; per-variant counts too small to pick one
CROSS2_NEAR = 8                              # above-k parents: nearest of this many candidate mates
# 10-09 bench c110a (new certified basins per CPU-h): aswap 177, kick 157, kicksym 137, lkick 134, rowslide 131, bigkick 101,
# mirror 52, crot 49, band 48, chainshift 0, reinsert 0 -> the last two off
WEIGHTS = dict(kick=2, kicksym=1, lkick=2, bigkick=2, crot=1, aswap=2, band=1, reinsert=0, rowslide=2, chainshift=0, mirror=2)


def tilt_classes(sq, thr=1.0, gap=3.0):
    a = sorted(t % 90 for _, _, t in sq if min(t % 90, 90 - t % 90) > thr)
    if not a:
        return 0, 0
    cl = 1 + sum(1 for u, v in zip(a, a[1:]) if v - u > gap)
    return len(a), cl


def roles(sq):
    c = collections.Counter()
    for _, _, t in sq:
        a = t % 90; d = min(a, 90 - a)
        c['A' if d < 3 else 'L' if 10 < a < 45 else 'B' if 45 <= a < 80 else 'O'] += 1
    return (c['L'], c['B'], c['A'], c['O'])


def roles_j(sq):
    """Role counts with a junction class (10-11): (L 10-40, B 50-80, axis < 3 off, J 40-50 deg mod 90, other).  roles()
    cuts at 45 deg, so the ~45 deg junction squares (the 10-05 (19,19,68,4) family) split at random into L or B."""
    c = collections.Counter()
    for _, _, t in sq:
        a = t % 90; d = min(a, 90 - a)
        c['A' if d < 3 else 'L' if 10 < a < 40 else 'J' if 40 <= a <= 50 else 'B' if 50 < a < 80 else 'O'] += 1
    return (c['L'], c['B'], c['A'], c['J'], c['O'])


def descriptor(s, sq, k):
    nt, ncl = tilt_classes(sq)
    return (nt // 2, ncl, s < k)


def work(job):
    """One proposal: move, screen, (maybe) full polish, grid check.  Runs in a worker process.  Adds 'cpu' = measured CPU
    seconds of the worker + its waited-for children (fq, anneal) for this proposal."""
    from pk.manifest import cpu_seconds
    c0 = cpu_seconds()
    r = _work(job)
    r['cpu'] = round(cpu_seconds() - c0, 3)
    return r


def _work(job):
    s, sq, kind, seed, k, known_sides, same, smax, pol_above = job[:9]
    pextra = tuple(job[9]) if len(job) > 9 else ()
    from layout import full_lines
    rng = random.Random(seed)
    if kind == 'cross':                     # recombination (cross.py): best-fit K of P same-type archive parents
        import cross
        cands = job[10] if len(job) > 10 else []
        al = []
        for pth in cands:
            sQ, Q = mcmin.load_deg(pth)
            d, Qa = cross.align(sq, s, Q, sQ)
            al.append((d, Qa))
        al.sort(key=lambda c: c[0])
        parents = [sq] + [c[1] for c in al[:CROSS_P - 1]]
        prop = cross.recombine(f'bestfit:{CROSS_K}', s, parents, rng) if len(parents) > 1 else MOVES['kick'](s, sq, rng, A)[0]
        desc = f'cross P{len(parents)} K{CROSS_K} d{al[0][0] if al else 0:.3f}'
    elif kind == 'cross2':                  # two-parent recombination (battery 10-09 winner: cross:P=2,pick=random)
        import cross
        cands = job[10] if len(job) > 10 else []
        if not cands:
            prop, desc = MOVES['kick'](s, sq, rng, A); desc = 'cross2 no-mate ' + desc
        else:
            # mate: random for sub-k parents; for above-k parents the nearest of the candidates (battery: random
            # mates sent above-grid starts to the grid 71 % vs 33 % for near mates, 42 % for the arm mix)
            if s < k:
                mate = cands[0]; sQ, Q = mcmin.load_deg(mate); d, Qa = cross.align(sq, s, Q, sQ)
            else:
                best = None
                for pth in cands[:CROSS2_NEAR]:
                    sQ, Q = mcmin.load_deg(pth); c = cross.align(sq, s, Q, sQ)
                    if best is None or c[0] < best[0][0]:
                        best = (c, pth)
                (d, Qa), mate = best
            v = rng.choice(CROSS2_VARIANTS)
            prop = cross.recombine(v, s, [sq, Qa], rng)
            desc = f'cross2 {v} {"rand" if s < k else "near"} d{d:.3f}'
    elif kind == 'ashallow':                # shallow whole-box anneal (pk.moves 'anneal' arm, rmax 0.03-0.15)
        from pk import moves as pkm
        from pk.packing import Packing
        import numpy as np
        q, info = pkm.apply(Packing(s, np.array(sq, float)), 'ashallow', rng.randrange(1 << 30))
        if info.get('failed'):
            prop, desc = MOVES['kick'](s, sq, rng, A); desc = 'ashallow failed ' + desc
        else:
            s = float(q.s); prop = q.tuples(); desc = f'ashallow s{s:.5f}'
    elif kind == 'harden':                  # soft-to-rigid re-hardening (src/harden.rs, 10-14; T1: #575's band merge)
        s, prop, desc = mv_harden(s, sq, rng)
    elif kind == 'melt':                    # regional NPT melt: the box changes size, keep the anneal's side
        s, prop, desc = melt_side(s, sq, rng, A)
    elif kind == 'bigmelt':                 # TT3 arm M: larger regions, deeper rounding
        s, prop, desc = melt_side(s, sq, rng, A, **BIGMELT); desc = 'big' + desc
    elif kind == 'gls':                     # TT3 arm L: GLS feasibility attempt below the gate line
        s, prop, desc = gls_side(s, sq, rng, pol_above)
    else:
        prop, desc = MOVES[kind](s, sq, rng, A)
    kr = tuple(job[11]) if len(job) > 11 and job[11] else (0, 1e-4)
    kr = kr + (True, False)[len(kr) - 2:]       # (tries, sigma, alm, only_new); old 2-tuples = --kick-retry semantics
    with tempfile.TemporaryDirectory() as tmp:
        return _screen_polish(s, prop, kind, desc, rng, k, known_sides, same, smax, pol_above, pextra, tmp,
                              mate if kind == 'cross2' and cands else None, kr)


HARDEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'target', 'release', 'harden')
HARDEN_R0 = (0.05, 0.1, 0.2)
HARDEN_NOISE = (0.002, 0.004)


def mv_harden(s, sq, rng):
    """Re-harden the whole packing (box held at s, then release + settle; legalised output).  Off unless weighted
    (--weights harden=W).  Falls back to a kick if the engine fails."""
    import subprocess
    r0, nz = rng.choice(HARDEN_R0), rng.choice(HARDEN_NOISE)
    with tempfile.TemporaryDirectory() as tmp:
        pi, po = os.path.join(tmp, 'i.txt'), os.path.join(tmp, 'o.txt')
        mcmin.write_deg(pi, s, sq)
        q = subprocess.run([HARDEN, 'reharden', '--in', pi, '--out', po, '--seed', str(rng.randrange(1 << 30)),
                            '--r0', str(r0), '--noise', str(nz)], capture_output=True, text=True, timeout=600)
        if q.returncode != 0 or not os.path.exists(po):
            prop, desc = MOVES['kick'](s, sq, rng, A)
            return s, prop, 'harden failed ' + desc
        s2, sq2 = mcmin.load_deg(po)
    return s2, sq2, f'harden r0 {r0} noise {nz} s{s2:.5f}'


def kick_retry(s, sq, rng, tmp, k, tries, sigma=1e-4, pextra=(), alm=True):
    """fq's polish can stall at points that are not jammed (10-10: ~90 % of lineage-run sub-11 outputs; a corner-corner
    MILP finds a descent).  A tiny kick + full re-quench breaks the stall (10-08: every such state near the 110 record went
    to a known minimum).  Up to `tries` kicked re-quenches from the current best; a strictly lower (by SAME_SIDE),
    line-free result replaces it.  Returns (s, sq, info)."""
    from layout import full_lines
    info = dict(tries=0, drops=0, drop=0.0)
    s0 = s
    for _ in range(tries):
        # sigma goes through '%g' (6 significant digits), as the flag string always did; no-alm: kick, uniform repair,
        # SLP polish only; pextra (fq flags) on top
        opt = QOpt(loosen=1.0, kick=float(f'{sigma:g}'), seed=rng.randrange(1 << 30), no_alm=not alm).with_args(pextra)
        r = hop.quench(s, sq, tmp, opt=opt)
        info['tries'] += 1
        info.setdefault('raw', []).append(r[0] if r else None)
        if r is None or r[0] >= s - ID.SAME_SIDE:
            info.setdefault('traj', []).append(s)
            continue
        p = os.path.join(tmp, 'kr.txt'); mcmin.write_deg(p, r[0], r[1])
        if full_lines(p, k):
            continue
        s, sq = r[0], r[1]
        info['drops'] += 1
        info.setdefault('traj', []).append(s)
    info['drop'] = s0 - s
    return s, sq, info


def _screen_polish(s, prop, kind, desc, rng, k, known_sides, same, smax, pol_above, pextra, tmp, mate, kr=(0, 1e-4, True, False)):
    """Screen, classify, (maybe) full polish, grid check, in the scratch dir `tmp` (removed by the caller)."""
    from layout import full_lines
    loosen = rng.choice(('1.0', '1.02', '1.05'))
    t0 = time.time()
    r = hop.quench(s, prop, tmp, opt=SCREEN.but(loosen=float(loosen)))
    out = dict(kind=kind, desc=desc, loosen=loosen)
    if mate is not None:
        out['mate'] = mate                   # archive path of the mate (lineage analysis: own lineage or borrowed?)
    if r is None:
        return dict(out, status='fail', sec=time.time() - t0)
    s1, sq1, _ = r
    if s1 > smax + 1e-3:                     # clearly above the stepping-stone ceiling: no polish
        return dict(out, status='screen-discard', s_screen=s1, sec=time.time() - t0)
    p1 = os.path.join(tmp, 's1.txt'); mcmin.write_deg(p1, s1, sq1)
    if full_lines(p1, k):                    # grid-obstructed already after the screen
        return dict(out, status='screen-grid', s_screen=s1, sec=time.time() - t0)
    near = [x for x in known_sides if abs(x - s1) < same]
    if near:
        return dict(out, status='return', s=min(near, key=lambda x: abs(x - s1)), s_screen=s1, sec=time.time() - t0)
    if s1 > pol_above:                       # far from the best: keep the screened state, no full polish
        return dict(out, status='new?', s=s1, sq=sq1, lines=False, s_screen=s1, unpolished=True, sec=time.time() - t0)
    r2 = hop.quench(s1, sq1, tmp, opt=POLISH.with_args(pextra))
    if r2 is None:
        return dict(out, status='fail', sec=time.time() - t0)
    s2, sq2, d2 = r2
    if d2.get('fp'):
        out['fp'] = d2['fp']                 # fq's load-bearing contact fingerprint (10-14: kept, a second identity key)
    p = os.path.join(tmp, 'q.txt'); mcmin.write_deg(p, s2, sq2)
    lines = bool(full_lines(p, k))
    tries, sigma, alm, only_new = kr
    if tries > 0 and not lines and s2 < smax and not (only_new and (s2 >= k or any(abs(x - s2) < ID.SAME_SIDE for x in known_sides))):
        # --kick-retry (alm, every result below smax) / --finish (kick + polish only, archive-new sub-k results only)
        s_pol = s2
        s2, sq2, info = kick_retry(s2, sq2, rng, tmp, k, tries, sigma, pextra, alm=alm)
        out.update(kr_drop=info['drop'], kr_drops=info['drops'], s_polish=s_pol)
        out.pop('fp', None)                  # the fingerprint was of the pre-retry state
    return dict(out, status='new?', s=s2, sq=sq2, lines=lines, s_screen=s1, sec=time.time() - t0)


class Archive:
    def __init__(self, out, n, k, smax, known):
        self.out, self.n, self.k, self.smax, self.known = out, n, k, smax, known
        self.E = []                          # entries
        self.fp = None                       # sparse-parent rule (--sparse-share): fingerprint images, aligned with E
        self.log = open(f'{out}/archive.jsonl', 'a')
        self.plog = open(f'{out}/proposals.jsonl', 'a')

    def find(self, s, tol=ID.SAME_SIDE):
        for e in self.E:
            if abs(e['s'] - s) < tol:
                return e
        return None

    def add(self, s, sq, parent, kind, t, mate=None, fp=None, unpolished=False):
        e = self.find(s, UNP_TOL if unpolished else ID.SAME_SIDE)
        if e:
            e['visits'] += 1
            return e, False
        i = len(self.E)
        path = f'{self.out}/b{i:05d}.txt'
        mcmin.write_deg(path, s, sq)
        root = i if parent < 0 else self.E[parent].get('root', parent)
        e = dict(i=i, s=s, path=path, desc=descriptor(s, sq, self.k), roles=roles(sq), parent=parent, kind=kind, root=root,
                 visits=1, expanded=0, children=0, t=round(t, 1),
                 known=any(abs(s - x) < ID.SAME_SIDE for x in self.known))
        if mate:
            e['mate'] = mate                 # crossover mate's archive path (own lineage or borrowed: compare roots)
        if fp:
            e['cfp'] = fp                    # fq contact fingerprint (self.fp is the sparse rule's image list)
        if unpolished:
            e['unpolished'] = True           # --polish-gate: screened side only (store import: status 'screened')
        if self.fp is not None:
            self.fp_add(e, s, sq)
        self.E.append(e)
        self.log.write(json.dumps({k: v for k, v in e.items()}) + '\n'); self.log.flush()
        return e, True

    def fp_init(self, bank_path):
        """Sparse-parent rule: nnd = fingerprint distance (pk/fingerprint.py) to the nearest other known configuration
        (bank = e.g. the holdout's visible minima, plus this archive)."""
        import numpy as np
        self.fp = []
        self.bank = np.load(bank_path)['images'] if bank_path else np.zeros((0, 2, FP.G, FP.G))
        for e in self.E:                     # resume: rebuild from the archive files
            s, sq = mcmin.load_deg(e['path']); self.fp_add(e, s, sq, own=True)

    def fp_add(self, e, s, sq, own=False):
        import numpy as np
        im = FP.image(s, sq)
        d = [FP.nearest(im, self.bank, self.n).min()] if len(self.bank) else []
        if self.fp:
            da = FP.nearest(im, np.stack(self.fp), self.n)
            d.append(da.min())
            if not own:
                for j, x in enumerate(da):
                    self.E[j]['nnd'] = min(self.E[j].get('nnd', math.inf), float(x))
        e['nnd'] = float(min(d)) if d else math.inf
        self.fp.append(im)

    def pick_sparse(self, rng, k):
        """Evan's distance rule (10-11): sub-k entries far from every other known configuration, minima or not.
        Weight (nnd / median nnd)^2 / (1 + expanded)."""
        sub = [e for e in self.E if e['s'] < k and math.isfinite(e.get('nnd', math.inf))]
        if not sub:
            return None
        med = sorted(e['nnd'] for e in sub)[len(sub) // 2] or 1e-9
        return rng.choices(sub, weights=[1e-6 + (e['nnd'] / med) ** 2 / (1 + e['expanded']) for e in sub])[0]

    def dump(self, stats, t):
        tmp = f'{self.out}/state.json.tmp'
        json.dump(dict(t=t, stats=dict(stats), E=self.E), open(tmp, 'w'))
        os.replace(tmp, f'{self.out}/state.json')

    def load(self, path):
        if not os.path.exists(path):         # runs from before state dumps: rebuild from the archive log
            E = [json.loads(l) for l in open(f'{self.out}/archive.jsonl')]
            self.E = E
            return max([e['t'] for e in E] + [0.0]), collections.Counter()
        d = json.load(open(path))
        self.E = d['E']
        return d.get('t', 0.0), collections.Counter(d.get('stats', {}))

    def pick(self, rng, topk=8, cb=None, roots=None):
        cells = collections.defaultdict(list)
        pool = self.E
        if roots:                            # exploration budget: one frontier lineage, uniform over roots
            live = [r for r in roots if any(e.get('root') == r and e['s'] < self.smax for e in self.E)]
            if live:
                r = rng.choice(live)
                pool = [e for e in self.E if e.get('root') == r]
                cb = None
        for e in pool:
            if e['s'] < self.smax:
                cells[tuple(e['desc'])].append(e)
        cell = cb.choose(list(cells), rng) if cb else rng.choice(list(cells))
        es = sorted(cells[cell], key=lambda e: e['s'])[:topk]
        return rng.choices(es, weights=[1.0 / (1 + e['expanded']) ** 2 for e in es])[0]


def report(out):
    E = [json.loads(l) for l in open(f'{out}/archive.jsonl')]
    with open(os.path.join(out, os.path.basename(E[0]['path']))) as f:    # n from the first archive entry (was 110 hard-coded)
        n = int(f.readline().split()[0])
    k = math.ceil(math.sqrt(n))
    sub = [e for e in E if e['s'] < k]
    new = [e for e in sub if not e['known']]
    print(f'{out}: n = {n}, {len(E)} basins, {len(sub)} below {k} ({len(new)} not in the --known / --novel-ref set); '
          f'best {min(e["s"] for e in E):.10f}')
    by = collections.Counter(tuple(e['roles']) for e in sub)
    print('  sub-k role groups (L, B, axis, other):', dict(by.most_common()))
    print('  sub-k descriptor cells:', dict(collections.Counter(tuple(e['desc']) for e in sub).most_common()))
    print('  new sub-k basins by kind:', dict(collections.Counter(e['kind'] for e in new)))
    for e in sorted(new, key=lambda e: e['s'])[:12]:
        print(f'    {e["s"]:.10f} roles {tuple(e["roles"])} desc {tuple(e["desc"])} from b{e["parent"]} by {e["kind"]} at {e["t"]}s')


def replay(out, line):
    """Re-run proposal `line` (0-based) of <out>/proposals.jsonl through work() from the archive parent + logged seed / mate
    and compare with the log (10-11 provenance check; needs a run with manifest.json and seeded proposal records)."""
    man = json.load(open(f'{out}/manifest.json'))['args']
    P = [json.loads(l) for l in open(f'{out}/proposals.jsonl')]
    E = {e['i']: e for e in (json.loads(l) for l in open(f'{out}/archive.jsonl'))}
    p = P[line]
    if 'seed' not in p:
        raise SystemExit('proposal record has no seed (run predates 10-11 provenance)')
    if man.get('polish_margin') or man.get('polish_gate'):
        print('warning: --polish-margin / --polish-gate run: pol_above depended on the run best at the time (not logged); '
              'replayed with polish everything')
    par = E[p['par']]
    s, sq = mcmin.load_deg(os.path.join(out, os.path.basename(par['path'])))
    n = len(sq); k = math.ceil(math.sqrt(n) - 1e-12)
    smax = man.get('smax') or k + 0.05
    mate = [os.path.join(out, os.path.basename(p['mate']))] if p.get('mate') else []
    import scratch
    scratch.scope('replay')
    r = work((s, sq, p['kind'], p['seed'], k, [], man.get('same', 0.0), smax, float('inf'),
              (man.get('polish_extra') or '').split(), mate,
              (man['finish'], man.get('kick_sigma') or 1e-4, False, True) if man.get('finish') else
              (man.get('kick_retry') or 0, man.get('kick_sigma') or 1e-4, True, False)))
    same = (r.get('s') == p.get('s')) or (r.get('s') is not None and p.get('s') is not None and abs(r['s'] - p['s']) < 1e-12)
    print(json.dumps(dict(logged=dict(st=p['st'], s=p.get('s'), desc=p.get('desc')),
                          replay=dict(st=r['status'], s=r.get('s'), desc=r.get('desc')), reproduced=same and r['status'] == p['st'])))
    return same


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=110); ap.add_argument('--starts', nargs='+')
    ap.add_argument('--minutes', type=float, default=60); ap.add_argument('--procs', type=int, default=15)
    ap.add_argument('--smax', type=float, default=None, help='stepping-stone ceiling (default k + 0.05)')
    ap.add_argument('--same', type=float, default=0.0, help='screened side within this of a known basin = return, no polish '
                    '(10-09 bench c110a: 1e-6 lost half the new certified basins; default 0 = polish everything)')
    ap.add_argument('--star', action='store_true', help='control: always expand the first start (cen7-style sampling)')
    ap.add_argument('--adapt-cells', action='store_true', help='Thompson sampling over descriptor cells for parents')
    ap.add_argument('--frontier', help='start-path prefix marking frontier lineages (e.g. seeds110c/)')
    ap.add_argument('--frontier-share', type=float, default=0.5, help='share of parent picks from frontier lineages')
    ap.add_argument('--elite-share', type=float, default=0.0, help='share of parent picks from the global top-K basins (exploit)')
    ap.add_argument('--elite-k', type=int, default=20)
    ap.add_argument('--polish-margin', type=float, default=0.0, help='full polish only if screened side < best + margin (0 = always)')
    ap.add_argument('--polish-gate', type=float, default=0.0, help='TT3 (10-15): full polish only if the screened side < '
                    'min(--frontier-s, run best) + G; the rest are kept as unpolished stepping stones (never elite parents, never '
                    'the run best, identity / novelty at UNP_TOL).  0 = off (polish everything)')
    ap.add_argument('--novel-ref', help='json list of sides: bandit rewards only basins not within 2e-9 of these (global novelty)')
    ap.add_argument('--polish-extra', default='', help='extra fq args for the stage-2 polish (e.g. "--stag-tol 1e-7": search precision)')
    ap.add_argument('--final-polish', type=int, default=0, help='at the end, full default polish of the K best archive entries')
    ap.add_argument('--bandit-state', help='json file: load (x --bandit-carry) and save the move-kind bandit statistics')
    ap.add_argument('--bandit-half', type=float, default=600.0,
                    help='bandit count half-life, s (inf = no decay; analysis/bandit_timescale.md: no drift at round scale)')
    ap.add_argument('--bandit-carry', type=float, default=0.5, help='factor on carried bandit statistics (1 + half inf = pooled, merged on save)')
    ap.add_argument('--melt', type=float, default=0, help='weight of the regional melt move (anneal melt); 0 = off')
    ap.add_argument('--bigmelt', type=float, default=0, help='weight of the big regional melt (R 3.5-7, rmax 0.1-0.25); 0 = off')
    ap.add_argument('--gate-ref', default='front', choices=['front', 'run'],
                    help='polish gate line: front = min(frontier_s, run best) (TT3-tested); run = the run best (searches from far seeds)')
    ap.add_argument('--pm-share', type=float, default=0, help='share of parent picks by the parent value model (pm_pick); 0 = off')
    ap.add_argument('--focus', type=int, default=0,
                    help='FB1 (10-16): each new run best (and the best start) gets its next FOCUS expansions as the parent '
                         '(new-best hits per CPU-h fall ~2x per expansion; below the ranks 2-20 rate after ~10); 0 = off')
    ap.add_argument('--focus-share', type=float, default=1.0, help='share of picks that go to the focus while it has budget')
    ap.add_argument('--pm-beta', type=float, default=1.0, help='parent value model sharpness: weight = rate ** beta')
    ap.add_argument('--gls', type=float, default=0, help='weight of the GLS feasibility move (anneal gls); 0 = off')
    ap.add_argument('--cross', type=float, default=0, help='weight of the recombination move (cross.py bestfit 3 of 5); 0 = off')
    ap.add_argument('--cross2', type=float, default=2, help='weight of two-parent crossover (random sub-k mate; nearest '
                    'mate for above-k parents; battery 10-09 best reach move); 0 = off')
    ap.add_argument('--ashallow', type=float, default=2, help='weight of the shallow whole-box anneal (battery 10-09); 0 = off')
    ap.add_argument('--weights', help='move weight overrides, e.g. "mirror=0,kicksym=3" (0 removes a kind; ablations)')
    ap.add_argument('--adapt', action='store_true', help='Thompson sampling over move kinds (reward: new below-k basin)')
    ap.add_argument('--reward', default='legacy', choices=['legacy', 'value'],
                    help='bandit reward: legacy (1 for a new sub-k basin) or value (gap-graded x parent robustness)')
    ap.add_argument('--reward-g0', type=float, default=1e-3); ap.add_argument('--reward-alpha', type=float, default=1.0)
    ap.add_argument('--frontier-s', type=float, default=None, help='best known side (default: best start)')
    ap.add_argument('--resume', action='store_true', help='continue from <out>/state.json (time offset carried over)')
    ap.add_argument('--out'); ap.add_argument('--report'); ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--kick-retry', type=int, default=0, help='after the full polish, up to N kicked re-quenches (sigma '
                    '--kick-sigma); a strictly lower line-free result replaces the polished one (breaks fq polish stalls; 0 = off)')
    ap.add_argument('--kick-sigma', type=float, default=1e-4)
    ap.add_argument('--finish', type=int, default=0, help='inline finisher: up to N kick (--kick-sigma) + polish-only tries on '
                    'archive-new sub-k results (kr_eval_noalm 10-11: 1/60 certified minima moved); 0 = off')
    ap.add_argument('--sparse-share', type=float, default=0.0, help='share of parent picks by the distance rule: sub-k '
                    'entries weighted by (fingerprint distance to the nearest known configuration)^2 (Archive.pick_sparse); 0 = off')
    ap.add_argument('--fp-bank', help='npz of fingerprint images of known configurations (fingerprint.py bank), for --sparse-share')
    ap.add_argument('--replay', help='OUT:LINE: re-run proposal LINE of OUT/proposals.jsonl and compare with the log')
    a = ap.parse_args()
    if a.report:
        report(a.report); raise SystemExit
    if a.replay:
        out_, line_ = a.replay.rsplit(':', 1)
        raise SystemExit(0 if replay(out_, int(line_)) else 1)
    import scratch
    scratch.scope('explore')                 # all temp dirs of this run (workers, fq / anneal files) under one dir, removed at exit
    from pk import manifest
    man = manifest.start(a.out, 'explore', seed=a.seed, args=vars(a), procs=a.procs)
    k = math.ceil(math.sqrt(a.n) - 1e-12)
    known = json.load(open(f'{HERE}/runs/known{a.n}.json')) if os.path.exists(f'{HERE}/runs/known{a.n}.json') else []
    ar = Archive(a.out, a.n, k, a.smax or k + 0.05, known)
    rng = random.Random(a.seed)
    tmp = tempfile.mkdtemp()
    t0 = time.time()
    stats = collections.Counter()
    if a.sparse_share and not a.resume:
        ar.fp_init(a.fp_bank)
    if a.resume:
        toff, stats = ar.load(f'{a.out}/state.json')
        if a.sparse_share:
            ar.fp_init(a.fp_bank)
        t0 -= toff
        a.starts = []
        print(f'resumed {len(ar.E)} basins at t = {toff:.0f}s', flush=True)
    for p in a.starts:                       # starts are polished in place (no ALM, no loosen: keep their basins)
        s, sq = mcmin.load_deg(p)
        r = hop.quench(s, sq, tmp, opt=POLISH)
        if r:
            e, _ = ar.add(r[0], r[1], -1, 'start:' + os.path.basename(p), 0, fp=r[2].get('fp'))
            e['src'] = p
            print('start', p, f'{r[0]:.10f}', e['desc'], e['roles'], flush=True)
    if a.cross:
        WEIGHTS['cross'] = a.cross
    if a.melt:
        WEIGHTS['melt'] = a.melt
    if a.bigmelt:
        WEIGHTS['bigmelt'] = a.bigmelt
    if a.gls:
        WEIGHTS['gls'] = a.gls
    WEIGHTS['cross2'] = a.cross2
    WEIGHTS['ashallow'] = a.ashallow
    for kv in (a.weights.split(',') if a.weights else []):    # ablations (bench110): kind=weight, 0 drops a kind
        k_, v_ = kv.split('=')
        WEIGHTS[k_.strip()] = float(v_)
    for k_ in [k_ for k_, v_ in WEIGHTS.items() if v_ == 0]:
        del WEIGHTS[k_]
    kinds, wts = zip(*WEIGHTS.items())
    bandit = KindBandit([kk for kk, w in WEIGHTS.items() if w > 0], half=a.bandit_half) if a.adapt else None
    b_init = {}
    if bandit and a.bandit_state and os.path.exists(a.bandit_state):   # carried move statistics (chain rounds)
        bs = json.load(open(a.bandit_state))
        for kk in bandit.kinds:
            bandit.r[kk] = a.bandit_carry * bs.get('r', {}).get(kk, 0.0); bandit.c[kk] = a.bandit_carry * bs.get('c', {}).get(kk, 0.0)
        b_init = {kk: (bandit.r[kk], bandit.c[kk]) for kk in bandit.kinds}
    cellb = CellBandit() if a.adapt_cells else None
    import bisect
    nref = sorted(json.load(open(a.novel_ref))) if a.novel_ref else []
    def novel(s, tol=ID.SAME_SIDE):
        i = bisect.bisect_left(nref, s - tol)
        return not (i < len(nref) and abs(nref[i] - s) < tol)
    pend = {}
    ar_best = [min(e['s'] for e in ar.E)] if getattr(ar, 'E', None) else [math.inf]
    frontier_s = a.frontier_s if a.frontier_s is not None else ar_best[0]
    pol0 = [e for e in getattr(ar, 'E', []) if not e.get('unpolished')]
    focus = [min(pol0, key=lambda e: e['s']) if (a.focus and pol0) else None, a.focus]   # [entry, budget left]
    t_start = time.time()
    def mates(kind, par):
        if kind == 'cross':
            xp = [e['path'] for e in ar.E if e['s'] < ar.smax and e['i'] != par['i']]
            return rng.sample(xp, min(CROSS_CANDS, len(xp)))
        if kind == 'cross2':                 # sub-k mates when there are any (battery mates were sub-k suite members)
            xp = [e['path'] for e in ar.E if e['s'] < k and e['i'] != par['i']] or \
                 [e['path'] for e in ar.E if e['s'] < ar.smax and e['i'] != par['i']]
            return rng.sample(xp, min(CROSS2_NEAR, len(xp)))
        return []
    def pol_above():
        if a.polish_gate:                    # gate-ref run (10-15): far seeds; polish near the run's own best
            return (ar_best[0] if a.gate_ref == 'run' else min(frontier_s, ar_best[0])) + a.polish_gate
        return (min(e['s'] for e in ar.E) + a.polish_margin) if a.polish_margin else float('inf')
    with ProcessPoolExecutor(a.procs) as ex:
        def submit():
            fr = None; pick = None
            if focus[0] is not None and focus[1] > 0 and rng.random() < a.focus_share:   # FB1: fresh run best
                par = focus[0]; focus[1] -= 1
                pick = ('focus', float(focus[1]))
            elif a.pm_share and rng.random() < a.pm_share:     # parent value model (TT3 round 3)
                par, pp = pm_pick(ar.E, frontier_s, ar.smax, a.pm_beta, rng)
                pick = ('pm', pp)
            elif a.frontier and rng.random() < a.frontier_share:
                fr = [e['i'] for e in ar.E if e['parent'] < 0 and e['kind'].startswith('start:') and e.get('src', '').startswith(a.frontier)]
            if pick:
                pass
            elif not fr and a.elite_share and rng.random() < a.elite_share:
                el = sorted((e for e in ar.E if e['s'] < k and not e.get('unpolished')), key=lambda e: e['s'])[:a.elite_k]
                par = rng.choices(el, weights=[1.0 / (1 + e['expanded']) for e in el])[0] if el else ar.pick(rng, cb=cellb)
            elif a.sparse_share and rng.random() < a.sparse_share and (par := ar.pick_sparse(rng, k)) is not None:
                pass
            else:
                par = ar.E[0] if a.star else ar.pick(rng, cb=cellb, roots=fr)
            par['expanded'] += 1
            s, sq = mcmin.load_deg(par['path'])
            kind = bandit.choose(rng) if bandit else rng.choices(kinds, weights=wts)[0]
            sd = rng.randrange(1 << 30)
            f = ex.submit(work, (s, sq, kind, sd, k, [e['s'] for e in ar.E], a.same, ar.smax,
                                       pol_above(), a.polish_extra.split(),
                                       mates(kind, par), (a.finish, a.kick_sigma, False, True) if a.finish else (a.kick_retry, a.kick_sigma, True, False)))
            pend[f] = (par, sd, pick)
        for _ in range(a.procs):
            submit()
        last = 0
        while pend:
            done, _ = wait(pend, return_when=FIRST_COMPLETED)
            for f in done:
                par, sd, pick = pend.pop(f)
                try:
                    r = f.result()
                except Exception as exn:
                    stats['error'] += 1; r = None
                if r:
                    stats[r['status']] += 1
                    newi = hit = None
                    if r['status'] == 'return':
                        e = ar.find(r['s'])
                        if e: e['visits'] += 1; hit = e['i']
                    elif r['status'] == 'new?':
                        if r['lines'] or r['s'] >= ar.smax:
                            stats['discard'] += 1
                        else:
                            e, isnew = ar.add(r['s'], r['sq'], par['i'], r['kind'], time.time() - t0, mate=r.get('mate'), fp=r.get('fp'),
                                              unpolished=bool(r.get('unpolished')))
                            stats['new' if isnew else 'dup'] += 1
                            hit = e['i']
                            if isnew:
                                par['children'] += 1
                                newi = e['i']
                    # bandit reward for a new (globally novel) basin.  legacy: 1 below k, else 0.  value: graded by the
                    # gap to the frontier, w = min(1, (g0 / gap)^alpha) (10-09 lineage calibration: subtree success
                    # falls ~1 decade per decade of gap, g0 ~ 1e-3), times the parent's robustness (posterior mean of
                    # its children's non-grid rate; above-grid states that keep collapsing earn little).  No special
                    # case for above k: it is just a larger gap.
                    rew = 0.0
                    if r['status'] != 'fail':
                        par['nkids'] = par.get('nkids', 0) + 1
                        par['ngrid'] = par.get('ngrid', 0) + (r['status'] == 'screen-grid' or bool(r.get('lines')))
                    if newi is not None and novel(r['s'], UNP_TOL if r.get('unpolished') else ID.SAME_SIDE):
                        if a.reward == 'legacy':
                            rew = 1.0 if r['s'] < k else 0.0
                        else:
                            front = min(frontier_s, ar_best[0])
                            gap = max(r['s'] - front, 1e-12)
                            robust = (1 + par.get('nkids', 0) - par.get('ngrid', 0)) / (2 + par.get('nkids', 0))
                            rew = min(1.0, (a.reward_g0 / gap) ** a.reward_alpha) * robust
                    if r.get('s') is not None and r['status'] == 'new?' and not r.get('lines') and not r.get('unpolished'):
                        if a.focus and newi is not None and r['s'] < ar_best[0] - 1e-9:
                            focus[0] = next(x for x in ar.E if x['i'] == newi); focus[1] = a.focus
                        ar_best[0] = min(ar_best[0], r['s'])
                    if cellb:
                        cellb.update(tuple(par['desc']), r.get('sec', 0.0), rew)
                    if bandit:
                        bandit.update(r['kind'], r.get('sec', 0.0), rew)
                    # proposal log (10-11: + seed / desc / loosen / s_screen / hit / cpu): par + seed + mate replay the
                    # proposal through work(); hit = archive entry it landed on (new, dup or return); new = hit if created
                    ar.plog.write(json.dumps(dict(t=round(time.time() - t0, 1), kind=r['kind'], st=r['status'],
                                                  sec=round(r.get('sec', 0), 2), cpu=r.get('cpu'), s=r.get('s'),
                                                  s_screen=r.get('s_screen'), new=newi, hit=hit, par=par['i'], seed=sd,
                                                  desc=r.get('desc'), loosen=r.get('loosen'),
                                                  **({'unp': True} if r.get('unpolished') else {}),
                                                  **({'pick': pick[0], 'pp': round(pick[1], 8)} if pick else {}),
                                                  **({'kr_drop': r['kr_drop'], 'kr_drops': r['kr_drops']} if 'kr_drop' in r else {}),
                                                  **({'mate': r['mate']} if r.get('mate') else {}))) + '\n')
                if time.time() - t_start < 60 * a.minutes:
                    submit()
            if time.time() - last > 120:
                last = time.time()
                ar.dump(stats, time.time() - t0)
                sub = [e for e in ar.E if e['s'] < k]
                if bandit: print('  bandit', bandit.summary(), flush=True)
                print(f'{time.time() - t0:7.0f}s basins {len(ar.E)} sub-k {len(sub)} (new vs known {sum(not e["known"] for e in sub)}) '
                      f'best {min(e["s"] for e in ar.E):.10f} cells {len({tuple(e["desc"]) for e in ar.E})} | {dict(stats)}', flush=True)
    if a.final_polish:                        # census step: finish the best entries at full precision
        for e in sorted((e for e in ar.E if e['s'] < ar.smax), key=lambda e: e['s'])[:a.final_polish]:
            s0, sq0 = mcmin.load_deg(e['path'])
            r = hop.quench(s0, sq0, tmp, opt=POLISH)
            if r and r[0] < e['s'] - 1e-12:
                e2, isnew = ar.add(r[0], r[1], e['i'], 'refine', time.time() - t0)
                print(f'refine b{e["i"]} {e["s"]:.12f} -> {r[0]:.12f}', flush=True)
    ar.dump(stats, time.time() - t0)
    if bandit and a.bandit_state:
        bandit.decay()
        if a.bandit_carry == 1.0 and not math.isfinite(a.bandit_half):
            # pooled file shared by concurrent rounds (chain n bands, 10-14): add this run's increments to the file as it
            # is now (lock), so rounds running side by side don't overwrite each other
            import fcntl
            with open(a.bandit_state + '.lock', 'w') as lk:
                fcntl.flock(lk, fcntl.LOCK_EX)
                cur = json.load(open(a.bandit_state)) if os.path.exists(a.bandit_state) else dict(r={}, c={})
                for kk in bandit.kinds:
                    r0, c0 = b_init.get(kk, (0.0, 0.0))
                    cur['r'][kk] = cur['r'].get(kk, 0.0) + bandit.r[kk] - r0
                    cur['c'][kk] = cur['c'].get(kk, 0.0) + bandit.c[kk] - c0
                json.dump(cur, open(a.bandit_state + '.tmp', 'w')); os.replace(a.bandit_state + '.tmp', a.bandit_state)
        else:
            json.dump(dict(r=bandit.r, c=bandit.c), open(a.bandit_state, 'w'))
    report(a.out)
    man.finish(summary=dict(stats=dict(stats), basins=len(ar.E), sub_k=sum(e['s'] < k for e in ar.E),
                            best=min(e['s'] for e in ar.E) if ar.E else None))
