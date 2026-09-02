"""Target-blind production adapters for one digest-bound UnitSquare parent."""

from __future__ import annotations

import hashlib
import json
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from typing import BinaryIO, Literal, Protocol, cast, override

from cases.unitsquare_precision.refusal.run import (
    DIHEDRAL_CORRESPONDENCES,
    Axis,
    CoverLeaf,
    CoverSplit,
    ExactPose,
    ExactWitness,
    PoseBox,
    ProofFormatError,
    RationalAffine,
    RationalInterval,
    RunnerModelEvaluation,
    SourceBinding,
    build_exact_witness,
    build_proof_receipt,
    outward_wall_signs,
    rejected_leaf,
    retained_leaf,
    source_cells_sha256,
)

type SourceModel = Literal["declared:svg-literal", "nearest-6", "truncate-6"]
type SourceCells = tuple[
    tuple[RationalInterval, RationalInterval],
    tuple[RationalInterval, RationalInterval],
    tuple[RationalInterval, RationalInterval],
    tuple[RationalInterval, RationalInterval],
]

MAX_PARENT_BYTES = 4_000_000
MAX_XML_ELEMENTS = 20_000
MAX_XML_DEPTH = 64
MAX_COVER_NODES = 16_383
MAX_COVER_DEPTH = 48
MAX_NUMBER_TOKEN_BYTES = 128
MAX_STABLE_ID_BYTES = 512
PARENT_TIMEOUT_SECONDS = 30
REPORTED_SIDE_TOKEN = "8.80345993651653"

_NUMBER_PATTERN = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"
_NUMBER = re.compile(_NUMBER_PATTERN)
_TRANSFORM = re.compile(r"([A-Za-z]+)\s*\(([^()]*)\)")
_NUMBER_GAP = re.compile(r"(?:\s+|\s*,\s*)\Z")
_SIX_PLACES = re.compile(r"[+-]?(?:\d+\.\d{6}|\.\d{6})\Z")


class ProductionAdapterError(ValueError):
    """A typed, bounded refusal in the production adapter."""


class StructuralRefusalError(ProductionAdapterError):
    """The source cannot be scanned without ambiguity."""


class TransformRefusalError(ProductionAdapterError):
    """The source transform is not supported by exact arithmetic."""


class SerializationRefusalError(ProductionAdapterError):
    """A declared decimal model does not apply to the selected source."""


class PoseRefusalError(ProductionAdapterError):
    """No exact compatible pose was found by the bounded proposer."""


@dataclass(frozen=True, slots=True)
class Container:
    """One unambiguous exact SVG container."""

    x0: Fraction
    y0: Fraction
    width: Fraction
    height: Fraction

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise StructuralRefusalError("container dimensions must be positive")


@dataclass(frozen=True, slots=True)
class PolygonFacts:
    """Sanitized exact facts for one polygon; source text is not retained."""

    stable_id: str
    coordinate_tokens: tuple[str, ...]
    transform: RationalAffine
    transform_tokens: tuple[str, ...]
    polygon_sha256: str


@dataclass(frozen=True, slots=True)
class SceneFacts:
    """One exact container and its deterministically ordered polygons."""

    container: Container
    polygons: tuple[PolygonFacts, ...]


class _RejectRedirect(urllib.request.HTTPRedirectHandler):
    @override
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class BoundedResponse:
    """Expose one bounded read while preserving deterministic cleanup."""

    def __init__(self, response: BinaryIO, *, byte_cap: int = MAX_PARENT_BYTES) -> None:
        if byte_cap <= 0:
            raise ProductionAdapterError("parent byte cap must be positive")
        self._response = response
        self._byte_cap = byte_cap
        self._read = False

    @property
    def closed(self) -> bool:
        return bool(getattr(self._response, "closed", False))

    def read(self) -> bytes:
        if self._read:
            raise ProductionAdapterError("parent response permits one bounded read")
        self._read = True
        payload = self._response.read(self._byte_cap + 1)
        if not isinstance(payload, bytes):
            raise ProductionAdapterError("parent response did not return bytes")
        if len(payload) > self._byte_cap:
            raise ProductionAdapterError("parent response exceeds the byte cap")
        return payload

    def close(self) -> None:
        self._response.close()


class ParentTransport(Protocol):
    """The only transport method visible to the bounded opener."""

    def open(self, url: str, *, timeout: int) -> BinaryIO: ...


def bounded_parent_opener(
    expected_url: str,
    *,
    byte_cap: int = MAX_PARENT_BYTES,
    timeout_seconds: int = PARENT_TIMEOUT_SECONDS,
    transport: ParentTransport | None = None,
) -> Callable[[str], BinaryIO]:
    """Return an exact-URL, no-redirect, timeout-bound opener.

    Merely constructing this callable performs no I/O.  BC-124 exercises it only with
    injected responses; a later W6 phase must supply the authority to call it.
    """

    if not expected_url.startswith("https://"):
        raise ProductionAdapterError("parent URL must use HTTPS")
    if timeout_seconds <= 0:
        raise ProductionAdapterError("parent timeout must be positive")
    network = transport or cast(
        ParentTransport,
        urllib.request.build_opener(_RejectRedirect()),
    )

    def open_exact(url: str) -> BinaryIO:
        if url != expected_url:
            raise ProductionAdapterError("parent URL does not match the frozen source")
        try:
            response = cast(BinaryIO, network.open(url, timeout=timeout_seconds))
        except (OSError, urllib.error.URLError) as error:
            raise ProductionAdapterError("bounded parent retrieval failed") from error
        final_url = getattr(response, "geturl", lambda: url)()
        if final_url != expected_url:
            response.close()
            raise ProductionAdapterError("parent redirect is forbidden")
        return cast(BinaryIO, BoundedResponse(response, byte_cap=byte_cap))

    return open_exact


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _numbers(text: str, *, label: str) -> tuple[str, ...]:
    """Parse every numeric token and reject any unconsumed source character."""

    tokens: list[str] = []
    cursor = 0
    for match in _NUMBER.finditer(text):
        gap = text[cursor : match.start()]
        token = match.group(0)
        if cursor == 0:
            valid_gap = not gap.strip()
        elif not gap:
            valid_gap = token.startswith(("+", "-"))
        else:
            valid_gap = _NUMBER_GAP.fullmatch(gap) is not None
        if not valid_gap:
            raise StructuralRefusalError(f"{label} contains unsupported syntax")
        tokens.append(token)
        cursor = match.end()
    if not tokens or text[cursor:].strip():
        raise StructuralRefusalError(f"{label} contains unsupported syntax")
    return tuple(tokens)


def _fraction(token: str, *, label: str) -> Fraction:
    if len(token.encode("ascii", errors="ignore")) > MAX_NUMBER_TOKEN_BYTES:
        raise StructuralRefusalError(f"{label} exceeds the numeric token bound")
    try:
        return Fraction(token)
    except (ValueError, ZeroDivisionError) as error:
        raise StructuralRefusalError(f"{label} is not an exact finite decimal") from error


def _container(root: ET.Element) -> Container:
    candidates: list[Container] = []
    view_box = root.attrib.get("viewBox")
    if view_box is not None:
        values = _numbers(view_box, label="viewBox")
        if len(values) != 4:
            raise StructuralRefusalError("viewBox must have four exact coordinates")
        candidates.append(Container(*(_fraction(value, label="viewBox") for value in values)))
    rectangles = [
        element
        for element in root.iter()
        if _local_name(element.tag) == "rect" and element.attrib.get("id") == "container"
    ]
    if len(rectangles) > 1:
        raise StructuralRefusalError("container rectangle is ambiguous")
    if rectangles:
        rectangle = rectangles[0]
        if rectangle.attrib.get("transform", "").strip():
            raise StructuralRefusalError("container rectangle transform is unsupported")
        try:
            candidates.append(
                Container(
                    _fraction(rectangle.attrib.get("x", "0"), label="container x"),
                    _fraction(rectangle.attrib.get("y", "0"), label="container y"),
                    _fraction(rectangle.attrib["width"], label="container width"),
                    _fraction(rectangle.attrib["height"], label="container height"),
                )
            )
        except KeyError as error:
            raise StructuralRefusalError("container rectangle lacks dimensions") from error
    if not candidates:
        raise StructuralRefusalError("SVG has no exact container")
    if any(candidate != candidates[0] for candidate in candidates[1:]):
        raise StructuralRefusalError("SVG container declarations disagree")
    return candidates[0]


def _quarter_turn(angle: Fraction) -> RationalAffine:
    quotient = angle / 90
    if quotient.denominator != 1:
        raise TransformRefusalError("decimal-angle rotation lacks an outward exact certificate")
    turn = quotient.numerator % 4
    coefficients = (
        (1, 0, 0, 1),
        (0, 1, -1, 0),
        (-1, 0, 0, -1),
        (0, -1, 1, 0),
    )[turn]
    a, b, c, d = (Fraction(value) for value in coefficients)
    return RationalAffine(a, b, c, d, Fraction(0), Fraction(0))


def parse_transform(text: str) -> RationalAffine:
    """Parse exact matrix/translate/scale and exact quadrant rotations."""

    if not text.strip():
        return RationalAffine.identity()
    result = RationalAffine.identity()
    cursor = 0
    for match in _TRANSFORM.finditer(text):
        gap = text[cursor : match.start()]
        valid_gap = (
            not gap.strip()
            if cursor == 0
            else not gap or _NUMBER_GAP.fullmatch(gap) is not None
        )
        if not valid_gap:
            raise TransformRefusalError("malformed SVG transform list")
        name = match.group(1)
        try:
            values = tuple(
                _fraction(token, label="transform coefficient")
                for token in _numbers(match.group(2), label=f"{name} transform")
            )
        except StructuralRefusalError as error:
            raise TransformRefusalError(str(error)) from error
        if name == "matrix" and len(values) == 6:
            operation = RationalAffine(*values)
        elif name == "translate" and len(values) in (1, 2):
            operation = RationalAffine(
                Fraction(1),
                Fraction(0),
                Fraction(0),
                Fraction(1),
                values[0],
                values[1] if len(values) == 2 else Fraction(0),
            )
        elif name == "scale" and len(values) in (1, 2):
            operation = RationalAffine(
                values[0],
                Fraction(0),
                Fraction(0),
                values[1] if len(values) == 2 else values[0],
                Fraction(0),
                Fraction(0),
            )
        elif name == "rotate" and len(values) in (1, 3):
            rotation = _quarter_turn(values[0])
            if len(values) == 3:
                forward = RationalAffine.translation(str(values[1]), str(values[2]))
                backward = RationalAffine.translation(str(-values[1]), str(-values[2]))
                operation = forward.compose(rotation).compose(backward)
            else:
                operation = rotation
        else:
            raise TransformRefusalError(f"unsupported SVG transform: {name}")
        determinant = operation.a * operation.d - operation.b * operation.c
        if determinant == 0:
            raise TransformRefusalError("singular SVG transform")
        result = result.compose(operation)
        cursor = match.end()
    if cursor == 0 or text[cursor:].strip():
        raise TransformRefusalError("malformed SVG transform list")
    if result.a * result.d - result.b * result.c == 0:
        raise TransformRefusalError("singular composed SVG transform")
    return result


def _secure_root(payload: memoryview) -> ET.Element:
    def contains_ascii_casefolded(token: bytes) -> bool:
        if len(payload) < len(token):
            return False
        for start in range(len(payload) - len(token) + 1):
            if all(
                (payload[start + offset] | 0x20) == expected
                for offset, expected in enumerate(token)
            ):
                return True
        return False

    if contains_ascii_casefolded(b"<!doctype") or contains_ascii_casefolded(b"<!entity"):
        raise StructuralRefusalError("DTD and entity declarations are forbidden")
    try:
        root = ET.fromstring(payload)
    except ET.ParseError as error:
        raise StructuralRefusalError("source is not well-formed XML") from error
    if _local_name(root.tag) != "svg":
        raise StructuralRefusalError("source root is not SVG")
    for element in root.iter():
        local_name = _local_name(element.tag)
        if local_name in {"script", "use", "foreignObject"}:
            raise StructuralRefusalError(f"unsupported SVG geometry indirection: {local_name}")
        if local_name == "svg" and element is not root:
            raise StructuralRefusalError("nested SVG viewports are unsupported")
        if local_name == "style" and (element.text or "").strip():
            raise StructuralRefusalError("embedded stylesheets are unsupported")
        style = element.attrib.get("style", "")
        if re.search(r"(?:^|;)\s*transform(?:-origin)?\s*:", style, re.IGNORECASE):
            raise StructuralRefusalError("CSS transforms are unsupported")
    return root


def _polygon_digest(
    stable_id: str,
    coordinates: tuple[str, ...],
    transform_tokens: tuple[str, ...],
    container: Container,
) -> str:
    document = {
        "stable_id": stable_id,
        "coordinates": list(coordinates),
        "transform_chain": list(transform_tokens),
        "container": [
            str(container.x0),
            str(container.y0),
            str(container.width),
            str(container.height),
        ],
    }
    return hashlib.sha256(
        json.dumps(document, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def parse_scene(
    payload: memoryview,
    *,
    parse_transforms: bool,
    selected_id: str | None = None,
) -> SceneFacts:
    """Parse bounded SVG structure, optionally constructing exact global transforms."""

    root = _secure_root(payload)
    container = _container(root)
    polygons: list[PolygonFacts] = []
    identifiers: set[str] = set()
    element_count = 0
    selected_ancestors: set[int] | None = None
    if parse_transforms and selected_id is not None:
        selected_ancestors = set()
        selected_path_elements = 0

        def mark_selected_path(element: ET.Element, depth: int) -> bool:
            nonlocal selected_path_elements
            selected_path_elements += 1
            if selected_path_elements > MAX_XML_ELEMENTS or depth > MAX_XML_DEPTH:
                raise StructuralRefusalError("SVG structure exceeds the bounded parser limits")
            contains = (
                _local_name(element.tag) == "polygon"
                and element.attrib.get("id") == selected_id
            )
            for child in element:
                contains = mark_selected_path(child, depth + 1) or contains
            if contains:
                selected_ancestors.add(id(element))
            return contains

        mark_selected_path(root, 0)

    def visit(
        element: ET.Element,
        parent: RationalAffine,
        chain: tuple[str, ...],
        depth: int,
    ) -> None:
        nonlocal element_count
        element_count += 1
        if element_count > MAX_XML_ELEMENTS or depth > MAX_XML_DEPTH:
            raise StructuralRefusalError("SVG structure exceeds the bounded parser limits")
        transform_text = element.attrib.get("transform", "")
        should_parse_transform = parse_transforms and (
            selected_ancestors is None or id(element) in selected_ancestors
        )
        local = (
            parse_transform(transform_text)
            if should_parse_transform
            else RationalAffine.identity()
        )
        current = parent.compose(local)
        current_chain = chain + ((transform_text,) if transform_text.strip() else ())
        if _local_name(element.tag) == "polygon":
            stable_id = element.attrib.get("id")
            if not stable_id:
                raise StructuralRefusalError("every square polygon requires a stable id")
            try:
                encoded_id = stable_id.encode("utf-8")
            except UnicodeEncodeError as error:
                raise StructuralRefusalError("polygon id is not valid UTF-8") from error
            if len(encoded_id) > MAX_STABLE_ID_BYTES:
                raise StructuralRefusalError("polygon id exceeds the retained-id bound")
            if stable_id in identifiers:
                raise StructuralRefusalError(f"duplicate square id: {stable_id}")
            identifiers.add(stable_id)
            coordinates = _numbers(element.attrib.get("points", ""), label="polygon points")
            if len(coordinates) != 8:
                raise StructuralRefusalError(
                    f"square {stable_id} must publish exactly four coordinate pairs"
                )
            polygons.append(
                PolygonFacts(
                    stable_id,
                    coordinates,
                    current,
                    current_chain,
                    _polygon_digest(stable_id, coordinates, current_chain, container),
                )
            )
        for child in element:
            visit(child, current, current_chain, depth + 1)

    visit(root, RationalAffine.identity(), (), 0)
    if not polygons:
        raise StructuralRefusalError("SVG contains no square polygons")
    return SceneFacts(
        container,
        tuple(sorted(polygons, key=lambda polygon: polygon.stable_id.encode("utf-8"))),
    )


def structural_scanner(
    *, expected_polygon_count: int
) -> Callable[[memoryview], Sequence[Mapping[str, object]]]:
    """Build the strict source scanner consumed after the runner's digest guard."""

    if expected_polygon_count <= 0:
        raise ProductionAdapterError("expected polygon count must be positive")

    def scan(payload: memoryview) -> Sequence[Mapping[str, object]]:
        scene = parse_scene(payload, parse_transforms=False)
        if len(scene.polygons) != expected_polygon_count:
            raise StructuralRefusalError(
                "expected "
                f"{expected_polygon_count} square polygons, found {len(scene.polygons)}"
            )
        return tuple(
            {
                "stable_id": polygon.stable_id,
                "vertex_count": 4,
                "polygon_sha256": polygon.polygon_sha256,
            }
            for polygon in scene.polygons
        )

    return scan


def _source_interval(token: str, model: SourceModel) -> RationalInterval:
    value = _fraction(token, label="source coordinate")
    if model == "declared:svg-literal":
        return RationalInterval(value, value)
    if _SIX_PLACES.fullmatch(token) is None:
        raise SerializationRefusalError(
            f"{model} requires exactly six fractional decimal places"
        )
    quantum = Fraction(1, 1_000_000)
    if model == "nearest-6":
        return RationalInterval(value - quantum / 2, value + quantum / 2)
    if model == "truncate-6":
        return (
            RationalInterval(value - quantum, value)
            if token.startswith("-")
            else RationalInterval(value, value + quantum)
        )
    raise SerializationRefusalError(f"unknown source model: {model}")


def _exact_side(side: Fraction | None) -> Fraction:
    if side is None:
        raise SerializationRefusalError(
            "reported side token lacks exact or directional semantics"
        )
    return side


def _linear(
    first: Fraction,
    x: RationalInterval,
    second: Fraction,
    y: RationalInterval,
    offset: Fraction,
) -> RationalInterval:
    values = (
        first * x.lower + second * y.lower + offset,
        first * x.lower + second * y.upper + offset,
        first * x.upper + second * y.lower + offset,
        first * x.upper + second * y.upper + offset,
    )
    return RationalInterval(min(values), max(values))


def _normalized_cells(
    polygon: PolygonFacts,
    container: Container,
    model: SourceModel,
    side: Fraction,
) -> SourceCells:
    cells: list[tuple[RationalInterval, RationalInterval]] = []
    for index in range(0, 8, 2):
        local_x = _source_interval(polygon.coordinate_tokens[index], model)
        local_y = _source_interval(polygon.coordinate_tokens[index + 1], model)
        global_x = _linear(
            polygon.transform.a,
            local_x,
            polygon.transform.c,
            local_y,
            polygon.transform.e,
        )
        global_y = _linear(
            polygon.transform.b,
            local_x,
            polygon.transform.d,
            local_y,
            polygon.transform.f,
        )
        normalized_x = RationalInterval(
            side * (global_x.lower - container.x0) / container.width,
            side * (global_x.upper - container.x0) / container.width,
        )
        normalized_y = RationalInterval(
            side * (container.y0 + container.height - global_y.upper) / container.height,
            side * (container.y0 + container.height - global_y.lower) / container.height,
        )
        cells.append((normalized_x, normalized_y))
    return cast(SourceCells, tuple(cells))


def _midpoint(interval: RationalInterval) -> Fraction:
    return (interval.lower + interval.upper) / 2


def _pose_for_t(
    cells: SourceCells,
    correspondence: tuple[int, int, int, int],
    t: Fraction,
) -> ExactPose | None:
    if not Fraction(-1, 2) <= t <= Fraction(1, 2):
        return None
    denominator = 1 + t * t
    cosine = (1 - t * t) / denominator
    sine = 2 * t / denominator
    offsets = (
        (-cosine / 2 + sine / 2, -sine / 2 - cosine / 2),
        (cosine / 2 + sine / 2, sine / 2 - cosine / 2),
        (cosine / 2 - sine / 2, sine / 2 + cosine / 2),
        (-cosine / 2 - sine / 2, -sine / 2 + cosine / 2),
    )
    cx_lower: Fraction | None = None
    cx_upper: Fraction | None = None
    cy_lower: Fraction | None = None
    cy_upper: Fraction | None = None
    for source_index, corner_index in enumerate(correspondence):
        x_cell, y_cell = cells[source_index]
        dx, dy = offsets[corner_index]
        lower_x, upper_x = x_cell.lower - dx, x_cell.upper - dx
        lower_y, upper_y = y_cell.lower - dy, y_cell.upper - dy
        cx_lower = lower_x if cx_lower is None else max(cx_lower, lower_x)
        cx_upper = upper_x if cx_upper is None else min(cx_upper, upper_x)
        cy_lower = lower_y if cy_lower is None else max(cy_lower, lower_y)
        cy_upper = upper_y if cy_upper is None else min(cy_upper, upper_y)
    if (
        cx_lower is None
        or cx_upper is None
        or cy_lower is None
        or cy_upper is None
        or cx_lower > cx_upper
        or cy_lower > cy_upper
    ):
        return None
    return ExactPose((cx_lower + cx_upper) / 2, (cy_lower + cy_upper) / 2, t)


def propose_exact_witness(
    binding: SourceBinding, cells: SourceCells
) -> tuple[ExactWitness, tuple[int, int, int, int]]:
    """Use source midpoints only to propose; exact containment admits the witness."""

    for correspondence in DIHEDRAL_CORRESPONDENCES:
        ordered: list[tuple[Fraction, Fraction] | None] = [None, None, None, None]
        for source_index, corner_index in enumerate(correspondence):
            x_cell, y_cell = cells[source_index]
            ordered[corner_index] = (_midpoint(x_cell), _midpoint(y_cell))
        if any(point is None for point in ordered):
            continue
        points = cast(list[tuple[Fraction, Fraction]], ordered)
        edge_x = points[1][0] - points[0][0]
        edge_y = points[1][1] - points[0][1]
        candidates: list[Fraction] = [Fraction(0), Fraction(1, 2), Fraction(-1, 2)]
        if 1 + edge_x != 0:
            raw = edge_y / (1 + edge_x)
            candidates.extend(raw.limit_denominator(limit) for limit in (10**4, 10**6, 10**8))
        for t in dict.fromkeys(candidates):
            pose = _pose_for_t(cells, correspondence, t)
            if pose is None:
                continue
            try:
                witness = build_exact_witness(binding, pose, cells, correspondence)
            except ProofFormatError:
                continue
            return witness, correspondence
    raise PoseRefusalError("bounded exact proposer found no compatible rational witness")


def _proof_for_polygon(
    *,
    source_sha256: str,
    polygon: PolygonFacts,
    container: Container,
    cells: SourceCells,
    model: SourceModel,
    side: Fraction,
) -> tuple[dict[str, object], dict[str, object], str]:
    binding = SourceBinding(
        model,
        source_sha256,
        polygon.polygon_sha256,
        polygon.transform,
        (container.x0, container.y0, container.width, container.height, side),
    )
    witness, _correspondence = propose_exact_witness(binding, cells)
    cx_lower = max(cell[0].lower - 1 for cell in cells)
    cx_upper = min(cell[0].upper + 1 for cell in cells)
    cy_lower = max(cell[1].lower - 1 for cell in cells)
    cy_upper = min(cell[1].upper + 1 for cell in cells)
    if cx_lower > cx_upper or cy_lower > cy_upper:
        raise PoseRefusalError("source-derived center bounds are empty")
    root = PoseBox(
        RationalInterval(cx_lower, cx_upper),
        RationalInterval(cy_lower, cy_upper),
        RationalInterval(Fraction(-1, 2), Fraction(1, 2)),
    )
    cover = _wall_cover(
        root,
        cells,
        witness.correspondence,
        side,
    )
    proof = build_proof_receipt(witness, cover)
    proof_document = proof.get("proof")
    if not isinstance(proof_document, dict):
        raise PoseRefusalError("proof builder returned an invalid envelope")
    wall_signs = proof_document.get("wall_signs")
    if not isinstance(wall_signs, dict) or wall_signs.get("decision") != "nonnegative":
        raise PoseRefusalError("outer cover does not prove nonnegative wall containment")
    return proof, binding.to_document(), source_cells_sha256(cells)


def _wall_cover(
    root: PoseBox,
    cells: SourceCells,
    correspondence: tuple[int, int, int, int],
    side: Fraction,
) -> CoverLeaf | CoverSplit:
    """Build a complete bounded cover, rejecting or wall-certifying every leaf."""

    visited = 0

    def visit(region: PoseBox, depth: int) -> CoverLeaf | CoverSplit:
        nonlocal visited
        visited += 1
        if visited > MAX_COVER_NODES or depth > MAX_COVER_DEPTH:
            raise PoseRefusalError("wall-cover node budget exhausted")
        try:
            return rejected_leaf(region, cells, correspondence)
        except ProofFormatError:
            pass
        retained = retained_leaf(region)
        if outward_wall_signs(retained, side)["decision"] == "nonnegative":
            return retained
        widths: dict[Axis, Fraction] = {
            "cx": region.cx.upper - region.cx.lower,
            "cy": region.cy.upper - region.cy.lower,
            "t": region.t.upper - region.t.lower,
        }
        axis: Axis = max(
            ("cx", "cy", "t"),
            key=lambda name: widths[name],
        )
        interval = region.interval(axis)
        if interval.lower == interval.upper:
            raise PoseRefusalError("wall-cover point leaf is not nonnegative")
        cut = (interval.lower + interval.upper) / 2
        lower, upper = region.split(axis, cut)
        return CoverSplit(
            region,
            axis,
            cut,
            visit(lower, depth + 1),
            visit(upper, depth + 1),
        )

    return visit(root, 0)


def production_model_factory(
    *,
    expected_polygon_count: int,
    side: Fraction | None,
) -> Callable[[str], Callable[[memoryview, str], RunnerModelEvaluation]]:
    """Create isolated exact parser/evaluator instances for the frozen three models."""

    if side is not None and side <= 0:
        raise ProductionAdapterError("normalized side must be positive")

    def factory(model_name: str) -> Callable[[memoryview, str], RunnerModelEvaluation]:
        if model_name not in ("declared:svg-literal", "nearest-6", "truncate-6"):
            raise ProductionAdapterError("model factory received an unknown model")
        model: SourceModel = cast(SourceModel, model_name)

        class Evaluator:
            def __call__(self, payload: memoryview, stable_id: str) -> RunnerModelEvaluation:
                source_sha256 = hashlib.sha256(payload).hexdigest()
                try:
                    scene = parse_scene(
                        payload,
                        parse_transforms=True,
                        selected_id=stable_id,
                    )
                    if len(scene.polygons) != expected_polygon_count:
                        raise StructuralRefusalError(
                            "model parse changed the polygon inventory"
                        )
                    matches = [
                        polygon for polygon in scene.polygons if polygon.stable_id == stable_id
                    ]
                    if len(matches) != 1:
                        raise StructuralRefusalError("selected polygon is absent or ambiguous")
                    polygon = matches[0]
                    exact_side = _exact_side(side)
                    cells = _normalized_cells(polygon, scene.container, model, exact_side)
                    proof, binding, cells_sha256 = _proof_for_polygon(
                        source_sha256=source_sha256,
                        polygon=polygon,
                        container=scene.container,
                        cells=cells,
                        model=model,
                        side=exact_side,
                    )
                    return RunnerModelEvaluation(
                        model,
                        "compatible",
                        "localized-compatible",
                        proof,
                        binding,
                        cells_sha256,
                    )
                except TransformRefusalError:
                    return RunnerModelEvaluation(model, "refused", "affine-transform-refusal")
                except SerializationRefusalError:
                    return RunnerModelEvaluation(model, "refused", "serialization-refusal")
                except PoseRefusalError:
                    return RunnerModelEvaluation(model, "refused", "unresolved")

        return Evaluator()

    return factory
