"""Lane r1012: decide a corners certificate and the claim's 12-place arithmetic.

Usage: r1012_check.py CERTIFICATE EXPECTED_GIT_BLOB CLAIM OUT.json

Reads the certificate through r1012_reader, compares the bytes' git blob id with
the one the source tree lists, decides every square, wall and pair by methods A
and B (r1012_decide), and reports the exact side against the claim. The
Euclidean gaps it lists come from r1012_geom's third formulation and decide
nothing.
"""

import json
import os
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.set_int_max_str_digits(0)

import r1012_decide  # noqa: E402
import r1012_geom  # noqa: E402
import r1012_reader  # noqa: E402

getcontext().prec = 60
THRESHOLDS = ["1e-15", "1e-12", "1e-9", "1e-6", "1e-3"]


def exact_text(fr):
    fr = Fraction(fr)
    return f"{fr.numerator}" if fr.denominator == 1 else f"{fr.numerator}/{fr.denominator}"


def dec(fr, places=30):
    fr = Fraction(fr)
    q = Decimal(fr.numerator) / Decimal(fr.denominator)
    return f"{q:.{places}f}"


def sci(fr, digits=6):
    fr = Fraction(fr)
    if fr == 0:
        return "0"
    q = Decimal(fr.numerator) / Decimal(fr.denominator)
    return f"{q:.{digits - 1}e}"


def sqrt_sci(fr, digits=12):
    fr = Fraction(fr)
    if fr == 0:
        return "0"
    q = (Decimal(fr.numerator) / Decimal(fr.denominator)).sqrt()
    return f"{q:.{digits - 1}e}"


def ceil_places(fr, places):
    s = 10 ** places
    return Fraction(-((-fr.numerator * s) // fr.denominator), s)


def floor_places(fr, places):
    s = 10 ** places
    return Fraction((fr.numerator * s) // fr.denominator, s)


def main(argv):
    cert, expected_blob, claim_text, out_path = argv[1:5]
    t0 = time.process_time()
    packing = r1012_reader.read_path(cert)
    n, side, ids, quads = packing["n"], packing["side"], packing["ids"], packing["corners"]
    result = r1012_decide.decide(side, quads)
    a, b = result["a"], result["b"]
    t_decide = time.process_time() - t0

    def name(k):
        return ids[k]

    # squares
    axis_aligned = []
    for k, q in enumerate(quads):
        e, _ = r1012_geom.edges(q)
        if e[0] == 0 or e[1] == 0:
            axis_aligned.append(k)
    senses = {"counterclockwise": a["sense"].count(1), "clockwise": a["sense"].count(-1)}

    # pairs
    pair_items = [(k, Fraction(*m)) for k, m in a["pairs"].items() if m is not None]
    pair_items.sort(key=lambda kv: (kv[1], kv[0]))
    classes = {}
    for _, cls in a["pair_class"].items():
        classes[cls] = classes.get(cls, 0) + 1
    below = {t: sum(1 for _, m in pair_items if 0 <= m < Fraction(t)) for t in THRESHOLDS}
    least_pairs = []
    for (i, j), m in pair_items[:25]:
        entry = {
            "pair": [name(i), name(j)],
            "margin": sci(m, 9),
            "margin_exact": exact_text(m),
            "axis": a["pair_axis"][(i, j)],
            "class_A": a["pair_class"][(i, j)],
            "class_B": b["pair_class"][(i, j)],
        }
        least_pairs.append(entry)
    touching = [[name(i), name(j)] for (i, j), m in pair_items if m == 0]
    overlapping = [[name(i), name(j)] for (i, j), m in pair_items if m < 0]

    # Euclidean gaps of the apart pairs (third formulation; descriptive)
    gaps = []
    for (i, j), m in pair_items:
        if m > 0:
            g2 = r1012_geom.gap2(quads[i], quads[j])
            gaps.append(((i, j), g2, m))
    gaps.sort(key=lambda t: (t[1], t[0]))
    least_gaps = [
        {
            "pair": [name(i), name(j)],
            "gap": sqrt_sci(g2, 12),
            "gap_squared_exact": exact_text(g2),
            "margin": sci(m, 9),
            "gap_over_margin": f"{(Decimal(g2.numerator) / Decimal(g2.denominator)).sqrt() / (Decimal(m.numerator) / Decimal(m.denominator)):.12f}",
        }
        for (i, j), g2, m in gaps[:25]
    ]
    gap_is_margin = sum(1 for _, g2, m in gaps if g2 == m * m and m < Fraction(1, 1000))
    near = sum(1 for _, _, m in gaps if m < Fraction(1, 1000))

    # walls
    wall_names = ["left", "bottom", "right", "top"]
    contacts = {w: [] for w in wall_names}
    least_positive = None
    per_wall_least_positive = {}
    for k in range(n):
        if a["walls"][k] is None:
            continue
        for w, c in enumerate(a["walls"][k]):
            cf = Fraction(*c)
            if cf == 0:
                contacts[wall_names[w]].append(name(k))
            elif cf > 0:
                if least_positive is None or cf < least_positive[0]:
                    least_positive = (cf, name(k), wall_names[w])
                cur = per_wall_least_positive.get(wall_names[w])
                if cur is None or cf < cur[0]:
                    per_wall_least_positive[wall_names[w]] = (cf, name(k))
    contact_shapes = {}
    for w in wall_names:
        for sid in contacts[w]:
            k = ids.index(sid)
            shape = "axis-aligned edge" if k in axis_aligned else "corner of a turned square"
            contact_shapes[shape] = contact_shapes.get(shape, 0) + 1

    # denominators
    den_digits = [len(str(d)) for d in a["den"]]

    # claim
    claim = Fraction(Decimal(claim_text))
    places = len(claim_text.split(".")[1]) if "." in claim_text else 0
    ceil12 = ceil_places(side, places)
    floor12 = floor_places(side, places)

    receipt = {
        "program": "r1012_check.py",
        "certificate": os.path.basename(cert),
        "sha256": packing["sha256"],
        "git_blob": packing["git_blob"],
        "git_blob_expected": expected_blob,
        "git_blob_matches": packing["git_blob"] == expected_blob,
        "reading": {
            "enveloped": packing["enveloped"],
            "envelope": packing["envelope"],
            "witness_id": packing["witness_id"],
            "witness_id_matches_schema_pattern": packing["witness_id_matches_schema_pattern"],
            "origin": packing["origin"],
            "angle_unit": packing["angle_unit"],
            "scalars": packing["scalars"],
            "scalar_forms": packing["scalar_forms"],
            "noncanonical_count": len(packing["noncanonical"]),
            "noncanonical_first": packing["noncanonical"][:10],
            "square_info_keys": packing["square_info_keys"],
            "certificate_keys": packing["certificate_keys"],
            "text_facts": packing["text_facts"],
            "ids_first_last": [ids[0], ids[-1]],
            "ids_are_square_dash_index": ids == [f"square-{k}" for k in range(n)],
        },
        "n": n,
        "side_exact": exact_text(side),
        "side_decimal": dec(side, 30),
        "verdict": result["verdict"],
        "problems": [list(map(str, p)) for p in result["problems"]][:50],
        "problem_count": len(result["problems"]),
        "disagreements": [list(map(str, d)) for d in result["disagreements"]][:50],
        "disagreement_count": len(result["disagreements"]),
        "squares": {
            "unit_by_A": sum(a["unit"]),
            "unit_by_B": sum(b["unit"]),
            "senses": senses,
            "axis_aligned": len(axis_aligned),
            "turned": n - len(axis_aligned),
            "area_inside_exactly_1_by_B": sum(1 for v in b["inside_area"] if v == 1),
            "denominator_digits_max": max(den_digits),
            "denominator_digits_min": min(den_digits),
        },
        "pairs": {
            "count": len(a["pair_class"]),
            "classes_A": classes,
            "classes_B": {c: list(b["pair_class"].values()).count(c) for c in ("apart", "touch", "overlap")},
            "clip_order_disagreements": len(b["order_disagree"]),
            "below_threshold_nonnegative": below,
            "touching": touching,
            "overlapping": overlapping[:50],
            "least_margins": least_pairs,
            "least_euclidean_gaps": least_gaps,
            "pairs_below_1e-3_whose_gap_equals_margin": gap_is_margin,
            "apart_pairs_below_1e-3": near,
        },
        "walls": {
            "contacts": contacts,
            "contact_count": sum(len(v) for v in contacts.values()),
            "contact_shapes": contact_shapes,
            "least_positive_clearance": None
            if least_positive is None
            else {"value": sci(least_positive[0], 9), "exact": exact_text(least_positive[0]),
                  "square": least_positive[1], "wall": least_positive[2]},
            "least_positive_by_wall": {
                w: {"value": sci(v[0], 9), "square": v[1]} for w, v in per_wall_least_positive.items()
            },
        },
        "claim": {
            "claim": claim_text,
            "places": places,
            "claim_minus_side": sci(claim - side, 9),
            "claim_minus_side_exact": exact_text(claim - side),
            "claim_is_ceiling_of_side": claim == ceil12,
            "ceiling": dec(ceil12, places),
            "floor": dec(floor12, places),
            "side_minus_floor": sci(side - floor12, 9),
            "side_at_most_claim": side <= claim,
        },
        "cpu_seconds_decide": round(t_decide, 2),
        "cpu_seconds_total": round(time.process_time() - t0, 2),
        "python": sys.version.split()[0],
    }
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(receipt, handle, indent=1, sort_keys=False)
        handle.write("\n")
    print(f"{result['verdict']} {n} squares, {len(a['pair_class'])} pairs, side {dec(side, 30)}")
    return 0 if result["verdict"] == "ACCEPT" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
