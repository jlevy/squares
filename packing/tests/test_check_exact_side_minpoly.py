"""Tests for devtools.check_exact_side_minpoly: isolation, signs, factor-degree patterns."""

from __future__ import annotations

import random
from fractions import Fraction

import numpy as np
import pytest
from gmpy2 import mpz
from sympy import GF, Poly, symbols

from devtools.check_exact_side_minpoly import (
    ModPoly,
    Reducer,
    compare,
    distinct_degree_pattern,
    irreducible,
    isolate,
    rational_sign,
)

X = symbols("x")


def coefficients(expression: object) -> list[object]:
    return [mpz(int(c)) for c in reversed(Poly(expression, X).all_coeffs())]


def test_isolates_sqrt2_and_orders_it_against_a_rational() -> None:
    p = coefficients(X**2 - 2)
    result = isolate(p, Fraction("1.41421356"), Fraction("1.41421357"), exponent=60, order=8)
    assert result["exactly_one_root"]
    assert compare(p, result, Fraction(3, 2))["root_below_rational"]
    assert rational_sign(p, Fraction(3, 2)) == 1
    assert rational_sign(p, Fraction(7, 5)) == -1


def test_refuses_an_interval_holding_two_roots() -> None:
    p = coefficients(
        (X - Fraction(1, 3)) * (X - Fraction(1, 3) - Fraction(1, 10**6)) * 3 * 10**6 * 3
    )
    result = isolate(p, Fraction(1, 4), Fraction(1, 2), exponent=60, order=8)
    assert not result["exactly_one_root"]


def test_refuses_an_interval_with_no_sign_change() -> None:
    result = isolate(coefficients(X**2 - 2), Fraction(3, 2), Fraction(2), exponent=60, order=8)
    assert not result["sign_change"]
    assert not result["exactly_one_root"]


def test_modular_product_and_reduction_agree_with_sympy() -> None:
    q = 40009
    rng = random.Random(7)
    a = [rng.randrange(q) for _ in range(300)]
    b = [rng.randrange(q) for _ in range(200)]
    f = [rng.randrange(q) for _ in range(150)] + [1]
    ring = ModPoly(q)
    product = ring.mul(np.array(a), np.array(b))
    expected = Poly(list(reversed(a)), X, domain=GF(q)) * Poly(
        list(reversed(b)), X, domain=GF(q)
    )
    assert [int(c) % q for c in reversed(expected.all_coeffs())] == [
        int(c) for c in ring.trim(product)
    ]
    reduced = Reducer(ring, np.array(f)).reduce(product)
    remainder = expected.rem(Poly(list(reversed(f)), X, domain=GF(q)))
    assert [int(c) % q for c in reversed(remainder.all_coeffs())] == [int(c) for c in reduced]


def test_distinct_degree_pattern_matches_sympy_factorization() -> None:
    q = 40009
    rng = random.Random(11)
    coeffs = [rng.randrange(q) for _ in range(60)] + [1]
    ring = ModPoly(q)
    f = np.array(coeffs, dtype=np.int64)
    if ring.gcd(f, ring.derivative(f)).size > 1:
        pytest.skip("random polynomial not squarefree")
    _, factors = Poly(list(reversed(coeffs)), X, domain=GF(q)).factor_list()
    expected = sorted(factor.degree() for factor, exponent in factors for _ in range(exponent))
    assert distinct_degree_pattern(ring, f, block=4) == expected


def test_certifies_an_irreducible_quintic_and_refuses_reducible_controls() -> None:
    assert irreducible(coefficients(X**5 - X - 1), primes=6, start=40000)["irreducible_over_Q"]
    reducible = irreducible(coefficients((X**2 + 1) * (X**3 + X + 1)), primes=6, start=40000)
    assert not reducible["irreducible_over_Q"]
    assert {2, 3} <= set(reducible["possible_proper_factor_degrees"])
    # x^4 + 1 is irreducible over Q but splits modulo every prime: the degree-pattern
    # method must say "not proven" rather than certify it.
    assert not irreducible(coefficients(X**4 + 1), primes=6, start=40000)["irreducible_over_Q"]
