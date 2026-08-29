"""The `n = 29` layout map, as a function of the unknowns rather than of the printed digits.

:func:`cases.kingbird29.verify_svg.materialise_svg` already builds this packing's 29
squares from the source SVG.  What it cannot do is build them from a *box*: the XML
parser substitutes each `&a;` with the decimal the source prints, so the squares it
returns are the ones at the published pose and nowhere else.

Interval certification needs the other thing.  A certified pose box has to be pushed
through the layout to corner boxes, which means the transforms have to stay written in
the unknowns until the moment they are evaluated.

**Nothing here is a new transcription.**  The transforms are the source's, read from the
same file; the only change is that entity references survive parsing as markers instead
of being replaced with digits.  Every entity resolves from the six unknowns:
`s, a, b, c, d, i` are the unknowns themselves, and the nine slide scalars `r1 … rD` are
already closed forms in them, supplied by
:func:`cases.kingbird29.system.slide_scalars`.

The risk this design carries is drift between the two walks, so it is pinned rather than
argued away: :func:`agrees_with_materialised` evaluates this layout at the *published*
entity values and requires it to reproduce `materialise_svg` corner for corner.  If the
two ever disagree, that check fails before any certificate is built on the difference.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

import mpmath as mp

from cases.kingbird29 import system
from cases.kingbird29.verify_svg import (
    ENTITY_RE,
    SVG,
    XLINK_HREF,
    apply,
    compose,
    identity,
    integer,
    local_square,
    materialise_svg,
    parse_transform,
    unit_cells_from_path,
)

#: An entity reference becomes this once the DTD is dropped.  Chosen because `#` and the
#: entity name are inert to both the XML parser and the transform grammar, so a marker
#: reaches `parse_transform` intact and is impossible to mistake for a number.
MARKER = "#{}#"
MARKER_RE = re.compile(r"([-+]?)#([A-Za-z][A-Za-z0-9]*)#")

#: Numbers *or* markers, in the order the transform grammar expects its arguments.
#:
#: The leading sign is part of the marker alternative and not optional decoration.  The
#: source writes `rotate(-&a;)` as often as `rotate(&a;)`, and a pattern that matched the
#: marker alone skipped past the minus and silently rotated the other way -- which
#: mirrors a square about its own rotation centre and still produces a plausible-looking
#: packing. `agrees_with_materialised` caught it at square 15.
TOKEN_RE = re.compile(r"[-+]?#[A-Za-z][A-Za-z0-9]*#|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")

DEFAULT_SOURCE = Path("resources/papers/kingbird-square-29-provenance.svg")


class LayoutError(ValueError):
    """A typed failure building or evaluating the layout map."""

    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = kind


def markered_document(source: Path) -> tuple[str, dict[str, str]]:
    """The SVG body with entity references preserved as markers, and the entity table.

    The internal DTD subset is removed rather than kept, because an XML parser that can
    see the declarations will expand the references and there is no portable way to ask
    it not to.
    """
    text = source.read_text(encoding="utf-8")
    entities = dict(ENTITY_RE.findall(text))
    if not entities:
        raise LayoutError("no-entities", f"{source} declares no entity table")
    start = text.find("<svg")
    if start < 0:
        raise LayoutError("no-svg-element", f"{source} has no <svg> element")
    body = text[start:]
    for name in entities:
        body = body.replace(f"&{name};", MARKER.format(name))
    leftover = re.search(r"&[A-Za-z][A-Za-z0-9]*;", body)
    if leftover:
        raise LayoutError(
            "unresolved-entity",
            f"{leftover.group(0)} survives marker substitution, so the layout would be "
            "evaluated with an entity this map cannot supply",
        )
    return body, entities


def entity_values(unknowns: Sequence[Any]) -> dict[str, Any]:
    """Every entity the transforms reference, as a value in the caller's scalar type.

    The six unknowns pass through; the nine slide scalars come from the source's own
    closed forms.  So a caller supplying interval duals gets interval duals back for all
    fifteen, and the layout below never sees a printed digit.
    """
    if len(unknowns) != len(system.UNKNOWNS):
        raise LayoutError(
            "bad-request",
            f"{len(unknowns)} values against {len(system.UNKNOWNS)} unknowns {system.UNKNOWNS}",
        )
    values: dict[str, Any] = dict(zip(system.UNKNOWNS, unknowns, strict=True))
    values.update(system.slide_scalars(*unknowns))
    return values


def _resolver(values: dict[str, Any]) -> Callable[[str], Any]:
    def resolve(token: str) -> Any:
        marker = MARKER_RE.fullmatch(token)
        if marker is None:
            return mp.mpf(token)
        sign, name = marker.group(1), marker.group(2)
        if name not in values:
            raise LayoutError(
                "unknown-entity",
                f"the layout references &{name}; and no value was supplied for it",
            )
        value = values[name]
        return -value if sign == "-" else value

    return resolve


def squares_at(source: Path, unknowns: Sequence[Any]) -> list[list[tuple[Any, Any]]]:
    """The 29 squares as corner lists, evaluated at `unknowns`.

    Hand it floats and it reproduces the published packing; hand it interval duals and
    it returns corner enclosures over the whole box, which is what a certificate needs.
    """
    body, _ = markered_document(source)
    resolve = _resolver(entity_values(unknowns))
    root = ET.fromstring(body)
    squares: list[list[tuple[Any, Any]]] = []

    def visit(node, parent_matrix) -> None:
        tag = node.tag.removeprefix(SVG)
        if tag == "defs":
            return
        matrix = compose(
            parent_matrix,
            parse_transform(node.attrib.get("transform"), scalar=resolve, tokens=TOKEN_RE),
        )
        style = re.sub(r"\s", "", node.attrib.get("style", ""))
        if tag == "use" and node.attrib.get(XLINK_HREF) == "#one":
            squares.append([apply(matrix, point) for point in local_square(0, 0)])
        elif tag == "path" and "fill:none" not in style:
            for x, y in unit_cells_from_path(node.attrib["d"]):
                squares.append([apply(matrix, point) for point in local_square(x, y)])
        elif tag == "rect" and "fill:none" not in style:
            x = integer(mp.mpf(node.attrib.get("x", "0")))
            y = integer(mp.mpf(node.attrib.get("y", "0")))
            width = integer(mp.mpf(node.attrib["width"]))
            height = integer(mp.mpf(node.attrib["height"]))
            squares.extend(
                [apply(matrix, point) for point in local_square(cell_x, cell_y)]
                for cell_y in range(y, y + height)
                for cell_x in range(x, x + width)
            )
        for child in node:
            visit(child, matrix)

    visit(root, identity())
    return squares


def layout_map(source: Path = DEFAULT_SOURCE) -> Callable[..., list]:
    """A `(s, a, b, c, d, i) -> squares` map, ready for interval propagation."""

    def layout(*unknowns) -> list:
        return squares_at(source, unknowns)

    return layout


def agrees_with_materialised(source: Path = DEFAULT_SOURCE, *, digits: int = 40) -> int:
    """Reproduce `materialise_svg` from this map at the published pose, corner for corner.

    The known-answer check that keeps the two walks from drifting.  It returns the number
    of squares compared so a caller can assert on it rather than on a bare boolean, and
    raises :class:`LayoutError` naming the first corner that disagrees.
    """
    previous = mp.mp.dps
    mp.mp.dps = digits + 20
    try:
        _raw, _entities, _side, published = materialise_svg(source)
        squares = squares_at(source, [mp.mpf(v) for v in system.seed(source)])
        if len(squares) != len(published):
            raise LayoutError(
                "square-count-differs",
                f"the symbolic walk found {len(squares)} squares against "
                f"{len(published)} from the numeric one",
            )
        tolerance = mp.mpf(10) ** (-digits)
        for index, (mine, theirs) in enumerate(zip(squares, published, strict=True)):
            for corner, (here, there) in enumerate(zip(mine, theirs, strict=True)):
                for axis, (one, other) in enumerate(zip(here, there, strict=True)):
                    if abs(one - other) > tolerance:
                        raise LayoutError(
                            "corner-differs",
                            f"square {index} corner {corner} axis {axis}: symbolic walk "
                            f"gives {mp.nstr(one, 20)} against {mp.nstr(other, 20)}",
                        )
        return len(squares)
    finally:
        mp.mp.dps = previous
