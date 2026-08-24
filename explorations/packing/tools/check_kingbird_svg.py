#!/usr/bin/env python3
"""Reconstruct and independently screen a Kingbird square-packing SVG.

The catalogue encodes unit squares in two ways: explicit ``#one`` uses for rotated
pieces and filled orthogonal polyomino paths for axis-aligned blocks.  This importer
materialises both into four-corner polygons, then sends those polygons through the
separate SAT oracle in :mod:`sqpack.verify` at high precision.

This is a numerical source-reconstruction check, not an exact packing certificate.
The retained SVG gives roughly 100 decimal digits; contacts are classified with a
declared tolerance far below the separation between its angle classes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sqpack.verify import edge_axes, project, verify_packing

SVG = "{http://www.w3.org/2000/svg}"
XLINK_HREF = "{http://www.w3.org/1999/xlink}href"
ENTITY_RE = re.compile(r'<!ENTITY\s+([A-Za-z][A-Za-z0-9]*)\s+"([^"]+)">')
TRANSFORM_RE = re.compile(r"([A-Za-z]+)\s*\(([^)]*)\)")
NUMBER_RE = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?")
PATH_TOKEN_RE = re.compile(r"[A-Za-z]|[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?")

DECIMAL_DIGITS = 160
ZERO_TOLERANCE = mp.mpf("1e-80")
ANGLE_MATCH_TOLERANCE_DEGREES = mp.mpf("1e-70")
ANGLE_INTERVAL_RADIUS_DEGREES = mp.mpf("1e-90")

# The upstream response retrieved on 2026-08-24 used CRLF and no terminal newline.
# The checked-in mirror is text-normalised to LF, so both identities are retained.
UPSTREAM_URL = "https://kingbird.myphotos.cc/packing/square-29.svg"
UPSTREAM_SHA256 = "30c725b27e1b90ff0c9c238fb8923c3da6ce26e046cdd46d5c33a485bbec821c"
NORMALISED_SHA256 = "d25d36f87a75066b13fb9f88c67b9feb2d99eaa6e9a310295dcbf3591b6b3726"


def identity():
    return (mp.mpf(1), mp.mpf(0), mp.mpf(0), mp.mpf(1), mp.mpf(0), mp.mpf(0))


def compose(left, right):
    """Return the affine map ``left(right(point))`` in SVG matrix order."""
    la, lb, lc, ld, le, lf = left
    ra, rb, rc, rd, re_, rf = right
    return (
        la * ra + lc * rb,
        lb * ra + ld * rb,
        la * rc + lc * rd,
        lb * rc + ld * rd,
        la * re_ + lc * rf + le,
        lb * re_ + ld * rf + lf,
    )


def apply(matrix, point):
    a, b, c, d, e, f = matrix
    x, y = point
    return a * x + c * y + e, b * x + d * y + f


def translate(x, y=None):
    if y is None:
        y = mp.mpf(0)
    return (mp.mpf(1), mp.mpf(0), mp.mpf(0), mp.mpf(1), x, y)


def scale(x, y=None):
    if y is None:
        y = x
    return (x, mp.mpf(0), mp.mpf(0), y, mp.mpf(0), mp.mpf(0))


def rotate(degrees):
    radians = mp.radians(degrees)
    cosine, sine = mp.cos(radians), mp.sin(radians)
    return (cosine, sine, -sine, cosine, mp.mpf(0), mp.mpf(0))


def rotate_vector(degrees, point):
    return apply(rotate(degrees), point)


def vector_sum(*vectors):
    return sum(vector[0] for vector in vectors), sum(vector[1] for vector in vectors)


def vector_difference(left, right):
    return left[0] - right[0], left[1] - right[1]


def parse_transform(value: str | None):
    result = identity()
    if not value:
        return result
    consumed = ""
    for match in TRANSFORM_RE.finditer(value):
        consumed += match.group(0)
        name = match.group(1)
        args = [mp.mpf(token) for token in NUMBER_RE.findall(match.group(2))]
        if name == "translate" and len(args) in {1, 2}:
            operation = translate(args[0], args[1] if len(args) == 2 else mp.mpf(0))
        elif name == "scale" and len(args) in {1, 2}:
            operation = scale(args[0], args[1] if len(args) == 2 else None)
        elif name == "rotate" and len(args) == 1:
            operation = rotate(args[0])
        else:
            raise ValueError(f"unsupported SVG transform: {match.group(0)}")
        result = compose(result, operation)
    if re.sub(r"[\s,]", "", consumed) != re.sub(r"[\s,]", "", value):
        raise ValueError(f"unparsed SVG transform text: {value}")
    return result


def integer(value) -> int:
    rounded = int(mp.nint(value))
    if abs(value - rounded) > ZERO_TOLERANCE:
        raise ValueError(f"expected an integer grid coordinate, got {value}")
    return rounded


def path_vertices(description: str):
    tokens = PATH_TOKEN_RE.findall(description)
    vertices = []
    command = None
    x = y = mp.mpf(0)
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token.isalpha():
            command = token.upper()
            index += 1
            if command == "Z":
                continue
        if command in {"M", "L"}:
            if (
                index + 1 >= len(tokens)
                or tokens[index].isalpha()
                or tokens[index + 1].isalpha()
            ):
                raise ValueError(f"incomplete {command} command in path {description!r}")
            x, y = mp.mpf(tokens[index]), mp.mpf(tokens[index + 1])
            index += 2
            vertices.append((x, y))
            if command == "M":
                command = "L"
        elif command == "H":
            x = mp.mpf(tokens[index])
            index += 1
            vertices.append((x, y))
        elif command == "V":
            y = mp.mpf(tokens[index])
            index += 1
            vertices.append((x, y))
        elif command == "Z":
            command = None
        else:
            raise ValueError(f"unsupported path command {command!r} in {description!r}")
    if len(vertices) < 3:
        raise ValueError(f"filled path has fewer than three vertices: {description!r}")
    return vertices


def point_inside_polygon(point, vertices) -> bool:
    x, y = point
    inside = False
    previous = vertices[-1]
    for current in vertices:
        x1, y1 = previous
        x2, y2 = current
        if (y1 > y) != (y2 > y):
            crossing_x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < crossing_x:
                inside = not inside
        previous = current
    return inside


def unit_cells_from_path(description: str):
    vertices = path_vertices(description)
    min_x = min(integer(x) for x, _ in vertices)
    max_x = max(integer(x) for x, _ in vertices)
    min_y = min(integer(y) for _, y in vertices)
    max_y = max(integer(y) for _, y in vertices)
    cells = [
        (x, y)
        for y in range(min_y, max_y)
        for x in range(min_x, max_x)
        if point_inside_polygon(
            (mp.mpf(x) + mp.mpf("0.5"), mp.mpf(y) + mp.mpf("0.5")), vertices
        )
    ]
    twice_area = abs(
        sum(
            x1 * y2 - x2 * y1
            for (x1, y1), (x2, y2) in zip(vertices, vertices[1:] + vertices[:1], strict=True)
        )
    )
    area = twice_area / 2
    if abs(area - len(cells)) > ZERO_TOLERANCE:
        raise ValueError(
            f"filled path is not a union of whole unit cells: area={area}, cells={len(cells)}"
        )
    return cells


def local_square(x, y):
    return [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]


def materialise_svg(source: Path):
    raw = source.read_bytes()
    text = raw.decode("utf-8")
    entities = {name: mp.mpf(value) for name, value in ENTITY_RE.findall(text)}
    root = ET.fromstring(raw)
    view_box = [mp.mpf(value) for value in root.attrib["viewBox"].split()]
    if view_box[:2] != [mp.mpf(0), mp.mpf(0)] or view_box[2] != view_box[3]:
        raise ValueError(f"expected a square origin-zero viewBox, got {view_box}")
    side = view_box[2]
    squares = []

    def visit(node, parent_matrix) -> None:
        tag = node.tag.removeprefix(SVG)
        if tag == "defs":
            return
        matrix = compose(parent_matrix, parse_transform(node.attrib.get("transform")))
        style = re.sub(r"\s", "", node.attrib.get("style", ""))
        if tag == "use" and node.attrib.get(XLINK_HREF) == "#one":
            squares.append(
                [apply(matrix, point) for point in local_square(mp.mpf(0), mp.mpf(0))]
            )
        elif tag == "path" and "fill:none" not in style:
            for x, y in unit_cells_from_path(node.attrib["d"]):
                squares.append(
                    [apply(matrix, point) for point in local_square(mp.mpf(x), mp.mpf(y))]
                )
        elif tag == "rect" and "fill:none" not in style:
            x = integer(mp.mpf(node.attrib.get("x", "0")))
            y = integer(mp.mpf(node.attrib.get("y", "0")))
            width = integer(mp.mpf(node.attrib["width"]))
            height = integer(mp.mpf(node.attrib["height"]))
            squares.extend(
                [apply(matrix, point) for point in local_square(mp.mpf(cell_x), mp.mpf(cell_y))]
                for cell_y in range(y, y + height)
                for cell_x in range(x, x + width)
            )
        for child in node:
            visit(child, matrix)

    visit(root, identity())
    return raw, entities, side, squares


def canonical_angle_degrees(square):
    (x0, y0), (x1, y1) = square[:2]
    angle = mp.degrees(mp.atan2(y1 - y0, x1 - x0))
    canonical = mp.fmod(angle + 45, 90)
    if canonical < 0:
        canonical += 90
    canonical -= 45
    return mp.mpf(0) if abs(canonical) < ANGLE_MATCH_TOLERANCE_DEGREES else canonical


def classify_angles(squares, entities):
    expected = {
        "axis": mp.mpf(0),
        "a": entities["a"],
        "b": entities["b"],
        "-c": -entities["c"],
        "d": entities["d"],
        "i": entities["i"],
    }
    counts: Counter[str] = Counter()
    observed = []
    for square in squares:
        angle = canonical_angle_degrees(square)
        matches = [
            label
            for label, reference in expected.items()
            if abs(angle - reference) <= ANGLE_MATCH_TOLERANCE_DEGREES
        ]
        if len(matches) != 1:
            raise ValueError(f"orientation {mp.nstr(angle, 30)} matched labels {matches}")
        counts[matches[0]] += 1
        observed.append(angle)
    ordered = ["axis", "a", "b", "-c", "d", "i"]
    minimum_gap = min(
        abs(expected[left] - expected[right])
        for index, left in enumerate(ordered)
        for right in ordered[index + 1 :]
    )
    if minimum_gap <= 2 * ANGLE_INTERVAL_RADIUS_DEGREES:
        raise ValueError("declared angle intervals overlap")
    return expected, counts, observed, minimum_gap


def sign(value) -> int:
    if value > ZERO_TOLERANCE:
        return 1
    if value < -ZERO_TOLERANCE:
        return -1
    return 0


def pair_separation_margin(first, second):
    margins = []
    for axis in edge_axes(first) + edge_axes(second):
        first_lo, first_hi = project(first, axis, sign)
        second_lo, second_hi = project(second, axis, sign)
        margins.append(max(second_lo - first_hi, first_lo - second_hi))
    return max(margins)


def source_equation_residuals(entities):
    """Recompute every derived offset and defining equation in the SVG comment."""
    s = entities["s"]
    a, b, c, d, i = (entities[name] for name in ("a", "b", "c", "d", "i"))

    def sin(degrees):
        return mp.sin(mp.radians(degrees))

    def cos(degrees):
        return mp.cos(mp.radians(degrees))

    derived = {}
    derived["r1"] = (s - 5) * sin(a)
    derived["r2"] = 1 - (s - 5) * cos(b)
    derived["r3"] = (
        vector_sum((s - 1, mp.mpf(3)), rotate_vector(-c, (-1, 1)))[1] - (s - 2)
    ) / cos(c)
    derived["r4"] = (
        vector_sum((s - 3, mp.mpf(1)), rotate_vector(a, (1 - (s - 5) * cos(a), 0)))[1] - 1
    ) / cos(d)
    derived["r5"] = (
        (s - 1)
        - vector_sum(
            (mp.mpf(2), mp.mpf(1)),
            rotate_vector(a, (1, -derived["r1"])),
            rotate_vector(d, (1, -derived["r4"])),
            rotate_vector(d, (1, 0)),
        )[0]
    ) / sin(d)
    derived["r8"] = 2 - rotate_vector(-b, (4 - s, 1))[1]
    derived["rB"] = -vector_sum((s - 2, s - 2), rotate_vector(b, (-4, 1 - derived["r8"])))[
        0
    ] / sin(b)
    derived["rC"] = (
        1
        - rotate_vector(
            -i,
            vector_difference(
                vector_sum(
                    (s - 2, s - 2),
                    rotate_vector(b, (-3, -derived["r8"] - derived["rB"])),
                ),
                (mp.mpf(1), mp.mpf(2)),
            ),
        )[1]
    )
    derived["rD"] = rotate_vector(
        -b,
        vector_difference(
            vector_sum(
                (mp.mpf(2), mp.mpf(1)),
                rotate_vector(a, (1, 1 - derived["r1"])),
            ),
            vector_sum(
                (mp.mpf(1), mp.mpf(2)),
                rotate_vector(i, (1, -derived["rC"])),
            ),
        ),
    )[1] / cos(i - b)

    r1, r4, r5 = (entities[name] for name in ("r1", "r4", "r5"))
    r8, _r_b, r_c, r_d = (entities[name] for name in ("r8", "rB", "rC", "rD"))
    upper_middle = vector_sum(
        (mp.mpf(1), mp.mpf(2)),
        rotate_vector(i, (1, -r_c + r_d)),
        rotate_vector(b, (2, 0)),
    )
    f1 = rotate_vector(
        -a,
        vector_difference(
            vector_sum((mp.mpf(1), mp.mpf(2)), rotate_vector(i, (1, -r_c))),
            vector_sum((mp.mpf(2), mp.mpf(1)), rotate_vector(a, (0, 1 - r1))),
        ),
    )[1]
    f2 = rotate_vector(
        -d,
        vector_difference(
            upper_middle,
            vector_sum(
                (mp.mpf(2), mp.mpf(1)),
                rotate_vector(a, (1, -r1)),
                rotate_vector(d, (1, -r4)),
                rotate_vector(d, (0, 1 - r5)),
            ),
        ),
    )[1]
    f3 = rotate_vector(
        -b,
        vector_difference(
            upper_middle,
            vector_sum(
                (mp.mpf(2), mp.mpf(1)),
                rotate_vector(a, (1, -r1)),
                rotate_vector(d, (1, 1 - r4)),
            ),
        ),
    )[1]
    f4 = rotate_vector(
        -b,
        vector_difference(
            vector_sum((s - 1, mp.mpf(3)), rotate_vector(-c, (-1, -entities["r3"]))),
            upper_middle,
        ),
    )[0]
    f5 = rotate_vector(
        -b,
        vector_difference(
            vector_sum((s - 2, s - 2), rotate_vector(b, (-1, -r8))),
            vector_sum(
                (mp.mpf(1), mp.mpf(2)),
                rotate_vector(i, (1, -r_c + r_d)),
                rotate_vector(b, (0, 1)),
            ),
        ),
    )[1]
    f6 = (
        rotate_vector(
            c,
            vector_difference(
                (s - 1, mp.mpf(3)),
                vector_sum((s - 2, s - 2), rotate_vector(b, (0, -r8))),
            ),
        )[0]
        - 1
    )
    offset_errors = {name: derived[name] - entities[name] for name in derived}
    equation_residuals = dict(
        zip(("f1", "f2", "f3", "f4", "f5", "f6"), (f1, f2, f3, f4, f5, f6), strict=True)
    )
    maximum_offset_error = max(abs(value) for value in offset_errors.values())
    maximum_equation_residual = max(abs(value) for value in equation_residuals.values())
    if maximum_offset_error > ZERO_TOLERANCE or maximum_equation_residual > ZERO_TOLERANCE:
        raise ValueError(
            "source equations exceed the declared serialization tolerance: "
            f"offset={maximum_offset_error}, equation={maximum_equation_residual}"
        )
    return maximum_offset_error, maximum_equation_residual


def run_selftests(squares, side) -> dict[str, bool]:
    composition = parse_transform("translate(2 1) rotate(90) translate(1)")
    x, y = apply(composition, (mp.mpf(0), mp.mpf(0)))
    if abs(x - 2) > ZERO_TOLERANCE or abs(y - 2) > ZERO_TOLERANCE:
        raise AssertionError("SVG transform composition order is wrong")
    expected_polyomino_counts = {
        "M0,0 H2 V1 H1 V2 H0": 3,
        "M0,0 V3 H1 V1 H3 V0 H0": 5,
        "M0,0 H3 V1 H2 V2 H0": 5,
    }
    for description, expected in expected_polyomino_counts.items():
        if len(unit_cells_from_path(description)) != expected:
            raise AssertionError(f"polyomino extractor failed for {description}")
    duplicated = [list(square) for square in squares]
    duplicated[-1] = list(duplicated[0])
    if verify_packing(duplicated, side, sign=sign).valid:
        raise AssertionError("validity guard accepted a deliberate duplicate square")
    return {
        "transform_composition": True,
        "polyomino_cell_extraction": True,
        "duplicate_square_rejected": True,
    }


def decimal_string(value, digits: int = 100) -> str:
    return str(mp.nstr(value, n=digits, strip_zeros=False))


def build_result(source: Path) -> dict:
    started = time.monotonic()
    mp.mp.dps = DECIMAL_DIGITS
    raw, entities, side, squares = materialise_svg(source)
    source_sha256 = hashlib.sha256(raw).hexdigest()
    if (
        source.name == "kingbird-square-29-provenance.svg"
        and source_sha256 != NORMALISED_SHA256
    ):
        raise ValueError(
            f"retained n=29 source hash changed: {source_sha256} != {NORMALISED_SHA256}"
        )
    selftests = run_selftests(squares, side)
    report = verify_packing(squares, side, sign=sign)
    if not report.valid:
        raise ValueError(f"source reconstruction failed validity:\n{report}")
    expected, counts, _observed, minimum_angle_gap = classify_angles(squares, entities)
    maximum_offset_error, maximum_equation_residual = source_equation_residuals(entities)
    pair_margins = [
        pair_separation_margin(squares[left], squares[right])
        for left in range(len(squares))
        for right in range(left + 1, len(squares))
    ]
    container_margins = [
        margin for square in squares for x, y in square for margin in (x, y, side - x, side - y)
    ]
    return {
        "schema_version": 1,
        "source": {
            "path": source.as_posix(),
            "url": UPSTREAM_URL,
            "retrieved": "2026-08-24",
            "upstream_sha256": UPSTREAM_SHA256,
            "normalisation": "CRLF converted to LF and one terminal newline added",
            "retained_sha256": source_sha256,
            "retained_bytes": len(raw),
        },
        "precision": {
            "decimal_digits": DECIMAL_DIGITS,
            "zero_tolerance": decimal_string(ZERO_TOLERANCE, 5),
            "angle_match_tolerance_degrees": decimal_string(ANGLE_MATCH_TOLERANCE_DEGREES, 5),
            "angle_interval_radius_degrees": decimal_string(ANGLE_INTERVAL_RADIUS_DEGREES, 5),
            "claim_scope": (
                "high-precision numerical source reconstruction; not an exact certificate"
            ),
        },
        "packing": {
            "n": len(squares),
            "side": decimal_string(side),
            "valid": report.valid,
            "pairs_tested": report.pairs_tested,
            "touching_pairs_within_tolerance": report.touching_pairs,
            "strict_pairs": report.strict_pairs,
            "container_contacts_within_tolerance": report.container_contacts,
            "minimum_pair_separation_margin": decimal_string(min(pair_margins), 30),
            "smallest_strict_pair_separation": decimal_string(
                min(margin for margin in pair_margins if margin > ZERO_TOLERANCE), 30
            ),
            "minimum_container_margin": decimal_string(min(container_margins), 30),
        },
        "source_equations": {
            "derived_offsets_checked": [
                "r1",
                "r2",
                "r3",
                "r4",
                "r5",
                "r8",
                "rB",
                "rC",
                "rD",
            ],
            "defining_equations_checked": ["f1", "f2", "f3", "f4", "f5", "f6"],
            "maximum_offset_discrepancy": decimal_string(maximum_offset_error, 30),
            "maximum_equation_residual": decimal_string(maximum_equation_residual, 30),
        },
        "orientation_rule": {
            "quotient_degrees": 90,
            "canonical_interval_degrees": "[-45, 45)",
            "merge_rule": "same symbolic entity or overlapping declared decimal intervals",
            "minimum_class_gap_degrees": decimal_string(minimum_angle_gap, 30),
        },
        "orientation_classes": [
            {
                "label": label,
                "degrees": decimal_string(expected[label], 30),
                "count": counts[label],
            }
            for label in ("axis", "a", "b", "-c", "d", "i")
        ],
        "orientation_class_count": len(counts),
        "selftests": selftests,
        "elapsed_seconds": round(time.monotonic() - started, 6),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="retained Kingbird SVG")
    parser.add_argument("--record", type=Path, help="write the JSON evidence record atomically")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = build_result(args.source)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.record:
        args.record.parent.mkdir(parents=True, exist_ok=True)
        temporary = args.record.with_suffix(args.record.suffix + ".tmp")
        temporary.write_text(rendered)
        temporary.replace(args.record)
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
