"""Decide one rational corner certificate by both methods (lane L72, bead think-qqyg).

Usage: python -I -B l72_check.py CERT.yaml [TWIN.json] OUT.json

Every square, every wall and every pair, with no distance filter: method A (separating
axes in fractions.Fraction) and method B (clipped areas in gmpy2.mpq), which share only
the reader. ACCEPT needs the reader to accept the file, every square to be a unit square
by both methods, every square to lie in [0, S]^2 by both, every pair to have disjoint
interiors by both, and the two methods to give every square, wall and pair the same class.
"""

import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fractions import Fraction  # noqa: E402

from gmpy2 import mpq  # noqa: E402

import l72_clip as clipm  # noqa: E402
import l72_reader as reader  # noqa: E402
import l72_sat as sat  # noqa: E402
import l72_util as util  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKER_FILES = ["l72_util.py", "l72_reader.py", "l72_sat.py", "l72_clip.py", "l72_check.py"]
THRESHOLDS = ["1e-30", "1e-20", "1e-15", "1e-13", "1e-12", "1e-11", "1e-10", "1e-9", "1e-6", "1e-3"]


def _thr(t):
    mant, exp = t.split("e")
    return Fraction(int(mant)) * Fraction(10) ** int(exp)


def decide_data(data, keep_least=40, wall_report_below="1e-9"):
    """Decide a read certificate (the reader's integer output). Returns a receipt dict."""
    n = data["n"]
    p, q = data["side"]
    ids = data["ids"]
    S_A = Fraction(p, q)
    S_B = mpq(p, q)
    PA = [sat.corners_frac(c) for c in data["corners"]]
    PB = [clipm.corners_q(c) for c in data["corners"]]

    problems = []
    # Squares
    sqA = [sat.square(P) for P in PA]
    sqB = [clipm.square(P) for P in PB]
    unitA = sum(1 for r in sqA if r[0])
    unitB = sum(1 for r in sqB if r[0])
    orient_disagree = [ids[i] for i in range(n) if sqA[i][0] and sqB[i][0] and sqA[i][1] != sqB[i][1]]
    not_unit = [
        {"id": ids[i], "A": sqA[i][3], "B": sqB[i][2]} for i in range(n) if not (sqA[i][0] and sqB[i][0])
    ]
    unit_class_disagree = [ids[i] for i in range(n) if sqA[i][0] != sqB[i][0]]
    if not_unit:
        problems.append(f"{len(not_unit)} squares are not unit squares by both methods")
    if unit_class_disagree or orient_disagree:
        problems.append("methods disagree on a square")
    ccw = sum(1 for r in sqA if r[0] and r[1] == 1)
    cw = sum(1 for r in sqA if r[0] and r[1] == -1)

    # Walls
    wall_rows = []
    contacts = []
    outside = []
    wall_disagree = []
    inside_A = 0
    inside_B = 0
    least_pos = None
    below = _thr(wall_report_below)
    near_walls = []
    wall_counts = {t: 0 for t in THRESHOLDS}
    for i in range(n):
        cl = sat.wall_clearances(PA[i], S_A)
        clsA = [sat.wall_class(c) for c in cl]
        clsB = clipm.wall_classes(PB[i], S_B)
        if clsA != clsB:
            wall_disagree.append({"id": ids[i], "A": clsA, "B": clsB})
        if all(c >= 0 for c in cl):
            inside_A += 1
        if clipm.inside_area(PB[i], S_B) == 1:
            inside_B += 1
        for w, c in zip(sat.WALLS, cl):
            if c == 0:
                contacts.append({"id": ids[i], "wall": w})
            elif c < 0:
                outside.append({"id": ids[i], "wall": w, "clearance": util.frac_str(c)})
            else:
                if least_pos is None or c < least_pos[0]:
                    least_pos = (c, ids[i], w)
                for t in THRESHOLDS:
                    if c < _thr(t):
                        wall_counts[t] += 1
            if c < below:
                near_walls.append(
                    {"id": ids[i], "wall": w, "clearance": util.frac_str(c), "sci": util.sci(c)}
                )
        wall_rows.append(cl)
    if inside_A != n or inside_B != n:
        problems.append(f"squares outside the box: A {n - inside_A}, B {n - inside_B}")
    if wall_disagree:
        problems.append(f"methods disagree on {len(wall_disagree)} squares' wall classes")

    xs = [pt[0] for P in PA for pt in P]
    ys = [pt[1] for P in PA for pt in P]
    extents = {
        "least_x": util.frac_str(min(xs)),
        "least_y": util.frac_str(min(ys)),
        "greatest_x": util.frac_str(max(xs)),
        "greatest_y": util.frac_str(max(ys)),
        "side_minus_greatest_x": util.frac_str(S_A - max(xs)),
        "side_minus_greatest_y": util.frac_str(S_A - max(ys)),
    }

    # Pairs
    axesA = [r[2] for r in sqA]
    can_pairs = all(r[0] for r in sqA) and all(r[0] for r in sqB)
    pair_summary = None
    if can_pairs:
        own = [sat.own_ranges(PA[i], axesA[i]) for i in range(n)]
        hps = [clipm.halfplanes(PB[i], sqB[i][1]) for i in range(n)]
        countsA = {"apart": 0, "touching": 0, "overlapping": 0}
        countsB = {"apart": 0, "touching": 0, "overlapping": 0}
        disagree = []
        least = []  # (margin, i, j, axis)
        below_counts = {t: 0 for t in THRESHOLDS}
        thr_vals = [(t, _thr(t)) for t in THRESHOLDS]
        h = hashlib.sha256()
        area_sum = mpq(0)
        overlapping = []
        touching = []
        npairs = 0
        for i in range(n):
            for j in range(i + 1, n):
                npairs += 1
                mA, axis = sat.pair_margin(PA[i], axesA[i], own[i], PA[j], axesA[j], own[j])
                cA = sat.classify(mA)
                aB, ne = clipm.pair(PB[i], hps[j])
                cB = clipm.classify(aB, ne)
                countsA[cA] += 1
                countsB[cB] += 1
                area_sum += aB
                h.update(f"{ids[i]},{ids[j]}:{util.frac_str(mA)};".encode())
                if cA != cB:
                    disagree.append({"pair": [ids[i], ids[j]], "A": cA, "B": cB})
                if cA == "overlapping" and len(overlapping) < 200:
                    overlapping.append(
                        {"pair": [ids[i], ids[j]], "margin": util.frac_str(mA), "area": str(aB)}
                    )
                if cA == "touching" and len(touching) < 200:
                    touching.append({"pair": [ids[i], ids[j]]})
                for t, tv in thr_vals:
                    if 0 <= mA < tv:
                        below_counts[t] += 1
                least.append((mA, i, j, axis))
                if len(least) > 4 * keep_least:
                    least.sort(key=lambda r: r[0])
                    del least[keep_least:]
        least.sort(key=lambda r: r[0])
        del least[keep_least:]
        if countsA["overlapping"] or countsB["overlapping"]:
            problems.append(f"overlapping pairs: A {countsA['overlapping']}, B {countsB['overlapping']}")
        if disagree:
            problems.append(f"methods disagree on {len(disagree)} pairs")
        pair_summary = {
            "pairs": npairs,
            "classes_A": countsA,
            "classes_B": countsB,
            "class_disagreements": disagree[:50],
            "class_disagreement_count": len(disagree),
            "overlapping": overlapping,
            "touching": touching,
            "least_margin": {
                "pair": [ids[least[0][1]], ids[least[0][2]]],
                "margin": util.frac_str(least[0][0]),
                "sci": util.sci(least[0][0], 12),
                "axis": least[0][3],
            },
            "least": [
                {
                    "pair": [ids[r[1]], ids[r[2]]],
                    "margin": util.frac_str(r[0]),
                    "sci": util.sci(r[0], 12),
                    "axis": r[3],
                }
                for r in least
            ],
            "nonnegative_margins_below": below_counts,
            "area_sum_B": str(area_sum),
            "margins_sha256": h.hexdigest(),
        }
    else:
        problems.append("pairs not decided: some square is not a unit square")

    verdict = "ACCEPT" if not problems else "REFUSE"
    return {
        "verdict": verdict,
        "problems": problems,
        "n": n,
        "side": util.frac_str(S_A),
        "side_denominator_digits": len(str(q)),
        "squares": {
            "unit_A": unitA,
            "unit_B": unitB,
            "counterclockwise": ccw,
            "clockwise": cw,
            "not_unit": not_unit[:50],
            "orientation_disagreements": orient_disagree,
        },
        "walls": {
            "inside_A": inside_A,
            "inside_B": inside_B,
            "contacts": contacts,
            "outside": outside[:200],
            "outside_count": len(outside),
            "class_disagreements": wall_disagree[:50],
            "least_positive_clearance": None
            if least_pos is None
            else {
                "id": least_pos[1],
                "wall": least_pos[2],
                "clearance": util.frac_str(least_pos[0]),
                "sci": util.sci(least_pos[0]),
            },
            "positive_clearances_below": wall_counts,
            f"square_walls_below_{wall_report_below}": near_walls,
        },
        "extents": extents,
        "pairs": pair_summary,
    }


def main(argv):
    if len(argv) not in (3, 4):
        print(__doc__)
        return 2
    cert = argv[1]
    twin = argv[2] if len(argv) == 4 else None
    out = argv[-1]
    t0 = util.cpu_seconds()
    receipt = {
        "program": "l72_check.py",
        "lane": "L72",
        "bead": "think-qqyg",
        "environment": util.environment(),
        "checker_digests": util.program_digests([os.path.join(HERE, f) for f in CHECKER_FILES]),
        "certificate": {"file": os.path.basename(cert), "sha256": util.sha256_file(cert)},
    }
    if twin:
        receipt["json_twin"] = {"file": os.path.basename(twin), "sha256": util.sha256_file(twin)}
    try:
        data = reader.read_files(cert, twin)
    except reader.ReadError as exc:
        receipt.update({"verdict": "REFUSE", "problems": [f"reader: {exc}"]})
        receipt["cpu_seconds"] = round(util.cpu_seconds() - t0, 2)
        util.write_receipt(out, receipt)
        print("REFUSE", exc)
        return 1
    receipt["reader"] = data["meta"]
    receipt.update(decide_data(data))
    receipt["cpu_seconds"] = round(util.cpu_seconds() - t0, 2)
    util.write_receipt(out, receipt)
    print(receipt["verdict"], receipt["problems"], f"{receipt['cpu_seconds']} s")
    return 0 if receipt["verdict"] == "ACCEPT" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
