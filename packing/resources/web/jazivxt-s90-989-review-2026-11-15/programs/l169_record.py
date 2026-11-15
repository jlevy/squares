"""Lane L169 record (after the freeze): the claim against what the record holds.

Usage: l169_record.py FRONTIER_DIR CERT OUT_JSON

It decides nothing. It reads the front matter of every case record
`FRONTIER_DIR/n-NNN.md` (the reported and verified upper bounds as decimal strings, and
`conjectured_optimum`) and the certificate's exact side S, and reports
- the claim's arithmetic: S as a decimal, its 12-place floor and ceiling, the gain on the
  reported and verified bounds at 90, absolute and relative;
- the grid boundary: for each k, every n = k^2 - c in ((k-1)^2, k^2] and whether its
  reported bound is k or below; the deficits at which the grid still stands; s(k^2 - k)
  and s(k^2 - 10) for every k the record holds;
- the families: which of n = k^2 - c with c = 1 to 5 equals 90 (none can);
- closed forms: S - (s(m) + j) for every reported s(m), m < 90, and integer j >= 0, the
  nearest within 1e-3, and whether any lies within 1e-9;
- the L steps: adding an L of width w to the new packing gives
  n' = 90 + w (floor(S + w) + floor(S)) squares in side S + w, against the record there;
- monotonicity: every reported s(m), m < 90, above S (none would move otherwise).
"""

from __future__ import annotations

import glob
import json
import math
import os
import re
import sys
from fractions import Fraction as F

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves it off

import l169_reader as rd


def front(path: str) -> dict:
    text = open(path).read()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return yaml.safe_load(m.group(1))["packing"]


def dec(f: F, places: int) -> str:
    q = f.numerator * 10**places // f.denominator
    s = str(q).rjust(places + 1, "0")
    return f"{s[:-places]}.{s[-places:]}"


def main(argv: list[str]) -> int:
    cases = {}
    for p in sorted(glob.glob(os.path.join(argv[1], "n-[0-9][0-9][0-9].md"))):
        c = front(p)
        rub = c.get("reported_upper_bound") or {}
        vub = c.get("verified_upper_bound") or {}
        cases[c["n"]] = {
            "reported": F(str(rub.get("value"))) if rub.get("value") is not None else None,
            "reported_exact_form": rub.get("exact_form"),
            "verified": F(str(vub.get("value"))) if vub.get("value") is not None else None,
            "conjectured_optimum": c.get("conjectured_optimum"),
        }
    rdg = rd.read_file(argv[2])
    S = F(*rdg["side"])
    out: dict = {"program": "l169_record.py", "cases_read": len(cases)}
    c90 = cases[90]
    out["claim"] = {
        "side": f"{S.numerator}/{S.denominator}",
        "side_decimal_exact": dec(S, 12),
        "side_is_its_12_place_decimal": S * 10**12 == int(S * 10**12),
        "reported_at_90": str(c90["reported"]),
        "verified_at_90": str(c90["verified"]),
        "gain_on_reported": f"{(c90['reported'] - S).numerator}/{(c90['reported'] - S).denominator}",
        "gain_on_reported_decimal": dec(c90["reported"] - S, 15),
        "gain_relative": float((c90["reported"] - S) / c90["reported"]),
        "conjectured_optimum_at_90": c90["conjectured_optimum"],
    }
    # The grid boundary.
    kmax = int(math.isqrt(max(cases)))
    grid = {}
    for k in range(2, kmax + 1):
        rows = []
        for n in range((k - 1) ** 2 + 1, k * k + 1):
            if n not in cases or cases[n]["reported"] is None:
                continue
            rows.append({"n": n, "deficit": k * k - n, "at_grid": cases[n]["reported"] == k,
                         "reported": float(cases[n]["reported"])})
        at = [r["deficit"] for r in rows if r["at_grid"]]
        below = [r["deficit"] for r in rows if not r["at_grid"]]
        grid[k] = {"deficits_at_grid": at, "least_deficit_below": min(below) if below else None,
                   "largest_deficit_at_grid": max(at) if at else None}
    out["grid_boundary"] = grid
    out["n2_minus_n"] = {k: {"n": k * k - k, "reported": float(cases[k * k - k]["reported"]),
                             "below_k": cases[k * k - k]["reported"] < k}
                         for k in range(2, kmax + 1) if k * k - k in cases}
    out["deficit_10"] = {k: {"n": k * k - 10, "reported": float(cases[k * k - 10]["reported"]),
                             "below_k": cases[k * k - 10]["reported"] < k}
                         for k in range(4, kmax + 1) if k * k - 10 in cases}
    out["families_reaching_90"] = [c for c in range(1, 6) if math.isqrt(90 + c) ** 2 == 90 + c]
    # Closed forms.
    near = []
    for m, c in cases.items():
        if m >= 90 or c["reported"] is None:
            continue
        for j in range(0, 12):
            d = S - (c["reported"] + j)
            if abs(d) < F(1, 1000):
                near.append((abs(d), m, j, float(d), c["reported_exact_form"]))
    near.sort()
    out["closed_forms_within_1e-3"] = [{"m": m, "j": j, "S_minus": d, "exact_form": str(e)} for _, m, j, d, e in near]
    out["closed_forms_within_1e-9"] = [x for x in out["closed_forms_within_1e-3"] if abs(x["S_minus"]) < 1e-9]
    # L steps.
    steps = []
    for w in range(1, 12):
        n2 = 90 + w * (math.floor(S + w) + math.floor(S))
        if n2 not in cases:
            break
        r = cases[n2]["reported"]
        steps.append({"w": w, "n": n2, "side": float(S + w), "reported_there": float(r),
                      "improves": S + w < r, "excess": float(S + w - r)})
    out["l_steps"] = steps
    out["monotone_below_moved"] = [m for m, c in cases.items() if m < 90 and c["reported"] is not None and c["reported"] > S]
    out["monotone_above_reported_below_S"] = [m for m, c in cases.items() if m > 90 and c["reported"] is not None and c["reported"] < S]
    with open(argv[3], "w") as fh:
        json.dump(out, fh, indent=1, default=str)
        fh.write("\n")
    print("claim", out["claim"])
    print("n^2 - n", {k: (v["n"], round(v["reported"], 6), v["below_k"]) for k, v in out["n2_minus_n"].items()})
    print("deficit 10", {k: (v["n"], round(v["reported"], 6), v["below_k"]) for k, v in out["deficit_10"].items()})
    print("largest deficit at grid", {k: (v["largest_deficit_at_grid"], v["least_deficit_below"]) for k, v in grid.items()})
    print("families reaching 90", out["families_reaching_90"])
    print("closed forms within 1e-3", out["closed_forms_within_1e-3"][:6])
    print("closed forms within 1e-9", out["closed_forms_within_1e-9"])
    print("L steps", [(s["w"], s["n"], round(s["excess"], 6), s["improves"]) for s in steps])
    print("monotone", out["monotone_below_moved"], out["monotone_above_reported_below_S"][:10])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
