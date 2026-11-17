"""Sides, extents, prints, house gaps, and the certificates against their 80-digit points.

Usage (from packing/, Python 3.14):
  python -I sides_and_kkt.py CANDIDATES_DIR HOUSES_DIR OUT.json

Reads, as data: the 13 certificate files (cert_reader), the six .exact.txt 80-digit
points, the six *_regularized.json 'packing' blocks, the seven .input.txt binary64
inputs, and main's seven house witnesses (Witness/v2 YAML) plus T-257's s260 and s293
certificates. Decides nothing about feasibility (decide_feasibility.py does); it
measures:
  * each header side against the claim fraction and the issue's prints, and its
    12-place round-up;
  * each file's extent (the corners' bounding box) against its side;
  * the KKT certificates against (1 + 10^-20) times their 80-digit points (side,
    centres, and angles through t = tan(theta/2) at 120 digits);
  * each regularized view against (1 + 10^-20) times its JSON's regularized point, and
    that point's box against S*;
  * the 260 certificate against its binary64 input;
  * each new side against the house side on main, exactly.
"""

from __future__ import annotations

import json
import math
import re
import sys
from fractions import Fraction as F
from pathlib import Path

import mpmath
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

import exact_geometry as eg  # noqa: E402
from cert_reader import read_cert  # noqa: E402

mpmath.mp.dps = 120

NAMES = {
    175: "s175_1105",
    204: "s204_trig1",
    260: "s260_ks_1105",
    268: "s268_1105",
    293: "s293_1105",
    303: "s303_1105",
    304: "s304_1105",
}
# The claim fractions as the brief (bead think-lrj4) states them.
CLAIMED = {
    175: F(13764050051543175143919941166751, 10**30),
    204: F(7402180691825929362760144937013, 5 * 10**29),
    260: F(8316760475444266760475435949833, 5 * 10**29),
    268: F(2109062439766878830759866953431, 125 * 10**27),
    293: F(17623065212060701770633564247069, 10**30),
    303: F(17901832750854048761575294038467, 10**30),
    304: F(17920944093340242061198022152503, 10**30),
}
# Issue #914 (body as fetched 2026-11-05): the 12-place prints, the S' prints, the S* prints,
# and the "best public bound before it" column.
ISSUE_12 = {
    175: "13.764050051544",
    204: "14.804361383652",
    260: "16.633520950889",
    268: "16.872499518136",
    293: "17.623065212061",
    303: "17.901832750855",
    304: "17.920944093341",
}
ISSUE_SPRIME = {
    175: "13.764050051543175143919941166751",
    204: "14.804361383651858725520289874026",
    260: "16.633520950888535",
    268: "16.872499518135030646078935627448",
    293: "17.623065212060701770633564247069",
    303: "17.901832750854048761575294038467",
    304: "17.920944093340242061198022152503",
}
ISSUE_SSTAR = {
    175: "13.764050051543175143782",
    204: "14.804361383651858725372",
    268: "16.872499518135030645910",
    293: "17.623065212060701770457",
    303: "17.901832750854048761396",
    304: "17.920944093340242061018",
}
ISSUE_BEFORE = {
    175: "13.764174317487",
    204: "14.807620995586",
    260: "16.633982501923",
    268: "16.874361715870",
    293: "17.633982502123",
    303: "17.906978233799",
    304: "17.926898900357",
}
ISSUE_IMPROVEMENT = {175: "1.24e-4", 204: "3.26e-3", 260: "4.62e-4", 268: "1.86e-3", 293: "1.09e-2", 303: "5.15e-3", 304: "5.95e-3"}
HOUSE_T = {175: "T-186", 204: "T-264", 260: "T-265", 268: "T-242", 293: "T-257", 303: "T-240", 304: "T-242"}

DEC = re.compile(r"-?[0-9]+(\.[0-9]+)?([eE][-+]?[0-9]+)?\Z")
D20 = 1 + F(1, 10**20)
FL_1EM12 = F(1e-12)  # the binary64 value of 1e-12, exactly


def dec(s: str) -> F:
    if not DEC.match(s):
        raise ValueError(s)
    return F(s)


def fs(v: F) -> str:
    return f"{v.numerator}/{v.denominator}"


def sci(v) -> str:
    v = F(v)
    if v == 0:
        return "0"
    return mpmath.nstr(mpmath.mpf(v.numerator) / v.denominator, 6)


def round_up(v: F, places: int) -> str:
    scale = 10**places
    k = -((-v.numerator * scale) // v.denominator)  # ceil
    sign = "-" if k < 0 else ""
    k = abs(k)
    return f"{sign}{k // scale}.{k % scale:0{places}d}"


def decimals(v: F, places: int) -> str:
    """Truncated decimal expansion (v > 0)."""
    scale = 10**places
    k = (v.numerator * scale) // v.denominator
    return f"{k // scale}.{k % scale:0{places}d}"


def extent(cert: dict) -> dict:
    side = cert["S"]
    xs, ys = [], []
    for (x, y, t) in cert["squares"]:
        corners, _ = eg.square_a(x, y, t)
        xs += [p[0] for p in corners]
        ys += [p[1] for p in corners]
    xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)
    return {
        "xmin": sci(xmin),
        "ymin": sci(ymin),
        "S_minus_xmax": sci(side - xmax),
        "S_minus_ymax": sci(side - ymax),
        "extent_x": sci(xmax - xmin),
        "extent_y": sci(ymax - ymin),
        "S_minus_extent_max": sci(side - max(xmax - xmin, ymax - ymin)),
        "max_corner_coordinate": decimals(max(xmax, ymax), 40),
        "side_equals_max_corner": side == max(xmax, ymax),
        "S_minus_max_corner": fs(side - max(xmax, ymax)),
        "S_minus_max_corner_sci": sci(side - max(xmax, ymax)),
        "min_corner_coordinate_sci": sci(min(xmin, ymin)),
    }


def read_points(path: Path) -> tuple[int, F, list[tuple[F, F, F]]]:
    rows = path.read_text().split("\n")
    rows = [r for r in rows if r.strip()]
    n_str, s_str = rows[0].split()
    pts = []
    for r in rows[1:]:
        a, b, c = r.split()
        pts.append((dec(a), dec(b), dec(c)))
    if len(pts) != int(n_str):
        raise ValueError("count")
    return int(n_str), dec(s_str), pts


def theta_deg_of_t(t: F):
    return 2 * mpmath.degrees(mpmath.atan(mpmath.mpf(t.numerator) / t.denominator))


def ang_diff(a, b):
    """Difference of two angles in degrees, reduced modulo 360 into (-180, 180]."""
    d = (a - b) % 360
    if d > 180:
        d -= 360
    return d


def house_side(path: Path) -> F:
    doc = yaml.load(path.read_text(), Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
    s = str(doc["witness"]["side"])
    p, _, q = s.partition("/")
    return F(int(p), int(q or 1))


def main() -> None:
    cand = Path(sys.argv[1])
    houses = Path(sys.argv[2])
    out_path = Path(sys.argv[3])
    result: dict = {"counts": {}}
    for n, name in NAMES.items():
        r: dict = {}
        cert = read_cert(cand / f"{name}.cert")
        side = cert["S"]
        r["file"] = f"{name}.cert"
        r["sha256"] = cert["sha256"]
        r["n_ok"] = cert["n"] == n == len(cert["squares"])
        r["header_side"] = fs(side)
        r["header_side_40_places"] = decimals(side, 40)
        r["equals_claimed_fraction"] = side == CLAIMED[n]
        r["round_up_12"] = round_up(side, 12)
        r["round_up_12_equals_issue"] = round_up(side, 12) == ISSUE_12[n]
        sp = ISSUE_SPRIME[n]
        r["issue_S_prime_print"] = sp
        r["issue_S_prime_equals_header"] = dec(sp) == side
        r["issue_S_prime_minus_header"] = sci(dec(sp) - side)
        r["extent"] = extent(cert)
        # against the house on main
        hs = house_side(houses / f"W-known-best-n{n}.yaml")
        r["house"] = HOUSE_T[n]
        r["house_side"] = fs(hs)
        r["house_side_20_places"] = decimals(hs, 20)
        r["house_round_up_12"] = round_up(hs, 12)
        r["issue_before_print"] = ISSUE_BEFORE[n]
        r["issue_before_equals_house_round_up"] = round_up(hs, 12) == ISSUE_BEFORE[n]
        r["house_minus_new"] = fs(hs - side)
        r["house_minus_new_sci"] = sci(hs - side)
        r["relative_improvement_sci"] = sci((hs - side) / hs)
        r["issue_improvement_print"] = ISSUE_IMPROVEMENT[n]
        # KKT points
        exact = cand / f"{name}.exact.txt"
        if exact.exists():
            m, sstar, pts = read_points(exact)
            k: dict = {"n_ok": m == n}
            k["S_star_80"] = decimals(sstar, 60)
            k["issue_S_star_print_is_prefix"] = decimals(sstar, 60).startswith(ISSUE_SSTAR[n])
            k["S_prime_minus_dilated_S_star"] = sci(side - D20 * sstar)
            k["S_prime_minus_dilated_S_star_in_0_1e-30"] = 0 <= side - D20 * sstar < F(1, 10**30)
            k["S_prime_minus_S_star"] = sci(side - sstar)
            dx = max(max(abs(x - D20 * px), abs(y - D20 * py)) for (x, y, _), (px, py, _) in zip(cert["squares"], pts))
            k["max_centre_minus_dilated_point"] = sci(dx)
            da = max(abs(ang_diff(theta_deg_of_t(t), mpmath.mpf(pa.numerator) / pa.denominator)) for (_, _, t), (_, _, pa) in zip(cert["squares"], pts))
            k["max_angle_difference_degrees"] = mpmath.nstr(da, 6)
            r["kkt"] = k
        # regularized view
        view = cand / f"{name}_regularized.cert"
        if view.exists():
            vc = read_cert(view)
            v: dict = {"file": view.name, "sha256": vc["sha256"], "n_ok": vc["n"] == n}
            v["side_equals_certificate_side"] = vc["S"] == side
            v["extent"] = extent(vc)
            js = json.loads((cand / f"{name}_regularized.json").read_text())
            pk = js["packing"]
            sreg = dec(pk["S"])
            v["json_S_cert_equals_header"] = js.get("S_cert") == fs(side)
            v["regularized_point_S"] = decimals(sreg, 50)
            if exact.exists():
                v["regularized_S_minus_S_star"] = sci(sreg - sstar)
                v["dilated_regularized_S_le_S_prime"] = D20 * sreg <= side
            pts_v = [(dec(a), dec(b), dec(c)) for a, b, c in pk["sq"]]
            v["regularized_point_count_ok"] = len(pts_v) == n
            dxv = max(max(abs(x - D20 * px), abs(y - D20 * py)) for (x, y, _), (px, py, _) in zip(vc["squares"], pts_v))
            v["max_centre_minus_dilated_regularized_point"] = sci(dxv)
            dav = max(abs(ang_diff(theta_deg_of_t(t), mpmath.mpf(pa.numerator) / pa.denominator)) for (_, _, t), (_, _, pa) in zip(vc["squares"], pts_v))
            v["max_angle_difference_degrees"] = mpmath.nstr(dav, 6)
            v["json_level_text"] = js.get("level_text")
            v["json_S_grow"] = js.get("S_grow")
            r["view"] = v
        # the binary64 input
        m, s_in, pin = read_points(cand / f"{name}.input.txt")
        inp: dict = {"n_ok": m == n, "S_input": decimals(s_in, 20)}
        inp["S_prime_over_S_input_minus_1"] = sci(side / s_in - 1)
        inp["S_prime_minus_S_input"] = sci(side - s_in)
        inp["S_prime_equals_ceil30_of_S_input_times_1_plus_fl_1e-12"] = round_up(s_in * (1 + FL_1EM12), 30) == decimals(side, 30)
        # the input's own extent and wall clearance, at 120 digits
        lo = mpmath.mpf("inf")
        hi = mpmath.mpf("-inf")
        for (x, y, a) in pin:
            th = mpmath.radians(mpmath.mpf(a.numerator) / a.denominator)
            c, s = mpmath.cos(th), mpmath.sin(th)
            X, Y = mpmath.mpf(x.numerator) / x.denominator, mpmath.mpf(y.numerator) / y.denominator
            for sa, sb in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
                px = X + (sa * c - sb * s) / 2
                py = Y + (sa * s + sb * c) / 2
                lo = min(lo, px, py)
                hi = max(hi, px, py)
        inp["input_min_corner_coordinate"] = mpmath.nstr(lo, 8)
        inp["input_max_corner_coordinate"] = mpmath.nstr(hi, 20)
        inp["S_prime_minus_input_max_corner"] = mpmath.nstr(mpmath.mpf(side.numerator) / side.denominator - hi, 8)
        inp["S_input_minus_input_max_corner"] = mpmath.nstr(mpmath.mpf(s_in.numerator) / s_in.denominator - hi, 8)
        dmax = max(max(abs(x - px), abs(y - py)) for (x, y, _), (px, py, _) in zip(cert["squares"], pin))
        inp["max_centre_minus_input"] = sci(dmax)
        if n == 260:
            # fit x' = alpha x_in + beta from squares 1 and the one with the largest x_in
            pairs = list(zip(cert["squares"], pin))
            (c1, p1) = pairs[0]
            (c2, p2) = max(pairs, key=lambda q: q[1][0])
            alpha = (c2[0] - c1[0]) / (p2[0] - p1[0])
            beta = c1[0] - alpha * p1[0]
            resid = max(abs(c[0] - (alpha * p[0] + beta)) for c, p in pairs)
            residy = max(abs(c[1] - (alpha * p[1] + beta)) for c, p in pairs)
            inp["fit_alpha_minus_1"] = sci(alpha - 1)
            inp["fit_beta"] = sci(beta)
            inp["fit_max_residual_x"] = sci(resid)
            inp["fit_max_residual_y_same_map"] = sci(residy)
            inp["dilation_1_plus_fl_1e-12_residual_x"] = sci(max(abs(c[0] - (1 + FL_1EM12) * p[0]) for c, p in pairs))
            inp["dilation_1_plus_fl_1e-12_residual_y"] = sci(max(abs(c[1] - (1 + FL_1EM12) * p[1]) for c, p in pairs))
            inp["dilation_1_plus_1e-12_residual_x"] = sci(max(abs(c[0] - (1 + F(1, 10**12)) * p[0]) for c, p in pairs))
            da = max(abs(ang_diff(theta_deg_of_t(c[2]), mpmath.mpf(p[2].numerator) / p[2].denominator)) % 90 for c, p in pairs)
            inp["max_angle_difference_mod_90_degrees"] = mpmath.nstr(min(da, 90 - da) if da > 45 else da, 6)
        r["input"] = inp
        result["counts"][str(n)] = r
    # T-257's certificates at 260 and 293 (for 260's lineage)
    for label, fn in (("T-257 s260_1028", "T-257-s260_1028.cert"), ("T-257 s293_1028", "T-257-s293_1028.cert")):
        c = read_cert(houses / fn)
        result[label] = {"sha256": c["sha256"], "n": c["n"], "side": fs(c["S"]), "side_20": decimals(c["S"], 30)}
    t257_260 = read_cert(houses / "T-257-s260_1028.cert")["S"]
    new260 = read_cert(cand / "s260_ks_1105.cert")["S"]
    result["T-257 s260 minus new 260"] = sci(t257_260 - new260)
    out_path.write_text(json.dumps(result, indent=1, default=str) + "\n")
    for n in NAMES:
        r = result["counts"][str(n)]
        print(n, "claimed", r["equals_claimed_fraction"], "12up", r["round_up_12"], r["round_up_12_equals_issue"],
              "S'print", r["issue_S_prime_equals_header"], r["issue_S_prime_minus_header"],
              "| house", r["house"], r["house_minus_new_sci"], "rel", r["relative_improvement_sci"],
              "before==", r["issue_before_equals_house_round_up"], r["house_round_up_12"])
        print("    extent", {k: r["extent"][k] for k in ("xmin", "ymin", "S_minus_xmax", "S_minus_ymax", "side_equals_max_corner", "S_minus_max_corner_sci")})
        if "kkt" in r:
            print("    kkt", r["kkt"])
        if "view" in r:
            v = r["view"]
            print("    view", {k: v[k] for k in v if k not in ("extent", "json_level_text", "sha256")})
            print("    view extent", {k: v["extent"][k] for k in ("xmin", "ymin", "S_minus_xmax", "S_minus_ymax", "S_minus_max_corner_sci")})
        print("    input", r["input"])
    print({k: v for k, v in result.items() if k != "counts"})


if __name__ == "__main__":
    main()
