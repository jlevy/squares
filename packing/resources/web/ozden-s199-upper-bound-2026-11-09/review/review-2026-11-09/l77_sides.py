"""Exact side arithmetic for #938: the claim, the gap to the record, and every print.

Run: python -I -B l77_sides.py CANDIDATE.yaml STATEMENTS.json MAIN_N199_WITNESS.yaml MAIN_N199_CASE.md OUT.json
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from decimal import Decimal, ROUND_HALF_EVEN, getcontext
from fractions import Fraction as F

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l77_checker as C  # noqa: E402

getcontext().prec = 120


def sha(p: str) -> str:
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def floor_k(x: F, k: int) -> str:
    q = x.numerator * 10**k // x.denominator
    s = str(q).rjust(k + 1, "0")
    return s[:-k] + "." + s[-k:]


def ceil_k(x: F, k: int) -> str:
    q = -((-x.numerator * 10**k) // x.denominator)
    s = str(q).rjust(k + 1, "0")
    return s[:-k] + "." + s[-k:]


def dec(text: str) -> F:
    return F(Decimal(text))


def sig(x: F, digits: int) -> str:
    """x rounded half-even to ``digits`` significant digits, exponent of at least two
    digits (the issue's form, e.g. 2.882e-03)."""
    d = Decimal(x.numerator) / Decimal(x.denominator)
    m, e = f"{d:.{digits - 1}e}".split("e")
    return f"{m}e{int(e):+03d}"


def main() -> int:
    cand, stmts_p, w199_main, case199 = sys.argv[1:5]
    out = sys.argv[5]
    st = json.load(open(stmts_p))
    w = C.read_witness(cand)
    S = F(*w["side"])
    R = F(*C.parse_scalar(st["record_exact"]))
    S172 = S - 1
    # the record as main holds it
    wm = yaml.safe_load(open(w199_main))["witness"]
    R_w = F(*C.parse_scalar(str(wm["side"])))
    fm = yaml.safe_load(open(case199).read().split("---", 2)[1])["packing"]
    R_rep = F(*C.parse_scalar(str(fm["reported_upper_bound"]["exact_form"])))
    R_ver = F(*C.parse_scalar(str(fm["verified_upper_bound"]["exact_form"])))
    gap = R - S
    res: dict = {
        "program": "l77_sides.py",
        "program_sha256": sha(__file__),
        "checker_sha256": sha(os.path.join(HERE, "l77_checker.py")),
        "statements_sha256": sha(stmts_p),
        "side": C.q_str(S),
        "side_denominator_digits": len(str(S.denominator)),
        "side_terminates": all(p in (2, 5) for p in _small_factors(S.denominator)),
        "side_floor_40": floor_k(S, 40),
        "S172_floor_40": floor_k(S172, 40),
        "record_equals_main_witness_side": R == R_w,
        "record_equals_case_reported": R == R_rep,
        "record_equals_case_verified": R == R_ver,
        "record_floor_30": floor_k(R, 30),
        "record_exact_decimal_places": 30 if R * 10**30 == int(R * 10**30) else None,
    }
    checks = {}
    checks["claim_is_12_place_ceiling"] = ceil_k(S, 12) == st["claim_12_places"]
    checks["claim_bounds_side"] = dec(st["claim_12_places"]) >= S
    checks["12_place_floor_below_side"] = dec(floor_k(S, 12)) < S
    res["claim_minus_side"] = float(dec(st["claim_12_places"]) - S)
    res["gap_record_minus_side"] = {"exact": C.q_str(gap), "12_sig": sig(gap, 12), "float": float(gap)}
    res["relative_gap_over_record"] = sig(gap / R, 6)
    res["relative_gap_over_side"] = sig(gap / S, 6)
    checks["gap_positive"] = gap > 0
    checks["improvement_print_is_gap_4_sig"] = sig(gap, 4) == st["improvement"]
    checks["relative_print_is_gap_over_record_3_sig"] = sig(gap / R, 3) == st["relative_improvement"]
    res["gap_in_units_of_1e-12"] = float(gap * 10**12)
    res["gap_in_binary64_spacings_at_side"] = float(gap / F(2) ** (-49))  # ulp(14.6) = 2^-49
    # prints
    checks["record_print_is_16_place_ceiling"] = ceil_k(R, 16) == st["record_print_issue"]
    res["record_16_floor_ceiling"] = [floor_k(R, 16), ceil_k(R, 16)]
    res["S172_16_floor_ceiling"] = [floor_k(S172, 16), ceil_k(S172, 16)]
    checks["s172_issue_print_is_16_place_ceiling"] = ceil_k(S172, 16) == st["s172_print_issue"]
    r11 = st["s172_print_readme_line11"].rstrip("…")
    res["readme_line11_print"] = {
        "print": st["s172_print_readme_line11"],
        "is_16_floor": r11 == floor_k(S172, 16),
        "is_16_ceiling": r11 == ceil_k(S172, 16),
        "print_minus_S172": float(dec(r11) - S172),
    }
    checks["readme_line7_is_15_place_floor"] = st["side_print_readme_line7"].rstrip("…") == floor_k(S, 15)
    checks["sqcheck_print_is_15_place_ceiling"] = st["side_print_sqcheck_candidate"] == ceil_k(S, 15)
    checks["verify_print_is_side_exactly"] = F(*C.parse_scalar(st["side_exact_verify_print"])) == S
    checks["pairs_tested_is_all_pairs"] = st["pairs_tested"] == 199 * 198 // 2
    c13 = dec(st["side_print_comment"])
    res["comment_print"] = {"is_13_floor": st["side_print_comment"] == floor_k(S, 13),
                            "minus_side": float(c13 - S)}
    pose = dec(st["pose_side"])
    res["pose_side"] = {
        "pose_side_minus_certificate_side": float(pose - S),
        "dilated_1e-24_15_place_ceiling": ceil_k(pose * (1 + F(1, 10**24)), 15),
        "sqcheck_pose_print_matches_dilated_ceiling": ceil_k(pose * (1 + F(1, 10**24)), 15)
        == st["pose_side_print_sqcheck"],
        "pose_side_15_place_ceiling_undilated": ceil_k(pose, 15),
    }
    kag = dec(st["kaggle_published_kirilltym"])
    so = dec(st["kaggle_side_only_oigazhdn"])
    res["context"] = {
        "kirilltym_minus_side": float(kag - S),
        "kirilltym_minus_record": float(kag - R),
        "side_minus_side_only_entry": float(S - so),
        "side_only_entry_below_side": so < S,
    }
    checks["comment_difference_print"] = f"+{sig(S - so, 2)}" == st["comment_difference_to_side_only"]
    checks["kirilltym_above_side_and_record"] = kag > S and kag > R
    res["checks"] = checks
    res["verdict"] = "SIDES_AS_STATED" if all(checks.values()) else "SEE_CHECKS"
    with open(out, "w") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    print(json.dumps(res, indent=1))
    return 0


def _small_factors(n: int) -> set[int]:
    fs = set()
    for p in (2, 3, 5, 7, 11, 13):
        while n % p == 0:
            fs.add(p)
            n //= p
    if n > 1:
        fs.add(n)
    return fs


if __name__ == "__main__":
    sys.exit(main())
