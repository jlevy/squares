#!/usr/bin/env python3
"""The exact sides of issue #639's 23 exact forms, and the ties their prints cannot decide.

Evan Daniel's ``search/exact/cur/data/n-N.minpoly.json.gz`` (evand/square-packing at
``7d1407a``, the ``evand-exact-cur-2026-10-16`` packet) gives each side ``S*`` as the one
root of an integer polynomial ``p`` in a rational interval. This program reads each file
from the packet, or for the four the packet pins by digest only from ``--pinned``, holds
its bytes to the packet's manifest, and writes ``exact-sides.json``:

- ``p`` and an interval of width below ``10^-130`` around its one root there, by exact
  bisection after Sturm's theorem (``sympy.Poly.count_roots``) has counted one root in the
  source's interval;
- the print the ledger reads: ``S*`` cut at `PLACES` places, so ``S*`` lies in
  ``[print, print + 10^-PLACES)``, the ledger's ``cut`` rounding;
- at 51, 126 and 295 the closed form the source states, checked to be that root;
- the ties the prints leave open, decided exactly. At 51 the case's lanes hold
  ``(16 + 5 sqrt 2)/3``. At 70, 153 and 207 register entry T-174 states the side of
  PingYou Ltd's algebraic witness, ``c(b)`` with ``b`` the root of ``m`` in an isolating
  interval (``facts/alg-n-NNN.yaml.gz`` of the ``pingyou-pr574-certificates-2026-10-13``
  packet). Equality is decided by the resultant ``Res_b(m(b), x - c(b))``, which must be
  ``p`` up to a rational factor, and by an interval enclosure of ``c(b)`` inside the
  interval where ``p`` has its one root.

Nothing here uses floating point. It decides nothing about the packings; the source's
checker does that, and the replay of think-g59l runs it.

From ``packing/``, with the project interpreter::

    python campaign/issue-intake/upper-bounds-20261016/review/exact_sides.py \\
        --pinned DIR [--check]
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import sympy
import yaml

#: The repository root: this file is packing/campaign/issue-intake/<directory>/review/.
REPO = Path(__file__).resolve().parents[5]
PACKING = REPO / "packing"
HERE = Path(__file__).resolve().parents[1]
PACKET = PACKING / "resources/web/evand-exact-cur-2026-10-16"
DATA = PACKET / "source/search/exact/cur/data"
MANIFEST = PACKET / "acquisition/upstream-subtree.sha256"
PINGYOU = PACKING / "resources/web/pingyou-pr574-certificates-2026-10-13/facts"
OUT = HERE / "exact-sides.json"
# fmt: off
COUNTS = (
    51, 70, 88, 102, 123, 126, 153, 172, 175, 199, 204, 207, 232, 258, 259, 263, 266, 267,
    292, 295, 297, 301, 302,
)
# fmt: on
PLACES = 120
WIDTH = Fraction(1, 10**130)
X = sympy.Symbol("x")
B = sympy.Symbol("b")
SQRT2 = sympy.sqrt(2)
#: The closed forms the source states (README.md, RESULTS.md).
CLOSED = {
    51: (sympy.Rational(16, 3) + sympy.Rational(5, 3) * SQRT2, "(16 + 5√2)/3"),
    126: (sympy.Rational(15, 2) + 3 * SQRT2, "15/2 + 3√2"),
    295: (sympy.Rational(22, 3) * (1 + SQRT2), "22(1 + √2)/3"),
}
#: The ties to decide: the count, what the standing side is, and how to read it.
CASE_51 = "the case record's reported and verified lanes, exact form (16 + 5√2)/3"
T174 = (70, 153, 207)


def digests() -> dict[str, str]:
    rows = (line.split() for line in MANIFEST.read_text(encoding="utf-8").splitlines())
    return {path.removeprefix("./"): digest for digest, path in rows}


def source_file(n: int, pinned: Path, manifest: dict[str, str]) -> tuple[Path, str, str]:
    name = f"n-{n}.minpoly.json.gz"
    upstream = f"search/exact/cur/data/{name}"
    path = DATA / name
    where = f"packet:{path.relative_to(REPO)}"
    if not path.is_file():
        path = pinned / name
        where = f"pinned only, read from a copy outside the repository ({name})"
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != manifest[upstream]:
        sys.exit(f"{name}: SHA-256 {digest} is not the manifest's {manifest[upstream]}")
    return path, where, digest


def value(poly: list[int], x: Fraction) -> Fraction:
    total = Fraction(0)
    for coefficient in reversed(poly):
        total = total * x + coefficient
    return total


def isolate(poly: list[int], low: Fraction, high: Fraction) -> tuple[Fraction, Fraction]:
    """Narrow ``[low, high]``, in which ``poly`` has one root and changes sign, below WIDTH."""
    sign_low = value(poly, low) > 0
    while high - low >= WIDTH:
        middle = (low + high) / 2
        at = value(poly, middle)
        if at == 0:
            return middle, middle
        if (at > 0) == sign_low:
            low = middle
        else:
            high = middle
    return low, high


def cut(low: Fraction, high: Fraction) -> str:
    scale = 10**PLACES
    floor_low, floor_high = (
        (low.numerator * scale) // low.denominator,
        (high.numerator * scale) // high.denominator,
    )
    if floor_low != floor_high:
        sys.exit("the root sits on a cut boundary; refine further")
    whole, fraction = divmod(floor_low, scale)
    return f"{whole}.{fraction:0{PLACES}d}"


def closed_form_check(n: int, poly: list[int], low: Fraction, high: Fraction) -> dict[str, Any]:
    form, text = CLOSED[n]
    p = sympy.Poly(list(reversed(poly)), X)
    residue = sympy.simplify(p.as_expr().subs(X, form))
    inside = bool(sympy.Rational(low.numerator, low.denominator) <= form) and bool(
        form <= sympy.Rational(high.numerator, high.denominator)
    )
    return {"form": text, "p_vanishes": residue == 0, "inside_interval": inside}


def fact(n: int) -> dict[str, Any]:
    path = PINGYOU / f"alg-n-{n:03d}.yaml.gz"
    witness = yaml.safe_load(gzip.decompress(path.read_bytes()).decode("utf-8"))["witness"]
    scalar = witness["scalar"]
    return {
        "path": str(path.relative_to(REPO)),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "side": [Fraction(c) for c in witness["side"]],
        "minimal_polynomial": [int(c) for c in scalar["minimal_polynomial"]],
        "interval": [Fraction(c) for c in scalar["isolating_interval"]],
    }


def interval_value(
    coefficients: list[Fraction], low: Fraction, high: Fraction
) -> tuple[Fraction, Fraction]:
    """An enclosure of ``sum c_i b^i`` over ``b`` in ``[low, high]``, by interval Horner."""
    lo = hi = Fraction(0)
    for coefficient in reversed(coefficients):
        products = (lo * low, lo * high, hi * low, hi * high)
        lo, hi = min(products) + coefficient, max(products) + coefficient
    return lo, hi


def tie_t174(n: int, poly: list[int], low: Fraction, high: Fraction) -> dict[str, Any]:
    witness = fact(n)
    m = witness["minimal_polynomial"]  # high to low
    m_poly = sympy.Poly(m, B)
    side = sum(
        sympy.Rational(c.numerator, c.denominator) * B**i for i, c in enumerate(witness["side"])
    )
    resultant = sympy.Poly(sympy.resultant(m_poly.as_expr(), X - side, B), X)
    p = sympy.Poly(list(reversed(poly)), X)
    ratio = sympy.simplify(resultant.LC() / p.LC())
    proportional = sympy.Poly(resultant - ratio * p, X).is_zero
    b_low, b_high = witness["interval"]
    m_low_to_high = [int(c) for c in reversed(m)]
    sturm = int(
        sympy.Poly(m, B).count_roots(
            sympy.Rational(b_low.numerator, b_low.denominator),
            sympy.Rational(b_high.numerator, b_high.denominator),
        )
    )
    b_low, b_high = isolate(m_low_to_high, b_low, b_high)
    s_low, s_high = interval_value(witness["side"], b_low, b_high)
    inside = low <= s_low and s_high <= high
    return {
        "against": f"register T-174 (PR #574), the algebraic witness {witness['path']}",
        "witness_sha256": witness["sha256"],
        "b_roots_in_interval": sturm,
        "resultant_proportional_to_p": bool(proportional),
        "enclosure_inside_p_interval": bool(inside),
        "relation": "equal" if proportional and inside and sturm == 1 else "undecided",
        "method": (
            "Res_b(m(b), x - c(b)) is p times a rational, and an interval enclosure of c(b), "
            "b narrowed below 1e-130 in its interval, lies inside the source's interval, "
            "where p has one root"
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("--pinned", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    manifest = digests()
    rows: list[dict[str, Any]] = []
    for n in COUNTS:
        path, where, digest = source_file(n, args.pinned, manifest)
        data = json.loads(gzip.decompress(path.read_bytes()).decode("utf-8"))
        if data["n"] != n or len(data["squares"]) != n:
            sys.exit(
                f"n = {n}: the file states n = {data['n']} with {len(data['squares'])} squares"
            )
        poly = [int(c) for c in data["S"]["poly"]]
        source_low, source_high = (Fraction(c) for c in data["S"]["interval"])
        roots = int(
            sympy.Poly(list(reversed(poly)), X).count_roots(
                sympy.Rational(source_low.numerator, source_low.denominator),
                sympy.Rational(source_high.numerator, source_high.denominator),
            )
        )
        if roots != 1 or value(poly, source_low) * value(poly, source_high) >= 0:
            sys.exit(f"n = {n}: {roots} roots of p in the source's interval")
        low, high = isolate(poly, source_low, source_high)
        row: dict[str, Any] = {
            "n": n,
            "file": where,
            "sha256": digest,
            "degree": len(poly) - 1,
            "polynomial_low_to_high": [str(c) for c in poly],
            "source_interval": [str(source_low), str(source_high)],
            "roots_in_source_interval": roots,
            "interval": [str(low), str(high)],
            "print": cut(low, high),
            "rounding": "cut",
        }
        if n in CLOSED:
            row["closed_form"] = closed_form_check(n, poly, source_low, source_high)
        if n == 51:
            check = row["closed_form"]
            row["tie"] = {
                "against": CASE_51,
                "relation": "equal"
                if check["p_vanishes"] and check["inside_interval"]
                else "undecided",
                "method": (
                    "the case's exact form is a root of p inside the source's interval, "
                    "where p has one root"
                ),
            }
        if n in T174:
            row["tie"] = tie_t174(n, poly, source_low, source_high)
        rows.append(row)
        print(n, row["degree"], row["print"][:40], row.get("tie", {}).get("relation", ""))
    document = {
        "format": "issue-639-exact-sides-v1",
        "tool": "packing/campaign/issue-intake/upper-bounds-20261016/review/exact_sides.py",
        "source": (
            "evand/square-packing@7d1407a0b66c46e32cdbcbd5619586fe2bdd52a1 "
            "search/exact/cur/data"
        ),
        "places": PLACES,
        "rows": rows,
    }
    text = json.dumps(document, indent=1, ensure_ascii=False) + "\n"
    if args.check:
        if OUT.read_text(encoding="utf-8") != text:
            print(f"{OUT.name} differs from a fresh computation")
            return 1
        print(f"{OUT.name} matches")
        return 0
    OUT.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
