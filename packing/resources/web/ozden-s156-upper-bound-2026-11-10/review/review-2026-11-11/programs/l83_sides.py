"""Exact side arithmetic, claims, gaps and the author's prints (review L83).

Usage: python -I -B l83_sides.py SRC_DIR KNOWN_BEST_DIR STATEMENTS.json OUT.json
"""

from __future__ import annotations

import json
import re
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l83_check as C  # noqa: E402
import l83_house as H  # noqa: E402
import l83_reader as R  # noqa: E402


def floor_places(x: F, k: int) -> F:
    s = x * 10**k
    return F(s.numerator // s.denominator, 10**k)


def ceil_places(x: F, k: int) -> F:
    f = floor_places(x, k)
    return f if f == x else f + F(1, 10**k)


def dec(x: F, k: int) -> str:
    """x truncated to k places, as text."""
    f = floor_places(x, k)
    s = str(f.numerator * 10**k // f.denominator)
    neg = s.startswith("-")
    s = s.lstrip("-").rjust(k + 1, "0")
    return ("-" if neg else "") + s[:-k] + "." + s[-k:]


def which(print_text: str, x: F) -> str:
    """Is a decimal print the floor, ceiling or nearest rounding of x at its own places?"""
    k = len(print_text.split(".")[1])
    p = F(print_text)
    tags = []
    if p == floor_places(x, k):
        tags.append("floor")
    if p == ceil_places(x, k):
        tags.append("ceiling")
    if abs(p - x) <= F(1, 2 * 10**k):
        tags.append("nearest")
    return f"{k} places: " + ("/".join(tags) if tags else "none")


def sig(x: F, k: int) -> str:
    return f"{float(x):.{k - 1}e}"


def main(argv):
    src, kb, st_path, out = Path(argv[1]), Path(argv[2]), Path(argv[3]), Path(argv[4])
    st = json.loads(st_path.read_text())
    res = {}
    ok_all = True
    for n in (156, 180, 268, 269):
        s = st[str(n)]
        d = src / f"s{n}"
        w = R.read_files(d / f"n-{n}-candidate.yaml").witness
        S = F(*w.side)
        hn, hside, *_ = H.read_rational(kb / f"n-{n}.yaml")
        claim = F(s["claim"])
        gap = hside - S
        rel = gap / hside
        readme = (d / "README.md").read_text()
        m7 = re.search(r"`S = ([0-9.]+)…`", readme)
        m9 = re.search(r"side ([0-9.]+)\) is larger by \*\*([0-9.e-]+)\*\* \(relative ([0-9.e-]+)\)", readme)
        verify = (d / "packing-witness-verify.txt").read_text()
        vside = re.search(r"side: (\S+)", verify).group(1)
        vpairs = int(re.search(r"pairs tested: (\d+)", verify).group(1))
        sq = (d / "sqcheck-output.txt").read_text()
        sqs = re.search(r"s<=([0-9.]+)", sq).group(1)
        r = {
            "side": f"{S.numerator}/{S.denominator}",
            "side_denominator_digits": len(str(S.denominator)),
            "side_floor_40": dec(S, 40),
            "ceil12": dec(ceil_places(S, 12), 12),
            "claim": s["claim"],
            "claim_is_ceil12": claim == ceil_places(S, 12),
            "claim_minus_side": float(claim - S),
            "floor12_below_side": floor_places(S, 12) < S,
            "house": s["house"],
            "house_side_equals_issue_fraction": hside == F(s["house_fraction"]),
            "house_floor_20": dec(hside, 20),
            "house_print": s["house_print"],
            "house_print_is": which(s["house_print"], hside),
            "gap": dec(gap, 20) if gap < 1 else str(gap),
            "gap_float": float(gap),
            "gap_12sig": f"{float(gap):.11e}",
            "gap_positive": gap > 0,
            "issue_improvement": s["improvement"],
            "improvement_matches_4sig": f"{float(gap):.3e}" == s["improvement"],
            "relative": float(rel),
            "issue_relative": s["relative"],
            "relative_matches_3sig": f"{float(rel):.2e}" == s["relative"],
            "gap_in_units_of_12th_place": float(gap * 10**12),
            "readme_S": m7.group(1) if m7 else None,
            "readme_S_is": which(m7.group(1), S) if m7 else None,
            "readme_house_print": m9.group(1) if m9 else None,
            "readme_improvement": m9.group(2) if m9 else None,
            "verify_txt_side_equals_side": F(vside) == S,
            "verify_txt_pairs": vpairs,
            "pairs_tested_is_n_choose_2": vpairs == n * (n - 1) // 2 == s["pairs_tested"],
            "sqcheck_print": sqs,
            "sqcheck_print_is": which(sqs, S),
            "sqcheck_print_minus_side": float(F(sqs) - S),
            "context": {},
        }
        for k, v in s["context"].items():
            if k in ("leaderboard", "kaggle_packing"):
                x = F(v)
                r["context"][k] = {"value": v, "minus_side": float(x - S), "minus_claim": float(x - claim), "minus_house": float(x - hside)}
        if n == 156:
            r["exact_side_print_is"] = which(s["exact_side_print"], S)
            r["leaderboard_minus_side_2sig"] = sig(F(s["context"]["leaderboard"]) - S, 2)
            t260 = F(st["T-260"]["side"])
            r["T-260"] = {
                "side_floor_60": dec(t260, 60),
                "T-186_minus_T-260": str(hside - t260),
                "gap": dec(t260 - S, 20),
                "gap_float": float(t260 - S),
                "gap_positive": t260 > S,
            }
        checks = [r["claim_is_ceil12"], r["house_side_equals_issue_fraction"], r["gap_positive"], r["improvement_matches_4sig"], r["relative_matches_3sig"], r["verify_txt_side_equals_side"], r["pairs_tested_is_n_choose_2"]]
        r["all_stated_values_hold"] = all(checks)
        ok_all = ok_all and all(checks)
        res[str(n)] = r
        print(n, r["ceil12"], r["claim_is_ceil12"], r["gap_12sig"], r["improvement_matches_4sig"], r["relative_matches_3sig"], r["house_print_is"], r["readme_S_is"], r["sqcheck_print_is"])
    doc = {"verdict": "SIDES_AS_STATED" if ok_all else "SOME_SIDE_STATEMENT_DIFFERS", "counts": res, "programs": C.program_digests()}
    out.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    print(doc["verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
