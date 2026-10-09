"""Certify the finite comparison gap in Ryu v1.2 Lemma 4.10's circular count.

This is a new arithmetic route derived from paper/paper.tex and code/bnb.py:max_points,
with the closed-cell convention of verify_leaves2.py. It imports no upstream code and
runs no box checker. All 9 * 2881 comparisons are enclosed independently of a cell mask.
The implementation uses exact binary-rational lifts and 60-digit intervals, with a
conservative error envelope rather than the source's tighter claimed 1e-14 bound.

The mathematical argument is conditional on the reviewed operation model: binary64
round-to-nearest, 1440 cells, positions formed by restarting at a cell lower end or
adding the separation, at most eight accepted additions, and the stated comparison
slacks. A ninth step is refused by the same certified gap; the empty/full-circle cases
are separate. The finite endpoints and operation counts are explained in the review.
Current-host pi, DPHI and G0_SAFE are printed as exact hexadecimal binary64 values.
Historical receipts did not record their libm-derived G0_SAFE, so this command does not
certify an unobserved historical host's transcendental output or replay its box labels.

Run from packing with project Python: python -m cases.asymptotic.ryu_k2_minus_c_float_gap
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import cache
from typing import Any

from mpmath.ctx_iv import MPIntervalContext

from cases.asymptotic.ryu_k2_minus_c_constants import Check

CELLS = 1440
MAX_STEPS = 9
MAX_MULTIPLE = 2 * CELLS
# Every basic operation has result magnitude < 16, so half an ulp is at most 2^-50.
ROUNDING_UNIT = Fraction(1, 2**50)


@dataclass(frozen=True)
class GapAudit:
    """The complete finite-domain decision and its explicit runtime boundary."""

    checks: tuple[Check, ...]
    comparisons: int
    closest: tuple[int, int]
    gap_interval: str
    binary_constants: dict[str, str]

    @property
    def passed(self) -> bool:
        return all(check.holds for check in self.checks)


def _interval(context: Any, value: Fraction | int) -> Any:
    rational = Fraction(value)
    return context.mpf(rational.numerator) / context.mpf(rational.denominator)


def _below(left: Any, right: Any) -> bool:
    return bool((left - right).b < 0)


@cache
def _geometry() -> tuple[Any, Any, Any, Any, Any, tuple[int, int], int]:
    # A private context makes this route independent of ambient mpmath precision.
    context: Any = MPIntervalContext()
    context.dps = 60
    lam = context.sqrt(2) + _interval(context, Fraction("0.0001"))
    # acos(1 - 1/(2 Lambda^2)) = 2 atan2(1, sqrt(4 Lambda^2 - 1)).
    gamma = 2 * context.atan2(context.mpf(1), context.sqrt(4 * lam * lam - 1))
    step = context.pi / 720
    lower = upper = None
    closest = (0, 0)
    comparisons = 0
    for j in range(1, MAX_STEPS + 1):
        for m in range(MAX_MULTIPLE + 1):
            distance = abs(j * gamma - m * step)
            comparisons += 1
            if lower is None or distance.a < lower:
                lower = distance.a
                closest = (j, m)
            if upper is None or distance.b < upper:
                upper = distance.b
    return context, gamma, step, lower, upper, closest, comparisons


def check_float_gap(
    *,
    gap_floor: str = "0.00004",
    roundoff_cap: str = "1e-12",
    separation_deficit: str = "1e-12",
    closing_slack: str = "1e-12",
    separation_hex: str | None = None,
) -> GapAudit:
    """Certify every comparison under explicit arithmetic and runtime premises.

    Overrides are falsifiable controls for the gap, cumulative error and separation;
    they do not change the retained source or supply historical runtime constants.
    """
    floor, rounding_cap, deficit, closing = map(
        Fraction, (gap_floor, roundoff_cap, separation_deficit, closing_slack)
    )
    if any(value <= 0 for value in (floor, rounding_cap, deficit, closing)):
        raise ValueError("gap, roundoff, separation deficit and closing slack must be positive")
    context, gamma, step, lower, upper, closest, comparisons = _geometry()
    dphi_float = 2 * math.pi / CELLS
    lam_float = math.sqrt(2) + 1e-4
    separation = (
        math.acos(1 - 1 / (2 * lam_float**2)) - float(deficit)
        if separation_hex is None
        else float.fromhex(separation_hex)
    )
    if not math.isfinite(separation) or separation <= 0:
        raise ValueError("a finite positive binary64 separation is required")
    binary_pi, binary_step, binary_sep = map(Fraction, (math.pi, dphi_float, separation))
    cell_slack = Fraction(1e-15)
    binary_closing = Fraction(float(closing))
    checks: list[Check] = []

    def record(name: str, value: Any, *, holds: bool) -> None:
        checks.append(Check(name, "v1.2 Lemma 4.10 / max_points", holds, str(value)))

    record(
        "binary64 round-to-nearest runtime",
        (
            f"radix={sys.float_info.radix}; mantissa={sys.float_info.mant_dig}; "
            f"rounds={sys.float_info.rounds}"
        ),
        holds=sys.float_info.radix == 2
        and sys.float_info.mant_dig == 53
        and sys.float_info.rounds == 1,
    )
    record(
        "complete finite comparison domain",
        comparisons,
        holds=comparisons == 25929
        and _below(context.mpf(0), gamma)
        and _below(9 * gamma, 4 * context.pi)
        and _below(_interval(context, floor), gamma)
        and _below(_interval(context, floor), 4 * context.pi - 9 * gamma),
    )
    record(
        "every finite angular difference exceeds gap floor",
        f"minimum in [{lower}, {upper}], at {closest}",
        holds=_below(_interval(context, floor), lower),
    )
    record(
        "full circle admits eight and refuses nine separations",
        2 * context.pi / gamma,
        holds=_below(8 * gamma, 2 * context.pi) and _below(2 * context.pi, 9 * gamma),
    )
    step_error = abs(_interval(context, binary_step) - step)
    circle_error = abs(_interval(context, 2 * binary_pi) - 2 * context.pi)
    separation_error = abs(_interval(context, binary_sep + deficit) - gamma)
    record(
        "binary separation is conservative and within 1e-15 of gamma minus deficit",
        separation_error,
        holds=_below(_interval(context, binary_sep), gamma)
        and _below(separation_error, _interval(context, Fraction("1e-15"))),
    )
    record(
        "binary cell width differs by less than 1e-18",
        step_error,
        holds=_below(step_error, _interval(context, Fraction("1e-18"))),
    )
    # fl(fl(s*d) + fl(off*d)) + d has s+off+1 <= 2879 and four roundings.
    # Certified max(hi[k], lo[k+1]) has <= 1440 widths/two roundings;
    # its final end is extended to exact 2pi. Thus this larger bound covers both.
    endpoint_error = 2 * CELLS * step_error + _interval(context, 4 * ROUNDING_UNIT)
    # Two endpoints, the unwrapped circle and sixteen additional roundings cover
    # <= nine position additions and the target, endpoint and closing comparisons.
    roundoff = 2 * endpoint_error + circle_error + _interval(context, 16 * ROUNDING_UNIT)
    record(
        "all endpoint and basic-operation errors fit roundoff cap",
        roundoff,
        holds=_below(roundoff, _interval(context, rounding_cap)),
    )
    # A closing comparison includes at most nine gamma terms in total, including
    # the subtracted final separation. Exact lifts also retain both source slacks.
    total_error = (
        _interval(context, rounding_cap + MAX_STEPS * deficit + binary_closing + cell_slack)
        + MAX_STEPS * separation_error
    )
    record(
        "combined error and slacks are below every comparison gap",
        total_error,
        holds=_below(total_error, _interval(context, floor)),
    )
    record(
        "off-loop boundary stays a full cell below one revolution",
        step,
        holds=_below(total_error, step),
    )
    record(
        "all unwrapped operation results have magnitude below 14",
        4 * context.pi + step + total_error,
        holds=_below(4 * context.pi + step + total_error, context.mpf(14)),
    )
    full_circle_value = 2 * math.pi / separation + 1e-12
    record(
        "actual full-circle binary floor agrees with exact eight",
        full_circle_value.hex(),
        holds=Fraction(8) <= Fraction(full_circle_value) < Fraction(9),
    )
    return GapAudit(
        tuple(checks),
        comparisons,
        closest,
        f"[{lower}, {upper}]",
        {
            "pi": math.pi.hex(),
            "dphi": dphi_float.hex(),
            "g0_safe": separation.hex(),
            "cell_slack": float(cell_slack).hex(),
            "closing_slack": float(binary_closing).hex(),
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.parse_args()
    audit = check_float_gap()
    print(json.dumps(asdict(audit), indent=2))
    return 0 if audit.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
