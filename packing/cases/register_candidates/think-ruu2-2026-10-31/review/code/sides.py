"""Exact sides, margins, 12-place prints, and the ceilings above each count.

Usage: python3.14 sides.py INPUTS_DIR OUT_DIR CASE_DIR
CASE_DIR holds n-NNN.md case records read from main (git show), as data.

Prints are the record's upward 12-place display: ceil(side * 10^12) / 10^12. Each case
record's verified_upper_bound exact_form is evaluated with Decimal at 60 digits (only
numbers, + - * /, parentheses and sqrt are accepted); a form the evaluator refuses is
reported, never guessed.
"""

from __future__ import annotations

import json
import re
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

import qio

getcontext().prec = 60


def ceil_print(x: Fraction, places: int = 12) -> str:
    q = 10**places
    k = -((-x.numerator * q) // x.denominator)
    s = str(k)
    return f"{s[:-places]}.{s[-places:]}"


def decimal_of(x: Fraction, places: int = 40) -> str:
    q = 10**places
    k = x.numerator * q // x.denominator
    s = str(k)
    return f"{s[:-places]}.{s[-places:]}"


TOKEN = re.compile(r"\s*(sqrt|\d+(?:\.\d+)?|[()+\-*/])")


def evaluate(expr: str) -> Decimal:
    toks = []
    pos = 0
    expr = expr.strip().strip("'")
    while pos < len(expr):
        m = TOKEN.match(expr, pos)
        if not m:
            raise ValueError(f"cannot read {expr!r} at {pos}")
        toks.append(m.group(1))
        pos = m.end()
    k = 0

    def peek() -> str | None:
        return toks[k] if k < len(toks) else None

    def take() -> str:
        nonlocal k
        k += 1
        return toks[k - 1]

    def atom() -> Decimal:
        t = take()
        if t == "(":
            v = add()
            assert take() == ")"
            return v
        if t == "sqrt":
            assert take() == "("
            v = add()
            assert take() == ")"
            return v.sqrt()
        if t == "-":
            return -atom()
        return Decimal(t)

    def mul() -> Decimal:
        v = atom()
        while peek() in ("*", "/"):
            v = v * atom() if take() == "*" else v / atom()
        return v

    def add() -> Decimal:
        v = mul()
        while peek() in ("+", "-"):
            v = v + mul() if take() == "+" else v - mul()
        return v

    v = add()
    if k != len(toks):
        raise ValueError(f"trailing tokens in {expr!r}")
    return v


def verified_upper(case_md: str) -> str:
    block = case_md.split("verified_upper_bound:", 1)[1]
    m = re.search(r"\n    exact_form: (.+)", block)
    if not m:
        raise ValueError("no exact_form")
    return m.group(1).strip()


def main() -> None:
    inp, outdir, cases = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    _, s260, _, _ = qio.read_tcert(inp / "s260_1028.cert")
    rows = {
        130: (qio.read_view(inp / "n130-view-solved.yaml")[1], qio.read_view(inp / "house-n130.yaml")[1]),
        293: (s260 + 1, qio.read_view(inp / "house-n293.yaml")[1]),
        307: (qio.read_view(inp / "n307-view-solved.yaml")[1], qio.read_view(inp / "house-n307.yaml")[1]),
    }
    out: dict[str, object] = {}
    for n, (cand, house) in rows.items():
        case = (cases / f"n-{n:03d}.md").read_text(encoding="utf-8")
        vub = Fraction(verified_upper(case).strip("'"))
        margin = house - cand
        rec = {
            "candidate_side": str(cand),
            "candidate_decimal": decimal_of(cand),
            "house_side": str(house),
            "house_equals_case_verified_upper_bound": house == vub,
            "candidate_below_house": cand < house,
            "margin": str(margin),
            "margin_approx": f"{float(margin):.6e}",
            "margin_below_1e-12": margin < Fraction(1, 10**12),
            "print12_candidate": ceil_print(cand),
            "print12_house": ceil_print(house),
            "same_print12": ceil_print(cand) == ceil_print(house),
        }
        above = []
        for m in range(n + 1, 325):
            path = cases / f"n-{m:03d}.md"
            form = verified_upper(path.read_text(encoding="utf-8"))
            try:
                v = evaluate(form)
            except Exception as exc:  # noqa: BLE001
                above.append((m, form[:60], f"unread: {exc}"))
                continue
            gap = v - Decimal(cand.numerator) / Decimal(cand.denominator)
            above.append((m, form[:60], f"{gap:.3e}"))
        least = min((r for r in above if not r[2].startswith("unread")), key=lambda r: Decimal(r[2]))
        rec["least_ceiling_above_minus_candidate"] = least
        rec["unread_ceilings_above"] = [r for r in above if r[2].startswith("unread")]
        out[str(n)] = rec
        print(
            f"n={n}: candidate {decimal_of(cand, 30)} house {decimal_of(house, 30)}"
            f" (= case verified upper: {rec['house_equals_case_verified_upper_bound']})\n"
            f"       below: {rec['candidate_below_house']} margin {rec['margin_approx']} (< 1e-12: {rec['margin_below_1e-12']})"
            f" prints {rec['print12_candidate']} vs {rec['print12_house']} same={rec['same_print12']}\n"
            f"       least U(m) - candidate over n < m <= 324: {least}; unread: {rec['unread_ceilings_above']}"
        )
    # the contracted sides from contract.py, printed the same way
    contracted = json.loads((outdir / "contract.json").read_text())
    for label, r in contracted.items():
        lp = Fraction(r["contracted_side"])
        side = Fraction(r["house_or_certificate_side"])
        print(f"{label}: contracted {decimal_of(lp, 30)} print {ceil_print(lp)}; its certificate's print {ceil_print(side)}")
        if label == "s260":
            print(f"   s260 contracted + 1 = {decimal_of(lp + 1, 30)} print {ceil_print(lp + 1)}")
        out[f"contracted-{label}"] = {"side": str(lp), "print12": ceil_print(lp), "certificate_print12": ceil_print(side)}
    (outdir / "sides.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
