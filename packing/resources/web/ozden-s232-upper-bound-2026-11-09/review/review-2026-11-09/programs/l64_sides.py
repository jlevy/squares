"""Sides, prints and gaps of the five certificates of issues 927 to 931 (lane L64).

Usage: python -I -B l64_sides.py STATEMENTS.json SRC_DIR HOUSE_DIR RESULTS_YAML OUT.json

All arithmetic is exact. For each count it reads the certificate with the frozen reader,
and the house witness `n-NNN.yaml` on main with `l64_house.py`, and computes:

- the side in lowest terms, whether it is a terminating decimal, and its 40-place floor;
- the side's 12-place ceiling and floor, and whether the issue's claim is the ceiling;
- the extent of the corners, to say which walls fix the side;
- the record side (the house witness's `side`), its equality with the issue's record
  fraction and with the register entry's claim on main, and the exact gap and relative
  gap, with the issue's 4- and 3-significant-digit prints checked against them;
- the gap in units of the 12th place and of the binary64 spacing at the side;
- the issue's Kaggle context value against the side.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml  # noqa: E402

from l64_house import read_house  # noqa: E402
from l64_reader import read_witness  # noqa: E402
from l64_util import (  # noqa: E402
    Clock,
    ceil_places,
    environment,
    exp10,
    fixed,
    floor_places,
    frac_str,
    program_digests,
    sci,
    write_receipt,
)

HERE = Path(__file__).resolve().parent


def round_sig(x: F, digits: int) -> str:
    """x rounded to nearest (ties away from zero) at `digits` significant digits, as d.ddde-XX."""
    sign = "-" if x < 0 else ""
    a = abs(x)
    e = exp10(a)
    scaled = a / F(10) ** e * 10 ** (digits - 1)
    q, r = divmod(scaled.numerator, scaled.denominator)
    if 2 * r >= scaled.denominator:
        q += 1
    if q == 10**digits:
        q //= 10
        e += 1
    s = str(q)
    return f"{sign}{s[0]}.{s[1:]}e{e:+03d}"


def parse_decimal(text: str) -> F:
    whole, _, frac = text.partition(".")
    return F(int(whole + frac), 10 ** len(frac)) if frac else F(int(whole))


def terminating(x: F) -> bool:
    d = x.denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return d == 1


def binary64_spacing(x: F) -> F:
    """The spacing of binary64 numbers at x > 0: 2**(e - 52) for 2**e <= x < 2**(e + 1)."""
    e = x.numerator.bit_length() - x.denominator.bit_length()
    while F(2) ** e > x:
        e -= 1
    while F(2) ** (e + 1) <= x:
        e += 1
    return F(2) ** (e - 52)


def register_claims(results_yaml: Path, ids: set[str]) -> dict[str, str]:
    loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
    doc = yaml.load(results_yaml.read_text(encoding="utf-8"), Loader=loader)  # noqa: S506
    return {r["id"]: r.get("claim", "") for r in doc["results"] if r.get("id") in ids}


def main(argv: list[str]) -> int:
    if len(argv) != 6:
        print(__doc__)
        return 2
    statements = json.loads(Path(argv[1]).read_text())["counts"]
    src, house_dir, results_yaml, out = Path(argv[2]), Path(argv[3]), Path(argv[4]), argv[5]
    clock = Clock()
    claims = register_claims(results_yaml, {s["record_entry"] for s in statements.values()})
    rows = {}
    for n_text, st in statements.items():
        n = int(n_text)
        w = read_witness(src / st["repo"] / st["certificate"], expected_n=n)
        side = F(*w["side"])
        xs = [F(c[0], c[1]) for sq in w["squares"] for c in sq["corners"]]
        ys = [F(c[2], c[3]) for sq in w["squares"] for c in sq["corners"]]
        house = read_house(house_dir / f"n-{n:03d}.yaml", expected_n=n)
        record = F(*house["side"])
        rec_issue = F(st["record_fraction"])
        claim = parse_decimal(st["claim_12"])
        ceil12, floor12 = ceil_places(side, 12), floor_places(side, 12)
        gap = record - side
        rel = gap / record
        reg_text = claims.get(st["record_entry"], "")
        exact_dec = fixed(record, 60, "floor").rstrip("0") if terminating(record) else None
        in_register = st["record_fraction"] in reg_text or (
            exact_dec is not None and exact_dec in reg_text
        )
        unit12 = F(1, 10**12)
        repo = src / st["repo"]
        pwv = (repo / "packing-witness-verify.txt").read_text(encoding="ascii")
        pwv_side = [ln.split("side:", 1)[1].strip() for ln in pwv.splitlines() if ln.strip().startswith("side:")]
        sqc = (repo / "sqcheck-output.txt").read_text(encoding="ascii").split()
        sqc_side = [tok[3:] for tok in sqc if tok.startswith("s<=")]
        prints = {
            "packing_witness_verify_first_line": pwv.splitlines()[0],
            "packing_witness_verify_side_equals_side": len(pwv_side) == 1 and F(pwv_side[0]) == side,
            "sqcheck_first_token": sqc[0],
            "sqcheck_print": sqc_side[0] if sqc_side else None,
            "sqcheck_print_is_ceil_15": bool(sqc_side) and sqc_side[0] == fixed(side, 15, "ceil"),
            "sqcheck_print_minus_side": sci(parse_decimal(sqc_side[0]) - side, 6) if sqc_side else None,
        }
        rows[n_text] = {
            "author_prints": prints,
            "issue": st["issue"],
            "side": frac_str(side),
            "side_denominator_digits": len(str(side.denominator)),
            "side_terminating_decimal": terminating(side),
            "side_floor_40": fixed(side, 40, "floor"),
            "ceil_12": fixed(side, 12, "ceil"),
            "floor_12": fixed(side, 12, "floor"),
            "claim_12": st["claim_12"],
            "claim_is_ceil_12": claim == ceil12,
            "claim_minus_side": sci(claim - side, 6),
            "side_minus_floor_12": sci(side - floor12, 6),
            "extent": {
                "min_x": frac_str(min(xs)),
                "min_y": frac_str(min(ys)),
                "side_minus_max_x": sci(side - max(xs), 6),
                "side_minus_max_y": sci(side - max(ys), 6),
                "side_is_max_extent": side == max(max(xs), max(ys)),
            },
            "record_entry": st["record_entry"],
            "record_side": frac_str(record),
            "record_floor_20": fixed(record, 20, "floor"),
            "record_equals_issue_fraction": record == rec_issue,
            "record_in_register_claim_on_main": in_register,
            "record_print_in_issue": st["record_print"],
            "record_print_is_floor_16": fixed(record, 16, "floor") == st["record_print"],
            "record_print_is_ceil_16": fixed(record, 16, "ceil") == st["record_print"],
            "record_print_is_binary64_to_16_places": f"{float(record):.16f}" == st["record_print"],
            "record_print_minus_record": sci(parse_decimal(st["record_print"]) - record, 6),
            "gap": frac_str(gap),
            "gap_sci": sci(gap, 12),
            "gap_positive": gap > 0,
            "gap_4sig": round_sig(gap, 4),
            "issue_improvement": st["improvement"],
            "issue_improvement_matches_4sig": round_sig(gap, 4) == st["improvement"],
            "relative_gap_sci": sci(rel, 6),
            "relative_3sig": round_sig(rel, 3),
            "issue_relative": st["relative"],
            "issue_relative_matches_3sig": round_sig(rel, 3) == st["relative"],
            "gap_in_12th_place_units": str((gap / unit12).numerator // (gap / unit12).denominator),
            "gap_in_binary64_spacings_at_side": str(
                (gap / binary64_spacing(side)).numerator // (gap / binary64_spacing(side)).denominator
            ),
            "claim_below_record": claim < record,
            "kaggle_context": st["kaggle_best"],
            "kaggle_above_side": parse_decimal(st["kaggle_best"]) > side,
            "kaggle_above_claim": parse_decimal(st["kaggle_best"]) > claim,
        }
    receipt = {
        "program": "l64_sides.py",
        "programs_sha256": program_digests([HERE / f for f in ("l64_sides.py", "l64_house.py", "l64_reader.py", "l64_util.py")]),
        "environment": environment(),
        "counts": rows,
        "clock": clock.report(),
    }
    write_receipt(out, receipt)
    for n_text, r in rows.items():
        print(
            n_text,
            r["ceil_12"],
            "claim ok" if r["claim_is_ceil_12"] else "CLAIM DIFFERS",
            "gap",
            r["gap_sci"],
            "issue",
            r["issue_improvement"],
            r["issue_improvement_matches_4sig"],
            r["issue_relative_matches_3sig"],
            "record ok" if r["record_equals_issue_fraction"] and r["record_in_register_claim_on_main"] else "RECORD?",
        )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
