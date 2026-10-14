"""A232 -- the SWAP-LEAF verifier (`swap-leaf-certificate-v1`).  stdlib + exact Fractions ONLY.

It is a NEW verifier file: the frozen `verify_case.py` (sha 521cb01f...) and A185's
`verify_case_v4.py` are not read, not imported and not changed by anything here.

THE CLAUSE IT CHECKS (docs/proofs/swap_leaf.md; Lean `Statements/SwapLeaf.lean`).  A cell is a
list of ROLES over the window W = [m_lo, s0]; a boxed role carries pose PIECES stated at s0 on
F = D_lambda P (A115/A183/A185 convention), an unboxed role carries none.  The certificate names
a corner `c`, a set `X` of roles and |X| unit cells `F_0 .. F_{|X|-1}` with `F_0` the corner slot.
The verifier re-derives, itself, from the s0 pieces:

  (1) PULL-BACK.   the original square's centre is the s0 centre divided by lambda in
      [1, lambda_max], lambda_max = s0 / m_lo, so its centre lies in
      [x0/lambda_max, x1] x [y0/lambda_max, y1]  (K0-WIDEN, k0_route.md s.4.1, read backwards);
      the tilt is unchanged by the dilation.
  (2) CORNER FRAME. the D4 map taking `c` to BL is x -> m - x and/or y -> m - y, an isometry of
      [0, m]^2; over m in [m_lo, s0] the image of the pulled-back centre range is contained in
      [m_lo - x1, s0 - x0/lambda_max] (resp. y), and the tilt bin becomes [90 - th1, 90 - th0]
      under an ODD number of flips.  These supersets are m-free: that is the whole point.
  Then it checks, exactly:
  (3) every role NOT in X is BOXED (an unboxed role could be anywhere, so it must be in X);
  (4) |cells| == |X|, and cell 0 is the closed unit square [0,1]^2 (the BL slot);
  (5) every cell lies in [0, m_lo]^2, hence in [0, m]^2 for every m of the window;
  (6) the cells are pairwise interior-disjoint;
  (7) every cell MISSES the reach set of every role not in X: for every piece and every pose in
      it, the posed unit square has interior disjoint from the cell's interior.
  A PASS says: for every side m of the window and every packing in the cell, Lemma CELLS
  (`cells_swap`) exchanges it, at the SAME side, into a packing with the corner `c` settled.
  With k1-a (no packing at m in [3.82, s-hat) has a settled corner) the cell is DEAD.  The k1-a
  citation is a DEPENDENCY, printed on every PASS; the verifier does not prove it.

    python verify_swap232.py <cert.json> [--quiet]
"""
import json
import math
import sys
from fractions import Fraction as Fr

TDEN = 1 << 24                       # A57's rational grid for t = tan(theta/2)
SQRT2_HI = Fr(1414214, 10 ** 6)      # > sqrt 2
SQRT2_LO = Fr(1414213, 10 ** 6)      # < sqrt 2
HALF = Fr(1, 2)


def t_lo(th):
    return Fr(math.floor(math.tan(math.radians(th) / 2) * TDEN) - 1, TDEN) if th > 0 else Fr(0)


def t_hi(th):
    return Fr(math.ceil(math.tan(math.radians(th) / 2) * TDEN) + 1, TDEN) if th < 90 else Fr(1)


def _u_of_t(t):
    return (1 - t * t + 2 * t) / (1 + t * t)


def cs_max_exact(t0, t1):
    """exact rational UPPER bound of max(cos th + sin th) over t = tan(th/2) in [t0, t1]."""
    tlo, thi = SQRT2_LO - 1, SQRT2_HI - 1
    if t0 <= thi and t1 >= tlo:
        return SQRT2_HI
    return max(_u_of_t(t0), _u_of_t(t1))


def proj_min_exact(dx, dy, t0, t1):
    """exact lower bound of min over the tilt bin of  dx cos th + dy sin th  (A161's two-endpoint
    rule: dx cos + dy sin = R cos(th - phi) is unimodal on [0, 90] unless dx, dy <= 0)."""
    dx, dy = Fr(dx), Fr(dy)
    if dx <= 0 and dy <= 0:
        return -(abs(dx) + abs(dy))
    out = None
    for t in (Fr(t0), Fr(t1)):
        D = 1 + t * t
        g = (dx * (1 - t * t) + 2 * dy * t) / D
        out = g if out is None else min(out, g)
    return out


# ===================================================================== exact geometry
def box_misses_axis_cell(box, cell):
    """SOUND and exact: every pose in `box` = (x0, x1, y0, y1, t0, t1) gives a unit square whose
    interior misses the interior of the axis cell [X0, X1] x [Y0, Y1].  Full separating axis:
    the cell's two normals (square radius <= cs_max/2) and the square's own two (radius 1/2),
    each with both signs -- A161 `chordlane.box_misses_cell_exact`, re-implemented here."""
    x0, x1, y0, y1, t0, t1 = box
    X0, X1, Y0, Y1 = (Fr(v) for v in cell)
    hmax = cs_max_exact(t0, t1) / 2
    for nm, mgn in (("ex+", x0 - X1), ("ex-", X0 - x1), ("ey+", y0 - Y1), ("ey-", Y0 - y1)):
        if mgn >= hmax:
            return True, dict(axis=nm, margin=str(mgn - hmax))
    DX, DY = (x0 - X1, x1 - X0), (y0 - Y1, y1 - Y0)
    for k in (0, 1):
        for sg in (1, -1):
            worst = None
            for dx in DX:
                for dy in DY:
                    ex, ey = sg * dx, sg * dy
                    if k == 1:
                        ex, ey = ey, -ex
                    g = proj_min_exact(ex, ey, t0, t1)
                    worst = g if worst is None else min(worst, g)
            if worst >= HALF:
                return True, dict(axis="w%d%s" % (k, "+-"[sg < 0]), margin=str(worst - HALF))
    return False, None


def box_misses_poly(box, verts):
    """SOUND (not complete): every pose in `box` misses the interior of the convex polygon
    `verts` (rational, counter-clockwise).  Separating axes = the POLYGON's edge normals only,
    with the posed square's support radius bounded by |n| * sqrt2 / 2 (tilt-free).  Incomplete
    by design -- a failure is reported as `not certified`, never as `meets`."""
    x0, x1, y0, y1, _t0, _t1 = box
    V = [(Fr(a), Fr(b)) for a, b in verts]
    C = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    k = len(V)
    for i in range(k):
        ax, ay = V[i]
        bx, by = V[(i + 1) % k]
        for nx, ny in ((by - ay, ax - bx), (ay - by, bx - ax)):
            L = min(nx * cx + ny * cy for cx, cy in C) - max(nx * vx + ny * vy for vx, vy in V)
            if L > 0 and 2 * L * L >= nx * nx + ny * ny:
                return True, dict(axis="n%d" % i, margin=str(L))
    return False, None


def poly_of(cell):
    """the cell's four rational vertices, counter-clockwise."""
    if cell["kind"] == "axis":
        x, y = Fr(cell["x"]), Fr(cell["y"])
        return [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
    return [(Fr(a), Fr(b)) for a, b in cell["verts"]]


def is_unit_square(V):
    if len(V) != 4:
        return False
    for i in range(4):
        ax = V[(i + 1) % 4][0] - V[i][0]
        ay = V[(i + 1) % 4][1] - V[i][1]
        bx = V[(i + 2) % 4][0] - V[(i + 1) % 4][0]
        by = V[(i + 2) % 4][1] - V[(i + 1) % 4][1]
        if ax * ax + ay * ay != 1 or ax * bx + ay * by != 0:
            return False
    return True


def polys_interior_disjoint(A, B):
    """exact SAT over both polygons' edge normals; a non-negative gap on one axis certifies
    disjoint INTERIORS (closed convex sets may touch)."""
    for P, Q in ((A, B), (B, A)):
        k = len(P)
        for i in range(k):
            ax, ay = P[i]
            bx, by = P[(i + 1) % k]
            nx, ny = by - ay, ax - bx                      # outward for ccw order
            if min(nx * qx + ny * qy for qx, qy in Q) >= max(nx * px + ny * py for px, py in P):
                return True, dict(sep="edge %d" % i)
    return False, None


# ===================================================================== the normalisation
def normalise_piece(p, corner, m_lo, s0):
    """(1) pull-back by lambda in [1, s0/m_lo] and (2) the D4 map taking `corner` to BL, as
    m-free supersets.  Returns (x0, x1, y0, y1, t0, t1) with t = tan(theta/2) outward-rounded."""
    lam = Fr(s0) / Fr(m_lo)
    x0, x1 = Fr(p["x0"]) / lam, Fr(p["x1"])
    y0, y1 = Fr(p["y0"]) / lam, Fr(p["y1"])
    th0, th1 = float(p["th0"]), float(p["th1"])
    fx, fy = corner in (1, 2), corner in (2, 3)
    if fx:
        x0, x1 = Fr(m_lo) - x1, Fr(s0) - x0
    if fy:
        y0, y1 = Fr(m_lo) - y1, Fr(s0) - y0
    if fx != fy:
        th0, th1 = 90.0 - th1, 90.0 - th0
    t0, t1 = t_lo(th0), t_hi(th1)
    if t0 > t1:
        t0, t1 = t1, t0
    return (x0, x1, y0, y1, t0, t1)


# ===================================================================== the verifier
def verify(cert, log=print):
    fails = []

    def need(ok, msg):
        if not ok:
            fails.append(msg)
        return ok

    need(cert.get("format") == "swap-leaf-certificate-v1", "format")
    m_lo, s0 = Fr(cert["m_lo"]), Fr(cert["s0"])
    need(Fr(191, 50) <= m_lo < s0 <= Fr(3877084, 10 ** 6), "window [m_lo, s0] inside [3.82, s-hat]")
    corner = int(cert["corner"])
    need(corner in (0, 1, 2, 3), "corner in 0..3")
    roles, X = cert["roles"], list(cert["X"])
    names = [r["name"] for r in roles]
    need(len(set(names)) == len(names) == int(cert["n"]), "n distinct roles")
    need(set(X) <= set(names), "X is a set of roles")
    outside = [r for r in roles if r["name"] not in X]
    for r in outside:
        need(bool(r.get("pieces")), "role %s is outside X and must be BOXED" % r["name"])
        for p in r.get("pieces") or []:
            need(0 <= float(p["th0"]) <= float(p["th1"]) <= 90,
                 "role %s: tilt bin inside [0, 90] (a bin crossing 90 must be split)" % r["name"])
            need(Fr(p["x0"]) <= Fr(p["x1"]) and Fr(p["y0"]) <= Fr(p["y1"]),
                 "role %s: centre box non-empty" % r["name"])
    cells = cert["cells"]
    need(len(cells) == len(X), "|cells| = |X| (%d vs %d)" % (len(cells), len(X)))
    polys = [poly_of(c) for c in cells]
    for i, V in enumerate(polys):
        need(is_unit_square(V), "cell %d is a unit square" % i)
        need(all(0 <= v[0] <= m_lo and 0 <= v[1] <= m_lo for v in V), "cell %d inside [0, m_lo]^2" % i)
    need(cells and cells[0]["kind"] == "axis" and Fr(cells[0]["x"]) == 0 and Fr(cells[0]["y"]) == 0,
         "cell 0 is the BL slot [0,1]^2 of the corner frame")
    for i in range(len(polys)):
        for j in range(i + 1, len(polys)):
            ok, _d = polys_interior_disjoint(polys[i], polys[j])
            need(ok, "cells %d, %d interior-disjoint" % (i, j))
    misses = 0
    for r in outside:
        for pi, p in enumerate(r["pieces"]):
            b = normalise_piece(p, corner, m_lo, s0)
            for ci, c in enumerate(cells):
                if c["kind"] == "axis":
                    ok, d = box_misses_axis_cell(b, (Fr(c["x"]), Fr(c["x"]) + 1,
                                                     Fr(c["y"]), Fr(c["y"]) + 1))
                else:
                    ok, d = box_misses_poly(b, c["verts"])
                need(ok, "role %s piece %d misses cell %d" % (r["name"], pi, ci))
                misses += 1
    if fails:
        for f in fails[:12]:
            log("FAIL %s" % f)
        log("FAIL swap-leaf certificate (%d failed checks)" % len(fails))
        return 1
    log("miss certificates checked: %d ; cells %d ; |X| %d ; roles outside X %d"
        % (misses, len(cells), len(X), len(outside)))
    log("PASS swap-leaf: every packing of the cell exchanges at the same side into one with "
        "corner %d settled (Lemma CELLS / cells_swap)." % corner)
    log("DEPENDENCY (not checked here): k1-a -- no packing at m in [3.82, s-hat) contains a "
        "corner slot square (k0_route.md s.3, the k1_00 tree).  Given k1-a the cell is DEAD.")
    return 0


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    quiet = "--quiet" in sys.argv
    cert = json.load(open(args[0], encoding="utf-8"))
    return verify(cert, log=(lambda *a: None) if quiet else print)


if __name__ == "__main__":
    sys.exit(main())
