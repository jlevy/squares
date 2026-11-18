"""Exact decimal prints of Fractions for lane r1021-1118's receipts.  Decides nothing."""

from __future__ import annotations

from fractions import Fraction


def floor_places(fr: Fraction, k: int) -> str:
    """fr rounded down at k decimal places, as a decimal string."""
    scaled = (fr.numerator * 10**k) // fr.denominator
    return _place(scaled, k)


def ceil_places(fr: Fraction, k: int) -> str:
    """fr rounded up at k decimal places, as a decimal string."""
    scaled = -((-fr.numerator * 10**k) // fr.denominator)
    return _place(scaled, k)


def _place(scaled: int, k: int) -> str:
    sign = "-" if scaled < 0 else ""
    a = abs(scaled)
    whole, frac = divmod(a, 10**k)
    return f"{sign}{whole}.{frac:0{k}d}" if k else f"{sign}{whole}"


def sci(fr, sig: int = 8) -> str:
    """fr in scientific notation with sig significant digits, rounded half up, exactly."""
    fr = Fraction(fr)
    if fr == 0:
        return "0"
    sign = "-" if fr < 0 else ""
    a = abs(fr)
    e = len(str(a.numerator)) - len(str(a.denominator))
    # 10**e <= a < 10**(e+1)
    while Fraction(10) ** e > a:
        e -= 1
    while Fraction(10) ** (e + 1) <= a:
        e += 1
    shift = sig - 1 - e
    m = a * Fraction(10) ** shift
    mi = int(m)
    if m - mi >= Fraction(1, 2):
        mi += 1
    if mi >= 10**sig:
        mi //= 10
        e += 1
    digits = str(mi)
    mant = digits[0] + ("." + digits[1:] if sig > 1 else "")
    return f"{sign}{mant}e{e:+d}"


def frac_text(fr: Fraction) -> str:
    return f"{fr.numerator}/{fr.denominator}" if fr.denominator != 1 else str(fr.numerator)
