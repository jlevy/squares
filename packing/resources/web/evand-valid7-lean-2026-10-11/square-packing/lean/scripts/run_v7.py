#!/usr/bin/env python3
"""Generate the Lean certificate of Valid7's pose trees (run V3 of qx2_zm), one module per root.

    run_v7.py --lo I --hi J [--nproc N] [--out DIR]

For every root in [I, J): rebuild its tree (tree_rebuild.py), certify every EXACT-type leaf (EXACT,
EXACT0, EXACT45, PIECE, CAP) with gen_exact.Leaf at the leaf's own scale (retrying with the high
McCormick anchor, then without the corner kinds), and write `DIR/R%05d.lean`: the leaves' ExLeaf
data and pair theorems, and the root theorem `root_%05d : CovT ...` at the global scale.  A status
line per root goes to stdout (JSON).  Nothing here is trusted.
"""
import argparse, json, os, pickle, signal, sys, time
from fractions import Fraction as F
from math import lcm
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tree_rebuild import load, build, count  # noqa: E402
from gen_tree import Glue  # noqa: E402
from gen_axis import read_cover  # noqa: E402
import gen_exact as G  # noqa: E402
from gen_credit import credit  # noqa: E402
import capk  # noqa: E402

COVER = os.path.join(HERE, '..', '..', 'certificates', 'k2m3', 'L4_k02_box7.txt')
LEAVES = os.path.join(HERE, '..', '..', 'certificates', 'k2m3', 'qx2_zm', 'runV3_6294052a_leaves.jsonl.gz')
SG, RG, MQ = 128, 1 << 72, 35
SIMPLE = ('EMPTY', 'SYM', 'AXIS', 'LEB')
LIMIT = int(os.environ.get('V7_LIMIT', '1200'))   # seconds per attempt


class Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise Timeout()

_cov = None


def leaves_of(t):
    if t[0] == 'L':
        yield t
    elif t[0] == 'C':
        yield from leaves_of(t[2])
    else:
        yield from leaves_of(t[2])
        yield from leaves_of(t[3])


def scales(b):
    dx = lcm(*[x.denominator for x in b[:4]])
    Sl = 1
    while (5 * Sl) % dx:
        Sl *= 2
    du = lcm(*[x.denominator for x in b[4:]])
    return Sl, max(1 << 16, du << 10) << RSHIFT


CG, CH = 2048, F(1, 256)     # the credit's denominator and strip height (a multiple of 1/CG)


def set_credit(lf, b, ib, Rl):
    """`lf.cred` for the Lebesgue rectangle of the cover, and the reduced vertex target"""
    e = _cov[5][0]
    D = _cov[1]
    rect = tuple(F(e[i], D) for i in range(4))
    strips, area = credit(tuple(b[:4]), ib[4], ib[5], Rl, rect, h=CH)
    hh = int(CH * CG)
    st = [(int(xa * CG), int(xb * CG), int(yb * CG)) for xa, xb, yb in strips]
    assert all(F(t[0], CG) == xa and F(t[1], CG) == xb and F(t[2], CG) == yb for t, (xa, xb, yb) in zip(st, strips))
    amt = e[4] * sum((t[1] - t[0]) * hh for t in st) // (CG * CG)
    lf.cred = (tuple(e), CG, hh, amt, st)
    lf.W = lf.W0 - amt


RSHIFT = int(os.environ.get('V7_RSHIFT', '0'))       # finer angle grid (2^RSHIFT) for deep bisection
SPLIT_DEPTH = int(os.environ.get('V7_SPLIT', '3'))   # levels of splitting a failing leaf
LIMIT0 = int(os.environ.get('V7_LIMIT0', '1800'))    # seconds per attempt before splitting


def split_box(b, D):
    """halve the box along its largest side (u counted twice), at a point the glue can name
    (centres on the grid 1/(D SG)); None if no side can be halved"""
    dx, dy, du = b[1] - b[0], b[3] - b[2], 2 * (b[5] - b[4])
    for ax, i in sorted((('X', 0), ('Y', 2), ('U', 4)), key=lambda a: -(dx, dy, du)[a[1] // 2]):
        mid = (b[i] + b[i + 1]) / 2
        if ax != 'U' and (mid * D * SG).denominator != 1:
            continue
        if ax == 'U' and (mid * RG).denominator != 1:
            continue
        bl = list(b); bl[i + 1] = mid
        bh = list(b); bh[i] = mid
        return ax, mid, tuple(bl), tuple(bh)
    return None


def certify(b, limit=None):
    Sl, Rl = scales(b)
    ib = [int(x * 5 * Sl) for x in b[:4]] + [int(x * Rl) for x in b[4:]]
    # Lemma K first (a few exact tests; covers the caps of the Lebesgue rectangle at zero margin)
    _, D, W, _, segs, rects = _cov
    k = capk.certify(D, Sl, Rl, W, *ib, segs, [tuple(r) for r in rects])
    if k is not None:
        return ('capk', k, ib), 'capk', Sl, Rl
    # the last flag keeps the Lebesgue rectangles; without them the bound is weaker but never negative
    # (the rectangle term `1 - U_x - U_y` goes below 0 where the square barely meets the rectangle)
    # 'credit': no rectangle terms, the rectangle's mass bounded by strips inside every square
    # the credit first: when it applies it is usually the fastest
    tries = [('hi', True, True, 'credit'), ('hi', True, True, True), ('hi', True, True, False),
             ('lo', True, True, True), ('hi', False, True, True), ('hi', False, False, True)]
    log = []
    timed_out = False
    for anchor, corner, tan, rect in tries:
        if timed_out and rect is True:
            # the other modes only help where a check fails; a slow leaf needs a longer limit (V7_LIMIT)
            continue
        G.Leaf.ANCHOR, G.Leaf.USE_CORNER, G.Leaf.USE_TAN = anchor, corner, tan
        lf = G.Leaf(_cov, Sl, Rl, *ib)
        if not lf.ok:
            return None, 'wall', Sl, Rl
        if rect is not True:
            if not lf.crs:
                continue
            if rect == 'credit':
                set_credit(lf, b, ib, Rl)
            lf.crs = []
        signal.signal(signal.SIGALRM, _alarm)
        signal.alarm(limit or LIMIT)
        try:
            c = lf.run()
        except Timeout:
            c = None
            lf.stat['timeout'] = limit or LIMIT
        finally:
            signal.alarm(0)
        tag = f'{anchor}/{int(corner)}{int(tan)}' + {True: '', False: '/norect', 'credit': '/credit'}[rect]
        log.append(f"{tag}:{'timeout' if 'timeout' in lf.stat else 'fail' + str(lf.stat['fail'])}")
        timed_out = timed_out or 'timeout' in lf.stat
        if c:
            return lf, tag, Sl, Rl
    return None, ('timeout ' if timed_out else 'fail ') + ' '.join(log), Sl, Rl


def work(args):
    idx, root, leaves, outdir = args
    global _cov
    if _cov is None:
        _cov = sorted_cover()
    _, D, W, pts, segs, rects = _cov
    t0 = time.time()
    tree = build(root, leaves, F(7))
    g = Glue(D, SG, RG, W, MQ)
    body, fails, how = [], [], []
    cert = {}
    counter = [0]

    def cert_leaf(b, k, depth):
        """the leaf `b` certified, or split in two (up to SPLIT_DEPTH levels) where it fails or is slow"""
        n = counter[0]; counter[0] += 1
        lf, why, Sl, Rl = certify(b, LIMIT0 if depth < SPLIT_DEPTH else None)
        how.append(why)
        if lf is None:
            sp = split_box(b, D) if depth < SPLIT_DEPTH else None
            if sp is None:
                fails.append([n, k, [str(x) for x in b], why])
                return ('L', b, k)
            ax, mid, bl, bh = sp
            return (ax, mid, cert_leaf(bl, k, depth + 1), cert_leaf(bh, k, depth + 1))
        name = f"r{idx:05d}l{n}"
        if isinstance(lf, tuple) and lf[0] == 'capk':
            g.leaf_names[b] = (f"{name}_ok", Sl, Rl, 'cap')
            cert[b] = dict(name=name, S=Sl, R=Rl, capk=lf[1], box=tuple(lf[2]))
            return ('L', b, k)
        g.leaf_names[b] = (f"{name}_ok", Sl, Rl)
        cert[b] = dict(name=name, S=Sl, R=Rl, D=lf.D, W=lf.W, W0=lf.W0, cred=lf.cred, Q=lf.Q, box=lf.box,
                       wx=lf.wx, wy=lf.wy, ex=lf.ex, ey=lf.ey, chs=lf.chs, cvs=lf.cvs, crs=lf.crs, Ls=lf.Ls,
                       side=lf.side, hbx=lf.hbx, vbx=lf.vbx, certs=lf.certs)
        return ('L', b, k)

    def walk(t):
        if t[0] == 'L':
            _, b, k = t
            if b[4] == b[5] or (k == 'LEB' and g.lebOk(b, rects[0])) or (k in SIMPLE and k != 'LEB'):
                return t
            return cert_leaf(b, k, 0)
        if t[0] == 'C':
            return ('C', t[1], walk(t[2]))
        return (t[0], t[1], walk(t[2]), walk(t[3]))

    tree = walk(tree)
    status = dict(root=idx, kinds=count(tree), fails=fails, how=how, sec=round(time.time() - t0, 1))
    if not fails:
        path = os.path.join(outdir, f"R{idx:05d}.pkl")
        with open(path + ".tmp", 'wb') as f:
            pickle.dump(dict(idx=idx, root=root, tree=tree, leaves=cert), f)
        os.replace(path + ".tmp", path)
    return status


def sorted_cover():
    """The cover with its segments normalised (`segNorm`) and sorted by key (`STree.chainB`)."""
    side, D, W, pts, segs, rects = read_cover(COVER)
    segs = sorted(segs, key=lambda e: e[:4])
    return side, D, W, pts, segs, rects


def stree(segs):
    if not segs:
        return "STree.leaf"
    m = len(segs) // 2
    return f"(STree.node {stree(segs[:m])} {G.ltup(segs[m])} {stree(segs[m + 1:])})"


def data_module(outdir):
    _, D, W, pts, segs, rects = sorted_cover()
    txt = "\n".join([
        "import Sqpack.ExTree",
        "/-! The cover `L4_k02_box7.txt`: segments normalised (`segNorm`) and sorted by key, as a list",
        "(`tsegs`, used by the leaves) and as a search tree (`segsT`); the Lebesgue square (`trects`). -/",
        "namespace SquarePacking.LemmaELeaf", "open ZMTreeM",
        f"def tsegs : List SegE := [{', '.join(G.ltup(e) for e in segs)}]",
        f"def trects : List RectE := [{', '.join(G.ltup(r) for r in rects)}]",
        f"def segsT : STree := {stree(segs)}",
        "set_option maxRecDepth 100000 in",
        "theorem segsT_toList : segsT.toList = tsegs := by decide +kernel",
        "end SquarePacking.LemmaELeaf"]) + "\n"
    with open(os.path.join(outdir, "Data.lean"), 'w') as f:
        f.write(txt)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lo', type=int, default=0)
    ap.add_argument('--hi', type=int, default=10 ** 9)
    ap.add_argument('--nproc', type=int, default=1)
    ap.add_argument('--out', default=os.path.join(HERE, '..', 'v7cert'))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    jobs = [(i, r, l, a.out) for i, (r, l, u) in enumerate(load(LEAVES)) if a.lo <= i < a.hi
            and not os.path.exists(os.path.join(a.out, f"R{i:05d}.pkl"))]
    print(json.dumps(dict(todo=len(jobs))), flush=True)
    with Pool(a.nproc) as p:
        for st in p.imap_unordered(work, jobs):
            print(json.dumps(st), flush=True)


if __name__ == '__main__':
    main()
