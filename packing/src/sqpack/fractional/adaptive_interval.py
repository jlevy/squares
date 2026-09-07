"""Independent cell geometry and interval coverage controls for BC-231.

The cell derivation below does not call the exact adaptive route. Coverage uses
the existing directed-rounding box search, with each reflected direction retaining
its own source cell's core side. No result here is a retention verdict.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import TYPE_CHECKING

from sqpack.fractional.certificate import Certificate
from sqpack.fractional.interval import (
    AtomData,
    DirectionOutcome,
    DirectionSearch,
    Interval,
    IntervalInputError,
    doubled_net,
)

if TYPE_CHECKING:
    from sqpack.fractional.adaptive import AdaptiveCertificate, AngleCell


def check_cell_geometry(cells: tuple[AngleCell, ...]) -> None:
    """Rebuild seams and mismatches from rotations, independently of ``derive_cells``."""
    count = len(cells)
    if count < 2:
        raise IntervalInputError("the adaptive net needs at least two cells")
    tangents = tuple(cell.half_tangent for cell in cells)
    if any(not isinstance(tangent, Fraction) for tangent in tangents):
        raise IntervalInputError("half-tangents must be exact Fractions")
    if tangents[0] != 0 or any(not 0 <= tangent < 1 for tangent in tangents):
        raise IntervalInputError("half-tangents must start at zero and lie in [0, 1)")
    boundaries = [Fraction(0)]
    for index in range(1, count):
        left, right = tangents[index - 1], tangents[index]
        if left >= right:
            raise IntervalInputError("half-tangents must be strictly increasing")
        boundaries.append((left + right) / (1 - left * right))
    boundaries.append(Fraction(1))
    if not ((1 + tangents[-2]) ** 2 < 2 <= (1 + tangents[-1]) ** 2):
        raise IntervalInputError("the final directions must bracket the folded endpoint")
    if any(boundaries[index] >= boundaries[index + 1] for index in range(count)):
        raise IntervalInputError(
            "derived seams must increase strictly through the folded endpoint"
        )
    for index, cell in enumerate(cells):
        if type(cell.index) is not int or cell.index != index:
            raise IntervalInputError("angle-cell indices must be contiguous from zero")
        tangent = tangents[index]
        cosine = (1 - tangent * tangent) / (1 + tangent * tangent)
        sine = 2 * tangent / (1 + tangent * tangent)
        lower, upper = boundaries[index : index + 2]
        mismatch = max(
            abs(sine - cosine * edge) / (cosine + sine * edge) for edge in (lower, upper)
        )
        if (
            cell.lower_boundary_tangent,
            cell.upper_boundary_tangent,
            cell.max_mismatch_tangent,
        ) != (lower, upper, mismatch):
            raise IntervalInputError(
                f"cell {index} differs from its independently derived geometry"
            )
        if not isinstance(cell.square_side, Fraction) or cell.square_side <= 0:
            raise IntervalInputError(f"cell {index} needs a positive exact core side")
        if cell.square_side * (1 + mismatch) >= 1:
            raise IntervalInputError(f"strict containment fails in cell {index}")


@dataclass(frozen=True, slots=True)
class IntervalMinima:
    directions: tuple[DirectionOutcome, ...]
    scale: int


def interval_minima(certificate: AdaptiveCertificate) -> IntervalMinima:
    """Enclose every directional minimum, including the reflected half of the net."""
    check_cell_geometry(certificate.cells)
    tangents = tuple(cell.half_tangent for cell in certificate.cells)
    # AtomData's scalar carrier supplies only n and atoms to the mass arithmetic.
    # Neither its scalar containment predicate nor its geometry is evaluated here.
    carrier = Certificate(
        certificate.n,
        certificate.outer_side,
        certificate.cells[0].square_side,
        certificate.atoms,
        tangents,
        certificate.symmetry,
    )
    atoms = AtomData.of(carrier)
    results = []
    for rotation in doubled_net(tangents):
        index = int(rotation.label.removesuffix("'"))
        search = DirectionSearch(
            atoms,
            rotation,
            Interval.of(certificate.outer_side),
            Interval.of(certificate.cells[index].square_side),
        )
        results.append(search.search(prune_at=None))
    return IntervalMinima(tuple(results), atoms.scale)
