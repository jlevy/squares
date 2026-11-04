"""The sides against the issues' prints and against the houses' sides, exactly.

Usage: oz_sides.py CERT299.yaml HOUSE299.yaml CERT204.yaml HOUSE204.yaml OUT.json

The prints, the stated fractions and the stated improvements are copied from issues #893
and #894 (their titles and Claim paragraphs, read on 2026-11-04) and from the draft register
claims the import lane wrote; they are data. A print bounds s(n) only if it is at or above
the exact side.
"""

from __future__ import annotations

import json
import platform
import sys
import time
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ozlib as oz  # noqa: E402

ISSUES = {
    299: {
        "issue": 893,
        "stated_fraction": "3560247706795812422293947620670679551/200000000000000000000000000000000000",
        "stated_decimal_prefix": "17.801238533979062",
        "print": "17.801238533979",
        "print_said_to_be": "rounded up at 12 places",
        "house_stated": "17801238549388584084680137655023/1000000000000000000000000000000",
        "house_stated_decimal": "17.8012385493885841",
        "improvement_stated": "1.54e-8",
        "lane_claim_decimal": "17.801238533979062111469738103353397755",
        "lane_ceiling": "17.8012385339790622",
        "lane_difference": "3081904394642079910333920449/200000000000000000000000000000000000",
    },
    204: {
        "issue": 894,
        "stated_fraction": "7403810497792604009019579959/500000000000000000000000000",
        "stated_decimal_prefix": "14.807620995585208",
        "print": "14.807620995586",
        "print_said_to_be": "rounded up at 12 places",
        "house_stated": "14807627471881579627471866771703/1000000000000000000000000000000",
        "house_stated_decimal": "14.8076274718815797",
        "improvement_stated": "6.48e-6",
        "lane_claim_decimal": "14.807620995585208018039159918",
        "lane_ceiling": "14.8076209955852081",
        "lane_difference": "6476296371609432706853703/1000000000000000000000000000000",
    },
}


def one(n: int, cert: str, house: str) -> dict:
    meta = ISSUES[n]
    doc = oz.read_witness_yaml(cert)
    hdoc = oz.read_witness_yaml(house)
    S = oz.to_F(doc["header"]["side"])
    H = oz.to_F(hdoc["header"]["side"])
    pr = Fraction(meta["print"])
    places = oz.terminating_places(S)
    up12 = oz.decimal_places(S, 12, "ceil")
    down12 = oz.decimal_places(S, 12, "floor")
    exact_dec = oz.decimal_places(S, places, "exact") if places is not None else None
    diff_house = H - S
    lane_diff = oz.to_F(meta["lane_difference"])
    return {
        "n": n,
        "issue": meta["issue"],
        "cert_sha256": doc["sha256"],
        "house_sha256": hdoc["sha256"],
        "side": oz.frac_str(S),
        "side_equals_stated_fraction": S == oz.to_F(meta["stated_fraction"]),
        "side_terminating_places": places,
        "side_exact_decimal": exact_dec,
        "stated_prefix_matches": (exact_dec or "").startswith(meta["stated_decimal_prefix"]),
        "ceil_12": up12,
        "floor_12": down12,
        "ceil_16": oz.decimal_places(S, 16, "ceil"),
        "print": meta["print"],
        "print_said_to_be": meta["print_said_to_be"],
        "print_is_ceil_12": meta["print"] == up12,
        "print_is_floor_12": meta["print"] == down12,
        "print_bounds_side": pr >= S,
        "print_minus_side": oz.frac_str(pr - S),
        "print_minus_side_approx": oz.sci(pr - S),
        "house_side": oz.frac_str(H),
        "house_side_equals_stated": H == oz.to_F(meta["house_stated"]),
        "house_decimal_ceil_16": oz.decimal_places(H, 16, "ceil"),
        "house_minus_side": oz.frac_str(diff_house),
        "house_minus_side_approx": oz.sci(diff_house),
        "improvement_stated": meta["improvement_stated"],
        "improvement_rounds_to_stated": f"{float(diff_house):.2e}" == meta["improvement_stated"].replace("e-", "e-0"),
        "lane_claim_decimal_exact": exact_dec == meta["lane_claim_decimal"],
        "lane_ceiling_is_ceil_16": oz.decimal_places(S, 16, "ceil") == meta["lane_ceiling"],
        "lane_difference_exact": lane_diff == diff_house,
        "relative_improvement_approx": oz.sci(diff_house / H),
    }


def main() -> int:
    c299, h299, c204, h204, out_p = sys.argv[1:6]
    t0 = time.process_time()
    rows = [one(299, c299, h299), one(204, c204, h204)]
    receipt = {
        "program": "oz_sides.py",
        "program_sha256": oz.sha256_file(__file__),
        "ozlib_sha256": oz.sha256_file(HERE / "ozlib.py"),
        "python": platform.python_version(),
        "argv": sys.argv[1:],
        "results": rows,
        "cpu_seconds": round(time.process_time() - t0, 3),
    }
    Path(out_p).write_text(json.dumps(receipt, indent=1) + "\n")
    for r in rows:
        print(f"n={r['n']}: side {r['side_exact_decimal']}; ceil12 {r['ceil_12']}; print {r['print']} "
              f"bounds={r['print_bounds_side']} (print - side = {r['print_minus_side_approx']}); "
              f"house - side = {r['house_minus_side_approx']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
