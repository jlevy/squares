"""Lane L186: decide one Witness/v2 rational-corner certificate.

Usage: python -I -B l186_check.py CERT.yaml EXPECTED_SHA256 CLAIM OUT.json

It reads the file strictly (l186_reader), decides every square, wall and pair
by both methods (l186_decide), and does the claim's arithmetic exactly: the
12-place ceiling and floor of the side, and whether CLAIM (the issue's printed
side) is that ceiling and at least the side. ACCEPT needs the decision's ACCEPT
and the file's SHA-256 equal to EXPECTED_SHA256.
"""

from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from l186_decide import decide, decimal_text, ftext, sci  # noqa: E402
from l186_reader import ReadError, read_witness_file  # noqa: E402

TEN12 = 10**12


def ceil_places(v: Fraction, places: int) -> Fraction:
    scale = 10**places
    return Fraction(-((-v.numerator * scale) // v.denominator), scale)


def floor_places(v: Fraction, places: int) -> Fraction:
    scale = 10**places
    return Fraction((v.numerator * scale) // v.denominator, scale)


def claim_facts(side: Fraction, claim_text: str) -> dict[str, Any]:
    claim = Fraction(claim_text)
    ceil12 = ceil_places(side, 12)
    floor12 = floor_places(side, 12)
    return {
        "claim_text": claim_text,
        "ceil12": decimal_text(ceil12, 12),
        "floor12": decimal_text(floor12, 12),
        "claim_is_ceil12": claim == ceil12,
        "claim_at_least_side": claim >= side,
        "claim_minus_side": ftext(claim - side),
        "claim_minus_side_sci": sci(claim - side),
        "side_minus_floor12_sci": sci(side - floor12),
    }


def extents(res_clear: list[list[str]], side: Fraction) -> dict[str, Any]:
    cl = [[Fraction(c) for c in row] for row in res_clear]
    min_x = min(r[0] for r in cl)
    min_y = min(r[1] for r in cl)
    max_x = side - min(r[2] for r in cl)
    max_y = side - min(r[3] for r in cl)
    in_place = max(max_x, max_y)
    translated = max(max_x - min_x, max_y - min_y)
    return {
        "min_x": ftext(min_x),
        "min_y": ftext(min_y),
        "max_x": ftext(max_x),
        "max_y": ftext(max_y),
        "least_box_in_place": ftext(in_place),
        "side_minus_least_box_in_place_sci": sci(side - in_place),
        "least_box_translated": ftext(translated),
        "side_minus_least_box_translated_sci": sci(side - translated),
    }


def main() -> None:
    path, expected, claim_text, out_path = sys.argv[1:5]
    t0 = time.process_time()
    rec: dict[str, Any] = {"file": os.path.basename(path), "expected_sha256": expected}
    try:
        w = read_witness_file(path)
    except ReadError as exc:
        rec.update({"verdict": "REFUSE", "reader": f"refused: {exc}"})
        w = None
    if w is not None:
        rec["sha256"] = w.sha256
        rec["sha256_matches"] = w.sha256 == expected
        rec["reader"] = {
            "status": "read",
            "witness_id": w.witness_id,
            "n": w.n,
            "noncanonical_scalars": len(w.noncanonical),
            "noncanonical_first": w.noncanonical[:10],
            "meta": w.meta,
        }
        rec["side"] = {
            "exact": ftext(w.side),
            "decimal_40": decimal_text(w.side, 40),
            "numerator_digits": len(str(w.side.numerator)),
            "denominator_digits": len(str(w.side.denominator)),
        }
        res = decide(w.side, w.squares, keep_lists=True)
        clear = res.pop("_clearances")
        res.pop("_margins")
        rec["decision"] = res
        rec["extents"] = extents(clear, w.side)
        rec["claim"] = claim_facts(w.side, claim_text)
        rec["verdict"] = "ACCEPT" if res["verdict"] == "ACCEPT" and rec["sha256_matches"] else (
            "DISAGREE" if res["verdict"] == "DISAGREE" else "REFUSE"
        )
    rec["cpu_seconds"] = round(time.process_time() - t0, 1)
    with open(out_path, "w") as fh:
        json.dump(rec, fh, indent=1)
        fh.write("\n")
    d = rec.get("decision", {})
    print(
        rec["file"],
        rec["verdict"],
        "pairs",
        d.get("pairs", {}).get("decided"),
        "least margin",
        d.get("pairs", {}).get("least_margin_sci"),
        "least clearance",
        d.get("walls", {}).get("least_clearance_sci"),
        "claim is ceil12:",
        rec.get("claim", {}).get("claim_is_ceil12"),
    )


if __name__ == "__main__":
    main()
