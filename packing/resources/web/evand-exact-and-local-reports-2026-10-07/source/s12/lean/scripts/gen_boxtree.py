#!/usr/bin/env python3
"""Build a pose-space box tree for a weighted point certificate and emit it as Lean data for the
generic kernel checker `Sqpack/BoxTree.lean` (the Lean lower-bound ladder; see `lean/LADDER.md`).

Usage (from s12/):
  python3 lean/scripts/gen_boxtree.py CERT --n N --name NAME --outdir lean/Sqpack/NAME
          [--K 12] [--J 20] [--ru 29/70] [--chunk 600] [--parts 4] [--fratio 0.85] [--look 1]
          [--balance leaves|digits]

writes NAME/Pts.lean (the points and their data checks), NAME/Part*.lean (the kernel-checked
chunks, one file per parallel build job) and NAME/Cov.lean (`cov_root`, glued by `Cov.split*`).

The integer semantics here mirror `BoxTree.check` exactly (the Lean kernel is the judge; this
script only has to find a tree the kernel accepts):

* spatial scale        Q = D * S, S = 2^K (point (X, Y) of the certificate is (X*S, Y*S) / Q),
                       container M = Mq * S where Mq/D is the container side;
* angle parameter      u = tan(theta/2) = U / R, R = r_den * 2^J, root U in [0, r_num * 2^J]
                       (the root must reach tan(pi/8) = sqrt2 - 1; 29/70 > sqrt2 - 1);
* root centre box      [0, M - M//2]^2: the D4 fundamental region (the certificate must be
                       D4-invariant; `BoxTree.lean` checks that);
* a node splits one axis at the floor midpoint; a leaf is accepted when u1 <= R and either the
  admissible centre rectangle (the box clipped by a lower bound for w(theta)/2) is empty, or the
  points certified to lie in every admissible square of the box weigh >= W.

Pruning (`F` nodes, `near`) is placed where it shrinks the candidate list to <= fratio of its size;
each leaf carries its selection (gaps into its candidate list) of certified points.  Each chunk
is shipped as one numeral, a digit stream decoded in the kernel by `BoxTree.dec`.

The tree is cut into chunks of <= --chunk leaves; every chunk becomes its own theorem proved
`by decide +kernel` (separate kernel declarations: bounded memory, and Lean checks them in
parallel), and a generated skeleton proof glues the chunk theorems together with the
`Cov.splitX/Y/U` lemmas.
"""
import argparse
import hashlib
import sys
import time
from fractions import Fraction

sys.setrecursionlimit(100000)


def read_cert(path):
    raw = open(path, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    it = iter(raw.decode().split())
    snum, sden = int(next(it)), int(next(it))
    D = int(next(it)); W = int(next(it)); m = int(next(it))
    pts = [(int(next(it)), int(next(it)), int(next(it))) for _ in range(m)]
    assert next(it, None) is None, "trailing data (cliques/branch blocks are not supported)"
    return sha, Fraction(snum, sden), D, W, pts


# ---------------------------------------------------------------------------------------------
# the exact integer checker (mirror of BoxTree.lean, Nat semantics)

def nsub(a, b):
    return a - b if a > b else 0


def triples(R, U0, U1):
    RR = R * R
    return [(2 * nsub(RR, U0 * U0), 4 * R * U0, RR + U0 * U0),
            (2 * nsub(RR, U1 * U1), 4 * R * U1, RR + U1 * U1),
            (2 * nsub(RR, U0 * U1), 2 * R * (U0 + U1), RR + U0 * U1)]


def tri_ok(G, a, b, xl, xh, yl, yh, X, Y):
    aX, bY, bX, aY = a * X, b * Y, b * X, a * Y
    return (aX + bY <= G + a * xl + b * yl and a * xh + b * yh <= G + aX + bY
            and aY + b * xh <= G + bX + a * yl and bX + a * yh <= G + aY + b * xl)


def wlo(Q, R, U0, U1):
    return (Q * nsub(R * R + 2 * U0 * R, U1 * U1)) // (2 * (R * R + U1 * U1))


class Ctx:
    def __init__(self, S, Q, M, R, W, F):
        self.S, self.Q, self.M, self.R, self.W, self.F = S, Q, M, R, W, F


def clip(ctx, box):
    x0, x1, y0, y1, U0, U1 = box
    WL = wlo(ctx.Q, ctx.R, U0, U1)
    return max(x0, WL), min(x1, nsub(ctx.M, WL)), max(y0, WL), min(y1, nsub(ctx.M, WL))


def deficit(ctx, box, cands):
    """W minus the certified weight, as `capOk` computes it (<= 0: the leaf is accepted)."""
    x0, x1, y0, y1, U0, U1 = box
    if U1 > ctx.R:
        return ctx.W + 1
    xl, xh, yl, yh = clip(ctx, box)
    if xh < xl or yh < yl:
        return -1
    tr = [(g * ctx.Q, a, b) for a, b, g in triples(ctx.R, U0, U1)]
    need = ctx.W
    for X, Y, w in cands:
        if need == 0:
            break
        X *= ctx.S; Y *= ctx.S
        if all(tri_ok(G, a, b, xl, xh, yl, yh, X, Y) for G, a, b in tr):
            need = nsub(need, w)
    return need


def near(ctx, box, cands):
    x0, x1, y0, y1 = box[:4]
    S, F = ctx.S, ctx.F
    return [p for p in cands
            if x0 <= p[0] * S + F and p[0] * S <= x1 + F and y0 <= p[1] * S + F and p[1] * S <= y1 + F]


def split(box, axis):
    b = list(box)
    mid = (b[2 * axis] + b[2 * axis + 1]) // 2
    l = b.copy(); r = b.copy()
    l[2 * axis + 1] = mid
    r[2 * axis] = mid
    return tuple(l), tuple(r)


def score(ctx, box, cands, depth):
    """Lookahead cost: 0 if the box is a leaf, else (at depth 0) its deficit, else the best
    split's children's scores."""
    d = deficit(ctx, box, cands)
    if d <= 0:
        return 0
    if depth == 0:
        return d
    cn = near(ctx, box, cands)
    best = None
    for a in range(3):
        if box[2 * a + 1] - box[2 * a] <= 0:
            continue
        l, r = split(box, a)
        v = score(ctx, l, cn, depth - 1) + score(ctx, r, cn, depth - 1)
        best = v if best is None else min(best, v)
    return best + 0.5


# tree: 'L' or (axis, left, right)
def build(ctx, box, cands, depth, stats):
    """`cands` is what `check` receives at this node; a leaf tests exactly these."""
    if deficit(ctx, box, cands) <= 0:
        stats['leaves'] += 1
        stats['maxdepth'] = max(stats['maxdepth'], depth)
        stats['cand'] += len(cands)
        return 'L'
    if depth > stats['limit']:
        raise RuntimeError(f"depth limit at box {box}")
    x0, x1, y0, y1, U0, U1 = box
    ws = [(x1 - x0) / ctx.Q, (y1 - y0) / ctx.Q, (U1 - U0) / ctx.R]
    cn = near(ctx, box, cands)          # what the children receive (pruning never changes a verdict)
    best = None
    for a in range(3):                  # lookahead: minimise the children's scores
        if ws[a] == 0:
            continue
        l, r = split(box, a)
        key = (score(ctx, l, cn, stats['look']) + score(ctx, r, cn, stats['look']), -ws[a])
        if best is None or key < best[0]:
            best = (key, a)
    axis = best[1]
    stats['nodes'] += 1
    l, r = split(box, axis)
    return (axis, build(ctx, l, cn, depth + 1, stats), build(ctx, r, cn, depth + 1, stats))


# ---------------------------------------------------------------------------------------------
# Lean emission

def leaves(t, memo):
    if t == 'L':
        return 1
    k = id(t)
    if k not in memo:
        memo[k] = leaves(t[1], memo) + leaves(t[2], memo)
    return memo[k]


def select(ctx, box, cands):
    """The gap list `sel` of a leaf (see `BoxTree.capSel`)."""
    x0, x1, y0, y1, U0, U1 = box
    assert U1 <= ctx.R
    xl, xh, yl, yh = clip(ctx, box)
    if xh < xl or yh < yl:
        return []
    tr = [(g * ctx.Q, a, b) for a, b, g in triples(ctx.R, U0, U1)]
    ok = [i for i, (X, Y, w) in enumerate(cands)
          if all(tri_ok(G, a, b, xl, xh, yl, yh, X * ctx.S, Y * ctx.S) for G, a, b in tr)]
    # claim the heaviest certified points (fewest kernel tests), listed in candidate order
    need, take = ctx.W, []
    for i in sorted(ok, key=lambda i: -cands[i][2]):
        if need == 0:
            break
        take.append(i)
        need = nsub(need, cands[i][2])
    sel, prev = [], -1
    for i in sorted(take):
        sel.append(i - prev - 1)
        prev = i
    assert need == 0, f"leaf fails on replay: {box}"
    return sel


def replay(ctx, t, box, cands, fratio, st, out):
    """Append to `out` the digit stream (see `BoxTree.dec`) of the subtree `t` checked on `box`
    with candidate list `cands`, deciding where to prune (`F`) and each leaf's selection."""
    if t == 'L':
        sel = select(ctx, box, cands)
        out += [0, len(sel)] + sel
        return
    axis, l, r = t
    fc = near(ctx, box, cands)
    if len(fc) <= fratio * len(cands):
        out.append(4)
        cands = fc
        st['F'] += 1
    out.append(1 + axis)
    lb, rb = split(box, axis)
    replay(ctx, l, lb, cands, fratio, st, out)
    replay(ctx, r, rb, cands, fratio, st, out)


def encode(digits):
    B = max(5, max(digits) + 1)
    n = 0
    for d in reversed(digits):
        n = n * B + d
    return B, n


def emit_ptree(P):
    def b(lo, hi):
        if lo >= hi:
            return '.leaf'
        mid = (lo + hi) // 2
        x, y, w = P[mid]
        return f"(.node {b(lo, mid)} {x} {y} {w} {b(mid + 1, hi)})"
    return b(0, len(P))


HDR = "set_option linter.style.longLine false\n"
FUEL = 128  # > depth of any chunk (each split or prune node is one level)


def emit(args, sha, s, D, W, pts, S, R, Umax, root_box, tree, stats, ctx):
    import os
    name, outdir = args.name, args.outdir
    os.makedirs(outdir, exist_ok=True)
    mod = outdir.rstrip('/').replace('lean/', '', 1).replace('/', '.')   # e.g. Sqpack.S12U
    Mq = int(s * D)
    P = sorted(pts)
    memo = {}
    chunks = []   # (tree, box)

    def skel(t, box):
        if t == 'L' or leaves(t, memo) <= args.chunk:
            chunks.append((t, box))
            return f"ok{len(chunks) - 1}"
        axis, l, r = t
        lb, rb = split(box, axis)
        return f"(Cov.split{'XYU'[axis]} {lb[2 * axis + 1]} {skel(l, lb)} {skel(r, rb)})"

    proof = skel(tree, root_box)
    ns = f"SquarePacking.{name}"
    covT = f"Cov {D} {S} {Mq} {R} {W} pts.toList"
    # --- points
    doc = (f"/-!\n# `{name}`: certificate points (generated by `lean/scripts/gen_boxtree.py`; do not edit)\n\n"
           f"From `{args.cert}`, sha256 `{sha}`:\n{len(pts)} points `(X/{D}, Y/{D})` with weights `w/{W}`, "
           f"container `[0, {Mq}/{D}]²`.\n-/\n")
    L = ["import Sqpack.BoxTree\n", HDR, doc, f"namespace {ns}\n", "open BoxTree\n",
         "/-- The certificate points `(X, Y, w)`, in a search tree on `(X, Y)`. -/",
         f"def pts : PTree :=\n  {emit_ptree(P)}\n",
         "theorem pts_nodup : pts.toList.Nodup :=\n  PTree.nodup_of_chainB _ (by decide +kernel)\n",
         f"theorem pts_d4 : d4Check {Mq} pts = true := by decide +kernel\n",
         f"theorem pts_wsum : pts.wsum = {sum(w for _, _, w in pts)} := by decide +kernel\n",
         f"end {ns}\n"]
    open(f"{outdir}/Pts.lean", 'w').write("\n".join(L))
    # --- parts
    st = dict(F=0, digits=0)
    enc = []      # per chunk: (base, numeral, number of digits)
    for t, box in chunks:
        digits = []
        replay(ctx, t, box, P, args.fratio, st, digits)
        enc.append(encode(digits) + (len(digits),))
    # balance the parts by leaves (default) or by digits (the kernel's time *and* memory grow with
    # a file's digits: dense certificates put far more digits on some leaves than on others)
    size = [enc[i][2] if args.balance == 'digits' else leaves(t, memo) for i, (t, _) in enumerate(chunks)]
    total = sum(size)
    parts, cur, acc = [], [], 0
    for i in range(len(chunks)):
        cur.append(i); acc += size[i]
        if acc >= total * (len(parts) + 1) / args.parts and len(parts) < args.parts - 1:
            parts.append(cur); cur = []
    parts.append(cur)
    for pi, idxs in enumerate(parts):
        L = [f"import {mod}.Pts\n", HDR,
             f"/-!\n# `{name}`: box-tree chunks {idxs[0]}..{idxs[-1]} (generated; do not edit)\n\n"
             f"Each `okI` is one kernel evaluation (`decide +kernel`) of `BoxTree.check` on one subtree.\n-/\n",
             f"namespace {ns}\n", "open BoxTree BoxTree.BT\n"]
        for i in idxs:
            t, box = chunks[i]
            bx = ' '.join(map(str, box))
            B, code, nd = enc[i]
            st['digits'] += nd
            L.append(f"/-- Chunk {i}: {leaves(t, memo)} leaves, {nd} base-{B} digits. -/")
            L.append(f"def c{i} : ℕ :=\n  0x{code:x}\n")
            L.append(f"theorem ok{i} : {covT} {bx} :=\n"
                     f"  sound {D} {S} {Mq} {R} {W} {ctx.F} pts.toList (by norm_num) (by norm_num) "
                     f"(by norm_num) pts_nodup (dec {B} {FUEL} c{i}).1 {bx} pts.toList\n"
                     f"    (List.Sublist.refl _) (by decide +kernel)\n")
        L.append(f"end {ns}\n")
        open(f"{outdir}/Part{pi}.lean", 'w').write("\n".join(L))
    # --- glue
    imports = "\n".join(f"import {mod}.Part{pi}" for pi in range(len(parts)))
    L = [imports + "\n", HDR,
         f"/-!\n# `{name}`: the box tree covers the D4 fundamental region (generated; do not edit)\n\n"
         f"{stats['leaves']} leaves ({stats['nodes']} splits, depth {stats['maxdepth']}) in {len(chunks)} chunks "
         f"of at most {args.chunk} leaves, {len(parts)} files;\n"
         f"spatial scale `Q = {D}·{S}`, angle `u = U/{R}`, root `u ∈ [0, {Umax}/{R}]`.\n-/\n",
         f"namespace {ns}\n", "open BoxTree\n",
         "/-- **The box tree covers the D4 fundamental region.** -/",
         f"theorem cov_root : {covT} {' '.join(map(str, root_box))} :=\n  {proof}\n",
         f"end {ns}\n"]
    open(f"{outdir}/Cov.lean", 'w').write("\n".join(L))
    print(f"wrote {outdir}: {len(chunks)} chunks in {len(parts)} parts, {st['F']} prune nodes, "
          f"{st['digits']} digits",
          file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cert')
    ap.add_argument('--n', type=int, required=True)
    ap.add_argument('--K', type=int, default=12)
    ap.add_argument('--J', type=int, default=20)
    ap.add_argument('--ru', default='29/70')
    ap.add_argument('--chunk', type=int, default=600)
    ap.add_argument('--parts', type=int, default=4)
    ap.add_argument('--look', type=int, default=1, help='split lookahead depth')
    ap.add_argument('--fratio', type=float, default=0.85)
    ap.add_argument('--balance', choices=['leaves', 'digits'], default='leaves',
                    help='what the --parts files are balanced by')
    ap.add_argument('--name')
    ap.add_argument('--outdir')
    args = ap.parse_args()
    sha, s, D, W, pts = read_cert(args.cert)
    assert sum(w for _, _, w in pts) < args.n * W, "total weight is not < n"
    ru = Fraction(args.ru)
    assert ru * ru + 2 * ru > 1, "root u range must reach sqrt2 - 1"
    S = 2 ** args.K
    Q = D * S
    Mq = s * D
    assert Mq.denominator == 1, "container side must be a multiple of 1/D"
    M = int(Mq) * S
    R = ru.denominator * 2 ** args.J
    Umax = ru.numerator * 2 ** args.J
    ctx = Ctx(S, Q, M, R, W, 3 * Q // 4)
    stats = dict(leaves=0, nodes=0, maxdepth=0, cand=0, limit=80, look=args.look)
    root = (0, M - M // 2, 0, M - M // 2, 0, Umax)
    t0 = time.time()
    tree = build(ctx, root, sorted(pts), 0, stats)
    print(f"leaves {stats['leaves']} splits {stats['nodes']} maxdepth {stats['maxdepth']} "
          f"avg cands/leaf {stats['cand'] / stats['leaves']:.1f}  ({time.time() - t0:.1f}s)",
          file=sys.stderr)
    if args.outdir:
        emit(args, sha, s, D, W, pts, S, R, Umax, root, tree, stats, ctx)


if __name__ == '__main__':
    main()
