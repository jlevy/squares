"""Lane L109's arithmetic of the claim, written after the findings were frozen.

Usage: python -I -B l109_sides.py CERT.yaml TWIN.json ISSUE.json REPO_ROOT SOURCE_DIR OUT.json

Decides nothing about the packing. Computes exactly: the side's decimal prints, the
12-place floor and ceiling, the claim less the side, the record's sides at 237 (the case
record's reported and verified `exact_form`, the house witness's `side`, and T-189's
claim in the register), the gain and the relative gain, and the context values the
issue quotes; and compares the issue's, the README's and the author's printed outputs'
numbers with them.
"""

from __future__ import annotations

import json
import os
import re
import sys
from fractions import Fraction as Q

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l109_check as C  # noqa: E402
import l109_reader as R  # noqa: E402

PROGRAMS = ["l109_reader.py", "l109_check.py", "l109_sides.py"]


def floor_places(q: Q, k: int) -> str:
    f = (q.numerator * 10**k) // q.denominator
    s = str(f).rjust(k + 1, "0")
    return f"{s[:-k]}.{s[-k:]}"


def ceil_places(q: Q, k: int) -> str:
    f = -((-q.numerator * 10**k) // q.denominator)
    s = str(f).rjust(k + 1, "0")
    return f"{s[:-k]}.{s[-k:]}"


def round_places(q: Q, k: int) -> str:
    f = (2 * q.numerator * 10**k + q.denominator) // (2 * q.denominator)
    s = str(f).rjust(k + 1, "0")
    return f"{s[:-k]}.{s[-k:]}"


def dec(s: str) -> Q:
    return Q(s)


def sci(q: Q, digits: int = 6) -> str:
    return f"{float(q):.{digits}e}"


def main() -> int:
    cert, twin, issue_path, repo, src, out = sys.argv[1:7]
    rd = R.read_files(cert, twin)
    side = Q(*rd.side)
    with open(issue_path, encoding="utf-8") as f:
        issue = json.load(f)
    body = issue["body"]
    with open(os.path.join(repo, "packing/frontier/n-237.md"), encoding="utf-8") as f:
        case = f.read()
    m = re.search(r"reported_upper_bound:\n    value: '([0-9.]+)'\n    exact_form: ([0-9/]+)\n", case)
    assert m
    rep_value, rep_exact = m.group(1), Q(m.group(2))
    m = re.search(r"verified_upper_bound:\n    value: '([0-9.]+)'\n    exact_form: ([0-9/]+)\n", case)
    assert m
    ver_value, ver_exact = m.group(1), Q(m.group(2))
    with open(os.path.join(repo, "packing/witnesses/known-best/n-237.yaml"), encoding="utf-8") as f:
        wit = f.read()
    m = re.search(r"\n  side: ([0-9/]+)\n", wit)
    assert m
    house = Q(m.group(1))
    with open(os.path.join(repo, "packing/frontier/results.yaml"), encoding="utf-8") as f:
        res = f.read()
    i = res.index("  - id: T-189\n")
    j = res.index("\n  - id: T-190\n", i)
    m = re.search(r"s\(237\) <=\s+([0-9]+/[0-9]+)", res[i:j])
    assert m
    t189_claim = Q(m.group(1))
    claim = Q("15.893805580573")
    elegans = Q("15.893805585209")
    kirill = Q("15.902603638274")
    with open(os.path.join(src, "packing-witness-verify.txt"), encoding="utf-8") as f:
        pwv = f.read()
    with open(os.path.join(src, "sqcheck-output.txt"), encoding="utf-8") as f:
        sqc = f.read()
    m = re.search(r"\n  side: ([0-9/]+)\n", pwv)
    pwv_side = Q(m.group(1)) if m else None
    m = re.search(r"s<=([0-9.]+)", sqc)
    sqc_print = m.group(1) if m else None
    gain = house - side
    receipt = {
        "program": "l109_sides.py",
        "programs_sha256": C.program_digests(PROGRAMS),
        "side": {
            "floor_40": floor_places(side, 40),
            "floor_12": floor_places(side, 12),
            "ceil_12": ceil_places(side, 12),
            "floor_15": floor_places(side, 15),
            "ceil_15": ceil_places(side, 15),
            "round_15": round_places(side, 15),
            "floor_16": floor_places(side, 16),
            "ceil_16": ceil_places(side, 16),
            "round_16": round_places(side, 16),
            "numerator_digits": len(str(side.numerator)),
            "denominator_digits": len(str(side.denominator)),
            "denominator_factor_note": "the denominator is printed in full in the certificate",
        },
        "claim": {
            "claim_is_ceil_12": ceil_places(side, 12) == "15.893805580573",
            "claim_less_side": sci(claim - side),
        },
        "record": {
            "case_reported_value": rep_value,
            "case_reported_exact": str(rep_exact),
            "case_verified_value": ver_value,
            "case_verified_exact_equals_reported": ver_exact == rep_exact,
            "house_witness_side_equals_case_exact": house == rep_exact,
            "house_floor_20": floor_places(house, 20),
            "house_value_is_ceil_16": ceil_places(house, 16) == rep_value,
            "t189_claim": str(t189_claim),
            "t189_claim_floor_25": floor_places(t189_claim, 25),
            "t189_claim_equals_house": t189_claim == house,
            "house_less_t189_claim": sci(house - t189_claim) if house != t189_claim else "0",
            "issue_states_exact": "7951301819129798440089572127137/500000000000000000000000000000" in body,
        },
        "gain": {
            "house_less_side": sci(gain, 9),
            "relative_to_house": sci(gain / house, 6),
            "t189_claim_less_side": sci(t189_claim - side, 9),
            "issue_8.798e-03": f"{float(gain):.3e}" == "8.798e-03",
            "issue_relative_5.53e-04": f"{float(gain / house):.2e}" == "5.53e-04",
            "side_less_house_negative": side - house < 0,
        },
        "context": {
            "elegans_less_side": sci(elegans - side),
            "elegans_less_claim": sci(elegans - claim),
            "issue_4.64e-9": f"{float(elegans - side):.2e}" == "4.64e-09",
            "kirilltym_less_house": sci(kirill - house),
            "kirilltym_less_side": sci(kirill - side),
            "issue_8.80e-3_below_record": f"{float(gain):.2e}" == "8.80e-03",
            "issue_exact_side_print_16": "15.8938055805725735" in body,
            "readme_print": "15.893805580572574…",
            "binary64_of_side": repr(float(side)),
            "binary64_of_side_exact_floor_19": floor_places(Q(float(side)), 19),
            "binary64_of_side_less_side": sci(Q(float(side)) - side),
            "issue_print_16_is_binary64_rounded_16": round_places(Q(float(side)), 16) == "15.8938055805725735",
            "issue_print_16_less_side": sci(Q("15.8938055805725735") - side),
        },
        "author_prints": {
            "packing_witness_verify_side_equals": pwv_side == side,
            "packing_witness_verify_pairs": re.search(r"pairs tested: ([0-9]+)", pwv).group(1) if re.search(r"pairs tested: ([0-9]+)", pwv) else None,
            "pairs_expected": rd.n * (rd.n - 1) // 2,
            "sqcheck_print": sqc_print,
            "sqcheck_print_is_ceil_15": sqc_print == ceil_places(side, 15),
            "sqcheck_print_is_round_15": sqc_print == round_places(side, 15),
        },
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=1)
        f.write("\n")
    print(json.dumps(receipt, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
