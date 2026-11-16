"""Lane L186, after the freeze: the claims' arithmetic against the record. Decides nothing.

Usage: python -I -B l186_sides.py FRONTIER_DIR ISSUE.json OUT.json CHECK_n127.json ... CHECK_n305.json

For each certificate (its exact side from this lane's check receipt) it computes, exactly:
the gain on the record's reported upper bound at the count (the case record's
`exact_form`, or its `value` where the form is not rational); the issue's printed
record values, gains, Kodaj's sides and "our part" against these; the reported s(m) + j
within 1e-3 of the side for m < n; the counts one L step of width 1 to 8 reaches from the
side and whether any lies below the record there; and the counts below n whose record lies
above the side (monotonicity). It reads the case records' front matter only.
"""

from __future__ import annotations

import json
import os
import re
import sys
from fractions import Fraction
from math import floor
from typing import Any

import yaml

ISSUE_ROWS = {
    # n: (claimed side, record as printed, lower by, Kodaj's side, our part), from the issue's table
    "127": ("11.801753890487", "11.8108787875891799", "9.1249e-3", "11.801765635430", "1.174e-5"),
    "204": ("14.802646843107", "14.8043613836518588", "1.7145e-3", "14.802646907234", "6.41e-8"),
    "232": ("15.759531627557", "15.7614096448817244", "1.8780e-3", "15.759531732104", "1.045e-7"),
    "264": ("16.773807598002", "16.7747351323878329", "9.275e-4", "16.773891500852", "8.390e-5"),
    "305": ("17.945762359659", "17.9504664821377123", "4.7041e-3", "17.946298110350", "5.358e-4"),
}
LEADERBOARD = {
    "127": "11.800793726617",
    "204": "14.802436041464",
    "232": "15.758852775266",
    "264": "16.770127228405",
    "305": "17.945755838742",
}
RATIONAL = re.compile(r"-?\d+(/\d+)?\Z")


def sci(v: Fraction, digits: int = 6) -> str:
    if v == 0:
        return "0"
    return f"{float(v):.{digits}e}"


def record_bounds(frontier: str) -> dict[int, dict[str, Any]]:
    out: dict[int, dict[str, Any]] = {}
    for name in sorted(os.listdir(frontier)):
        m = re.fullmatch(r"n-(\d+)\.md", name)
        if not m:
            continue
        text = open(os.path.join(frontier, name), encoding="utf-8").read()
        if not text.startswith("---\n"):
            continue
        front = yaml.safe_load(text[4 : text.index("\n---", 4)])
        ub = (front.get("packing") or {}).get("reported_upper_bound") or {}
        if not ub or ub.get("value") is None:
            continue
        form = ub.get("exact_form")
        exact = isinstance(form, str) and RATIONAL.match(form.strip()) is not None
        value = Fraction(form.strip()) if exact else Fraction(str(ub["value"]))
        out[int(m.group(1))] = {
            "value": value,
            "exact": exact,
            "text": str(ub["value"]),
            "found_by": ub.get("found_by"),
            "improved_by": ub.get("improved_by"),
            "evidence": ub.get("evidence"),
        }
    return out


def main() -> None:
    frontier, issue_path, out_path = sys.argv[1:4]
    checks = sys.argv[4:]
    with open(issue_path) as fh:
        json.load(fh)  # kept beside the receipt; the issue's numbers are the table above
    rec = record_bounds(frontier)
    result: dict[str, Any] = {"cases_read": len(rec), "counts": {}}
    for path in checks:
        with open(path) as fh:
            chk = json.load(fh)
        n = int(chk["reader"]["n"])
        S = Fraction(chk["side"]["exact"])
        key = str(n)
        claim, rec_print, lower_by, kodaj, ours = ISSUE_ROWS[key]
        house = rec[n]
        gain = house["value"] - S
        claim_gain = Fraction(house["text"]) - Fraction(claim)
        k = Fraction(kodaj)
        near: list[Any] = []
        for m, r in rec.items():
            if m >= n:
                continue
            for j in range(0, 20):
                d = S - (r["value"] + j)
                if abs(d) < Fraction(1, 1000):
                    near.append([m, j, sci(d)])
        lsteps = []
        for w in range(1, 9):
            add = w * (floor(S + w) + floor(S))
            m = n + add
            r = rec.get(m)
            lsteps.append(
                {
                    "width": w,
                    "count": m,
                    "side": sci(S + w, 12),
                    "record": None if r is None else r["text"],
                    "below_record": None if r is None else (S + w < r["value"]),
                    "above_record_by": None if r is None else sci(S + w - r["value"]),
                }
            )
        mono_below = [[m, r["text"]] for m, r in rec.items() if m < n and r["value"] > S]
        mono_above = [[m, r["text"]] for m, r in rec.items() if m > n and r["value"] < S]
        result["counts"][key] = {
            "side_exact_digits": [len(str(S.numerator)), len(str(S.denominator))],
            "record": {
                "text": house["text"],
                "exact_form_rational": house["exact"],
                "found_by": house["found_by"],
                "improved_by": house["improved_by"],
                "evidence": house["evidence"],
            },
            "issue_record_print": rec_print,
            "issue_record_print_minus_record": sci(Fraction(rec_print) - house["value"]),
            "gain_exact_sci": sci(gain, 12),
            "gain_relative": sci(gain / house["value"]),
            "gain_positive": gain > 0,
            "claim_to_record_as_printed": sci(claim_gain, 12),
            "issue_lower_by": lower_by,
            "issue_lower_by_matches_3sf": f"{float(gain):.4g}" == f"{float(Fraction(lower_by)):.4g}"
            or abs(gain - Fraction(lower_by)) < Fraction(lower_by) * Fraction(5, 10**4),
            "kodaj_side": kodaj,
            "kodaj_minus_side": sci(k - S, 6),
            "issue_our_part": ours,
            "kodaj_below_record": k < house["value"],
            "kodaj_gain_on_record": sci(house["value"] - k, 6),
            "kodaj_share_of_gain": sci((house["value"] - k) / gain, 6),
            "leaderboard_side": LEADERBOARD[key],
            "leaderboard_below_side_by": sci(S - Fraction(LEADERBOARD[key]), 6),
            "closed_forms_within_1e-3": near[:20],
            "l_steps": lsteps,
            "monotonicity_counts_below_with_record_above_side": mono_below,
            "monotonicity_counts_above_with_record_below_side": mono_above,
        }
    with open(out_path, "w") as fh:
        json.dump(result, fh, indent=1)
        fh.write("\n")
    for key, v in result["counts"].items():
        print(key, "gain", v["gain_exact_sci"], "kodaj-side", v["kodaj_minus_side"], "near", len(v["closed_forms_within_1e-3"]),
              "L below record", [s["count"] for s in v["l_steps"] if s["below_record"]], "mono", v["monotonicity_counts_below_with_record_above_side"][:5])


if __name__ == "__main__":
    main()
