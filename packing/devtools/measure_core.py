"""Measure how much of a smaller packing a larger one carries: a core, a border, a band.

A packing at ``n`` is sometimes said to be built from a registry packing at ``m < n``: a
core of it set in a corner with a border of unit squares round it, or a band of its tilted
squares laid again further along the diagonal. The credit follows from how much of the
smaller packing the larger one keeps. `devtools.measure_identity` compares two packings of
one count; this module places the smaller packing's squares in the larger box and counts
the squares of the larger packing that lie on them. A measurement for credit; it decides
nothing. Doğa Özden's issue 959 at 179 was the first (think-89i7): its side lies 2.6e-12
above s(70) + 5, and the issue says its band was seeded from the registry's 70.

**Inputs.** The view is a spec `devtools.measure_identity` reads at ``n``. The core is a
``packing.squares:Witness/v2`` file at ``m``, in any representation and scalar kind,
number fields included, projected by `sqpack.witness.materialize_witness` at `DIGITS`
digits.

**Measures**, in binary64 after that projection but for the sides:

- ``side``: the view's side less the core's, and less that again each whole number up to
  the integer part of the difference, at `DIGITS` digits; with ``l_border``, the squares a
  border of unit squares that wide adds to the core by L steps, ``k (2 floor(s) + k)`` at
  width ``k`` on side ``s``, which is what a core and its border hold at that side;
- ``core``: the core's box set flush in each corner of the view's box, under each of the
  eight symmetries of the core's box; each core square is matched to the view square of
  nearest centre, and counted within a bound where the centres lie within it and the two
  turn by less than a degree modulo a quarter turn; every placement's counts, and the
  best at each bound;
- ``diagonal``: the core, under each symmetry, laid at each diagonal shift ``(k, k)`` from
  0 to the integer part of the difference of the sides; each of the view's squares is
  counted within a bound where some placed core square lies within it and turns by less
  than a degree from it, so a core cut along the diagonal and laid at both ends of a
  longer one counts once per view square. Every symmetry's counts, and, for the symmetry
  that matches most at the tightest bound any symmetry meets, the counts shift by shift;
- ``band``: the same with only the squares of each beyond a degree from upright, the
  tilted band.

The bounds are `devtools.measure_identity`'s, with 0.05 added, the bound the stage 4 review
of issue 954 measured that issue's seed at (F8 of review-2026-11-11-ozden-954.md).

From ``packing/``, with the project interpreter::

    python -m devtools.measure_core --n 179 "#959=packet:ozden-s179-issue959-2026-11-11" \\
        --m 70 witnesses/known-best/n-070.yaml \\
        --out resources/web/ozden-s179-issue959-2026-11-11/measure/core-n070.json

The JSON written is the receipt a packet keeps under ``measure/``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath as mp
import numpy as np

from devtools import measure_identity as identity
from devtools import upper_bound_reports as reports
from sqpack.witness import WitnessError, load_witness, materialize_witness

FORMAT = "measure-core-v1"
DIGITS = 50
BOUNDS = ("1e-9", "1e-6", "1e-3", "1e-2", "5e-2", "1e-1")
#: Two squares turn alike where they differ by less than this, modulo a quarter turn.
TURN_DEGREES = 1.0
#: A square is tilted beyond this many degrees from upright.
TILTED_DEGREES = 1.0
WITNESS_SCHEMA = reports.ROOT / "witnesses/witness.schema.yaml"
CORNERS = ("lower-left", "lower-right", "upper-left", "upper-right")
#: The eight symmetries of a box of side s, as maps of a centre and whether they reflect.
SYMMETRIES = (
    "identity",
    "quarter-turn",
    "half-turn",
    "three-quarter-turn",
    "reflect-x",
    "reflect-y",
    "reflect-diagonal",
    "reflect-antidiagonal",
)


class CoreError(ValueError):
    """An input this module refuses to measure."""


@dataclass(frozen=True)
class Placed:
    """Centres and signed tilts in degrees, folded to (-45, 45], with the side."""

    side: float
    xy: np.ndarray
    tilt: np.ndarray


def fold(degrees: np.ndarray) -> np.ndarray:
    """Angles in degrees folded modulo a quarter turn to (-45, 45]."""
    folded = np.mod(degrees, 90.0)
    return np.where(folded > 45.0, folded - 90.0, folded)


def read_view(spec: str, n: int) -> tuple[Placed, Fraction, dict[str, Any]]:
    """The view, read exactly by `devtools.measure_identity`, then in binary64."""
    try:
        packing = identity.read_packing(spec, n)
    except identity.MeasureError as error:
        raise CoreError(str(error)) from error
    xy = np.array([[float(x), float(y)] for x, y, _c, _s in packing.squares])
    tilt = np.array([identity.signed_tilt(c, s) for _x, _y, c, s in packing.squares])
    source = {"label": packing.label, **packing.source, "side": str(packing.side)}
    return Placed(float(packing.side), xy, tilt), packing.side, source


def read_core(path: Path, m: int) -> tuple[Placed, Any, dict[str, Any]]:
    """The core witness projected at `DIGITS` digits, its side kept at that precision."""
    try:
        raw = path.read_bytes()
        witness = load_witness(path, fallback_schema=WITNESS_SCHEMA)
        corners, side = materialize_witness(witness, digits=DIGITS)
    except (OSError, WitnessError) as error:
        raise CoreError(f"{path}: {error}") from error
    if len(corners) != m or int(witness["n"]) != m:
        raise CoreError(f"{path}: {len(corners)} squares, not {m}")
    xy, tilt = [], []
    for square in corners:
        xs = [float(x) for x, _y in square]
        ys = [float(y) for _x, y in square]
        xy.append([sum(xs) / 4, sum(ys) / 4])
        tilt.append(math.degrees(math.atan2(ys[1] - ys[0], xs[1] - xs[0])))
    try:
        where = path.resolve().relative_to(reports.REPO.resolve()).as_posix()
    except ValueError:
        where = path.name
    source = {
        "path": where,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "witness": witness["id"],
        "scalar": witness["scalar"]["kind"],
        "side": mp.nstr(side, 25),
    }
    return Placed(float(side), np.array(xy), fold(np.array(tilt))), side, source


def transform(core: Placed, symmetry: str) -> Placed:
    """The core under one symmetry of its own box."""
    s, x, y = core.side, core.xy[:, 0], core.xy[:, 1]
    maps = {
        "identity": (x, y, False),
        "quarter-turn": (s - y, x, False),
        "half-turn": (s - x, s - y, False),
        "three-quarter-turn": (y, s - x, False),
        "reflect-x": (s - x, y, True),
        "reflect-y": (x, s - y, True),
        "reflect-diagonal": (y, x, True),
        "reflect-antidiagonal": (s - y, s - x, True),
    }
    nx, ny, reflects = maps[symmetry]
    tilt = fold(-core.tilt) if reflects else core.tilt
    return Placed(s, np.column_stack([nx, ny]), tilt)


def _turned_alike(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return np.abs(fold(left[:, None] - right[None, :])) < TURN_DEGREES


def _within(distance: np.ndarray) -> dict[str, int]:
    return {bound: int(np.sum(distance <= float(bound))) for bound in BOUNDS}


def core_matches(view: Placed, core: Placed) -> dict[str, Any]:
    """Every corner and symmetry placement of the core's box, with its counts."""
    gap = view.side - core.side
    offsets = {
        "lower-left": (0.0, 0.0),
        "lower-right": (gap, 0.0),
        "upper-left": (0.0, gap),
        "upper-right": (gap, gap),
    }
    rows = []
    for symmetry in SYMMETRIES:
        placed = transform(core, symmetry)
        for corner in CORNERS:
            centres = placed.xy + np.array(offsets[corner])
            distance = np.linalg.norm(centres[:, None, :] - view.xy[None, :, :], axis=2)
            distance = np.where(_turned_alike(placed.tilt, view.tilt), distance, np.inf)
            rows.append(
                {
                    "symmetry": symmetry,
                    "corner": corner,
                    "matched": _within(distance.min(axis=1)),
                }
            )
    best = {
        bound: max(rows, key=lambda row: row["matched"][bound])["matched"][bound]
        for bound in BOUNDS
    }
    return {"of": len(core.xy), "best": best, "placements": rows}


def diagonal_matches(view: Placed, core: Placed, *, tilted: bool) -> dict[str, Any]:
    """The core laid at each diagonal shift, against the view, square by view square.

    With ``tilted``, only the squares of each beyond a degree from upright take part.
    """
    shifts = range(math.floor(view.side - core.side) + 1)
    seen = np.abs(view.tilt) >= TILTED_DEGREES if tilted else np.ones(len(view.xy), bool)
    rows, per_shift = [], {}
    for symmetry in SYMMETRIES:
        placed = transform(core, symmetry)
        laid = (
            np.abs(placed.tilt) >= TILTED_DEGREES if tilted else np.ones(len(placed.xy), bool)
        )
        nearest = np.full(int(seen.sum()), np.inf)
        shifted: dict[str, dict[str, int]] = {}
        for k in shifts:
            centres = placed.xy[laid] + k
            distance = np.linalg.norm(view.xy[seen][:, None, :] - centres[None, :, :], axis=2)
            alike = _turned_alike(view.tilt[seen], placed.tilt[laid])
            reach = np.where(alike, distance, np.inf).min(axis=1)
            shifted[str(k)] = _within(reach)
            nearest = np.minimum(nearest, reach)
        rows.append({"symmetry": symmetry, "matched": _within(nearest)})
        per_shift[symmetry] = shifted
    best = None
    for bound in BOUNDS:
        if any(row["matched"][bound] for row in rows):
            best = max(rows, key=lambda row: row["matched"][bound])["symmetry"]
            break
    return {
        "view_squares": int(seen.sum()),
        "core_squares": int(laid_count(core, tilted=tilted)),
        "shifts": list(shifts),
        "symmetries": rows,
        "best_symmetry": best,
        "by_shift": per_shift[best] if best is not None else {},
    }


def laid_count(core: Placed, *, tilted: bool) -> int:
    """How many of the core's squares a diagonal measure lays."""
    return int(np.sum(np.abs(core.tilt) >= TILTED_DEGREES)) if tilted else len(core.xy)


def l_border(side: Any, width: int) -> int:
    """The unit squares a border ``width`` wide adds to a packing of ``side`` by L steps."""
    whole = math.floor(side)
    return width * (2 * whole + width)


def side_relation(view_side: Fraction, core_side: Any, m: int) -> dict[str, Any]:
    """The view's side against the core's plus each whole number, at `DIGITS` digits."""
    mp.mp.dps = DIGITS
    exact = mp.mpf(view_side.numerator) / view_side.denominator
    difference = exact - core_side
    rows = []
    for k in range(math.floor(difference) + 1):
        excess = difference - k
        rows.append(
            {
                "plus": k,
                "excess": mp.nstr(excess, 7, min_fixed=0, max_fixed=0, strip_zeros=False),
                "relative": mp.nstr(
                    excess / exact, 7, min_fixed=0, max_fixed=0, strip_zeros=False
                ),
                "l_border_count": m + l_border(core_side, k),
            }
        )
    return {"difference": mp.nstr(difference, 25), "plus": rows}


def receipt(view_spec: str, n: int, core_path: Path, m: int) -> dict[str, Any]:
    """The receipt of one view measured against one core."""
    if not 0 < m < n:
        raise CoreError(f"the core's count {m} must lie below the view's {n}")
    view, view_side, view_source = read_view(view_spec, n)
    core, core_side, core_source = read_core(core_path, m)
    if core.side > view.side:
        raise CoreError("the core's box is larger than the view's")
    return {
        "format": FORMAT,
        "n": n,
        "m": m,
        "inputs": {"view": view_source, "core": core_source},
        "bounds": list(BOUNDS),
        "side": side_relation(view_side, core_side, m),
        "core": core_matches(view, core),
        "diagonal": diagonal_matches(view, core, tilted=False),
        "band": diagonal_matches(view, core, tilted=True),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--n", type=int, required=True, help="the view's count")
    parser.add_argument("view", help="the packing measured, [LABEL=]KIND:TARGET")
    parser.add_argument("--m", type=int, required=True, help="the core's count")
    parser.add_argument("core", type=Path, help="the core's Witness/v2 file")
    parser.add_argument("--out", type=Path, help="where to write the receipt as well")
    args = parser.parse_args(argv)
    try:
        result = receipt(args.view, args.n, args.core, args.m)
    except CoreError as error:
        sys.stderr.write(f"measure_core: {error}\n")
        return 2
    text = json.dumps(result, indent=1) + "\n"
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
