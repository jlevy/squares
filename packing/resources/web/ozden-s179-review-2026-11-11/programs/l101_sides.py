"""The claim's arithmetic, after the freeze. Decides no packing.

Usage: python -I -B l101_sides.py SOURCE_DIR ISSUE.json REPO_ROOT OUT.json

Exactly: the certificate's side S to 40 places, its 12- and 15-place floors and
ceilings, against the issue's claim and the author's prints (README, packing-witness
verify, sqcheck); the house side at 179 (case record `exact_form`, house witness `side`,
the issue's stated fraction) and the gain and relative gain; the context values the issue
quotes; and the 70 and 207 sides the issue cites, from the case records' printed roots.
"""

from __future__ import annotations

import json
import re
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.set_int_max_str_digits(0)

import yaml  # noqa: E402

import l101_reader as reader  # noqa: E402
from l101_check import frac_str, sci, sha256_file  # noqa: E402



def places(x: F, k: int, up: bool) -> F:
    scale = 10**k
    q, r = divmod(x.numerator * scale, x.denominator)
    if up and r:
        q += 1
    return F(q, scale)


def show(x: F, k: int) -> str:
    """x written to k places, truncated (exact for a k-place value)."""
    scale = 10**k
    q = (x.numerator * scale) // x.denominator
    whole, frac = divmod(q, scale)
    return f"{whole}.{frac:0{k}d}"



def rounds_to(exact: F, printed: str) -> dict:
    """How a printed decimal relates to an exact value: floor, ceiling or nearest."""
    k = len(printed.split(".")[1])
    p = F(printed)
    return {
        "printed": printed,
        "places": k,
        "is_floor": p == places(exact, k, up=False),
        "is_ceiling": p == places(exact, k, up=True),
        "is_nearest": abs(p - exact) <= F(1, 2 * 10**k),
        "printed_less_exact": sci(p - exact, 6),
    }


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---", 2)[1])


def main() -> int:
    src, issue_path, repo, out = (Path(a) for a in sys.argv[1:5])
    w = reader.read_files(src / "n-179-candidate.yaml", src / "n179-witness.json", 179)
    s = F(*w.side)
    issue = json.loads(issue_path.read_text(encoding="utf-8"))["body"]
    record = frontmatter(repo / "packing/frontier/n-179.md")["packing"]
    house_side_text = yaml.safe_load((repo / "packing/witnesses/known-best/n-179.yaml").read_text(
        encoding="utf-8"))["witness"]["side"]
    h_record = F(record["verified_upper_bound"]["exact_form"])
    h_witness = F(str(house_side_text))
    issue_fraction = re.search(r"The record holds `([0-9]+/[0-9]+) = ([0-9.]+)`", issue)
    assert issue_fraction is not None
    h_issue = F(issue_fraction[1])
    h = h_record
    gap = h - s
    readme = (src / "README.md").read_text(encoding="utf-8")
    readme_s = re.search(r"`S = ([0-9.]+)…`", readme)
    verify = (src / "packing-witness-verify.txt").read_text(encoding="utf-8")
    verify_side = re.search(r"side: ([0-9]+/[0-9]+)", verify)
    sqcheck = (src / "sqcheck-output.txt").read_text(encoding="utf-8")
    sq_side = re.search(r"s<=([0-9.]+)", sqcheck)
    assert readme_s and verify_side and sq_side
    c = F("13.881367160110")
    nevska = F("13.880960371556")
    kirill = F("13.883795490524")
    rec70 = frontmatter(repo / "packing/frontier/n-070.md")["packing"]["reported_upper_bound"]
    rec207 = frontmatter(repo / "packing/frontier/n-207.md")["packing"]["reported_upper_bound"]
    root70 = F(re.search(r"root\([^,]+, ([0-9.]+)", rec70["exact_form"])[1])
    root207 = F(re.search(r"root\([^,]+, ([0-9.]+)", rec207["exact_form"])[1])
    result = {
        "program": "l101_sides.py",
        "certificate_sha256": sha256_file(src / "n-179-candidate.yaml"),
        "side": {
            "fraction_digits": [len(str(s.numerator)), len(str(s.denominator))],
            "terminates": places(s, 400, up=False) == s,
            "floor_40": show(s, 40),
            "floor_12": show(places(s, 12, up=False), 12),
            "ceiling_12": show(places(s, 12, up=True), 12),
            "floor_15": show(places(s, 15, up=False), 15),
            "ceiling_15": show(places(s, 15, up=True), 15),
        },
        "claim": {"printed": "13.881367160110", **rounds_to(s, "13.881367160110"),
                  "claim_above_side": c > s, "claim_less_side": sci(c - s, 6)},
        "author_prints": {
            "readme_S": {**rounds_to(s, readme_s[1]), "note": "followed by an ellipsis"},
            "packing_witness_verify_side_equals_certificate": F(verify_side[1]) == s
            and verify_side[1] == frac_str(s),
            "packing_witness_verify_pairs": re.search(r"pairs tested: ([0-9]+)", verify)[1],
            "pairs_n_choose_2": 179 * 178 // 2,
            "sqcheck_side": rounds_to(s, sq_side[1]),
        },
        "house": {
            "record_exact_form_equals_witness_side": h_record == h_witness,
            "issue_fraction_equals_record": h_issue == h_record,
            "issue_print": rounds_to(h, issue_fraction[2]),
            "record_value": rounds_to(h, record["verified_upper_bound"]["value"]),
            "floor_20": show(h, 20),
            "credits": {"found_by": record["reported_upper_bound"]["found_by"],
                        "improved_by": record["reported_upper_bound"]["improved_by"]},
        },
        "gain": {
            "exact_positive": gap > 0,
            "gap": sci(gap, 12),
            "issue_gap": "2.428e-03",
            "gap_rounds_to_issue": f"{float(gap):.3e}" == "2.428e-03",
            "relative_to_house": sci(gap / h, 6),
            "relative_to_new": sci(gap / s, 6),
            "issue_relative": "1.75e-04",
            "relative_rounds_to_issue": f"{float(gap / h):.2e}" == "1.75e-04",
            "gap_in_units_of_12th_place": str(int(gap * 10**12)),
        },
        "context": {
            "nevska_below_claim": sci(c - nevska, 6),
            "nevska_below_claim_rounds_to_4.07e-4": f"{float(c - nevska):.2e}" == "4.07e-04",
            "nevska_below_side": sci(s - nevska, 6),
            "kirilltym_above_claim": sci(kirill - c, 6),
            "kirilltym_above_house": sci(kirill - h, 6),
            "kirilltym_is_house_rounded_12": show(places(h, 12, up=True), 12),
            "nevska_less_5_is_70_print_12": nevska - 5 == places(root70, 12, up=True),
            "frac_70_12_places": show(places(root70 - 8, 12, up=True), 12),
            "frac_207_12_places": show(places(root207 - 14, 12, up=True), 12),
            "frac_side_12_places": show(places(s - 13, 12, up=True), 12),
            "root207_less_root70": str(root207 - root70),
            "issue_70_print": rounds_to(root70, "8.880960371555579595"),
            "record_70_credits": {
                "found_by": rec70["found_by"], "improved_by": rec70["improved_by"]},
            "record_207_credits": {
                "found_by": rec207["found_by"], "improved_by": rec207["improved_by"]},
        },
    }
    Path(out).write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
