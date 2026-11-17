"""Sides, prints, extents and gaps against the houses (lane L72, bead think-qqyg).

Usage: python -I -B l72_sides.py STATEMENTS.json SRC REPO_ROOT OUT.json

Exact arithmetic on the certificates' sides (read by the frozen reader) and on the house
witnesses on main (read by l72_house): each claim against the side's 12-place ceiling, the
extents, the gap and relative gap against each house with the issues' rounded prints, the
author's printed sides, the README's print, the decimal pose's side and the Kaggle values
the issues quote. Decides no bound.
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fractions import Fraction  # noqa: E402

import l72_house as house  # noqa: E402
import l72_reader as reader  # noqa: E402
import l72_sat as sat  # noqa: E402
import l72_util as util  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def dec(text):
    """A decimal string as an exact Fraction."""
    text = text.strip()
    m = re.fullmatch(r"(-?)(\d+)(?:\.(\d+))?(?:e([+-]?\d+))?", text)
    if not m:
        raise ValueError(text)
    sign, ip, fp, ex = m.groups()
    fp = fp or ""
    v = Fraction(int(ip + fp), 10 ** len(fp))
    if ex:
        v *= Fraction(10) ** int(ex)
    return -v if sign else v


def round_sig(x, sig):
    """x rounded half-up to `sig` significant digits, as 'd.ddde-XX'."""
    x = Fraction(x)
    e = len(str(x.numerator)) - len(str(x.denominator))
    while Fraction(10) ** e > x:
        e -= 1
    while Fraction(10) ** (e + 1) <= x:
        e += 1
    m = x / Fraction(10) ** e * 10 ** (sig - 1)
    k = int(m + Fraction(1, 2))
    if k == 10**sig:
        k //= 10
        e += 1
    s = str(k)
    return f"{s[0]}.{s[1:]}e{e:+03d}"


def ulp64(x):
    """The binary64 spacing at a positive x (a power of two)."""
    e = 0
    while Fraction(2) ** (e + 1) <= x:
        e += 1
    while Fraction(2) ** e > x:
        e -= 1
    return Fraction(2) ** (e - 52)


def terminates(q):
    for p in (2, 5):
        while q % p == 0:
            q //= p
    return q == 1


def main(argv):
    statements = json.load(open(argv[1]))
    src, repo_root, out = argv[2], argv[3], argv[4]
    report = {"program": "l72_sides.py", "lane": "L72", "bead": "think-qqyg", "environment": util.environment()}
    report["program_digests"] = util.program_digests(
        [os.path.join(HERE, f) for f in ("l72_sides.py", "l72_house.py", "l72_reader.py", "l72_sat.py", "l72_util.py")] + [argv[1]]
    )
    problems = []
    for count in ("172", "270"):
        st = statements[count]
        repo = os.path.join(src, st["repository"].split("/")[1])
        data = reader.read_files(os.path.join(repo, st["certificate"]))
        p, q = data["side"]
        S = Fraction(p, q)
        P = [sat.corners_frac(c) for c in data["corners"]]
        xs = [pt[0] for Q in P for pt in Q]
        ys = [pt[1] for Q in P for pt in Q]
        ceil12 = util.ceil_decimal(S, 12)
        floor12 = util.floor_decimal(S, 12)
        claim = st["claim"]
        row = {
            "side": util.frac_str(S),
            "numerator_digits": len(str(p)),
            "denominator_digits": len(str(q)),
            "expansion_terminates": terminates(q),
            "floor_20": util.floor_decimal(S, 20),
            "floor_40": util.floor_decimal(S, 40),
            "floor_12": floor12,
            "ceil_12": ceil12,
            "claim": claim,
            "claim_is_ceil_12": claim == ceil12,
            "claim_minus_side": util.sci(dec(claim) - S, 6),
            "side_minus_floor_12": util.sci(S - dec(floor12), 6),
            "extents": {
                "least_x": util.frac_str(min(xs)),
                "least_y": util.frac_str(min(ys)),
                "side_equals_greatest_x": max(xs) == S,
                "side_equals_greatest_y": max(ys) == S,
                "side_minus_greatest_x": util.sci(S - max(xs), 6),
                "side_minus_greatest_y": util.sci(S - max(ys), 6),
            },
        }
        if claim != ceil12:
            problems.append(f"{count}: the claim is not the 12-place ceiling")
        # the house
        hw = house.read_center_basis(os.path.join(repo_root, st["house_witness"]))
        H = Fraction(*hw["side"])
        gap = H - S
        rel = gap / H
        row["house"] = {
            "entry": st["record_entry"],
            "witness": st["house_witness"],
            "witness_id": hw["witness_id"],
            "side": util.frac_str(H),
            "equals_issue_fraction": H == Fraction(*map(int, st["record_fraction"].split("/"))),
            "floor_20": util.floor_decimal(H, 20),
            "ceil_16": util.ceil_decimal(H, 16),
            "issue_print": st["record_print"],
            "issue_print_is_ceil_16": util.ceil_decimal(H, 16) == st["record_print"],
        }
        row["gap"] = {
            "exact": util.frac_str(gap),
            "sci_12_truncated": util.sci(gap, 12),
            "rounded_4_sig": round_sig(gap, 4),
            "issue_improvement": st["improvement"],
            "issue_improvement_is_rounded_gap": round_sig(gap, 4) == st["improvement"].replace("e-0", "e-0"),
            "relative_sci_12": util.sci(rel, 12),
            "relative_rounded_3_sig": round_sig(rel, 3),
            "issue_relative": st["relative"],
            "issue_relative_is_rounded": round_sig(rel, 3) == st["relative"],
            "units_of_12th_place": util.sci(gap * 10**12, 6),
            "binary64_spacings_at_side": util.sci(gap / ulp64(S), 6),
            "binary64_spacing_at_side": util.sci(ulp64(S), 6),
        }
        if gap <= 0:
            problems.append(f"{count}: the side is not below the house")
        # the author's prints
        pwv = open(os.path.join(repo, "packing-witness-verify.txt"), encoding="utf-8").read()
        m = re.search(r"^\s*side:\s*(\d+)/(\d+)\s*$", pwv, re.M)
        pwv_side = Fraction(int(m.group(1)), int(m.group(2))) if m else None
        m2 = re.search(r"pairs tested:\s*(\d+)", pwv)
        sqc = open(os.path.join(repo, "sqcheck-output.txt"), encoding="utf-8").read()
        m3 = re.search(r"s<=([0-9.]+)", sqc)
        sq_print = m3.group(1) if m3 else None
        places = len(sq_print.split(".")[1]) if sq_print else 0
        readme_print = st["readme_side_print"].rstrip("…")
        rplaces = len(readme_print.split(".")[1])
        row["prints"] = {
            "packing_witness_verify_side_equals": pwv_side == S,
            "packing_witness_verify_verdict": pwv.split("\n", 1)[0].strip(),
            "packing_witness_verify_pairs": int(m2.group(1)) if m2 else None,
            "pairs_n_choose_2": data["n"] * (data["n"] - 1) // 2,
            "sqcheck_line": sqc.strip(),
            "sqcheck_print": sq_print,
            "sqcheck_print_is_ceil": sq_print == util.ceil_decimal(S, places),
            "sqcheck_print_places": places,
            "sqcheck_print_minus_side": util.sci(dec(sq_print) - S, 4) if sq_print else None,
            "readme_print": st["readme_side_print"],
            "readme_print_is_floor": readme_print == util.floor_decimal(S, rplaces),
            "readme_print_places": rplaces,
        }
        # the decimal pose's own side, and the context values
        pose = reader.yaml_tree(open(os.path.join(repo, st["pose"]), encoding="utf-8").read())
        pose_side = dec(pose["witness"]["side"])
        K = dec(st["kaggle"])
        row["pose_side"] = {
            "print": pose["witness"]["side"],
            "minus_side": util.sci(pose_side - S, 6),
            "pose_schema": pose["softschema"].get("schema"),
            "pose_representation": pose["witness"]["representation"],
            "pose_angle_unit": pose["witness"]["coordinates"]["angle_unit"],
            "pose_claim": pose["witness"]["claim"],
        }
        row["kaggle"] = {
            "value": st["kaggle"],
            "minus_side": util.sci(K - S, 6),
            "minus_claim": util.sci(K - dec(claim), 6),
            "minus_house": util.sci(K - H, 6),
        }
        report[count] = row
    report["problems"] = problems
    report["verdict"] = "SIDES_AS_STATED" if not problems else "SIDE_PROBLEMS"
    util.write_receipt(out, report)
    print(json.dumps({c: {k: v for k, v in report[c].items() if k not in ("floor_40",)} for c in ("172", "270")}, indent=1))
    print(report["verdict"], problems)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
