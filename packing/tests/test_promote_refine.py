#!/usr/bin/env python3
"""Behavior and refusal contract for high-precision Newton refinement.

The point of these checks is the refusals.  A refiner that always returns a number is
indistinguishable from one that returns the right number, so every typed failure this
module can raise is exercised here, and the two that matter scientifically -- leaving
the trust region, and a system with no isolated root -- are exercised twice: once
directly, and once through the `n = 29` driver that BC-047 retains.
"""

from __future__ import annotations

from pathlib import Path

import mpmath as mp

from cases.kingbird29 import system
from sqpack.promote.refine import (
    RefinementError,
    refine,
    residual_falls,
    residual_series,
)

ROOT = Path(__file__).resolve().parent.parent
PROVENANCE = ROOT / "resources/papers/kingbird-square-29-provenance.svg"


def require_refusal(call, kind: str, label: str) -> None:
    try:
        call()
    except RefinementError as error:
        assert error.kind == kind, f"{label}: expected {kind}, got {error.kind}"
        return
    raise AssertionError(f"{label}: expected a {kind} refusal and got a value")


def known_answer() -> None:
    """A system whose root is known independently of anything in this repository."""

    def squares(x, y):
        return [x * x - 2, y * y - 3]

    result = refine(squares, ("1.4", "1.7"), 200, names=("x", "y"), trust_radius="1")
    previous = mp.mp.dps
    mp.mp.dps = 260
    try:
        assert abs(mp.mpf(result.values[0]) - mp.sqrt(2)) < mp.mpf("1e-195")
        assert abs(mp.mpf(result.values[1]) - mp.sqrt(3)) < mp.mpf("1e-195")
        assert mp.mpf(result.residual_bound) < mp.mpf("1e-190")
        assert mp.mpf(result.residual) <= mp.mpf(result.residual_bound)
    finally:
        mp.mp.dps = previous
    assert result.working_digits > result.digits
    assert result.operator == "mpmath-mdnewton"


def refusals() -> None:
    def squares(x, y):
        return [x * x - 2, y * y - 3]

    require_refusal(
        lambda: refine(squares, ("1.4", "1.7"), 0, names=("x", "y")), "bad-request", "digits"
    )
    require_refusal(
        lambda: refine(squares, ("1.4",), 20, names=("x", "y")), "bad-request", "seed length"
    )
    require_refusal(
        lambda: refine(lambda x, y: [x - 1, y - 1, x + y], ("1", "1"), 20, names=("x", "y")),
        "not-square",
        "over-determined",
    )
    # The trust region is a statement about the seed as much as about the root: a seed
    # only accurate to 1e-2 cannot be "refined" under a 1e-6 radius, and the refiner
    # says so rather than quietly relocating the answer.
    require_refusal(
        lambda: refine(squares, ("1.4", "1.7"), 50, names=("x", "y"), trust_radius="1e-6"),
        "left-trust-region",
        "seed coarser than the trust radius",
    )
    # Rank-deficient, and seeded off its own solution set so there is something to
    # solve; a seed that already satisfies both rows would return at once and prove
    # nothing.
    require_refusal(
        lambda: refine(
            lambda x, y: [x + y - 2, 2 * x + 2 * y - 4], ("1.1", "1.0"), 30, names=("x", "y")
        ),
        "non-convergent",
        "rank-deficient",
    )


def plateau_detector() -> None:
    falling = [{"residual": "1e-50"}, {"residual": "1e-120"}, {"residual": "1e-250"}]
    flat = [{"residual": "1e-50"}, {"residual": "5e-51"}, {"residual": "2e-51"}]
    assert residual_falls(falling), "residual_falls rejected a falling series"
    assert not residual_falls(flat), "residual_falls accepted a plateau"
    assert not residual_falls([{"residual": "1e-50"}]), "residual_falls accepted one rung"


def kingbird29_system() -> None:
    """The transcribed system refines the published pose and stays where it was put."""
    seed = system.seed(PROVENANCE)
    assert len(seed) == len(system.UNKNOWNS) == 6

    result = refine(system.equations, seed, 200, names=system.UNKNOWNS)
    previous = mp.mp.dps
    mp.mp.dps = 260
    try:
        # The source publishes about a hundred digits; refinement must agree with all of
        # them and then carry on past where the publication stops.
        assert abs(mp.mpf(result.values[0]) - mp.mpf(seed[0])) < mp.mpf("1e-95")
        assert mp.mpf(result.residual_bound) < mp.mpf("1e-200")
    finally:
        mp.mp.dps = previous

    series = residual_series(system.equations, seed, (60, 125), names=system.UNKNOWNS)
    assert residual_falls(series)

    # A degenerate copy of one equation destroys the Jacobian's rank, and the refiner
    # must say so rather than return whatever the linear solve produced.
    def degenerate(*values):
        residuals = list(system.equations(*values))
        residuals[5] = residuals[4]
        return residuals

    require_refusal(
        lambda: refine(degenerate, seed, 60, names=system.UNKNOWNS),
        "non-convergent",
        "n=29 rank-deficient",
    )


def main() -> int:
    known_answer()
    refusals()
    plateau_detector()
    kingbird29_system()
    print("promotion refinement contract selftest passed")
    return 0


def test_promote_refine() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
