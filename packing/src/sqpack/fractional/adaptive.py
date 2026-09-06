"""In-memory BC-231 controls for the BC-230 ``legacy-linear-v1`` core theorem.

This module has no JSON loader or retention verdict. It supplies the scalar
specialization and direction-dependent sweep controls needed before the full
adaptive decision boundary, including its independent third route, can exist.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import pairwise

from sqpack.fractional.certificate import Certificate, ceiling_side, d4_images
from sqpack.fractional.model import Atom, rotation_from_half_tangent
from sqpack.fractional.sweep import minimum_covered_mass


@dataclass(frozen=True, slots=True)
class AngleCell:
    """One closed mismatch interval; interior seams belong to the lower index."""

    index: int
    half_tangent: Fraction
    lower_boundary_tangent: Fraction
    upper_boundary_tangent: Fraction
    max_mismatch_tangent: Fraction
    square_side: Fraction


def derive_cells(
    half_tangents: tuple[Fraction, ...], square_sides: tuple[Fraction, ...]
) -> tuple[AngleCell, ...]:
    """Derive BC-230 seams and endpoint mismatches without sampling angles."""
    if len(half_tangents) < 2 or len(square_sides) != len(half_tangents):
        raise ValueError("each direction needs one core side, with at least two directions")
    if not all(isinstance(value, Fraction) for value in (*half_tangents, *square_sides)):
        raise ValueError("half-tangents and core sides must be exact Fractions")
    if half_tangents[0] != 0 or any(t < 0 or t >= 1 for t in half_tangents):
        raise ValueError("half-tangents must start at zero and lie in [0, 1)")
    if any(left >= right for left, right in pairwise(half_tangents)):
        raise ValueError("half-tangents must be strictly increasing")
    previous, final = half_tangents[-2:]
    if previous * previous + 2 * previous - 1 >= 0 or final * final + 2 * final - 1 < 0:
        raise ValueError("the final directions must bracket the folded endpoint")
    seams = (
        Fraction(0),
        *((left + right) / (1 - left * right) for left, right in pairwise(half_tangents)),
        Fraction(1),
    )
    if seams[-2] >= 1:
        raise ValueError("the final seam must lie strictly before the folded endpoint")
    if any(left >= right for left, right in pairwise(seams)):
        raise ValueError("derived seams must be strictly increasing")
    cells = []
    for index, (tangent, side) in enumerate(zip(half_tangents, square_sides, strict=True)):
        direction_tangent = 2 * tangent / (1 - tangent * tangent)
        lower, upper = seams[index : index + 2]
        mismatch = max(
            abs(direction_tangent - boundary) / (1 + direction_tangent * boundary)
            for boundary in (lower, upper)
        )
        cells.append(AngleCell(index, tangent, lower, upper, mismatch, side))
    return tuple(cells)


def validate_cells(cells: tuple[AngleCell, ...]) -> None:
    """Check declared geometry and the strict conservative containment rule."""
    if any(
        type(cell.index) is not int or cell.index != index for index, cell in enumerate(cells)
    ):
        raise ValueError("angle-cell indices must be contiguous from zero")
    expected = derive_cells(
        tuple(cell.half_tangent for cell in cells), tuple(cell.square_side for cell in cells)
    )
    for cell, derived in zip(cells, expected, strict=True):
        if cell != derived:
            raise ValueError(f"cell {cell.index} differs from its derived seam or mismatch")
        if cell.square_side <= 0:
            raise ValueError(f"cell {cell.index} needs a positive core side")
        if cell.square_side * (1 + cell.max_mismatch_tangent) >= 1:
            raise ValueError(f"strict containment fails in cell {cell.index}")


def owner_cell(cells: tuple[AngleCell, ...], folded_tangent: Fraction) -> int:
    """Select the unique lower-index owner, including the axis and folded endpoint."""
    validate_cells(cells)
    if not isinstance(folded_tangent, Fraction) or not 0 <= folded_tangent <= 1:
        raise ValueError("the folded tangent must be an exact value in [0, 1]")
    return next(cell.index for cell in cells if folded_tangent <= cell.upper_boundary_tangent)


@dataclass(frozen=True, slots=True)
class AdaptiveCertificate:
    """An in-memory control object, not a frozen or retainable certificate."""

    n: int
    outer_side: Fraction
    atoms: tuple[Atom, ...]
    cells: tuple[AngleCell, ...]
    symmetry: str = "D4"

    def __post_init__(self) -> None:
        if type(self.n) is not int or self.n < 1:
            raise ValueError("n must be a positive integer")
        if not isinstance(self.outer_side, Fraction) or self.outer_side <= 0:
            raise ValueError("the outer side must be a positive Fraction")
        validate_cells(self.cells)
        if self.symmetry != "D4":
            raise ValueError("only D4 symmetry is supported")
        weights: dict[tuple[Fraction, Fraction], Fraction] = {}
        for atom in self.atoms:
            if not all(isinstance(value, Fraction) for value in (atom.x, atom.y, atom.weight)):
                raise ValueError("atom coordinates and weights must be exact Fractions")
            if atom.weight < 0:
                raise ValueError("atom weights must be nonnegative")
            if not (0 <= atom.x <= self.outer_side and 0 <= atom.y <= self.outer_side):
                raise ValueError("atom support must lie inside the container")
            if (atom.x, atom.y) in weights:
                raise ValueError("atom sites must be distinct")
            weights[atom.x, atom.y] = atom.weight
        for site, weight in weights.items():
            if any(weights.get(image) != weight for image in d4_images(*site, self.outer_side)):
                raise ValueError(
                    "listed atom domain must contain complete equal-weight D4 orbits"
                )
        if self.total_mass >= self.n:
            raise ValueError("total mass must be strictly below n")
        if self.outer_side > ceiling_side(self.n, self.cells[0].square_side):
            raise ValueError("the adaptive axis-core method ceiling is exceeded")

    @property
    def total_mass(self) -> Fraction:
        return sum((atom.weight for atom in self.atoms), start=Fraction(0))


def specialize_scalar(certificate: Certificate) -> AdaptiveCertificate:
    """Copy a canonical scalar net into memory without migrating its source bytes.

    Noncanonical legacy nets remain the scalar route's responsibility; a refusal
    here does not replace that route's verdict.
    """
    return AdaptiveCertificate(
        certificate.n,
        certificate.outer_side,
        certificate.atoms,
        derive_cells(
            certificate.half_tangents,
            (certificate.square_side,) * len(certificate.half_tangents),
        ),
        certificate.symmetry,
    )


@dataclass(frozen=True, slots=True)
class DirectionMinimum:
    index: int
    minimum: Fraction
    centre: tuple[Fraction, Fraction]


def sweep_minima(certificate: AdaptiveCertificate) -> tuple[DirectionMinimum, ...]:
    """Run the existing exact event sweep separately for each direction and side.

    Only positive-area center domains are supported in this control slice. Empty
    and singleton domains require an explicit later decision policy; they must not
    be sent to the legacy polygon constructor with reversed or collapsed bounds.
    """
    directions = tuple(
        rotation_from_half_tangent(str(cell.index), cell.half_tangent)
        for cell in certificate.cells
    )
    for cell, direction in zip(certificate.cells, directions, strict=True):
        if cell.square_side * (direction.ux + direction.uy) >= certificate.outer_side:
            raise ValueError(
                f"control sweep requires a positive-area centre domain in cell {cell.index}"
            )
    results = []
    for cell, direction in zip(certificate.cells, directions, strict=True):
        minimum, centre = minimum_covered_mass(
            certificate.atoms, direction, certificate.outer_side, cell.square_side
        )
        results.append(DirectionMinimum(cell.index, minimum, centre))
    return tuple(results)
