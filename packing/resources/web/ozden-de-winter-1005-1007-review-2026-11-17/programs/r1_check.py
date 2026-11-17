"""Decide one certificate file and write its receipt.

Lane R1, stage 4 review of #1005, #1006 and #1007.  Clean-room.

    python -I -B r1_check.py FILE FORM STATED_SHA256|- CLAIM OUT.json

FORM is witness-yaml, witness-json or centre-json.  STATED_SHA256 is the digest
the issue lists for the file, or ``-`` where the issue lists none.  CLAIM is the
side the issue claims, a decimal.

The file is hashed, read strictly (r1_read), and decided by method A (r1_axes) and
method B (r1_area) on every square, wall and pair (r1_decide).  The verdict is
ACCEPT only when the stated digest (if any) is the file's, the reading holds, and
both methods accept everything with equal classes.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
import time
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gmpy2  # noqa: E402
import yaml  # noqa: E402

import r1_axes  # noqa: E402
import r1_decide  # noqa: E402
import r1_fmt  # noqa: E402
import r1_read  # noqa: E402

WALLS = r1_decide.WALLS
THRESHOLDS = (-12, -11, -10, -9, -6, -3, -1)
TEN_30 = Fraction(1, 10**30)


def decimal_claim(text):
    if not text.replace(".", "", 1).isdigit():
        raise SystemExit(f"claim {text!r} is not a plain decimal")
    return Fraction(text)


def summarise(packing, dec, claim):
    """The exact facts of a decision, as a JSON-ready mapping."""
    n, side = packing.n, packing.side
    out = {}
    out["n"] = n
    out["side"] = {
        "exact": r1_fmt.frac(side),
        "to_40_places": r1_fmt.dec(side, 40),
        "numerator_digits": len(str(side.numerator)),
        "denominator_digits": len(str(side.denominator)),
        "is_terminating_decimal": r1_fmt.is_exact_decimal(side),
    }
    out["squares"] = {
        "unit_by_a": sum(dec.unit_a),
        "unit_by_b": sum(dec.unit_b),
        "counterclockwise_by_a": sum(1 for s in dec.sense_a if s > 0),
        "clockwise_by_a": sum(1 for s in dec.sense_a if s < 0),
        "counterclockwise_by_b": sum(1 for s in dec.sense_b if s > 0),
        "clockwise_by_b": sum(1 for s in dec.sense_b if s < 0),
        "not_unit": [
            {"square": k + 1, "why_a": dec.why_a[k], "unit_by_b": dec.unit_b[k]}
            for k in range(n)
            if not (dec.unit_a[k] and dec.unit_b[k])
        ][:40],
    }
    classes_a = {"apart": 0, "touching": 0, "overlapping": 0}
    classes_b = {"apart": 0, "touching": 0, "overlapping": 0}
    for key, value in dec.margin.items():
        classes_a[r1_axes.classify(value)] += 1
        classes_b[dec.class_b[key]] += 1
    ordered = sorted(dec.margin.items(), key=lambda kv: (kv[1], kv[0]))
    positive = [(key, value) for key, value in ordered if value > 0]
    touching = [key for key, value in ordered if value == 0]
    pairs = {
        "decided": len(dec.margin),
        "expected": n * (n - 1) // 2,
        "by_a": classes_a,
        "by_b": classes_b,
        "sum_of_overlap_areas_by_b": r1_fmt.frac(sum(dec.area_b.values(), Fraction(0))),
        "touching_pairs": len(touching),
        "touching_pairs_listed": [list(key) for key in touching[:400]],
    }
    if ordered:
        least = ordered[0][1]
        pairs["least_margin"] = r1_fmt.exact_and_sci(least)
        pairs["least_margin_pairs"] = [list(k) for k, v in ordered if v == least][:40]
    if positive:
        least_pos = positive[0][1]
        pairs["least_positive_margin"] = r1_fmt.exact_and_sci(least_pos)
        pairs["least_positive_margin_pairs"] = [list(k) for k, v in positive if v == least_pos][
            :40
        ]
        pairs["positive_margins_below"] = {
            f"1e{e}": sum(1 for _, v in positive if v < Fraction(10) ** e) for e in THRESHOLDS
        }
        pairs["thirty_least_positive"] = [
            {"pair": list(k), "margin": r1_fmt.sci(v)} for k, v in positive[:30]
        ]
        below = [v for _, v in positive if v < Fraction(1, 10**9)]
        above = [(k, v) for k, v in positive if v >= Fraction(1, 10**9)]
        pairs["positive_below_1e-9"] = {
            "count": len(below),
            "least": r1_fmt.sci(below[0]) if below else None,
            "greatest": r1_fmt.sci(below[-1]) if below else None,
            "median": r1_fmt.sci(below[len(below) // 2]) if below else None,
            "distinct_values": len(set(below)),
            "next_above": (
                {"pair": list(above[0][0]), "margin": r1_fmt.sci(above[0][1])} if above else None
            ),
        }
    out["pairs"] = pairs
    walls = {}
    for w, name in enumerate(WALLS):
        values = [(dec.clear[k][w], k + 1) for k in range(n)]
        least = min(values)[0]
        positive_w = sorted(v for v in values if v[0] > 0)
        walls[name] = {
            "touching_squares": [k for v, k in values if v == 0][:400],
            "touching_count": sum(1 for v, _ in values if v == 0),
            "crossing_squares": [k for v, k in values if v < 0][:400],
            "least_clearance": r1_fmt.exact_and_sci(least),
            "least_clearance_squares": [k for v, k in values if v == least][:40],
            "least_positive_clearance": (
                r1_fmt.exact_and_sci(positive_w[0][0]) if positive_w else None
            ),
            "least_positive_clearance_squares": (
                [k for v, k in positive_w if v == positive_w[0][0]][:40] if positive_w else []
            ),
            "positive_clearances_below_1e-9": sum(
                1 for v, _ in positive_w if v < Fraction(1, 10**9)
            ),
            "classes_by_b": {
                cls: sum(
                    1 for k in range(n) if dec.wall_b[k] is not None and dec.wall_b[k][w][0] == cls
                )
                for cls in ("apart", "touching", "overlapping")
            },
        }
    out["walls"] = walls
    mins = [min(dec.clear[k][w] for k in range(n)) for w in range(4)]
    width_slack = mins[0] + mins[2]
    height_slack = mins[1] + mins[3]
    out["extent"] = {
        "width": r1_fmt.exact_and_sci(side - width_slack, 20),
        "height": r1_fmt.exact_and_sci(side - height_slack, 20),
        "side_less_width": r1_fmt.exact_and_sci(width_slack),
        "side_less_height": r1_fmt.exact_and_sci(height_slack),
        "side_less_larger_extent": r1_fmt.exact_and_sci(min(width_slack, height_slack)),
        "least_right_or_top_clearance": r1_fmt.exact_and_sci(min(mins[2], mins[3])),
    }
    out["area_inside_box_by_b"] = {
        "exactly_1": sum(1 for a in dec.inside_b if a == 1),
        "below_1": sum(1 for a in dec.inside_b if a is not None and a != 1),
    }
    ceiling = r1_fmt.ceil_places(side, 12)
    out["claim"] = {
        "claimed": r1_fmt.dec(claim, 12),
        "claim_less_side": r1_fmt.exact_and_sci(claim - side),
        "claim_at_least_side": claim >= side,
        "twelve_place_ceiling_of_side": r1_fmt.dec(ceiling, 12),
        "claim_is_that_ceiling": claim == ceiling,
    }
    disagreements = dec.disagreements()
    out["methods_disagree"] = {"count": len(disagreements), "first": disagreements[:40]}
    return out


def main(argv):
    if len(argv) != 6:
        raise SystemExit(__doc__)
    path, form, stated, claim_text, out_path = argv[1:]
    started = time.process_time()
    claim = decimal_claim(claim_text)
    receipt = {
        "program": "r1_check.py",
        "lane": "R1 (c-review-1005-1117)",
        "file": os.path.basename(path),
        "form": form,
        "python": platform.python_version(),
        "gmpy2": gmpy2.version(),
        "gmp": gmpy2.mp_version(),
        "pyyaml": yaml.__version__,
    }
    with open(path, "rb") as handle:
        raw = handle.read()
    digest = hashlib.sha256(raw).hexdigest()
    receipt["bytes"] = len(raw)
    receipt["sha256"] = digest
    receipt["stated_sha256"] = None if stated == "-" else stated
    receipt["sha256_is_the_stated_one"] = None if stated == "-" else digest == stated
    reasons = []
    if stated != "-" and digest != stated:
        reasons.append("the file's SHA-256 is not the stated one")
    try:
        packing = r1_read.READERS[form](raw, where=os.path.basename(path))
    except r1_read.Refusal as exc:
        receipt["reading"] = {"refused": str(exc)}
        receipt["verdict"] = "REFUSE"
        receipt["reasons"] = reasons + [f"reading refused: {exc}"]
    else:
        receipt["reading"] = packing.notes
        dec, _, _ = r1_decide.decide(packing)
        receipt.update(summarise(packing, dec, claim))
        verdict, why = dec.verdict()
        for kind, items in why:
            reasons.append({"kind": kind, "count": len(items), "first": items[:40]})
        receipt["verdict"] = "ACCEPT" if verdict == "ACCEPT" and not reasons else "REFUSE"
        receipt["reasons"] = reasons
    receipt["cpu_seconds"] = round(time.process_time() - started, 1)
    with open(out_path, "w") as handle:
        json.dump(receipt, handle, indent=1)
        handle.write("\n")
    print(receipt["verdict"], receipt["file"], f"cpu {receipt['cpu_seconds']} s")
    return 0 if receipt["verdict"] == "ACCEPT" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
