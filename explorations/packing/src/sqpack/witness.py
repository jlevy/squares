"""Generic interchange, inspection, checking, and verification for packing witnesses."""

from __future__ import annotations

import json
import math
import shlex
from collections.abc import Callable, Mapping, Sequence
from copy import deepcopy
from dataclasses import asdict
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath as mp
import yaml
from jsonschema import Draft202012Validator
from strif import atomic_output_file

from sqpack.field import FieldElement, NumberField
from sqpack.verify import Report, edge_axes, exact_sign, project, verify_packing
from sqpack.yamlio import load_yaml

type Scalar = Any
type Point = tuple[Scalar, Scalar]
type Square = list[Point]


class WitnessError(ValueError):
    """A typed witness failure suitable for both human and machine callers."""

    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = kind


def load_witness(path: Path, *, fallback_schema: Path | None = None) -> dict[str, Any]:
    """Load and structurally validate one Witness/v1 YAML artifact."""
    try:
        document = load_yaml(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise WitnessError("malformed-input", f"invalid or ambiguous YAML: {error}") from error
    if not isinstance(document, dict):
        raise WitnessError("malformed-input", "witness document is not an object")
    metadata = document.get("softschema")
    witness = document.get("witness")
    if not isinstance(metadata, dict) or not isinstance(witness, dict):
        raise WitnessError("malformed-input", "expected softschema and witness objects")
    if metadata.get("contract") != "packing.squares:Witness/v1":
        raise WitnessError("unsupported-contract", "expected packing.squares:Witness/v1")
    schema_path = path.parent / str(metadata.get("schema", "witness.schema.yaml"))
    if not schema_path.is_file() and fallback_schema is not None:
        schema_path = fallback_schema
    if not schema_path.is_file():
        raise WitnessError(
            "schema-missing",
            f"witness schema not found at {schema_path}",
        )
    try:
        schema = load_yaml(schema_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise WitnessError(
            "schema-invalid", f"invalid or ambiguous schema YAML: {error}"
        ) from error
    problems = sorted(
        Draft202012Validator(schema).iter_errors(witness), key=lambda error: list(error.path)
    )
    if problems:
        problem = problems[0]
        location = ".".join(str(part) for part in problem.path) or "witness"
        raise WitnessError("schema-invalid", f"{location}: {problem.message}")
    semantic_problems = check_witness_semantics(witness)
    if semantic_problems:
        raise WitnessError("semantic-invalid", semantic_problems[0])
    return witness


def check_witness_semantics(witness: Mapping[str, Any]) -> list[str]:
    """Enforce cross-field rules the JSON schema cannot express clearly."""
    problems: list[str] = []
    squares = witness.get("squares")
    n = witness.get("n")
    if not isinstance(squares, list) or len(squares) != n:
        problems.append(f"n={n!r} but the artifact contains {len(squares or [])} squares")
        return problems
    ids = [square.get("id") for square in squares if isinstance(square, Mapping)]
    if len(ids) != len(set(ids)):
        problems.append("square ids must be unique")

    representation = str(witness.get("representation"))
    required = {
        "corners": {"corners"},
        "center-angle": {"center", "angle"},
        "center-basis": {"center", "basis"},
    }.get(representation, set())
    allowed = required | {"id"}
    for index, square in enumerate(squares, start=1):
        if not isinstance(square, Mapping):
            continue
        missing = required - set(square)
        extra_geometry = ({"corners", "center", "angle", "basis"} & set(square)) - required
        if missing:
            problems.append(f"square {index} is missing {sorted(missing)} for {representation}")
        if extra_geometry:
            problems.append(
                f"square {index} has incompatible geometry fields {sorted(extra_geometry)}"
            )
        if set(square) - allowed:
            problems.append(
                f"square {index} has unsupported fields {sorted(set(square) - allowed)}"
            )

    coordinates = witness.get("coordinates") or {}
    angle_unit = coordinates.get("angle_unit")
    if representation == "center-angle" and angle_unit not in {"degrees", "radians"}:
        problems.append("center-angle geometry requires degrees or radians")
    if representation != "center-angle" and angle_unit != "not-applicable":
        problems.append(f"{representation} geometry requires angle_unit: not-applicable")

    scalar_kind = (witness.get("scalar") or {}).get("kind")
    claim = witness.get("claim") or {}
    provenance, method = claim.get("coordinate_provenance"), claim.get("method")
    if method in {"numerical-f64", "numerical-multiprecision"}:
        if provenance == "verified":
            problems.append("a numerical method cannot support coordinate_provenance: verified")
        if claim.get("precision") is None or claim.get("tolerance") is None:
            problems.append("numerical claims require actual precision and tolerance")
        precision = claim.get("precision")
        if method == "numerical-f64" and (
            not isinstance(precision, Mapping)
            or precision.get("binary_bits") != 53
            or "decimal_digits" in precision
        ):
            problems.append("numerical-f64 claims require binary_bits: 53")
        if method == "numerical-multiprecision" and (
            not isinstance(precision, Mapping)
            or not isinstance(precision.get("decimal_digits"), int)
            or "binary_bits" in precision
        ):
            problems.append("numerical-multiprecision claims require decimal_digits")
    if provenance == "verified" and method not in {"exact-algebraic", "interval-certified"}:
        problems.append(
            "verified coordinate_provenance requires an exact or interval-certified method"
        )
    if method == "exact-algebraic" and scalar_kind == "decimal":
        problems.append("exact-algebraic claims require rational or algebraic scalar data")
    if provenance == "verified" and not isinstance(witness.get("certificate"), Mapping):
        problems.append("verified claims require a replayable certificate record")
    if (
        scalar_kind in {"rational", "algebraic-number-field"}
        and representation == "center-angle"
    ):
        problems.append("exact scalar input must use corners or center-basis, not an angle")
    return problems


def _fraction(value: Any) -> Fraction:
    if not isinstance(value, str):
        raise WitnessError("malformed-scalar", "rational literals must be strings")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise WitnessError("malformed-scalar", f"invalid rational literal {value!r}") from error


def _field_scalar(value: Any, field: NumberField) -> FieldElement:
    if isinstance(value, str):
        return field.rational(_fraction(value))
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return field.element([_fraction(item) for item in value])
    raise WitnessError(
        "malformed-scalar",
        "algebraic literals must be rational strings or coefficient-string arrays",
    )


def _square_from_pose(center: Point, cosine: Scalar, sine: Scalar) -> Square:
    half = cosine * 0 + Fraction(1, 2) if isinstance(cosine, Fraction) else cosine * 0 + 0.5
    # Field elements do not accept float coercion; replace the generic half there.
    if isinstance(cosine, FieldElement):
        half = cosine.field.rational(Fraction(1, 2))
    ux, uy = cosine * half, sine * half
    vx, vy = -sine * half, cosine * half
    cx, cy = center
    return [
        (cx - ux - vx, cy - uy - vy),
        (cx + ux - vx, cy + uy - vy),
        (cx + ux + vx, cy + uy + vy),
        (cx - ux + vx, cy - uy + vy),
    ]


def _materialize(
    witness: Mapping[str, Any],
    parse: Callable[[Any], Scalar],
    angle_basis: Callable[[Any, str], tuple[Scalar, Scalar]] | None = None,
) -> tuple[list[Square], Scalar]:
    side = parse(witness["side"])
    representation = witness["representation"]
    angle_unit = witness["coordinates"]["angle_unit"]
    squares: list[Square] = []
    for square in witness["squares"]:
        if representation == "corners":
            corners = [(parse(point[0]), parse(point[1])) for point in square["corners"]]
        else:
            center = (parse(square["center"][0]), parse(square["center"][1]))
            if representation == "center-angle":
                if angle_basis is None:
                    raise WitnessError(
                        "unsupported-representation", "angle evaluation is unavailable"
                    )
                cosine, sine = angle_basis(square["angle"], angle_unit)
            else:
                cosine, sine = parse(square["basis"][0]), parse(square["basis"][1])
            corners = _square_from_pose(center, cosine, sine)
        squares.append(corners)
    if witness["coordinates"]["origin"] == "container-center":
        half_side = side / 2
        squares = [[(x + half_side, y + half_side) for x, y in square] for square in squares]
    return squares, side


def _mp_materialize(witness: Mapping[str, Any], digits: int) -> tuple[list[Square], Any]:
    mp.mp.dps = digits

    def parse(value: Any) -> Any:
        if not isinstance(value, str):
            raise WitnessError("malformed-scalar", "decimal literals must be strings")
        try:
            return mp.mpf(value)
        except ValueError:
            rational = _fraction(value)
            return mp.mpf(rational.numerator) / rational.denominator

    def basis(value: Any, unit: str) -> tuple[Any, Any]:
        angle = parse(value)
        radians = angle * mp.pi / 180 if unit == "degrees" else angle
        return mp.cos(radians), mp.sin(radians)

    squares, side = _materialize(witness, parse, basis)
    return squares, side


def _mp_fraction(value: Fraction) -> Any:
    return mp.mpf(value.numerator) / value.denominator


def _field_value_to_mp(value: FieldElement, root: Any) -> Any:
    result = mp.mpf("0")
    for coefficient in reversed(value.coeffs):
        result = result * root + _mp_fraction(coefficient)
    return result


def _approximate_materialize(
    witness: Mapping[str, Any], digits: int
) -> tuple[list[Square], Any]:
    """Materialize every supported scalar kind for inspection or numerical checking."""
    if witness["scalar"]["kind"] != "algebraic-number-field":
        return _mp_materialize(witness, digits)

    mp.mp.dps = digits
    squares, side, field = _exact_materialize(witness)
    if field is None:  # Defensive: the scalar-kind branch above requires a field.
        raise WitnessError("internal-error", "algebraic materialization produced no field")
    field.refine_to(digits + 5)
    lo, hi = field.root_bounds()
    root = (_mp_fraction(lo) + _mp_fraction(hi)) / 2

    def approximate(value: Scalar) -> Any:
        if isinstance(value, FieldElement):
            return _field_value_to_mp(value, root)
        if isinstance(value, Fraction):
            return _mp_fraction(value)
        raise WitnessError("internal-error", f"unsupported exact scalar {type(value).__name__}")

    return (
        [[(approximate(x), approximate(y)) for x, y in square] for square in squares],
        approximate(side),
    )


def _f64_materialize(witness: Mapping[str, Any]) -> tuple[list[Square], float]:
    def parse(value: Any) -> float:
        if not isinstance(value, str):
            raise WitnessError("malformed-scalar", "decimal literals must be strings")
        try:
            return float(value)
        except ValueError:
            return float(_fraction(value))

    def basis(value: Any, unit: str) -> tuple[float, float]:
        angle = parse(value)
        radians = math.radians(angle) if unit == "degrees" else angle
        return math.cos(radians), math.sin(radians)

    squares, side = _materialize(witness, parse, basis)
    return squares, side


def _exact_materialize(
    witness: Mapping[str, Any],
) -> tuple[list[Square], Scalar, NumberField | None]:
    scalar = witness["scalar"]
    if scalar["kind"] == "rational":
        squares, side = _materialize(witness, _fraction)
        return squares, side, None
    if scalar["kind"] != "algebraic-number-field":
        raise WitnessError(
            "formal-certificate-missing",
            "decimal geometry is numerical data; verify requires exact or interval evidence",
        )
    field = NumberField(
        [_fraction(value) for value in scalar["minimal_polynomial"]],
        tuple(_fraction(value) for value in scalar["isolating_interval"]),
    )
    squares, side = _materialize(witness, lambda value: _field_scalar(value, field))
    return squares, side, field


def _sign_with_tolerance(tolerance: Scalar) -> Callable[[Scalar], int]:
    def sign(value: Scalar) -> int:
        if value > tolerance:
            return 1
        if value < -tolerance:
            return -1
        return 0

    return sign


def _margin_summary(
    squares: Sequence[Square], side: Scalar, sign: Callable[[Scalar], int]
) -> tuple[Scalar, Scalar]:
    containment = [
        clearance
        for square in squares
        for x, y in square
        for clearance in (x, y, side - x, side - y)
    ]
    pair_margins: list[Scalar] = []
    for left_index, left in enumerate(squares):
        for right in squares[left_index + 1 :]:
            gaps: list[Scalar] = []
            for axis in edge_axes(left) + edge_axes(right):
                left_lo, left_hi = project(left, axis, sign)
                right_lo, right_hi = project(right, axis, sign)
                gaps.extend((right_lo - left_hi, left_lo - right_hi))
            best_gap = gaps[0]
            for gap in gaps[1:]:
                if sign(gap - best_gap) > 0:
                    best_gap = gap
            pair_margins.append(best_gap)

    minimum_containment = containment[0]
    for clearance in containment[1:]:
        if sign(clearance - minimum_containment) < 0:
            minimum_containment = clearance
    minimum_pair_gap = side
    if pair_margins:
        minimum_pair_gap = pair_margins[0]
        for gap in pair_margins[1:]:
            if sign(gap - minimum_pair_gap) < 0:
                minimum_pair_gap = gap
    return minimum_containment, minimum_pair_gap


def _number(value: Scalar, digits: int = 40) -> str:
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, FieldElement):
        return value.field.decimal(value, digits)
    if isinstance(value, mp.mpf):
        return str(mp.nstr(value, digits))
    return repr(value)


def inspect_witness(witness: Mapping[str, Any], *, digits: int = 50) -> dict[str, Any]:
    """Summarize geometry without making or upgrading an assurance claim."""
    squares, side = _approximate_materialize(witness, digits)
    values = [(x, y) for square in squares for x, y in square]
    return {
        "operation": "inspect",
        "id": witness["id"],
        "n": witness["n"],
        "representation": witness["representation"],
        "scalar_kind": witness["scalar"]["kind"],
        "declared_side": _number(side),
        "bounding_box": {
            "min_x": _number(min(x for x, _ in values)),
            "max_x": _number(max(x for x, _ in values)),
            "min_y": _number(min(y for _, y in values)),
            "max_y": _number(max(y for _, y in values)),
        },
        "declared_coordinate_provenance": witness["claim"]["coordinate_provenance"],
        "assurance_conclusion": "none",
        "limitations": "Inspection renders and summarizes; it checks no packing claim.",
    }


def materialize_witness(
    witness: Mapping[str, Any], *, digits: int = 60
) -> tuple[list[Square], Scalar]:
    """Project a witness for inspection or rendering without upgrading its assurance.

    This is the public presentation boundary for callers that need geometry rather than
    the summary returned by :func:`inspect_witness`.  Formal callers must continue to
    use :func:`exact_verify`; a high-precision projection is still only a projection.
    """
    if digits < 1:
        raise WitnessError("malformed-option", "digits must be a positive integer")
    return _approximate_materialize(witness, digits)


def numerical_check(
    witness: Mapping[str, Any], *, method: str, precision: int, tolerance: str
) -> tuple[dict[str, Any], Report]:
    """Recompute feasibility numerically under an explicit finite arithmetic profile."""
    if precision < 1:
        raise WitnessError("malformed-option", "precision must be a positive integer")
    if method == "numerical-f64":
        if precision != 53:
            raise WitnessError(
                "malformed-option", "numerical-f64 has exactly 53 binary precision bits"
            )
        try:
            numeric_tolerance = float(tolerance)
        except ValueError as error:
            raise WitnessError("malformed-option", "tolerance must be numeric") from error
        if not math.isfinite(numeric_tolerance) or numeric_tolerance < 0:
            raise WitnessError("malformed-option", "tolerance must be finite and nonnegative")
        if witness["scalar"]["kind"] == "algebraic-number-field":
            approximate, approximate_side = _approximate_materialize(witness, 25)
            squares = [[(float(x), float(y)) for x, y in square] for square in approximate]
            side = float(approximate_side)
        else:
            squares, side = _f64_materialize(witness)
        numeric_tolerance = float(tolerance)
        precision_record = {"binary_bits": 53, "rounding": "nearest-even"}
    elif method == "numerical-multiprecision":
        try:
            numeric_tolerance = mp.mpf(tolerance)
        except ValueError as error:
            raise WitnessError("malformed-option", "tolerance must be numeric") from error
        if not mp.isfinite(numeric_tolerance) or numeric_tolerance < 0:
            raise WitnessError("malformed-option", "tolerance must be finite and nonnegative")
        squares, side = _approximate_materialize(witness, precision)
        precision_record = {"decimal_digits": precision, "rounding": "nearest"}
    else:
        raise WitnessError("unsupported-method", f"unknown numerical method {method!r}")
    sign = _sign_with_tolerance(numeric_tolerance)
    report = verify_packing(squares, side, sign=sign)
    containment, separation = _margin_summary(squares, side, sign)
    result = {
        "operation": "check",
        "id": witness["id"],
        "coordinate_provenance": "numerically-checked",
        "method": method,
        "precision": precision_record,
        "tolerance": tolerance,
        "check_passed": report.valid,
        "n": report.n,
        "pairs_tested": report.pairs_tested,
        "minimum_containment_clearance": _number(containment),
        "minimum_best_pair_gap": _number(separation),
        "failures": report.failures,
        "limitations": (
            "Finite-precision evidence only. A small tolerance, including 1e-100, "
            "does not establish exact feasibility or optimality."
        ),
    }
    return result, report


def exact_verify(witness: Mapping[str, Any]) -> tuple[dict[str, Any], Report]:
    """Verify a rational or certified algebraic witness with exact predicates."""
    if witness["claim"]["method"] == "interval-certified":
        raise WitnessError(
            "checker-not-built",
            "Witness/v1 can describe interval evidence, but the generic interval "
            "certificate checker is not built",
        )
    squares, side, field = _exact_materialize(witness)
    if field is None:
        sign: Callable[[Scalar], int] = _rational_sign
        field_certificate = {"field": "Q", "preconditions": "degree-one rational field"}
    else:
        sign = exact_sign
        field_certificate = field.precondition_certificate()
    report = verify_packing(squares, side, sign=sign)
    containment, separation = _margin_summary(squares, side, sign)
    result = {
        "operation": "verify",
        "id": witness["id"],
        "coordinate_provenance": "verified" if report.valid else "not-established",
        "method": "exact-algebraic",
        "verification_passed": report.valid,
        "n": report.n,
        "side": _number(side),
        "pairs_tested": report.pairs_tested,
        "minimum_containment_clearance": _number(containment),
        "minimum_best_pair_gap": _number(separation),
        "field_certificate": field_certificate,
        "failures": report.failures,
        "limitations": (
            "Verifies witness feasibility and its upper bound, not global optimality."
        ),
    }
    return result, report


def render_svg(witness: Mapping[str, Any], path: Path, *, digits: int = 60) -> None:
    """Render a simple source-independent SVG inspection view."""
    squares, side = _approximate_materialize(witness, digits)
    side_text = mp.nstr(side, 30)
    polygons = []
    for index, square in enumerate(squares, start=1):
        points = " ".join(f"{mp.nstr(x, 20)},{mp.nstr(y, 20)}" for x, y in square)
        polygons.append(
            f'  <polygon points="{points}" fill="#78a9ff88" stroke="#14213d" '
            f'stroke-width="0.01"><title>square {index}</title></polygon>'
        )
    content = "\n".join(
        [
            (
                '<svg xmlns="http://www.w3.org/2000/svg" '
                f'viewBox="0 0 {side_text} {side_text}" role="img">'
            ),
            f"<title>{witness['id']}: {witness['n']} unit squares</title>",
            (
                f'<rect x="0" y="0" width="{side_text}" height="{side_text}" '
                'fill="white" stroke="#c1121f" stroke-width="0.02"/>'
            ),
            f'<g transform="translate(0 {side_text}) scale(1 -1)">',
            *polygons,
            "</g>",
            "</svg>",
            "",
        ]
    )
    with atomic_output_file(path) as temporary:
        temporary.write_text(content, encoding="utf-8")


def _rational_basis(angle_text: str, unit: str, digits: int) -> tuple[Fraction, Fraction]:
    mp.mp.dps = digits + 20
    angle = mp.mpf(angle_text)
    radians = angle * mp.pi / 180 if unit == "degrees" else angle
    tangent = mp.tan(radians / 2)
    t = Fraction(str(mp.nstr(tangent, digits)))
    denominator = 1 + t * t
    return (1 - t * t) / denominator, 2 * t / denominator


def _rational_decimal(value: str, digits: int) -> Fraction:
    """Round a decimal source literal to a declared number of significant digits."""
    mp.mp.dps = digits + 20
    return Fraction(str(mp.nstr(mp.mpf(value), digits)))


def _promoted_candidate(
    witness: Mapping[str, Any], *, rational_digits: int, dilation: Fraction
) -> tuple[list[Square], Fraction]:
    if witness["representation"] != "center-angle" or witness["scalar"]["kind"] != "decimal":
        raise WitnessError(
            "unsupported-promotion-input",
            "robust rational promotion currently accepts decimal center-angle witnesses",
        )
    centered = witness["coordinates"]["origin"] == "container-center"
    if centered:
        reference = Fraction(0)
    else:
        reference = _rational_decimal(witness["side"], rational_digits) / 2
    unit = witness["coordinates"]["angle_unit"]
    squares: list[Square] = []
    for square in witness["squares"]:
        center = (
            _rational_decimal(square["center"][0], rational_digits),
            _rational_decimal(square["center"][1], rational_digits),
        )
        scaled = (
            reference + dilation * (center[0] - reference),
            reference + dilation * (center[1] - reference),
        )
        cosine, sine = _rational_basis(square["angle"], unit, rational_digits)
        squares.append(_square_from_pose(scaled, cosine, sine))
    values = [(x, y) for square in squares for x, y in square]
    min_x, min_y = min(x for x, _ in values), min(y for _, y in values)
    translated = [[(x - min_x, y - min_y) for x, y in square] for square in squares]
    translated_values = [(x, y) for square in translated for x, y in square]
    exact_side = max(coordinate for point in translated_values for coordinate in point)
    return translated, exact_side


def _literal(value: Fraction) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def _rational_sign(value: Fraction) -> int:
    return (value > 0) - (value < 0)


def promote_rational(
    witness: Mapping[str, Any],
    *,
    rational_digits: int,
    max_side_increase: str,
    source_path: str,
    replay_path: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Try exact rational robustification and return a certificate or a typed failure."""
    if rational_digits < 2:
        raise WitnessError("malformed-option", "rational-digits must be at least 2")
    original_side = _fraction(witness["side"])
    allowed = _fraction(max_side_increase)
    if allowed < 0:
        raise WitnessError("malformed-option", "max-side-increase must be nonnegative")
    exponents = list(range(max(2, rational_digits - 5), 1, -2))
    dilations = [Fraction(1), *(Fraction(1) + Fraction(1, 10**power) for power in exponents)]
    last_reason = "no candidate attempted"
    for dilation in dilations:
        squares, side = _promoted_candidate(
            witness, rational_digits=rational_digits, dilation=dilation
        )
        if side > original_side + allowed:
            last_reason = f"candidate side {_literal(side)} exceeds the allowed relaxation"
            continue
        report = verify_packing(squares, side, sign=_rational_sign)
        if not report.valid:
            last_reason = str(report.failures[:3])
            continue
        source: dict[str, str] = {"path": source_path}
        retained_source = witness.get("source") or {}
        for field in ("key", "url", "retrieved"):
            value = retained_source.get(field)
            if isinstance(value, str) and value:
                source[field] = value
        promoted = {
            "id": f"{witness['id']}-rational",
            "n": witness["n"],
            "side": _literal(side),
            "square_size": "1",
            "representation": "corners",
            "scalar": {"kind": "rational"},
            "coordinates": {
                "origin": "lower-left",
                "axes": "x-right-y-up",
                "angle_unit": "not-applicable",
            },
            "squares": [
                {
                    "id": original["id"],
                    "corners": [[_literal(x), _literal(y)] for x, y in square],
                }
                for original, square in zip(witness["squares"], squares, strict=True)
            ],
            "claim": {
                "coordinate_provenance": "verified",
                "method": "exact-algebraic",
                "limitations": (
                    "Exact feasible upper-bound witness derived by rational robustification; "
                    "does not establish global optimality or certify the original decimal pose."
                ),
            },
            "source": source,
            "certificate": {
                "kind": "exact-rational-sat",
                "derived_from": witness["id"],
                "rational_digits": rational_digits,
                "center_dilation": _literal(dilation),
                "pairs_tested": report.pairs_tested,
                "replay": (
                    f"uv run --frozen packing-witness verify {shlex.quote(replay_path)}"
                ),
            },
        }
        result = {
            "operation": "promote",
            "status": "certificate-produced",
            "coordinate_provenance": "verified",
            "method": "exact-algebraic",
            "source_witness": witness["id"],
            "promoted_witness": promoted["id"],
            "side": _literal(side),
            "side_decimal": f"{float(side):.16g}",
            "side_increase": _literal(side - original_side),
            "center_dilation": _literal(dilation),
            "pairs_tested": report.pairs_tested,
            "limitations": promoted["claim"]["limitations"],
        }
        return result, promoted
    raise WitnessError(
        "robustification-failed",
        (
            "no exact rational candidate passed within side increase "
            f"{max_side_increase}: {last_reason}"
        ),
    )


def witness_document(witness: Mapping[str, Any], *, schema: str = "witness.schema.yaml") -> str:
    """Serialize one generated witness with its enforced soft-schema envelope."""
    if not schema.strip():
        raise WitnessError("malformed-option", "schema path must be non-empty")
    document = {
        "softschema": {
            "contract": "packing.squares:Witness/v1",
            "schema": schema,
            "envelope": "witness",
            "status": "enforced",
        },
        "witness": deepcopy(dict(witness)),
    }
    return yaml.safe_dump(document, sort_keys=False, width=100, allow_unicode=True)


def result_json(result: Mapping[str, Any]) -> str:
    """Stable JSON for machine-facing command output."""
    return json.dumps(result, indent=2, sort_keys=True, default=str)


def report_dict(report: Report) -> dict[str, Any]:
    """Expose a report without leaking dataclass implementation details."""
    return asdict(report)
