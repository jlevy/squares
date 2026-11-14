"""Lane L163 claim arithmetic, after the freeze: the prints, the gains and the side-only entries.

Usage: l163_sides.py N228.json N147.json N-228.md N-147.md T300.yaml ISSUES.json OUT.json

Exact throughout: the sides are fractions, 7 + 4 sqrt 2 is bracketed by integer square
roots at 80 digits, and every decimal the issues print is compared with the exact
quantity it stands for. Decides nothing.
"""

from __future__ import annotations

import json
import os
import re
import sys
from decimal import Decimal
from fractions import Fraction as F
from math import isqrt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l163_geom as geom  # noqa: E402
import yaml  # noqa: E402
from l163_reader import read_json  # noqa: E402

DIG = 80


def front(path: str) -> dict:  # pyright: ignore[reportMissingTypeArgument]
    text = open(path, encoding="utf-8").read()
    return yaml.safe_load(text.split("---", 2)[1])["packing"]


def dec(s: str) -> F:
    return F(Decimal(s.rstrip("…").replace("…", "")))


def sqrt2_bracket() -> tuple[F, F]:
    r = isqrt(2 * 10 ** (2 * DIG))
    return F(r, 10**DIG), F(r + 1, 10**DIG)


def near(x: F, printed: str) -> dict[str, object]:
    """How a printed decimal relates to the exact x."""
    p = dec(printed)
    places = len(printed.split(".")[1].rstrip("…")) if "." in printed else 0
    return {
        "printed": printed,
        "exact_floor_at_places": geom.floor_places(x, places),
        "exact_ceil_at_places": geom.ceil_places(x, places),
        "printed_less_exact_sci": geom.sci(p - x),
        "is_floor": geom.floor_places(x, places) == printed.rstrip("…"),
        "is_ceil": geom.ceil_places(x, places) == printed.rstrip("…"),
    }


def main() -> None:
    p228, p147, md228, md147, t300, issues_path, out = sys.argv[1:8]
    s228 = F(*read_json(p228).side)
    s147 = F(*read_json(p147).side)
    f228, f147 = front(md228), front(md147)
    t174 = F(f228["reported_upper_bound"]["exact_form"])
    t174v = F(f228["verified_upper_bound"]["exact_form"])
    t155 = F(f147["verified_upper_bound"]["exact_form"])
    with open(t300, encoding="utf-8") as fh:
        s983 = F(str(yaml.safe_load(fh)["witness"]["side"]))
    lo2, hi2 = sqrt2_bracket()
    cf_lo, cf_hi = 7 + 4 * lo2, 7 + 4 * hi2
    with open(issues_path, encoding="utf-8") as fh:
        issues = {i["number"]: i["body"] for i in json.load(fh)["issues"]}
    c228, c147 = F("15.596043120921"), F("12.651043556588")
    nevska228 = dec("15.596043116631669919627353")
    sq1000 = dec("15.596043116646272293906688")
    nevska147 = dec("12.651043553172632772258400")
    rec: dict[str, object] = {"lane": "L163", "program": "l163_sides.py"}
    rec["n228"] = {
        "side_45_floor": geom.floor_places(s228, 45),
        "claim_is_ceil12": geom.ceil_places(s228, 12) == "15.596043120921",
        "claim_less_side_sci": geom.sci(c228 - s228),
        "T-174_reported_equals_verified": t174 == t174v,
        "T-174_floor_20": geom.floor_places(t174, 20),
        "T-174_print_is": near(t174, "15.60460147572967429"),
        "gain_on_T-174": {"exact_sci": geom.sci(t174 - s228, 12), "relative_sci": geom.sci((t174 - s228) / t174), "issue_print": near(t174 - s228, "0.008558354808882")},
        "claim_gain_on_T-174_sci": geom.sci(t174 - c228, 12),
        "T-300_side_45_floor": geom.floor_places(s983, 45),
        "T-300_claim_is_ceil12": geom.ceil_places(s983, 12) == "15.600801734812",
        "gain_on_T-300_exact": {"sci": geom.sci(s983 - s228, 12), "relative_sci": geom.sci((s983 - s228) / s983)},
        "issue_983_above": {
            "claim983_less_S": near(F("15.600801734812") - s228, "0.004758613890"),
            "exact983_less_S": near(s983 - s228, "0.004758613890"),
            "exact983_less_claim": near(s983 - c228, "0.004758613890"),
            "claim983_less_claim": near(F("15.600801734812") - c228, "0.004758613890"),
        },
        "side_only": {
            "S_less_nevska_sci": geom.sci(s228 - nevska228),
            "S_less_square1000_sci": geom.sci(s228 - sq1000),
            "square1000_less_nevska_sci": geom.sci(sq1000 - nevska228),
            "issue_prints": ["4.289e-09", "4.275e-09"],
        },
        "strict_side_print": near(s228 + F(2, 10**15), "15.596043120920793646"),
    }
    gain147_lo, gain147_hi = cf_lo - s147, cf_hi - s147
    rec["n147"] = {
        "side_45_floor": geom.floor_places(s147, 45),
        "claim_is_ceil12": geom.ceil_places(s147, 12) == "12.651043556588",
        "claim_less_side_sci": geom.sci(c147 - s147),
        "seven_plus_four_root2_floor_40": geom.floor_places(cf_lo, 40),
        "record_print_is": near(cf_lo, "12.65685424949238"),
        "gain_on_closed_form": {
            "floor_30": geom.floor_places(gain147_lo, 30),
            "ceil_30": geom.ceil_places(gain147_hi, 30),
            "relative_sci": geom.sci(gain147_lo / cf_lo),
            "issue_print": near(gain147_lo, "0.005810692904685"),
            "issue_print_hi": near(gain147_hi, "0.005810692904685"),
        },
        "claim_gain_on_closed_form_floor_15": geom.floor_places(cf_lo - c147, 15),
        "T-155_verified_less_closed_form_sci": geom.sci(t155 - cf_hi),
        "gain_on_T-155_sci": geom.sci(t155 - s147, 12),
        "side_only": {"S_less_nevska_sci": geom.sci(s147 - nevska147), "issue_print": "3.415e-09"},
        "strict_side_print": near(s147 + F(2, 10**15), "12.651043556587696471"),
    }
    # the exact sides the issues print to 30 places with an ellipsis
    exact_prints = {}
    for num, s, n in ((984, s228, 228), (985, s147, 147)):
        m = re.search(r"exact side in the certificate is ([0-9.]+)…", issues[num])
        exact_prints[n] = near(s, m.group(1)) if m else None
    rec["issue_exact_side_prints"] = exact_prints
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1, ensure_ascii=False)
    print(json.dumps(rec, ensure_ascii=False)[:3000])


if __name__ == "__main__":
    main()
