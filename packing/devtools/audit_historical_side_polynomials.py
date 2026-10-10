"""Independently audit the retained historical polynomial corpus, without geometry claims.

The builder's NumPy modular arithmetic and derivative enclosures are not imported.
SymPy finite-field routines replay the prime witnesses; an integer Mobius transform
and Descartes' rule independently certify each retained root interval. Source equations
are expanded separately and checked at their retained locators. This audits the bounded
historical corpus, not the current frontier's degree-672 n=83 polynomial.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections.abc import Mapping, Sequence
from fractions import Fraction
from itertools import pairwise
from math import comb, gcd, lcm
from pathlib import Path
from typing import Any

import sympy as sp
from sympy.polys.densetools import dup_shift
from sympy.polys.domains import ZZ
from sympy.polys.galoistools import gf_ddf_zassenhaus, gf_monic, gf_sqf_p

REPO = Path(__file__).resolve().parents[2]
CORPUS = REPO / (
    "packing/resources/web/kingbird-exact-side-facts-2026-10-07/"
    "facts/historical-polynomials.json"
)


class HistoricalAuditError(ValueError):
    """A retained algebraic or source claim failed an independent check."""


def verify_irreducibility(coefficients: Sequence[int], certificate: Mapping[str, Any]) -> int:
    """Replay a certificate over Q, returning the number of good-prime checks."""
    degree = len(coefficients) - 1
    method = certificate["method"]
    if method == "factorization":
        polynomial = sp.Poly(list(coefficients), sp.Symbol("s"), domain=ZZ)
        _, factors = polynomial.factor_list()
        if len(factors) != 1 or factors[0][1] != 1 or factors[0][0].degree() != degree:
            raise HistoricalAuditError("polynomial is reducible over Q")
        return 0
    if method != "modular-degree-patterns":
        raise HistoricalAuditError(f"unsupported irreducibility certificate: {method}")
    primes = certificate["primes"]
    if not primes:
        raise HistoricalAuditError("empty modular certificate")
    possible = set(range(1, degree))
    for prime in primes:
        if type(prime) is not int or not sp.isprime(prime):
            raise HistoricalAuditError(f"certificate contains a nonprime: {prime}")
        if coefficients[0] % prime == 0:
            raise HistoricalAuditError(f"degree drops modulo {prime}")
        _, reduced = gf_monic([ZZ(value % prime) for value in coefficients], prime, ZZ)
        if len(reduced) != degree + 1 or not gf_sqf_p(reduced, prime, ZZ):
            raise HistoricalAuditError(f"reduction is not squarefree modulo {prime}")
        degrees: list[int] = []
        for factor, factor_degree in gf_ddf_zassenhaus(reduced, prime, ZZ):
            if (len(factor) - 1) % factor_degree:
                raise HistoricalAuditError("distinct-degree block has inconsistent degree")
            degrees.extend([factor_degree] * ((len(factor) - 1) // factor_degree))
        if sum(degrees) != degree:
            raise HistoricalAuditError("finite-field factor degrees do not cover polynomial")
        # Bit k records whether a subset of the irreducible factor degrees sums to k.
        mask = 1
        for factor_degree in degrees:
            mask |= mask << factor_degree
        possible.intersection_update(k for k in range(1, degree) if mask & (1 << k))
    if possible:
        raise HistoricalAuditError(
            f"modular certificate leaves proper degrees {sorted(possible)}"
        )
    return len(primes)


def verify_root_interval(coefficients: Sequence[int], lo: Fraction, hi: Fraction) -> None:
    """Prove exactly one root in the open interval using integer Descartes signs."""
    if lo >= hi:
        raise HistoricalAuditError("root interval is empty or reversed")
    degree = len(coefficients) - 1
    # Direct homogeneous sums deliberately avoid the builder's homogeneous Horner loop.
    endpoint_values = [
        sum(
            value * endpoint.numerator ** (degree - index) * endpoint.denominator**index
            for index, value in enumerate(coefficients)
        )
        for endpoint in (lo, hi)
    ]
    if endpoint_values[0] * endpoint_values[1] >= 0:
        raise HistoricalAuditError("root interval lacks a strict endpoint sign change")
    denominator = lcm(lo.denominator, hi.denominator)
    left = lo.numerator * (denominator // lo.denominator)
    right = hi.numerator * (denominator // hi.denominator)
    shifted = dup_shift(
        [ZZ(value * denominator**index) for index, value in enumerate(coefficients)],
        ZZ(left),
        ZZ,
    )[::-1]
    # Q(t) = D^d (1+t)^d P((A+B*t)/(D*(1+t))). The positive t axis maps
    # bijectively onto (lo,hi), and Q has no introduced positive roots.
    transformed = [
        sum(
            int(shifted[k]) * (right - left) ** k * comb(degree - k, j - k)
            for k in range(j + 1)
        )
        for j in range(degree + 1)
    ]
    signs = [1 if value > 0 else -1 for value in transformed if value]
    variations = sum(first != second for first, second in pairwise(signs))
    if variations != 1:
        raise HistoricalAuditError(
            f"Descartes transform has {variations} sign variations, not one"
        )


def verify_source_equation(expression: str, coefficients: Sequence[int]) -> None:
    """Expand the printed equation independently of the collector's term parser."""
    if expression.count("=") != 1 or expression.split("=")[1].strip() != "0":
        raise HistoricalAuditError("source equation must end in '=0'")
    text = re.sub(r"\s+", "", expression.split("=", maxsplit=1)[0])
    text = text.replace("{", "(").replace("}", ")").replace("^", "**")
    # Restrict evaluation to integer arithmetic and the sole indeterminate s.
    if re.fullmatch(r"[0-9s+*()\-]+", text) is None:
        raise HistoricalAuditError("source equation is not an integer polynomial in s")
    text = re.sub(r"(\d)s", r"\1*s", text)
    symbol = sp.Symbol("s")
    polynomial = sp.Poly(sp.sympify(text), symbol, domain=ZZ).primitive()[1]
    expanded = [int(value) for value in polynomial.all_coeffs()]
    if expanded[0] < 0:
        expanded = [-value for value in expanded]
    if expanded != list(coefficients):
        raise HistoricalAuditError("source equation disagrees with retained coefficients")


def _audit_pair(
    row: Mapping[str, Any], source_lines: dict[str, list[str]], repo: Path
) -> tuple[int, int]:
    coefficients = row["coefficients"]
    if (
        len(coefficients) < 2
        or any(type(value) is not int for value in coefficients)
        or coefficients[0] <= 0
        or gcd(*coefficients) != 1
        or len(coefficients) != row["degree"] + 1
    ):
        raise HistoricalAuditError(
            "coefficients are not primitive, positive-leading, or declared-degree"
        )
    checks = row["validation"]["checks"]
    prime_replays = verify_irreducibility(coefficients, checks["irreducible"])
    lo, hi = (Fraction(value) for value in checks["root"]["interval"])
    if lo <= 0:
        raise HistoricalAuditError("side interval must be positive")
    verify_root_interval(coefficients, lo, hi)
    printed_text = row["historical_side"]
    if re.fullmatch(r"[0-9]+\.[0-9]+", printed_text) is None:
        raise HistoricalAuditError("printed side is not a positive decimal")
    printed = Fraction(printed_text)
    unit = Fraction(1, 10 ** len(printed_text.split(".")[1]))
    if not printed - unit / 2 <= lo < hi <= printed + unit:
        raise HistoricalAuditError(
            "root interval disagrees with printed rounding/truncation window"
        )
    if not row["occurrences"]:
        raise HistoricalAuditError("polynomial has no source occurrences")
    for occurrence in row["occurrences"]:
        source = occurrence["source"]
        path = source["path"]
        location = source["locator"]
        if path not in source_lines:
            source_path = (repo / path).resolve()
            if not source_path.is_relative_to(repo.resolve()):
                raise HistoricalAuditError("source path leaves repository")
            source_lines[path] = source_path.read_text(encoding="utf-8").splitlines()
        lines = source_lines[path]
        if location["section"] != str(row["n"]) or not 1 <= location["line"] <= location[
            "line_end"
        ] <= len(lines):
            raise HistoricalAuditError("invalid source locator")
        expression = occurrence["printed_equation"]
        if expression not in "\n".join(lines[location["line"] - 1 : location["line_end"]]):
            raise HistoricalAuditError("printed equation is absent at source locator")
        verify_source_equation(expression, coefficients)
    return prime_replays, len(row["occurrences"])


def audit_document(document: Mapping[str, Any], *, repo: Path = REPO) -> dict[str, int]:
    """Check source math, primitive coefficients, irreducibility, roots, and print windows.

    Source geometry flags and current/historical classifications are outside this
    arithmetic audit. No result here certifies packing feasibility or optimality.
    """
    if document["format"] != "kingbird-historical-side-polynomials-v2":
        raise HistoricalAuditError("unsupported historical corpus format")
    rows = document["entries"]
    if not rows or len(rows) != document["scope"]["unique_polynomial_side_pairs"]:
        raise HistoricalAuditError("empty corpus or inconsistent pair count")
    counts = {"pairs": 0, "source_equations": 0, "prime_replays": 0, "root_intervals": 0}
    source_lines: dict[str, list[str]] = {}
    for row in rows:
        try:
            primes, occurrences = _audit_pair(row, source_lines, repo)
            counts["prime_replays"] += primes
            counts["source_equations"] += occurrences
            counts["pairs"] += 1
            counts["root_intervals"] += 1
        except (HistoricalAuditError, KeyError, TypeError, ValueError, OSError) as error:
            raise HistoricalAuditError(
                f"n={row.get('n')} side={row.get('historical_side')}: {error}"
            ) from error
    if counts["source_equations"] != document["scope"]["decoded_source_rows"]:
        raise HistoricalAuditError("source occurrence count disagrees with corpus scope")
    return counts


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=CORPUS)
    args = parser.parse_args(argv)
    started = time.monotonic()
    try:
        document = json.loads(args.corpus.read_text(encoding="utf-8"))
        counts = audit_document(document)
    except (HistoricalAuditError, KeyError, TypeError, ValueError, OSError) as error:
        print(f"Historical algebra audit FAILED: {error}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {"status": "PASS", **counts, "elapsed_s": round(time.monotonic() - started, 3)}
        )
    )
    print(
        "Scope: source math, primitive coefficients, irreducibility, unique roots, "
        "printed sides; geometry not certified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
