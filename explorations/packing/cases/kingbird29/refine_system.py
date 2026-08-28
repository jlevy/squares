#!/usr/bin/env python3
"""Drive the transcribed `n = 29` system to a declared precision, and report the residual.

This is BC-047.  It makes **no algebraic claim**: it reports precision, a residual
bound, and how the residual behaves as the working precision rises.  Whether the
refined value satisfies a minimal polynomial, and whether the pose it describes is a
certified packing, are separate questions owned by BC-044 and BC-045.

Two controls run alongside the refinement, because a refiner that cannot fail has not
been tested:

- **a far seed** must produce a typed refusal, never a silently returned number.  The
  refusal may be non-convergence or a departure from the declared trust region; both
  are typed, and converging quietly to some other root is the failure this rules out.
- **the residual must fall** with working precision.  A residual that plateaus is how a
  wrong system looks from here, and this control is what stops an impressive-looking
  single number from standing on its own.
- **the refiner must refuse a degenerate system.**  Replacing one equation with a copy
  of another leaves the system square but rank-deficient, so Newton has no isolated root
  to find; the refiner is required to say so rather than return whatever the linear
  solve produced.

A third check was written, failed to fire, and is retained as a measurement rather than
deleted.  Displacing one equation of this system by a small constant does *not* make the
residual plateau: the displaced system still has a root, about as far from the original
as the displacement, and Newton finds it.  The consequence is recorded in the evidence
file and is worth stating plainly here -- on a square, consistent, well-conditioned
system, "the residual falls" is nearly unfalsifiable and is therefore **not** evidence
that the transcription is correct.  The plateau failure mode the spec anticipates
belongs to an *over-determined* system, which is what a wrong contact structure produces,
and detecting it is BC-042 and BC-043's problem rather than this step's.
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict
from pathlib import Path

import mpmath as mp

from cases.kingbird29 import system
from sqpack.promote.refine import (
    RefinementError,
    refine,
    residual_falls,
    residual_series,
)

TARGET_DIGITS = 1000
LADDER = (60, 125, 250, 500, 1000)
TRUST_RADIUS = "1e-6"

#: Degrees added to `a` for the far-seed control.  Far enough to leave the basin, and
#: still a physically sensible angle, so the control tests the refiner rather than
#: mpmath's handling of nonsense input.
FAR_SEED_OFFSET_DEGREES = "5"


def far_seed(seed: tuple[str, ...]) -> tuple[str, ...]:
    """The serialized pose with one angle displaced well outside the trust region."""
    values = list(seed)
    index = system.UNKNOWNS.index("a")
    values[index] = str(mp.mpf(values[index]) + mp.mpf(FAR_SEED_OFFSET_DEGREES))
    return tuple(values)


def run_far_seed_control(seed: tuple[str, ...]) -> dict:
    """Require a typed refusal from a seed outside the basin."""
    try:
        result = refine(
            system.equations,
            far_seed(seed),
            60,
            names=system.UNKNOWNS,
            trust_radius=TRUST_RADIUS,
        )
    except RefinementError as error:
        return {"refused": True, "kind": error.kind, "detail": str(error)}
    return {
        "refused": False,
        "kind": None,
        "detail": (
            "the refiner returned a value from a seed five degrees outside the trust "
            f"region: {dict(zip(result.names, result.values, strict=True))['s'][:40]}"
        ),
    }


def run_degenerate_system_control(seed: tuple[str, ...]) -> dict:
    """Require a typed refusal from a square but rank-deficient system.

    Replacing `f6` with a copy of `f5` keeps the system six-by-six while destroying the
    rank of its Jacobian, so no isolated root exists to refine towards.  This is the
    wrong-system control that can actually fire.
    """

    def degenerate(*values):
        residuals = list(system.equations(*values))
        residuals[5] = residuals[4]
        return residuals

    try:
        result = refine(degenerate, seed, 60, names=system.UNKNOWNS, trust_radius=TRUST_RADIUS)
    except RefinementError as error:
        return {"refused": True, "kind": error.kind, "detail": str(error)}
    except (ZeroDivisionError, ArithmeticError) as error:
        return {
            "refused": False,
            "kind": None,
            "detail": (
                "the refiner raised an untyped "
                f"{type(error).__name__} instead of a RefinementError: {error}"
            ),
        }
    return {
        "refused": False,
        "kind": None,
        "detail": (
            "the refiner returned a value for a rank-deficient system, residual "
            f"{result.residual}"
        ),
    }


def measure_displaced_equation(seed: tuple[str, ...]) -> dict:
    """Measure what a small constant displacement of one equation actually does.

    This began as a control and did not fire.  It is retained because the reason it
    cannot fire is a fact about the system worth recording: a square consistent system
    perturbed by a constant still has a nearby root, so the residual keeps tracking the
    working precision and "the residual falls" says nothing about whether the equations
    are the right ones.
    """
    displacement = mp.mpf("1e-12")

    def displaced(*values):
        residuals = list(system.equations(*values))
        residuals[0] = residuals[0] + displacement
        return residuals

    try:
        series = residual_series(
            displaced, seed, (60, 125, 250), names=system.UNKNOWNS, trust_radius=TRUST_RADIUS
        )
    except RefinementError as error:
        return {"plateaued": True, "kind": error.kind, "series": []}
    return {
        "displacement": "1e-12",
        "plateaued": not residual_falls(series),
        "finding": (
            "a constant displacement of one equation does not plateau the residual; the "
            "displaced system has its own nearby root and Newton converges to it, so "
            "residual_falls is not a test of whether the system is the right one"
        ),
        "series": series,
    }


def build_result(source: Path) -> dict:
    started = time.monotonic()
    seed = system.seed(source)
    series = residual_series(
        system.equations, seed, LADDER, names=system.UNKNOWNS, trust_radius=TRUST_RADIUS
    )
    refinement = refine(
        system.equations,
        seed,
        TARGET_DIGITS,
        names=system.UNKNOWNS,
        trust_radius=TRUST_RADIUS,
    )
    control = run_far_seed_control(seed)
    degenerate_control = run_degenerate_system_control(seed)
    displacement = measure_displaced_equation(seed)
    falls = residual_falls(series)
    return {
        "schema_version": 1,
        "commitment": "BC-047",
        "source": {
            "path": source.as_posix(),
            "transcription": "cases.kingbird29.system",
            "unknowns": list(system.UNKNOWNS),
            "slide_scalars": list(system.SLIDE_SCALARS),
            "equations": list(system.EQUATIONS),
        },
        "claim_scope": (
            "high-precision refinement of a transcribed system; reports precision and a "
            "residual bound, and makes no algebraic or feasibility claim"
        ),
        "refinement": asdict(refinement),
        "residual_series": series,
        "controls": {
            "residual_falls_with_precision": falls,
            "residual_falls_scope": (
                "reported, not a control: on a square consistent system this is nearly "
                "unfalsifiable, as the displaced-equation measurement below shows"
            ),
            "far_seed_refused": control,
            "degenerate_system_refused": degenerate_control,
        },
        "measurements": {"displaced_equation": displacement},
        "elapsed_seconds": round(time.monotonic() - started, 6),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="retained Kingbird provenance SVG")
    parser.add_argument("--record", type=Path, help="write the JSON evidence record atomically")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = build_result(args.source)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.record:
        args.record.parent.mkdir(parents=True, exist_ok=True)
        temporary = args.record.with_suffix(args.record.suffix + ".tmp")
        temporary.write_text(rendered)
        temporary.replace(args.record)
    print(rendered, end="")
    controls = result["controls"]
    if not controls["residual_falls_with_precision"]:
        print("REFUSED: the residual does not fall with precision; the system is wrong")
        return 1
    if not controls["far_seed_refused"]["refused"]:
        print("REFUSED: the far-seed control did not produce a typed refusal")
        return 1
    if not controls["degenerate_system_refused"]["refused"]:
        print("REFUSED: the refiner did not refuse a rank-deficient system")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
