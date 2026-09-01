"""Independent exact verifier for UnitSquarePoseProof/v1 receipts."""

from __future__ import annotations

import hashlib
import json
import re
from fractions import Fraction
from typing import Any

_RATIONAL = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")
_DIGEST = re.compile(r"[0-9a-f]{64}\Z")
_MODELS = ("declared:svg-literal", "nearest-6", "truncate-6")
_DIHEDRAL = (
    (0, 1, 2, 3),
    (1, 2, 3, 0),
    (2, 3, 0, 1),
    (3, 0, 1, 2),
    (0, 3, 2, 1),
    (3, 2, 1, 0),
    (2, 1, 0, 3),
    (1, 0, 3, 2),
)


class _InvalidProof(ValueError):  # noqa: N818
    pass


def _mapping(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise _InvalidProof(f"{label} must be an object")
    return value


def _sequence(value: object, label: str, length: int | None = None) -> list[Any]:
    if not isinstance(value, list) or (length is not None and len(value) != length):
        raise _InvalidProof(f"{label} has invalid shape")
    return value


def _fraction(value: object, label: str) -> Fraction:
    if not isinstance(value, str) or _RATIONAL.fullmatch(value) is None:
        raise _InvalidProof(f"{label} is not a strict rational")
    result = Fraction(value)
    canonical = str(result.numerator)
    if result.denominator != 1:
        canonical += f"/{result.denominator}"
    if value != canonical:
        raise _InvalidProof(f"{label} is not canonical")
    return result


def _interval(value: object, label: str) -> tuple[Fraction, Fraction]:
    endpoints = _sequence(value, label, 2)
    lower = _fraction(endpoints[0], label)
    upper = _fraction(endpoints[1], label)
    if lower > upper:
        raise _InvalidProof(f"{label} endpoints are reversed")
    return lower, upper


def _box(value: object) -> dict[str, tuple[Fraction, Fraction]]:
    document = _mapping(value, "pose box")
    if set(document) != {"cx", "cy", "t"}:
        raise _InvalidProof("pose box fields are incomplete")
    return {axis: _interval(document[axis], f"pose box {axis}") for axis in ("cx", "cy", "t")}


def _interval_add(
    left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    return left[0] + right[0], left[1] + right[1]


def _interval_scale(
    value: tuple[Fraction, Fraction], coefficient: Fraction
) -> tuple[Fraction, Fraction]:
    products = value[0] * coefficient, value[1] * coefficient
    return min(products), max(products)


def _rotation(
    value: tuple[Fraction, Fraction],
) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    lower, upper = value
    if lower < -1 or upper > 1:
        raise _InvalidProof("cover t interval exceeds the monotone proof range")
    maximum = max(abs(lower), abs(upper))
    minimum = Fraction(0) if lower <= 0 <= upper else min(abs(lower), abs(upper))

    def cosine(argument: Fraction) -> Fraction:
        return (1 - argument * argument) / (1 + argument * argument)

    def sine(argument: Fraction) -> Fraction:
        return 2 * argument / (1 + argument * argument)

    return (cosine(maximum), cosine(minimum)), (sine(lower), sine(upper))


def _corner_images(
    box: dict[str, tuple[Fraction, Fraction]],
) -> tuple[tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]], ...]:
    cosine, sine = _rotation(box["t"])
    offsets = (
        (Fraction(-1, 2), Fraction(-1, 2)),
        (Fraction(1, 2), Fraction(-1, 2)),
        (Fraction(1, 2), Fraction(1, 2)),
        (Fraction(-1, 2), Fraction(1, 2)),
    )
    return tuple(
        (
            _interval_add(
                _interval_add(box["cx"], _interval_scale(cosine, u)),
                _interval_scale(sine, -v),
            ),
            _interval_add(
                _interval_add(box["cy"], _interval_scale(sine, u)),
                _interval_scale(cosine, v),
            ),
        )
        for u, v in offsets
    )


def _document_images(
    value: object,
) -> tuple[tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]], ...]:
    images = _sequence(value, "corner images", 4)
    parsed = []
    for index, image in enumerate(images):
        item = _mapping(image, "corner image")
        if set(item) != {"x", "y"}:
            raise _InvalidProof("corner image fields are incomplete")
        parsed.append(
            (
                _interval(item["x"], f"corner {index} x"),
                _interval(item["y"], f"corner {index} y"),
            )
        )
    return tuple(parsed)


def _verify_binding(value: object, expected: dict[str, object]) -> dict[str, Any]:
    binding = _mapping(value, "binding")
    if binding != expected:
        raise _InvalidProof("binding does not match the independently supplied source facts")
    if binding.get("model") not in _MODELS:
        raise _InvalidProof("source model is invalid")
    for name in ("source_sha256", "polygon_sha256"):
        digest = binding.get(name)
        if not isinstance(digest, str) or _DIGEST.fullmatch(digest) is None:
            raise _InvalidProof(f"{name} is invalid")
    transform = _sequence(binding.get("transform"), "transform", 6)
    a, b, c, d, _, _ = (_fraction(item, "transform coefficient") for item in transform)
    if a * d - b * c == 0:
        raise _InvalidProof("source transform is singular")
    container = _mapping(binding.get("container"), "container")
    required = {"x0", "y0", "width", "height", "side", "normalization"}
    if set(container) != required:
        raise _InvalidProof("container binding fields are incomplete")
    for name in ("x0", "y0", "width", "height", "side"):
        _fraction(container[name], f"container {name}")
    if any(_fraction(container[name], name) <= 0 for name in ("width", "height", "side")):
        raise _InvalidProof("container dimensions must be positive")
    if container["normalization"] != "x=L*(X-x0)/W;y=L*(y0+H-Y)/H":
        raise _InvalidProof("container normalization is unbound")
    return binding


def _verify_witness(
    value: object, binding: dict[str, Any]
) -> tuple[
    list[tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]],
    tuple[int, ...],
    dict[str, Fraction],
]:
    witness = _mapping(value, "witness")
    if (
        witness.get("format") != "UnitSquareExactWitness/v1"
        or witness.get("binding") != binding
    ):
        raise _InvalidProof("witness format or binding is invalid")
    correspondence = tuple(_sequence(witness.get("correspondence"), "correspondence", 4))
    if correspondence not in _DIHEDRAL:
        raise _InvalidProof("correspondence is not one of the eight dihedral actions")
    pose_doc = _mapping(witness.get("pose"), "pose")
    pose = {name: _fraction(pose_doc.get(name), f"pose {name}") for name in ("cx", "cy", "t")}
    if not Fraction(-1, 2) <= pose["t"] <= Fraction(1, 2):
        raise _InvalidProof("witness is outside the frozen quotient")
    denominator = 1 + pose["t"] * pose["t"]
    cosine = (1 - pose["t"] * pose["t"]) / denominator
    sine = 2 * pose["t"] / denominator
    rotation = _mapping(witness.get("rotation"), "rotation")
    declared_cosine = _fraction(rotation.get("c"), "rotation cosine")
    declared_sine = _fraction(rotation.get("s"), "rotation sine")
    if (declared_cosine, declared_sine) != (cosine, sine):
        raise _InvalidProof("half-angle rotation does not match t")
    if declared_cosine * declared_cosine + declared_sine * declared_sine != 1:
        raise _InvalidProof("half-angle rotation does not satisfy c^2+s^2=1")
    cells_doc = _sequence(witness.get("source_cells"), "source cells", 4)
    cells = []
    for index, item in enumerate(cells_doc):
        cell = _mapping(item, "source cell")
        cells.append(
            (
                _interval(cell.get("x"), f"cell {index} x"),
                _interval(cell.get("y"), f"cell {index} y"),
            )
        )
    digest = hashlib.sha256(
        json.dumps(cells_doc, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if witness.get("source_cells_sha256") != digest:
        raise _InvalidProof("source-cell digest mismatch")
    offsets = ((-1, -1), (1, -1), (1, 1), (-1, 1))
    corners = tuple(
        (
            pose["cx"] + cosine * Fraction(u, 2) - sine * Fraction(v, 2),
            pose["cy"] + sine * Fraction(u, 2) + cosine * Fraction(v, 2),
        )
        for u, v in offsets
    )
    declared = _sequence(witness.get("corners"), "witness corners", 4)
    if (
        tuple((_fraction(p[0], "corner x"), _fraction(p[1], "corner y")) for p in declared)
        != corners
    ):
        raise _InvalidProof("witness corners do not replay")
    for source_index, corner_index in enumerate(correspondence):
        x, y = corners[corner_index]
        if (
            not cells[source_index][0][0] <= x <= cells[source_index][0][1]
            or not cells[source_index][1][0] <= y <= cells[source_index][1][1]
        ):
            raise _InvalidProof("witness corner is outside its source cell")
    return cells, correspondence, pose


def _verify_cover(
    value: object,
    cells: list[tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]],
    correspondence: tuple[int, ...],
    expected_region: dict[str, tuple[Fraction, Fraction]] | None = None,
) -> tuple[dict[str, tuple[Fraction, Fraction]], list[dict[str, tuple[Fraction, Fraction]]]]:
    node = _mapping(value, "cover node")
    region = _box(node.get("region"))
    if expected_region is not None and region != expected_region:
        raise _InvalidProof("cover child does not match its declared partition")
    kind = node.get("kind")
    if kind == "split":
        axis = node.get("axis")
        if axis not in ("cx", "cy", "t"):
            raise _InvalidProof("cover split axis is invalid")
        cut = _fraction(node.get("cut"), "cover split")
        lower, upper = region[axis]
        if not lower < cut < upper:
            raise _InvalidProof("cover split is not interior")
        lower_region = dict(region)
        upper_region = dict(region)
        lower_region[axis] = lower, cut
        upper_region[axis] = cut, upper
        _, lower_retained = _verify_cover(
            node.get("lower"), cells, correspondence, lower_region
        )
        _, upper_retained = _verify_cover(
            node.get("upper"), cells, correspondence, upper_region
        )
        return region, lower_retained + upper_retained
    if kind != "leaf" or node.get("status") not in ("retained", "rejected"):
        raise _InvalidProof("cover leaf is invalid")
    images = _corner_images(region)
    if node["status"] == "retained":
        if _document_images(node.get("corner_images")) != images:
            raise _InvalidProof("retained outward corner images do not replay")
        return region, [region]
    rejection = _mapping(node.get("rejection"), "rejection")
    source_index = rejection.get("source_index")
    corner_index = rejection.get("corner_index")
    coordinate = rejection.get("coordinate")
    relation = rejection.get("relation")
    if not isinstance(source_index, int) or not 0 <= source_index < 4:
        raise _InvalidProof("rejection source index is invalid")
    if (
        not isinstance(corner_index, int)
        or corner_index != correspondence[source_index]
        or coordinate not in ("x", "y")
    ):
        raise _InvalidProof("rejection correspondence is invalid")
    image = images[corner_index][0 if coordinate == "x" else 1]
    cell = cells[source_index][0 if coordinate == "x" else 1]
    if not (
        (relation == "below" and image[1] < cell[0])
        or (relation == "above" and image[0] > cell[1])
    ):
        raise _InvalidProof("rejection inequality does not replay")
    return region, []


def _wall_signs(
    retained: list[dict[str, tuple[Fraction, Fraction]]], side: Fraction
) -> dict[str, object]:
    if not retained:
        raise _InvalidProof("cover has no retained pose box")
    images = tuple(image for region in retained for image in _corner_images(region))
    xs = tuple(image[0] for image in images)
    ys = tuple(image[1] for image in images)
    walls = {
        "left": (min(x[0] for x in xs), min(x[1] for x in xs)),
        "right": (side - max(x[1] for x in xs), side - max(x[0] for x in xs)),
        "bottom": (min(y[0] for y in ys), min(y[1] for y in ys)),
        "top": (side - max(y[1] for y in ys), side - max(y[0] for y in ys)),
    }
    minimum = min(v[0] for v in walls.values()), min(v[1] for v in walls.values())
    decision = (
        "nonnegative" if minimum[0] >= 0 else "negative" if minimum[1] < 0 else "undecided"
    )

    def text(value: Fraction) -> str:
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"

    return {
        "walls": {name: [text(value[0]), text(value[1])] for name, value in walls.items()},
        "minimum": [text(minimum[0]), text(minimum[1])],
        "decision": decision,
    }


def _pair_signs(value: object) -> dict[str, object]:
    document = _mapping(value, "pair signs")
    boxes = _box(document.get("first")), _box(document.get("second"))
    poses = []
    for box in boxes:
        if any(lower != upper for lower, upper in box.values()):
            raise _InvalidProof("pair control is not a point-pose box")
        poses.append({axis: box[axis][0] for axis in ("cx", "cy", "t")})
    rotations = []
    for pose in poses:
        denominator = 1 + pose["t"] * pose["t"]
        rotations.append(
            ((1 - pose["t"] * pose["t"]) / denominator, 2 * pose["t"] / denominator)
        )
    axes = (
        rotations[0],
        (-rotations[0][1], rotations[0][0]),
        rotations[1],
        (-rotations[1][1], rotations[1][0]),
    )
    delta = poses[1]["cx"] - poses[0]["cx"], poses[1]["cy"] - poses[0]["cy"]
    gaps = []
    for nx, ny in axes:
        distance = abs(delta[0] * nx + delta[1] * ny)
        widths = []
        for cosine, sine in rotations:
            widths.append((abs(nx * cosine + ny * sine) + abs(-nx * sine + ny * cosine)) / 2)
        gaps.append(distance - widths[0] - widths[1])

    def text(number: Fraction) -> str:
        if number.denominator == 1:
            return str(number.numerator)
        return f"{number.numerator}/{number.denominator}"

    maximum = max(gaps)
    decision = "separated" if maximum > 0 else "overlap" if maximum < 0 else "possible-contact"
    return {
        "first": document["first"],
        "second": document["second"],
        "axis_gaps": [[text(gap), text(gap)] for gap in gaps],
        "maximum": [text(maximum), text(maximum)],
        "decision": decision,
    }


def _verify_pair_controls(value: object) -> None:
    controls = _sequence(value, "pair controls", 3)
    expected = (
        ("separated", "separated"),
        ("tangent", "possible-contact"),
        ("overlap", "overlap"),
    )
    for item, (label, decision) in zip(controls, expected, strict=True):
        control = _mapping(item, "pair control")
        if control.get("label") != label:
            raise _InvalidProof("pair-control order is invalid")
        signs = _pair_signs(control.get("signs"))
        if control.get("signs") != signs or signs["decision"] != decision:
            raise _InvalidProof("pair-sign intervals do not replay")


def _verify_proof_or_raise(
    document: object,
    expected_binding: dict[str, object],
    expected_source_cells_sha256: str,
) -> None:
    envelope = _mapping(document, "proof envelope")
    if set(envelope) != {"proof", "proof_sha256"}:
        raise _InvalidProof("proof envelope fields are invalid")
    proof = _mapping(envelope["proof"], "proof")
    canonical = json.dumps(proof, sort_keys=True, separators=(",", ":")).encode()
    if envelope["proof_sha256"] != hashlib.sha256(canonical).hexdigest():
        raise _InvalidProof("proof digest mismatch")
    if proof.get("format") != "UnitSquarePoseProof/v1":
        raise _InvalidProof("proof format is invalid")
    binding = _verify_binding(proof.get("binding"), expected_binding)
    cells, correspondence, pose = _verify_witness(proof.get("witness"), binding)
    witness = _mapping(proof.get("witness"), "witness")
    if witness.get("source_cells_sha256") != expected_source_cells_sha256:
        raise _InvalidProof("source cells do not match the independently supplied digest")
    root, retained = _verify_cover(proof.get("cover"), cells, correspondence)
    if root["t"] != (Fraction(-1, 2), Fraction(1, 2)):
        raise _InvalidProof("cover root is not the frozen t quotient")
    if any(not root[axis][0] <= pose[axis] <= root[axis][1] for axis in ("cx", "cy", "t")):
        raise _InvalidProof("witness lies outside the cover root")
    for axis, coordinate in (("cx", 0), ("cy", 1)):
        lower = max(cell[coordinate][0] - 1 for cell in cells)
        upper = min(cell[coordinate][1] + 1 for cell in cells)
        if root[axis][0] > lower or root[axis][1] < upper:
            raise _InvalidProof("cover root does not enclose the source-derived center bound")
    side = _fraction(binding["container"]["side"], "container side")
    if proof.get("wall_signs") != _wall_signs(retained, side):
        raise _InvalidProof("wall-sign intervals do not replay")
    _verify_pair_controls(proof.get("pair_controls"))


def verify_proof(
    document: object,
    expected_binding: dict[str, object],
    expected_source_cells_sha256: str,
) -> list[str]:
    """Return bounded errors for a source-bound proof receipt."""

    try:
        _verify_proof_or_raise(document, expected_binding, expected_source_cells_sha256)
    except (KeyError, IndexError, TypeError, _InvalidProof) as error:
        return [
            str(error) if isinstance(error, _InvalidProof) else "proof structure is malformed"
        ]
    return []
