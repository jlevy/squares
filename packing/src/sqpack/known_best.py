"""Source-faithful normalization for the retained known-best packing corpus."""

from __future__ import annotations

import html
import json
import re
from collections.abc import Mapping
from copy import deepcopy
from dataclasses import dataclass
from fractions import Fraction
from itertools import pairwise
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

import mpmath as mp

from sqpack.witness import numerical_check

KINGBIRD_BASE_URL = "https://kingbird.myphotos.cc/packing"
UNITSQUARE_BASE_URL = "https://hmbelvedere.com/packings"
NORMALIZATION_DIGITS = 100
CHECK_DIGITS = 120
KINGBIRD_TOLERANCE = "1e-8"
UNITSQUARE_TOLERANCE = "2e-6"
RETRIEVED_DATE = "2026-08-26"
KINGBIRD_ATTRIBUTION = (
    "SVG and high-precision updates by David Ellsworth; catalogue based on "
    "Erich Friedman's original compilation."
)
KINGBIRD_LICENSE_STATUS = "no-express-reuse-terms-found"

KINGBIRD_RETENTION_POLICY = "metadata-and-derived-numerical-facts-only"
"""What this repository keeps from a source that states no reuse terms, and why.

The inspected catalogue page states no express reuse terms, so the raw source assets are
not retained -- the 34 Kingbird SVG paths were removed rather than committed -- while
attributed metadata and numerical facts *derived* from them are. This is a retention
policy, not a legal conclusion, and it is deliberately conservative in the direction that
costs this project effort rather than the direction that costs the source anything.

**The criterion this label was missing, which is what it permits and what would move a
record out of it.** The policy is about *dependence on the source*, not about the
assurance level of the record. So:

- A record whose numbers are transcribed from the source stays under this policy however
  they are re-expressed. Re-encoding a transcription into a number field does not make it
  less derived from what it was transcribed from, and promoting one on that basis would
  be relabelling provenance rather than changing it.
- A record whose numbers are *recomputed from a published mathematical rule*, without
  reading the source at all, is not under this policy, because it does not depend on the
  source. It is first-party work that happens to agree with a retained record, and the
  agreement is a check on both rather than a derivation of either.

`cases/gobel_family` and `cases/gobel40` are the second kind and can be checked to be:
neither module imports `load_witness` or names `witnesses/`, and both build from
`[Friedman DS7]` section 2's statement of Goebel's rule. The retained witnesses at
`n = 5, 40, 65, 89` agree with them to those witnesses' own rounding, which identifies
what the witnesses are without being how the constructions were made.

The consequence for promoting a witness to `exact-algebraic` is therefore decidable
rather than a judgement: it is available exactly where a construction independent of the
source exists, and unavailable where the only route is the source's own numbers. What
this does not settle, and what no rule here can, is whether the underlying licensing
assessment is right -- that is a review decision, and this criterion assumes it rather
than revisiting it.
"""

_NUMBER = r"[-+]?(?:(?:\d+(?:\.\d*)?)|(?:\.\d+))(?:[eE][-+]?\d+)?"
_PATH_TOKEN = re.compile(rf"[MmLlHhVvZz]|{_NUMBER}")
_TRANSFORM = re.compile(r"([A-Za-z]+)\s*\(([^)]*)\)")
_ALLOWED_PATH_COMMANDS = frozenset("MmLlHhVvZz")


class SourceGeometryError(ValueError):
    """A typed failure to recover complete unit-square geometry from a source asset."""

    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = kind


@dataclass(frozen=True)
class Affine:
    """One SVG affine transform in column-vector convention."""

    a: Any
    b: Any
    c: Any
    d: Any
    e: Any
    f: Any

    @classmethod
    def identity(cls) -> Affine:
        return cls(mp.mpf(1), mp.mpf(0), mp.mpf(0), mp.mpf(1), mp.mpf(0), mp.mpf(0))

    def multiply(self, other: Affine) -> Affine:
        """Return ``self * other``, matching SVG transform-list composition."""
        return Affine(
            self.a * other.a + self.c * other.b,
            self.b * other.a + self.d * other.b,
            self.a * other.c + self.c * other.d,
            self.b * other.c + self.d * other.d,
            self.a * other.e + self.c * other.f + self.e,
            self.b * other.e + self.d * other.f + self.f,
        )

    def point(self, x: Any, y: Any) -> tuple[Any, Any]:
        return self.a * x + self.c * y + self.e, self.b * x + self.d * y + self.f


@dataclass(frozen=True)
class SquarePose:
    """A unit-square pose normalized to lower-left, y-up coordinates."""

    center_x: str
    center_y: str
    angle_degrees: str


@dataclass(frozen=True)
class KingbirdGeometry:
    side: str
    poses: tuple[SquarePose, ...]


@dataclass(frozen=True)
class UnitSquareGeometry:
    side: str
    upstream_declared_parent_content_sha256: str
    squares: tuple[tuple[tuple[str, str], ...], ...]


def _local_name(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def _numeric_list(text: str) -> list[Any]:
    return [mp.mpf(value) for value in re.findall(_NUMBER, text)]


def _translation(x: Any, y: Any = 0) -> Affine:
    return Affine(mp.mpf(1), mp.mpf(0), mp.mpf(0), mp.mpf(1), x, y)


def _rotation(angle_degrees: Any) -> Affine:
    radians = angle_degrees * mp.pi / 180
    cosine, sine = mp.cos(radians), mp.sin(radians)
    return Affine(cosine, sine, -sine, cosine, mp.mpf(0), mp.mpf(0))


def _parse_transform(text: str | None) -> Affine:
    result = Affine.identity()
    if not text:
        return result
    consumed = ""
    for match in _TRANSFORM.finditer(text):
        consumed += match.group(0)
        name = match.group(1)
        values = _numeric_list(match.group(2))
        if name == "translate" and values:
            transform = _translation(values[0], values[1] if len(values) > 1 else mp.mpf(0))
        elif name == "rotate" and values:
            transform = _rotation(values[0])
            if len(values) == 3:
                transform = (
                    _translation(values[1], values[2])
                    .multiply(transform)
                    .multiply(_translation(-values[1], -values[2]))
                )
            elif len(values) != 1:
                raise SourceGeometryError("unsupported-transform", f"invalid rotate: {text}")
        elif name == "scale" and values:
            scale_y = values[1] if len(values) > 1 else values[0]
            transform = Affine(values[0], mp.mpf(0), mp.mpf(0), scale_y, mp.mpf(0), mp.mpf(0))
        elif name == "matrix" and len(values) == 6:
            transform = Affine(*values)
        else:
            raise SourceGeometryError(
                "unsupported-transform", f"unsupported SVG transform {name!r}: {text}"
            )
        result = result.multiply(transform)
    remainder = re.sub(r"[\s,]", "", text)
    parsed = re.sub(r"[\s,]", "", consumed)
    if remainder != parsed:
        raise SourceGeometryError("unsupported-transform", f"cannot parse transform: {text}")
    return result


def _same(left: Any, right: Any, tolerance: Any) -> bool:
    return abs(left - right) <= tolerance


def _parse_path(data: str, tolerance: Any) -> list[list[tuple[Any, Any]]]:
    commands = set(re.findall(r"[A-Za-z]", data))
    unsupported = commands - _ALLOWED_PATH_COMMANDS
    if unsupported:
        raise SourceGeometryError(
            "unsupported-path", f"path uses unsupported commands {sorted(unsupported)}"
        )
    tokens = _PATH_TOKEN.findall(data)
    paths: list[list[tuple[Any, Any]]] = []
    current: list[tuple[Any, Any]] = []
    x = y = start_x = start_y = mp.mpf(0)
    command: str | None = None
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token in _ALLOWED_PATH_COMMANDS:
            command = token
            index += 1
            if token in "Zz":
                if current and not (
                    _same(x, start_x, tolerance) and _same(y, start_y, tolerance)
                ):
                    current.append((start_x, start_y))
                x, y = start_x, start_y
                command = None
            continue
        if command is None:
            raise SourceGeometryError("malformed-path", f"number without command in {data!r}")
        if command in "MmLl":
            if index + 1 >= len(tokens):
                raise SourceGeometryError(
                    "malformed-path", f"truncated coordinate pair: {data}"
                )
            next_x, next_y = mp.mpf(tokens[index]), mp.mpf(tokens[index + 1])
            index += 2
            if command in "ml":
                next_x += x
                next_y += y
            if command in "Mm":
                if current:
                    paths.append(current)
                current = []
                start_x, start_y = next_x, next_y
                command = "l" if command == "m" else "L"
            x, y = next_x, next_y
            current.append((x, y))
        elif command in "Hh":
            next_x = mp.mpf(tokens[index])
            index += 1
            x = x + next_x if command == "h" else next_x
            current.append((x, y))
        elif command in "Vv":
            next_y = mp.mpf(tokens[index])
            index += 1
            y = y + next_y if command == "v" else next_y
            current.append((x, y))
    if current:
        paths.append(current)
    return paths


def _remove_collinear(vertices: list[tuple[Any, Any]], tolerance: Any) -> list[tuple[Any, Any]]:
    cleaned: list[tuple[Any, Any]] = []
    for vertex in vertices:
        if not cleaned or not (
            _same(vertex[0], cleaned[-1][0], tolerance)
            and _same(vertex[1], cleaned[-1][1], tolerance)
        ):
            cleaned.append(vertex)
    if (
        len(cleaned) > 1
        and _same(cleaned[0][0], cleaned[-1][0], tolerance)
        and _same(cleaned[0][1], cleaned[-1][1], tolerance)
    ):
        cleaned.pop()
    if len(cleaned) < 3:
        return cleaned
    result: list[tuple[Any, Any]] = []
    for index, current in enumerate(cleaned):
        previous = cleaned[index - 1]
        following = cleaned[(index + 1) % len(cleaned)]
        same_x = _same(previous[0], current[0], tolerance) and _same(
            current[0], following[0], tolerance
        )
        same_y = _same(previous[1], current[1], tolerance) and _same(
            current[1], following[1], tolerance
        )
        if not same_x and not same_y:
            result.append(current)
    return result


type Interval = tuple[Any, Any]
type Band = tuple[Any, Any, list[Interval]]


def _region_from_paths(
    paths: list[list[tuple[Any, Any]]], fill_rule: str, tolerance: Any
) -> list[Band]:
    polygons = [
        cleaned for path in paths if len(cleaned := _remove_collinear(path, tolerance)) >= 3
    ]
    y_coordinates = sorted({point[1] for polygon in polygons for point in polygon})
    region: list[Band] = []
    for y_start, y_end in pairwise(y_coordinates):
        test_y = (y_start + y_end) / 2
        crossings: list[tuple[Any, int]] = []
        for polygon in polygons:
            for index, first in enumerate(polygon):
                second = polygon[(index + 1) % len(polygon)]
                if (first[1] < test_y < second[1]) or (second[1] < test_y < first[1]):
                    direction = 1 if second[1] > first[1] else -1
                    if _same(first[0], second[0], tolerance):
                        crossing_x = first[0]
                    else:
                        ratio = (test_y - first[1]) / (second[1] - first[1])
                        crossing_x = first[0] + ratio * (second[0] - first[0])
                    crossings.append((crossing_x, direction))
        crossings.sort(key=lambda item: item[0])
        intervals: list[Interval] = []
        if fill_rule == "evenodd":
            intervals.extend(
                (crossings[index][0], crossings[index + 1][0])
                for index in range(0, len(crossings) - 1, 2)
            )
        else:
            winding = 0
            interval_start = None
            for crossing_x, direction in crossings:
                previous = winding
                winding += direction
                if previous == 0 and winding != 0:
                    interval_start = crossing_x
                elif previous != 0 and winding == 0 and interval_start is not None:
                    intervals.append((interval_start, crossing_x))
                    interval_start = None
        if intervals:
            region.append((y_start, y_end, intervals))
    return region


def _region_empty(region: list[Band], tolerance: Any) -> bool:
    return not any(
        right - left > tolerance and y_end - y_start > tolerance
        for y_start, y_end, intervals in region
        for left, right in intervals
    )


def _square_in_region(x: Any, y: Any, region: list[Band], tolerance: Any) -> bool:
    covered = mp.mpf(0)
    for y_start, y_end, intervals in region:
        overlap_start, overlap_end = max(y, y_start), min(y + 1, y_end)
        if overlap_end <= overlap_start + tolerance:
            continue
        if any(
            left <= x + tolerance and right >= x + 1 - tolerance for left, right in intervals
        ):
            covered += overlap_end - overlap_start
    return covered >= 1 - tolerance


def _corner_square(region: list[Band], tolerance: Any) -> tuple[Any, Any] | None:
    corners = [
        corner
        for y_start, y_end, intervals in region
        for left, right in intervals
        for corner in ((left, y_start), (right, y_start), (left, y_end), (right, y_end))
    ]
    for x, y in corners:
        if _square_in_region(x, y, region, tolerance):
            return x, y
    for x, y in corners:
        for delta_x, delta_y in ((-1, 0), (0, -1), (-1, -1)):
            if _square_in_region(x + delta_x, y + delta_y, region, tolerance):
                return x + delta_x, y + delta_y
    return None


def _subtract_square(region: list[Band], x: Any, y: Any, tolerance: Any) -> list[Band]:
    result: list[Band] = []
    for y_start, y_end, intervals in region:
        if y_end <= y + tolerance or y_start >= y + 1 - tolerance:
            result.append((y_start, y_end, list(intervals)))
            continue
        if y_start < y - tolerance:
            result.append((y_start, y, list(intervals)))
        overlap_start, overlap_end = max(y_start, y), min(y_end, y + 1)
        remaining: list[Interval] = []
        for left, right in intervals:
            if right <= x + tolerance or left >= x + 1 - tolerance:
                remaining.append((left, right))
            else:
                if left < x - tolerance:
                    remaining.append((left, x))
                if right > x + 1 + tolerance:
                    remaining.append((x + 1, right))
        if remaining and overlap_end > overlap_start + tolerance:
            result.append((overlap_start, overlap_end, remaining))
        if y_end > y + 1 + tolerance:
            result.append((y + 1, y_end, list(intervals)))
    return result


def _path_centers(data: str, fill_rule: str, tolerance: Any) -> list[tuple[Any, Any]]:
    region = _region_from_paths(_parse_path(data, tolerance), fill_rule, tolerance)
    centers: list[tuple[Any, Any]] = []
    for _ in range(10_000):
        if _region_empty(region, tolerance):
            return centers
        corner = _corner_square(region, tolerance)
        if corner is None:
            break
        region = _subtract_square(region, corner[0], corner[1], tolerance)
        centers.append((corner[0] + mp.mpf("0.5"), corner[1] + mp.mpf("0.5")))
    raise SourceGeometryError("non-tileable-path", "path leaves a non-unit-square residue")


def _format(value: Any, digits: int = NORMALIZATION_DIGITS) -> str:
    if abs(value) < mp.mpf(10) ** (-(digits - 10)):
        return "0"
    return str(
        mp.nstr(
            value,
            digits,
            strip_zeros=True,
            min_fixed=-10_000,
            max_fixed=10_000,
        )
    )


def _has_fill_none(element: ET.Element, *, inherited: bool) -> bool:
    style = re.sub(r"\s+", "", element.get("style", "")).lower()
    fill = element.get("fill", "").replace(" ", "").lower()
    return inherited or "fill:none" in style or fill == "none"


def parse_kingbird_svg(text: str, *, expected_n: int | None = None) -> KingbirdGeometry:
    """Recover every intended unit square from a supplied Kingbird catalogue SVG."""
    with mp.workdps(NORMALIZATION_DIGITS + 40):
        try:
            root = ET.fromstring(text)
        except ET.ParseError as error:
            raise SourceGeometryError("malformed-svg", str(error)) from error
        definitions: dict[str, ET.Element] = {}
        for element in root.iter():
            if identifier := element.get("id"):
                # Kingbird has a few invalid duplicate IDs. DOM getElementById resolves
                # the first element in tree order, so mirror that recovery behavior.
                definitions.setdefault(identifier, element)
        outer = definitions.get("outer")
        if outer is None or _local_name(outer) != "rect":
            raise SourceGeometryError("outer-frame-missing", "expected a rectangular #outer")
        tolerance = mp.mpf("1e-70")
        try:
            side = mp.mpf(outer.get("width", ""))
            outer_height = mp.mpf(outer.get("height", ""))
        except ValueError as error:
            raise SourceGeometryError(
                "outer-frame-malformed", "outer frame needs numeric width and height"
            ) from error
        if side <= 0 or not _same(side, outer_height, tolerance):
            raise SourceGeometryError(
                "outer-frame-not-square", "outer frame needs equal positive dimensions"
            )
        outer_x = mp.mpf(outer.get("x", "0"))
        outer_y = mp.mpf(outer.get("y", "0"))
        extracted: list[tuple[Any, Any, Any]] = []
        ignored_bare_local_references: list[str] = []

        def add_center(x: Any, y: Any, transform: Affine) -> None:
            center_x, center_y = transform.point(x, y)
            column_norm = mp.sqrt(transform.a * transform.a + transform.b * transform.b)
            other_norm = mp.sqrt(transform.c * transform.c + transform.d * transform.d)
            orthogonality = transform.a * transform.c + transform.b * transform.d
            if (
                abs(column_norm - 1) > mp.mpf("1e-25")
                or abs(other_norm - 1) > mp.mpf("1e-25")
                or abs(orthogonality) > mp.mpf("1e-25")
            ):
                raise SourceGeometryError(
                    "non-rigid-transform", "source square transform is not an isometry"
                )
            angle = mp.degrees(mp.atan2(-transform.b, transform.a)) % 90
            if min(abs(angle), abs(angle - 90)) < mp.mpf("1e-70"):
                angle = mp.mpf(0)
            extracted.append((center_x - outer_x, outer_y + side - center_y, angle))

        active_references: set[str] = set()

        def process(  # noqa: PLR0911
            element: ET.Element,
            inherited_transform: Affine,
            *,
            inherited_fill_none: bool = False,
        ) -> None:
            tag = _local_name(element)
            if tag in {"defs", "script"}:
                return
            fill_none = _has_fill_none(element, inherited=inherited_fill_none)
            transform = inherited_transform.multiply(_parse_transform(element.get("transform")))
            if tag == "use":
                href = element.get("href") or next(
                    (value for key, value in element.attrib.items() if key.endswith("}href")),
                    "",
                )
                if href == "#outer" or fill_none:
                    return
                if href.startswith("#"):
                    reference = href[1:]
                elif href in definitions and expected_n is not None:
                    # A bare href is not a same-document reference. One Kingbird source
                    # contains such a no-op typo; skip it only when the catalogue count
                    # supplied by the caller can reconcile all remaining geometry.
                    ignored_bare_local_references.append(href)
                    return
                else:
                    raise SourceGeometryError(
                        "broken-reference", f"unresolved SVG use {href!r}"
                    )
                if not reference or reference not in definitions:
                    raise SourceGeometryError(
                        "broken-reference", f"unresolved SVG use {href!r}"
                    )
                if reference in active_references:
                    raise SourceGeometryError(
                        "cyclic-reference", f"cyclic SVG use #{reference}"
                    )
                x, y = mp.mpf(element.get("x", "0")), mp.mpf(element.get("y", "0"))
                active_references.add(reference)
                try:
                    process(
                        definitions[reference],
                        transform.multiply(_translation(x, y)),
                        inherited_fill_none=fill_none,
                    )
                finally:
                    active_references.remove(reference)
                return
            if tag == "g":
                for child in element:
                    process(child, transform, inherited_fill_none=fill_none)
                return
            if fill_none:
                return
            if tag == "rect":
                if element.get("id") == "outer":
                    return
                width, height = (
                    mp.mpf(element.get("width", "0")),
                    mp.mpf(element.get("height", "0")),
                )
                rounded_width, rounded_height = int(mp.nint(width)), int(mp.nint(height))
                if (
                    rounded_width < 1
                    or rounded_height < 1
                    or not _same(width, rounded_width, tolerance)
                    or not _same(height, rounded_height, tolerance)
                ):
                    raise SourceGeometryError(
                        "non-unit-tiling-rect",
                        f"filled rect is not an integer unit-square block: {width} by {height}",
                    )
                x, y = mp.mpf(element.get("x", "0")), mp.mpf(element.get("y", "0"))
                for column in range(rounded_width):
                    for row in range(rounded_height):
                        add_center(
                            x + column + mp.mpf("0.5"),
                            y + row + mp.mpf("0.5"),
                            transform,
                        )
                return
            if tag == "path":
                data = element.get("d")
                if data:
                    for x, y in _path_centers(
                        data, element.get("fill-rule", "nonzero"), tolerance
                    ):
                        add_center(x, y, transform)
                return
            if tag not in {"title", "desc", "metadata", "circle"}:
                raise SourceGeometryError("unsupported-element", f"unsupported filled <{tag}>")

        for child in root:
            process(child, Affine.identity())
        if not extracted:
            raise SourceGeometryError("empty-geometry", "source contains no unit squares")
        if ignored_bare_local_references and len(extracted) != expected_n:
            raise SourceGeometryError(
                "broken-reference",
                "bare local SVG use cannot be ignored because the remaining geometry "
                f"has {len(extracted)} squares, not {expected_n}",
            )
        if expected_n is not None and len(extracted) != expected_n:
            raise SourceGeometryError(
                "square-count-mismatch",
                f"expected {expected_n} squares but extracted {len(extracted)}",
            )
        poses = tuple(
            SquarePose(_format(x), _format(y), _format(angle)) for x, y, angle in extracted
        )
        return KingbirdGeometry(_format(side), poses)


def parse_unitsquare_svg(text: str, *, expected_n: int) -> UnitSquareGeometry:
    """Recover approximate corners from a UnitSquare public evidence rendering."""
    with mp.workdps(NORMALIZATION_DIGITS + 40):
        try:
            root = ET.fromstring(text)
        except ET.ParseError as error:
            raise SourceGeometryError("malformed-svg", str(error)) from error
        metadata_element = next(
            (element for element in root if _local_name(element) == "metadata"), None
        )
        if metadata_element is None or not metadata_element.text:
            raise SourceGeometryError("metadata-missing", "UnitSquare SVG has no metadata")
        try:
            metadata = json.loads(html.unescape(metadata_element.text.strip()))
        except json.JSONDecodeError as error:
            raise SourceGeometryError("metadata-malformed", str(error)) from error
        if (
            metadata.get("schema") != "unitsquare.sota-svg.v1"
            or metadata.get("n") != expected_n
        ):
            raise SourceGeometryError("metadata-mismatch", "unexpected UnitSquare SVG metadata")
        side = mp.mpf(str(metadata["proven_side"]))
        upstream_declared_parent_content_sha256 = str(metadata["source_sha256"])
        frame = next(
            (
                element
                for element in root
                if _local_name(element) == "rect"
                and element.get("x") is not None
                and element.get("y") is not None
                and element.get("width") == element.get("height")
            ),
            None,
        )
        if frame is None:
            raise SourceGeometryError("frame-missing", "UnitSquare SVG has no square frame")
        frame_x, frame_y = mp.mpf(frame.get("x", "")), mp.mpf(frame.get("y", ""))
        frame_size = mp.mpf(frame.get("width", ""))
        squares: list[tuple[tuple[str, str], ...]] = []
        for polygon in root.iter():
            if _local_name(polygon) != "polygon" or polygon.get("data-square-id") is None:
                continue
            values = _numeric_list(polygon.get("points", ""))
            if len(values) != 8:
                raise SourceGeometryError("malformed-polygon", "expected four polygon points")
            corners = []
            for x, y in zip(values[::2], values[1::2], strict=True):
                normalized_x = (x - frame_x) * side / frame_size
                normalized_y = (frame_y + frame_size - y) * side / frame_size
                corners.append((_format(normalized_x), _format(normalized_y)))
            # The y-axis reflection reverses the polygon winding. Restore cyclic CCW
            # order so the shared unit-square checker sees the intended edge sequence.
            squares.append(tuple(reversed(corners)))
        if len(squares) != expected_n:
            raise SourceGeometryError(
                "square-count-mismatch",
                f"expected {expected_n} squares but extracted {len(squares)}",
            )
        return UnitSquareGeometry(
            _format(side), upstream_declared_parent_content_sha256, tuple(squares)
        )


def exact_grid_witness(
    n: int,
    side: int,
    *,
    frontier_path: str,
    witness_id: str | None = None,
    witness_path: str | None = None,
    source_key: str = "E-basic-grid-upper",
    limitations: str | None = None,
) -> dict[str, Any]:
    """Build the canonical row-major exact grid witness for one integer record."""
    if n < 1 or side < 1 or side * side < n:
        raise ValueError("grid witness requires 1 <= n <= side^2")
    squares = []
    for index in range(n):
        x, y = index % side, index // side
        squares.append(
            {
                "id": index + 1,
                "corners": [
                    [str(x), str(y)],
                    [str(x + 1), str(y)],
                    [str(x + 1), str(y + 1)],
                    [str(x), str(y + 1)],
                ],
            }
        )
    witness_id = witness_id or f"W-known-best-n{n:03d}"
    witness_path = witness_path or f"witnesses/known-best/n-{n:03d}.yaml"
    limitations = limitations or (
        "Verifies this known-best upper-bound construction, not uniqueness; "
        "optimality comes only from the separately cited frontier lower bound."
    )
    return {
        "id": witness_id,
        "n": n,
        "side": str(side),
        "square_size": "1",
        "representation": "corners",
        "scalar": {"kind": "rational"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": squares,
        "claim": {
            "coordinate_provenance": "verified",
            "method": "exact-algebraic",
            "limitations": limitations,
        },
        "source": {
            "key": source_key,
            "path": frontier_path,
        },
        "certificate": {
            "kind": "exact-rational-sat",
            "replay": f"uv run --frozen packing-witness verify {witness_path}",
        },
    }


def _checked_witness(
    witness: dict[str, Any], *, tolerance: str, witness_path: str
) -> dict[str, Any]:
    result, report = numerical_check(
        witness,
        method="numerical-multiprecision",
        precision=CHECK_DIGITS,
        tolerance=tolerance,
    )
    if not report.valid:
        first = report.failures[0] if report.failures else "unknown failure"
        raise SourceGeometryError(
            "numerical-check-failed", f"{witness['id']} failed normalization check: {first}"
        )
    witness["claim"]["coordinate_provenance"] = "numerically-checked"
    witness["certificate"] = {
        "kind": "numerical-feasibility-receipt",
        "replay": (
            "uv run --frozen packing-witness check "
            f"{witness_path} --method numerical-multiprecision "
            f"--precision {CHECK_DIGITS} --tolerance {tolerance}"
        ),
        "result": result,
    }
    return witness


def kingbird_derived_witness(
    n: int,
    retained_witness: Mapping[str, Any],
    *,
    source_n: int,
    source_path: str,
    source_url: str,
) -> dict[str, Any]:
    """Recheck retained Kingbird numerical facts without requiring the source SVG."""
    expected_id = f"W-known-best-n{n:03d}"
    if retained_witness.get("id") != expected_id or retained_witness.get("n") != n:
        raise ValueError("retained Kingbird witness identity does not match requested n")
    if not 1 <= n <= source_n:
        raise ValueError("Kingbird source count does not cover requested n")
    if retained_witness.get("representation") != "center-angle":
        raise ValueError("retained Kingbird facts must use center-angle representation")
    scalar = retained_witness.get("scalar")
    if not isinstance(scalar, Mapping) or scalar.get("kind") != "decimal":
        raise ValueError("retained Kingbird facts must use decimal scalars")
    squares = retained_witness.get("squares")
    if not isinstance(squares, list) or len(squares) != n:
        raise ValueError("retained Kingbird facts do not contain the requested square count")

    witness_path = f"witnesses/known-best/n-{n:03d}.yaml"
    derivation = (
        "direct retained numerical center/angle facts"
        if n == source_n
        else (
            f"retained numerical center/angle subpacking for n={n} from the "
            f"catalogue's n={source_n} construction"
        )
    )
    witness = deepcopy(dict(retained_witness))
    witness["claim"] = {
        "coordinate_provenance": "reported",
        "method": "numerical-multiprecision",
        "precision": {"decimal_digits": CHECK_DIGITS, "rounding": "nearest"},
        "tolerance": KINGBIRD_TOLERANCE,
        "limitations": (
            f"{derivation}. The source metadata supplies attribution and provenance; "
            "the upstream SVG is not retained because no express redistribution terms "
            "were located. This conservative retention policy is not a legal conclusion. "
            "The replayed finite-precision numerical check establishes only "
            "tolerance-bounded feasibility of these retained facts, not exact geometry, "
            "an exact certificate, or optimality."
        ),
    }
    witness["source"] = {
        "key": "Kingbird derived numerical facts",
        "path": source_path,
        "url": source_url,
        "retrieved": RETRIEVED_DATE,
    }
    witness.pop("certificate", None)
    return _checked_witness(witness, tolerance=KINGBIRD_TOLERANCE, witness_path=witness_path)


def unitsquare_witness(
    n: int,
    geometry: UnitSquareGeometry,
    *,
    source_path: str,
    source_url: str,
    witness_id: str | None = None,
    witness_path: str | None = None,
    limitations: str | None = None,
) -> dict[str, Any]:
    """Build and check one rendering-derived UnitSquare public witness."""
    witness_id = witness_id or f"W-known-best-n{n:03d}"
    witness_path = witness_path or f"witnesses/known-best/n-{n:03d}.yaml"
    limitations = limitations or (
        "Coordinates were recovered from the public six-decimal SVG rendering, "
        "not the unavailable governed interval boxes named by its metadata. This "
        "checks the displayed construction only and does not replay the source's "
        "interval claim or prove optimality."
    )
    witness = {
        "id": witness_id,
        "n": n,
        "side": geometry.side,
        "square_size": "1",
        "representation": "corners",
        "scalar": {"kind": "decimal"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": [
            {
                "id": index,
                "corners": [[x, y] for x, y in corners],
            }
            for index, corners in enumerate(geometry.squares, start=1)
        ],
        "claim": {
            "coordinate_provenance": "reported",
            "method": "numerical-multiprecision",
            "precision": {"decimal_digits": CHECK_DIGITS, "rounding": "nearest"},
            "tolerance": UNITSQUARE_TOLERANCE,
            "limitations": limitations,
        },
        "source": {
            "key": "UnitSquare public SOTA rendering",
            "path": source_path,
            "url": source_url,
            "retrieved": RETRIEVED_DATE,
            "revision": (
                "upstream-declared parent-content SHA-256 "
                f"{geometry.upstream_declared_parent_content_sha256}"
            ),
        },
    }
    return _checked_witness(witness, tolerance=UNITSQUARE_TOLERANCE, witness_path=witness_path)


def catalogue_source_map(
    path: Path, *, first_n: int = 1, last_n: int = 100
) -> dict[int, tuple[str, int, tuple[int, ...]]]:
    """Map a closed range of listed counts to their active Kingbird SVGs."""
    if first_n < 1 or last_n < first_n:
        raise ValueError("catalogue range must be nonempty and positive")
    text = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
    pattern = re.compile(
        r'<div class="box"><font size="\+3">\s*([0-9 ,]+)<br>'
        r'<a href="(square-[^"]+\.svg)"',
        re.IGNORECASE,
    )
    result: dict[int, tuple[str, int, tuple[int, ...]]] = {}
    for label, filename in pattern.findall(text):
        values = tuple(int(value) for value in re.findall(r"\d+", label))
        selected = tuple(n for n in values if first_n <= n <= last_n)
        if not selected:
            continue
        source_n = max(values)
        for n in selected:
            result[n] = filename, source_n, values
    return result


def rational_integer(value: str) -> int | None:
    """Return an exact integer decimal, otherwise ``None``."""
    rational = Fraction(value)
    return rational.numerator if rational.denominator == 1 else None
