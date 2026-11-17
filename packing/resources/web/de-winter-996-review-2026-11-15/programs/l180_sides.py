"""Lane L180, after the freeze: the claim's arithmetic, closed forms, L steps, monotonicity.

Written for the blind stage 4 review of issue #996. It decides nothing about the bound.
Every number is exact (fractions) unless a case record states only a decimal, which is
then read as the rational its decimal names and flagged.

Usage: l180_sides.py JSON FRONTIER_DIR HOUSE_WITNESS OUT
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction as F
from typing import Any

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l180_reader as R  # noqa: E402
from l180_decide import fstr, sci  # noqa: E402


def places(v: F, k: int, up: bool) -> F:
    q = v * 10**k
    n = -((-q.numerator) // q.denominator) if up else q.numerator // q.denominator
    return F(n, 10**k)


def dec(v: F, k: int) -> str:
    n = abs(v.numerator) * 10**k // v.denominator
    s = str(n).rjust(k + 1, "0")
    return f"{'-' if v < 0 else ''}{s[:-k]}.{s[-k:]}"


def case_bounds(frontier: str) -> dict[int, dict[str, Any]]:
    out: dict[int, dict[str, Any]] = {}
    for name in sorted(os.listdir(frontier)):
        if not (name.startswith("n-") and name.endswith(".md")):
            continue
        with open(os.path.join(frontier, name), encoding="utf-8") as fh:
            text = fh.read()
        if not text.startswith("---\n"):
            continue
        front = yaml.safe_load(text.split("---\n", 2)[1])
        p = front.get("packing", {}) if isinstance(front, dict) else {}
        n = p.get("n")
        ub = p.get("reported_upper_bound") or {}
        if not isinstance(n, int) or not ub:
            continue
        exact, flag = None, "exact_form"
        ef = ub.get("exact_form")
        if isinstance(ef, str):
            try:
                exact = R.scalar(ef.strip())
            except R.ReadError:
                exact = None
        if exact is None and ub.get("value") is not None:
            exact, flag = F(str(ub["value"])), "decimal value"
        if exact is not None:
            out[n] = {"side": exact, "read_from": flag, "exact_form": ef, "value": ub.get("value")}
    return out


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(__doc__)
        return 2
    r = R.read_json(argv[1])
    S = r.side
    with open(argv[3], encoding="utf-8") as fh:
        house = yaml.safe_load(fh)["witness"]
    t303 = R.scalar(str(house["side"]))
    claim = F(9994038857546, 10**12)
    t303_print = F(9998277166926, 10**12)
    bryant = F(9998277166917, 10**12)
    cases = case_bounds(argv[2])
    out: dict[str, Any] = {"program": "l180_sides.py", "lane": "L180"}
    out["side"] = {
        "exact": fstr(S),
        "places_30": dec(S, 30),
        "ceil_12": dec(places(S, 12, True), 12),
        "floor_12": dec(places(S, 12, False), 12),
        "claim": dec(claim, 12),
        "claim_is_ceil_12": claim == places(S, 12, True),
        "claim_minus_side": sci(claim - S),
        "side_is_ceil_20_of_itself": places(S, 20, True) == S,
    }
    rec90 = cases.get(90, {})
    out["t303"] = {
        "house_witness_side": fstr(t303),
        "case_record_exact_form": rec90.get("exact_form"),
        "case_record_side_equal": rec90.get("side") == t303,
        "print": dec(t303, 12),
    }
    gain = t303 - S
    out["gain"] = {
        "on_t303_exact": fstr(gain),
        "on_t303_decimal": dec(gain, 20),
        "on_t303_approx": sci(gain),
        "relative": sci(gain / t303),
        "on_t303_print_claim_to_claim": dec(t303_print - claim, 12),
        "issue_print": "0.00424",
        "issue_print_is_gain_to_three_figures": round(float(gain), 5) == 0.00424,
        "on_grid_10": dec(10 - S, 20),
        "below_public_submission_9.998277166917": dec(bryant - S, 20),
        "public_submission_below_t303_by": sci(t303 - bryant),
    }
    # The author's close pairs: centres closer than sqrt(2).
    close = 0
    n = r.n
    for i in range(n):
        for j in range(i + 1, n):
            dx = r.poses[i].x - r.poses[j].x
            dy = r.poses[i].y - r.poses[j].y
            if dx * dx + dy * dy < 2:
                close += 1
    out["pairs_with_centres_closer_than_sqrt2"] = close
    # Lower bounds and the record at 90.
    out["record_90"] = {k: (fstr(v) if isinstance(v, F) else v) for k, v in rec90.items()}
    # Closed forms: S - (s(m) + j) for every reported s(m), m < 90, and j >= 0.
    near = []
    best: tuple[F, int, int] | None = None
    for m, c in cases.items():
        if m >= 90:
            continue
        j = max(0, round(float(S - c["side"])))
        for jj in (j - 1, j, j + 1):
            if jj < 0:
                continue
            d = S - (c["side"] + jj)
            if best is None or abs(d) < abs(best[0]):
                best = (d, m, jj)
            if abs(d) < F(1, 1000):
                near.append({"m": m, "j": jj, "difference": sci(d), "read_from": c["read_from"]})
    out["closed_forms"] = {
        "within_1e-3": near,
        "nearest": {"m": best[1], "j": best[2], "difference": sci(best[0])} if best else None,
        "cases_read": len(cases),
    }
    # L steps of integer width w: n + w (2 floor(S) + w) squares at side S + w.
    fl = S.numerator // S.denominator
    steps = []
    for w in range(1, 9):
        m = 90 + w * (2 * fl + w)
        c = cases.get(m)
        steps.append(
            {
                "width": w,
                "count": m,
                "side": dec(S + w, 12),
                "reported": dec(c["side"], 12) if c else None,
                "improves": bool(c and S + w < c["side"]),
                "above_record_by": sci(S + w - c["side"]) if c else None,
            }
        )
    out["l_steps"] = steps
    # Monotonicity: s(m) <= s(90) for m < 90, and s(90) <= s(m) for m > 90.
    out["monotonicity"] = {
        "below_90_reported_above_S": sorted(m for m, c in cases.items() if m < 90 and c["side"] > S),
        "above_90_reported_below_S": sorted(m for m, c in cases.items() if m > 90 and c["side"] < S),
        "s89": dec(cases[89]["side"], 12) if 89 in cases else None,
        "s91": dec(cases[91]["side"], 12) if 91 in cases else None,
    }
    with open(argv[4], "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(
        f"gain {out['gain']['on_t303_approx']}; close pairs {close}; closed forms within 1e-3 {len(near)}, nearest {out['closed_forms']['nearest']}; "
        f"L steps improving {[s['count'] for s in steps if s['improves']]}; monotonicity {out['monotonicity']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
