"""How the rational corners were made, and the decimal pose behind them (lane L72, bead think-qqyg).

Usage: python -I -B l72_construct.py STATEMENTS.json COUNT SRC CHECK.json OUT.json

Measures the certificate exactly (read by the frozen reader): its angles and half-angle
heights, every square-wall clearance, the pair margins below 1e-9 and, for the pairs below
1e-12, the margin over the centres' separation along the separating axis (what a uniform
scaling would leave). Then compares the certificate with the author's decimal pose
(centre and angle per square, in degrees) at 60 significant digits with mpmath: the pose's
corners, translated so its least corner coordinates are 0, against the certificate's centres
and edge directions, and the pose's own margins on the near pairs against the certificate's
exact ones, and the pose's own wall clearances at its own side. Decides no bound; the pose
measurements are numerical.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fractions import Fraction  # noqa: E402

import mpmath  # noqa: E402

import l72_reader as reader  # noqa: E402
import l72_sat as sat  # noqa: E402
import l72_util as util  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
mpmath.mp.dps = 60


def mpf_of(x):
    x = Fraction(x)
    return mpmath.mpf(x.numerator) / x.denominator


def bucket(x, edges):
    for lo, hi, name in edges:
        if lo <= x < hi:
            return name
    return "other"


def pose_squares(path):
    tree = reader.yaml_tree(open(path, encoding="utf-8").read())
    w = tree["witness"]
    assert w["representation"] == "center-angle" and w["coordinates"]["angle_unit"] == "degrees"
    out = []
    for sq in w["squares"]:
        cx, cy = (mpmath.mpf(v) for v in sq["center"])
        th = mpmath.radians(mpmath.mpf(sq["angle"]))
        u = (mpmath.cos(th), mpmath.sin(th))
        f = (-u[1], u[0])
        p0 = (cx - u[0] / 2 - f[0] / 2, cy - u[1] / 2 - f[1] / 2)
        P = [p0, (p0[0] + u[0], p0[1] + u[1]), (p0[0] + u[0] + f[0], p0[1] + u[1] + f[1]), (p0[0] + f[0], p0[1] + f[1])]
        out.append({"id": int(sq["id"]), "centre": (cx, cy), "u": u, "corners": P, "angle_deg": mpmath.mpf(sq["angle"])})
    return out, mpmath.mpf(w["side"])


def mp_margin(Pi, ui, Pj, uj):
    best = None
    for a in (ui, (-ui[1], ui[0]), uj, (-uj[1], uj[0])):
        pi = [p[0] * a[0] + p[1] * a[1] for p in Pi]
        pj = [p[0] * a[0] + p[1] * a[1] for p in Pj]
        g = max(min(pj) - max(pi), min(pi) - max(pj))
        if best is None or g > best:
            best = g
    return best


def main(argv):
    statements = json.load(open(argv[1]))
    count = argv[2]
    src, check_path, out = argv[3], argv[4], argv[5]
    st = statements[count]
    repo = os.path.join(src, st["repository"].split("/")[1])
    data = reader.read_files(os.path.join(repo, st["certificate"]))
    rc = json.load(open(check_path))
    n = data["n"]
    ids = data["ids"]
    S = Fraction(*data["side"])
    P = [sat.corners_frac(c) for c in data["corners"]]
    axes = [sat.square(x)[2] for x in P]
    report = {
        "program": "l72_construct.py",
        "lane": "L72",
        "bead": "think-qqyg",
        "count": count,
        "environment": util.environment(),
        "program_digests": util.program_digests([os.path.join(HERE, f) for f in ("l72_construct.py", "l72_reader.py", "l72_sat.py", "l72_util.py")]),
        "certificate_block": data["meta"]["certificate"],
        "source_block": data["meta"]["source"],
    }
    # angles
    cats = {"exactly_on_the_axes": 0, "below_1e-9_rad": 0, "1e-9_rad_to_0.5deg": 0, "beyond_0.5deg": 0}
    small_turns = []
    t_digits = []
    half_deg = mpmath.radians(mpmath.mpf("0.5"))
    for (u, _) in axes:
        if u[0] == 0 or u[1] == 0:
            cats["exactly_on_the_axes"] += 1
            continue
        ang = abs(mpmath.atan2(mpf_of(u[1]), mpf_of(u[0])))
        ang = ang % (mpmath.pi / 2)
        ang = min(ang, mpmath.pi / 2 - ang)
        if ang < mpmath.mpf("1e-9"):
            cats["below_1e-9_rad"] += 1
            small_turns.append(ang)
        elif ang <= half_deg:
            cats["1e-9_rad_to_0.5deg"] += 1
        else:
            cats["beyond_0.5deg"] += 1
        # half-angle height of the listed edge direction
        t = u[1] / (1 + u[0]) if u[0] != -1 else None
        if t is not None:
            t_digits.append((len(str(abs(t.numerator))), len(str(t.denominator))))
    report["angles"] = {
        "categories": cats,
        "below_1e-9_rad_range": [mpmath.nstr(min(small_turns), 3), mpmath.nstr(max(small_turns), 3)] if small_turns else None,
        "half_angle_numerator_digits_max": max(d[0] for d in t_digits) if t_digits else None,
        "half_angle_denominator_digits_max": max(d[1] for d in t_digits) if t_digits else None,
    }
    # walls
    edges = [
        (Fraction(0), Fraction(0), "zero"),
        (Fraction(0), Fraction(1, 10**15), "(0, 1e-15)"),
        (Fraction(1, 10**15), Fraction(1, 10**13), "[1e-15, 1e-13)"),
        (Fraction(1, 10**13), Fraction(1, 10**12), "[1e-13, 1e-12)"),
        (Fraction(1, 10**12), Fraction(1, 10**9), "[1e-12, 1e-9)"),
        (Fraction(1, 10**9), Fraction(1, 10**6), "[1e-9, 1e-6)"),
        (Fraction(1, 10**6), Fraction(1, 10**3), "[1e-6, 1e-3)"),
    ]
    wall_hist = {}
    mid = []
    largest_small = None
    for k in range(n):
        for w, c in zip(sat.WALLS, sat.wall_clearances(P[k], S)):
            name = "zero" if c == 0 else bucket(c, edges[1:])
            if name == "other":
                continue
            wall_hist[name] = wall_hist.get(name, 0) + 1
            if 0 < c < Fraction(1, 10**12) and (largest_small is None or c > largest_small[0]):
                largest_small = (c, ids[k], w)
            if Fraction(1, 10**12) <= c < Fraction(1, 10**3):
                mid.append({"id": ids[k], "wall": w, "clearance": util.sci(c, 4)})
    report["walls"] = {
        "histogram": wall_hist,
        "largest_positive_below_1e-12": {"id": largest_small[1], "wall": largest_small[2], "sci": util.sci(largest_small[0], 4)} if largest_small else None,
        "between_1e-12_and_1e-3": sorted(mid, key=lambda r: float(r["clearance"])),
    }
    # pairs below 1e-9, exact, and the implied scaling of those below 1e-12
    own = [sat.own_ranges(P[k], axes[k]) for k in range(n)]
    near = []
    hist = {"[2.0, 2.1)e-13": 0, "[2.1, 3.0)e-13": 0, "[3e-13, 1e-12)": 0, "[1e-12, 1e-9)": 0}
    for i in range(n):
        for j in range(i + 1, n):
            m, ax = sat.pair_margin(P[i], axes[i], own[i], P[j], axes[j], own[j])
            if m < Fraction(1, 10**9):
                hist[bucket(m, [
                    (Fraction(20, 10**14), Fraction(21, 10**14), "[2.0, 2.1)e-13"),
                    (Fraction(21, 10**14), Fraction(30, 10**14), "[2.1, 3.0)e-13"),
                    (Fraction(30, 10**14), Fraction(1, 10**12), "[3e-13, 1e-12)"),
                    (Fraction(1, 10**12), Fraction(1, 10**9), "[1e-12, 1e-9)"),
                ])] += 1
                if m < Fraction(1, 10**12):
                    a = axes[i][ax] if ax < 2 else axes[j][ax - 2]
                    ci = ((P[i][0][0] + P[i][2][0]) / 2, (P[i][0][1] + P[i][2][1]) / 2)
                    cj = ((P[j][0][0] + P[j][2][0]) / 2, (P[j][0][1] + P[j][2][1]) / 2)
                    sep = abs((cj[0] - ci[0]) * a[0] + (cj[1] - ci[1]) * a[1])
                    near.append((i, j, m, m / sep))
    ratios = sorted(r[3] for r in near)
    report["pairs"] = {
        "below_1e-9_histogram": hist,
        "below_1e-12": len(near),
        "margin_over_axis_separation": {
            "min": util.sci(ratios[0], 4),
            "median": util.sci(ratios[len(ratios) // 2], 4),
            "max": util.sci(ratios[-1], 4),
        },
    }
    # the decimal pose
    pose, pose_side = pose_squares(os.path.join(repo, st["pose"]))
    pid = {p["id"]: p for p in pose}
    ox = min(pt[0] for p in pose for pt in p["corners"])
    oy = min(pt[1] for p in pose for pt in p["corners"])
    max_dc = mpmath.mpf(0)
    max_dth = mpmath.mpf(0)
    for k in range(n):
        p = pid[ids[k]]
        cc = ((P[k][0][0] + P[k][2][0]) / 2, (P[k][0][1] + P[k][2][1]) / 2)
        dc = max(abs(mpf_of(cc[0]) - (p["centre"][0] - ox)), abs(mpf_of(cc[1]) - (p["centre"][1] - oy)))
        max_dc = max(max_dc, dc)
        u = axes[k][0]
        a_cert = mpmath.atan2(mpf_of(u[1]), mpf_of(u[0]))
        a_pose = mpmath.atan2(p["u"][1], p["u"][0])
        d = (a_cert - a_pose) % (mpmath.pi / 2)
        d = min(d, mpmath.pi / 2 - d)
        max_dth = max(max_dth, d)
    worst_margin = mpmath.mpf(0)
    for i, j, m, _ in near:
        a, b = pid[ids[i]], pid[ids[j]]
        Pa = [(x - ox, y - oy) for x, y in a["corners"]]
        Pb = [(x - ox, y - oy) for x, y in b["corners"]]
        pm = mp_margin(Pa, a["u"], Pb, b["u"])
        worst_margin = max(worst_margin, abs(pm - mpf_of(m)))
    pose_cl = []
    for p in pose:
        xs = [pt[0] for pt in p["corners"]]
        ys = [pt[1] for pt in p["corners"]]
        pose_cl.extend([min(xs), pose_side - max(xs), min(ys), pose_side - max(ys)])
    ext_x = max(pt[0] for p in pose for pt in p["corners"]) - ox
    ext_y = max(pt[1] for p in pose for pt in p["corners"]) - oy
    report["pose"] = {
        "file": st["pose"],
        "side": mpmath.nstr(pose_side, 20),
        "least_corner_x": mpmath.nstr(ox, 6),
        "least_corner_y": mpmath.nstr(oy, 6),
        "extent_x_minus_certificate_side": mpmath.nstr(ext_x - mpf_of(S), 6),
        "extent_y_minus_certificate_side": mpmath.nstr(ext_y - mpf_of(S), 6),
        "max_centre_difference_after_translation": mpmath.nstr(max_dc, 4),
        "max_angle_difference_rad": mpmath.nstr(max_dth, 4),
        "near_pairs_compared": len(near),
        "max_margin_difference_on_near_pairs": mpmath.nstr(worst_margin, 4),
        "pose_least_wall_clearance_at_own_side": mpmath.nstr(min(pose_cl), 6),
        "pose_negative_wall_clearances_at_own_side": sum(1 for c in pose_cl if c < 0),
    }
    util.write_receipt(out, report)
    print(json.dumps({k: v for k, v in report.items() if k not in ("environment", "program_digests")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
