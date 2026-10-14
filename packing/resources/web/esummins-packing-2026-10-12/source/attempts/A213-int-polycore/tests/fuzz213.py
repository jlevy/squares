"""A213 differential test 2 -- FUZZ: random piece sets through the library rebuild and the integer-space rebuild
(identical vertices / cores / k_info / exceptions), random boxes through both builds, random and BOUNDARY rational
points through the three vertex tests (Fraction / integer / float-filter+exact / object), plus the polygon
primitives on random rational polygons.   python tests/fuzz213.py [n_sets=150] [seed=213]"""
import os
import random
import sys
import time
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.abspath(os.path.join(HERE, "..", "code"))
sys.path.insert(0, CODE)
sys.path.insert(0, HERE)
os.environ["A213_INTCORE"] = "1"
import polycore_int as PI                                      # noqa: E402
import polycore_vec as PV                                      # noqa: E402
import mbpatch213 as M                                         # noqa: E402
import multibox as MB                                          # noqa: E402
import polycore as PC                                          # noqa: E402
from caselp import Box, t_lo, t_hi                             # noqa: E402
import replay213 as R                                          # noqa: E402

VDEN = PC.VDEN


def rand_pieces(rng):
    """a role's pieces: sub-rects of one hull x sub-bins of one tilt interval, some dropped, some split."""
    x0 = Fr(rng.randint(500, 3000), 1000)
    y0 = Fr(rng.randint(500, 3000), 1000)
    w = Fr(rng.randint(2, 400), 1000)
    h = Fr(rng.randint(2, 400), 1000)
    d0 = rng.uniform(0.0, 88.0)
    d1 = min(90.0, d0 + rng.choice([0.0, 0.3, 2.0, 8.0, 25.0, 60.0]))
    t0, t1 = t_lo(d0), t_hi(d1)
    nx, ny, nb = rng.choice([1, 1, 2, 4]), rng.choice([1, 1, 2, 4]), rng.choice([1, 2, 3, 6])
    out = []
    for i in range(nx):
        for j in range(ny):
            for (a, b) in MB.sub_bins(t0, t1, nb):
                if rng.random() < 0.25:
                    continue
                r = (x0 + w * Fr(i, nx), x0 + w * Fr(i + 1, nx), y0 + h * Fr(j, ny), y0 + h * Fr(j + 1, ny))
                if rng.random() < 0.3:                          # an uneven clip: shave one side by a random rational
                    k = rng.randint(0, 3)
                    r = list(r)
                    sh = (r[1] - r[0] if k < 2 else r[3] - r[2]) * Fr(rng.randint(1, 40), 100)
                    r[k] = r[k] + sh if k in (0, 2) else r[k] - sh
                    r = tuple(r)
                out.append((R.mkbin(a, b), r))
    if not out:
        out.append((R.mkbin(t0, t1), (x0, x0 + w, y0, y0 + h)))
    return out


def rec_of(pieces, kmode, n_grid):
    return dict(name="F", kmode=kmode, args=[], kw=dict(n_grid=str(n_grid)) if kmode == "union" else {},
                pieces=[[str(bn.t0), str(bn.t1), [str(x) for x in r]] for (bn, r) in pieces])


def main():
    n_sets = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 213)
    lib = MB.MBox.rebuild
    n = mism = 0
    kinds = {}
    tl = ti = 0.0
    for _ in range(n_sets):
        pieces = rand_pieces(rng)
        kmode = rng.choice(["pieces", "pieces", "union"])
        rec = rec_of(pieces, kmode, rng.choice([33, 97]))
        M.uninstall()
        r0, dt0, _ = R.run_one(rec, lib)
        M.install(verify=False)
        r1, dt1, _ = R.run_one(rec, lib)
        n += 1
        tl += dt0
        ti += dt1
        k = r0.get("k_source") or ("error:" + r0["error"].split(":")[0])
        kinds[k] = kinds.get(k, 0) + 1
        if r0 != r1:
            mism += 1
            print("REBUILD MISMATCH", rec, r0, r1)
    print("fuzz rebuilds: %d sets, %d mismatches; kinds %s; lib %.3f s/call int %.3f s/call (x%.1f)" % (
        n, mism, kinds, tl / n, ti / n, tl / max(ti, 1e-9)))
    # --- vertex tests: random + boundary points against random boxes (Fraction / int / vec-filter / obj)
    nv = vm = 0
    M.uninstall()
    for _ in range(max(20, n_sets // 3)):
        x0, y0 = rng.uniform(0.5, 3.0), rng.uniform(0.5, 3.0)
        b = Box(x0, x0 + rng.uniform(0.0, 0.3), y0, y0 + rng.uniform(0.0, 0.3), rng.uniform(0, 89), 0)
        b.th1 = min(90.0, b.th0 + rng.choice([0.0, 0.5, 5.0, 30.0]))
        t0, t1 = t_lo(b.th0), t_hi(b.th1)
        pts = []
        for _k in range(30):
            pts.append((Fr(round(rng.uniform(b.x0 - 0.7, b.x1 + 0.7) * VDEN), VDEN), Fr(round(rng.uniform(b.y0 - 0.7, b.y1 + 0.7) * VDEN), VDEN)))
        # boundary: exactly half a side from a corner along the axes at t = t0 (cos, sin rational) and small offsets
        c, s = MB._cs_at(t0)
        for (cx, cy) in ((b.x0, b.y0), (b.x1, b.y1)):
            for (u, w) in ((Fr(1, 2), Fr(0)), (Fr(1, 2), Fr(1, 3)), (Fr(-1, 2), Fr(-1, 2)), (Fr(0), Fr(1, 2))):
                px = Fr(cx) + u * c - w * s
                py = Fr(cy) + u * s + w * c
                for e in (0, Fr(1, 10 ** 12), -Fr(1, 10 ** 12)):
                    pts.append((px + e, py))
        for (x, y) in pts:
            a0 = PC.vertex_ok(x, y, b, t0, t1)
            a1 = PI.vertex_ok(x, y, b, t0, t1)
            a2 = PV.certify_verts([(x, y)], [(b, t0, t1)]) == []
            a3 = PV.certify_verts_obj([(x, y)], [(b, t0, t1)]) == []
            nv += 1
            if not (a0 == a1 == a2 == a3):
                vm += 1
                print("VERTEX MISMATCH", b, x, y, a0, a1, a2, a3)
    print("fuzz vertex tests: %d points, %d mismatches; vec filter exact fallbacks %d of %d pairs" % (
        nv, vm, PV.STATS["exact_pairs"], PV.STATS["pairs"]))
    # --- polygon primitives on random rational polygons (intersect / simplify / round / hull)
    npoly = pm = 0
    for _ in range(max(20, n_sets // 2)):
        polys = []
        for _k in range(rng.randint(2, 6)):
            cx, cy = Fr(rng.randint(1000, 3000), 1000), Fr(rng.randint(1000, 3000), 1000)
            rad = Fr(rng.randint(100, 600), 1000)
            m = rng.randint(3, 9)
            import math
            pts = [(cx + Fr(round(float(rad) * math.cos(2 * math.pi * i / m) * VDEN), VDEN),
                    cy + Fr(round(float(rad) * math.sin(2 * math.pi * i / m) * VDEN), VDEN)) for i in range(m)]
            polys.append(PC._hull_frac(pts))
        mv = rng.choice([4, 6, 16])
        P0 = MB.intersect_frac(polys, max_v=mv)
        P1 = PI.intersect_h([[PI.hom(x, y) for (x, y) in V] for V in polys], max_v=mv)
        npoly += 1
        P1f = [(Fr(X, W), Fr(Y, W)) for (X, Y, W) in P1]
        if [tuple(p) for p in P0] != P1f:
            pm += 1
            print("INTERSECT MISMATCH", P0[:3], P1f[:3])
        if len(P0) >= 3:
            for sh in MB.K_SHRINKS:
                V0 = MB._round_grid_inward(P0, sh)
                V1 = [(Fr(x, VDEN), Fr(y, VDEN)) for (x, y) in PI.round_inward_h([PI.hom(x, y) for (x, y) in P0], sh)]
                if [tuple(p) for p in V0] != V1:
                    pm += 1
                    print("ROUND MISMATCH", sh, V0[:2], V1[:2])
    print("fuzz polygon primitives: %d cases, %d mismatches" % (npoly, pm))
    return mism + vm + pm


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
