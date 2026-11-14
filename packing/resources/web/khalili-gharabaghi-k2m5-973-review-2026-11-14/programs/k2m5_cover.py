"""Clean-room checks of the k^2 - 5 board and family (review of issue #973, lane L144).

Written for this review from the paper's Definition 3, Lemma 6 and Lemma 7; it imports no
code of the source or of evand/square-packing.  Exact rational arithmetic throughout.

usage: python -I k2m5_cover.py BOARD FAMILY SOL_JSON OUT_JSON

Checks:
  1. the board: side 11, pitch 1/10, segment shape, weights, the Lebesgue square;
  2. its exact total, D = (121 - total)/4, D against sol_exact.json and against 5/4;
  3. D4 invariance as a measure (canonical elementary pieces, weights summed);
  4. mu_k built from the family file by Definition 3, for k = 10..40: built mu_11 equals
     the board; D4 invariance for k = 10..20; total = k^2 - 4D for every k;
  5. the premises the proof of Lemma 7 uses (elementary pieces on the 1/10 grid, nu in
     [0,R]^2 and diagonal-symmetric, omega_0 in [0,1] x [0,R] and mirror-symmetric);
  6. the window identity of Lemma 7 for k = 10, 12, 13, 14, 20, 25: for every pair of
     x- and y-windows of the lemma's three cases, mu_k on the window equals the
     translate of mu_11 on the shifted window.
"""
import json
import sys
from fractions import Fraction as F

R10 = 40          # R = 4, in tenths
A10 = 38          # Lebesgue edge 19/5, in tenths


def read_board(path):
    lines = open(path).read().split("\n")
    i = 0
    while not lines[i].split() or lines[i].startswith("#") or lines[i].startswith("mixed"):
        i += 1
    sn, sd = map(int, lines[i].split())
    pitch = int(lines[i + 1])
    wden = int(lines[i + 2])
    npts = int(lines[i + 3])
    nseg = int(lines[i + 4])
    segs = [tuple(map(int, lines[i + 5 + j].split())) for j in range(nseg)]
    rest = [ln for ln in lines[i + 5 + nseg:] if ln.strip()]
    npoly = int(rest[0])
    polys = [list(map(int, rest[1 + j].split())) for j in range(npoly)]
    extra = rest[1 + npoly:]
    return dict(side=F(sn, sd), pitch=pitch, wden=wden, npts=npts, segs=segs, polys=polys, extra=extra)


def key_of(x0, y0, x1, y1):
    """canonical elementary piece: ('h', y, xmin) or ('v', x, ymin), tenths"""
    if y0 == y1 and abs(x1 - x0) == 1:
        return ("h", y0, min(x0, x1))
    if x0 == x1 and abs(y1 - y0) == 1:
        return ("v", x0, min(y0, y1))
    raise ValueError(f"not an elementary 1/10 piece: {(x0, y0, x1, y1)}")


def ends_of(key):
    o, line, s = key
    return ((s, line), (s + 1, line)) if o == "h" else ((line, s), (line, s + 1))


def add(meas, key, w):
    meas[key] = meas.get(key, F(0)) + w


def transform(meas, g):
    out = {}
    for key, w in meas.items():
        (a, b) = ends_of(key)
        p, q = g(*a), g(*b)
        add(out, key_of(p[0], p[1], q[0], q[1]), w)
    return out


def d4_maps(n10):
    return [
        lambda x, y: (x, y), lambda x, y: (n10 - x, y), lambda x, y: (x, n10 - y),
        lambda x, y: (n10 - x, n10 - y), lambda x, y: (y, x), lambda x, y: (n10 - y, x),
        lambda x, y: (y, n10 - x), lambda x, y: (n10 - y, n10 - x),
    ]


def read_family(path):
    prof, corner = [], []
    for ln in open(path):
        t = ln.split()
        if not t or t[0].startswith("#"):
            continue
        tag = t[0]
        vals = [F(v) for v in t[1:]]
        if tag in ("h", "v"):
            prof.append((tag, vals))
        elif tag in ("H", "V"):
            corner.append((tag, vals))
        else:
            raise ValueError(ln)
    return prof, corner


def tenths(v):
    t = v * 10
    if t.denominator != 1:
        raise ValueError(f"not on the 1/10 grid: {v}")
    return int(t)


def family_pieces(prof, corner):
    """omega_0 pieces as (x0, y0, x1, y1, w) in tenths with x along the wall, y = depth; nu likewise"""
    om, nu = [], []
    for tag, v in prof:
        if tag == "h":           # h y phase0 phase1 mass
            y, p0, p1, m = v
            om.append((tenths(p0), tenths(y), tenths(p1), tenths(y), m))
        else:                    # v phase y0 y1 mass
            ph, y0, y1, m = v
            om.append((tenths(ph), tenths(y0), tenths(ph), tenths(y1), m))
    for tag, v in corner:
        if tag == "H":           # H y x0 x1 mass
            y, x0, x1, m = v
            nu.append((tenths(x0), tenths(y), tenths(x1), tenths(y), m))
        else:                    # V x y0 y1 mass
            x, y0, y1, m = v
            nu.append((tenths(x), tenths(y0), tenths(x), tenths(y1), m))
    return om, nu


def premises(om, nu):
    r = {}
    r["omega0_pieces"] = len(om)
    r["nu_pieces"] = len(nu)
    r["all_elementary"] = all(abs(x1 - x0) + abs(y1 - y0) == 1 for x0, y0, x1, y1, _ in om + nu)
    r["all_weights_positive"] = all(w > 0 for *_, w in om + nu)
    r["omega0_start_phase_in_0_1"] = all(0 <= min(x0, x1) < 10 for x0, _, x1, _, _ in om)
    r["omega0_depth_in_0_R"] = all(0 <= min(y0, y1) and max(y0, y1) <= R10 for _, y0, _, y1, _ in om)
    r["nu_in_0_R_square"] = all(0 <= min(x0, x1, y0, y1) and max(x0, x1, y0, y1) <= R10 for x0, y0, x1, y1, _ in nu)
    # nu invariant under (x, y) -> (y, x)
    m_nu = {}
    for x0, y0, x1, y1, w in nu:
        add(m_nu, key_of(x0, y0, x1, y1), w)
    r["nu_diagonal_symmetric"] = transform(m_nu, lambda x, y: (y, x)) == m_nu
    # omega periodic extension is invariant under x -> -x: compare one period mod 1 (tenths mod 10)
    def per(pieces, mirror):
        out = {}
        for x0, y0, x1, y1, w in pieces:
            if mirror:
                x0, x1 = -x0, -x1
            k = key_of(x0, y0, x1, y1)
            o, line, s = k
            k = (o, line, s % 10) if o == "h" else (o, line % 10, s)
            add(out, k, w)
        return out
    r["omega_mirror_symmetric"] = per(om, False) == per(om, True)
    r["omega0_total"] = str(sum(w for *_, w in om))
    r["nu_total"] = str(sum(w for *_, w in nu))
    return r


def build_mu(om, nu, k):
    n10 = 10 * k
    bottom = {}
    for m in range(-1, k + 1):
        for x0, y0, x1, y1, w in om:
            a, b = x0 + 10 * m, x1 + 10 * m
            if R10 <= min(a, b) and max(a, b) <= n10 - R10:
                add(bottom, key_of(a, y0, b, y1), w)
    meas = {}
    for g in (lambda x, y: (x, y), lambda x, y: (y, x), lambda x, y: (x, n10 - y), lambda x, y: (n10 - y, x)):
        for key, w in transform(bottom, g).items():
            add(meas, key, w)
    corner = {}
    for x0, y0, x1, y1, w in nu:
        add(corner, key_of(x0, y0, x1, y1), w)
    for g in (lambda x, y: (x, y), lambda x, y: (n10 - x, y), lambda x, y: (x, n10 - y), lambda x, y: (n10 - x, n10 - y)):
        for key, w in transform(corner, g).items():
            add(meas, key, w)
    leb = (A10, n10 - A10)  # [19/5, k - 19/5]^2 in tenths
    return meas, leb


def total(meas, leb):
    side = F(leb[1] - leb[0], 10)
    return sum(meas.values(), F(0)) + side * side


def windows(k):
    """the lemma's per-axis windows in tenths: (lo, hi, lo_open, hi_open, shift)"""
    n10 = 10 * k
    w = [(0, 55, False, False, 0)]                                   # case L
    for j in range(0, k - 9):                                        # case M, shift j
        w.append((R10 + 10 * j, min(65 + 10 * j, n10 - R10), True, True, 10 * j))
    w.append((n10 - 55, n10, False, False, n10 - 110))               # case H, shift k - 11
    return w


def in_line(v, lo, hi, lo_open, hi_open):
    return (v > lo if lo_open else v >= lo) and (v < hi if hi_open else v <= hi)


def restrict(meas, wx, wy, sx=0, sy=0):
    """pieces of meas in the window wx x wy (shifted by -s), keys translated by +s"""
    (xl, xh, xlo, xho, _), (yl, yh, ylo, yho, _) = wx, wy
    xl, xh, yl, yh = xl - sx, xh - sx, yl - sy, yh - sy
    out = {}
    for (o, line, s), w in meas.items():
        if o == "h":
            ok = in_line(line, yl, yh, ylo, yho) and xl <= s and s + 1 <= xh
            key = ("h", line + sy, s + sx)
        else:
            ok = in_line(line, xl, xh, xlo, xho) and yl <= s and s + 1 <= yh
            key = ("v", line + sx, s + sy)
        if ok:
            add(out, key, w)
    return out


def leb_restrict(leb, wx, wy, sx=0, sy=0):
    a, b = leb
    x0, x1 = max(a, wx[0] - sx), min(b, wx[1] - sx)
    y0, y1 = max(a, wy[0] - sy), min(b, wy[1] - sy)
    if x0 >= x1 or y0 >= y1:
        return None
    return (x0 + sx, x1 + sx, y0 + sy, y1 + sy)


def window_check(om, nu, k, mu11, leb11, mutate=None):
    mk, lebk = build_mu(om, nu, k)
    if mutate is not None:          # self-control: change one weight of mu_k
        key = mutate(mk)
        mk[key] = mk[key] * 2
    ws = windows(k)
    bad = []
    n = 0
    compared = 0
    for wx in ws:
        rx = restrict(mk, wx, (0, 10 * k, False, False, 0))   # prefilter by x
        for wy in ws:
            n += 1
            a = restrict(rx, (0, 10 * k, False, False, 0), wy)
            # mu_11 on the window shifted by -(m1, m2), its pieces translated back by +(m1, m2)
            b = restrict(mu11, wx, wy, wx[4], wy[4])
            la = leb_restrict(lebk, wx, wy)
            lb = leb_restrict(leb11, wx, wy, wx[4], wy[4])
            compared += len(a)
            if a != b or la != lb:
                bad.append((wx, wy, len(a), len(b), la, lb))
    return dict(k=k, window_pairs=n, pieces_compared=compared, mismatches=len(bad), first=[str(x) for x in bad[:3]])


def main():
    board_path, fam_path, sol_path, out_path = sys.argv[1:5]
    bd = read_board(board_path)
    res = {}
    segs = bd["segs"]
    res["board"] = dict(side=str(bd["side"]), pitch=bd["pitch"], wden=bd["wden"], points=bd["npts"],
                        segments=len(segs), polygons=bd["polys"], trailing_lines=len(bd["extra"]))
    wden = bd["wden"]
    meas = {}
    for x0, y0, x1, y1, w in segs:
        add(meas, key_of(x0, y0, x1, y1), F(w, wden))
    res["board"]["distinct_pieces"] = len(meas)
    res["board"]["repeated_pieces"] = len(segs) - len(meas)
    res["board"]["min_weight"] = str(min(F(s[4], wden) for s in segs))
    res["board"]["weights_positive"] = all(s[4] > 0 for s in segs)
    res["board"]["inside_container"] = all(0 <= min(s[:4]) and max(s[:4]) <= 110 for s in segs)
    poly = bd["polys"][0]
    assert len(bd["polys"]) == 1 and poly[0] == 4
    xs, ys = poly[2::2], poly[3::2]
    rect = (min(xs), max(xs), min(ys), max(ys))
    area = F(rect[1] - rect[0], 10) * F(rect[3] - rect[2], 10)
    res["board"]["lebesgue_rect_tenths"] = rect
    res["board"]["lebesgue_density"] = str(F(poly[1], wden) / area)
    leb11 = (rect[0], rect[1])
    assert rect[0] == rect[2] and rect[1] == rect[3]
    tot = sum(meas.values(), F(0)) + F(poly[1], wden)
    D = (121 - tot) / 4
    Djson = F(json.load(open(sol_path))["D"])
    res["total"] = str(tot)
    res["D"] = str(D)
    res["D_float"] = float(D)
    res["D_equals_sol_json"] = D == Djson
    res["D_gt_5_4"] = D > F(5, 4)
    res["slack_below_k2_minus_5_per_k"] = str(4 * D - 5)
    # D4 as a measure
    res["board_d4_invariant"] = all(transform(meas, g) == meas for g in d4_maps(110))
    # family
    prof, corner = read_family(fam_path)
    om, nu = family_pieces(prof, corner)
    res["premises"] = premises(om, nu)
    mu11, lebb = build_mu(om, nu, 11)
    res["built_mu11_equals_board"] = (mu11 == meas) and (lebb == leb11) and (F(poly[1], wden) / area == 1)
    totals = {}
    for k in range(10, 41):
        mk, lebk = build_mu(om, nu, k)
        totals[k] = total(mk, lebk) == k * k - 4 * D
        if k <= 20:
            res.setdefault("built_d4_invariant", {})[k] = all(transform(mk, g) == mk for g in d4_maps(10 * k))
    res["totals_equal_k2_minus_4D_k10_to_40"] = all(totals.values())
    res["omega0_total_equals_19_5"] = F(res["premises"]["omega0_total"]) == F(19, 5)
    res["windows"] = [window_check(om, nu, k, mu11, leb11) for k in (10, 12, 13, 14, 20, 25)]
    # self-control: one band piece of mu_12 (bottom wall, x in [6.0, 6.1], depth 1) with its weight doubled
    def pick(mk):
        return next(kk for kk in sorted(mk) if kk[0] == "h" and kk[1] == 10 and kk[2] == 60)
    res["window_self_control_k12"] = window_check(om, nu, 12, mu11, leb11, mutate=pick)
    json.dump(res, open(out_path, "w"), indent=1, default=str)
    print(json.dumps(res, indent=1, default=str))


if __name__ == "__main__":
    main()
