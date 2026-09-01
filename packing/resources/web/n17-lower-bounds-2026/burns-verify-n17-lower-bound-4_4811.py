from __future__ import annotations

from bisect import bisect_left, bisect_right
from fractions import Fraction as F
import numpy as np

# Proposed exact lower-bound certificate for packing 17 unit squares in a square.
#
# All geometric quantities and predicates are rational. NumPy is used only for
# integer range-addition and cumulative sums; no floating-point geometry is used.

L = F(44811, 10000)
B = F(9973, 10000)
T = F(207107, 500000)
KMAX = 180
D = T / KMAX
WEIGHT_SCALE = 10000
NGRID = 29
LAST = NGRID - 1

# (i, j, w): every distinct D4 image of grid point (i,j) receives weight w/10000.
CERT = [
    (1, 11, 107),
    (2, 4, 137),
    (2, 9, 214),
    (2, 11, 107),
    (2, 12, 137),
    (3, 4, 3884),
    (3, 7, 214),
    (3, 8, 913),
    (3, 9, 214),
    (3, 10, 214),
    (3, 11, 1234),
    (3, 12, 2189),
    (3, 14, 384),
    (4, 4, 1961),
    (4, 7, 520),
    (4, 8, 214),
    (4, 9, 1413),
    (4, 10, 1234),
    (4, 11, 1083),
    (4, 13, 137),
    (4, 14, 292),
    (7, 11, 529),
    (7, 12, 33),
    (8, 10, 906),
    (8, 11, 384),
    (8, 12, 351),
    (9, 9, 340),
    (9, 10, 180),
    (9, 11, 204),
    (9, 12, 549),
    (10, 12, 879),
    (10, 13, 201),
    (10, 14, 378),
    (11, 11, 396),
    (11, 12, 622),
    (11, 13, 204),
    (11, 14, 204),
]


def orbit(i: int, j: int) -> set[tuple[int, int]]:
    n = LAST
    return {
        (i, j), (n - i, j), (i, n - j), (n - i, n - j),
        (j, i), (n - j, i), (j, n - i), (n - j, n - i),
    }


def build_atoms() -> list[tuple[F, F, int]]:
    step = (L - 1) / LAST
    coord = [F(1, 2) + step * i for i in range(NGRID)]
    by_index: dict[tuple[int, int], int] = {}
    for i, j, w in CERT:
        for ij in orbit(i, j):
            if ij in by_index:
                raise ValueError(f"duplicate orbit assignment at {ij}")
            by_index[ij] = w
    return [
        (coord[i], coord[j], w)
        for (i, j), w in sorted(by_index.items())
    ]


# Clip a convex rational polygon against U >= bound or U <= bound.
def clip_u(
    poly: list[tuple[F, F]],
    bound: F,
    keep_ge: bool,
) -> list[tuple[F, F]]:
    if not poly:
        return []

    out: list[tuple[F, F]] = []

    def inside(p: tuple[F, F]) -> bool:
        return p[0] >= bound if keep_ge else p[0] <= bound

    prev = poly[-1]
    prev_in = inside(prev)
    for cur in poly:
        cur_in = inside(cur)
        if cur_in != prev_in:
            u1, v1 = prev
            u2, v2 = cur
            if u2 == u1:
                v = v1
            else:
                lam = (bound - u1) / (u2 - u1)
                v = v1 + lam * (v2 - v1)
            out.append((bound, v))
        if cur_in:
            out.append(cur)
        prev, prev_in = cur, cur_in
    return out


def center_domain(c: F, s: F) -> list[tuple[F, F]]:
    # A B-square at orientation (c,s) lies in [0,L]^2 exactly when its
    # center lies in [h,L-h]^2, with h=B(c+s)/2.
    # Transform that square to the B-square's (U,V) frame.
    h = B * (c + s) / 2
    lo, hi = h, L - h
    corners_xy = [(lo, lo), (hi, lo), (hi, hi), (lo, hi)]
    return [(c * x + s * y, -s * x + c * y) for x, y in corners_xy]


def verify_orientation(
    c: F,
    s: F,
    atoms: list[tuple[F, F, int]],
) -> int:
    """Return the exact minimum integer score for one rational orientation."""
    half = B / 2
    dom = center_domain(c, s)
    u_dom_min = min(u for u, _ in dom)
    u_dom_max = max(u for u, _ in dom)
    v_dom_min = min(v for _, v in dom)
    v_dom_max = max(v for _, v in dom)

    rects: list[tuple[F, F, F, F, int]] = []
    u_events = {u_dom_min, u_dom_max}
    v_events = {v_dom_min, v_dom_max}

    # In center coordinates, atom membership is an axis-aligned rectangle.
    for x, y, w in atoms:
        pu = c * x + s * y
        pv = -s * x + c * y
        u1, u2 = pu - half, pu + half
        v1, v2 = pv - half, pv + half
        rects.append((u1, u2, v1, v2, w))
        u_events.add(u1)
        u_events.add(u2)
        v_events.add(v1)
        v_events.add(v2)

    ue = sorted(u_events)
    ve = sorted(v_events)
    ui = {x: i for i, x in enumerate(ue)}
    vi = {x: i for i, x in enumerate(ve)}

    # Exact integer 2D difference array. Scores are constant in every open
    # event cell. NumPy performs only integer arithmetic here.
    diff = np.zeros((len(ue), len(ve)), dtype=np.int64)
    for u1, u2, v1, v2, w in rects:
        a, b = ui[u1], ui[u2]
        p, q = vi[v1], vi[v2]
        diff[a, p] += w
        diff[b, p] -= w
        diff[a, q] -= w
        diff[b, q] += w

    scores = diff.cumsum(axis=0).cumsum(axis=1)
    nu, nv = len(ue) - 1, len(ve) - 1

    best = 10**18
    for i in range(nu):
        u0, u1 = ue[i], ue[i + 1]
        if u1 <= u_dom_min or u0 >= u_dom_max:
            continue

        slab = clip_u(dom, u0, True)
        slab = clip_u(slab, u1, False)
        if not slab:
            continue

        vlo = min(v for _, v in slab)
        vhi = max(v for _, v in slab)
        if vhi <= vlo:
            continue

        # This may examine a superset of feasible event cells, which is
        # conservative for a lower-bound verification.
        j0 = max(0, bisect_right(ve, vlo) - 1)
        j1 = min(nv - 1, bisect_left(ve, vhi) - 1)
        if j0 <= j1:
            row_min = int(scores[i, j0:j1 + 1].min())
            best = min(best, row_min)

    if best == 10**18:
        raise RuntimeError("center domain was not enumerated")
    return best


def angle_net() -> list[tuple[F, F]]:
    out: list[tuple[F, F]] = []
    for k in range(KMAX + 1):
        t = T * k / KMAX
        den = 1 + t * t
        c = (1 - t * t) / den
        s = 2 * t / den
        assert c * c + s * s == 1
        out.append((c, s))

    # The final adjacent pair brackets pi/4.
    assert out[-2][1] < out[-2][0]
    assert out[-1][1] >= out[-1][0]

    # If psi_k=2 arctan(t_k), half an adjacent angular gap is
    # arctan(t_{k+1})-arctan(t_k), whose tangent is
    # D/(1+t_k*t_{k+1}) <= D. Therefore every angle in [0,pi/4]
    # is within an error epsilon < D of a net direction.
    for k in range(KMAX):
        t0 = T * k / KMAX
        t1 = T * (k + 1) / KMAX
        tan_half_gap = (t1 - t0) / (1 + t0 * t1)
        assert tan_half_gap <= D

    return out


def main() -> None:
    atoms = build_atoms()
    total = sum(w for _, _, w in atoms)

    print(f"atoms = {len(atoms)}")
    print(
        f"total_weight = {total}/{WEIGHT_SCALE}"
        f" = {total / WEIGHT_SCALE:.4f}"
    )
    assert len(atoms) == 268
    assert total == 169476
    assert total < 17 * WEIGHT_SCALE

    net = angle_net()

    # For an orientation error epsilon <= D,
    # cos(epsilon)+sin(epsilon) <= 1+epsilon <= 1+D.
    contain = B * (1 + D)
    print(f"angle_net_size = {len(net)}")
    print(f"b*(1+d) = {contain} = {float(contain):.12f} < 1")
    assert contain < 1

    global_min = 10**18
    argmin = -1
    for k, (c, s) in enumerate(net):
        m = verify_orientation(c, s, atoms)
        if m < global_min:
            global_min, argmin = m, k
        if k % 30 == 0 or k == KMAX:
            print(
                f"orientation {k:3d}/{KMAX}: "
                f"min={m}/{WEIGHT_SCALE}, "
                f"global={global_min}/{WEIGHT_SCALE}"
            )

    print(
        f"minimum_score = {global_min}/{WEIGHT_SCALE}"
        f" = {global_min / WEIGHT_SCALE:.4f} at k={argmin}"
    )
    assert global_min >= WEIGHT_SCALE

    print("CERTIFICATE CONDITIONS VERIFIED.")
    print("By the scaling argument: s(17) >= 44811/10000 = 4.4811.")


if __name__ == "__main__":
    main()
