"""Newton refinement of a closed system, at a precision the caller declares.

This step manufactures precision and makes **no algebraic claim**.  It exists because
reading digits off a serialized source does not supply enough of them: a probe recorded
in X-004 ran integer relation directly on the serialized `n = 29` side and got
candidate relations at almost every degree from eight to twenty-one, because roughly a
hundred available digits cannot separate a degree-eight coincidence from a minimal
polynomial.  Precision has to come from the system, and the system is what a caller
brings here.

Three things are reported rather than assumed:

- **the residual**, measured as `max |f_i(x)|` at the refined point, and widened to a
  `residual_bound` that allows for evaluation error at the working precision;
- **the movement** from the seed, because a Newton iteration that converges to some
  *other* root has not refined the pose it was given;
- **how the residual falls with precision**, through :func:`residual_series`, because a
  residual that plateaus is evidence of a wrong system and must be reported as that
  rather than worked around.

Every failure is typed.  :class:`RefinementError` carries a `kind` a caller can branch
on, so a refusal stays a refusal instead of becoming a silently returned number.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

import mpmath as mp

# Newton is evaluated above the precision it reports, so the reported digits are not
# the ones carrying the iteration's own rounding error.
DEFAULT_GUARD_DIGITS = 40

System = Callable[..., Sequence]


class RefinementError(ValueError):
    """A typed refinement failure suitable for both human and machine callers."""

    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = kind


@dataclass(frozen=True)
class Refinement:
    """One refined solution, with everything a caller needs to distrust it."""

    names: tuple[str, ...]
    values: tuple[str, ...]
    digits: int
    working_digits: int
    seed_residual: str
    residual: str
    residual_bound: str
    max_seed_movement: str
    operator: str


def _decimal(value, digits: int) -> str:
    return str(mp.nstr(value, n=digits, strip_zeros=False))


def _max_abs(values: Sequence) -> mp.mpf:
    return max(abs(value) for value in values)


def refine(
    system: System,
    seed: Sequence[str],
    digits: int,
    *,
    names: Sequence[str],
    trust_radius: str = "1e-6",
    guard_digits: int = DEFAULT_GUARD_DIGITS,
) -> Refinement:
    """Refine `seed` to a root of `system` at `digits` decimal digits.

    `system` takes one argument per unknown and returns one residual per equation.
    `trust_radius` bounds how far the refined point may move from its seed; a Newton
    iteration that runs off to a different root is a typed refusal here, not a result,
    because the caller asked to sharpen *this* pose.
    """
    if digits < 1:
        raise RefinementError("bad-request", f"digits must be positive, got {digits}")
    if len(seed) != len(names):
        raise RefinementError(
            "bad-request", f"{len(seed)} seed values against {len(names)} names"
        )

    working = digits + guard_digits
    previous = mp.mp.dps
    mp.mp.dps = working
    try:
        start = [mp.mpf(value) for value in seed]
        residuals = system(*start)
        if len(residuals) != len(start):
            raise RefinementError(
                "not-square",
                f"{len(residuals)} equations against {len(start)} unknowns; "
                "Newton refinement needs a square system",
            )
        seed_residual = _max_abs(residuals)
        tolerance = mp.mpf(10) ** (-2 * digits)
        try:
            solution = mp.findroot(system, tuple(start), tol=tolerance)
        except (ValueError, ZeroDivisionError, mp.libmp.libhyper.NoConvergence) as error:
            raise RefinementError(
                "non-convergent",
                f"Newton did not reach {digits} digits from the supplied seed: {error}",
            ) from error
        refined = [solution[index] for index in range(len(start))]
        movement = _max_abs(
            [value - anchor for value, anchor in zip(refined, start, strict=True)]
        )
        radius = mp.mpf(trust_radius)
        if movement > radius:
            raise RefinementError(
                "left-trust-region",
                f"the refined point moved {mp.nstr(movement, 6)} from its seed, past the "
                f"declared trust radius {trust_radius}, so it is not a refinement of the "
                "pose supplied; whether it is a different root or the same one reached "
                "from far away is not decided here",
            )
        residual = _max_abs(system(*refined))
        # The measured residual is itself evaluated in floating point, so the reported
        # bound allows one working-precision ulp of the largest term.
        bound = residual + mp.mpf(10) ** (-(working - 1))
        return Refinement(
            names=tuple(names),
            values=tuple(_decimal(value, digits) for value in refined),
            digits=digits,
            working_digits=working,
            seed_residual=_decimal(seed_residual, 6),
            residual=_decimal(residual, 6),
            residual_bound=_decimal(bound, 6),
            max_seed_movement=_decimal(movement, 6),
            operator="mpmath-mdnewton",
        )
    finally:
        mp.mp.dps = previous


def residual_series(
    system: System,
    seed: Sequence[str],
    ladder: Sequence[int],
    *,
    names: Sequence[str],
    trust_radius: str = "1e-6",
    guard_digits: int = DEFAULT_GUARD_DIGITS,
) -> list[dict[str, str]]:
    """Refine at each precision in `ladder` and report how the residual moves.

    A Newton refinement of a *correct* system drives the residual down roughly in step
    with the working precision.  One that plateaus is refining against equations the
    pose does not satisfy, and this series is what makes that visible instead of
    letting a single impressive-looking residual stand on its own.
    """
    rows: list[dict[str, str]] = []
    for digits in ladder:
        result = refine(
            system,
            seed,
            digits,
            names=names,
            trust_radius=trust_radius,
            guard_digits=guard_digits,
        )
        rows.append(
            {
                "digits": str(digits),
                "working_digits": str(result.working_digits),
                "residual": result.residual,
                "residual_bound": result.residual_bound,
            }
        )
    return rows


def residual_falls(series: Sequence[dict[str, str]], *, minimum_decades: int = 10) -> bool:
    """Whether each rung of a residual series improves on the one below it.

    `minimum_decades` is the improvement a doubled precision must at least buy before
    the series counts as falling rather than plateauing.
    """
    if len(series) < 2:
        return False
    previous = mp.mpf(series[0]["residual"])
    for row in series[1:]:
        current = mp.mpf(row["residual"])
        if current <= 0:
            previous = current
            continue
        if previous > 0 and current > previous * mp.mpf(10) ** (-minimum_decades):
            return False
        previous = current
    return True
