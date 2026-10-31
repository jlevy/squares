"""Exact side comparisons for the review; decides nothing about feasibility.

Reads each certificate's header side and each house witness's side as exact rationals,
checks the 12-place prints round the sides up, orders the sides at each count, and
compares each side with the house witnesses at the next counts (s is non-decreasing in n,
so a side is informative only below every bound at every later count).

Usage: sides.py TREE_PACKING_DIR
"""

from __future__ import annotations

import math
import sys
from decimal import ROUND_CEILING, Decimal, getcontext
from fractions import Fraction as F
from pathlib import Path

import yaml

getcontext().prec = 80


def cert_side(p: Path) -> F:
    for ln in p.read_text(encoding="utf-8").splitlines():
        if ln.strip() and not ln.startswith("#"):
            return F(ln.split()[1])
    raise ValueError(p)


def witness_side(p: Path):
    """Exact side where the witness states it as a rational or decimal; None otherwise."""
    head = []
    with p.open(encoding="utf-8") as fh:
        for ln in fh:
            if ln.startswith("  squares:"):
                break
            head.append(ln)
    d = yaml.safe_load("".join(head))["witness"]
    v = d.get("side")
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return F(str(v))
    if isinstance(v, str):
        return F(v) if "/" in v or "." not in v else F(Decimal(v))
    return None


def up12(x: F) -> str:
    d = Decimal(x.numerator) / Decimal(x.denominator)
    return str(d.quantize(Decimal("1e-12"), rounding=ROUND_CEILING))


def main():
    root = Path(sys.argv[1])
    web = root / "resources/web"
    certs = {
        130: {
            "#843 (T-254)": (web / "couzo-issue843-2026-10-28/source/certificates/n130.cert", "11.902430645985"),
            "#846 (T-259)": (web / "mishapolk-issue846-2026-10-30/source/certificates/0000-0999/n130.cert", None),
        },
        232: {"#844 (T-256)": (web / "couzo-issue844-2026-10-28/source/certificates/best/n232.cert", "15.761661759482")},
        260: {
            "a5a5d76 (T-255)": (web / "couzo-a5a5d76-2026-10-28/source/certificates/n260.cert", "16.638532792320"),
            "#844 (T-256)": (web / "couzo-issue844-2026-10-28/source/certificates/n260.cert", "16.637029558871"),
            "#845 (T-257)": (web / "evand-issue845-2026-10-29/source/search/packer/candidates/s260_1028.cert", None),
            "#846 (T-259)": (web / "mishapolk-issue846-2026-10-30/source/certificates/0000-0999/n260.cert", None),
        },
        307: {
            "a5a5d76 (T-255)": (web / "couzo-a5a5d76-2026-10-28/source/certificates/n307.cert", "17.979251283693"),
            "#844 (T-256)": (web / "couzo-issue844-2026-10-28/source/certificates/n307.cert", "17.979251283689"),
        },
    }
    for n, rows in certs.items():
        house = witness_side(root / f"witnesses/known-best/n-{n:03d}.yaml")
        print(f"== {n}: house witness side {float(house):.15f}")
        sides = {}
        for k, (p, printed) in rows.items():
            s = cert_side(p)
            sides[k] = s
            pr = up12(s)
            ok = "" if printed is None else ("print ok" if pr == printed else f"PRINT MISMATCH {printed}")
            terminates = (F(math.ceil(s * 10**12), 10**12) == s)
            print(f"  {k}: {float(s):.16f}  up12 {pr}  {ok}  terminates@12: {terminates}  minus house {float(s - house):+.6e}")
        order = sorted(sides.items(), key=lambda kv: kv[1])
        print("  ascending:", " < ".join(f"{k}" for k, _ in order))
        for (a, sa), (b, sb) in zip(order, order[1:]):
            print(f"    {b} - {a} = {float(sb - sa):.6e}")
        smallest = order[0][1]
        later = []
        for m in range(n + 1, n + 40):
            p = root / f"witnesses/known-best/n-{m:03d}.yaml"
            if p.exists():
                w = witness_side(p)
                if w is None:
                    print(f"  (n={m}: side not a rational or decimal; not compared)")
                else:
                    later.append((w, m))
        lo = min(later)
        print(f"  least house side at {n + 1}..{n + 39}: n={lo[1]} {float(lo[0]):.12f}; above every claimed side here by >= {float(lo[0] - max(sides.values())):.6e}")


if __name__ == "__main__":
    main()
