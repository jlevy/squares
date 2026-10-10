"""Interval re-check of the closed-form constants of Ryu's k^{2/5} and k^{3/8} bounds on c*(k).

Sungjoon Ryu's preprint "Packing k^2-c unit squares: an upper bound of order k^{3/8} for
the deficiency" (issue #471, version 1.0, and #486, version 1.1; retained in
``packing/resources/web/squarepacker-k2-minus-c-upper-2026-10-09/`` and
``...-v11-2026-10-10/``) reduces its two asymptotic theorems to a few numbers. Written
from the text and not from the author's ``const_stair.py``, ``cert3e.py`` or merges, this
module re-decides them on ``mpmath`` intervals at 50 digits:

- Theorem 1.2: the seven terms of Phi of Corollary 7.4 at x0 = 10^(-4/3), Phi(x0) <=
  5.0163 <= C_E = 5.03, the tilt bounds, the limit sqrt(A/kappa) + 3/2, a supremum of Phi
  over a subdivision of [0, x0] that does not use the monotonicity argument, the closed
  form (20/3)(3/2)^{2/5} 5.03^{3/5} < 20.668 and (8/3) 5.03 10^{-4/3} < 0.623, the
  threshold k0 = 1.6*10^7, lambda' < 1, the limit coefficient 18.89, and the two
  comparison columns of Table 2.
- Theorem 1.1 of version 1.0: (32/5)(5/3)^{3/8} 15.54^{5/8} < 43.06, (12/5) 15.54
  10^{-32/5} <= 2*10^-5, (3/5) 15.54 10^{128/5} <= 4*10^26, and the crossing with
  Theorem 1.2 at about 5.6*10^12.
- Theorem 1.1 of version 1.1: for each of the twelve tiers of Table 1, the three stated
  inequalities C_i >= (32/5)(5/3)^{3/8} C_E^{5/8}, k_i >= (3/5) C_E b0^{8/5} and
  a_i >= (12/5) C_E b0^{-2/5}, a_i < 0.623, and the table's last column
  max(k_i, (C_i/20.668)^40).

What it does not decide: that Corollaries 7.4, 8.3 and 8.12 hold. Their end constants
C_E = 5.03, 15.54 and each tier's C_E are inputs here; C_E for the k^{3/8} bounds comes
from the source's interval coverings, which ``cases.asymptotic.ryu_upper_replay`` replays.
A check holds only when the intervals decide it; every comparison is with a decimal
string, never a binary float.

Run from ``packing/``::

    uv run --frozen --all-extras --group dev python -m \\
        cases.asymptotic.ryu_upper_constants [--subdivisions 400]
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from math import isqrt
from typing import Any

import mpmath

from cases.asymptotic.ryu_k2_minus_c_constants import Check

#: mpmath's interval context; its functions are attached at run time.
iv: Any = mpmath.iv
DIGITS = 50


@dataclass(frozen=True)
class Tier:
    """One row of version 1.1's Table 1 (``tab:tiers``), as printed."""

    name: str
    log_b0: str
    c_e: str
    c: str
    k: str
    a: str
    better_from: str


TIERS = (
    Tier("B1", "7.7", "17.461", "46.31", "2.2e13", "0.035", "1.04e14"),
    Tier("B1s", "7.9", "16.968", "45.49", "4.5e13", "0.029", "5.07e13"),
    Tier("B2", "8", "16.721", "45.08", "6.4e13", "0.026", "6.4e13"),
    Tier("A1", "8.5", "18.961", "48.76", "4.6e14", "0.019", "8.14e14"),
    Tier("A1s", "8.58", "18.722", "48.38", "6.1e14", "0.017", "6.1e14"),
    Tier("A2", "9", "17.523", "46.42", "2.7e15", "0.011", "2.7e15"),
    Tier("A3", "10", "15.859", "43.61", "9.6e16", "0.0039", "9.6e16"),
    Tier("A4", "12", "14.778", "41.73", "1.5e20", "5.7e-4", "1.5e20"),
    Tier("A5", "16", "14.153", "40.62", "3.4e26", "1.4e-5", "3.4e26"),
    Tier("C1", "7.3617", "14.473", "41.19", "5.22e12", "0.04", "5.22e12"),
    Tier("C2", "7.2", "14.805", "41.78", "2.95e12", "0.047", "2.95e12"),
    Tier("C3", "7.15", "14.983", "42.09", "2.48e12", "0.05", "2.48e12"),
)

#: Table 2 of the text: k and its two comparison columns, the integer part of
#: 20.668 k^{2/5} + 0.623 and 8 ceil(sqrt(k-4)) - 1.
TABLE_2 = (
    (100000, 2067, 2535),
    (1000000, 5192, 7999),
    (10000000, 13041, 25303),
    (38250000, 22302, 49479),
    (100000000, 32757, 79999),
)


def _d(text: str):
    """The interval of a decimal string."""
    return iv.mpf(text)


def at_most(value, text: str) -> bool:
    """Every point of ``value`` is at most the decimal ``text``."""
    return bool(value.b <= _d(text).a)


def below(value, text: str) -> bool:
    return bool(value.b < _d(text).a)


def at_least(value, text: str) -> bool:
    return bool(value.a >= _d(text).b)


def dominates(value, other) -> bool:
    """Every point of the interval ``value`` is at least every point of ``other``."""
    return bool(value.a >= other.b)


def inside(value, low: str, high: str) -> bool:
    return bool(value.a >= _d(low).b and value.b <= _d(high).a)


def show(value) -> str:
    return str(iv.nstr(value, 12))


def phi_terms(x) -> dict[str, Any]:
    """The seven right-hand sides of Corollary 7.4 (iv), with t-bar and tau-bar."""
    kappa = _d("0.75")
    a = _d("6.000002")
    p = kappa - _d("5e-8") * x**2
    theta = (x + iv.sqrt(x**2 + a * kappa)) / (2 * p) + x**2 / 16
    t_bar = x * theta
    tau_bar = 2 * t_bar / (1 - t_bar**2)
    sec_bar = (1 + t_bar**2) / (1 - t_bar**2)
    mu = _d("2.000001")
    omega = x**2 * sec_bar + (kappa + _d("4.000001") * x**2) * tau_bar
    terms = {
        "T1": 2 * theta,
        "T2": 2 * x * theta**2,
        "T3": mu * (x**2 * sec_bar + (kappa + _d("5.000001") * x**2) * tau_bar),
        "T4": (kappa + _d("4.000001") * x**2) * (1 + tau_bar / 2),
        "T5": (1 + mu * x * omega) * omega,
        "T6": (kappa + 2 * x**2) * (1 + tau_bar / 2),
        "T7": _d("4.000001") * tau_bar * x**2 * (1 + mu * _d("4.000001") * x**3 * tau_bar),
    }
    terms["Phi"] = sum(terms.values(), iv.mpf(0))
    terms["t_bar"] = t_bar
    terms["tau_bar"] = tau_bar
    return terms


def check_theorem_12(c_e: str = "5.03", subdivisions: int = 400) -> list[Check]:
    """Corollary 7.4 at b = 10^4 and the closed form of Section 7.3."""
    out: list[Check] = []
    x0 = iv.mpf(10) ** (iv.mpf(-4) / 3)
    terms = phi_terms(x0)
    phi = terms["Phi"]
    printed = ("2.89126", "0.19400", "0.20946", "0.80975", "0.10545", "0.80515", "0.00116")
    for index, value in enumerate(printed, start=1):
        term = terms[f"T{index}"]
        out.append(
            Check(
                f"Corollary 7.4: T{index}(x0) rounds to {value}",
                "Corollary 7.4 (vi)",
                bool(abs(term - _d(value)).b <= _d("0.000005").a),
                show(term),
            )
        )
    out += [
        Check(
            "Phi(x0) in [5.0162487, 5.0162488]",
            "Corollary 7.4 and its remark",
            inside(phi, "5.0162487", "5.0162488"),
            show(phi),
        ),
        Check(
            "Phi(x0) <= 5.01625 <= 5.0163",
            "Corollary 7.4 (vi)",
            at_most(phi, "5.01625"),
            show(phi),
        ),
        Check(f"Phi(x0) <= C_E = {c_e}", "Corollary 7.4", at_most(phi, c_e), show(phi)),
        Check(
            "t_bar(x0) <= 0.0672",
            "Corollary 7.4 (iii)",
            at_most(terms["t_bar"], "0.0672"),
            show(terms["t_bar"]),
        ),
        Check(
            "tau_bar(x0) <= 0.1349",
            "Corollary 7.4 (iii)",
            at_most(terms["tau_bar"], "0.1349"),
            show(terms["tau_bar"]),
        ),
    ]
    limit = phi_terms(iv.mpf(0))["Phi"]
    exact_limit = iv.sqrt(_d("6.000002") / _d("0.75")) + iv.mpf(3) / 2
    out.append(
        Check(
            "Phi(0) = sqrt(A/kappa) + 3/2, about 4.3284",
            "Corollary 7.4",
            bool(abs(limit - exact_limit).b < _d("1e-40").a)
            and inside(limit, "4.3284", "4.3285"),
            show(limit),
        )
    )
    supremum = iv.mpf(0)
    for i in range(subdivisions):
        piece = iv.mpf([x0.a * i / subdivisions, x0.b * (i + 1) / subdivisions])
        value = phi_terms(piece)["Phi"]
        if value.b > supremum.b:
            supremum = value
    out.append(
        Check(
            f"sup of Phi over {subdivisions} subintervals of [0, x0] <= 5.0163",
            "remark after Corollary 7.4 (no monotonicity used)",
            at_most(supremum, "5.0163"),
            show(supremum),
        )
    )
    ce = _d(c_e)
    coefficient = iv.mpf(20) / 3 * (iv.mpf(3) / 2) ** (iv.mpf(2) / 5) * ce ** (iv.mpf(3) / 5)
    constant = iv.mpf(8) / 3 * ce * x0
    threshold = 2 * ce / 3 * iv.mpf(10) ** (iv.mpf(20) / 3)
    lam_first = _d("8.001") * (2 * ce / 3) * iv.mpf(10) ** (iv.mpf(-16) / 3)
    lam = lam_first + _d("4.1e-4")
    limit_coefficient = (
        iv.mpf(20) / 3 * (iv.mpf(3) / 2) ** (iv.mpf(2) / 5) * exact_limit ** (iv.mpf(3) / 5)
    )
    out += [
        Check(
            "(20/3)(3/2)^{2/5} 5.03^{3/5} in [20.66740, 20.66741], < 20.668",
            "Section 7.3",
            inside(coefficient, "20.66740", "20.66741") and below(coefficient, "20.668"),
            show(coefficient),
        ),
        Check(
            "(8/3) 5.03 10^{-4/3} in [0.62259, 0.62260], < 0.623",
            "Section 7.3",
            inside(constant, "0.62259", "0.62260") and below(constant, "0.623"),
            show(constant),
        ),
        Check(
            "k0 = 1.6*10^7 >= (2/3) C_E 10^{20/3}, about 1.5565*10^7",
            "Section 7.3",
            at_most(threshold, "1.6e7") and inside(threshold, "1.55645e7", "1.55655e7"),
            show(threshold),
        ),
        Check(
            "8.001 (2/3) C_E b^{-4/3} <= 1.25*10^-4 at b = 10^4, so lambda' < 1",
            "Section 7.3",
            at_most(lam_first, "1.25e-4") and below(lam, "1"),
            show(lam),
        ),
        Check(
            "limit coefficient (20/3)(3/2)^{2/5}(sqrt(A/kappa)+3/2)^{3/5} <= 18.89",
            "Section 7.3",
            at_most(limit_coefficient, "18.89"),
            show(limit_coefficient),
        ),
    ]
    k0 = _d("1.6e7")
    at_k0 = _d("20.668") * k0 ** (iv.mpf(2) / 5) + _d("0.623")
    out.append(
        Check(
            "20.668 k0^{2/5} + 0.623 rounds to 15738.5",
            "Section 1",
            inside(at_k0, "15738.45", "15738.55"),
            show(at_k0),
        )
    )
    columns: list[str] = []
    for k, theorem_12, theorem_14 in TABLE_2:
        value = _d("20.668") * iv.mpf(k) ** (iv.mpf(2) / 5) + _d("0.623")
        root = isqrt(k - 4)
        root += root * root < k - 4
        ok = (
            bool(value.a >= theorem_12 and value.b < theorem_12 + 1)
            and 8 * root - 1 == theorem_14
        )
        if not ok:
            columns.append(f"k = {k}: {show(value)}, 8 ceil(sqrt(k-4)) - 1 = {8 * root - 1}")
    out.append(
        Check(
            "Table 2's columns floor(20.668 k^{2/5} + 0.623) and 8 ceil(sqrt(k-4)) - 1",
            "Table 2",
            not columns,
            "; ".join(columns) or "all five rows",
        )
    )
    return out


def tier_closed_form(c_e, log_b0) -> tuple[Any, Any, Any]:
    """(32/5)(5/3)^{3/8} C_E^{5/8}, (3/5) C_E b0^{8/5} and (12/5) C_E b0^{-2/5}."""
    b0 = iv.mpf(10) ** log_b0
    return (
        iv.mpf(32) / 5 * (iv.mpf(5) / 3) ** (iv.mpf(3) / 8) * c_e ** (iv.mpf(5) / 8),
        iv.mpf(3) / 5 * c_e * b0 ** (iv.mpf(8) / 5),
        iv.mpf(12) / 5 * c_e * b0 ** (iv.mpf(-2) / 5),
    )


def check_theorem_11_v10(c_e: str = "15.54", psi_sup: str = "96.477") -> list[Check]:
    """Section 8.4 of version 1.0 with b0 = 10^16."""
    coefficient, threshold, constant = tier_closed_form(_d(c_e), iv.mpf(16))
    certified = (
        _d(psi_sup)
        * iv.mpf(12) ** (iv.mpf(-3) / 4)
        * (1 + _d("60.000012") * iv.mpf(10) ** (iv.mpf(-64) / 5)) ** (iv.mpf(3) / 4)
    )
    cross = (_d("43.06") / _d("20.668")) ** 40
    k1 = _d("4e26")
    at_k1 = (_d("43.06") * k1 ** (iv.mpf(3) / 8), _d("20.668") * k1 ** (iv.mpf(2) / 5))
    return [
        Check(
            f"(32/5)(5/3)^{{3/8}} {c_e}^{{5/8}} < 43.06",
            "Theorem 1.1 (v1.0)",
            below(coefficient, "43.06"),
            show(coefficient),
        ),
        Check(
            "(32/5)(5/3)^{3/8} is about 7.751277",
            "Section 8.4 (v1.1 fix)",
            inside(
                iv.mpf(32) / 5 * (iv.mpf(5) / 3) ** (iv.mpf(3) / 8), "7.7512765", "7.7512775"
            ),
            show(iv.mpf(32) / 5 * (iv.mpf(5) / 3) ** (iv.mpf(3) / 8)),
        ),
        Check(
            f"(12/5) {c_e} 10^{{-32/5}} <= 2*10^-5",
            "Theorem 1.1 (v1.0)",
            at_most(constant, "2e-5"),
            show(constant),
        ),
        Check(
            f"(3/5) {c_e} 10^{{128/5}} <= k1 = 4*10^26",
            "Theorem 1.1 (v1.0)",
            at_most(threshold, "4e26"),
            show(threshold),
        ),
        Check(
            f"C_E from the covering's Psi_sup = {psi_sup} (reported input) <= 14.964 <= {c_e}",
            "Corollary 8.3 and cert3e.py",
            at_most(certified, "14.964"),
            show(certified),
        ),
        Check(
            "43.06 k^{3/8} < 20.668 k^{2/5} from about k = 5.6*10^12",
            "Section 1",
            inside(cross, "5.55e12", "5.65e12"),
            show(cross),
        ),
        Check(
            "at k = 4*10^26 the closed forms are about 4.07*10^11 and 9.04*10^11",
            "Section 1",
            inside(at_k1[0], "4.065e11", "4.075e11")
            and inside(at_k1[1], "9.035e11", "9.045e11"),
            f"{show(at_k1[0])}, {show(at_k1[1])}",
        ),
    ]


def check_tiers(tiers: Sequence[Tier] = TIERS) -> list[Check]:
    """The stated inequalities of version 1.1's Theorem 1.1 for every tier of Table 1."""
    out: list[Check] = []
    for tier in tiers:
        coefficient, threshold, constant = tier_closed_form(_d(tier.c_e), _d(tier.log_b0))
        cross = (_d(tier.c) / _d("20.668")) ** 40
        column = _d(tier.better_from)
        k_i = _d(tier.k)
        column_ok = bool(column.a >= k_i.b and column.a >= cross.b) and bool(
            column.a == k_i.a or column.b <= (cross * _d("1.01")).a
        )
        out += [
            Check(
                f"{tier.name}: C_i = {tier.c} >= (32/5)(5/3)^{{3/8}} C_E^{{5/8}}",
                "Theorem 1.1 (v1.1)",
                dominates(_d(tier.c), coefficient),
                show(coefficient),
            ),
            Check(
                f"{tier.name}: k_i = {tier.k} >= (3/5) C_E b0^{{8/5}}",
                "Theorem 1.1 (v1.1)",
                dominates(k_i, threshold),
                show(threshold),
            ),
            Check(
                f"{tier.name}: a_i = {tier.a} >= (12/5) C_E b0^{{-2/5}}, and a_i < 0.623",
                "Theorem 1.1 (v1.1), Table 1",
                dominates(_d(tier.a), constant) and below(_d(tier.a), "0.623"),
                show(constant),
            ),
            Check(
                f"{tier.name}: last column {tier.better_from} = "
                "max(k_i, (C_i/20.668)^40 rounded up)",
                "Table 1 caption",
                column_ok,
                show(cross),
            ),
        ]
    smallest = min(tiers, key=lambda tier: float(tier.better_from))
    out.append(
        Check(
            "the k^{3/8} tiers give a smaller bound than Theorem 1.2 from k = 2.48*10^12",
            "Section 1, 'Which bound to use'",
            smallest.better_from == "2.48e12",
            f"{smallest.name} from {smallest.better_from}",
        )
    )
    return out


def check_all(subdivisions: int = 400) -> tuple[Check, ...]:
    iv.dps = DIGITS
    return (
        *check_theorem_12(subdivisions=subdivisions),
        *check_theorem_11_v10(),
        *check_tiers(),
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("--subdivisions", type=int, default=400)
    args = parser.parse_args(argv)
    checks = check_all(args.subdivisions)
    passed = all(check.holds for check in checks)
    report = {
        "passed": passed,
        "digits": DIGITS,
        "tiers": [asdict(tier) for tier in TIERS],
        "checks": [asdict(check) for check in checks],
    }
    print(json.dumps(report, indent=1))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
