"""Independent interval arithmetic for Ryu's quarter/cube explicit consequences.

The formulas come from the retained primary texts, not their executable checkers.
Verdicts remain conditional on the reviewed geometric lemmas and their constant
ceilings. This command neither replays box labels nor proves those premises.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from typing import Any

from mpmath.ctx_iv import MPIntervalContext

from cases.asymptotic.ryu_k2_minus_c_constants import Check


@dataclass(frozen=True)
class QuarterRow:
    overlap: int
    c0: str
    c1: str
    y0: int
    epsilon: str
    omega: str
    threshold: int


@dataclass(frozen=True)
class CubeRow:
    case: int
    overlap: int
    exponent_denominator: int
    gamma: str
    b: str
    start: int
    end: int | None
    tau0: str
    tau1: str
    nu: str
    left_floor: str
    right_cap: str


QUARTER_ROWS = (
    QuarterRow(9, "0.3078", "0.2754", 42108000000, "5.8e-6", "1.7e-5", 4620000000000),
    QuarterRow(13, "0.3674", "0.3012", 60000000000, "5e-6", "1.4e-5", 21700000000000),
)
CUBE_ROWS = (
    CubeRow(
        1,
        9,
        2,
        "0.0001",
        "0.0012",
        10**8,
        2500000000000000,
        "0.0205",
        "0.02",
        "0.001",
        "0.95899994",
        "0.87266009",
    ),
    CubeRow(
        2,
        9,
        2,
        "0.00007",
        "0.0012",
        2500000000000000,
        350000000000000000,
        "0.1675",
        "0.167",
        "0.001",
        "0.66499999",
        "0.61085501",
    ),
    CubeRow(
        3,
        9,
        3,
        "0.06",
        "1",
        350000000000000000,
        None,
        "0.1675",
        "0.167",
        "0.01",
        "0.66499999",
        "0.62871651",
    ),
    CubeRow(
        4,
        9,
        3,
        "0.0625",
        "1",
        10**21,
        None,
        "0.1668",
        "0.1667",
        "0.005",
        "0.66639999",
        "0.66296281",
    ),
    CubeRow(
        5,
        13,
        2,
        "0.000085",
        "0.0012",
        10**8,
        2400000000000000,
        "0.0205",
        "0.02",
        "0.001",
        "0.95899994",
        "0.89044495",
    ),
    CubeRow(
        6,
        13,
        2,
        "0.00006",
        "0.0012",
        2400000000000000,
        339000000000000000,
        "0.1675",
        "0.167",
        "0.001",
        "0.66499999",
        "0.62854332",
    ),
    CubeRow(
        7,
        13,
        3,
        "0.05",
        "1",
        339000000000000000,
        None,
        "0.1675",
        "0.167",
        "0.01",
        "0.66499999",
        "0.63009391",
    ),
    CubeRow(
        8,
        13,
        3,
        "0.052",
        "1",
        10**21,
        None,
        "0.1668",
        "0.1667",
        "0.005",
        "0.66639999",
        "0.66284161",
    ),
)
# Primary Q Section 10.2 and C Section 2; all are geometric upper premises.
GEOMETRIC = {
    9: ("10.6067", "10.6068", "56.2501", "318.20", "56.2501", "754.8"),
    13: ("12.7476", "12.7476", "81.2502", "459.7", "81.26", "1090.3"),
}


def interval_max(ctx: Any, left: Any, right: Any) -> Any:
    """Enclose the maximum, including overlapping argument intervals."""
    return ctx.mpf([max(left.a, right.a), max(left.b, right.b)])


def check_constants(
    *,
    quarter_rows: tuple[QuarterRow, ...] = QUARTER_ROWS,
    cube_rows: tuple[CubeRow, ...] = CUBE_ROWS,
    quarter_claim: str = "0.1",
    quarter_asymptotic: tuple[str, str] = ("0.1696524", "0.1411593"),
    cube_asymptotic: tuple[str, str] = ("0.062853", "0.052297"),
) -> tuple[Check, ...]:
    """Decide all published ranges, outward table bounds and asymptotic floors."""
    ctx: Any = MPIntervalContext()
    ctx.dps = 60

    def iv(value: str | int | Fraction) -> Any:
        fraction = Fraction(value)
        return ctx.mpf(fraction.numerator) / ctx.mpf(fraction.denominator)

    def less(left: Any, right: Any) -> bool:
        return bool((left - right).b < 0)

    def power(value: Any, numerator: int, denominator: int) -> Any:
        return ctx.power(value, iv(Fraction(numerator, denominator)))

    checks: list[Check] = []

    def record(name: str, source: str, value: Any, holds: Any) -> None:
        checks.append(Check(name, source, holds, str(value)))

    claim = Fraction(quarter_claim)
    if claim <= 0 or any(Fraction(v) <= 0 for v in (*quarter_asymptotic, *cube_asymptotic)):
        raise ValueError("claimed coefficients must be positive")
    if len(quarter_asymptotic) != 2 or len(cube_asymptotic) != 2:
        raise ValueError("both overlap routes need an asymptotic floor")
    record(
        "quarter roster",
        "Q Theorems A/A13",
        len(quarter_rows),
        tuple(row.overlap for row in quarter_rows) == (9, 13),
    )
    record(
        "cube roster",
        "C Table 1",
        len(cube_rows),
        tuple(
            (row.case, row.overlap, row.exponent_denominator, row.start, row.end)
            for row in cube_rows
        )
        == tuple(
            (r.case, r.overlap, r.exponent_denominator, r.start, r.end) for r in CUBE_ROWS
        ),
    )
    delta, beta_bar = iv("1e-5"), iv("1.5e-6")
    for row in quarter_rows:
        if row.overlap not in GEOMETRIC or row.y0 < 1 or row.threshold < 14:
            raise ValueError("quarter overlap and integer scale domain are invalid")
        if not isinstance(row.y0, int) or not isinstance(row.threshold, int):
            raise TypeError("quarter scales must be integers")
        c0, c1, epsilon, omega = map(Fraction, (row.c0, row.c1, row.epsilon, row.omega))
        if c0 <= 0 or c1 <= 0 or not 0 < epsilon < 1 or not 0 < omega < Fraction(1, 2):
            raise ValueError("positive quarter parameters and physical fractions are required")
        c0i, c1i, ei, oi = map(iv, (c0, c1, epsilon, omega))
        y0, k0 = iv(row.y0), iv(row.threshold)
        a, aprime = map(iv, GEOMETRIC[row.overlap][:2])
        cl = iv("1.0000002")
        alpha = c0i / ctx.sqrt(y0)
        beta = c1i / power(y0, 3, 4)
        bstar = c1i / power((1 - ei) * y0, 3, 4)
        w0 = (
            iv("0.50001") * c0i**2 * (1 + iv("1.0001") / y0)
            + delta
            + iv("1.0001") * bstar
            + iv("1e-12")
        )
        h0 = 1 - 2 * w0
        t = power(1 - ei, 3, 4)
        invf = 4 * t * (1 - t) / (3 * ei * (1 + iv("2.0002") / (ei * y0)))
        gamma = iv("1.00002") * (
            2 * c1i * a / ctx.sqrt(y0) + iv("0.8") * c1i**2 / (delta * power(y0, 5, 4))
        )
        denominator = (
            1 / (oi * power(y0, 3, 4))
            + a / (2 * c1i)
            + 2 * c1i * (aprime + alpha * cl / delta) / (c0i * invf)
            + gamma
        )
        kw = iv("1.000001") * c0i**2 * 4 * c1i / (c0i * invf)
        y1 = k0 / 2 - 3
        lh = 8 * h0 * (power((1 - ei) * y1, 1, 4) - power(y0 + 1, 1, 4))
        psi = ((1 - oi) * lh - kw * (ctx.log(y1 / y0) + 2 / y0)) / denominator
        d1 = h0 * (1 - oi) * power(1 - ei, 1, 4) / denominator - iv(claim) / (
            4 * power(iv(2), 3, 4)
        )
        prefix = f"quarter K{row.overlap} "
        source = "Q domains C0-C7 / Sections 10-11"
        conditions = (
            ("alpha cap", alpha, less(alpha, beta_bar)),
            ("beta cap", beta, less(beta, beta_bar)),
            ("alpha small-angle domain", alpha, less(alpha, iv("0.001"))),
            ("beta star small-angle domain", bstar, less(bstar, iv("0.0001"))),
            ("C3", bstar, less(c1i / power(1 - ei, 3, 4), c0i * power(y0, 1, 4))),
            ("positive height", h0, less(iv(0), h0)),
            ("inclination geometry", delta, less(delta, ctx.cos(2 * alpha) / 2)),
            ("scale window", y1, less(y0 + 1, (1 - ei) * y1)),
            ("inverse factor", invf, less(iv(0), invf) and less(invf, iv(1))),
            (
                "threshold margin",
                psi - iv(claim) * power(k0, 1, 4),
                less(iv(claim) * power(k0, 1, 4), psi),
            ),
            ("positive derivative", d1, less(iv(0), d1)),
            (
                "derivative loss",
                power(y1, 1, 4) * d1 - kw / (2 * denominator),
                less(kw / (2 * denominator), power(y1, 1, 4) * d1),
            ),
        )
        for name, value, holds in conditions:
            record(prefix + name, source, value, holds)
    for row in cube_rows:
        if (
            row.overlap not in GEOMETRIC
            or row.exponent_denominator not in (2, 3)
            or not isinstance(row.start, int)
            or row.start < 14
            or (row.end is not None and (not isinstance(row.end, int) or row.end < row.start))
        ):
            raise ValueError("cube overlap, exponent and integer endpoint domain are invalid")
        gamma, b, tau0, tau1, nu = map(Fraction, (row.gamma, row.b, row.tau0, row.tau1, row.nu))
        if gamma <= 0 or b <= 0 or not 0 < nu < Fraction(1, 2) or tau1 <= 0:
            raise ValueError("positive cube parameters and physical fractions are required")
        p = Fraction(1, row.exponent_denominator)
        gi, bi, t0, t1, ni = map(iv, (gamma, b, tau0, tau1, nu))
        a, ap, s, cm, cg, ce = map(iv, GEOMETRIC[row.overlap])
        b1 = (a / 2 + 2 * beta_bar) / ctx.cos(beta_bar)
        l1 = (1 + s * delta**2) / delta + (cm + ce + cg) * delta + 4 * b1
        k = iv(row.start)
        waste = gi * power(k, p.numerator, p.denominator)
        beta = bi * power(k, p.numerator - p.denominator, p.denominator)
        excess = iv("0.50001") * beta * (a + beta / delta) * waste
        first, second = 1 / beta_bar, b1 * waste / (2 * t1)
        chosen = interval_max(ctx, first, second)
        length = ap * waste * chosen + l1 * waste + 4 * delta
        height = 1 - ni - excess
        prefix = f"cube case{row.case} "
        source = "C Proposition 3.1 / Table 1"
        record(
            prefix + "tau ordering",
            "C domain (D)",
            t0 - t1,
            delta < t1 and less(t1, t0) and less(t0, iv(Fraction(1, 2))),
        )
        record(prefix + "beta cap", source, beta, less(beta, beta_bar))
        record(
            prefix + "height room",
            source,
            t0 - iv("1.0001") * beta,
            less(t1, t0 - iv("1.0001") * beta),
        )
        record(prefix + "positive denominator", source, height, less(iv(0), height))
        if not less(iv(0), height):
            continue
        rhs = waste / (ni * k) + a * gi / (2 * bi) + beta * length / (2 * height)
        lhs = (1 - 2 * t0) * (1 - 6 / k)
        record(prefix + "main margin", source, lhs - rhs, less(rhs, lhs))
        record(prefix + "printed lower bound", "C Table 1", lhs, less(iv(row.left_floor), lhs))
        record(prefix + "printed upper bound", "C Table 1", rhs, less(rhs, iv(row.right_cap)))
        if p == Fraction(1, 2):
            record(
                prefix + "finite linear branch",
                source,
                row.end,
                row.end is not None
                and less(gi * ctx.sqrt(iv(row.end)), 2 * t1 / (b1 * beta_bar)),
            )
        else:
            record(
                prefix + "nonincreasing normalized exponents",
                source,
                (2 * p - 1, 3 * p - 1),
                2 * p - 1 <= 0 and 3 * p - 1 <= 0,
            )
    for index, overlap in enumerate((9, 13)):
        a = 4 * ctx.sqrt(iv(overlap) / iv("0.32")) / (2 - iv("3e-6"))
        ap = a / ctx.cos(beta_bar) + iv("1e-8")
        lam = 2 * delta + iv("2e-12")
        quarter_limit = (
            16
            * power(iv(2), -1, 4)
            * power(1 - lam, 5, 4)
            / (5 * power(iv("5.0001"), 1, 4) * ctx.sqrt(a * ap))
        )
        a_upper, ap_upper, s_upper, cm_upper, cg_upper, ce_upper = map(iv, GEOMETRIC[overlap])
        pair_ceiling = iv("41.933")  # Q Proposition 5.10's reviewed geometric ceiling.
        s_exact = (1 + iv("1e-11")) * 4 * iv(overlap) / (iv("0.32") * (2 - iv("3e-6")))
        geometric_values = (
            ("A", a, a_upper),
            ("A prime", ap, ap_upper),
            (
                "C Lambda",
                1 + iv("1185.6" if overlap == 9 else "1712.6") * delta**2,
                iv("1.0000002"),
            ),
            ("S", s_exact, s_upper),
            ("CM", 4 * s_exact / ctx.cos(ctx.pi / 4 + beta_bar), cm_upper),
            ("CG", s_exact / ctx.cos(beta_bar), cg_upper),
            ("CE", 2 * overlap * pair_ceiling, ce_upper),
        )
        for name, value, ceiling in geometric_values:
            record(
                f"K{overlap} geometric {name} ceiling",
                "Q Sections 5, 7-8 / C Section 2",
                value,
                less(value, ceiling),
            )
        b1 = (a_upper / 2 + 2 * beta_bar) / ctx.cos(beta_bar)
        cube_limit = power(iv(Fraction(4, 27)) / (a_upper * ap_upper * b1), 1, 3)
        record(
            f"quarter K{overlap} asymptotic floor",
            "Q Section 11",
            quarter_limit,
            less(iv(quarter_asymptotic[index]), quarter_limit),
        )
        record(
            f"cube K{overlap} asymptotic floor",
            "C Section 4",
            cube_limit,
            less(iv(cube_asymptotic[index]), cube_limit),
        )
    return tuple(checks)


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    checks = check_constants()
    print(
        json.dumps(
            {
                "passed": all(c.holds for c in checks),
                "parameters": {
                    "quarter": [asdict(r) for r in QUARTER_ROWS],
                    "cube": [asdict(r) for r in CUBE_ROWS],
                },
                "checks": [asdict(c) for c in checks],
            },
            indent=2,
        )
    )
    return 0 if all(c.holds for c in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
