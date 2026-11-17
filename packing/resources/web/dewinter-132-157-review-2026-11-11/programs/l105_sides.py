"""Lane L105, after the freeze: the claims' arithmetic. Decides no packing.

Usage: python -I -B l105_sides.py SOURCE_DIR REPO_DIR ISSUE_JSON OUT_JSON

Holds every printed number of issue #958 and of the two READMEs to the exact sides
(read through the frozen reader) and to the record at `main`: the case records'
`exact_form` at 132 and 157, and at 109 for the seed's comparison.
"""

from __future__ import annotations

import json
import re
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import l105_check as K  # noqa: E402
import l105_reader as R  # noqa: E402


def floor_places(v: F, k: int) -> F:
    return F((v.numerator * 10**k) // v.denominator, 10**k)


def ceil_places(v: F, k: int) -> F:
    return F(-((-v.numerator * 10**k) // v.denominator), 10**k)


def round_places(v: F, k: int) -> F:
    return F(round(v * 10**k), 10**k)


def dec(v: F, k: int) -> str:
    """v truncated (floor) to k places, as text."""
    m = (v.numerator * 10**k) // v.denominator
    s = str(m).rjust(k + 1, "0")
    return f"{s[:-k]}.{s[-k:]}"


def rules(print_text: str, v: F) -> list[str]:
    """Which rounding rules at the print's own places give the print."""
    k = len(print_text.split(".")[1]) if "." in print_text else 0
    p = F(print_text)
    out = []
    if floor_places(v, k) == p:
        out.append("floor")
    if ceil_places(v, k) == p:
        out.append("ceil")
    if round_places(v, k) == p:
        out.append("nearest")
    return out


def sig_round(v: F, digits: int) -> str:
    return f"{float(v):.{digits - 1}e}"


def frontier_exact(repo: Path, n: int) -> tuple[str, F]:
    text = (repo / "packing" / "frontier" / f"n-{n:03d}.md").read_text()
    head = text.split("\n---\n", 1)[0]
    m = re.search(r"reported_upper_bound:\n    value: '([^']+)'\n    exact_form: ([^\n]+)\n", head)
    assert m, n
    form = m.group(2).strip().strip("'")
    if re.fullmatch(r"-?\d+(/\d+)?", form):
        return m.group(1), F(form)
    return m.group(1), F(0)  # an algebraic form; handled by the caller


def main() -> None:
    sys.set_int_max_str_digits(0)
    src, repo, issue_p, outp = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    issue = json.loads(issue_p.read_text())
    body = issue["body"]
    out: dict[str, Any] = {"program": "l105_sides.py", "issue": {"number": issue["number"], "created_at": issue["created_at"], "updated_at": issue["updated_at"]}}
    rows = {}
    for line in body.splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|\s*([0-9.]+)\.\.\.\s*\|\s*([^|]+?)\s*\|\s*([0-9.e+-]+)\s*\|", line)
        if m:
            rows[int(m.group(1))] = {"new": m.group(2), "register": m.group(3), "gain": m.group(4)}
    res: dict[str, Any] = {}
    for n in (132, 157):
        pk = R.read_json(src / f"n{n}" / f"n{n}_exact.json")
        S = F(pk["side"][0], pk["side"][1])
        readme = (src / f"n{n}" / "README.md").read_text()
        m = re.search(r"\n    ([0-9.]+)\.\.\.\n", readme)
        assert m
        rd_side = m.group(1)
        m2 = re.search(r"listed ([0-9.]+) for n = %d" % n, readme)
        rd_listed = m2.group(1) if m2 else None
        m3 = re.search(r"The improvement is ([0-9.]+)\.", readme)
        rd_impr = m3.group(1) if m3 else None
        rec_print, rec_exact = frontier_exact(repo, n)
        if n == 157:
            rec_exact = F(13)
        r = rows[n]
        gain = rec_exact - S
        res[str(n)] = {
            "side_40_places_floor": dec(S, 40),
            "floor12": dec(floor_places(S, 12), 12),
            "ceil12": dec(ceil_places(S, 12), 12),
            "brief_claim": {"132": "11.976048383604", "157": "12.993302611344"}[str(n)],
            "brief_claim_is_ceil12": F({"132": "11.976048383604", "157": "12.993302611344"}[str(n)]) == ceil_places(S, 12),
            "issue_new_side": r["new"],
            "issue_new_side_rules": rules(r["new"], S),
            "readme_side": rd_side,
            "readme_side_rules": rules(rd_side, S),
            "issue_equals_readme_print": r["new"] == rd_side,
            "record_print_main": rec_print,
            "record_exact_main": K.frac_text(rec_exact),
            "record_print_rules": rules(rec_print, rec_exact) if n == 132 else "13 exactly",
            "issue_register": r["register"],
            "issue_register_rules": rules(r["register"], rec_exact) if n == 132 else r["register"],
            "readme_listed": rd_listed,
            "readme_listed_rules": rules(rd_listed, rec_exact) if rd_listed and n == 132 else rd_listed,
            "gain_exact_sci": K.sci(gain, 12),
            "issue_gain": r["gain"],
            "issue_gain_matches_3sig": sig_round(gain, 3) == f"{float(r['gain']):.2e}",
            "readme_improvement": rd_impr,
            "readme_improvement_rules": rules(rd_impr, gain) if rd_impr else None,
            "relative_gain_sci": K.sci(gain / rec_exact, 6),
            "gain_in_12th_place_units": str((gain * 10**12).numerator // (gain * 10**12).denominator),
        }
    # The seed's comparison at 109: the record's 6 + (7/2) sqrt(2), and the issue's prints.
    m = re.search(r"side ([0-9.]+), below the register's ([0-9.]+) for n = 109", body)
    seed = {}
    if m:
        seed_print, reg_print = m.group(1), m.group(2)
        # 6 + 3.5 sqrt 2 to 30 places by integer square root
        from math import isqrt

        k = 40
        root2 = F(isqrt(2 * 10 ** (2 * k)), 10**k)  # floor of sqrt 2 at k places
        lo, hi = 6 + F(7, 2) * root2, 6 + F(7, 2) * (root2 + F(1, 10**k))
        reg = F(reg_print)
        kreg = len(reg_print.split(".")[1])
        seed = {
            "issue_seed_side": seed_print,
            "issue_register_109": reg_print,
            "record_109_value_main": frontier_exact(repo, 109)[0],
            "record_109_form": "6 + (7/2)sqrt(2)",
            "record_109_enclosure_30": [dec(lo, 30), dec(hi, 30)],
            "issue_register_109_is_floor": floor_places(lo, kreg) == reg and floor_places(hi, kreg) == reg,
            "issue_register_109_is_nearest": round_places(lo, kreg) == reg and round_places(hi, kreg) == reg,
            "seed_below_record_by_sci": K.sci(lo - F(seed_print), 6),
        }
    out["counts"] = res
    out["seed_109"] = seed
    outp.write_text(json.dumps(out, indent=1) + "\n")
    for n, v in res.items():
        print(n, json.dumps({k: v[k] for k in ("ceil12", "brief_claim_is_ceil12", "issue_new_side_rules", "readme_side_rules", "record_print_rules", "issue_register_rules", "readme_listed_rules", "gain_exact_sci", "issue_gain_matches_3sig", "readme_improvement_rules", "relative_gain_sci")}))
    print("109", json.dumps(seed))


if __name__ == "__main__":
    main()
