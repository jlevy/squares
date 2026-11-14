"""Lane L153, after the freeze: the claims' arithmetic, exactly.

Clean-room: written for this review, importing nothing from this repository or the
source, and reusing no code of any earlier review. It decides nothing about the bounds.

It reads the three certificates through the frozen reader; T-174's exact side from the
297 case record's `reported_upper_bound.exact_form` and from the house witness; the
record's current rows at 332 and 409 from `frontier/source-coverage.yaml`
(`beyond_horizon_claims`, the row not superseded) and their exact sides from the
retained certificates those rows cite; the 250-digit solution's side from the author's
`n297_solution_250_digits.txt`; and the issues. It prints each side's 12-place floor and
ceiling against the claim, the gains, and the author's close-pair counts (pairs with
centres closer than sqrt(2)).

Usage: l153_sides.py N297.json N332.json N409.json CASE297.md HOUSE297.yaml
       SOURCE_COVERAGE.yaml CERT332 CERT409 SOLUTION.txt ISSUES.json OUT.json
"""

from __future__ import annotations

import json
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l153_reader as reader  # noqa: E402
from l153_check import floor_places, sci  # noqa: E402

getcontext().prec = 400


def ceil_places(v: Fraction, places: int) -> Fraction:
    scale = 10**places
    return Fraction(-((-v.numerator * scale) // v.denominator), scale)


def floor12(v: Fraction) -> Fraction:
    return Fraction(v.numerator * 10**12 // v.denominator, 10**12)


def dec(text: str) -> Fraction:
    return Fraction(Decimal(text))


def cert_side(path: str) -> Fraction:
    for line in Path(path).read_text().splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split()
        return Fraction(parts[1])
    raise SystemExit(f"no side in {path}")


def close_pairs(squares) -> int:
    cs = [(Fraction(*s[0]), Fraction(*s[1])) for s in squares]
    count = 0
    for i in range(len(cs)):
        xi, yi = cs[i]
        for j in range(i + 1, len(cs)):
            dx, dy = cs[j][0] - xi, cs[j][1] - yi
            if dx * dx + dy * dy < 2:
                count += 1
    return count


def main(argv: list[str]) -> int:
    (p297, p332, p409, case297, house297, coverage, cert332, cert409, solution, issues_path,
     out_path) = argv[1:12]
    files = {297: p297, 332: p332, 409: p409}
    data = {n: reader.read(p) for n, p in files.items()}
    side = {n: Fraction(*d["side"]) for n, d in data.items()}
    issues = {i["number"]: i for i in json.loads(Path(issues_path).read_text())["issues"]}
    claims = {297: Fraction("17.739455558289"), 332: Fraction("18.739455558289"),
              409: Fraction("20.739455558289")}
    for n, c in claims.items():
        number = 977 if n == 297 else 979
        if str(c.numerator * 10**12 // c.denominator)[:4] and f"{float(c):.12f}" not in issues[number]["body"]:
            raise SystemExit(f"claim {n} not in issue {number}")
    # T-174
    text = Path(case297).read_text()
    front = yaml.safe_load(text.split("---")[1])
    t174 = Fraction(front["packing"]["reported_upper_bound"]["exact_form"])
    t174_print = front["packing"]["reported_upper_bound"]["value"]
    house = yaml.safe_load(Path(house297).read_text())
    house_side = Fraction(house["witness"]["side"])
    # record rows beyond the horizon
    cov = yaml.safe_load(Path(coverage).read_text())
    rows = {}
    for n in (332, 409):
        current = [r for r in cov["beyond_horizon_claims"] if r.get("n") == n and r.get("disposition") != "superseded"]
        everyone = [r for r in cov["beyond_horizon_claims"] if r.get("n") == n]
        rows[n] = {"current": current, "all": len(everyone)}
    exact_rows = {332: cert_side(cert332), 409: cert_side(cert409)}
    # the 250-digit solution's side
    sol_line = next(ln.strip() for ln in Path(solution).read_text().splitlines() if ln.strip() and not ln.startswith("#"))
    sol_side = dec(sol_line.split()[0])
    out: dict = {"program": "l153_sides.py", "sides": {}, "record": {}}
    for n in (297, 332, 409):
        s = side[n]
        c = claims[n]
        entry = {
            "side_floor_40": floor_places(s, 40),
            "floor12": floor_places(floor12(s), 12),
            "ceil12": floor_places(ceil_places(s, 12), 12),
            "claim": floor_places(c, 12),
            "claim_is_ceil12": c == ceil_places(s, 12),
            "claim_minus_side": sci(c - s, 8),
            "close_pairs_centres_below_sqrt2": close_pairs(data[n]["squares"]),
        }
        out["sides"][str(n)] = entry
    out["sides"]["332_minus_297"] = str(side[332] - side[297])
    out["sides"]["409_minus_297"] = str(side[409] - side[297])
    out["record"]["T-174"] = {
        "print": t174_print,
        "exact_equals_house_witness_side": t174 == house_side,
        "floor_40": floor_places(t174, 40),
        "print_is": "ceil18" if Fraction(t174_print) == ceil_places(t174, 18) else "other",
        "print_minus_exact": sci(Fraction(t174_print) - t174, 6),
        "gain": sci(t174 - side[297], 12),
        "relative_gain": sci((t174 - side[297]) / t174, 6),
    }
    for n, k in ((332, 1), (409, 3)):
        cur = rows[n]["current"]
        printed = Fraction(cur[0]["value"]) if len(cur) == 1 else None
        exact = exact_rows[n]
        out["record"][str(n)] = {
            "current_rows": [{k2: r[k2] for k2 in ("source_id", "value", "disposition")} for r in cur],
            "rows_listed_at_count": rows[n]["all"],
            "exact_side_of_cited_certificate_floor_30": floor_places(exact, 30),
            "print_is_ceil12_of_exact": printed == ceil_places(exact, 12) if printed is not None else None,
            "gain_on_printed_row": sci(printed - side[n], 12) if printed is not None else None,
            "gain_on_exact_row": sci(exact - side[n], 12),
            "relative_gain_exact": sci((exact - side[n]) / exact, 6),
            f"exact_row_minus_T174_plus_{k}": sci(exact - (t174 + k), 8),
            f"new_side_minus_T174_plus_{k}": sci(side[n] - (t174 + k), 12),
        }
    out["solution_250"] = {
        "first_line_digits": len(sol_line.split()[0]),
        "certificate_side_minus_solution_side": sci(side[297] - sol_side, 6),
    }
    out["kaggle_297_by_author"] = {
        "value": "17.7404101723",
        "minus_side": sci(Fraction("17.7404101723") - side[297], 8),
        "minus_T174": sci(Fraction("17.7404101723") - t174, 8),
    }
    Path(out_path).write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
