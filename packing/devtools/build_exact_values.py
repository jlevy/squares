#!/usr/bin/env python3
"""Collect and check every exact fact the frontier holds about the side of each packing.

The frontier records are the system of record: each `reported_upper_bound` carries the
side's closed form, its degree over the rationals, its minimal polynomial, and where each
came from (`algebraic_source`). For an open record without that identity, a verified
rational bound is admitted only when it equals both current decimals exactly and its
retained certificate and passing replay bind the current source and count. Native witness
sides and outward ceilings carry distinct provenance; neither establishes an ideal contact
packing or optimality. This register is a view of those records and proof inputs, one
entry per `n`, and the paper on exact side values renders from it and from nothing else.

A view that only copied the records would add nothing, so every polynomial is checked
here rather than transcribed, and every check is exact -- no float decides anything:

1. **Irreducible over Q.** A linear polynomial is; up to degree 12 SymPy's factorisation
   must return one factor of full degree; above that, the degrees of the distinct-degree
   factorisation modulo successive good primes leave no proper factor degree possible.
2. **One real root where the side is.** A rational interval around Evan Daniel's 39-digit
   KKT value (or the record's own decimal, where the KKT value disagrees or is missing)
   carries a sign change of the polynomial, and an enclosure of the derivative over it
   that excludes zero proves the root unique there: rational interval Horner first, the
   centred Taylor form where Horner's widening is too large, bisection where neither
   decides. The root's 40-digit decimal is read off by exact bisection.
3. **The record agrees.** The recorded decimal must agree with that root to its printed
   digits, by truncation or by rounding. A verified SQUISH rational upper bound may use
   its upward decimal ceiling instead. A polynomial that misses the record is a wrong
   polynomial, and the build fails on it.
4. **The source agrees.** A transcribed polynomial must equal the catalogue's; a derived
   one must equal what `sqpack.exact_values.derive_from_exact_form` computes from the
   record's closed form now (think-kj6n), and an exact interval enclosure of the closed
   form must lie inside the isolated root's cell.
5. **Galois data** for degrees 2 to 6, from SymPy, including whether the group is
   solvable -- which is what says a radical form cannot exist at n = 28 and n = 39.

Where the record holds nothing exact, the entry says why and which bead owns the route
to a value, and every polynomial the catalogue prints for a packing that has since been
beaten is reported as a note, never as the side.

`--check` rebuilds the register from the records and compares bytes; `--review` prints
the totals and every check worth a second look.
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from functools import cache
from math import gcd, isqrt
from pathlib import Path
from typing import Any, cast

import numpy as np
import numpy.typing as npt
import sympy as sp
from sympy.polys.domains import ZZ
from sympy.polys.galoistools import gf_ddf_zassenhaus, gf_from_int_poly, gf_monic, gf_sqf_p
from sympy.polys.numberfields.galoisgroups import galois_group

from devtools import (
    acquire_source,
    refinement_custody,
    refinement_house_links,
    refinement_packets,
    upper_bound_packets,
)
from devtools import collect_reported_exact_roots as reported_roots
from devtools import couzo_followup_reports as couzo_followup
from devtools import couzo_refinement_reports as couzo_refinements
from devtools import evand_arrangement_houses as arrangement_houses
from devtools import evand_arrangement_reports as arrangement_reports
from devtools import evand_exact_certificates as evand
from devtools import evand_hunt_reports as hunt_reports
from devtools import gupta_house_links as gupta_houses
from devtools import ryxu_house_links as ryxu_houses
from devtools.retained_data import (
    compressed_path,
    read_retained_text,
    retained_exists,
    write_retained_text,
)
from sqpack import retained_json
from sqpack.exact_values import (
    CATALOGUE,
    DERIVED_FROM_EXACT_FORM,
    algebraic_fields,
    derive_from_exact_form,
    format_polynomial,
)
from sqpack.kingbird_catalogue import (
    CATALOGUE_MARKDOWN,
    CatalogueEntry,
    normalized_polynomial,
    parse_catalogue,
)
from sqpack.known_best import KNOWN_BEST_CORPUS
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
RECORD = FRONTIER / "exact-values.json"
GENERATOR = "python -m devtools.build_exact_values"
CONTRACT = "packing.squares:ExactValues/v1"
SCHEMA = "exact-values.schema.yaml"

#: Evan Daniel's exact-contact batch: numerical KKT points computed at 80 digits
#: and printed to 39 significant digits, independent of every source this register reads.
KKT_BATCH = (
    "resources/web/evand-square-packing-2026-10-05/square-packing/s12/search/exact/"
    "batch/results.json.gz"
)
KKT_KEY = "[evand exact optima 2026-10-05]"
KKT_DIGITS = 39
KKT_LOCAL_MIN = "KKT local min"
#: Below this many digits of agreement with a KKT local minimum, a polynomial's root and
#: Daniel's value are not the same number at the precision both claim, and the entry
#: says so in a note. It does not fail the build: the record, not the batch, is the
#: system of record, and the record's own agreement is what fails it.
KKT_AGREEMENT_FLOOR = 30

CATALOGUE_KEY = "[Kingbird]"
DERIVED_FROM_SOURCE_CLOSED_FORM = "derived-from-source-closed-form"
#: Retained exact replay evidence for sources whose rational bounds use upward displays.
CERTIFIED_CEILING_SOURCES = {
    "[SQUISH ten packings 2026-10-07]": "E-squish-ten-packings-2026-10-07-exact-replay",
    "[SQUISH n153 2026-10-07]": "E-squish-n153-2026-10-07-exact-replay",
    "[SQUISH update 2026-10-07]": "E-squish-update-2026-10-07-exact-replay",
    "[SQUISH second update 2026-10-07]": "E-squish-second-update-2026-10-07-exact-replay",
}
SVG_FACTS = "resources/web/kingbird-exact-side-facts-2026-10-07/facts"
HISTORICAL_FACTS = (
    "resources/web/kingbird-exact-side-facts-2026-10-07/facts/historical-polynomials.json"
)
SVG_RECEIPTS = "resources/web/known-best-packings/receipts/kingbird-2026-10-05-pictures.json"
#: Significant digits of the root's decimal.
DECIMAL_DIGITS = 40
#: The decimal grid every root is refined onto: a power of ten finer than any value the
#: register compares a root with (39 significant digits at most, sides below 100).
GRID_PLACES = 45
#: Half-width of the window around the KKT value in which the root is first sought.
KKT_WINDOW = Fraction(1, 10**30)
#: Exact factorisation is cheap to this degree; above it the modular certificate is used.
FACTORIZATION_MAX_DEGREE = 12
#: How many primes the modular certificate may try before the build refuses.
PRIME_BUDGET = 200
#: Galois groups SymPy computes, and the register records, for these degrees only.
GALOIS_DEGREES = range(2, 7)

#: Every current numeric-only count has a named lane and an owning bead.
ROUTES: dict[int, tuple[str, str]] = {
    29: (
        "think-je8y",
        (
            "The defining six-equation contact system is retained (X-004); exact "
            "elimination and real-branch certification remain open."
        ),
    ),
    55: (
        "think-phh8",
        (
            "Kingbird's square-55.svg retains seven exact contact/stationarity equations "
            "and credits David Ellsworth. Eliminate them and certify the current real branch."
        ),
    ),
    71: (
        "think-1blg",
        (
            "Kingbird's square-71.svg retains six exact contact equations and credits "
            "David Ellsworth. Eliminate them and certify the current real branch; the "
            "two retained historical polynomials describe weaker packings."
        ),
    ),
}
#: Disjoint sweep and seed lanes from the continuation plan. Claimed outputs must be
#: recovered and replayed before they can count as identifications.
ROUTE_GROUPS = (
    (
        (102, 106, 152, 172, 177, 206, 268, 297, 301),
        "think-ohhz",
        (
            "Earlier beads claim a polynomial identification, but its referenced output "
            "is unavailable on this branch. Recover or reproduce it (think-s6np), then "
            "check coefficients, irreducibility, root, and current contact branch."
        ),
    ),
    (
        (68, 103, 110, 131, 132, 156),
        "think-056g",
        (
            "Recover the digest-pinned KKT input (think-s6np), re-solve at rising precision, "
            "and run a bounded integer-relation search in the low-count sweep; "
            "retain scoped negatives."
        ),
    ),
    (
        (181, 182, 210, 228, 240, 241),
        "think-d2kj",
        (
            "Recover the digest-pinned KKT input (think-s6np), re-solve at rising precision, "
            "and run a bounded integer-relation search in the middle-count sweep; "
            "retain scoped negatives."
        ),
    ),
    (
        (259, 269, 270, 271, 273, 304, 305, 306, 307),
        "think-gg4k",
        (
            "Recover the digest-pinned KKT input (think-s6np), re-solve at rising precision, "
            "and run a bounded integer-relation search in the high-count sweep; "
            "retain scoped negatives. "
            "A historical source polynomial cannot replace the current side."
        ),
    ),
)
for _counts, _bead, _route in ROUTE_GROUPS:
    for _n in _counts:
        ROUTES[_n] = (_bead, _route)
# This current-pose prerequisite must survive the group assignment above.
ROUTES[102] = (
    ROUTES[102][0],
    ROUTES[102][1]
    + " Before resuming this ideal-contact lane, bind and convert the already retained "
    "current ry-xu certificate at 8dc415296f697f5140caea27c7a0193d52deb4e6. Derive its "
    "active, weak and forced contacts and frozen variables, confirm the current-pose "
    "seed, and pass the W7 driver and n11 control before a preregistered bounded W6 "
    "run. The earlier evand 13ee36e5 input remains a historical fixture; its contact "
    "system and local-minimum claims do not transfer to this new geometry.",
)
for _n, _bead in (
    (105, "think-gl59"),
    (211, "think-uc8i"),
    (272, "think-olv8"),
    (292, "think-w622"),
):
    ROUTES[_n] = (
        _bead,
        (
            "Daniel's retained batch supplies no confirmed KKT local minimum for this "
            "count. Establish the current witness's active contact system and a stable "
            "high-precision KKT seed before attempting polynomial identification."
        ),
    )
SWEEP_BEAD = "think-eu89"
#: Recorded integer-relation searches that came back empty, with their exact scope.
RELATION_NEGATIVES: dict[int, tuple[str, int, str]] = {
    29: (
        "think-je8y",
        20,
        (
            "X-004 re-solved the system at 1200 digits and ran PSLQ at 700 digits for "
            "degrees 2 through 20, tolerance 1e-675, maxcoeff 10^22, and maxsteps 50000; "
            "no relation was found in that bounded search."
        ),
    ),
}
#: A future catalogue degree without retained coefficients gets an explicit route.
MISSING_POLYNOMIAL_TEXT: dict[int, tuple[str, str]] = {}

STATES = (
    "integer",
    "rational",
    "closed-form",
    "minimal-polynomial",
    "degree-only",
    "numeric-only",
)


class ExactValuesError(ValueError):
    """A recorded exact fact failed an exact check, or a certificate could not be found."""


# --- exact polynomial arithmetic --------------------------------------------------------


def _sign(value: int) -> int:
    return (value > 0) - (value < 0)


def _sign_at(coefficients: Sequence[int], x: Fraction) -> int:
    """The sign of the polynomial at a rational point, by homogeneous integer Horner."""
    numerator, denominator = x.numerator, x.denominator
    value = 0
    power = 1
    for index, coefficient in enumerate(coefficients):
        if index:
            power *= denominator
            value = value * numerator + coefficient * power
        else:
            value = coefficient
    return _sign(value)


def _derivative(coefficients: Sequence[int]) -> tuple[int, ...]:
    degree = len(coefficients) - 1
    return tuple(c * (degree - i) for i, c in enumerate(coefficients[:-1]))


def _enclosure_excludes_zero(coefficients: Sequence[int], lo: Fraction, hi: Fraction) -> bool:
    """Whether interval Horner over `[lo, hi]`, with `0 < lo <= hi`, excludes zero.

    Exact: both endpoints share one denominator and every partial value is an integer
    scaled by its power, so the enclosure is computed without rounding and without the
    gcds `Fraction` would take at every step. Positive `x` makes the product rule a sign
    test on the lower and upper ends rather than four products.
    """
    if lo <= 0:
        raise ExactValuesError("interval Horner here is for positive intervals only")
    denominator = lo.denominator * hi.denominator // gcd(lo.denominator, hi.denominator)
    low_x = lo.numerator * (denominator // lo.denominator)
    high_x = hi.numerator * (denominator // hi.denominator)
    low = high = coefficients[0]
    power = 1
    for coefficient in coefficients[1:]:
        power *= denominator
        low = low * low_x if low >= 0 else low * high_x
        high = high * high_x if high >= 0 else high * low_x
        low += coefficient * power
        high += coefficient * power
    return low > 0 or high < 0


def _taylor_shift(coefficients: Sequence[int], shift: int) -> list[int]:
    """The coefficients of `B(u + shift)`, highest first, by repeated synthetic division."""
    shifted = list(coefficients)
    size = len(shifted)
    for done in range(size - 1):
        for index in range(1, size - done):
            shifted[index] += shift * shifted[index - 1]
    return shifted


def _centred_form_excludes_zero(
    coefficients: Sequence[int], lo: Fraction, hi: Fraction
) -> bool:
    """Whether the centred (Taylor) form of the polynomial over `[lo, hi]` excludes zero.

    Interval Horner widens by the polynomial's condition number, which for a degree-38
    polynomial with 44-digit coefficients is more than a 10^-30 window can absorb. The
    centred form does not: with the exact Taylor coefficients `r_k` at the midpoint, the
    value over the window lies within `r_0 +- sum |r_k| h^k`, and that excludes zero as
    soon as the window is narrower than the root's distance to its neighbours. Integers
    throughout: with `c = C/D` and `h = H/D`, `D^e p(c + t) = sum r_k (D t)^k`, where `r`
    is the integer polynomial `D^e p(Y/D)` shifted by `C`.
    """
    centre, half = (lo + hi) / 2, (hi - lo) / 2
    denominator = (
        centre.denominator * half.denominator // gcd(centre.denominator, half.denominator)
    )
    shift = centre.numerator * (denominator // centre.denominator)
    radius = half.numerator * (denominator // half.denominator)
    scaled = [c * denominator**index for index, c in enumerate(coefficients)]
    shifted = _taylor_shift(scaled, shift)
    constant = shifted[-1]
    bound = 0
    power = 1
    for coefficient in reversed(shifted[:-1]):
        power *= radius
        bound += abs(coefficient) * power
    return abs(constant) > bound


def _excludes_zero(coefficients: Sequence[int], lo: Fraction, hi: Fraction) -> bool:
    """Interval Horner first, being cheap; the centred form where it is too wide."""
    return _enclosure_excludes_zero(coefficients, lo, hi) or _centred_form_excludes_zero(
        coefficients, lo, hi
    )


@dataclass(frozen=True)
class Root:
    """A real root of an integer polynomial, held exactly.

    Either `exact` is the rational root itself (degree one), or the root lies strictly
    inside the open cell `(lo, hi)` of the decimal grid and is the only root in a larger
    window the certificate proved. For an interior comparison point, its polynomial
    sign and the lower endpoint's sign decide which side of the unique root it lies on.
    This remains exact even when the comparison has more decimal places than the cell.
    """

    coefficients: tuple[int, ...]
    lo: Fraction
    hi: Fraction
    exact: Fraction | None = None

    def compare(self, x: Fraction) -> int:
        """-1, 0 or 1 as the root is below, equal to, or above `x`."""
        if self.exact is not None:
            return (self.exact > x) - (self.exact < x)
        if x <= self.lo:
            return 1
        if x >= self.hi:
            return -1
        point_sign = _sign_at(self.coefficients, x)
        if point_sign == 0:
            raise ExactValuesError("a rational root of an irreducible polynomial")
        return 1 if point_sign == _sign_at(self.coefficients, self.lo) else -1


def _grid(value: Fraction) -> int:
    scaled = value * 10**GRID_PLACES
    if scaled.denominator != 1:
        raise ExactValuesError(f"{value} is not on the 10^-{GRID_PLACES} grid")
    return scaled.numerator


def unique_root_in(coefficients: tuple[int, ...], lo: Fraction, hi: Fraction) -> bool:
    """Whether the polynomial has exactly one root in `[lo, hi]`, decided exactly.

    The window is split until each piece either has a derivative enclosure excluding
    zero (the polynomial is monotone there, so a sign change at its ends is one root and
    no sign change is none) or a value enclosure excluding zero (no root). A piece that
    is neither after forty halvings refuses rather than guesses.
    """
    derivative = _derivative(coefficients)
    roots = 0
    stack: list[tuple[Fraction, Fraction, int]] = [(lo, hi, 0)]
    while stack:
        a, b, depth = stack.pop()
        if _excludes_zero(derivative, a, b):
            sign_a, sign_b = _sign_at(coefficients, a), _sign_at(coefficients, b)
            if sign_a == 0 or sign_b == 0:
                raise ExactValuesError("a root on a bisection point")
            roots += sign_a != sign_b
            continue
        if _excludes_zero(coefficients, a, b):
            continue
        if depth >= 40:
            raise ExactValuesError(
                f"could not separate the roots in [{float(lo)}, {float(hi)}]"
            )
        middle = (a + b) / 2
        stack.extend(((a, middle, depth + 1), (middle, b, depth + 1)))
    return roots == 1


def _decimal_places(text: str) -> int:
    exponent = Decimal(text).as_tuple().exponent
    return -exponent if isinstance(exponent, int) and exponent < 0 else 0


def _significant_digits(text: str) -> int:
    return len(text.replace(".", "").lstrip("0").replace("-", "")) or 1


def isolate_root(
    coefficients: tuple[int, ...], record_value: str, kkt_value: str | None
) -> tuple[Root, str]:
    """The unique real root near the side, and which window proved it.

    The first window is the KKT value plus or minus 10^-30; where that carries no sign
    change, or there is no KKT value, the record's decimal plus or minus ten of its last
    printed units. Each window must show a sign change and a single root.
    """
    if len(coefficients) == 2:
        exact = Fraction(-coefficients[1], coefficients[0])
        return Root(coefficients, exact, exact, exact), "exact"
    windows: list[tuple[str, Fraction, Fraction]] = []
    if kkt_value is not None:
        windows.append(("kkt", Fraction(Decimal(kkt_value)), KKT_WINDOW))
    places = _decimal_places(record_value)
    windows.append(("record", Fraction(Decimal(record_value)), Fraction(10, 10**places)))
    for name, centre, half_width in windows:
        lo, hi = centre - half_width, centre + half_width
        sign_lo, sign_hi = _sign_at(coefficients, lo), _sign_at(coefficients, hi)
        if sign_lo * sign_hi >= 0:
            continue
        if not unique_root_in(coefficients, lo, hi):
            raise ExactValuesError(
                f"more than one root within {float(half_width):.0e} of the side"
            )
        low, high = _grid(lo), _grid(hi)
        while high - low > 1:
            middle = (low + high) // 2
            sign = _sign_at(coefficients, Fraction(middle, 10**GRID_PLACES))
            if sign == 0:
                raise ExactValuesError("a rational root of an irreducible polynomial")
            if sign == sign_lo:
                low = middle
            else:
                high = middle
        cell = Root(
            coefficients,
            Fraction(low, 10**GRID_PLACES),
            Fraction(high, 10**GRID_PLACES),
        )
        return cell, name
    raise ExactValuesError(
        f"no sign change of the polynomial near the recorded side {record_value}"
    )


def root_decimal(root: Root, digits: int = DECIMAL_DIGITS) -> str:
    """The root to `digits` significant digits, correctly rounded, decided exactly."""
    integer_digits = len(str(int(root.lo if root.exact is None else root.exact)))
    for places in (digits - integer_digits, digits - integer_digits - 1):
        unit = Fraction(1, 10**places)
        if root.exact is not None:
            scaled = root.exact * 10**places
            floor = scaled.numerator // scaled.denominator
        else:
            floor = (root.lo.numerator * 10**places) // root.lo.denominator
        half = (Fraction(floor) + Fraction(1, 2)) * unit
        rounded = floor + (root.compare(half) >= 0)
        text = str(rounded)
        if len(text) <= digits:
            return f"{text[: len(text) - places]}.{text[len(text) - places :]}"
    raise ExactValuesError("could not round the root")  # pragma: no cover - unreachable


def agreement_digits(root: Root, value: str, cap: int) -> int:
    """How many significant digits of `value` the root confirms, at most `cap`.

    The largest `k <= cap` with `|root - value|` below one unit in the `k`-th significant
    place of the root, decided exactly. A value equal to the root confirms all `cap`.
    """
    target = Fraction(Decimal(value))
    leading = len(str(int(root.lo if root.exact is None else root.exact))) - 1
    for k in range(cap, 0, -1):
        unit = Fraction(10) ** (leading - k + 1)
        if root.compare(target - unit) > 0 and root.compare(target + unit) < 0:
            return k
    return 0


def contains_recorded_side(root: Root, value: str, *, upward_ceiling: bool = False) -> bool:
    """Whether the decimal uses the allowed rounding convention at its printed places."""
    unit = Fraction(1, 10 ** _decimal_places(value))
    printed = Fraction(Decimal(value))
    if upward_ceiling:
        return root.compare(printed - unit) > 0 and root.compare(printed) <= 0
    return root.compare(printed - unit / 2) >= 0 and root.compare(printed + unit) < 0


# --- irreducibility ---------------------------------------------------------------------


@cache
def first_primes(count: int) -> tuple[int, ...]:
    """The first `count` primes, in order, by trial division."""
    primes: list[int] = []
    candidate = 2
    while len(primes) < count:
        if all(candidate % prime for prime in primes if prime * prime <= candidate):
            primes.append(candidate)
        candidate += 1
    return tuple(primes)


def _sub_degrees(factor_degrees: Sequence[int], degree: int) -> set[int]:
    """The degrees a proper factor could have, given one prime's factor degrees."""
    sums = {0}
    for factor_degree in factor_degrees:
        sums |= {total + factor_degree for total in sums}
    return {total for total in sums if 0 < total < degree}


def reference_factor_degrees_mod(coefficients: Sequence[int], prime: int) -> list[int] | None:
    """SymPy's distinct-degree factorisation, kept as the reference the fast one is tested by.

    Pure Python, and about seven times slower than `factor_degrees_mod` at degree 158; the
    two must agree, and `tests/test_build_exact_values.py` holds them to it.
    """
    if coefficients[0] % prime == 0:
        return None
    _, reduced = gf_monic(gf_from_int_poly(list(coefficients), prime), prime, ZZ)
    if not gf_sqf_p(reduced, prime, ZZ):
        return None
    degrees: list[int] = []
    for factor, degree in gf_ddf_zassenhaus(reduced, prime, ZZ):
        degrees.extend([degree] * ((len(factor) - 1) // degree))
    return degrees


type _Vector = npt.NDArray[np.int64]


def _trim_mod(vector: _Vector) -> _Vector:
    nonzero = np.flatnonzero(vector)
    return vector[nonzero[0] :] if len(nonzero) else vector[:0]


def _divmod_mod(dividend: _Vector, divisor: _Vector, prime: int) -> tuple[_Vector, _Vector]:
    """Quotient and remainder over GF(prime), highest degree first.

    One vectorised row operation per quotient term. Every entry stays below `prime`
    and factor_degrees_mod checks the degree/prime product bound before calling it.
    """
    remainder = dividend.copy()
    degree = len(divisor) - 1
    if len(remainder) <= degree:
        return remainder[:0], _trim_mod(remainder)
    inverse = pow(int(divisor[0]), -1, prime)
    quotient = np.zeros(len(remainder) - degree, dtype=np.int64)
    for index in range(len(remainder) - degree):
        term = (int(remainder[index]) * inverse) % prime
        if term:
            quotient[index] = term
            window = slice(index, index + degree + 1)
            remainder[window] = (remainder[window] - term * divisor) % prime
    return quotient, _trim_mod(remainder[len(remainder) - degree :])


def _gcd_mod(left: _Vector, right: _Vector, prime: int) -> _Vector:
    """The monic greatest common divisor over GF(prime)."""
    while len(right):
        left, right = right, _divmod_mod(left, right, prime)[1]
    return (left * pow(int(left[0]), -1, prime)) % prime


def _mulmod(left: _Vector, right: _Vector, modulus: _Vector, prime: int) -> _Vector:
    # Both convolution and matrix products are bounded by degree * (prime - 1)^2;
    # factor_degrees_mod refuses inputs outside int64 before any arithmetic runs.
    return _divmod_mod(np.convolve(left, right) % prime, modulus, prime)[1]


def factor_degrees_mod(coefficients: Sequence[int], prime: int) -> list[int] | None:
    """The degrees of the irreducible factors modulo `prime`, or None for a bad prime.

    A bad prime divides the leading coefficient or leaves the reduction with a repeated
    factor; neither says anything about factors over the rationals.

    Distinct-degree factorisation with the Frobenius map as a matrix: row `j` of `Q` is
    `x^(pj) mod f`, so `h^p` is one vector-matrix product, and the factors of degree `i`
    are `gcd(f, x^(p^i) - x)` once the lower degrees are divided out. NumPy carries the
    arithmetic, all of it exact in int64.
    """
    if prime < 2 or (len(coefficients) - 1) * (prime - 1) ** 2 >= 2**63:
        raise ExactValuesError("modular arithmetic would exceed the exact int64 bound")
    if coefficients[0] % prime == 0:
        return None
    modulus = np.array([c % prime for c in coefficients], dtype=np.int64)
    modulus = (modulus * pow(int(modulus[0]), -1, prime)) % prime
    degree = len(modulus) - 1
    derivative = _trim_mod(
        np.array(
            [(int(c) * (degree - k)) % prime for k, c in enumerate(modulus[:-1])],
            dtype=np.int64,
        )
    )
    if not len(derivative) or len(_gcd_mod(modulus, derivative, prime)) > 1:
        return None
    frobenius = np.array([1], dtype=np.int64)
    base = np.array([1, 0], dtype=np.int64)
    exponent = prime
    while exponent:
        if exponent & 1:
            frobenius = _mulmod(frobenius, base, modulus, prime)
        exponent >>= 1
        if exponent:
            base = _mulmod(base, base, modulus, prime)
    matrix = np.zeros((degree, degree), dtype=np.int64)
    row = np.array([1], dtype=np.int64)
    for power in range(degree):
        matrix[power, : len(row)] = row[::-1]
        row = _mulmod(row, frobenius, modulus, prime)
    power_of_x = np.zeros(degree, dtype=np.int64)
    power_of_x[1] = 1
    remaining = modulus
    degrees: list[int] = []
    step = 0
    while True:
        step += 1
        if 2 * step > len(remaining) - 1:
            if len(remaining) > 1:
                degrees.append(len(remaining) - 1)
            return degrees
        power_of_x = (power_of_x @ matrix) % prime
        difference = np.zeros(max(degree, 2), dtype=np.int64)
        difference[: len(power_of_x)] = power_of_x
        difference[1] = (difference[1] - 1) % prime
        difference = _trim_mod(difference[::-1].copy())
        common = _gcd_mod(remaining, difference, prime) if len(difference) else remaining
        if len(common) > 1:
            degrees.extend([step] * ((len(common) - 1) // step))
            remaining = _divmod_mod(remaining, common, prime)[0]


def modular_certificate(
    coefficients: Sequence[int], budget: int = PRIME_BUDGET
) -> list[int] | None:
    """The good primes, in order, whose factor degrees together exclude every factor."""
    degree = len(coefficients) - 1
    possible = set(range(1, degree))
    used: list[int] = []
    for prime in first_primes(budget):
        degrees = factor_degrees_mod(coefficients, prime)
        if degrees is None:
            continue
        used.append(prime)
        possible &= _sub_degrees(degrees, degree)
        if not possible:
            return used
    return None


def verify_modular_certificate(coefficients: Sequence[int], primes: Sequence[int]) -> bool:
    """Re-check a stored certificate: its primes alone must exclude every factor degree."""
    degree = len(coefficients) - 1
    possible = set(range(1, degree))
    for prime in primes:
        degrees = factor_degrees_mod(coefficients, prime)
        if degrees is None:
            return False
        possible &= _sub_degrees(degrees, degree)
    return not possible


def irreducibility(coefficients: tuple[int, ...], budget: int = PRIME_BUDGET) -> dict:
    """An irreducibility certificate over Q, or `ExactValuesError` if none is found."""
    degree = len(coefficients) - 1
    if degree < 1:
        raise ExactValuesError("a constant is not a minimal polynomial")
    if degree == 1:
        return {"method": "linear", "primes": []}
    if degree <= FACTORIZATION_MAX_DEGREE:
        side = sp.Symbol("s")
        _, factors = sp.Poly(list(coefficients), side).factor_list()
        if len(factors) != 1 or factors[0][1] != 1 or factors[0][0].degree() != degree:
            raise ExactValuesError(f"reducible over Q: {format_polynomial(coefficients)}")
        return {"method": "factorization", "primes": []}
    primes = modular_certificate(coefficients, budget)
    if primes is None:
        raise ExactValuesError(
            f"no irreducibility certificate for a degree-{degree} polynomial within the "
            f"first {budget} primes"
        )
    return {"method": "modular-degree-patterns", "primes": primes}


# --- formatting -------------------------------------------------------------------------


def polynomial_latex(coefficients: Sequence[int]) -> str:
    """LaTeX for the polynomial in `s`, highest degree first: `2s^{2} - 28s + 97`."""
    degree = len(coefficients) - 1
    terms: list[str] = []
    for index, coefficient in enumerate(coefficients):
        if coefficient == 0:
            continue
        power = degree - index
        magnitude = abs(coefficient)
        monomial = "" if power == 0 else "s" if power == 1 else f"s^{{{power}}}"
        body = str(magnitude) if power == 0 or magnitude != 1 else ""
        body += monomial
        if not terms:
            terms.append(body if coefficient > 0 else f"-{body}")
        else:
            terms.append(f"+ {body}" if coefficient > 0 else f"- {body}")
    return " ".join(terms)


_SQRT_INNER = re.compile(r"sqrt\(([^()]*)\)")
_FRACTION_PAREN = re.compile(r"\((\d+)/(\d+)\)")
_FRACTION_BARE = re.compile(r"(?<![\d{])(\d+)/(\d+)")
_COEFFICIENT_SPACE = re.compile(r"(\d|\})\s+\\sqrt")
_LATEX_ALLOWED = re.compile(r"^[0-9 +\-\\{}a-z]*$")
_LATEX_FRACTION = re.compile(r"\\(?:tfrac|frac)\{([^{}]+)\}\{([^{}]+)\}")
_LATEX_SQRT_INNER = re.compile(r"\\sqrt\{([^{}]*)\}")


def parse_form(text: str) -> sp.Expr:
    from sympy.parsing.sympy_parser import (  # noqa: PLC0415 - one parser, as exact_values
        implicit_multiplication_application,
        parse_expr,
        standard_transformations,
    )

    transformations = (*standard_transformations, implicit_multiplication_application)
    return parse_expr(text, transformations=transformations)


def latex_to_form(latex: str) -> str:
    """The inverse of `exact_form_latex` on the forms it writes, for the round trip."""
    text = latex
    while True:
        replaced = _LATEX_SQRT_INNER.sub(r" sqrt(\1)", text)
        replaced = _LATEX_FRACTION.sub(r"(\1)/(\2)", replaced)
        if replaced == text:
            return " ".join(text.split())
        text = replaced


def exact_form_latex(exact_form: str) -> str:
    """LaTeX for a record's closed form, in the record's own order of terms.

    `(1/2)sqrt(2)` becomes `\\tfrac{1}{2}\\sqrt{2}`. A form outside the small grammar the
    records use falls back to SymPy's LaTeX of the parsed value, and either way the result
    is read back and must denote the same number.
    """
    text = exact_form
    while True:
        replaced = _SQRT_INNER.sub(r"\\sqrt{\1}", text)
        if replaced == text:
            break
        text = replaced
    text = _FRACTION_PAREN.sub(r"\\tfrac{\1}{\2}", text)
    text = _FRACTION_BARE.sub(r"\\tfrac{\1}{\2}", text)
    text = _COEFFICIENT_SPACE.sub(r"\1\\sqrt", text)
    value = parse_form(exact_form)
    if _LATEX_ALLOWED.match(text) and sp.simplify(parse_form(latex_to_form(text)) - value) == 0:
        return text
    return sp.latex(value)


# --- sources ----------------------------------------------------------------------------


def load_packing(n: int) -> dict:
    text = (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    return safe_load(text.split("---", 2)[1])["packing"]


@cache
def kkt_rows() -> dict[int, dict]:
    with gzip.open(ROOT / KKT_BATCH, "rt", encoding="utf-8") as handle:
        rows = json.load(handle)
    return {int(row["n"]): row for row in rows}


@cache
def catalogue_entries() -> dict[int, CatalogueEntry]:
    return parse_catalogue()


# --- one entry --------------------------------------------------------------------------


def _monic(polynomial: str) -> bool:
    return normalized_polynomial(polynomial)[0] == 1


def _state(exact_form: str | None, degree: int | None, polynomial: str | None) -> str:
    if exact_form is not None:
        if degree != 1:
            return "closed-form"
        # A degree-1 side can be fractional (n = 50 is 7 + 4/7), so degree 1 alone does not
        # make a side an integer: its minimal polynomial is monic only when it is one.
        return "integer" if polynomial is not None and _monic(polynomial) else "rational"
    if polynomial is not None:
        return "minimal-polynomial"
    if degree is not None:
        return "degree-only"
    return "numeric-only"


def _note(kind: str, text: str, bead: str | None = None, degree: int | None = None) -> dict:
    return {"kind": kind, "text": text, "bead": bead, "degree": degree}


@cache
def _normalized(text: str) -> tuple[int, ...]:
    """`normalized_polynomial`, once per text: SymPy's parse is most of a cheap entry."""
    return normalized_polynomial(text)


def _catalogue_polynomial(entry: CatalogueEntry | None) -> tuple[int, ...] | None:
    if entry is None or entry.minimal_polynomial is None:
        return None
    return _normalized(entry.minimal_polynomial)


def _polynomial_record(coefficients: tuple[int, ...]) -> dict:
    """The complete polynomial, in the register's machine and reader forms."""
    return {
        "coefficients": [str(c) for c in coefficients],
        "text": format_polynomial(coefficients),
        "latex": polynomial_latex(coefficients),
        "height_digits": len(str(max(abs(c) for c in coefficients))),
    }


def _superseded_note(
    n: int, reported: dict, entry: CatalogueEntry | None, budget: int
) -> dict | None:
    """The catalogue's polynomial for a packing the record has since replaced, if any."""
    printed = _catalogue_polynomial(entry)
    if entry is None or printed is None:
        return None
    same_source = reported.get("source_key") == CATALOGUE_KEY
    current = reported.get("minimal_polynomial")
    if same_source and (
        str(reported["value"]) == entry.side_decimal
        or (current is not None and _normalized(str(current)) == printed)
    ):
        return None
    verb = (
        "beaten"
        if Decimal(str(reported["value"])) < Decimal(entry.side_decimal)
        else "replaced"
    )
    note = _note(
        "superseded-catalogue-polynomial",
        f"The catalogue's degree-{len(printed) - 1} polynomial is for its own packing of "
        f"side {entry.side_decimal}, since {verb} by the record's "
        f"({reported.get('source_key')}); it is not this side's minimal polynomial.",
        degree=len(printed) - 1,
    )
    checks, _ = polynomial_checks(n, printed, entry.side_decimal, None, budget)
    checks["catalogue"] = "matches"
    checks["galois"] = _galois(printed)
    note.update(
        side=entry.side_decimal,
        polynomial=_polynomial_record(printed),
        checks=checks,
    )
    return note


def _galois(coefficients: tuple[int, ...]) -> dict | None:
    if len(coefficients) - 1 not in GALOIS_DEGREES:
        return None
    side = sp.Symbol("s")
    # By name, SymPy returns a member of its transitive-subgroup enums, which it types as
    # a permutation group or None; the member carries both the name and the group.
    group = cast("Any", galois_group(sp.Poly(list(coefficients), side), by_name=True)[0])
    permutations = group.get_perm_group()
    return {
        "group": str(group.name),
        "order": int(permutations.order()),
        "solvable": bool(permutations.is_solvable),
    }


def source_check(
    n: int,
    reported: dict,
    coefficients: tuple[int, ...],
    entry: CatalogueEntry | None,
) -> str:
    """Which source the polynomial agrees with; a disagreement is a defect and raises."""
    source = reported.get("algebraic_source")
    if source == DERIVED_FROM_EXACT_FORM:
        derived = derive_from_exact_form(str(reported["exact_form"])).coefficients
        if derived != coefficients:
            raise ExactValuesError(
                f"n = {n}: the recorded polynomial {format_polynomial(coefficients)} is not "
                f"the minimal polynomial of {reported['exact_form']}, "
                f"{format_polynomial(derived)}"
            )
        return "derived-here"
    printed = _catalogue_polynomial(entry)
    if (
        source == CATALOGUE
        and printed is not None
        and entry is not None
        and reported.get("source_key") == CATALOGUE_KEY
    ):
        if printed != coefficients:
            raise ExactValuesError(
                f"n = {n}: the recorded polynomial differs from the catalogue's, "
                f"line {entry.source_line}"
            )
        return "matches"
    if source == CATALOGUE and reported.get("source_key") == CATALOGUE_KEY:
        fact = retained_svg_fact(n)
        if fact is not None:
            printed = tuple(
                int(c)
                for c in next(root for root in fact["roots"] if root["assigned_to"] == "s")[
                    "coefficients"
                ]
            )
            if printed != coefficients:
                raise ExactValuesError(f"n = {n}: the polynomial differs from the retained SVG")
            return "matches-svg"
        raise ExactValuesError(
            f"n = {n}: no retained polynomial source for this catalogue claim"
        )
    return "not-in-catalogue"


@cache
def retained_svg_fact(n: int) -> dict | None:
    """Exact source identity from a retained extraction, bound to the acquisition pin.

    The register replays its mathematics independently. A source's `verified` flag is
    not a certificate, and prime patterns from the extraction are only replay hints.
    """
    path = ROOT / SVG_FACTS / f"n-{n:03d}.json"
    if not path.exists():
        return None
    fact = json.loads(path.read_text(encoding="utf-8"))
    roots = [root for root in fact["roots"] if root["assigned_to"] == "s"]
    if not roots:
        return None
    receipts = json.loads((ROOT / SVG_RECEIPTS).read_text(encoding="utf-8"))
    pins = [pin for pin in receipts["readings"] if pin["n"] == n]
    if (
        fact["format"] != "kingbird-svg-exact-facts-v1"
        or fact["n"] != n
        or len(roots) != 1
        or len(fact["checks"]) != 1
        or len(pins) != 1
        or any(fact[key] != pins[0][key] for key in ("sha256", "bytes", "url"))
        or roots[0]["coefficients"] is None
        or roots[0]["degree"] != len(roots[0]["coefficients"]) - 1
    ):
        raise ExactValuesError(f"n = {n}: retained SVG facts do not match the pinned source")
    return fact


def enclose(expression: sp.Expr, places: int) -> tuple[Fraction, Fraction]:
    """Rational bounds on a closed form, from exact interval arithmetic.

    The records' closed forms are sums and products of rationals and square roots, nested
    at most twice. A square root is bounded by integer square roots at `places` decimals,
    rounded outward, so the enclosure is a proof rather than an estimate.
    """
    if expression.is_Rational:
        numerator, denominator = sp.fraction(expression)
        value = Fraction(int(numerator), int(denominator))
        return value, value
    arguments = cast("tuple[sp.Expr, ...]", expression.args)
    if expression.is_Add:
        bounds = [enclose(term, places) for term in arguments]
        return sum((low for low, _ in bounds), Fraction(0)), sum(
            (high for _, high in bounds), Fraction(0)
        )
    if expression.is_Mul:
        low = high = Fraction(1)
        for factor in arguments:
            factor_low, factor_high = enclose(factor, places)
            products = (
                low * factor_low,
                low * factor_high,
                high * factor_low,
                high * factor_high,
            )
            low, high = min(products), max(products)
        return low, high
    if expression.is_Pow and arguments[1] == sp.Rational(1, 2):
        base_low, base_high = enclose(arguments[0], places)
        if base_low < 0:
            raise ExactValuesError(f"a square root of a possibly negative {arguments[0]}")
        scale = 10**places
        low_square = base_low * scale**2
        high_square = base_high * scale**2
        low_root = isqrt(low_square.numerator // low_square.denominator)
        high_root = isqrt(-(-high_square.numerator // high_square.denominator)) + 1
        return Fraction(low_root, scale), Fraction(high_root, scale)
    raise ExactValuesError(
        f"a closed form outside sums, products and square roots: {expression}"
    )


def check_closed_form_is_the_root(n: int, exact_form: str, root: Root) -> None:
    """The closed form names the isolated root, not another root of its polynomial.

    The polynomial is the closed form's minimal polynomial, so the closed form is one of
    its roots, and the isolated root is the only one in its cell. An exact enclosure of
    the closed form strictly inside that cell therefore identifies the two; one disjoint
    from it refuses. An enclosure straddling a cell end is refined before either.
    """
    derived = derive_from_exact_form(exact_form)
    if derived.coefficients != root.coefficients:
        raise ExactValuesError(f"n = {n}: {exact_form} is not the recorded root")
    value = parse_form(exact_form)
    for places in (60, 120, 240):
        low, high = enclose(value, places)
        if root.exact is not None:
            if low == high == root.exact:
                return
            raise ExactValuesError(f"n = {n}: {exact_form} is not the recorded root")
        if root.lo < low and high < root.hi:
            return
        if high <= root.lo or low >= root.hi:
            break
    raise ExactValuesError(f"n = {n}: {exact_form} is not the isolated root")


def polynomial_checks(
    n: int,
    coefficients: tuple[int, ...],
    record_value: str,
    kkt: dict | None,
    budget: int = PRIME_BUDGET,
    *,
    upward_ceiling: bool = False,
    certificate_primes: Sequence[int] | None = None,
) -> tuple[dict, Root]:
    """Rebuild every check; retained prime hints choose work, never supply a verdict."""
    if certificate_primes is None:
        certificate = irreducibility(coefficients, budget)
    else:
        if not certificate_primes or len(certificate_primes) > budget:
            raise ExactValuesError(f"n = {n}: empty or over-budget SVG prime hints")
        if not all(sp.isprime(prime) for prime in certificate_primes):
            raise ExactValuesError(f"n = {n}: SVG prime hints include a composite")
        if not verify_modular_certificate(coefficients, certificate_primes):
            raise ExactValuesError(f"n = {n}: SVG prime hints do not prove irreducibility")
        certificate = {"method": "modular-degree-patterns", "primes": list(certificate_primes)}
    kkt_value = None if kkt is None else kkt["value"]
    root, window = isolate_root(coefficients, record_value, kkt_value)
    inside = contains_recorded_side(root, record_value, upward_ceiling=upward_ceiling)
    if not inside:
        raise ExactValuesError(
            f"n = {n}: the root of {format_polynomial(coefficients)[:60]} near the side is "
            f"{root_decimal(root, 25)}, which the recorded {record_value} does not truncate "
            "or round to: a wrong polynomial"
        )
    checks = {
        "irreducible": certificate,
        "root": {
            "interval": [
                f"{root.lo.numerator}/{root.lo.denominator}",
                f"{root.hi.numerator}/{root.hi.denominator}",
            ],
            "unique": True,
            "contains_recorded_side": inside,
            "window": window,
        },
        "decimal": root_decimal(root),
        "kkt_agreement_digits": (
            None if kkt_value is None else agreement_digits(root, kkt_value, KKT_DIGITS)
        ),
        "recorded_agreement_digits": agreement_digits(
            root, record_value, _significant_digits(record_value)
        ),
    }
    return checks, root


class VerifiedRationalInputs:
    """Proof inputs reused within one build, never across mathematical invocations."""

    def __init__(self) -> None:
        self.evidence: dict[str, dict] | None = None
        self.native_rows: dict[int, dict] | None = None
        self.source_rows: dict[int, dict] = {}
        self.packet_validated = False
        self.refinements_validated = False
        self.arrangements: arrangement_houses.VerifiedInputs | None = None
        self.imported: dict[str, dict[int, dict]] = {}
        self.source_facts: dict[str, dict[int, evand.Certificate]] = {}

    def evidence_row(self, n: int, identifier: str, source_key: str) -> dict:
        if self.evidence is None:
            record = safe_load((FRONTIER / "evidence.yaml").read_text(encoding="utf-8"))
            self.evidence = {row["id"]: row for row in record["evidence"]}
        row = self.evidence[identifier]
        if (
            row.get("claim") != "upper-bound"
            or row.get("assurance") != "verified"
            or row.get("method") != "exact-algebraic"
            or row.get("replay_status") != "passed"
            or row.get("source_key") != source_key
            or n not in row.get("scope", {}).get("n_values", [])
            or not row.get("certificate")
            or not row.get("replay")
        ):
            raise ValueError("the upper-bound evidence does not certify this source/count")
        return row

    def native_side(self, n: int) -> Fraction:
        if self.native_rows is None:
            problems = evand.receipt_problems()
            if problems:
                raise ValueError("; ".join(problems))
            first = json.loads(read_retained_text(evand.FIRST_PARTY_RECEIPT))
            source = json.loads(read_retained_text(evand.SOURCE_REPLAY_RECEIPT))
            expected = f"{evand.SOURCE}/tree/{evand.REVISION}/"
            if (
                first.get("format") != evand.FORMAT
                or first.get("source") != expected + evand.UPSTREAM_CERTS
                or source.get("format") != evand.FORMAT
                or source.get("source") != expected + "s12/search/exact"
            ):
                raise ValueError("native replay receipts name a different source")
            self.native_rows = {int(row["n"]): row for row in first["rows"]}
            self.source_rows = {int(row["n"]): row for row in source["rows"]}
        row = self.native_rows[n]
        source_row = self.source_rows[n]
        source_passed = all(
            source_row[name]["exit_status"] == 0
            and source_row[name]["last_line"].startswith(prefix)
            for name, prefix in (("verify_cert", "VALID: s(n) <="), ("verify_cert2", "VALID:"))
        )
        if (
            not row["exact_verify"]["passed"]
            or not row["independent"]["passed"]
            or not source_passed
        ):
            raise ValueError("the native certificate's replay did not pass")
        certificate = evand.parse(
            evand.certificate_path(evand.CERTS, n).read_text(encoding="utf-8"), expected_n=n
        )
        if certificate.side != Fraction(row["side"]):
            raise ValueError("native certificate side differs from its replay")
        return certificate.side

    def packet_ceiling(self, n: int, rational: Fraction) -> None:
        source = upper_bound_packets.FRANCISCOUZO
        if upper_bound_packets.acquisition(source)["source_commit"] != source.revision:
            raise ValueError("the ceiling packet names a different source revision")
        if not self.packet_validated:
            problems = upper_bound_packets.fast_problems(source)
            if problems:
                raise ValueError("; ".join(problems))
            self.packet_validated = True
        row = upper_bound_packets.certification(source)[n]
        witness = safe_load(
            gzip.decompress(source.certificate(n).read_bytes()).decode("utf-8")
        )["witness"]
        if witness["n"] != n or row["n"] != n or row["promotion"] != "certificate-produced":
            raise ValueError("the ceiling certificate/receipt names a different count")
        side = Fraction(witness["side"])
        printed = upper_bound_packets.cases(source)[n]["side"]
        derived = upper_bound_packets.derived(printed, side)
        if (
            side > rational
            or Fraction(derived["exact_form"]) != rational
            or Fraction(derived["verified_value"]) != rational
        ):
            raise ValueError("the registered fraction is not the certified outward ceiling")

    def refinement_provenance(
        self, n: int, rational: Fraction, source: refinement_packets.Source, replay: str
    ) -> dict:
        evidence = self.evidence_row(n, replay, source.key)
        certificate = refinement_packets.fact_path(source, n)
        if (ROOT.parent / evidence["certificate"]).resolve() != certificate.parent.resolve():
            raise ValueError("the evidence names a different refinement fact directory")
        fact = refinement_packets.read_fact(source, n)
        if rational != refinement_packets.rational(fact["side"]):
            raise ValueError(
                "the registered fraction differs from the admitted refinement side"
            )
        if not self.refinements_validated:
            refinement_custody.check_index(refinement_custody.read_index())
            self.refinements_validated = True
        refinement_house_links.check_houses([n])
        return _note(
            "verified-witness-side",
            f"This is the verified finite rational refinement witness side, from {source.key}; "
            f"certificate {certificate.relative_to(ROOT.parent)}, replay {replay}, receipt "
            f"{refinement_custody.INDEX.relative_to(ROOT.parent)}. "
            "Its degree-one identity establishes neither stationarity nor global optimality.",
            degree=1,
        )

    def arrangement_provenance(self, n: int, rational: Fraction) -> dict:
        evidence = self.evidence_row(
            n, arrangement_reports.EXACT_EVIDENCE, arrangement_reports.SOURCE_KEY
        )
        receipt = arrangement_reports.receipt_path()
        if evidence["certificate"] != receipt.relative_to(ROOT.parent).as_posix():
            raise ValueError("the evidence names a different #399 receipt file")
        if self.arrangements is None:
            self.arrangements = arrangement_houses.VerifiedInputs()
        certificate = self.arrangements.facts[n]
        if certificate.side != rational:
            raise ValueError("the registered fraction differs from the complete #399 side")
        arrangement_houses.check_houses([n], verified_inputs=self.arrangements)
        return _note(
            "verified-witness-side",
            f"This is the complete finite rational #399 witness side, from "
            f"{arrangement_reports.SOURCE_KEY}; source facts "
            f"{arrangement_reports.fact_path().relative_to(ROOT.parent)}, passing replay "
            f"{arrangement_reports.EXACT_EVIDENCE}, receipt "
            f"{receipt.relative_to(ROOT.parent)}. The verified display is its least upward "
            "sixteen-place ceiling; the linear identity names the native side. "
            "It establishes neither stationarity nor global optimality.",
            degree=1,
        )

    def imported_source(self, source_key: str) -> dict[int, dict]:
        """Bind complete current houses to retained native jobs once per build."""
        if source_key not in self.imported:
            if source_key == ryxu_houses.SOURCE_KEY:
                self.source_facts[source_key] = ryxu_houses.reports.read_facts()
                self.imported[source_key] = ryxu_houses.check_houses()
            elif source_key == gupta_houses.reports.SOURCE_KEY:
                self.source_facts[source_key] = gupta_houses.reports.read_facts()
                gupta_houses.check_houses()
                self.imported[source_key] = {n: {} for n in gupta_houses.NUMBERS}
            else:
                raise ValueError("unsupported imported finite source")
        return self.imported[source_key]

    def provenance(self, n: int, rational: Fraction, replay: str, source_key: str) -> dict:
        evidence = self.evidence_row(n, replay, source_key)
        if source_key == KKT_KEY:
            if (ROOT / evidence["certificate"]).resolve() != evand.CERTS.resolve():
                raise ValueError("the evidence names a different native certificate directory")
            if self.native_side(n) != rational:
                raise ValueError("the registered fraction differs from the native witness side")
            kind = "verified-witness-side"
            certificate = evand.certificate_path(evand.CERTS, n)
            receipt = evand.FIRST_PARTY_RECEIPT
            text = "This is the verified native rational witness side"
        else:
            source = upper_bound_packets.FRANCISCOUZO
            if (ROOT / evidence["certificate"]).resolve() != source.certificate(
                n
            ).parent.resolve():
                raise ValueError("the evidence names a different ceiling certificate directory")
            self.packet_ceiling(n, rational)
            kind = "verified-bound-ceiling"
            certificate = source.certificate(n)
            receipt = source.certification
            text = "This is a certified outward ceiling, not the native witness side"
        return _note(
            kind,
            f"{text}, from {source_key}; certificate {certificate.relative_to(ROOT)}, "
            f"replay {replay}, receipt {receipt.relative_to(ROOT)}. "
            "Its degree-one identity establishes neither stationarity nor global optimality.",
            degree=1,
        )


def _verified_rational_fallback(
    n: int, packing: dict, inputs: VerifiedRationalInputs
) -> tuple[Fraction, dict] | None:
    reported = packing["reported_upper_bound"]
    verified = packing.get("verified_upper_bound", {})
    source_key = reported.get("source_key")
    replays = {
        KKT_KEY: "E-evand-exact-optima-2026-10-05-exact-replay",
        upper_bound_packets.FRANCISCOUZO.key: "E-franciscouzo-2026-09-27-exact-replay",
    }
    replay = replays.get(source_key)
    if (
        packing.get("n") != n
        or packing.get("status") != "open"
        or any(
            reported.get(key) is not None
            for key in (
                "exact_form",
                "algebraic_degree",
                "minimal_polynomial",
                "algebraic_source",
            )
        )
        or replay is None
        or replay not in verified.get("evidence", [])
    ):
        return None
    try:
        rational = Fraction(str(verified.get("exact_form")))
        if rational != Fraction(str(reported["value"])) or rational != Fraction(
            str(verified["value"])
        ):
            return None
    except ValueError, ZeroDivisionError, KeyError:
        return None
    try:
        note = inputs.provenance(n, rational, replay, source_key)
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise ExactValuesError(f"n = {n}: verified rational bound refused: {error}") from error
    return rational, note


def _explicit_refinement_rational(
    n: int, packing: dict, inputs: VerifiedRationalInputs
) -> tuple[Fraction, dict] | None:
    """Admit only a current finite rational refinement and its retained geometry."""
    reported = packing["reported_upper_bound"]
    verified = packing.get("verified_upper_bound", {})
    source = next(
        (
            source
            for source in refinement_packets.SOURCES.values()
            if reported.get("source_key") == source.key
        ),
        None,
    )
    if source is None:
        return None

    def unavailable() -> None:
        if reported.get("minimal_polynomial") is not None:
            raise ExactValuesError(
                f"n = {n}: refinement rational bound refused: supplied polynomial "
                "requires matching current rational metadata and derived-from-exact-form origin"
            )

    replay = f"E-{source.packet_name}-exact-replay"
    if (
        n not in source.numbers
        or packing.get("n") != n
        or packing.get("status") != "open"
        or type(reported.get("algebraic_degree")) is not int
        or reported["algebraic_degree"] != 1
        or (
            reported.get("algebraic_source")
            != (None if reported.get("minimal_polynomial") is None else DERIVED_FROM_EXACT_FORM)
        )
        or replay not in verified.get("evidence", [])
    ):
        return unavailable()
    try:
        rational = refinement_packets.rational(reported.get("exact_form"))
        if rational != refinement_packets.rational(verified.get("exact_form")) or any(
            rational != Fraction(str(bound["value"])) for bound in (reported, verified)
        ):
            return unavailable()
    except ValueError, ZeroDivisionError, KeyError:
        return unavailable()
    try:
        note = inputs.refinement_provenance(n, rational, source, replay)
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise ExactValuesError(
            f"n = {n}: refinement rational bound refused: {error}"
        ) from error
    return rational, note


def _explicit_arrangement_rational(
    n: int, packing: dict, inputs: VerifiedRationalInputs
) -> tuple[Fraction, dict] | None:
    """Bind #399's native side separately from its upward verified display."""
    reported = packing["reported_upper_bound"]
    if reported.get("source_key") != arrangement_reports.SOURCE_KEY:
        return None
    verified = packing.get("verified_upper_bound", {})
    supplied = reported.get("minimal_polynomial") is not None
    if (
        n not in arrangement_reports.NUMBERS
        or packing.get("n") != n
        or packing.get("status") != "open"
        or type(reported.get("algebraic_degree")) is not int
        or reported["algebraic_degree"] != 1
        or reported.get("algebraic_source") != (DERIVED_FROM_EXACT_FORM if supplied else None)
        or arrangement_reports.EXACT_EVIDENCE not in verified.get("evidence", [])
    ):
        raise ExactValuesError(
            f"n = {n}: arrangement rational bound refused: matching current finite "
            "metadata and supported derived polynomial origin required"
        )

    def native_fraction() -> Fraction:
        rational = refinement_packets.rational(reported.get("exact_form"))
        if (
            rational != refinement_packets.rational(verified.get("exact_form"))
            or rational != Fraction(str(reported["value"]))
            or verified.get("value") != evand.ceiling_decimal(rational, 16)
        ):
            raise ValueError("native fraction or least upward sixteen-place display differs")
        return rational

    try:
        rational = native_fraction()
        note = inputs.arrangement_provenance(n, rational)
    except (OSError, ValueError, KeyError, TypeError, ZeroDivisionError) as error:
        raise ExactValuesError(
            f"n = {n}: arrangement rational bound refused: {error}"
        ) from error
    return rational, note


def _explicit_imported_exact(
    n: int, packing: dict, inputs: VerifiedRationalInputs
) -> tuple[dict, dict] | None:
    """Admit the native finite identity separately from its least upward display."""
    reported = packing["reported_upper_bound"]
    source_key = reported.get("source_key")
    if source_key not in {ryxu_houses.SOURCE_KEY, gupta_houses.reports.SOURCE_KEY}:
        return None

    def admit() -> tuple[dict, dict]:
        numbers = (
            ryxu_houses.NUMBERS
            if source_key == ryxu_houses.SOURCE_KEY
            else gupta_houses.NUMBERS
        )
        if packing.get("n") != n or packing.get("status") != "open" or n not in numbers:
            raise ValueError("source/count does not name a selected open house")
        radical = source_key == ryxu_houses.SOURCE_KEY and n == 51
        reports = (
            ryxu_houses.reports
            if source_key == ryxu_houses.SOURCE_KEY
            else gupta_houses.reports
        )
        certificate = ryxu_houses.radical.fact_path() if radical else reports.fact_path()
        replay = "E-ryxu-432-radical-n51-feasibility" if radical else reports.EXACT_EVIDENCE
        evidence = inputs.evidence_row(n, replay, source_key)
        if evidence["certificate"] != certificate.relative_to(ROOT.parent).as_posix():
            raise ValueError("evidence names a different complete source certificate")
        if radical:
            native = ryxu_houses.RADICAL_EXACT
            display = ryxu_houses.radical_display()
            receipt = reports.receipt_path().parent / "n051-radical-positive.json.xz"
        else:
            if source_key not in inputs.source_facts:
                inputs.source_facts[source_key] = reports.read_facts()
            native = str(inputs.source_facts[source_key][n].side)
            display = evand.ceiling_decimal(Fraction(native), 16)
            receipt = reports.receipt_path()
        fields = algebraic_fields(native, None, None)
        verified = packing.get("verified_upper_bound", {})
        if (
            type(reported.get("algebraic_degree")) is not int
            or reported["algebraic_degree"] != fields["algebraic_degree"]
            or reported.get("algebraic_source") not in {None, DERIVED_FROM_EXACT_FORM}
            or replay not in verified.get("evidence", [])
            or reported.get("value") != display
            or verified.get("value") != display
            or parse_form(str(reported.get("exact_form"))) != parse_form(native)
            or parse_form(str(verified.get("exact_form"))) != parse_form(native)
        ):
            raise ValueError("current native form, degree, evidence or upward display differs")
        if (
            reported.get("minimal_polynomial") is not None
            and _normalized(str(reported["minimal_polynomial"]))
            != derive_from_exact_form(native).coefficients
        ):
            raise ValueError("supplied polynomial differs from the complete native side")
        inputs.imported_source(source_key)
        note = _note(
            "verified-witness-side",
            f"This is the complete finite {'Q(sqrt2)' if radical else 'rational'} "
            f"native witness side from {source_key}; source facts "
            f"{certificate.relative_to(ROOT.parent)}, replay {replay}, receipt "
            f"{receipt.relative_to(ROOT.parent)}. The display is the least upward "
            "sixteen-place ceiling; the algebraic identity names the native side. "
            "It establishes neither stationarity nor global optimality.",
            degree=2 if radical else 1,
        )
        return {**reported, **fields}, note

    try:
        admitted = admit()
    except (OSError, ValueError, KeyError, TypeError, ZeroDivisionError) as error:
        raise ExactValuesError(f"n = {n}: imported exact bound refused: {error}") from error

    return admitted


def _arrangement_notes(n: int) -> list[dict]:
    bead = ROUTES.get(n, (SWEEP_BEAD, ""))[0]
    return [
        _note(
            "route",
            "The finite rational bound leaves ideal contact research open. Establish the "
            "new #399 witness's active contact system and a stable seed before ideal-side "
            "identification. No KKT or local-minimum result from the earlier 13ee36e5 pose "
            "transfers to this geometry.",
            bead=bead,
        )
    ]


def _certified_rational_ceiling(packing: dict, coefficients: tuple[int, ...]) -> bool:
    """Only a replay-backed rational upper bound may use an upward display ceiling."""
    reported = packing["reported_upper_bound"]
    verified = packing.get("verified_upper_bound", {})
    replay = CERTIFIED_CEILING_SOURCES.get(reported.get("source_key"))
    if (
        len(coefficients) != 2
        or packing["status"] == "proved"
        or replay is None
        or replay not in verified.get("evidence", [])
        or verified.get("value") != reported["value"]
        or verified.get("exact_form") != reported.get("exact_form")
        or reported.get("exact_form") is None
    ):
        return False
    try:
        rational = Fraction(str(reported["exact_form"]))
    except ValueError:
        return False
    return rational == Fraction(-coefficients[1], coefficients[0])


def build_entry(
    n: int,
    packing: dict,
    entry: CatalogueEntry | None,
    kkt_row: dict | None,
    budget: int = PRIME_BUDGET,
    *,
    verified_inputs: VerifiedRationalInputs | None = None,
) -> dict:
    """One register entry from one record, its catalogue block and its KKT row."""
    reported = packing["reported_upper_bound"]
    inputs = verified_inputs or VerifiedRationalInputs()
    imported = _explicit_imported_exact(n, packing, inputs)
    fallback = _verified_rational_fallback(n, packing, inputs)
    refinement = _explicit_refinement_rational(n, packing, inputs)
    arrangement = _explicit_arrangement_rational(n, packing, inputs)
    admitted = next(
        (item for item in (fallback, refinement, arrangement) if item is not None), None
    )
    projection = admitted if reported.get("minimal_polynomial") is None else None
    if projection is not None:
        rational, _provenance = projection
        reported = {
            **reported,
            "exact_form": f"{rational.numerator}/{rational.denominator}",
            "algebraic_degree": 1,
            "minimal_polynomial": format_polynomial(
                (rational.denominator, -rational.numerator)
            ),
            "algebraic_source": DERIVED_FROM_EXACT_FORM,
        }
    if imported is not None:
        reported = imported[0]
    status = str(packing["status"])
    value = str(reported["value"])
    exact_form = reported.get("exact_form")
    exact_form = None if exact_form is None else str(exact_form)
    recorded_degree = reported.get("algebraic_degree")
    degree = None if recorded_degree is None else int(recorded_degree)
    polynomial_text = reported.get("minimal_polynomial")
    polynomial_text = None if polynomial_text is None else str(polynomial_text)

    kkt = None
    if kkt_row is not None and kkt_row.get("S_exact"):
        kkt = {"value": str(kkt_row["S_exact"]), "status": str(kkt_row["status"])}

    notes: list[dict] = [] if admitted is None else [admitted[1]]
    if imported is not None:
        notes.append(imported[1])
    checks: dict[str, Any] = {
        "irreducible": None,
        "root": None,
        "decimal": None,
        "kkt_agreement_digits": None,
        "recorded_agreement_digits": None,
        "catalogue": None,
        "galois": None,
    }
    polynomial = None
    if polynomial_text is not None:
        coefficients = _normalized(polynomial_text)
        if degree is not None and degree != len(coefficients) - 1:
            raise ExactValuesError(
                f"n = {n}: algebraic_degree {degree} but the polynomial has degree "
                f"{len(coefficients) - 1}"
            )
        degree = len(coefficients) - 1
        polynomial = _polynomial_record(coefficients)
        # The source first: a polynomial that is not the one its source gives is refused
        # as that, before its root is sought at all.
        agreement_with_source = source_check(n, reported, coefficients, entry)
        svg_fact = retained_svg_fact(n) if agreement_with_source == "matches-svg" else None
        hints = None if svg_fact is None else svg_fact["checks"][0]["irreducibility"]["primes"]
        numeric, root = polynomial_checks(
            n,
            coefficients,
            value,
            kkt,
            budget,
            certificate_primes=hints,
            upward_ceiling=(
                imported is not None or _certified_rational_ceiling(packing, coefficients)
            ),
        )
        if (
            agreement_with_source == "matches"
            and entry is not None
            and not contains_recorded_side(root, entry.side_decimal)
        ):
            raise ExactValuesError(f"n = {n}: the root differs from the catalogue side")
        if svg_fact is not None:
            sides = [item["value"] for item in svg_fact["entities"] if item["name"] == "s"]
            if len(sides) != 1 or not contains_recorded_side(root, sides[0]):
                raise ExactValuesError(f"n = {n}: the root differs from the retained SVG side")
            numeric["root"]["source_index"] = {
                "stated": next(
                    item for item in svg_fact["roots"] if item["assigned_to"] == "s"
                )["index"],
                "counted": None,
            }
        checks.update(numeric)
        checks["catalogue"] = agreement_with_source
        if exact_form is not None:
            check_closed_form_is_the_root(n, exact_form, root)
        checks["galois"] = _galois(coefficients)
        if checks["galois"] is not None and not checks["galois"]["solvable"]:
            group = checks["galois"]["group"]
            notes.append(
                _note(
                    "no-radical-form",
                    f"The Galois group is {group}, which is not solvable, so the side "
                    "has no expression in radicals.",
                    degree=degree,
                )
            )
        agreement = checks["kkt_agreement_digits"]
        if (
            kkt is not None
            and kkt["status"] == KKT_LOCAL_MIN
            and agreement is not None
            and agreement < KKT_AGREEMENT_FLOOR
        ):
            notes.append(
                _note(
                    "route",
                    f"The root agrees with Daniel's KKT value to {agreement} digits only, "
                    "so the two describe different points; the record's root stands.",
                    bead=SWEEP_BEAD,
                    degree=degree,
                )
            )
    elif exact_form is not None:
        raise ExactValuesError(f"n = {n}: a closed form with no minimal polynomial")

    state = _state(exact_form, degree, polynomial_text)
    if n in MISSING_POLYNOMIAL_TEXT and state == "degree-only":
        bead, text = MISSING_POLYNOMIAL_TEXT[n]
        notes.append(_note("missing-polynomial-text", text, bead=bead, degree=degree))
    superseded = _superseded_note(n, reported, entry, budget)
    if superseded is not None:
        notes.append(superseded)
    if state == "numeric-only" or admitted is not None or imported is not None:
        routes = (
            _arrangement_notes(n)
            if arrangement is not None
            else _numeric_only_notes(n, kkt_row)
        )
        for note in routes:
            if (admitted is not None or imported is not None) and arrangement is None:
                note["text"] = (
                    "The finite native bound leaves ideal contact research open. "
                    + note["text"]
                )
            same_route = next(
                (
                    old
                    for old in notes
                    if old["kind"] == note["kind"] and old["bead"] == note["bead"]
                ),
                None,
            )
            if same_route is None:
                notes.append(note)
            else:
                same_route["text"] += " " + note["text"]

    return {
        "n": n,
        "status": status,
        "side": {
            "value": value,
            "relation": "equality" if status == "proved" else "upper-bound",
        },
        "lower": {"value": str(packing["verified_lower_bound"]["value"])},
        "state": state,
        "exact_form": exact_form,
        "exact_form_latex": None if exact_form is None else exact_form_latex(exact_form),
        "algebraic_source": reported.get("algebraic_source"),
        "degree": degree,
        "polynomial": polynomial,
        "checks": checks,
        "kkt": kkt,
        "notes": notes,
    }


def _numeric_only_notes(n: int, kkt_row: dict | None) -> list[dict]:
    notes: list[dict] = []
    if n in ROUTES:
        bead, text = ROUTES[n]
        status = None if kkt_row is None else str(kkt_row["status"])
        if status != KKT_LOCAL_MIN:
            text += f" No confirmed KKT local minimum is retained (batch status {status!r})."
        notes.append(_note("route", text, bead=bead))
    else:
        status = None if kkt_row is None else str(kkt_row["status"])
        if status == KKT_LOCAL_MIN:
            text = (
                f"Daniel's batch holds a KKT local minimum to {KKT_DIGITS} digits; a "
                "high-precision re-solve with a bounded integer-relation search is the route."
            )
        else:
            text = (
                f"No exact KKT point is available yet: Daniel's batch reports {status!r} "
                "for this count."
            )
        notes.append(_note("route", text, bead=SWEEP_BEAD))
    if n in RELATION_NEGATIVES:
        bead, degree, text = RELATION_NEGATIVES[n]
        notes.append(_note("relation-search-negative", text, bead=bead, degree=degree))
    return notes


def _registered_root(entry: dict) -> Root:
    coefficients = tuple(int(c) for c in entry["polynomial"]["coefficients"])
    lo, hi = (Fraction(value) for value in entry["checks"]["root"]["interval"])
    return Root(coefficients, lo, hi, lo if lo == hi else None)


def _occurrence_sources(pair: dict) -> list[dict]:
    return [
        {**occurrence["source"], "source_flags": occurrence["source_flags"]}
        for occurrence in pair["occurrences"]
    ]


def reported_source_historical_entries(entries: list[dict]) -> list[dict]:
    """Project independently checked source notes without admitting a current packing."""
    rows = []
    for entry in entries:
        for note in entry["notes"]:
            if note["kind"] != "unreconciled-source-polynomial":
                continue
            current_side = str(entry["side"]["value"])
            if Fraction(note["checks"]["root"]["interval"][1]) >= Fraction(current_side):
                raise ExactValuesError(
                    f"n = {entry['n']}: unreconciled source root is not strictly below "
                    "the current recorded bound"
                )
            rows.append(
                {
                    **note,
                    "n": entry["n"],
                    "kind": "unreconciled-source",
                    "current_side": current_side,
                    "algebraic_source": "reported-source-polynomial",
                }
            )
    return rows


def _catalogue_occurrence(n: int, entry: CatalogueEntry, kind: str) -> dict:
    return {
        "path": f"packing/{CATALOGUE_MARKDOWN}",
        "url": "https://kingbird.myphotos.cc/packing/squares_in_squares.html",
        "kind": kind,
        "locator": {"line": entry.source_line, "section": str(n)},
        "source_flags": [],
    }


def source_closed_form_history(entry: dict, source: CatalogueEntry) -> dict | None:
    """Check a superseded catalogue expression at its own root, with derived provenance."""
    exact_form = source.exact_form
    side, current_side = source.side_decimal, str(entry["side"]["value"])
    if exact_form is None or Decimal(side) <= Decimal(current_side):
        return None
    facts = derive_from_exact_form(exact_form)
    if (
        entry["polynomial"] is not None
        and tuple(int(c) for c in entry["polynomial"]["coefficients"]) == facts.coefficients
        and contains_recorded_side(_registered_root(entry), side)
    ):
        return None
    checks, root = polynomial_checks(entry["n"], facts.coefficients, side, None)
    check_closed_form_is_the_root(entry["n"], exact_form, root)
    if root.compare(Fraction(Decimal(current_side))) <= 0:
        return None
    checks.update(catalogue="derived-here", galois=_galois(facts.coefficients))
    return {
        "n": entry["n"],
        "kind": "superseded",
        "current_side": current_side,
        "side": side,
        "exact_form": exact_form,
        "algebraic_source": DERIVED_FROM_SOURCE_CLOSED_FORM,
        "degree": facts.degree,
        "polynomial": _polynomial_record(facts.coefficients),
        "checks": checks,
        "sources": [_catalogue_occurrence(entry["n"], source, DERIVED_FROM_SOURCE_CLOSED_FORM)],
        "source_statuses": [],
        "attribution": {
            "date_mentions": [] if source.found_year is None else [str(source.found_year)],
            "source_text": [] if source.credit_line is None else [source.credit_line],
        },
        "bead": None,
    }


def append_source_closed_form_history(entries: list[dict], historical: list[dict]) -> None:
    """Keep omitted source expressions, merging citations only for the same exact root."""
    catalogue = catalogue_entries()
    for entry in entries:
        source = catalogue.get(entry["n"])
        if source is None:
            continue
        derived = source_closed_form_history(entry, source)
        if derived is None:
            continue
        matches = [
            row
            for row in historical
            if row["n"] == entry["n"]
            and row["polynomial"]["coefficients"] == derived["polynomial"]["coefficients"]
            and contains_recorded_side(_registered_root(row), derived["side"])
        ]
        if not matches:
            historical.append(derived)
            continue
        row = matches[0]
        row["exact_form"] = derived["exact_form"]
        for citation in derived["sources"]:
            if citation not in row["sources"]:
                row["sources"].append(citation)


def build_historical_entries(entries: list[dict]) -> list[dict]:
    """Recheck printed equations and retained closed forms at each source's own side.

    Source equations can be correct even when their proposed geometry is invalid. These
    entries never change the current side, status or bound. The source flags and exact
    algebraic certificates travel separately and every coefficient is retained.
    """
    # The collector calls this module's arithmetic only after decoding the sources.
    from devtools.collect_kingbird_historical_polynomials import (  # noqa: PLC0415 -- cycle
        verify_source_identity,
    )

    document = json.loads((ROOT / HISTORICAL_FACTS).read_text(encoding="utf-8"))
    verify_source_identity(document)
    if document["unparsed_rows"]:
        raise ExactValuesError("historical source inventory has unparsed equation rows")
    current = {entry["n"]: entry for entry in entries}
    historical: list[dict] = []
    for pair in document["entries"]:
        n, side = int(pair["n"]), str(pair["historical_side"])
        coefficients = tuple(int(c) for c in pair["coefficients"])
        for occurrence in pair["occurrences"]:
            if _normalized(occurrence["printed_equation"]) != coefficients:
                raise ExactValuesError(
                    f"n = {n}: historical coefficients differ from the source equation"
                )
        sources = _occurrence_sources(pair)
        entry = current.get(n)
        if (
            entry is not None
            and entry["polynomial"] is not None
            and tuple(int(c) for c in entry["polynomial"]["coefficients"]) == coefficients
            and contains_recorded_side(_registered_root(entry), side)
        ):
            entry.setdefault("source_occurrences", []).extend(sources)
            continue
        checks, _ = polynomial_checks(n, coefficients, side, None)
        checks.update(catalogue="matches", galois=_galois(coefficients))
        current_side = None if entry is None else str(entry["side"]["value"])
        if "invalid" in pair["source_statuses"] and "fixed" not in pair["source_statuses"]:
            kind = "source-invalid"
        elif entry is None:
            kind = "outside-frontier"
        elif current_side is not None and Decimal(side) > Decimal(current_side):
            kind = "superseded"
        else:
            kind = "unreconciled-source"
        historical.append(
            {
                "n": n,
                "kind": kind,
                "algebraic_source": CATALOGUE,
                "current_side": current_side,
                "side": side,
                "degree": len(coefficients) - 1,
                "polynomial": _polynomial_record(coefficients),
                "checks": checks,
                "sources": sources,
                "source_statuses": pair["source_statuses"],
                "attribution": pair["attribution"],
                "bead": "think-492g" if kind == "unreconciled-source" else None,
            }
        )
    # The main catalogue's older rows remain even if a comparison page omits one. Merge
    # an exact same root's citations instead of printing that polynomial twice.
    for entry in entries:
        for note in entry["notes"]:
            if note["kind"] != "superseded-catalogue-polynomial":
                continue
            matches = [
                row
                for row in historical
                if row["n"] == entry["n"]
                and row["polynomial"]["coefficients"] == note["polynomial"]["coefficients"]
                and contains_recorded_side(_registered_root(row), note["side"])
            ]
            catalogue_entry = catalogue_entries()[entry["n"]]
            source = _catalogue_occurrence(entry["n"], catalogue_entry, "current-catalogue")
            if matches:
                matches[0]["sources"].append(source)
            else:
                historical.append(
                    {
                        "n": entry["n"],
                        "kind": "superseded",
                        "algebraic_source": CATALOGUE,
                        "current_side": entry["side"]["value"],
                        "side": note["side"],
                        "degree": note["degree"],
                        "polynomial": note["polynomial"],
                        "checks": note["checks"],
                        "sources": [source],
                        "source_statuses": [],
                        "attribution": {"date_mentions": [], "source_text": []},
                        "bead": None,
                    }
                )
    append_source_closed_form_history(entries, historical)
    historical.extend(reported_source_historical_entries(entries))
    return sorted(historical, key=lambda row: (row["n"], Decimal(row["side"]), row["kind"]))


# --- the register -----------------------------------------------------------------------


def _totals(entries: list[dict]) -> dict:
    totals = {state: sum(1 for e in entries if e["state"] == state) for state in STATES}
    totals["proved"] = sum(1 for e in entries if e["status"] == "proved")
    totals["irreducible-certified"] = sum(
        1 for e in entries if e["checks"]["irreducible"] is not None
    )
    totals["root-isolated"] = sum(1 for e in entries if e["checks"]["root"] is not None)
    return totals


def _standing_interval(entry: dict) -> tuple[Fraction, Fraction]:
    root = entry.get("checks", {}).get("root")
    if root is not None:
        lo, hi = root["interval"]
        return Fraction(lo), Fraction(hi)
    if entry.get("exact_form") is not None:
        return enclose(parse_form(entry["exact_form"]), GRID_PLACES)
    value = Fraction(entry["side"]["value"])
    return value, value


def _source_disposition(lo: Fraction, hi: Fraction, current: dict) -> str:
    """Compare isolated native identities; displayed ceilings do not decide standing."""
    current_lo, current_hi = _standing_interval(current)
    if lo == hi == current_lo == current_hi:
        return "current-equal"
    if hi < current_lo:
        return "unreconciled-source"
    if lo > current_hi:
        return "superseded"
    raise ExactValuesError(f"n = {current['n']}: source and standing root cells overlap")


def append_reported_source_notes(entries: list[dict]) -> list[dict]:
    """Keep improving source-only notes and move beaten source roots into history."""
    indexed = {entry["n"]: entry for entry in entries}
    historical = []
    for candidate in reported_roots.collect():
        current = indexed[candidate["n"]]
        lo, hi = (Fraction(value) for value in candidate["checks"]["root"]["interval"])
        disposition = _source_disposition(lo, hi, current)
        text = (
            "This independently checked source-only polynomial root lies below "
            "the current recorded bound. Source-reported feasibility remains "
            "V0/C0; binding to a complete new geometry and Lean replay are not "
            "attempted. It is not admitted as this current packing's side or "
            "as an upper bound."
            if disposition == "unreconciled-source"
            else "This independently checked source-only polynomial root is superseded "
            "by the current recorded construction. Its source-reported feasibility "
            "remains V0/C0; geometry and Lean replay are not attempted. It establishes "
            "no current packing bound, current-pose identity or global optimum."
        )
        if disposition == "unreconciled-source":
            current["notes"].append(
                {
                    **{key: value for key, value in candidate.items() if key != "n"},
                    "kind": "unreconciled-source-polynomial",
                    "text": text,
                }
            )
        else:
            historical.append(
                {
                    **candidate,
                    "kind": disposition,
                    "text": text,
                    "current_side": current["side"]["value"],
                    "algebraic_source": "reported-source-polynomial",
                }
            )
    return historical


def _finite_source_history_row(
    n: int,
    side: Fraction,
    current: dict,
    *,
    result: str,
    source_key: str,
    revision: str,
    facts: Path,
    original: str,
    url: str,
    receipt: Path | None,
    confirmed: bool,
    source_date: str = "2026-10-08",
) -> dict | None:
    disposition = _source_disposition(side, side, current)
    if disposition == "current-equal":
        return None
    coefficients = (side.denominator, -side.numerator)
    decimal = evand.terminating_decimal(side)
    if decimal is None:
        raise ExactValuesError("retained finite source side does not terminate")
    checks, _root = polynomial_checks(n, coefficients, decimal, None)
    checks.update(catalogue="not-in-catalogue", galois=None)
    pending = disposition == "unreconciled-source"
    replayed = receipt is not None
    assurance = {
        "result": result,
        "source_key": source_key,
        "revision": revision,
        "facts": facts.relative_to(ROOT.parent).as_posix(),
        "original_certificate": original,
        "receipt": None if receipt is None else receipt.relative_to(ROOT.parent).as_posix(),
        "verification": "V3" if confirmed else "V0",
        "confirmation": "C3" if confirmed else "C0",
        "algebraic_identity": "independently-checked",
        "geometry_replay": "native-replay-retained" if replayed else "not-replayed",
        "adoption": "pending" if pending else "not-selected",
        "global_optimality": "not-established",
    }
    return {
        "n": n,
        "kind": disposition,
        "algebraic_source": "derived-from-source-closed-form",
        "current_side": current["side"]["value"],
        "side": root_decimal(_root),
        "exact_form": str(side),
        "degree": 1,
        "polynomial": {
            "coefficients": [str(c) for c in coefficients],
            "text": format_polynomial(coefficients),
            "latex": polynomial_latex(coefficients),
            "height_digits": len(str(max(abs(c) for c in coefficients))),
        },
        "checks": checks,
        "sources": [
            {
                "path": facts.relative_to(ROOT.parent).as_posix(),
                "url": url,
                "kind": "derived-from-source-closed-form",
                "locator": {"line": 1, "section": str(n)},
                "source_flags": [f"source certificate; {result}"],
            }
        ],
        "source_statuses": [
            "pending-adoption" if pending else "superseded",
            "scoped-finite-feasibility-confirmed" if confirmed else "source-reported",
            "native-replay-retained" if replayed else "geometry-not-replayed",
        ],
        "attribution": {
            "date_mentions": [source_date],
            "source_text": [f"{source_key}; {result}; original {original}"],
        },
        "bead": None,
        "source_certificate": assurance,
        "text": (
            "The exact linear identity names this finite source certificate's native "
            "side. "
            + (
                "This improving offer is pending adoption and establishes no current bound. "
                if pending
                else "This source construction is superseded by the standing bound. "
            )
            + (
                "Complete native replay is retained; "
                if replayed
                else "Geometry has not been replayed; "
            )
            + (
                "scoped V3/C3 finite feasibility is preserved. "
                if confirmed
                else "the imported claim remains V0/C0. "
            )
            + "No stationarity, local-minimum, rigidity or global-optimality claim transfers."
        ),
    }


def hunt_equal_bound_occurrence(
    current: dict,
    previous: dict | None,
    certificate: evand.Certificate,
    comparison: dict,
) -> dict | None:
    """Retain Daniel's scoped T-128 evidence without replacing Couzo's custody."""
    try:
        same_side = Fraction(comparison["exact_side"]) == certificate.side
    except (KeyError, TypeError, ValueError) as error:
        raise ExactValuesError(
            "record-hunt equal-bound comparison lacks an exact side"
        ) from error
    if (
        certificate.n != 155
        or comparison.get("result") != "T-128"
        or comparison.get("source_key") != couzo_refinements.SOURCE_KEY
        or not same_side
    ):
        raise ExactValuesError("record-hunt equal-bound comparison does not name Couzo's T-128")
    original = couzo_refinements.source_pins()[155]["certificate"]["path"]
    expected = _finite_source_history_row(
        155,
        certificate.side,
        current,
        result="T-128",
        source_key=couzo_refinements.SOURCE_KEY,
        revision=couzo_refinements.REVISION,
        facts=couzo_refinements.fact_path(),
        original=original,
        url=f"{couzo_refinements.SOURCE}/blob/{couzo_refinements.REVISION}/{original}",
        receipt=couzo_refinements.receipt_path(),
        confirmed=False,
    )
    if previous != expected:
        raise ExactValuesError(
            "record-hunt equal-bound occurrence differs from retained Couzo custody"
        )
    if expected is None:
        return None
    original = hunt_reports.certificate_path(155)
    occurrence = _finite_source_history_row(
        155,
        certificate.side,
        current,
        result="T-128",
        source_key=hunt_reports.SOURCE_KEY,
        revision=hunt_reports.REVISION,
        facts=hunt_reports.PACKET / "source" / original,
        original=original,
        url=f"{hunt_reports.SOURCE}/blob/{hunt_reports.REVISION}/{original}",
        receipt=hunt_reports.receipt_path(),
        confirmed=False,
        source_date=hunt_reports.READ_ON,
    )
    assert occurrence is not None
    occurrence["text"] = (
        "This separately retained Daniel certificate is an equal-bound evidence update "
        "to T-128. "
        + occurrence["text"]
        + " Equality of the certificate sides does not establish a connecting motion "
        "or equivalence of local minima."
    )
    return occurrence


def source_certificate_history(
    entries: list[dict], *, verified_inputs: VerifiedRationalInputs | None = None
) -> list[dict]:
    """Project noncurrent exact source certificates without adopting their bounds."""
    indexed = {entry["n"]: entry for entry in entries}
    inputs = verified_inputs or VerifiedRationalInputs()
    rows: dict[tuple[int, Fraction], dict] = {}

    def add(n: int, side: Fraction, **metadata: Any) -> None:
        row = _finite_source_history_row(n, side, indexed[n], **metadata)
        if row is None:
            return
        identity = n, side
        if identity in rows:
            # One identity may have several independently retained source occurrences.
            previous = rows[identity]
            if previous["source_certificate"] != row["source_certificate"]:
                raise ExactValuesError(
                    "duplicate finite identity has distinct custody/assurance"
                )
            previous["sources"].extend(row["sources"])
        else:
            rows[identity] = row

    confirmed_sources = (
        (
            ryxu_houses.reports,
            ryxu_houses.SOURCE_KEY,
            "T-125",
            {n: ryxu_houses.reports.source_path(n) for n in ryxu_houses.reports.NUMBERS},
        ),
        (
            gupta_houses.reports,
            gupta_houses.reports.SOURCE_KEY,
            "T-127",
            {n: pin["certificate"] for n, pin in gupta_houses.reports.source_pins().items()},
        ),
    )
    for reports, key, result, originals in confirmed_sources:
        if key not in inputs.source_facts:
            inputs.source_facts[key] = reports.read_facts()
            reports.check_certification()
        for n, certificate in inputs.source_facts[key].items():
            evidence = inputs.evidence_row(n, reports.EXACT_EVIDENCE, key)
            if (
                evidence["certificate"]
                != reports.fact_path().relative_to(ROOT.parent).as_posix()
            ):
                raise ExactValuesError("confirmed source history names a different certificate")
            original = originals[n]
            add(
                n,
                certificate.side,
                result=result,
                source_key=key,
                revision=reports.REVISION,
                facts=reports.fact_path(),
                original=original,
                url=f"{reports.SOURCE}/blob/{reports.REVISION}/{original}",
                receipt=reports.receipt_path(),
                confirmed=True,
            )

    pending_sources = (
        (
            couzo_refinements,
            "T-128",
            {n: couzo_refinements.fact_path() for n in couzo_refinements.NUMBERS},
            {
                n: pin["certificate"]["path"]
                for n, pin in couzo_refinements.source_pins().items()
            },
        ),
        (
            couzo_followup,
            "T-130",
            {n: couzo_followup.fact_path(n) for n in couzo_followup.NUMBERS},
            {n: couzo_followup.certificate_path(n) for n in couzo_followup.NUMBERS},
        ),
    )
    for reports, result, fact_paths, originals in pending_sources:
        facts = reports.read_facts()
        reports.check_certification()
        for n, certificate in facts.items():
            original = originals[n]
            add(
                n,
                certificate.side,
                result=result,
                source_key=reports.SOURCE_KEY,
                revision=reports.REVISION,
                facts=fact_paths[n],
                original=original,
                url=f"{reports.SOURCE}/blob/{reports.REVISION}/{original}",
                receipt=reports.receipt_path(),
                confirmed=False,
            )

    hunt_facts = hunt_reports.read_facts()
    hunt_claims = hunt_reports.check_claims(hunt_facts)
    hunt_reports.check_certification()
    original = hunt_reports.certificate_path(132)
    add(
        132,
        hunt_facts[132].side,
        result="T-131",
        source_key=hunt_reports.SOURCE_KEY,
        revision=hunt_reports.REVISION,
        facts=hunt_reports.PACKET / "source" / original,
        original=original,
        url=f"{hunt_reports.SOURCE}/blob/{hunt_reports.REVISION}/{original}",
        receipt=hunt_reports.receipt_path(),
        confirmed=False,
        source_date=hunt_reports.READ_ON,
    )
    equal_side = next(row["equal_side"] for row in hunt_claims["results"] if row["n"] == 155)
    occurrence = hunt_equal_bound_occurrence(
        indexed[155], rows.get((155, hunt_facts[155].side)), hunt_facts[155], equal_side
    )
    evidence_occurrences = [] if occurrence is None else [occurrence]

    coverage = safe_load((FRONTIER / "source-coverage.yaml").read_text())
    for packet_name, numbers, revision in (
        (
            "evand-batch-105-130-2026-10-07",
            (105, 130),
            "7eef24f7221b8c3371d6171dd664b52541bbd479",
        ),
        ("evand-batch-292-2026-10-07", (292,), "f58a01774a733b232a88576470332185d8d11641"),
    ):
        packet = ROOT / "resources/web" / packet_name
        problems = acquire_source.check(packet, ROOT.parent)
        if problems:
            raise ExactValuesError("reported batch certificate custody: " + "; ".join(problems))
        record = json.loads(read_retained_text(packet / acquire_source.RECORD))
        (source,) = record["sources"]
        if source["source_commit"] != revision or source["source_url"] != evand.SOURCE:
            raise ExactValuesError("reported batch certificate names a different source pin")
        source_key = next(
            row["source_key"] for row in coverage["sources"] if row["id"] == packet_name
        )
        for n in numbers:
            original = f"s12/search/exact/batch/certs/n-{n:03d}.cert"
            path = packet / "source" / original
            certificate = evand.parse(read_retained_text(path), expected_n=n)
            add(
                n,
                certificate.side,
                result="T-129",
                source_key=source_key,
                revision=revision,
                facts=path,
                original=original,
                url=f"{evand.SOURCE}/blob/{revision}/{original}",
                receipt=None,
                confirmed=False,
                source_date="2026-10-07",
            )
    return sorted(
        [*rows.values(), *evidence_occurrences],
        key=lambda row: (row["n"], Fraction(row["exact_form"])),
    )


def build_record() -> dict:
    catalogue = catalogue_entries()
    kkt = kkt_rows()
    verified_inputs = VerifiedRationalInputs()
    entries = [
        build_entry(
            n, load_packing(n), catalogue.get(n), kkt.get(n), verified_inputs=verified_inputs
        )
        for n in KNOWN_BEST_CORPUS.numbers
    ]
    superseded_reported = append_reported_source_notes(entries)
    historical = build_historical_entries(entries)
    historical.extend(superseded_reported)
    historical.extend(source_certificate_history(entries, verified_inputs=verified_inputs))
    historical.sort(key=lambda row: (row["n"], Decimal(row["side"]), row["kind"]))
    return {
        "softschema": {
            "contract": CONTRACT,
            "envelope": "register",
            "schema": SCHEMA,
            "status": "enforced",
        },
        "register": {
            "generated_by": GENERATOR,
            "range": {"first": KNOWN_BEST_CORPUS.first_n, "last": KNOWN_BEST_CORPUS.last_n},
            "sources": {
                "records": "frontier/n-NNN.md",
                "catalogue": CATALOGUE_MARKDOWN,
                "svg_facts": SVG_FACTS,
                "svg_receipts": SVG_RECEIPTS,
                "historical_polynomials": HISTORICAL_FACTS,
                "kkt": {"path": KKT_BATCH, "key": KKT_KEY, "digits": KKT_DIGITS},
            },
            "totals": _totals(entries),
            "entries": entries,
            "historical_entries": historical,
        },
    }


def load_record() -> dict:
    """The register, as committed."""
    return json.loads(read_retained_text(RECORD))["register"]


def register_text(record: dict) -> str:
    return retained_json.dumps(record, sort_keys=True, ensure_ascii=False)


def update() -> None:
    content = register_text(build_record())
    if retained_exists(RECORD) and read_retained_text(RECORD) == content:
        print(f"exact values register already current: {RECORD.name}")
        return
    write_retained_text(RECORD if RECORD.is_file() else compressed_path(RECORD), content)
    print(f"exact values register updated: {RECORD.name}")


def check() -> None:
    if not retained_exists(RECORD):
        raise ValueError(f"missing {RECORD.relative_to(ROOT)}; run with --update")
    record = build_record()
    if read_retained_text(RECORD) != register_text(record):
        raise ValueError(f"stale {RECORD.relative_to(ROOT)}; re-run with --update")
    totals = record["register"]["totals"]
    print(
        "exact values register check passed: "
        f"{totals['irreducible-certified']} polynomials certified irreducible, "
        f"{totals['root-isolated']} roots isolated, matching the frontier records"
    )


def review() -> None:
    """Print the totals and every check worth a second look."""
    started = time.perf_counter()
    register = build_record()["register"]
    elapsed = time.perf_counter() - started
    entries = register["entries"]
    for label, value in register["totals"].items():
        print(f"  {label:24s} {value:3d}")
    print(f"  built in {elapsed:.2f}s")
    print()
    print("  polynomials above degree 12 (degree, height digits, primes):")
    for entry in entries:
        certificate = entry["checks"]["irreducible"]
        if certificate is not None and certificate["method"] == "modular-degree-patterns":
            print(
                f"    n = {entry['n']:3d}  degree {entry['degree']:3d}  "
                f"height {entry['polynomial']['height_digits']:3d}  "
                f"primes {certificate['primes']}"
            )
    print()
    lowest = sorted(
        (entry["checks"]["kkt_agreement_digits"], entry["n"], entry["kkt"]["status"])
        for entry in entries
        if entry["checks"]["kkt_agreement_digits"] is not None
        and entry["state"] not in {"integer", "rational"}
    )[:8]
    print(f"  lowest KKT agreement among non-integer roots (digits, n, status): {lowest}")
    for entry in entries:
        for note in entry["notes"]:
            if note["kind"] == "route" and entry["state"] != "numeric-only":
                print(f"  n = {entry['n']}: {note['text']}")
    rational = [
        (entry["n"], entry["exact_form"]) for entry in entries if entry["state"] == "rational"
    ]
    print(f"  rational sides that are not integers: {rational}")
    windows = [
        (entry["n"], entry["checks"]["root"]["window"])
        for entry in entries
        if entry["checks"]["root"] is not None
        and entry["checks"]["root"]["window"] not in {"kkt", "exact"}
    ]
    print(f"  roots isolated around the record rather than the KKT value: {windows}")
    galois = [
        (entry["n"], entry["checks"]["galois"]["group"])
        for entry in entries
        if entry["checks"]["galois"] is not None and entry["state"] != "closed-form"
    ]
    print(f"  Galois groups beyond the closed forms: {galois}")
    for kind in (
        "superseded-catalogue-polynomial",
        "missing-polynomial-text",
        "no-radical-form",
        "relation-search-negative",
    ):
        counts = [e["n"] for e in entries if any(note["kind"] == kind for note in e["notes"])]
        print(f"  {kind}: n = {counts}")
    numeric = [
        (entry["n"], next(note["bead"] for note in entry["notes"] if note["kind"] == "route"))
        for entry in entries
        if entry["state"] == "numeric-only"
    ]
    print(f"  numeric-only routes (n, bead): {numeric}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--update", action="store_true", help="write the register")
    group.add_argument("--check", action="store_true", help="fail if the register is stale")
    group.add_argument("--review", action="store_true", help="print totals and findings")
    arguments = parser.parse_args(argv)
    try:
        if arguments.update:
            update()
        elif arguments.check:
            check()
        else:
            review()
    except (OSError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
