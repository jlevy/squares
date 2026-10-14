#!/usr/bin/env python3
"""
verify_case_v3.py -- A135 T2.  The fixed-side case verifier of A13/A53
(`attempts/A57-shadow-trees/code/verify_case.py`, sha256 521cb01f...) PLUS ONE new exemption
clause: the POLYGON CORE (`hypotheses.polycores`), specified in
`attempts/A132-polygon-core/notes/spec.md` Sec.2-3.

**v1 IS FROZEN AND UNTOUCHED.**  This is a new file and it does not copy the frozen one: it
IMPORTS it, so the audited integer core (`imul4`, `trig_int`, `box_trig`, `atom_inside_int`,
`vacuous_int`, `clip_int`, `core_exempt_frac`, `nofam_exempt`, the box tree, `covered`, the
witness machinery, the mass arithmetic) is LITERALLY the same code -- the discipline
`verify_param.py` states for its own reuse.  The only new exact predicates are the two below.
On a certificate with no `polycores` field the class is v1 byte-for-byte in behaviour, which
`--regress` checks against the frozen verifier on a corpus.

WHAT IS PROVED.  Unchanged from v1 except for the exemption disjunction.  A certificate declares
the atomic measure mu, the budget b = n - #cores, the core squares K_j and the NO-families; a PASS
certifies

    every admissible closed unit square Q in [0,s]^2 that is not EXEMPT has mu(Q) >= 1 + margin,

with  Q EXEMPT  iff  (i) Q's pose is in a NO-family, or (ii) Q meets some core square K_j, or
(iii) [NEW] Q meets some certified polygon core P_k.  Together with sum_i w_i < b this kills the
node exactly as in v1, because the bridge argument uses only

    the exempting set is contained in Q0(pose) for EVERY pose in the hypothesis box of core j,

which is what the vertex test below certifies for a polygon just as `Box.core()`'s formula does for
a square (A132 spec Sec.0.1).  The n - #cores squares OTHER than the core witnesses are non-exempt,
pairwise disjoint and each of mass >= 1; a placement meeting the polygon of box j overlaps that
box's witness, so it either IS that witness or contradicts disjointness.  NOTHING about the
argument changes; only the exempting set grows.

TRUST STORY.  The emitter's polygon is UNTRUSTED DATA.  Before any box is discharged this verifier
re-runs, in exact rationals:

  (P1) every listed vertex lies in Q(c, theta) for every (c, theta) in the entry's own rational
       box  -- the two quadratics in t = tan(theta/2) of A132 spec Sec.1, at the four corners of the
       centre rectangle and for both edge normals, decided exactly;
  (P2) the four corners of the SQUARE core the entry refines (`cores[core]`) pass the same test
       against the same box.

(P2) is what binds the polygon to a hypothesis the certificate actually declares: the square core
and the polygon are then two cores of the SAME box, so the polygon inherits the square's bridge.
A `polycores` entry that fails either check is a HARD REJECT (exit 2), not a warning.

USAGE
    python verify_case_v3.py CERT.json [--depth D] [--jobs J] [--split k] [--report [path]]
        [--replay] [--regress FROZEN_CERT ...] [--quiet]   (+ every v1 flag)

    --replay   machine-independent replay: no float pre-filter anywhere (neither v1's atom
               shortlist nor the polygon pre-filter), one process, so every decision is taken by
               exact integer/Fraction arithmetic and the verdict does not depend on the FPU, the
               numpy build or the process count.
"""
import argparse
import json
import math
import os
import sys
import time
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FROZEN_DIR = os.path.join(ROOT, "A57-shadow-trees", "code")
if FROZEN_DIR not in sys.path:
    sys.path.insert(0, FROZEN_DIR)

import verify_case as vc                                        # noqa: E402  (FROZEN, imported)

try:
    import numpy as np
except Exception:                                               # pragma: no cover
    np = None

HALF = F(1, 2)
ZERO = F(0)
ONE = F(1)

FROZEN_SHA_PREFIX = "521cb01f"


# ===================================================================== (P1)/(P2) the vertex test
def _quad_nonneg(A, B, C, t0, t1):
    """A t^2 + B t + C >= 0 for every t in [t0, t1]?  Exact in Fractions.

    Independent re-implementation (A132 spec Sec.1): endpoints, plus the discriminant test at the
    stationary point when it is interior and the parabola opens upward."""
    if A * t0 * t0 + B * t0 + C < 0:
        return False
    if A * t1 * t1 + B * t1 + C < 0:
        return False
    if A > 0 and t0 * (2 * A) <= -B <= t1 * (2 * A):
        return 4 * A * C - B * B >= 0
    return True


def point_in_all_poses(vx, vy, x0, x1, y0, y1, t0, t1):
    """EXACT: does the rational point (vx, vy) lie in the CLOSED unit square Q(c, theta(t)) for
    every centre c in [x0,x1] x [y0,y1] and every t in [t0, t1]?

    With d = v - c, |R(-theta) d|_inf <= 1/2 for t = tan(theta/2) is, after clearing the positive
    denominator 1 + t^2, the pair of quadratics of A132 spec Sec.1 for (u, w) = (dx, dy) and
    (dy, -dx).  c enters affinely, so the maximum over the centre rectangle is at a corner and
    requiring all four corners is equivalent to requiring the maximum."""
    for (cx, cy) in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
        dx, dy = vx - cx, vy - cy
        for (u, w) in ((dx, dy), (dy, -dx)):
            if not _quad_nonneg(HALF + u, -2 * w, HALF - u, t0, t1):
                return False
            if not _quad_nonneg(HALF - u, 2 * w, HALF + u, t0, t1):
                return False
    return True


# ===================================================================== the polygon core hypothesis
class PolyCoreH:
    """One `polycores` entry, CERTIFIED at construction.

    Fields: `core` (index into `cores`), the rational box (x0,x1,y0,y1,t0,t1) and the rational ccw
    vertex list.  Raises ValueError if (P1) or (P2) fails."""

    def __init__(self, d, cores):
        self.core = int(d["core"])
        b = d["box"]
        self.x0, self.x1 = vc._rat(b["x0"]), vc._rat(b["x1"])
        self.y0, self.y1 = vc._rat(b["y0"]), vc._rat(b["y1"])
        self.t0, self.t1 = vc._rat(b["t0"]), vc._rat(b["t1"])
        if not (self.x0 <= self.x1 and self.y0 <= self.y1 and 0 <= self.t0 <= self.t1 <= 1):
            raise ValueError("polycore: malformed box")
        self.verts = [(vc._rat(v[0]), vc._rat(v[1])) for v in d["verts"]]
        if not (3 <= len(self.verts) <= 64):
            raise ValueError(f"polycore: {len(self.verts)} vertices (want 3..64)")
        if not (0 <= self.core < len(cores)):
            raise ValueError(f"polycore: core index {self.core} out of range")
        # ---- (P1) every vertex inside every pose of the box
        for i, (vx, vy) in enumerate(self.verts):
            if not point_in_all_poses(vx, vy, self.x0, self.x1, self.y0, self.y1, self.t0, self.t1):
                raise ValueError(f"polycore: vertex {i} ({vx}, {vy}) is NOT in every pose of the box")
        # ---- (P2) the square core it refines is inside every pose of the SAME box
        k = cores[self.core]
        for i, j in ((1, 1), (1, -1), (-1, -1), (-1, 1)):
            cx = k.kx + k.a * (i * k.cm - j * k.sm)
            cy = k.ky + k.a * (i * k.sm + j * k.cm)
            if not point_in_all_poses(cx, cy, self.x0, self.x1, self.y0, self.y1, self.t0, self.t1):
                raise ValueError(f"polycore: core {self.core} is NOT inside every pose of the "
                                 f"declared box -- the polygon has no hypothesis behind it")
        # ---- convexity + orientation of the vertex list (the SAT below assumes a convex polygon)
        n = len(self.verts)
        cr = []
        for i in range(n):
            ax, ay = self.verts[i]
            bx, by = self.verts[(i + 1) % n]
            cx, cy = self.verts[(i + 2) % n]
            cr.append((bx - ax) * (cy - by) - (by - ay) * (cx - bx))
        if not (all(c >= 0 for c in cr) or all(c <= 0 for c in cr)):
            raise ValueError("polycore: vertex list is not convex")
        self.ccw = sum(cr) > 0
        # ---- edge normals, exact rationals (outward if ccw: n = (dy, -dx))
        self.normals = []
        for i in range(n):
            ax, ay = self.verts[i]
            bx, by = self.verts[(i + 1) % n]
            ex, ey = bx - ax, by - ay
            if ex == 0 and ey == 0:
                continue
            self.normals.append((ey, -ex) if self.ccw else (-ey, ex))
        # ---- exact projection ranges on the own normals
        self.proj = []
        for (nx, ny) in self.normals:
            ps = [nx * vx + ny * vy for (vx, vy) in self.verts]
            self.proj.append((min(ps), max(ps)))
        # ---- floats (shortlist only; never decides)
        self.fV = ([(float(a), float(b)) for a, b in self.verts])
        self.fN = [(float(a), float(b)) for a, b in self.normals]
        self.fP = [(float(a), float(b)) for a, b in self.proj]

    def to_json(self):
        return dict(core=self.core, verts=len(self.verts), normals=len(self.normals),
                    box=dict(x0=str(self.x0), x1=str(self.x1), y0=str(self.y0), y1=str(self.y1),
                             t0=str(self.t0), t1=str(self.t1)))


def polycore_exempt_frac(pc, t0, t1, x0, x1, y0, y1):
    """True iff for EVERY (t, cx, cy) in the box the CLOSED unit square Q(c, theta(t)) meets the
    convex rational polygon `pc` (SAT over both edge-normal families, proven by outward interval
    arithmetic).  A132 spec Sec.3.

    Separating-axis theorem for two convex polygons: if the projections overlap on every edge
    normal of BOTH, they intersect.  Here one of them moves with (c, t), so each overlap is proven
    for the whole box at once, with left sides bounded above and right sides bounded below."""
    C1_, S0 = vc.cos_sin_t(t0)          # cos decreasing, sin increasing in t on [0,1]
    C0, S1 = vc.cos_sin_t(t1)

    # ---------------------------------------------------------------- the POLYGON's edge normals
    for (nx, ny), (Plo, Phi) in zip(pc.normals, pc.proj):
        # Q's half-width in direction n: h = (|n.f1| + |n.f2|)/2, f1 = (C,S), f2 = (-S,C).
        a0, a1 = vc.imul4(C0, C1_, nx, nx)
        b0, b1 = vc.imul4(S0, S1, ny, ny)
        Alo, Ahi = a0 + b0, a1 + b1                          # n.f1 =  nx C + ny S
        a0, a1 = vc.imul4(-S1, -S0, nx, nx)
        b0, b1 = vc.imul4(C0, C1_, ny, ny)
        Blo, Bhi = a0 + b0, a1 + b1                          # n.f2 = -nx S + ny C
        Aabs = ZERO if Alo <= 0 <= Ahi else min(abs(Alo), abs(Ahi))
        Babs = ZERO if Blo <= 0 <= Bhi else min(abs(Blo), abs(Bhi))
        hlo = (Aabs + Babs) / 2                              # LOWER bound of h over the t-interval
        # n.c over the centre rectangle (affine in c: extremes at the corners)
        cmax = (nx * x1 if nx > 0 else nx * x0) + (ny * y1 if ny > 0 else ny * y0)
        cmin = (nx * x0 if nx > 0 else nx * x1) + (ny * y0 if ny > 0 else ny * y1)
        if cmax - hlo > Phi:
            return False
        if cmin + hlo < Plo:
            return False

    # ---------------------------------------------------------------- the SQUARE's own two axes
    for which in (0, 1):
        if which == 0:
            Ex0, Ex1, Ey0, Ey1 = C0, C1_, S0, S1             # f1 = (C, S)
        else:
            Ex0, Ex1, Ey0, Ey1 = -S1, -S0, C0, C1_           # f2 = (-S, C)

        def rng(px, py):
            a0, a1 = vc.imul4(Ex0, Ex1, px, px)
            b0, b1 = vc.imul4(Ey0, Ey1, py, py)
            return a0 + b0, a1 + b1

        vlo = max(rng(vx, vy)[0] for (vx, vy) in pc.verts)    # <= max_v f.v for every t
        vhi = min(rng(vx, vy)[1] for (vx, vy) in pc.verts)    # >= min_v f.v for every t
        clo = min(rng(cx, cy)[0] for cx in (x0, x1) for cy in (y0, y1))
        chi = max(rng(cx, cy)[1] for cx in (x0, x1) for cy in (y0, y1))
        if chi - HALF > vlo:
            return False
        if clo + HALF < vhi:
            return False
    return True


def polycore_exempt_float(pc, ft0, ft1, fx0, fx1, fy0, fy1, slack=1e-7):
    """float pre-filter: False => certainly not provably exempt (with slack); never decides."""
    C1_ = (1 - ft0 * ft0) / (1 + ft0 * ft0); S0 = 2 * ft0 / (1 + ft0 * ft0)
    C0 = (1 - ft1 * ft1) / (1 + ft1 * ft1); S1 = 2 * ft1 / (1 + ft1 * ft1)
    for (nx, ny), (Plo, Phi) in zip(pc.fN, pc.fP):
        a0, a1 = vc.imul4(C0, C1_, nx, nx); b0, b1 = vc.imul4(S0, S1, ny, ny)
        Alo, Ahi = a0 + b0, a1 + b1
        a0, a1 = vc.imul4(-S1, -S0, nx, nx); b0, b1 = vc.imul4(C0, C1_, ny, ny)
        Blo, Bhi = a0 + b0, a1 + b1
        Aabs = 0.0 if Alo <= 0 <= Ahi else min(abs(Alo), abs(Ahi))
        Babs = 0.0 if Blo <= 0 <= Bhi else min(abs(Blo), abs(Bhi))
        hlo = (Aabs + Babs) / 2
        cmax = (nx * fx1 if nx > 0 else nx * fx0) + (ny * fy1 if ny > 0 else ny * fy0)
        cmin = (nx * fx0 if nx > 0 else nx * fx1) + (ny * fy0 if ny > 0 else ny * fy1)
        if cmax - hlo > Phi + slack or cmin + hlo < Plo - slack:
            return False
    for which in (0, 1):
        if which == 0:
            Ex0, Ex1, Ey0, Ey1 = C0, C1_, S0, S1
        else:
            Ex0, Ex1, Ey0, Ey1 = -S1, -S0, C0, C1_

        def rng(px, py):
            a0, a1 = vc.imul4(Ex0, Ex1, px, px)
            b0, b1 = vc.imul4(Ey0, Ey1, py, py)
            return a0 + b0, a1 + b1

        vlo = max(rng(vx, vy)[0] for (vx, vy) in pc.fV)
        vhi = min(rng(vx, vy)[1] for (vx, vy) in pc.fV)
        clo = min(rng(cx, cy)[0] for cx in (fx0, fx1) for cy in (fy0, fy1))
        chi = max(rng(cx, cy)[1] for cx in (fx0, fx1) for cy in (fy0, fy1))
        if chi - 0.5 > vlo + slack or clo + 0.5 < vhi - slack:
            return False
    return True


# ===================================================================== the v3 verifier
class VerifierV3(vc.Verifier):
    """v1's Verifier with a THIRD exemption disjunct.  Nothing else is overridden: the box tree,
    `covered`, `make_witness`, `run` and `stats` are the frozen ones."""

    def __init__(self, *args, polycores=(), use_float_poly=True, **kw):
        super().__init__(*args, **kw)
        self.polycores = list(polycores)
        self.use_float_poly = bool(use_float_poly)
        self.n_exempt_poly = 0

    def reset_stats(self):
        super().reset_stats()
        self.n_exempt_poly = 0

    def exempt(self, T0, T1, X0, X1, Y0, Y1):
        if super().exempt(T0, T1, X0, X1, Y0, Y1):
            return True
        if not self.polycores:
            return False
        r, D = self.T_ROOT, self.D
        t0, t1 = F(T0, r), F(T1, r)
        x0, x1, y0, y1 = F(X0, D), F(X1, D), F(Y0, D), F(Y1, D)
        ft0, ft1, fx0, fx1, fy0, fy1 = T0 / r, T1 / r, X0 / D, X1 / D, Y0 / D, Y1 / D
        for pc in self.polycores:
            if self.use_float_poly and not polycore_exempt_float(pc, ft0, ft1, fx0, fx1, fy0, fy1):
                continue
            if polycore_exempt_frac(pc, t0, t1, x0, x1, y0, y1):
                self.n_exempt_poly += 1
                return True
        return False

    def stats(self):
        st = super().stats()
        st["exempt_poly"] = self.n_exempt_poly
        return st


# ===================================================================== certificate I/O
def load_certificate_v3(path, n_override=None):
    """v1's loader, then the `polycores` field (absent => v1/v2 semantics exactly)."""
    d, s, n, atoms, weights, total = vc.load_certificate(path, n_override)
    raw = (d.get("hypotheses") or {}).get("polycores") or []
    pcs = [PolyCoreH(e, d["_cores"]) for e in raw]
    d["_polycores"] = pcs
    return d, s, n, atoms, weights, total


# ===================================================================== parallel driver
_G = {}


def _worker_init(s, atoms, weights, margin, depth, tscale, use_float, max_w, per_box_cap,
                 cores, nofams, polycores, use_float_poly):
    _G["v"] = VerifierV3(s, atoms, weights, margin=margin, depth=depth, tscale=tscale,
                         use_float=use_float, max_witnesses=max_w, verbose=False,
                         cores=cores, nofams=nofams, polycores=polycores,
                         use_float_poly=use_float_poly)
    _G["cap"] = per_box_cap


def _worker(box):
    v = _G["v"]
    v.reset_stats()
    v.run([box], per_box_cap=_G["cap"])
    return v.stats(), v.witnesses


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cert", nargs="?")
    ap.add_argument("--depth", type=int, default=48)
    ap.add_argument("--strict-margin", type=str, default="0")
    ap.add_argument("--report", nargs="?", const="__auto__", default=None)
    ap.add_argument("--witness-file", type=str, default=None)
    ap.add_argument("--max-witnesses", type=int, default=200)
    ap.add_argument("--max-witnesses-per-box", type=int, default=8)
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--split", type=int, default=3)
    ap.add_argument("--scale-weights", type=str, default="1")
    ap.add_argument("--tscale", type=str, default="2")
    ap.add_argument("--no-float-prepass", action="store_true")
    ap.add_argument("--replay", action="store_true",
                    help="machine-independent replay: no float pre-filter anywhere, one process")
    ap.add_argument("--n", type=int, default=None)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    if not a.cert:
        ap.error("certificate path required")
    if a.replay:
        a.no_float_prepass = True
        a.jobs = 1

    t_start = time.time()
    try:
        d, s, n, atoms, weights, total = load_certificate_v3(a.cert, a.n)
    except Exception as e:
        print(f"MALFORMED certificate: {e}")
        return 2
    margin = F(a.strict_margin)
    scale = F(a.scale_weights)
    if scale != 1:
        weights = [w * scale for w in weights]
        total = sum(weights, ZERO)
    verbose = not a.quiet
    cores, nofams, budget = d["_cores"], d["_nofams"], d["_budget"]
    pcs = d["_polycores"]
    print(f"certificate: {a.cert}")
    print(f"s = {s} (~{float(s):.10f}), n = {n}, atoms = {len(atoms)}, "
          f"total mass = {total} (~{float(total):.10f}), margin = {margin}")
    print(f"hypotheses: {len(cores)} cores, {len(nofams)} NO-families, "
          f"{len(pcs)} polycores (all re-certified: vertices in every pose, and the square core "
          f"they refine likewise), budget = {budget}"
          + ("  [REPLAY: exact-only, 1 process]" if a.replay else ""))
    if total >= budget:
        print(f"FAIL: total mass {float(total):.6f} >= budget = {budget}: certificate proves nothing")
        return 2
    if s < 1:
        print("s < 1: no unit square fits; vacuous PASS")
        return 0

    use_float = not a.no_float_prepass
    v0 = VerifierV3(s, atoms, weights, margin=margin, depth=a.depth, tscale=F(a.tscale),
                    use_float=use_float, max_witnesses=a.max_witnesses, verbose=verbose,
                    cores=cores, nofams=nofams, polycores=pcs, use_float_poly=use_float)
    boxes = v0.root_boxes(a.split)
    stats, witnesses = {}, []
    if a.jobs > 1:
        import multiprocessing as mp
        with mp.Pool(a.jobs, initializer=_worker_init,
                     initargs=(s, atoms, weights, margin, a.depth, F(a.tscale), use_float,
                               a.max_witnesses, a.max_witnesses_per_box, cores, nofams, pcs,
                               use_float)) as pool:
            for st, ws in pool.imap_unordered(_worker, boxes):
                vc.merge_stats(stats, st)
                witnesses.extend(ws)
                if len(witnesses) >= a.max_witnesses:
                    pool.terminate()
                    break
    else:
        v0.run(boxes, per_box_cap=a.max_witnesses_per_box)
        stats = v0.stats()
        witnesses = v0.witnesses
    stats["witnesses"] = len(witnesses)
    elapsed = time.time() - t_start
    passed = len(witnesses) == 0
    print(f"boxes = {stats['boxes']}  covered = {stats['covered']}  vacuous = {stats['vacuous']}  "
          f"exempt = {stats.get('exempt', 0)} (core {stats.get('exempt_core', 0)}, "
          f"nofam {stats.get('exempt_nofam', 0)}, poly {stats.get('exempt_poly', 0)})  "
          f"split = {stats['split']}  exact atom checks = {stats['exact_atom_checks']}  "
          f"max depth = {stats['max_depth']}  time = {elapsed:.1f}s")
    if passed:
        print(f"PASS: every NON-EXEMPT closed unit square in [0,{s}]^2 has mass >= {ONE + margin} ; "
              f"total {total} < budget {budget}  ==>  no packing of {n} unit squares in "
              f"side <= {s} (~{float(s):.10f}) satisfies the hypotheses (node DEAD)")
    else:
        holes = [w for w in witnesses if w.get("kind") == "hole"]
        print(f"FAIL: {len(witnesses)} witness boxes at depth {a.depth} ({len(holes)} HOLES)")
        pick = min(witnesses, key=lambda w: w.get("float_mass", 9e9))
        if pick.get("placement"):
            p = pick["placement"]
            print(f"  worst witness: theta = {p['theta_deg']:.6f} deg, centre = "
                  f"({p['cx_float']:.9f}, {p['cy_float']:.9f}), exact mass = {pick['exact_mass']}")
        wf = a.witness_file or (os.path.splitext(a.cert)[0] + ".witnesses.json")
        with open(wf, "w") as fh:
            json.dump({"cert": a.cert, "s": str(s), "depth": a.depth, "margin": str(margin),
                       "witnesses": witnesses}, fh, indent=1)
        print(f"  witnesses written to {wf}")
    if a.report is not None:
        rp = a.report if a.report != "__auto__" else os.path.splitext(a.cert)[0] + ".report.json"
        with open(rp, "w") as fh:
            json.dump({"cert": a.cert, "verifier": "verify_case_v3 (A135) over frozen "
                                                   f"verify_case sha {FROZEN_SHA_PREFIX}...",
                       "replay": bool(a.replay), "s": str(s), "n": n, "atoms": len(atoms),
                       "total": str(total), "total_float": float(total), "budget": budget,
                       "depth": a.depth, "jobs": a.jobs, "split": a.split,
                       "float_prepass": use_float,
                       "polycores": [p.to_json() for p in pcs],
                       "result": "PASS" if passed else "FAIL", "time_s": elapsed, "stats": stats,
                       "witnesses_preview": witnesses[:20]}, fh, indent=1)
        print(f"  report written to {rp}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
