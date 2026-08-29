"""From a certified pose box to outward-rounded square corner boxes.

The Krawczyk operator certifies a box of *unknowns* -- a side, some angles, whatever
the contact system was written in.  Nothing downstream can use that directly: the
separating-axis test wants corners.  This module is the map between them, and it is
where the enclosure either survives or is quietly lost.

Two rules, and neither is negotiable:

- **every operation stays in interval arithmetic.**  Converting a certified endpoint to
  a float to build a corner throws the certificate away and leaves something that looks
  exactly like it.
- **the map is the source's map.**  `n = 29`'s provenance SVG writes its `<use>`
  transforms symbolically in the same unknowns as its equations, so the layout is
  transcribed, not reinvented.  A layout map that disagrees with the system it was
  certified against certifies a different packing than the one on the page.

**Squares are unit squares by construction here, and that is deliberate.**
:func:`sqpack.verify.check_unit_squares` asks whether each edge has length exactly one,
which under intervals is a question no enclosure of positive width can answer -- the
edge-length enclosure contains one and is not the degenerate `[1, 1]`, so the sign
refuses.  Building each square from a centre and an angle makes it a unit square as a
matter of construction rather than of measurement, which is why the interval verifier
runs with shape checking off and says so.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from decimal import ROUND_CEILING, ROUND_FLOOR, Decimal, localcontext
from typing import Any

import mpmath as mp

from sqpack.promote.interval import Interval, cos, from_endpoints, interval, sin

# A pose is (centre x, centre y, angle); a layout map turns unknowns into a list of
# them, in the order the source draws its squares.
Pose = tuple[Interval, Interval, Interval]
LayoutMap = Callable[..., Sequence[Pose]]

Corner = tuple[Interval, Interval]
SquareBox = list[Corner]

HALF = "0.5"


def corners_from_pose(centre_x: Interval, centre_y: Interval, angle: Interval) -> SquareBox:
    """The four corner enclosures of a unit square at this pose.

    The same half-edge construction :func:`sqpack.verify.corners_from_poses` uses,
    carried out in interval arithmetic so the corners enclose every square the pose box
    admits.  Corner order matches that function's, because
    :func:`sqpack.verify.edge_axes` reads corners `0`, `1` and `2` to find the edge
    normals and would produce the wrong axes from any other order.
    """
    half = interval(HALF)
    cosine, sine = cos(angle), sin(angle)
    ux, uy = half * cosine, half * sine
    vx, vy = -(half * sine), half * cosine
    return [
        (centre_x - ux - vx, centre_y - uy - vy),
        (centre_x + ux - vx, centre_y + uy - vy),
        (centre_x + ux + vx, centre_y + uy + vy),
        (centre_x - ux + vx, centre_y - uy + vy),
    ]


def enclose_layout(layout: LayoutMap, unknowns: Sequence[Interval]) -> list[SquareBox]:
    """Push a certified box through `layout` to one corner box per square."""
    poses = layout(*unknowns)
    boxes = []
    for index, pose in enumerate(poses):
        if len(pose) != 3:
            raise ValueError(
                f"square {index}: a pose is (x, y, angle); got {len(pose)} components"
            )
        boxes.append(corners_from_pose(*pose))
    return boxes


def corner_span(squares: Sequence[SquareBox]) -> tuple[Interval, Interval]:
    """The outward-rounded x and y extents of every corner in the layout.

    Useful before verifying: a layout whose extent already exceeds the side under test
    has no chance of certifying, and saying so costs one pass instead of `n(n-1)/2`
    pair tests.
    """
    xs = [value for square in squares for value, _ in square]
    ys = [value for square in squares for _, value in square]
    return (
        from_endpoints(min(mp.mpf(v.a) for v in xs), max(mp.mpf(v.b) for v in xs)),
        from_endpoints(min(mp.mpf(v.a) for v in ys), max(mp.mpf(v.b) for v in ys)),
    )


def widen(squares: Sequence[SquareBox], amount: str) -> list[SquareBox]:
    """Every corner enclosure inflated by `amount` on each side.

    A deliberate way to make a layout less decidable without changing the packing it
    describes, so a control can prove the verifier refuses when the enclosures grow
    rather than passing on a coincidence.
    """
    pad = interval(f"-{amount}", amount)
    return [[(x + pad, y + pad) for x, y in square] for square in squares]


def enclose_field_squares(
    field: Any, squares: Sequence[Sequence[tuple]], side: Any, *, digits: int = 40
) -> tuple[list[SquareBox], Interval]:
    """Bridge an exactly-constructed packing into enclosures, losing nothing.

    The exact cases -- Göbel's `n = 5` and `n = 10`, Trump's `n = 11` -- carry corners
    as elements of a certified number field, which is a stronger representation than
    anything this route produces.  Certifying one of them by interval arithmetic is
    therefore not an upgrade; it is a **calibration**, and the point is that the two
    routes have to agree where both can speak.

    `NumberField.enclose` supplies a rigorous rational enclosure of each element, so the
    conversion is an exact widening rather than an evaluation: nothing here can report a
    corner the exact arithmetic does not admit.
    """
    field.refine_to(digits + 8)

    def as_interval(element) -> Interval:
        low, high = field.enclose(element)
        return from_endpoints(
            decimal_of(low, digits, upward=False), decimal_of(high, digits, upward=True)
        )

    boxes = [[(as_interval(x), as_interval(y)) for x, y in square] for square in squares]
    return boxes, as_interval(side)


def decimal_of(value, digits: int, *, upward: bool) -> str:
    """A rational rounded strictly outward to a decimal string.

    The same discipline as :func:`sqpack.promote.interval.decimal_string`, for the exact
    rationals a number field produces rather than for `mpmath` floats.  Rounding these
    to nearest would narrow an enclosure that was rigorous when it left the field, which
    is the one way this bridge could lose what it was built to preserve.
    """
    with localcontext() as context:
        context.prec = max(1, digits)
        context.rounding = ROUND_CEILING if upward else ROUND_FLOOR
        return str(Decimal(value.numerator) / Decimal(value.denominator))
