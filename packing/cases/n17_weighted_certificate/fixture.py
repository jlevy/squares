"""Static, exact reconstruction of the retained Massaccesi fixture data."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from cases.n17_weighted_certificate.extract import StaticExtractionError, verified_source
from cases.n17_weighted_certificate.model import Atom, Direction, scaling_preconditions

RETAINED_SHA256 = "04531a54da9a654f2318401aff43222daf721bd99e948b2491f91c05bd0b5d3f"
RETAINED_PATH = (
    Path(__file__).parents[2] / "resources/web/n17-lower-bounds-2026/"
    "massaccesi-verify-n17-lower-bound-4_5058.py"
)


@dataclass(frozen=True, slots=True)
class RetainedFixture:
    outer_side: Fraction
    shrink_margin: Fraction
    square_side: Fraction
    angle_limit: Fraction
    direction_steps: int
    weight_scale: int
    grid_size: int
    certificate: tuple[tuple[int, int, int], ...]
    atoms: tuple[Atom, ...]
    directions: tuple[Direction, ...]


def _value(node: ast.AST, known: dict[str, Any]) -> Any:  # noqa: PLR0911
    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        return node.value
    if isinstance(node, ast.Name) and node.id in known:
        return known[node.id]
    if isinstance(node, ast.Tuple):
        return tuple(_value(item, known) for item in node.elts)
    if isinstance(node, ast.List):
        return [_value(item, known) for item in node.elts]
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_value(node.operand, known)
    if isinstance(node, ast.BinOp):
        left = _value(node.left, known)
        right = _value(node.right, known)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "F"
        and not node.keywords
        and 1 <= len(node.args) <= 2
    ):
        return Fraction(*(_value(arg, known) for arg in node.args))
    raise StaticExtractionError(f"unsupported retained-fixture expression: {ast.dump(node)}")


def _assignments(path: Path) -> dict[str, Any]:
    source = verified_source(path, RETAINED_SHA256)
    tree = ast.parse(source, filename=str(path))
    required = {
        "L",
        "M",
        "B",
        "T",
        "KMAX",
        "WEIGHT_SCALE",
        "NGRID",
        "LAST",
        "CERT",
    }
    known: dict[str, Any] = {}
    for statement in tree.body:
        if not isinstance(statement, ast.Assign) or len(statement.targets) != 1:
            continue
        target = statement.targets[0]
        if not isinstance(target, ast.Name):
            continue
        try:
            known[target.id] = _value(statement.value, known)
        except StaticExtractionError:
            if target.id in required:
                raise
    missing = required - known.keys()
    if missing:
        raise StaticExtractionError(f"missing retained assignments: {sorted(missing)}")
    return known


def _orbit(i: int, j: int, last: int) -> set[tuple[int, int]]:
    return {
        (i, j),
        (last - i, j),
        (i, last - j),
        (last - i, last - j),
        (j, i),
        (last - j, i),
        (j, last - i),
        (last - j, last - i),
    }


def load_retained_fixture(path: Path = RETAINED_PATH) -> RetainedFixture:
    """Parse only exact top-level data and reconstruct atoms without executing source."""

    values = _assignments(path)
    outer_side = Fraction(values["L"])
    margin = Fraction(values["M"])
    square_side = Fraction(values["B"])
    angle_limit = Fraction(values["T"])
    steps = int(values["KMAX"])
    scale = int(values["WEIGHT_SCALE"])
    grid_size = int(values["NGRID"])
    last = int(values["LAST"])
    certificate_rows: list[tuple[int, int, int]] = []
    for row in values["CERT"]:
        if not isinstance(row, list | tuple) or len(row) != 3:
            raise StaticExtractionError("certificate row is not an integer triple")
        i, j, weight = row
        certificate_rows.append((int(i), int(j), int(weight)))
    certificate = tuple(certificate_rows)

    grid_step = (outer_side - margin) / last
    coordinates = tuple(margin / 2 + grid_step * index for index in range(grid_size))
    by_index: dict[tuple[int, int], int] = {}
    for i, j, weight in certificate:
        for grid_point in _orbit(i, j, last):
            if grid_point in by_index:
                raise StaticExtractionError(f"duplicate orbit assignment at {grid_point}")
            by_index[grid_point] = weight
    atoms = tuple(
        Atom(f"{i:02d},{j:02d}", coordinates[i], coordinates[j], Fraction(weight))
        for (i, j), weight in sorted(by_index.items())
    )

    directions: list[Direction] = []
    for index in range(steps + 1):
        tangent = angle_limit * index / steps
        denominator = 1 + tangent * tangent
        cosine = (1 - tangent * tangent) / denominator
        sine = 2 * tangent / denominator
        if cosine * cosine + sine * sine != 1:
            raise StaticExtractionError(f"direction {index} is not exactly unit length")
        directions.append(Direction(str(index), cosine, sine, -sine, cosine))

    fixture = RetainedFixture(
        outer_side=outer_side,
        shrink_margin=margin,
        square_side=square_side,
        angle_limit=angle_limit,
        direction_steps=steps,
        weight_scale=scale,
        grid_size=grid_size,
        certificate=certificate,
        atoms=atoms,
        directions=tuple(directions),
    )
    if len(fixture.atoms) != 168 or sum(atom.weight for atom in fixture.atoms) != 9744:
        raise StaticExtractionError("retained atom count or exact total differs from metadata")
    if len(fixture.directions) != 181 or fixture.grid_size != 29:
        raise StaticExtractionError("retained grid or direction count differs from metadata")
    if scaling_preconditions(
        outer_side=outer_side,
        internal_side=outer_side - margin,
        shrink_margin=margin,
    ) != (True, True, True):
        raise StaticExtractionError("retained side decomposition failed")
    return fixture
