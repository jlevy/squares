"""Independent checks of an exact side's minimal polynomial, in exact integer arithmetic.

T-246 records Evan Daniel's report that the side of the best known packing of 29 squares
is a root of an irreducible integer polynomial ``p`` of degree 7213.  His own checks run on
FLINT (``python-flint``: ``nmod_poly.factor`` for irreducibility, ``arb`` balls for the
root).  This module re-derives the same facts with other code and another library: GMP
integers through ``gmpy2`` for every exact step, and ``numpy`` for arithmetic modulo small
primes.  Nothing here imports FLINT, and nothing here reads the source's scripts.

``isolate``
    Exactly one root of ``p`` in a rational interval: an exact sign change at two inner
    dyadic points, and ``p'`` bounded away from zero on a dyadic hull of the interval by a
    Taylor expansion at its midpoint with exact coefficients and a rigorous tail bound
    (``|T_1| > sum_{k<K} k |T_k| r^{k-1} + n r^{K-1} P_abs(|m| + 1)``).  With ``--rational``,
    the exact sign of ``p`` there and the root's order against it.
``irreducible``
    Distinct-degree factorization of ``p`` modulo primes below ``2^31`` that divide neither
    the leading coefficient nor the discriminant (``p mod q`` squarefree of full degree),
    and the degree-pattern certificate: a factorization over ``Z`` into degrees ``(d,
    n-d)`` would give, modulo every such prime, factor degrees with a sub-multiset summing
    to ``d``; when the intersection over primes of the attainable ``d`` is empty, ``p`` is
    irreducible.  Multiplication modulo ``q`` is Kronecker substitution on GMP integers.
``price``
    The price of making the source's Monte Carlo identities deterministic: the size of an
    exact residue in ``Q[x]/(p)`` (measured on reductions of ``x^(n+j)``) and the number of
    primes a modular proof needs against the resultant bound on the identity's numerator.

Run from ``packing/``::

    uv run --frozen --all-extras --group dev python -m devtools.check_exact_side_minpoly \
        isolate --poly DATA/n29_poly_q4.json --lo LO --hi HI --rational N/D --out RECEIPT
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from collections.abc import Sequence
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

import gmpy2 as _gmpy2
import numpy as np

from devtools.check_exact_side_packing import parse_system

#: GMP through gmpy2; its local stubs omit shifts, byte conversion and the number
#: theory functions used here, so the module is reached through an untyped alias.
GMP: Any = _gmpy2
mpz: Any = _gmpy2.mpz


def load_poly(path: Path) -> list[Any]:
    sys.set_int_max_str_digits(0)
    return [mpz(c) for c in json.loads(path.read_text())["coeffs_ascending"]]


def dyadic_floor(value: Fraction, exponent: int) -> int:
    return math.floor(value * (1 << exponent))


def dyadic_ceil(value: Fraction, exponent: int) -> int:
    return math.ceil(value * (1 << exponent))


def scaled_value(coeffs: Sequence[Any], numerator: Any, denominator_power: int) -> Any:
    """``p(a / 2^E) * 2^(E n)`` exactly, by Horner with shifts."""
    n = len(coeffs) - 1
    acc = mpz(coeffs[n])
    for i in range(n - 1, -1, -1):
        acc = acc * numerator + (mpz(coeffs[i]) << (denominator_power * (n - i)))
    return acc


def rational_sign(coeffs: Sequence[Any], value: Fraction) -> int:
    """The exact sign of ``p`` at a rational, from ``p(N/D) D^n`` (``D > 0``)."""
    n = len(coeffs) - 1
    numerator, denominator = mpz(value.numerator), mpz(value.denominator)
    acc, power = mpz(coeffs[n]), mpz(1)
    for i in range(n - 1, -1, -1):
        power *= denominator
        acc = acc * numerator + coeffs[i] * power
    return (acc > 0) - (acc < 0)


def taylor_numerators(
    coeffs: Sequence[Any], numerator: Any, exponent: int, order: int
) -> list[Any]:
    """``Q_k = sum_i c_i C(i,k) a^(i-k) 2^(E(n-i))`` for ``k <= order``.

    The Taylor coefficients at ``m = a / 2^E`` are then ``T_k = Q_k 2^(-E(n-k))``.
    """
    n = len(coeffs) - 1
    acc = [mpz(0)] * (order + 1)
    for i in range(n, -1, -1):
        shifted = mpz(coeffs[i]) << (exponent * (n - i))
        binomial = mpz(1)
        for k in range(min(i, order) + 1):
            if k:
                binomial = binomial * (i - k + 1) // k
            acc[k] = acc[k] * numerator + shifted * binomial
    return acc


def isolate(
    coeffs: Sequence[Any], lo: Fraction, hi: Fraction, exponent: int = 200, order: int = 160
) -> dict[str, Any]:
    """Decide that ``p`` has exactly one root in ``[lo, hi]``, in exact arithmetic."""
    started = time.process_time()
    n = len(coeffs) - 1
    inner = (dyadic_ceil(lo, exponent), dyadic_floor(hi, exponent))
    signs = [scaled_value(coeffs, a, exponent) for a in inner]
    sign_change = (signs[0] > 0) != (signs[1] > 0) and signs[0] != 0 and signs[1] != 0
    hull = [dyadic_floor(lo, exponent), dyadic_ceil(hi, exponent)]
    if (hull[1] - hull[0]) % 2:
        hull[1] += 1
    centre, half = (hull[0] + hull[1]) // 2, (hull[1] - hull[0]) // 2
    q = taylor_numerators(coeffs, mpz(centre), exponent, order)
    top = abs(Fraction(centre, 1 << exponent)) + 1
    bound_point = math.ceil(top)
    absolute = mpz(0)
    for c in reversed(coeffs):
        absolute = absolute * bound_point + abs(c)
    lead = abs(q[1])
    monotone_order = None
    partial = mpz(0)
    for k in range(2, order + 1):
        tail = n * mpz(half) ** (k - 1) * absolute << (exponent * (n - k)) if k <= n else None
        if tail is not None and lead > partial + tail:
            monotone_order = k
            break
        partial += k * abs(q[k]) * mpz(half) ** (k - 1)
    return {
        "dyadic_exponent": exponent,
        "inner_points": [str(Fraction(a, 1 << exponent)) for a in inner],
        "signs_at_inner_points": [int((s > 0) - (s < 0)) for s in signs],
        "sign_change": bool(sign_change),
        "hull": [str(Fraction(a, 1 << exponent)) for a in hull],
        "derivative_bounded_away_from_zero_on_hull": monotone_order is not None,
        "taylor_terms_used": monotone_order,
        "log10_abs_p_prime_at_centre": round(
            float(GMP.log10(lead)) - exponent * (n - 1) * math.log10(2), 1
        ),
        "exactly_one_root": bool(sign_change and monotone_order is not None),
        "cpu_seconds": round(time.process_time() - started, 1),
    }


def compare(
    coeffs: Sequence[Any], isolation: dict[str, Any], rational: Fraction
) -> dict[str, Any]:
    started = time.process_time()
    inner = [Fraction(v) for v in isolation["inner_points"]]
    sign = rational_sign(coeffs, rational)
    below = isolation["exactly_one_root"] and inner[1] < rational
    with localcontext() as context:
        context.prec = 40
        gap_lo = Decimal((rational - inner[1]).numerator) / Decimal(
            (rational - inner[1]).denominator
        )
        gap_hi = Decimal((rational - inner[0]).numerator) / Decimal(
            (rational - inner[0]).denominator
        )
    return {
        "rational": f"{rational.numerator}/{rational.denominator}",
        "sign_of_p_at_rational": sign,
        "root_below_rational": bool(below),
        "rational_minus_root": [f"{gap_lo:.25e}", f"{gap_hi:.25e}"],
        "cpu_seconds": round(time.process_time() - started, 1),
    }


# --- arithmetic modulo a small prime ------------------------------------------------------


class ModPoly:
    """Dense polynomials modulo a prime ``q < 2^31``: int64 arrays, ascending."""

    def __init__(self, q: int, max_length: int = 1 << 14):
        if q >= 1 << 31 or sys.byteorder != "little":
            raise ValueError("needs q < 2^31 on a little-endian machine")
        self.q = q
        self.wrap = (1 << 64) % q
        # A product coefficient is a sum of fewer than max_length products below q^2.
        self.slot = -(-(2 * q.bit_length() + max_length.bit_length()) // 8)
        self.slot = max(8, self.slot)

    def trim(self, a: np.ndarray) -> np.ndarray:
        nonzero = np.flatnonzero(a)
        return a[: nonzero[-1] + 1] if nonzero.size else a[:0]

    def mul(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        if not a.size or not b.size:
            return np.zeros(0, dtype=np.int64)
        length = a.size + b.size - 1

        slot = self.slot

        def pack(v: np.ndarray) -> Any:
            if slot == 8:
                return mpz.from_bytes(v.astype(np.int64).tobytes(), "little")
            buffer = np.zeros((v.size, slot), dtype=np.uint8)
            width = min(8, slot)
            buffer[:, :width] = v.astype(np.int64).view(np.uint8).reshape(-1, 8)[:, :width]
            return mpz.from_bytes(buffer.tobytes(), "little")

        raw = (pack(a) * pack(b)).to_bytes(length * slot, "little")
        slots = np.frombuffer(raw, dtype=np.uint8).reshape(length, slot)
        q = np.uint64(self.q)
        if slot == 8:
            return (np.frombuffer(raw, dtype=np.uint64) % q).astype(np.int64)
        low = slots[:, :8].copy().view(np.uint64).ravel()
        high = np.zeros((length, 8), dtype=np.uint8)
        high[:, : slot - 8] = slots[:, 8:]
        return (
            (low % q + (high.view(np.uint64).ravel() * np.uint64(self.wrap)) % q) % q
        ).astype(np.int64)

    def rem(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        a = self.trim(a.copy())
        degree = b.size - 1
        inverse = pow(int(b[-1]), -1, self.q)
        for i in range(a.size - 1, degree - 1, -1):
            c = int(a[i]) * inverse % self.q
            if c:
                a[i - degree : i + 1] = (a[i - degree : i + 1] - c * b) % self.q
        return self.trim(a[:degree])

    def gcd(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        a, b = self.trim(a), self.trim(b)
        while b.size:
            a, b = b, self.rem(a, b)
        return (a * pow(int(a[-1]), -1, self.q)) % self.q if a.size else a

    def divide_exact(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        a = self.trim(a.copy())
        degree = b.size - 1
        inverse = pow(int(b[-1]), -1, self.q)
        quotient = np.zeros(a.size - degree, dtype=np.int64)
        for i in range(a.size - 1, degree - 1, -1):
            c = int(a[i]) * inverse % self.q
            quotient[i - degree] = c
            if c:
                a[i - degree : i + 1] = (a[i - degree : i + 1] - c * b) % self.q
        if self.trim(a[:degree]).size:
            raise ArithmeticError("division was not exact")
        return quotient

    def derivative(self, a: np.ndarray) -> np.ndarray:
        return (a[1:] * np.arange(1, a.size, dtype=np.int64)) % self.q


class Reducer:
    """Multiplication modulo a fixed monic ``f``, by a precomputed reversed inverse."""

    def __init__(self, ring: ModPoly, f: np.ndarray):
        self.ring, self.f, self.n = ring, f, f.size - 1
        reversed_f = f[::-1].copy()
        inverse = np.array([1], dtype=np.int64)
        precision = 1
        while precision < self.n:
            precision = min(2 * precision, self.n)
            square = ring.mul(inverse, inverse)[:precision]
            inverse = (
                2 * np.pad(inverse, (0, precision - inverse.size))
                - ring.mul(square, reversed_f[:precision])[:precision]
            ) % ring.q
        self.inverse = inverse[: self.n]

    def reduce(self, a: np.ndarray) -> np.ndarray:
        if a.size <= self.n:
            return a
        while a.size > 2 * self.n:
            # x^s * segment == x^s * (segment mod f): fold the top 2n coefficients down.
            start = a.size - 2 * self.n
            folded = self.reduce(a[start:])
            merged = np.zeros(start + self.n, dtype=np.int64)
            merged[:start] = a[:start]
            merged[start : start + folded.size] = folded
            a = self.ring.trim(merged)
        if a.size <= self.n:
            return a
        top = a[self.n :][::-1]
        quotient = self.ring.mul(top, self.inverse)[: a.size - self.n][::-1]
        product = self.ring.mul(quotient, self.f)
        return self.ring.trim((a[: self.n] - product[: self.n]) % self.ring.q)

    def mulmod(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        return self.reduce(self.ring.mul(a, b))

    def power(self, base: np.ndarray, exponent: int) -> np.ndarray:
        result = np.array([1], dtype=np.int64)
        for bit in f"{exponent:b}":
            result = self.mulmod(result, result)
            if bit == "1":
                result = self.mulmod(result, base)
        return result


class FrobeniusMatrix:
    """``h -> h^q mod f`` as ``h @ Q``, with ``Q``'s rows ``x^(iq) mod f``.

    For ``q < 2^16`` every entry of ``h @ Q`` is a sum of fewer than ``2^13`` products
    below ``2^32``, so below ``2^53``: float64 holds it exactly, and BLAS computes it.
    """

    def __init__(self, ring: ModPoly, reducer: Reducer):
        if ring.q.bit_length() > 16 or reducer.n >= 1 << 13:
            raise ValueError("the float64 Frobenius needs q < 2^16 and degree < 2^13")
        self.ring, self.n = ring, reducer.n
        step = reducer.power(np.array([0, 1], dtype=np.int64), ring.q)
        self.matrix = np.zeros((self.n, self.n), dtype=np.float64)
        row = np.array([1], dtype=np.int64)
        for i in range(self.n):
            self.matrix[i, : row.size] = row
            row = reducer.mulmod(row, step)

    def apply(self, h: np.ndarray) -> np.ndarray:
        padded = np.zeros(self.n, dtype=np.float64)
        padded[: h.size] = h
        return self.ring.trim((padded @ self.matrix % self.ring.q).astype(np.int64))


def distinct_degree_pattern(ring: ModPoly, f: np.ndarray, block: int = 40) -> list[int]:
    """Factor degrees of a squarefree monic ``f`` mod ``q``, by distinct-degree factoring."""
    reducer = Reducer(ring, f)
    frobenius_map = (
        FrobeniusMatrix(ring, reducer) if ring.q < 1 << 16 and f.size - 1 < 1 << 13 else None
    )
    x = np.array([0, 1], dtype=np.int64)
    rest = f.copy()
    degrees: list[int] = []
    frobenius = x
    d = 0
    while 2 * (d + 1) <= rest.size - 1:
        powers = []
        product = np.array([1], dtype=np.int64)
        for _ in range(block):
            d += 1
            frobenius = (
                frobenius_map.apply(frobenius)
                if frobenius_map is not None
                else reducer.power(frobenius, ring.q)
            )
            shifted = frobenius.copy()
            shifted = np.pad(shifted, (0, max(0, 2 - shifted.size)))
            shifted[1] = (shifted[1] - 1) % ring.q
            powers.append((d, ring.trim(shifted)))
            product = reducer.mulmod(product, ring.trim(shifted))
            if 2 * d >= rest.size - 1:
                break
        common = ring.gcd(
            rest, ring.rem(product, rest) if product.size >= rest.size else product
        )
        if common.size > 1:
            for degree, value in powers:
                if common.size <= 1:
                    break
                part = ring.gcd(
                    common, ring.rem(value, common) if value.size >= common.size else value
                )
                if part.size > 1:
                    count = (part.size - 1) // degree
                    degrees += [degree] * count
                    common = ring.divide_exact(common, part)
                    rest = ring.divide_exact(rest, part)
    if rest.size > 1:
        degrees.append(rest.size - 1)
    return sorted(degrees)


def next_prime(value: int) -> int:
    candidate = GMP.next_prime(value)
    return int(candidate)


def irreducible(
    coeffs: Sequence[Any],
    primes: int,
    start: int,
    out_log: Any = None,
    *,
    stop_when_empty: bool = False,
) -> dict[str, Any]:
    started = time.process_time()
    n = len(coeffs) - 1
    lead = mpz(coeffs[-1])
    content = mpz(0)
    for c in coeffs:
        content = GMP.gcd(content, c)
    possible: int | None = None
    rows = []
    skipped = []
    q = start
    while len(rows) < primes:
        q = next_prime(q)
        if lead % q == 0:
            skipped.append({"q": q, "reason": "divides the leading coefficient"})
            continue
        ring = ModPoly(q)
        f = np.array([int(c % q) for c in coeffs], dtype=np.int64)
        f = (f * pow(int(f[-1]), -1, q)) % q
        if ring.gcd(f, ring.derivative(f)).size > 1:
            skipped.append(
                {"q": q, "reason": "p mod q is not squarefree (q divides the discriminant)"}
            )
            continue
        t0 = time.process_time()
        degrees = distinct_degree_pattern(ring, f)
        if sum(degrees) != n:
            raise ArithmeticError(f"q={q}: factor degrees sum to {sum(degrees)}, not {n}")
        sums = 1
        for d in degrees:
            sums |= sums << d
        possible = sums if possible is None else possible & sums
        left = [d for d in range(1, n) if possible >> d & 1]
        rows.append(
            {
                "q": q,
                "factor_count": len(degrees),
                "degrees": degrees,
                "possible_left": len(left),
                "cpu_seconds": round(time.process_time() - t0, 1),
            }
        )
        if stop_when_empty and not left:
            if out_log is not None:
                print(
                    f"q={q}: {len(degrees)} factors; certificate empty",
                    file=out_log,
                    flush=True,
                )
            break
        if out_log is not None:
            print(
                f"q={q}: {len(degrees)} factors, smallest {degrees[:6]}, possible proper "
                f"factor degrees left {len(left)} ({rows[-1]['cpu_seconds']} s)",
                file=out_log,
                flush=True,
            )
    left = [d for d in range(1, n) if possible is not None and possible >> d & 1]
    emptied = next((i + 1 for i, r in enumerate(rows) if r["possible_left"] == 0), None)
    return {
        "method": (
            "distinct-degree factorization modulo primes below 2^16 (gmpy2 Kronecker "
            "multiplication, numpy); degree-pattern certificate"
        ),
        "degree": n,
        "content": int(content),
        "primes": rows,
        "skipped": skipped,
        "possible_proper_factor_degrees": left,
        "certificate_empty_after_primes": emptied,
        "irreducible_over_Q": bool(content == 1 and not left),
        "cpu_seconds": round(time.process_time() - started, 1),
    }


# --- the price of the deterministic identities -----------------------------------------------


def bits(value: Any) -> int:
    return int(GMP.bit_length(abs(mpz(value))))


def price(
    coeffs: Sequence[Any],
    params: Sequence[Path],
    system: Path,
    seconds_per_prime: float,
    identities: int,
) -> dict[str, Any]:
    """Size an exact residue and a modular proof against the resultant bound."""
    started = time.process_time()

    n = len(coeffs) - 1
    lead = mpz(coeffs[-1])
    growth = []
    # x^(n+j) mod p over Q, j = 0..6: the exact remainder's common denominator, measured.
    remainder = [Fraction(-int(c), int(lead)) for c in coeffs[:-1]]
    for j in range(7):
        common = math.lcm(*(r.denominator for r in remainder))
        growth.append(
            {
                "power": n + j,
                "denominator_bits": common.bit_length(),
                "lead_bits_times_j_plus_1": bits(lead) * (j + 1),
            }
        )
        top = remainder[-1]
        remainder = [Fraction(0), *remainder[:-1]]
        remainder = [
            r + top * Fraction(-int(c), int(lead))
            for r, c in zip(remainder, coeffs[:-1], strict=True)
        ]
    parsed = parse_system(system)
    p_bits = max(bits(c) for c in coeffs)
    p_norm2_bits = p_bits + math.ceil(math.log2(math.sqrt(n + 1)))
    derivative_l1_bits = math.ceil(math.log2(n)) + p_bits + math.ceil(math.log2(n + 1))
    g_bits, d_bits = [], []
    for path in params:
        g = json.loads(path.read_text())["g"][0]
        values = [mpz(c) for c in g["num_ascending"]]
        g_bits.append(max(bits(c) for c in values) + math.ceil(math.log2(len(values))))
        d_bits.append(bits(g["den"]))

    def multiply_seconds(left_bits: int, right_bits: int) -> float:
        a, b = mpz(1) << left_bits, (mpz(1) << right_bits) - 1
        t0 = time.perf_counter()
        for _ in range(20):
            _ = a * b
        return (time.perf_counter() - t0) / 20

    def bound(name: str, terms: list[tuple[tuple[int, ...], Any, int]]) -> dict[str, Any]:
        """Degree and height of the cleared numerator H of a polynomial identity in tau.

        ``terms`` are (monomial, coefficient, extra x-degree); H = prod_i (d_i p')^{M_i} f(tau).
        """
        top = [max(m[i] for m, _, _ in terms) for i in range(len(parsed.names))]
        coefficient_bits = max(
            bits(Fraction(str(c)).numerator) + bits(Fraction(str(c)).denominator)
            for _, c, _ in terms
        )
        height = (
            coefficient_bits
            + math.ceil(math.log2(len(terms)))
            + max(
                sum(
                    m[i] * g_bits[i] + (top[i] - m[i]) * (d_bits[i] + derivative_l1_bits)
                    for i in range(len(top))
                )
                for m, _, _ in terms
            )
        )
        degree = sum(top) * (n - 1) + max(extra for _, _, extra in terms)
        resultant_bits = degree * p_norm2_bits + n * (
            height + math.ceil(math.log2(math.sqrt(degree + 1)))
        )
        divisions = (degree - n + 1) * (n + 1)
        seconds = divisions * multiply_seconds(height, p_bits)
        return {
            "identity": name,
            "numerator_degree_bound": degree,
            "numerator_height_bits_bound": height,
            "exact_numerator_gigabytes": round(degree * height / 8 / 1e9, 2),
            "exact_division_cpu_hours_estimate": round(seconds / 3600, 1),
            "resultant_bits_bound": resultant_bits,
            "bad_primes_bound": resultant_bits // 61 + 1,
        }

    rows = [
        bound(f"F_{k + 1}(tau) = 0", [(m, c, 0) for m, c in f.terms()])
        for k, f in enumerate(parsed.polynomials)
    ]
    side_terms = [(m, c, 0) for m, c in parsed.side_numerator.terms()] + [
        (m, -c, 1) for m, c in parsed.side_denominator.terms()
    ]
    sample = bound("Sn(tau) - x Sd(tau) = 0 (the sample: least degree)", side_terms)
    primes_needed = max(r["bad_primes_bound"] for r in [*rows, sample]) + 1
    return {
        "sample_identity": sample,
        "exact_route": {
            "method": (
                "build each cleared numerator H in Z[x] and test p | H by exact division "
                "(Gauss's lemma: p is primitive)"
            ),
            "memory_gigabytes": {
                r["identity"]: r["exact_numerator_gigabytes"] for r in [*rows, sample]
            },
            "cpu_hours_estimate": round(
                sum(r["exact_division_cpu_hours_estimate"] for r in [*rows, sample]), 1
            ),
            "measured_denominator_growth_of_x_power_reductions": growth,
            "note": (
                "the cost is the classical exact division, quotient steps times p's "
                "coefficients, at a multiplication time measured here; the reduced "
                "representatives in Q[x]/(p) are far smaller than lc(p)^(n-1) suggests "
                "(their common denominator grows about 20 bits a degree, measured), "
                "but no reduction-based route avoids an exact product per term"
            ),
        },
        "modular_route": {
            "method": (
                "zero modulo enough primes above 2^61 that their product exceeds the "
                "resultant bound of p and H"
            ),
            "identities": rows,
            "primes_needed_above_2^61": primes_needed,
            "measured_seconds_per_prime_all_identities": seconds_per_prime,
            "cpu_hours": round(primes_needed * seconds_per_prime / 3600, 1),
            "identities_checked_per_prime": identities,
        },
        "cpu_seconds": round(time.process_time() - started, 1),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    one = sub.add_parser("isolate")
    one.add_argument("--poly", type=Path, required=True)
    one.add_argument("--lo", required=True)
    one.add_argument("--hi", required=True)
    one.add_argument(
        "--rational", help="also decide p's sign there and the root's order against it"
    )
    one.add_argument(
        "--order",
        type=int,
        default=300,
        help="Taylor terms available to the monotonicity bound",
    )
    one.add_argument("--out", type=Path)
    two = sub.add_parser("irreducible")
    two.add_argument("--poly", type=Path, required=True)
    two.add_argument("--primes", type=int, default=12)
    two.add_argument(
        "--start",
        type=int,
        default=40000,
        help="primes are taken upward from here (below 2^16 keeps products in 6-byte slots)",
    )
    two.add_argument(
        "--stop-when-empty",
        action="store_true",
        help="stop at the first prime that leaves no possible factor degree",
    )
    two.add_argument("--out", type=Path)
    three = sub.add_parser("price")
    three.add_argument("--poly", type=Path, required=True)
    three.add_argument("--params", type=Path, nargs="+", required=True)
    three.add_argument("--system", type=Path, required=True)
    three.add_argument("--seconds-per-prime", type=float, required=True)
    three.add_argument("--identities", type=int, default=6)
    three.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    coeffs = load_poly(args.poly)
    if args.command == "isolate":
        result: dict[str, Any] = {
            "isolation": isolate(coeffs, Fraction(args.lo), Fraction(args.hi), order=args.order)
        }
        result["interval"] = [args.lo, args.hi]
        if args.rational:
            result["comparison"] = compare(coeffs, result["isolation"], Fraction(args.rational))
        ok = result["isolation"]["exactly_one_root"]
    elif args.command == "irreducible":
        result = irreducible(
            coeffs, args.primes, args.start, sys.stdout, stop_when_empty=args.stop_when_empty
        )
        ok = result["irreducible_over_Q"]
    else:
        result = price(
            coeffs, args.params, args.system, args.seconds_per_prime, args.identities
        )
        ok = True
    text = json.dumps(result, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text)
    print(text[:2500])
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
