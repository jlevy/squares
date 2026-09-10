"""Replay the exact arithmetic in the robust outer-corner draft."""

from __future__ import annotations

import json
from fractions import Fraction

import sympy as sp


def arithmetic_checks(epsilon: Fraction = Fraction(1, 1000)) -> dict[str, bool]:
    """Named rational checks; the fixed draft uses the default epsilon."""
    q = Fraction(96, 25)
    h = Fraction(23, 25)
    a = Fraction(3152, 3175)
    b = Fraction(2336, 3175)
    d = 1 - a
    e = h - b
    big_h = h + epsilon
    big_e = e + epsilon
    return {
        "d": d == Fraction(23, 3175),
        "e": e == Fraction(117, 635),
        "mark_inside_horizontal_inset": epsilon < a < 1 - epsilon,
        "mark_below_inset": b < big_h,
        "left_case_H": big_h < Fraction(37, 40),
        "left_case_E": big_e < Fraction(1, 5),
        "left_case_a": a - epsilon > Fraction(9, 10),
        "left_case_sum": Fraction(37, 40) + Fraction(1, 4500) < 1,
        "r_cutoff": b < Fraction(369, 500),
        "r_function_increases": 1 - 2 * big_e > 0,
        "p_from_r": 1 - Fraction(9, 10) ** 2 > Fraction(2, 5) ** 2,
        "r_lower": 32 * (d - epsilon) > big_e,
        "r_lower_equivalent": Fraction(151, 3175) > 33 * epsilon,
        "alpha_lower": Fraction(2, 5) * h == Fraction(46, 125) > Fraction(1, 100),
        "beta_lower": h / 80 == Fraction(23, 2000) > Fraction(1, 100),
        "alpha_upper_norm": big_h**2 + big_e**2 < Fraction(1433, 1600),
        "alpha_upper_root": Fraction(1433, 1600) < Fraction(19, 20) ** 2,
        "ratio_root": Fraction(47, 50) ** 2 < Fraction(8, 9),
        "ratio_above_H": Fraction(47, 50) > big_h,
        "beta_upper": Fraction(47, 50) - big_h == Fraction(19, 1000) > Fraction(1, 100),
        "common_point": a + h + d == q / 2,
        "alternate_left": epsilon < b < 1 - epsilon and big_h < a < h + 1 - epsilon,
        "alternate_right": q - 1 + epsilon < q - b < q - epsilon,
    }


def algebra_checks() -> dict[str, bool]:
    """Polynomial identities modulo p²+r²=1; no numerical angle sampling."""
    p, r, h, b, e = sp.symbols("p r h b e")
    z = p * r
    circle = p**2 + r**2 - 1
    ratio_identity = sp.expand(9 * (p + r) ** 2 - 8 * (1 + z) ** 2 - (1 - 2 * z) * (1 + 4 * z))
    support_left = p + r - b - p * r * h - r**2 * e
    support_right = p + r - h * (1 + p * r) + e * p**2
    support_identity = sp.expand((support_left - support_right).subs(b, h - e))
    return {
        "ratio_identity_mod_circle": sp.expand(ratio_identity - 9 * circle) == 0,
        "support_identity_mod_circle": sp.expand(support_identity + e * circle) == 0,
    }


def main() -> int:
    checks = {**arithmetic_checks(), **algebra_checks()}
    failed = [name for name, holds in checks.items() if not holds]
    print(json.dumps({"schema": "robust-outer-corner-arithmetic-v1", "checks": checks}))
    return bool(failed)


if __name__ == "__main__":
    raise SystemExit(main())
