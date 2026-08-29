#!/usr/bin/env python3
"""Drive the `n = 29` packing through interval certification, end to end.

Five stages, each of which can refuse, and the refusals are as much the point as the
number at the end:

```
published digits -> Newton refinement -> Krawczyk (root exists, is unique)
                 -> layout map (pose box -> corner boxes)
                 -> relaxation -> interval separating-axis test -> a bound
```

**What the bound is, and what it is not.**  What comes out is a statement of the form
`s(29) <= S` for an `S` strictly above the packing's own side, obtained by opening every
contact by a declared `eps`.  It is not a claim about the optimum, it is not a claim that
the published record is exactly right, and it is not an optimality result -- the `n = 29`
bound gap of about `0.46` is untouched by any of this.

**Nothing here may promote it.**  An unattended runner records this `unresolved` with
`needs_review: true`; moving `verified_upper_bound` is a reviewed change through the
evidence contract, made by a person, never a side effect of a script that ran overnight.

Run it:

```shell
uv run --frozen python -m cases.kingbird29.certify_interval
```
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import mpmath as mp

from cases.kingbird29 import system
from cases.kingbird29.layout import DEFAULT_SOURCE, squares_at
from sqpack.promote.interval import Dual, carrier, decimal_string, interval
from sqpack.promote.krawczyk import PoseBox, certify
from sqpack.promote.refine import refine
from sqpack.promote.relax import certified_upper_bound, relax

#: Working precision for the whole chain.  Well above what the bound reports, so the
#: digits that are printed are not the ones carrying the chain's own rounding.
PRECISION = 80

#: How wide a box the operator is asked to certify around the refined pose.  Wide enough
#: that contraction is doing real work, narrow enough that the layout stays decidable.
SEED_RADIUS = "1e-30"

#: The relaxations reported, largest first, so the bound can be watched falling.
LADDER = ("1e-6", "1e-9", "1e-12", "1e-15", "1e-20")

#: The standing verified ceiling this construction would tighten, from `frontier/n-029`.
STANDING_VERIFIED_CEILING = "5.93388579981302587863645209"


def _scalar(value: Any) -> Any:
    """Corner components come back as duals where they depend on the unknowns.

    Squares built entirely from integer transforms do not, so both shapes reach here and
    both have to become enclosures.
    """
    return value.value if isinstance(value, Dual) else interval(value)


def certify_n29(source: Path = DEFAULT_SOURCE, *, digits: int = 45) -> dict:
    """Run the whole chain and return everything needed to distrust the result."""
    previous = mp.mp.dps, mp.iv.dps
    mp.mp.dps = mp.iv.dps = PRECISION
    try:
        started = time.time()
        seed = system.seed(source)
        refinement = refine(system.equations, seed, 60, names=system.UNKNOWNS)
        root = certify(
            system.equations,
            PoseBox.around(system.UNKNOWNS, refinement.values, SEED_RADIUS),
            digits=digits,
        )
        if not root.unique:
            return {
                "certified": False,
                "refusal": "the contact system's root was not proved unique, so which "
                "pose would be certified is not decided",
                "root": root.summary(),
            }

        squares = [
            [(_scalar(x), _scalar(y)) for x, y in square]
            for square in squares_at(source, [carrier(v) for v in root.box.intervals()])
        ]
        rungs = []
        best = None
        for epsilon in LADDER:
            bound = certified_upper_bound(squares, epsilon=epsilon, digits=30)
            rungs.append(
                {
                    "epsilon": epsilon,
                    "bound": bound.bound,
                    "certified": bound.certified,
                    "undecided_pairs": len(bound.report.undecided_pairs),
                    "overlapping_pairs": len(bound.report.overlapping_pairs),
                }
            )
            if bound.certified:
                best = bound
        return {
            "certified": best is not None,
            "n": 29,
            "root_box_radius": root.max_radius,
            "root_iterations": root.iterations,
            "root_operator": root.operator,
            "refinement_residual_bound": refinement.residual_bound,
            "squares": len(squares),
            "pairs_tested": best.report.pairs_tested if best else 0,
            "separated_pairs": best.report.separated_pairs if best else 0,
            "relaxation": best.relaxation if best else None,
            "bound": best.bound if best else None,
            "claim": best.claim() if best else None,
            "standing_verified_ceiling": STANDING_VERIFIED_CEILING,
            "ceiling_gap_closed": (
                mp.nstr(mp.mpf(STANDING_VERIFIED_CEILING) - mp.mpf(best.bound), 6)
                if best
                else None
            ),
            "ladder": rungs,
            "working_precision": PRECISION,
            "elapsed_seconds": round(time.time() - started, 3),
            "assurance": "interval-certified",
            "needs_review": True,
            "claim_boundary": (
                "An upper bound on s(29) at a declared relaxation. Not the optimum, not "
                "an optimality result, and not a promotion: verified_upper_bound moves "
                "only by a reviewed change through the evidence contract."
            ),
        }
    finally:
        mp.mp.dps, mp.iv.dps = previous


def emit_witness(source: Path = DEFAULT_SOURCE, *, epsilon: str = "1e-20") -> dict:
    """Build a `Witness/v2` record carrying the enclosures this route certified.

    The witness stores the **relaxed** corners, because those are what was verified.
    Storing the unrelaxed ones and the relaxation separately would leave a reader to
    redo the shift and hope they did it the same way; storing what was checked means the
    replay checks the same thing.
    """
    previous = mp.mp.dps, mp.iv.dps
    mp.mp.dps = mp.iv.dps = PRECISION
    try:
        seed = system.seed(source)
        refinement = refine(system.equations, seed, 60, names=system.UNKNOWNS)
        root = certify(
            system.equations,
            PoseBox.around(system.UNKNOWNS, refinement.values, SEED_RADIUS),
            digits=45,
        )
        if not root.unique:
            raise ValueError("the root was not proved unique; nothing may be emitted")
        squares = [
            [(_scalar(x), _scalar(y)) for x, y in square]
            for square in squares_at(source, [carrier(v) for v in root.box.intervals()])
        ]
        bound = certified_upper_bound(squares, epsilon=epsilon, digits=30)
        if not bound.certified:
            raise ValueError(f"nothing to emit: {bound.report.refusal_reason()}")
        relaxed = relax(squares, epsilon)

        def pair(value) -> list[str]:
            return [
                decimal_string(mp.mpf(value.a), 40, upward=False),
                decimal_string(mp.mpf(value.b), 40, upward=True),
            ]

        return {
            "id": "W-kingbird-n029-interval",
            "n": 29,
            "side": [bound.bound, bound.bound],
            "square_size": "1",
            "representation": "corners",
            "scalar": {
                "kind": "interval-enclosure",
                "enclosure": {
                    "operator": root.operator,
                    "exists": root.exists,
                    "unique": root.unique,
                    "radius": root.max_radius,
                    "working_precision": root.working_precision,
                    "relaxation": epsilon,
                    "contact_system": (
                        "cases.kingbird29.system.equations -- the six closing equations "
                        "f1..f6 the provenance SVG publishes, in {s, a, b, c, d, i}"
                    ),
                    "pose_box": {
                        "names": list(root.box.names),
                        "lo": list(root.box.lo),
                        "hi": list(root.box.hi),
                    },
                },
            },
            "coordinates": {
                "origin": "lower-left",
                "axes": "x-right-y-up",
                "angle_unit": "not-applicable",
            },
            "squares": [
                {"id": index + 1, "corners": [[pair(x), pair(y)] for x, y in square]}
                for index, square in enumerate(relaxed)
            ],
            "claim": {
                "coordinate_provenance": "verified",
                "method": "interval-certified",
                "precision": {"decimal_digits": 40, "rounding": "outward"},
                "limitations": (
                    "An upper bound on s(29) at a declared relaxation of "
                    f"{epsilon}, established on enclosures rather than exact values. Not "
                    "the optimum, not an optimality result, and below exact-algebraic on "
                    "the assurance ladder: soundness rests on the interval library's "
                    "directed rounding, not on exact predicates. The enclosures are of "
                    "the relaxed configuration, which is the one that was verified."
                ),
            },
            "source": {
                "key": "[Kingbird n=29 provenance SVG]",
                "path": str(source),
            },
            "certificate": {
                "kind": "interval-krawczyk-sat",
                "derived_from": "cases.kingbird29.system.equations",
                "operator": root.operator,
                "root_unique": root.unique,
                "pose_box_radius": root.max_radius,
                "operator_iterations": root.iterations,
                "working_precision": root.working_precision,
                "refinement_residual_bound": refinement.residual_bound,
                "relaxation": epsilon,
                "pairs_tested": bound.report.pairs_tested,
                "separated_pairs": bound.report.separated_pairs,
                "undecided_pairs": len(bound.report.undecided_pairs),
                "layout_equivalence": (
                    "cases.kingbird29.layout.agrees_with_materialised reproduces all 29 "
                    "squares of the independent numeric walk to 1e-40"
                ),
                "replay": (
                    "uv run --frozen packing-witness verify "
                    "witnesses/kingbird-n029-2026-interval.yaml"
                ),
                "rebuild": "uv run --frozen python -m cases.kingbird29.certify_interval",
            },
        }
    finally:
        mp.mp.dps, mp.iv.dps = previous


def main() -> int:
    result = certify_n29()
    if not result["certified"]:
        print("NOT CERTIFIED:", result.get("refusal", "no bound"))
        return 1
    print(f"n = 29 interval certification, {result['elapsed_seconds']}s")
    print(f"  root:      unique in a box of radius {result['root_box_radius']}")
    print(f"  layout:    {result['squares']} squares, {result['pairs_tested']} pairs")
    print(f"  verified:  {result['separated_pairs']} strictly separated, 0 undecided")
    print(f"  claim:     {result['claim']}")
    print(
        f"  ceiling:   {result['standing_verified_ceiling']} would tighten by "
        f"{result['ceiling_gap_closed']}"
    )
    print("  needs_review: True -- no runner may promote this")
    output = Path(
        "campaign/series/series-000-smoke-and-calibration/results/"
        "bc-053-n29-interval-certificate.json"
    )
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"  written:   {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
