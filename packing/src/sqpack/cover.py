"""Exact machinery shared by unavoidable-set certificates and their falsifiers.

An unavoidable-set proof certifies that every box (an open square of side strictly
greater than one) whose center lies in a container must contain a marked resource.
`cases/stromquist` carried the first two such certificates -- the printed Figure 14
refusal (exp-016) and the repaired cover (exp-017) -- as one-figure modules; this
module is the general core extracted from them under `BC-093`, so that any published
proof of this shape can be encoded against it.  The case modules keep their point
data, lemma-specific analysis, and record assembly, and call in here for everything
geometric.

**Scalar contract.**  Every decisive value is an exact scalar decided by sign, never
by tolerance: the functions here are duck-typed over any value supporting field
arithmetic (with `int` and `Fraction` mixing), unary negation, `.sign()`, and
`.is_zero()`.  The tiling and mesh validators additionally use `<=` ordering and
`.text()` serialization.  `cases.stromquist.repaired_cover.Q5` and
`sqpack.field.FieldElement` both satisfy the arithmetic-and-sign half; FieldElement
lacks ordering and `.text()` today, which is the recorded seam (X-010 Lane A).

**Resource kinds.**  Only capacity-one point resources are supported; the other kinds
a resource-system certifier will need (weighted points, segments with length
thresholds, threshold charges, moving families) are typed refusals here rather than
untested code, per BC-093's exit.

**Replay stability.**  The retained exp-016/exp-017 records are compared
byte-for-byte on replay, so these functions must keep producing values equal to the
originals; every function body is a behavior-identical move from the case modules
with module globals turned into parameters and additive zeros derived from inputs.
"""

from __future__ import annotations

import tempfile
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from sqpack.field import NumberField

#: Duck-typed exact scalar (see the module docstring's scalar contract).  `Any` follows
#: `sqpack.exact_lp`'s precedent: the caller's scalar carries the arithmetic, and every
#: decision routes through `sign()`/`is_zero()` rather than a tolerance.
type Scalar = Any
type Point = tuple[Scalar, Scalar]
type Face = tuple[str, ...]
type Edge = tuple[str, str]

RationalEndpoint = int | Fraction

SUPPORTED_RESOURCE_KINDS = frozenset({"point"})

#: Resource kinds a full resource-system certifier will need and this module refuses
#: by type rather than carrying untested: the Bentz direction (BC-099 onward).
KNOWN_UNSUPPORTED_RESOURCE_KINDS = frozenset(
    {"weighted-point", "segment", "threshold-charge", "moving-family"}
)


class ResourceKindNotSupportedError(ValueError):
    """A declared resource kind the certifier core does not yet decide."""

    def __init__(self, kind: str):
        super().__init__(
            f"resource kind {kind!r} is not yet supported; supported kinds: "
            f"{sorted(SUPPORTED_RESOURCE_KINDS)}"
        )
        self.kind = kind


def declare_resources(kinds: tuple[str, ...]) -> tuple[str, ...]:
    """Validate a declared resource-kind tuple, refusing unsupported kinds by type."""
    for kind in kinds:
        if kind in SUPPORTED_RESOURCE_KINDS:
            continue
        if kind in KNOWN_UNSUPPORTED_RESOURCE_KINDS:
            raise ResourceKindNotSupportedError(kind)
        raise ValueError(f"unknown resource kind {kind!r}")
    return kinds


def fraction_text(value: Fraction) -> str:
    """Serialize a rational without losing its denominator."""
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def exact_abs(value: Scalar) -> Scalar:
    return value if value.sign() >= 0 else -value


def exact_max(left: Scalar, right: Scalar) -> tuple[Scalar, str]:
    if (left - right).sign() >= 0:
        return left, "u"
    return right, "v"


def exact_min(labelled: list[tuple[str, Scalar]]) -> tuple[str, Scalar]:
    if not labelled:
        raise ValueError("cannot take the minimum of an empty exact list")
    label, value = labelled[0]
    for candidate_label, candidate in labelled[1:]:
        if (candidate - value).sign() < 0:
            label, value = candidate_label, candidate
    return label, value


def object_dict(value: object, label: str) -> dict[str, object]:
    """Narrow a nested evidence object without making the record dynamically typed."""
    if not isinstance(value, dict):
        raise TypeError(f"{label} evidence is not a mapping")
    return cast(dict[str, object], value)


def diagnostic_decimal(value: float) -> str:
    """Round non-decisive libm diagnostics before retaining them."""
    return format(value, ".12g")


def checked_number_field(
    min_poly: tuple[int, ...],
    isolating: tuple[RationalEndpoint, RationalEndpoint],
) -> tuple[NumberField, dict[str, bool]]:
    """Construct a field only after replaying its exact metadata contract."""
    # Lazy on purpose: sympy is heavy and only this constructor needs it, while the
    # geometry core above is imported by every certificate replay.
    import sympy as sp  # noqa: PLC0415

    from sqpack.field import NumberField  # noqa: PLC0415

    variable = sp.Symbol("x")
    polynomial = sp.Poly.from_list(list(min_poly), gens=variable, domain=sp.QQ)
    lower = sp.Rational(isolating[0].numerator, isolating[0].denominator)
    upper = sp.Rational(isolating[1].numerator, isolating[1].denominator)
    checks = {
        "minimal_polynomial_irreducible_over_Q": bool(polynomial.is_irreducible),
        "minimal_polynomial_squarefree": bool(polynomial.gcd(polynomial.diff()).degree() == 0),
        "isolating_interval_contains_exactly_one_root": bool(
            polynomial.count_roots(lower, upper) == 1
        ),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise ValueError(f"algebraic field metadata failed: {failed}")
    return NumberField(min_poly, isolating), checks


def add_points(left: Point, right: Point) -> Point:
    return left[0] + right[0], left[1] + right[1]


def scale_point(value: Point, scalar: Scalar) -> Point:
    return value[0] * scalar, value[1] * scalar


def subtract_points(left: Point, right: Point) -> Point:
    return left[0] - right[0], left[1] - right[1]


def cross(left: Point, right: Point) -> Scalar:
    return left[0] * right[1] - left[1] * right[0]


def orient(first: Point, second: Point, third: Point) -> Scalar:
    return cross(subtract_points(second, first), subtract_points(third, first))


def squared_distance(first: Point, second: Point) -> Scalar:
    delta = subtract_points(first, second)
    return delta[0] ** 2 + delta[1] ** 2


def polygon_area2(vertices: tuple[Point, ...]) -> Scalar:
    zero = vertices[0][0] - vertices[0][0]
    return sum(
        (
            cross(vertices[index], vertices[(index + 1) % len(vertices)])
            for index in range(len(vertices))
        ),
        zero,
    )


def normalized_edge(first: str, second: str) -> Edge:
    return cast(Edge, tuple(sorted((first, second))))


def edges_for_face(face: Face) -> tuple[Edge, ...]:
    return tuple(
        normalized_edge(face[index], face[(index + 1) % len(face)])
        for index in range(len(face))
    )


def between(value: Scalar, first: Scalar, second: Scalar) -> bool:
    low, high = (first, second) if first <= second else (second, first)
    return bool(low <= value <= high)


def segments_cross_strict(first: tuple[Point, Point], second: tuple[Point, Point]) -> bool:
    a, b = first
    c, d = second
    ab_c = orient(a, b, c).sign()
    ab_d = orient(a, b, d).sign()
    cd_a = orient(c, d, a).sign()
    cd_b = orient(c, d, b).sign()
    if ab_c * ab_d < 0 and cd_a * cd_b < 0:
        return True
    if ab_c == 0 and between(c[0], a[0], b[0]) and between(c[1], a[1], b[1]):
        return True
    if ab_d == 0 and between(d[0], a[0], b[0]) and between(d[1], a[1], b[1]):
        return True
    if cd_a == 0 and between(a[0], c[0], d[0]) and between(a[1], c[1], d[1]):
        return True
    return cd_b == 0 and between(b[0], c[0], d[0]) and between(b[1], c[1], d[1])


def validate_noncrossing(points: dict[str, Point], edges: tuple[Edge, ...]) -> None:
    if len(edges) != len(set(edges)):
        raise ValueError("edge inventory contains a duplicate")
    for index, first in enumerate(edges):
        for second in edges[index + 1 :]:
            if set(first) & set(second):
                continue
            if segments_cross_strict(
                (points[first[0]], points[first[1]]),
                (points[second[0]], points[second[1]]),
            ):
                raise ValueError(f"nonadjacent edges cross: {first}, {second}")


def connected_vertices(edges: tuple[Edge, ...]) -> set[str]:
    adjacency: dict[str, set[str]] = {}
    for first, second in edges:
        adjacency.setdefault(first, set()).add(second)
        adjacency.setdefault(second, set()).add(first)
    if not adjacency:
        return set()
    root = min(adjacency)
    reached = {root}
    queue = deque([root])
    while queue:
        vertex = queue.popleft()
        for neighbour in adjacency[vertex]:
            if neighbour not in reached:
                reached.add(neighbour)
                queue.append(neighbour)
    return reached


def point_in_closed_convex_polygon(value: Point, polygon: tuple[Point, ...]) -> bool:
    signs = {
        orient(polygon[index], polygon[(index + 1) % len(polygon)], value).sign()
        for index in range(len(polygon))
    }
    signs.discard(0)
    return len(signs) <= 1


def triangle_edge_certificate(points: dict[str, Point], face: Face) -> dict[str, object]:
    if len(face) != 3 or len(set(face)) != 3:
        raise ValueError(f"not a three-vertex triangle: {face}")
    distances = {
        "-".join(edge): squared_distance(points[edge[0]], points[edge[1]])
        for edge in edges_for_face(face)
    }
    if any(value > 1 for value in distances.values()):
        raise ValueError(f"triangle has an edge longer than one: {face}")
    return {
        "vertices": list(face),
        "squared_edge_lengths": {
            name: value.text() for name, value in sorted(distances.items())
        },
    }


def validate_triangle_mesh(
    points: dict[str, Point],
    faces: tuple[Face, ...],
    boundary: Face,
    *,
    expected_faces: int,
    declared_edges: tuple[Edge, ...] | None = None,
) -> dict[str, object]:
    if len(faces) != expected_faces:
        raise ValueError(f"expected {expected_faces} faces, got {len(faces)}")
    face_keys = [tuple(sorted(face)) for face in faces]
    if len(face_keys) != len(set(face_keys)):
        raise ValueError("triangle inventory contains a duplicate face")
    if any(len(face) != 3 or len(set(face)) != 3 for face in faces):
        raise ValueError("mesh contains a degenerate or nontriangular face")
    if any(vertex not in points for face in faces for vertex in face):
        raise ValueError("mesh references an unknown vertex")

    signed_areas = [polygon_area2(tuple(points[name] for name in face)) for face in faces]
    signs = {area.sign() for area in signed_areas}
    boundary_area = polygon_area2(tuple(points[name] for name in boundary))
    if signs != {boundary_area.sign()} or 0 in signs:
        raise ValueError("mesh faces do not share the boundary's nonzero orientation")

    incidence = Counter(edge for face in faces for edge in edges_for_face(face))
    boundary_edges = set(edges_for_face(boundary))
    if {edge for edge, count in incidence.items() if count == 1} != boundary_edges:
        raise ValueError("single-incidence edges are not exactly the declared boundary")
    if any(count not in (1, 2) for count in incidence.values()):
        raise ValueError("a mesh edge has invalid face incidence")
    derived_edges = tuple(sorted(incidence))
    if declared_edges is not None:
        if len(declared_edges) != len(set(declared_edges)):
            raise ValueError("declared mesh edge inventory contains a duplicate")
        if tuple(sorted(declared_edges)) != derived_edges:
            raise ValueError("declared mesh edges omit or invent an edge")
    validate_noncrossing(points, derived_edges)

    vertices = {vertex for face in faces for vertex in face}
    if connected_vertices(derived_edges) != vertices:
        raise ValueError("mesh edge graph is disconnected")
    if len(vertices) - len(derived_edges) + len(faces) != 1:
        raise ValueError("mesh violates the disk Euler characteristic")
    zero = boundary_area - boundary_area
    if sum(signed_areas, zero) != boundary_area:
        raise ValueError("mesh face areas do not exactly tile the boundary polygon")
    triangle_certificates = [triangle_edge_certificate(points, face) for face in faces]
    absolute_areas = [area if area.sign() > 0 else -area for area in signed_areas]
    minimum_area2 = min(absolute_areas)
    return {
        "face_count": len(faces),
        "edge_count": len(derived_edges),
        "vertex_count": len(vertices),
        "boundary_edge_count": len(boundary_edges),
        "euler_characteristic": 1,
        "signed_area_twice": boundary_area.text(),
        "minimum_abs_face_area_twice": minimum_area2.text(),
        "faces": triangle_certificates,
        "edges": [list(edge) for edge in derived_edges],
        "boundary": list(boundary),
        "all_edges_at_most_one": True,
        "noncrossing": True,
    }


def edge_on_container(points: dict[str, Point], edge: Edge, side: Scalar) -> bool:
    first, second = points[edge[0]], points[edge[1]]
    return bool(
        (first[0].is_zero() and second[0].is_zero())
        or (first[0] == side and second[0] == side)
        or (first[1].is_zero() and second[1].is_zero())
        or (first[1] == side and second[1] == side)
    )


def validate_vertices_in_container(
    points: dict[str, Point], vertices: set[str], side: Scalar
) -> dict[str, object]:
    unknown = vertices - points.keys()
    if unknown:
        raise ValueError(f"tiling references unknown vertices: {sorted(unknown)}")
    ordered = sorted(vertices)
    outside = [
        name
        for name in ordered
        if not (0 <= points[name][0] <= side and 0 <= points[name][1] <= side)
    ]
    if outside:
        raise ValueError(f"tiling vertices lie outside [0,SIDE]^2: {outside}")
    return {
        "container_x_interval": ["0", side.text()],
        "container_y_interval": ["0", side.text()],
        "vertex_count": len(ordered),
        "vertices": {
            name: [coordinate.text() for coordinate in points[name]] for name in ordered
        },
        "all_vertices_in_closed_container": True,
    }


def validate_square_tiling(
    points: dict[str, Point],
    faces: tuple[Face, ...],
    *,
    side: Scalar,
    expected_faces: int,
) -> dict[str, object]:
    if len(faces) != expected_faces:
        raise ValueError(f"expected {expected_faces} tiling faces, got {len(faces)}")
    keys = [tuple(sorted(face)) for face in faces]
    if len(keys) != len(set(keys)):
        raise ValueError("tiling contains a duplicate face")
    vertices = {vertex for face in faces for vertex in face}
    containment = validate_vertices_in_container(points, vertices, side)
    signed_areas = [polygon_area2(tuple(points[name] for name in face)) for face in faces]
    signs = {area.sign() for area in signed_areas}
    if len(signs) != 1 or 0 in signs:
        raise ValueError("tiling faces do not have one nonzero orientation")
    orientation_sign = signs.pop()
    zero = side - side
    absolute_area2 = sum((area * orientation_sign for area in signed_areas), zero)
    if absolute_area2 != 2 * side**2:
        raise ValueError("tiling face areas do not sum to the exact container area")

    incidence = Counter(edge for face in faces for edge in edges_for_face(face))
    if any(count not in (1, 2) for count in incidence.values()):
        raise ValueError("tiling edge incidence is not one or two")
    boundary_edges = {edge for edge, count in incidence.items() if count == 1}
    if not boundary_edges or any(
        not edge_on_container(points, edge, side) for edge in boundary_edges
    ):
        raise ValueError("tiling has a non-container single-incidence edge")
    edges = tuple(sorted(incidence))
    validate_noncrossing(points, edges)
    if connected_vertices(edges) != vertices:
        raise ValueError("tiling edge graph is disconnected")
    if len(vertices) - len(edges) + len(faces) != 1:
        raise ValueError("tiling violates the disk Euler characteristic")
    return {
        "face_count": len(faces),
        "edge_count": len(edges),
        "vertex_count": len(vertices),
        "boundary_edge_count": len(boundary_edges),
        "euler_characteristic": 1,
        "signed_area_twice": (2 * side**2 * orientation_sign).text(),
        "noncrossing": True,
        "all_internal_edges_have_two_incident_faces": True,
        "all_boundary_edges_lie_on_container": True,
        "vertex_containment": containment,
    }


def validate_polygon_partition(
    points: dict[str, Point],
    faces: tuple[Face, ...],
    boundary: Face,
    *,
    expected_faces: int,
) -> dict[str, object]:
    if len(faces) != expected_faces:
        raise ValueError(f"expected {expected_faces} partition faces, got {len(faces)}")
    keys = [tuple(sorted(face)) for face in faces]
    if len(keys) != len(set(keys)):
        raise ValueError("polygon partition has duplicate faces")
    areas = [polygon_area2(tuple(points[name] for name in face)) for face in faces]
    boundary_area = polygon_area2(tuple(points[name] for name in boundary))
    if {area.sign() for area in areas} != {boundary_area.sign()} or boundary_area.is_zero():
        raise ValueError("polygon partition orientations disagree")
    zero = boundary_area - boundary_area
    if sum(areas, zero) != boundary_area:
        raise ValueError("polygon partition areas do not sum to its boundary")
    incidence = Counter(edge for face in faces for edge in edges_for_face(face))
    if {edge for edge, count in incidence.items() if count == 1} != set(
        edges_for_face(boundary)
    ):
        raise ValueError("polygon partition boundary incidence is incomplete")
    if any(count not in (1, 2) for count in incidence.values()):
        raise ValueError("polygon partition has invalid edge incidence")
    edges = tuple(sorted(incidence))
    validate_noncrossing(points, edges)
    return {
        "face_count": len(faces),
        "edge_count": len(edges),
        "signed_area_twice": boundary_area.text(),
        "noncrossing": True,
    }


def box_corners(center: Point, half: Scalar, cosine: Scalar, sine: Scalar) -> list[Point]:
    """Ordered corners of the box using edge vectors L(cos,sin) and L(-sin,cos)."""
    center_x, center_y = center
    corners: list[Point] = []
    for sign_u, sign_v in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        corners.append(
            (
                center_x + sign_u * half * cosine - sign_v * half * sine,
                center_y + sign_u * half * sine + sign_v * half * cosine,
            )
        )
    return corners


def validate_box_shape(corners: list[Point], length: Scalar) -> None:
    """Refuse corners that are not an exact square of the declared side."""
    edge_squared = []
    corner_dots = []
    for index in range(4):
        x1, y1 = corners[index]
        x2, y2 = corners[(index + 1) % 4]
        x0, y0 = corners[(index - 1) % 4]
        edge_squared.append((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
        corner_dots.append((x0 - x1) * (x2 - x1) + (y0 - y1) * (y2 - y1))
    if not all((value - length * length).is_zero() for value in edge_squared):
        raise ValueError("witness corners do not have the declared exact side length")
    if not all(value.is_zero() for value in corner_dots):
        raise ValueError("witness corners are not exact right angles")


def corner_clearances(corners: list[Point], side: Scalar) -> list[tuple[str, Scalar]]:
    """Labelled wall clearances for each corner, in the retained label scheme."""
    clearances: list[tuple[str, Scalar]] = []
    for index, (x, y) in enumerate(corners):
        clearances.extend(
            (
                (f"corner_{index}_left", x),
                (f"corner_{index}_bottom", y),
                (f"corner_{index}_right", side - x),
                (f"corner_{index}_top", side - y),
            )
        )
    return clearances


def avoidance_margin(
    point: Point, center: Point, half: Scalar, cosine: Scalar, sine: Scalar
) -> tuple[Scalar, str]:
    """L-infinity margin from a point to the closed box boundary, in the box frame.

    A strictly positive margin means the point lies strictly outside the closed box,
    hence strictly avoids the open box; the returned axis is the active local axis.
    """
    dx, dy = point[0] - center[0], point[1] - center[1]
    local_u = cosine * dx + sine * dy
    local_v = -sine * dx + cosine * dy
    margin_u = exact_abs(local_u) - half
    margin_v = exact_abs(local_v) - half
    return exact_max(margin_u, margin_v)


def write_text_atomic(path: Path, text: str) -> None:
    """Write via a temporary file and rename, so a crash never leaves a torn record."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            delete=False,
        ) as temporary:
            temporary.write(text)
            temporary.flush()
            temporary_name = temporary.name
        Path(temporary_name).replace(path)
    finally:
        if temporary_name is not None:
            temporary_path = Path(temporary_name)
            if temporary_path.exists():
                temporary_path.unlink()
