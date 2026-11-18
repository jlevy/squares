"""Exact decimal prints of fractions (lane r127b-1118). Decides nothing.

Every print is made from the exact fraction with integer arithmetic; no value passes
through floating point on its way to a digit.
"""

from __future__ import annotations

from fractions import Fraction


def _floor_div(a: int, b: int) -> int:
    return a // b


def floor_places(f: Fraction, k: int) -> str:
    scaled = _floor_div(f.numerator * 10**k, f.denominator)
    return _digits(scaled, k)


def ceil_places(f: Fraction, k: int) -> str:
    scaled = -_floor_div(-f.numerator * 10**k, f.denominator)
    return _digits(scaled, k)


def nearest_places(f: Fraction, k: int) -> str:
    """Round half away from zero at ``k`` places."""
    num = abs(f.numerator) * 10**k * 2 + f.denominator
    scaled = num // (2 * f.denominator)
    return _digits(scaled if f >= 0 else -scaled, k)


def _digits(scaled: int, k: int) -> str:
    sign = "-" if scaled < 0 else ""
    s = str(abs(scaled)).rjust(k + 1, "0")
    if k == 0:
        return sign + s
    return f"{sign}{s[:-k]}.{s[-k:]}"


def sci(f: Fraction, digits: int = 6) -> str:
    """``f`` in scientific notation with ``digits`` significant figures, rounded half
    away from zero, from the exact value."""
    if f == 0:
        return "0"
    sign = "-" if f < 0 else ""
    a = abs(f)
    e = len(str(a.numerator)) - len(str(a.denominator))
    # Find e with 10**e <= a < 10**(e+1).
    while Fraction(10) ** e > a:
        e -= 1
    while Fraction(10) ** (e + 1) <= a:
        e += 1
    scaled = a / Fraction(10) ** (e - digits + 1)
    m = (2 * scaled.numerator + scaled.denominator) // (2 * scaled.denominator)
    if m >= 10**digits:
        m //= 10
        e += 1
    s = str(m)
    mant = s[0] + ("." + s[1:] if len(s) > 1 else "")
    return f"{sign}{mant}e{e:+d}"


def exact(f: Fraction) -> str:
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


def terminating_places(f: Fraction) -> int | None:
    """The number of decimal places at which ``f`` terminates, or ``None``."""
    d = f.denominator
    twos = fives = 0
    while d % 2 == 0:
        d //= 2
        twos += 1
    while d % 5 == 0:
        d //= 5
        fives += 1
    if d != 1:
        return None
    return max(twos, fives)
