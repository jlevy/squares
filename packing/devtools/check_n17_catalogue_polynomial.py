"""Identify the H-255 chart root's side with the n17 catalogue polynomial (H-265).

Primary route: the exact resultant in t of the two H-255 chart polynomials, its image
under S = (6 + 4t)/(1 + 2t - t^2) as a second exact resultant, factorization over Q,
and exact real-root isolation inside the outward rational image of the certified H-255
t-range. Every resultant lies in the ideal of its inputs, so it vanishes at the
certified root whatever its extraneous factors.

Recheck: a different elimination order (t first, then b), exact division by the
catalogue polynomial, an exact Taylor exclusion showing the cofactor has no root in the
side interval, a Fraction sign change of the catalogue polynomial across that interval,
and a pure-Python Rabin irreducibility test modulo a prime not dividing its leading
coefficient. None of the recheck uses the factorizer.

This identifies an algebraic number. It is no packing, feasibility or optimality claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import yaml
from sympy import Poly, Rational, Symbol, resultant

from sqpack.yamlio import load_yaml

REPO = Path(__file__).resolve().parents[2]
RUN = (
    REPO / "packing/campaign/series/series-000-smoke-and-calibration/results/"
    "exp-237-n17-polynomial-root/run-001"
)
CERTIFICATE = RUN / "certificate.json"
CHECKER = RUN / "checker.json"
CATALOGUE = REPO / "packing/frontier/n-017.md"
MODULE = Path(__file__).resolve()
SCHEMA = "n17-catalogue-polynomial/v1"
SIDE_DIGITS = 30
ENCLOSURE_EPS = Q(1, 10**40)
PRIME_LIMIT = 1000
T, B, S = Symbol("t"), Symbol("b"), Symbol("S")
TERM = re.compile(r"([+-])?(\d+)?(?:(s)(?:\^(?:\{(\d+)\}|(\d+)))?)?")

Terms = dict[tuple[int, int], int]


class RefusalError(ValueError):
    """An input that the frozen H-265 determination does not accept."""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def display(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO).as_posix()
    except ValueError:
        return str(path)


# --- Inputs -----------------------------------------------------------------------


def _integer(value: object) -> int:
    if type(value) is int:
        return value
    if type(value) is str and re.fullmatch(r"-?\d+", value):
        return int(value)
    raise RefusalError(f"expected an exact integer, got {value!r}")


def parse_terms(rows: object) -> Terms:
    """Read a certificate polynomial, ``[[i, j, "c"], ...]`` for c t^i b^j."""
    if type(rows) is not list or not rows:
        raise RefusalError("a chart polynomial must be a nonempty list of terms")
    terms: Terms = {}
    for row in rows:
        if type(row) is not list or len(row) != 3:
            raise RefusalError("a chart term must be [t_power, b_power, coefficient]")
        i, j, c = (_integer(value) for value in row)
        if i < 0 or j < 0 or c == 0 or (i, j) in terms:
            raise RefusalError(f"bad or repeated chart term {row!r}")
        terms[(i, j)] = c
    return terms


def load_certificate(path: Path, checker: Path) -> tuple[Terms, Terms, tuple[Q, Q]]:
    """The H-255 polynomials and t-range, accepted only with their passing checker."""
    document = json.loads(path.read_bytes())
    receipt = json.loads(checker.read_bytes())
    if type(document) is not dict or document.get("schema") != "n17-root-certificate/v1":
        raise RefusalError("not an n17 root certificate")
    if document.get("criterion_passed") is not True or document.get("failures") != []:
        raise RefusalError("the root certificate did not pass")
    if type(receipt) is not dict or receipt.get("verification_passed") is not True:
        raise RefusalError("the independent root checker did not pass")
    if receipt.get("q") != document.get("q") or receipt.get("inclusion_bounds") != document.get(
        "inclusion_bounds"
    ):
        raise RefusalError("the checker receipt does not match this certificate")
    polynomials = document.get("polynomials")
    box = document.get("box")
    if type(polynomials) is not list or len(polynomials) != 2 or type(box) is not dict:
        raise RefusalError("the certificate must carry two polynomials and a box")
    midpoint, radius = Q(box["midpoint"][0]), Q(box["radius"])
    if radius <= 0:
        raise RefusalError("the certificate radius must be positive")
    return (
        parse_terms(polynomials[0]),
        parse_terms(polynomials[1]),
        (midpoint - radius, midpoint + radius),
    )


def parse_catalogue_polynomial(text: str) -> list[int]:
    """Parse ``a s^{n} + ... + c = 0`` into integer coefficients, highest first."""
    body = re.sub(r"\s+", "", text)
    if not body.endswith("=0") or body.count("=") != 1:
        raise RefusalError("the catalogue polynomial must read '... = 0'")
    body = body[:-2]
    found: dict[int, int] = {}
    position = 0
    while position < len(body):
        match = TERM.match(body, position)
        if match is None or match.end() == position:
            raise RefusalError(f"unparsed catalogue text at {body[position:]!r}")
        sign, digits, variable, braced, bare = match.groups()
        if (position and sign is None) or (digits is None and variable is None):
            raise RefusalError(f"malformed catalogue term {match.group(0)!r}")
        power = int(braced or bare or 1) if variable else 0
        coefficient = int(digits or 1) * (-1 if sign == "-" else 1)
        if power in found or coefficient == 0:
            raise RefusalError(f"repeated or zero catalogue term s^{power}")
        found[power] = coefficient
        position = match.end()
    if not found or max(found) < 1:
        raise RefusalError("the catalogue polynomial must be nonconstant")
    return [found.get(power, 0) for power in range(max(found), -1, -1)]


def load_catalogue(path: Path) -> tuple[list[int], int]:
    """The recorded minimal polynomial and degree from a frontier case file."""
    text = path.read_text(encoding="utf-8")
    parts = text.split("\n---\n", 1)
    if not text.startswith("---\n") or len(parts) != 2:
        raise RefusalError("the frontier file has no YAML frontmatter")
    front = load_yaml(parts[0][4:])
    try:
        record = front["packing"]["reported_upper_bound"]
        polynomial, degree = record["minimal_polynomial"], record["algebraic_degree"]
    except (KeyError, TypeError) as error:
        raise RefusalError("the frontier file records no minimal polynomial") from error
    if type(polynomial) is not str or type(degree) is not int:
        raise RefusalError("the recorded polynomial or degree has the wrong type")
    return parse_catalogue_polynomial(polynomial), degree


# --- Exact algebra -----------------------------------------------------------------


def chart_poly(terms: Terms) -> Poly:
    return Poly(dict(terms), T, B, domain="ZZ")


def formula_polynomials() -> tuple[Poly, Poly]:
    """The H-255 pair, rebuilt in sympy from its defining formulas."""
    t, b = T, B
    d, e = 1 + t**2, 1 + b**2
    ell = (1 + t) * d
    n_alpha = (1 - t**2) * (1 - b**2) - 4 * t * b
    pi2 = 2 * t * (1 - t) * (1 - b**2) + (1 - t) ** 2 * ell * b - t * ell * e
    pi3 = (
        (1 - t**2) * d * e**2
        - (1 + t) * d * e * (b * (1 - t**2) + t * (1 - b**2))
        - (1 - t) * (1 - b**2) * n_alpha
    )
    return Poly(pi2, T, B, domain="ZZ"), Poly(pi3, T, B, domain="ZZ")


def substitution() -> Poly:
    """S*(1 + 2t - t^2) - (6 + 4t), whose t-roots are the preimages of S."""
    return Poly(S * (1 + 2 * T - T**2) - (6 + 4 * T), T, S, domain="ZZ")


def eliminate_b(p2: Poly, p3: Poly) -> Poly:
    value = Poly(resultant(p2.as_expr(), p3.as_expr(), B), T, domain="ZZ")
    if value.is_zero:
        raise RefusalError("the chart polynomials share a factor; the resultant vanishes")
    return value


def map_to_side(r: Poly) -> Poly:
    value = Poly(resultant(r.as_expr(), substitution().as_expr(), T), S, domain="ZZ")
    if value.is_zero:
        raise RefusalError("the side resultant vanishes identically")
    return value


def coefficients(poly: Poly) -> list[int]:
    return [int(value) for value in poly.all_coeffs()]


def fraction(value: Any) -> Q:
    """A sympy rational as a Fraction, through its exact ``a/b`` text."""
    return Q(str(Rational(value)))


def rational(value: Q) -> Any:
    """A Fraction as a sympy Rational."""
    return Rational(value.numerator, value.denominator)


def horner(coeffs: list[int], x: Q) -> Q:
    total = Q(0)
    for coefficient in coeffs:
        total = total * x + coefficient
    return total


def side_interval(t_lo: Q, t_hi: Q, digits: int = SIDE_DIGITS) -> tuple[Q, Q]:
    """Outward rational bounds on S(t) over [t_lo, t_hi], with monotonicity proved.

    K = 1 + 2t - t^2 is concave and S' = 4(t^2 + 3t - 2)/K^2 has a convex numerator,
    so their signs at both endpoints settle them on the whole range.
    """
    if not t_lo < t_hi:
        raise RefusalError("the t-range must have positive width")
    for t in (t_lo, t_hi):
        if 1 + 2 * t - t * t <= 0:
            raise RefusalError("K = 1 + 2t - t^2 is not positive on the t-range")
        if t * t + 3 * t - 2 >= 0:
            raise RefusalError("S is not certified decreasing on the t-range")
    scale = 10**digits

    def side(t: Q) -> Q:
        return (6 + 4 * t) / (1 + 2 * t - t * t)

    low, high = side(t_hi), side(t_lo)
    return Q((low.numerator * scale) // low.denominator, scale), Q(
        -((-high.numerator * scale) // high.denominator), scale
    )


def isolate(poly: Poly, lo: Q, hi: Q) -> list[tuple[Q, Q]]:
    """Exact isolating intervals of the real roots of ``poly`` in the closed [lo, hi]."""
    found: Any = poly.intervals(inf=rational(lo), sup=rational(hi))
    return [(fraction(pair[0][0]), fraction(pair[0][1])) for pair in found]


def factors(poly: Poly) -> list[tuple[Poly, int]]:
    _, found = poly.factor_list()
    return sorted(found, key=lambda pair: (pair[0].degree(), coefficients(pair[0])))


def unit_ratio(left: list[int], right: list[int]) -> Q | None:
    """The rational c with left = c * right, or None if there is none."""
    if len(left) != len(right) or not right or right[0] == 0:
        return None
    ratio = Q(left[0], right[0])
    return ratio if all(a == ratio * b for a, b in zip(left, right, strict=True)) else None


# --- Rabin irreducibility over F_p, pure Python ------------------------------------


def _trim(a: list[int]) -> list[int]:
    while a and a[-1] == 0:
        a.pop()
    return a


def _rem(a: list[int], f: list[int], p: int) -> list[int]:
    """a mod f over F_p; coefficient lists are lowest first and f is monic."""
    a = _trim([value % p for value in a])
    n = len(f) - 1
    while len(a) > n:
        lead, shift = a[-1], len(a) - 1 - n
        for i, value in enumerate(f):
            a[shift + i] = (a[shift + i] - lead * value) % p
        _trim(a)
    return a


def _mulmod(a: list[int], b: list[int], f: list[int], p: int) -> list[int]:
    product = [0] * (len(a) + len(b))
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            product[i + j] += x * y
    return _rem(product, f, p)


def _powmod(a: list[int], exponent: int, f: list[int], p: int) -> list[int]:
    result, base = [1], _rem(a, f, p)
    while exponent:
        if exponent & 1:
            result = _mulmod(result, base, f, p)
        base = _mulmod(base, base, f, p)
        exponent >>= 1
    return result


def _gcd(a: list[int], b: list[int], p: int) -> list[int]:
    a, b = _trim([v % p for v in a]), _trim([v % p for v in b])
    while b:
        inverse = pow(b[-1], -1, p)
        b = [(value * inverse) % p for value in b]
        a, b = b, _rem(a, b, p)
    return a


def _prime_divisors(n: int) -> list[int]:
    found, d = [], 2
    while d * d <= n:
        if n % d == 0:
            found.append(d)
            while n % d == 0:
                n //= d
        d += 1
    return [*found, n] if n > 1 else found


def irreducible_mod_p(coeffs: list[int], p: int) -> bool:
    """Rabin's test: f of degree n is irreducible over F_p iff f | x^(p^n) - x and
    gcd(f, x^(p^(n/q)) - x) = 1 for every prime q | n. The leading coefficient must
    be a unit mod p, so the reduction keeps its degree."""
    n = len(coeffs) - 1
    if n < 1 or coeffs[0] % p == 0:
        raise RefusalError("Rabin's test needs a nonconstant f with p not dividing its lead")
    inverse = pow(coeffs[0], -1, p)
    f = [(value * inverse) % p for value in reversed(coeffs)]
    frobenius = {0: [0, 1]}
    for k in range(1, n + 1):
        frobenius[k] = _powmod(frobenius[k - 1], p, f, p)
    x_mod_f = _rem([0, 1], f, p)
    if frobenius[n] != x_mod_f:
        return False
    for q in _prime_divisors(n):
        difference = list(frobenius[n // q]) + [0] * 2
        difference[1] -= 1
        if len(_gcd(f, difference, p)) != 1:
            return False
    return True


def first_irreducible_prime(
    coeffs: list[int], limit: int = PRIME_LIMIT
) -> tuple[int | None, int]:
    """The smallest prime below ``limit`` modulo which ``coeffs`` is irreducible."""
    tried = 0
    for p in range(2, limit):
        if any(p % d == 0 for d in range(2, int(p**0.5) + 1)) or coeffs[0] % p == 0:
            continue
        tried += 1
        if irreducible_mod_p(coeffs, p):
            return p, tried
    return None, tried


# --- Second elimination order ------------------------------------------------------


def taylor(coeffs: list[Q], centre: Q) -> list[Q]:
    """Coefficients of p(centre + x), lowest first, by repeated synthetic division."""
    remaining, shifted = list(coeffs), []
    while remaining:
        accumulator, quotient = Q(0), []
        for coefficient in remaining:
            accumulator = accumulator * centre + coefficient
            quotient.append(accumulator)
        shifted.append(quotient.pop())
        remaining = quotient
    return shifted


def root_free(coeffs: list[Q], lo: Q, hi: Q) -> bool:
    """True when |p(m)| exceeds the Taylor tail on [lo, hi], so p has no root there."""
    centre, radius = (lo + hi) / 2, (hi - lo) / 2
    shifted = taylor(coeffs, centre)
    tail = sum((abs(c) * radius**k for k, c in enumerate(shifted) if k), Q(0))
    return abs(shifted[0]) > tail


def second_route(p2: Poly, p3: Poly, catalogue: list[int], lo: Q, hi: Q) -> dict[str, Any]:
    """Eliminate t first, then b; show the catalogue polynomial carries the root.

    The total resultant vanishes at S*. Writing it as C^k H with the cofactor H root-free
    on the side interval (exact Taylor exclusion, no Sturm sequence or factorizer) puts
    S* among the roots of C.
    """
    g = substitution()
    first = resultant(p2.as_expr(), g.as_expr(), T)
    second = resultant(p3.as_expr(), g.as_expr(), T)
    total = Poly(resultant(first, second, B), S, domain="QQ")
    if total.is_zero:
        return {"failures": ["second-route resultant vanishes identically"]}
    target = Poly(catalogue, S, domain="QQ")
    cofactor, power = total, 0
    while True:
        quotient, remainder = cofactor.div(target)
        if not remainder.is_zero:
            break
        cofactor, power = quotient, power + 1
    cofactor_free = root_free([fraction(c) for c in cofactor.all_coeffs()], lo, hi)
    catalogue_roots = int(target.count_roots(rational(lo), rational(hi)))
    at_lo, at_hi = horner(catalogue, lo), horner(catalogue, hi)
    failures = [
        name
        for name, okay in (
            ("second route: catalogue polynomial does not divide the resultant", power >= 1),
            ("second route: cofactor is not root-free on the side interval", cofactor_free),
            ("second route: catalogue polynomial lacks one root there", catalogue_roots == 1),
            ("second route: no sign change across the side interval", at_lo * at_hi < 0),
        )
        if not okay
    ]
    return {
        "order": "res_b(res_t(Pi2, G), res_t(Pi3, G)), G = S(1 + 2t - t^2) - (6 + 4t)",
        "degree": total.degree(),
        "catalogue_multiplicity": power,
        "cofactor_degree": cofactor.degree(),
        "cofactor_root_free_on_side_interval": cofactor_free,
        "catalogue_roots_in_side_interval": catalogue_roots,
        "catalogue_sign_at_side_interval": [_sign(at_lo), _sign(at_hi)],
        "failures": failures,
    }


def _sign(value: Q) -> int:
    return (value > 0) - (value < 0)


# --- Determination -----------------------------------------------------------------


def _factor_rows(poly: Poly, lo: Q, hi: Q) -> list[dict[str, Any]]:
    return [
        {
            "degree": factor.degree(),
            "multiplicity": multiplicity,
            "coefficients": coefficients(factor),
            "roots_in_interval": [[str(a), str(b)] for a, b in isolate(factor, lo, hi)],
        }
        for factor, multiplicity in factors(poly)
    ]


def determine(
    p2_terms: Terms,
    p3_terms: Terms,
    t_box: tuple[Q, Q],
    catalogue: list[int],
    *,
    recorded_degree: int | None = None,
    formulas: tuple[Poly, Poly] | None = None,
    digits: int = SIDE_DIGITS,
) -> dict[str, Any]:
    """Run both routes and return the exact receipt body with its verdict."""
    failures: list[str] = []
    p2, p3 = chart_poly(p2_terms), chart_poly(p3_terms)
    if formulas is not None and (p2, p3) != formulas:
        failures.append("certificate polynomials differ from the H-255 formulas")
    t_lo, t_hi = t_box
    s_lo, s_hi = side_interval(t_lo, t_hi, digits)

    r = eliminate_b(p2, p3)
    side = map_to_side(r)
    t_rows = _factor_rows(r, t_lo, t_hi)
    s_rows = _factor_rows(side, s_lo, s_hi)
    if horner(coefficients(side), s_lo) == 0 or horner(coefficients(side), s_hi) == 0:
        failures.append("the side polynomial vanishes at an interval endpoint")
    carrying = [row for row in s_rows if row["roots_in_interval"]]
    if len(carrying) != 1 or len(carrying[0]["roots_in_interval"]) != 1:
        failures.append("the side interval does not isolate one root of one factor")
    vanishing = carrying[0]["coefficients"] if len(carrying) == 1 else []
    ratio = unit_ratio(vanishing, catalogue)
    if ratio is None:
        failures.append("the vanishing factor differs from the catalogue polynomial")

    catalogue_poly = Poly(catalogue, S, domain="ZZ")
    catalogue_factors = factors(catalogue_poly)
    over_q = len(catalogue_factors) == 1 and catalogue_factors[0][1] == 1
    if not over_q:
        failures.append("the catalogue polynomial factors over Q")
    if recorded_degree is not None and recorded_degree != len(catalogue) - 1:
        failures.append("the recorded algebraic degree differs from the polynomial's")
    prime, tried = first_irreducible_prime(catalogue)
    if prime is None:
        failures.append(f"no prime below {PRIME_LIMIT} certifies irreducibility")
    recheck = second_route(p2, p3, catalogue, s_lo, s_hi)
    failures.extend(recheck["failures"])

    enclosure: list[str] = []
    if len(carrying) == 1 and len(carrying[0]["roots_in_interval"]) == 1:
        lo, hi = (Q(value) for value in carrying[0]["roots_in_interval"][0])
        vanishing_poly = Poly(vanishing, S, domain="ZZ")
        a, b = vanishing_poly.refine_root(
            rational(lo), rational(hi), eps=rational(ENCLOSURE_EPS)
        )
        enclosure = [str(fraction(a)), str(fraction(b))]

    passed = not failures
    return {
        "schema": SCHEMA,
        "chart_polynomials": [
            [[i, j, c] for (i, j), c in sorted(terms.items())] for terms in (p2_terms, p3_terms)
        ],
        "t_box": [str(t_lo), str(t_hi)],
        "side_interval": {"digits": digits, "outward": [str(s_lo), str(s_hi)]},
        "resultant_t": {
            "degree": r.degree(),
            "coefficients": coefficients(r),
            "factors": t_rows,
        },
        "side_polynomial": {
            "degree": side.degree(),
            "coefficients": coefficients(side),
            "factors": s_rows,
        },
        "vanishing_factor": {"degree": len(vanishing) - 1, "coefficients": vanishing},
        "root_enclosure": enclosure,
        "catalogue": {
            "degree": len(catalogue) - 1,
            "recorded_degree": recorded_degree,
            "coefficients": catalogue,
        },
        "comparison": {
            "equal_up_to_unit": ratio is not None,
            "unit": str(ratio) if ratio is not None else None,
        },
        "irreducibility": {
            "factor_list_over_Q": [
                {"degree": f.degree(), "multiplicity": m} for f, m in catalogue_factors
            ],
            "rabin_prime": prime,
            "rabin_primes_tried": tried,
        },
        "second_route": recheck,
        "failures": failures,
        "criterion_passed": passed,
        "verdict": (
            "identical up to a rational unit and irreducible over Q"
            if passed
            else "not confirmed"
        ),
        "limitations": (
            "Identifies the side of the certified H-255 chart root as an algebraic number; "
            "no packing, feasibility, rigidity or optimality claim."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--checker", type=Path, default=CHECKER)
    parser.add_argument("--catalogue", type=Path, default=CATALOGUE)
    parser.add_argument("--output", type=Path)
    options = parser.parse_args(argv)
    try:
        p2, p3, t_box = load_certificate(options.certificate, options.checker)
        catalogue, degree = load_catalogue(options.catalogue)
        result = determine(
            p2, p3, t_box, catalogue, recorded_degree=degree, formulas=formula_polynomials()
        )
        result["inputs"] = {
            name: {"path": display(path), "sha256": sha256(path)}
            for name, path in (
                ("certificate", options.certificate),
                ("checker", options.checker),
                ("catalogue", options.catalogue),
                ("module", MODULE),
            )
        }
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as error:
        print(json.dumps({"schema": SCHEMA, "criterion_passed": False, "refused": str(error)}))
        return 2
    text = json.dumps(result, indent=2, sort_keys=True)
    if options.output is not None:
        options.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if result["criterion_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
