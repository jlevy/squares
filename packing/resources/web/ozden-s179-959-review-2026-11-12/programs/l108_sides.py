"""The claim's arithmetic: the side's prints, the gains, s(70) + 5 and the context values.

Lane L108, blind stage 4 review of jlevy/squares#959. Written after the findings were
frozen; decides nothing about the packing. Exact in Fraction where the values are
rational; s(70) and s(207) are number-field values evaluated at 60 digits.

Usage: python -I -B l108_sides.py CERT.yaml CERT954.yaml REPO_ROOT ISSUE.json AUTHOR_DIR OUT.json
"""

from __future__ import annotations

import json
import math
import re
import struct
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath
import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import l108_check as check  # noqa: E402  (print helpers)
import l108_wit as wit  # noqa: E402

mpmath.mp.dps = 60


def floor_places(x: Fraction, k: int) -> Fraction:
    return Fraction(math.floor(x * 10**k), 10**k)


def ceil_places(x: Fraction, k: int) -> Fraction:
    return Fraction(math.ceil(x * 10**k), 10**k)


def fixed(x: Fraction, k: int) -> str:
    """x truncated toward zero at k places, as a fixed-point string."""
    q = floor_places(abs(x), k)
    whole = q.numerator // q.denominator
    frac = (q - whole) * 10**k
    return f"{'-' if x < 0 else ''}{whole}.{int(frac):0{k}d}"


def nearest_binary64_repr(x: Fraction) -> str:
    f = float(x)  # correctly rounded from the exact fraction
    assert struct.unpack("<d", struct.pack("<d", f))[0] == f
    return repr(f)


def side_of(path: Path) -> Fraction:
    return Fraction(yaml.safe_load(path.read_text(encoding="utf-8"))["witness"]["side"])


def main(argv: list[str]) -> int:
    cert, cert954, repo, issue_path, author = Path(argv[1]), Path(argv[2]), Path(argv[3]), Path(argv[4]), Path(argv[5])
    s = side_of(cert)
    s954 = side_of(cert954)
    house_md = (repo / "packing/frontier/n-179.md").read_text(encoding="utf-8")
    m = re.search(r"reported_upper_bound:\n    value: '([0-9.]+)'\n    exact_form: ([0-9]+/[0-9]+)", house_md)
    assert m is not None
    s174_print, s174 = m.group(1), Fraction(m.group(2))
    s174_witness = side_of(repo / "packing/witnesses/known-best/n-179.yaml")
    issue = json.loads(issue_path.read_text(encoding="utf-8"))
    body = issue["body"]
    issue_fraction = re.search(r"`(\d+/\d+) = 13\.88379549051089845`", body)
    claim = Fraction("13.880960371559")
    p70 = wit.load(repo / "packing/witnesses/known-best/n-070.yaml", "n-070")
    p207 = wit.load(repo / "packing/witnesses/known-best/n-207.yaml", "n-207")
    w70 = yaml.safe_load((repo / "packing/witnesses/known-best/n-070.yaml").read_text(encoding="utf-8"))["witness"]
    w207 = yaml.safe_load((repo / "packing/witnesses/known-best/n-207.yaml").read_text(encoding="utf-8"))["witness"]
    s70 = p70.side
    nevska = mpmath.mpf("13.880960371556")
    kirill = Fraction("13.883795490524")
    smp = mpmath.mpf(s.numerator) / s.denominator
    verify_txt = (author / "packing-witness-verify.txt").read_text(encoding="utf-8")
    sqcheck_txt = (author / "sqcheck-output.txt").read_text(encoding="utf-8")
    readme = (author / "README.md").read_text(encoding="utf-8")
    out: dict[str, Any] = {
        "program": "l108_sides.py",
        "side_floor_40": fixed(s, 40),
        "side_floor_12": fixed(floor_places(s, 12), 12),
        "side_ceil_12": fixed(ceil_places(s, 12), 12),
        "claim_is_ceil_12": ceil_places(s, 12) == claim,
        "claim_less_side": check.dec(claim - s),
        "side_floor_15": fixed(floor_places(s, 15), 15),
        "side_ceil_15": fixed(ceil_places(s, 15), 15),
        "side_nearest_binary64_repr": nearest_binary64_repr(s),
        "issue_prints_13_880960371558224": "13.880960371558224" in body,
        "readme_prints_13_880960371558225_ellipsis": "13.880960371558225…" in readme,
        "verify_txt_side_equals_certificate": f"side: {s.numerator}/{s.denominator}" in verify_txt,
        "verify_txt_pairs": re.search(r"pairs tested: (\d+)", verify_txt).group(1),  # type: ignore[union-attr]
        "sqcheck_txt": sqcheck_txt.strip(),
        "sqcheck_print_is_ceil_15": f"s<={fixed(ceil_places(s, 15), 15)}" in sqcheck_txt,
        "t174": {
            "print": s174_print,
            "exact_equals_house_witness_side": s174 == s174_witness,
            "exact_equals_issue_fraction": issue_fraction is not None and Fraction(issue_fraction.group(1)) == s174,
            "print_is_ceil_17": fixed(ceil_places(s174, 17), 17) == s174_print,
            "floor_20": fixed(s174, 20),
            "gain": check.dec(s174 - s, 12),
            "relative_gain": check.dec((s174 - s) / s174, 6),
        },
        "n954": {
            "side_floor_20": fixed(s954, 20),
            "ceil_16": fixed(ceil_places(s954, 16), 16),
            "floor_16": fixed(floor_places(s954, 16), 16),
            "ceil_12": fixed(ceil_places(s954, 12), 12),
            "gain": check.dec(s954 - s, 12),
            "relative_gain": check.dec((s954 - s) / s954, 6),
            "gain_claim_to_claim": check.dec(Fraction("13.881367160110") - claim, 6),
        },
        "s70": {
            "value_60": mpmath.nstr(s70, 40),
            "s70_plus_5": mpmath.nstr(s70 + 5, 40),
            "side_less_s70_plus_5": mpmath.nstr(smp - (s70 + 5), 12),
            "relative_to_side": mpmath.nstr((smp - (s70 + 5)) / smp, 6),
            "claim_less_s70_plus_5": mpmath.nstr(mpmath.mpf("13.880960371559") - (s70 + 5), 6),
            "s70_plus_5_round_12": mpmath.nstr(s70 + 5, 14),
            "nevska_less_s70_plus_5": mpmath.nstr(nevska - (s70 + 5), 6),
            "side_less_nevska": mpmath.nstr(smp - nevska, 6),
            "claim_less_nevska": mpmath.nstr(mpmath.mpf("13.880960371559") - nevska, 6),
            "s70_registry_print_is_ceil_18": mpmath.nstr(s70, 25),
        },
        "s207": {
            "value_60": mpmath.nstr(p207.side, 40),
            "s207_less_s70": mpmath.nstr(p207.side - s70, 30),
            "side_lists_differ_only_in_constant": w70["side"][1:] == w207["side"][1:] and Fraction(w207["side"][0]) - Fraction(w70["side"][0]) == 6,
            "same_field": w70["scalar"] == w207["scalar"],
        },
        "fractional_parts_12": {
            "s70": mpmath.nstr(s70 - 8, 12),
            "s207": mpmath.nstr(p207.side - 14, 12),
            "side_rounded": fixed(Fraction(round(s * 10**12), 10**12) - 13, 12),
            "side_floor": fixed(floor_places(s, 12) - 13, 12),
            "side_ceil": fixed(ceil_places(s, 12) - 13, 12),
        },
        "kirilltym": {"less_house": check.dec(kirill - s174, 6), "less_side": check.dec(kirill - s, 6)},
    }
    Path(argv[6]).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
