#!/usr/bin/env python3
"""Census the near-tight event cells of a certificate, direction by direction.

A retained certificate says every reachable event cell carries mass at least 1
(``Condition 5``). This tool asks the next question: how many of them carry *barely*
more. For each net direction it counts the reachable cells whose covered mass is at
most ``1 + epsilon``, for each of several margins, and reports where in the rotated
frame that near-tight set sits.

The margin is a census margin and not a mass gap, and the two are easy to swap.
X-014's Lemma 1 writes ``epsilon(L) = M - 11`` for the mass gap, which exists only at a
side where the certificate fails; at ``381/100`` the retained certificate has
``M = 10.863675`` and the gap is negative. What is counted here is how many cells sit
just above one on a certificate that *succeeds*, which is the same geometry from the
other side and is what Corollary 1b asks for.

It is a readout, not a second computation. ``sweep.scaled_mass_grid`` fills the dense
integer grid that ``sweep.minimum_covered_mass_integer`` then takes a minimum of, and
``sweep.reduce_to_spans`` already returns the reachable cells as one ``(i, j0, j1)``
span per column; this walks the same array with a comparison instead of an ``argmin``.
Every count is decided in integers on the weights' common scale -- the threshold for
margin ``e`` is ``floor((1 + e) * scale)``, and a cell counts when its scaled mass is at
most that -- so no float chooses a cell.

The reading the census is for: a set at ``epsilon = 1/20`` that is a few hundred cells
clustered around a few dozen positions makes Corollary 1a's exact cover a check; a fat
set makes it a search, and a fat set is also what an integrality gap looks like from the
inside. So the per-direction row carries a count, a bounding box, and the number of
connected components of the near-tight set, which is the "positions" in that sentence.

Usage:
    uv run --frozen python -m devtools.census_tight_cells <path>...
    uv run --frozen python -m devtools.census_tight_cells <path> --json out.json
    uv run --frozen python -m devtools.census_tight_cells <path> --max-directions 4

A malformed certificate is refused by name before any grid is filled: the candidate is
parsed by `devtools.decide_certificate`'s loader, which is the same strict reader the
retention gate uses, so an inexact JSON number, a missing field or a declared
``class``/``conditional`` variant is named rather than silently censused.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy import ndimage

from devtools.decide_certificate import CertificateFormatError, load
from sqpack.fractional.certificate import Certificate
from sqpack.fractional.model import Atom, Direction
from sqpack.fractional.sweep import centre_domain, scaled_mass_grid, weight_scale

#: The four margins H-065 registers. ``0`` is a control rather than a measurement: on a
#: certificate whose least cell mass exceeds 1 it must come back empty at every
#: direction, and a nonzero count there means the census is reading a different object
#: than the gate decided.
DEFAULT_MARGINS: tuple[Fraction, ...] = (
    Fraction(0),
    Fraction(1, 100),
    Fraction(1, 20),
    Fraction(1, 10),
)

#: The margin whose geometry is reported: box, components, extents. X-014's reading is
#: stated at ``epsilon = 0.05`` and H-065's accept line is declared there.
CLUSTER_MARGIN = Fraction(1, 20)

#: Corner-touching connectivity for the component count. Two cells that meet only at a
#: corner still share a point of the plane, so they are one position; the edge-only
#: count is reported beside it because the difference is a real ambiguity in the word
#: "clustered" and neither number should be the only one on the record.
_CORNER = np.ones((3, 3), dtype=bool)


def tight_threshold(margin: Fraction, scale: int, scaled_total: int) -> int:
    """The largest scaled mass that is still within ``margin`` of one.

    A cell's mass is at most ``1 + margin`` exactly when its scaled mass -- an integer --
    is at most ``floor((1 + margin) * scale)``. Clamped at the scaled total because no
    cell can carry more than every atom, which keeps the comparison inside ``int64``
    when a margin is large and the scale is small.
    """

    if margin < 0:
        raise ValueError(f"a census margin must be nonnegative, got {margin}")
    exact = (1 + margin) * scale
    return min(exact.numerator // exact.denominator, scaled_total)


@dataclass(frozen=True, slots=True)
class DirectionCensus:
    """One direction's row: what was reachable, what was near-tight, and where."""

    index: int
    label: str
    half_tangent: Fraction
    reachable: int
    #: One count per margin, in the census's own margin order.
    tight: tuple[int, ...]
    least_mass: Fraction
    #: ``(u_low, u_high, v_low, v_high)`` of the near-tight set at the cluster margin,
    #: in the rotated frame, or ``None`` when that set is empty.
    box: tuple[Fraction, Fraction, Fraction, Fraction] | None
    #: The admissible centres' own extent in the same frame, for scale.
    domain_box: tuple[Fraction, Fraction, Fraction, Fraction]
    components_corner: int
    components_edge: int


@dataclass(frozen=True, slots=True)
class Census:
    """Every direction's row, plus the totals H-065 is read from."""

    margins: tuple[Fraction, ...]
    cluster_margin: Fraction
    scale: int
    directions: tuple[DirectionCensus, ...]

    @property
    def reachable(self) -> int:
        return sum(row.reachable for row in self.directions)

    @property
    def tight_totals(self) -> tuple[int, ...]:
        return tuple(
            sum(row.tight[k] for row in self.directions) for k in range(len(self.margins))
        )

    @property
    def fractions(self) -> tuple[Fraction, ...]:
        """The summed near-tight count over the summed reachable count, per margin."""
        reachable = self.reachable
        if reachable == 0:  # pragma: no cover - reduce_to_spans raises first
            raise ValueError("the census found no reachable cell")
        return tuple(Fraction(total, reachable) for total in self.tight_totals)


def census_direction(
    atoms: tuple[Atom, ...],
    direction: Direction,
    outer_side: Fraction,
    square_side: Fraction,
    scale: int,
    *,
    index: int = 0,
    half_tangent: Fraction = Fraction(0),
    margins: tuple[Fraction, ...] = DEFAULT_MARGINS,
    cluster_margin: Fraction = CLUSTER_MARGIN,
) -> DirectionCensus:
    """Count the near-tight reachable cells at one direction, in integers."""

    scaled_total = sum((atom.weight for atom in atoms), start=Fraction(0)) * scale
    if scaled_total.denominator != 1:  # pragma: no cover - scaled_mass_grid raises first
        raise ValueError("weights are not integers on the declared common scale")
    filled = scaled_mass_grid(atoms, direction, outer_side, square_side, scale)
    grid, reduction = filled.grid, filled.reduction

    reach = np.zeros(grid.shape, dtype=bool)
    for i, j0, j1 in reduction.spans:
        reach[i, j0 : j1 + 1] = True
    reachable = int(np.count_nonzero(reach))

    total = int(scaled_total)
    counts = tuple(
        int(np.count_nonzero(reach & (grid <= tight_threshold(margin, scale, total))))
        for margin in margins
    )
    least = Fraction(int(grid[reach].min()), scale)

    tight = reach & (grid <= tight_threshold(cluster_margin, scale, total))
    box: tuple[Fraction, Fraction, Fraction, Fraction] | None = None
    corner = edge = 0
    if bool(tight.any()):
        columns, rows = np.nonzero(tight)
        box = (
            reduction.u_events[int(columns.min())],
            reduction.u_events[int(columns.max()) + 1],
            reduction.v_events[int(rows.min())],
            reduction.v_events[int(rows.max()) + 1],
        )
        corner = int(ndimage.label(tight, structure=_CORNER)[1])
        edge = int(ndimage.label(tight)[1])

    domain = centre_domain(outer_side, square_side, direction)
    domain_box = (
        min(u for u, _ in domain),
        max(u for u, _ in domain),
        min(v for _, v in domain),
        max(v for _, v in domain),
    )
    return DirectionCensus(
        index=index,
        label=direction.label,
        half_tangent=half_tangent,
        reachable=reachable,
        tight=counts,
        least_mass=least,
        box=box,
        domain_box=domain_box,
        components_corner=corner,
        components_edge=edge,
    )


def census_certificate(
    certificate: Certificate,
    *,
    margins: tuple[Fraction, ...] = DEFAULT_MARGINS,
    cluster_margin: Fraction = CLUSTER_MARGIN,
    max_directions: int | None = None,
    progress: bool = False,
) -> Census:
    """Census every net direction in net order, in this process, on one core."""

    atoms = certificate.atoms
    scale = weight_scale(atoms)
    directions = certificate.directions
    tangents = certificate.half_tangents
    if max_directions is not None:
        directions = directions[:max_directions]
        tangents = tangents[:max_directions]
    rows: list[DirectionCensus] = []
    for index, (direction, tangent) in enumerate(zip(directions, tangents, strict=True)):
        started = time.monotonic()
        row = census_direction(
            atoms,
            direction,
            certificate.outer_side,
            certificate.square_side,
            scale,
            index=index,
            half_tangent=tangent,
            margins=margins,
            cluster_margin=cluster_margin,
        )
        rows.append(row)
        if progress:
            print(
                f"  direction {index:>3} reachable {row.reachable:>9} "
                f"tight {row.tight} least {_approx(row.least_mass)} "
                f"components {row.components_corner} "
                f"[{time.monotonic() - started:.2f} s]",
                flush=True,
            )
    return Census(margins, cluster_margin, scale, tuple(rows))


def _approx(value: Fraction) -> str:
    """A diagnostic float. Nothing here decides on one."""

    try:
        return f"{float(value):.6f}"
    except OverflowError:  # pragma: no cover - certificate masses are small
        return "outside-float-range"


def _row_record(row: DirectionCensus, margins: tuple[Fraction, ...]) -> dict[str, object]:
    return {
        "index": row.index,
        "label": row.label,
        "half_tangent": str(row.half_tangent),
        "reachable": row.reachable,
        "tight": {str(margin): count for margin, count in zip(margins, row.tight, strict=True)},
        "least_mass": str(row.least_mass),
        "least_mass_approx": _approx(row.least_mass),
        "box": None if row.box is None else [str(value) for value in row.box],
        "box_approx": None if row.box is None else [_approx(value) for value in row.box],
        "domain_box": [str(value) for value in row.domain_box],
        "components_corner": row.components_corner,
        "components_edge": row.components_edge,
    }


def census_record(
    path: Path, certificate: Certificate, census: Census, *, digest: str
) -> dict[str, object]:
    """The census as one JSON-shaped record, exact rationals as strings."""

    margins = census.margins
    return {
        "certificate": {
            "path": str(path),
            "sha256": digest,
            "n": certificate.n,
            "outer_side": str(certificate.outer_side),
            "square_side": str(certificate.square_side),
            "atoms": len(certificate.atoms),
            "directions": len(certificate.directions),
            "total_mass": str(certificate.total_mass),
        },
        "scale": census.scale,
        "margins": [str(margin) for margin in margins],
        "cluster_margin": str(census.cluster_margin),
        "totals": {
            "directions_censused": len(census.directions),
            "reachable": census.reachable,
            "tight": {
                str(margin): count
                for margin, count in zip(margins, census.tight_totals, strict=True)
            },
            "fraction": {
                str(margin): str(value)
                for margin, value in zip(margins, census.fractions, strict=True)
            },
            "fraction_approx": {
                str(margin): _approx(value)
                for margin, value in zip(margins, census.fractions, strict=True)
            },
        },
        "directions": [_row_record(row, margins) for row in census.directions],
    }


def _print_summary(census: Census) -> None:
    margins = census.margins
    print(
        f"  {len(census.directions)} directions, {census.reachable} reachable cells, "
        f"weight scale {census.scale}",
        flush=True,
    )
    for margin, count, fraction in zip(
        margins, census.tight_totals, census.fractions, strict=True
    ):
        print(
            f"  epsilon = {margin!s:<6} tight {count:>10}  "
            f"fraction {fraction} = {_approx(fraction)}",
            flush=True,
        )
    populated = [row for row in census.directions if row.box is not None]
    if not populated:
        print(f"  no cell within {census.cluster_margin} of one at any direction", flush=True)
        return
    cluster_index = census.margins.index(census.cluster_margin)
    counts = [row.tight[cluster_index] for row in populated]
    components = [row.components_corner for row in populated]
    worst = max(census.directions, key=lambda row: row.tight[cluster_index])
    best = min(census.directions, key=lambda row: row.tight[cluster_index])
    print(
        f"  at epsilon = {census.cluster_margin}: per direction "
        f"{min(counts)}..{max(counts)} cells in {min(components)}..{max(components)} "
        f"corner-connected components over {len(populated)} of "
        f"{len(census.directions)} directions",
        flush=True,
    )
    print(
        f"  most tight: direction {worst.index} ({worst.tight[cluster_index]} of "
        f"{worst.reachable}); least tight: direction {best.index} "
        f"({best.tight[cluster_index]} of {best.reachable})",
        flush=True,
    )


def run(
    path: Path,
    *,
    margins: tuple[Fraction, ...] = DEFAULT_MARGINS,
    cluster_margin: Fraction = CLUSTER_MARGIN,
    max_directions: int | None = None,
    progress: bool = False,
    json_path: Path | None = None,
) -> bool:
    """Census one candidate. Returns whether it could be read and censused."""

    try:
        data = path.read_bytes()
        certificate, _record = load(path)
    except (CertificateFormatError, OSError) as error:
        print(f"{path}: REFUSED: cannot load certificate: {error}", flush=True)
        return False
    digest = hashlib.sha256(data).hexdigest()
    print(
        f"{path}: n = {certificate.n}, L = {certificate.outer_side}, "
        f"{len(certificate.atoms)} atoms, {len(certificate.directions)} directions, "
        f"sha256 {digest[:16]}",
        flush=True,
    )
    started = time.monotonic()
    census = census_certificate(
        certificate,
        margins=margins,
        cluster_margin=cluster_margin,
        max_directions=max_directions,
        progress=progress,
    )
    _print_summary(census)
    print(f"  censused in {time.monotonic() - started:.1f} s", flush=True)
    if json_path is not None:
        record = census_record(path, certificate, census, digest=digest)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(record, indent=1) + "\n")
        print(f"  wrote {json_path}", flush=True)
    return True


def _margins(text: str) -> tuple[Fraction, ...]:
    try:
        values = tuple(Fraction(part.strip()) for part in text.split(",") if part.strip())
    except (ValueError, ZeroDivisionError) as error:
        raise argparse.ArgumentTypeError(f"not a list of exact rationals: {error}") from None
    if not values:
        raise argparse.ArgumentTypeError("at least one margin is required")
    if any(margin < 0 for margin in values):
        raise argparse.ArgumentTypeError("a census margin must be nonnegative")
    return values


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument(
        "--margins",
        type=_margins,
        default=DEFAULT_MARGINS,
        help="comma-separated exact rationals; default 0,1/100,1/20,1/10",
    )
    parser.add_argument(
        "--cluster-margin",
        type=Fraction,
        default=CLUSTER_MARGIN,
        help="the margin whose box and components are reported; default 1/20",
    )
    parser.add_argument(
        "--max-directions",
        type=int,
        default=None,
        help="census only the first N net directions, for a smoke run",
    )
    parser.add_argument("--json", type=Path, default=None, help="write the full table here")
    parser.add_argument("--progress", action="store_true", help="one line per direction")
    args = parser.parse_args(argv)
    margins = tuple(args.margins)
    cluster = Fraction(args.cluster_margin)
    if cluster not in margins:
        margins = tuple(sorted({*margins, cluster}))
    failed = 0
    for path in args.paths:
        ok = run(
            path,
            margins=margins,
            cluster_margin=cluster,
            max_directions=args.max_directions,
            progress=args.progress,
            json_path=args.json,
        )
        failed += not ok
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
