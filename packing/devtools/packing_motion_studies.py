"""Source-bound motion scenes for the interactive square-packing lab.

The publication renderer deliberately accepts a smaller, script-free SVG profile.
This module is the adapter between retained research results and an interactive HTML
consumer; it does not change that renderer contract and it does not prove new geometry.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from cases.n5 import equal_side_face as face
from cases.n5 import rotating_release_paths as release
from cases.n5 import second_order_obstruction, tangent_cones
from sqpack.field import FieldElement, NumberField
from sqpack.render.style import PAPER_THEME, color_for_square
from sqpack.verify import exact_sign, verify_packing

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "campaign/series/series-000-smoke-and-calibration/results"
EXP035 = RESULTS / "exp-035-h-023-n5-tangent-cones.json"
EXP036 = RESULTS / "exp-036-h-023-n5-second-order-obstruction.json"
EXP042 = RESULTS / "exp-042-h-023-n5-endpoint-aware-rotating-paths.json"
CONTRACT = "packing.squares:MotionLab/v1"
SCHEMA_VERSION = 1
PROJECTION_DIGITS = 20
CONTACTS = {
    "base": ((0, 4), (1, 4), (2, 4), (3, 4)),
    "open_interval": ((0, 4), (2, 4), (3, 4)),
    "endpoint": ((0, 3), (0, 4), (2, 4), (3, 4)),
}


@dataclass(frozen=True)
class ProjectedPose:
    """One display-only pose evaluated from a motion scene."""

    square_id: int
    centre_x: float
    centre_y: float
    angle_radians: float


def _load_record(path: Path, contract: str) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("contract") != contract:
        raise ValueError(f"retained motion source has the wrong contract: {path}")
    if value.get("schema_version") != 1:
        raise ValueError(f"retained motion source has the wrong schema version: {path}")
    return cast(dict[str, object], value)


def _require_mapping(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be an object")
    return cast(dict[str, object], value)


def _physical_pairs_from_owner_axes(value: object, label: str) -> tuple[tuple[int, int], ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise TypeError(f"{label} must be a list of owner-axis labels")
    pairs: set[tuple[int, int]] = set()
    for item in value:
        pair_text = item.split(":", 1)[0]
        try:
            first_text, second_text = pair_text.split("-", 1)
            pair = (int(first_text), int(second_text))
        except ValueError as error:
            raise ValueError(
                f"{label} contains a malformed owner-axis label: {item}"
            ) from error
        pairs.add(pair)
    return tuple(sorted(pairs))


def _validate_contact_inventory(feasibility: dict[str, object]) -> None:
    cases = feasibility.get("cases")
    if not isinstance(cases, list) or len(cases) != 6:
        raise ValueError("exp-042 feasibility certificate lacks its six cases")
    source_keys = {
        "base": "exact_base_zero_axes",
        "open_interval": "exact_pathwise_zero_axes",
        "endpoint": "exact_endpoint_zero_axes",
    }
    for index, value in enumerate(cases):
        case = _require_mapping(value, f"exp-042 case {index}")
        axes = _require_mapping(case.get("zero_axis_exhaustion"), "zero-axis exhaustion")
        for state, source_key in source_keys.items():
            pairs = _physical_pairs_from_owner_axes(
                axes.get(source_key),
                f"exp-042 {case.get('class')} {case.get('stratum')} {state}",
            )
            if pairs != CONTACTS[state]:
                raise ValueError(
                    f"exp-042 {case.get('class')} {case.get('stratum')} {state} "
                    "physical contact inventory drifted"
                )


def _validate_sources() -> tuple[dict[str, object], dict[str, object]]:
    exp042 = _load_record(EXP042, "packing.squares:N5RotatingReleasePaths/v1")
    determinations = _require_mapping(exp042.get("determinations"), "exp-042 determinations")
    for name in ("feasibility", "stress"):
        determination = _require_mapping(determinations.get(name), f"exp-042 {name}")
        if determination.get("outcome") != "criterion_met":
            raise ValueError(f"exp-042 {name} criterion is not retained as met")
    certificates = _require_mapping(exp042.get("certificates"), "exp-042 certificates")
    feasibility = _require_mapping(certificates.get("feasibility"), "exp-042 feasibility")
    if feasibility.get("case_count") != 6 or feasibility.get("criterion_met") is not True:
        raise ValueError("exp-042 does not retain all six certified release paths")
    field = face.make_field()
    regenerated_feasibility = release.feasibility_core(field, release.ProofInputs())
    if feasibility != regenerated_feasibility:
        raise ValueError("exp-042 feasibility certificate differs from exact regeneration")
    _validate_contact_inventory(feasibility)

    exp035 = _load_record(EXP035, "packing.squares:N5TangentCones/v1")
    if exp035 != tangent_cones.build_result():
        raise ValueError("exp-035 tangent directions differ from exact regeneration")

    exp036 = _load_record(EXP036, "packing.squares:N5SecondOrderObstruction/v1")
    determination = _require_mapping(exp036.get("determination"), "exp-036 determination")
    if determination.get("outcome") != "criterion_met":
        raise ValueError("exp-036 obstruction criterion is not retained as met")
    if exp036 != second_order_obstruction.build_result():
        raise ValueError("exp-036 obstruction result differs from exact regeneration")
    return exp042, exp036


def _exact_scalar(field: NumberField, value: FieldElement) -> dict[str, object]:
    return {
        "coefficients_low_degree_first": [str(coefficient) for coefficient in value.coeffs],
        "decimal": field.decimal(value, PROJECTION_DIGITS),
    }


def _exact_point(
    field: NumberField, point: tuple[FieldElement, FieldElement]
) -> dict[str, object]:
    return {"x": _exact_scalar(field, point[0]), "y": _exact_scalar(field, point[1])}


def _fixed_orientation(square_id: int) -> dict[str, object]:
    if square_id < 3:
        return {"kind": "fixed", "radians": "0", "source": "0"}
    return {
        "kind": "fixed",
        "radians": format(math.pi / 4, ".20g"),
        "source": "pi/4",
    }


def _release_squares(
    field: NumberField,
    centres: list[tuple[FieldElement, FieldElement]],
    direction: list[FieldElement],
    sigma: int,
) -> list[dict[str, object]]:
    squares: list[dict[str, object]] = []
    for square_id, centre in enumerate(centres):
        orientation = _fixed_orientation(square_id)
        angular_velocity = field.zero
        if square_id == 1:
            orientation = {
                "kind": "rational-half-angle",
                "sigma": sigma,
                "cosine": "(4-u^2)/(4+u^2)",
                "sine": f"{4 * sigma}u/(4+u^2)",
                "angle": "2*atan(sigma*u/2)",
            }
            angular_velocity = field.rational(sigma)
        squares.append(
            {
                "id": square_id,
                "stable_id": f"square-{square_id:02d}",
                "label": str(square_id),
                "fill": color_for_square(square_id),
                "centre_start": _exact_point(field, centre),
                "centre_derivative": _exact_point(
                    field,
                    (
                        direction[tangent_cones.x(square_id)],
                        direction[tangent_cones.y(square_id)],
                    ),
                ),
                "orientation": orientation,
                "angle_derivative_at_zero": _exact_scalar(field, angular_velocity),
            }
        )
    return squares


def _verify_release_samples(
    field: NumberField,
    stratum: str,
    direction: list[FieldElement],
    sigma: int,
    interval_end: FieldElement,
) -> None:
    side = cast(FieldElement, face.exact_data(field)["side"])
    for u in (field.zero, interval_end / 2, interval_end):
        centres = release.centres_at(field, stratum, direction, u)
        squares = release.rotating_squares(field, centres, sigma, u)
        report = verify_packing(squares, side, sign=exact_sign)
        if not report.valid:
            raise ValueError(f"generated {stratum} rotating-release sample is invalid")


def build_release_scene(class_name: str, stratum: str) -> dict[str, object]:
    """Build one analytic R4/R5 scene from exp-042's exact case functions."""
    signs = dict(release.SIGNS)
    if class_name not in signs:
        raise ValueError(f"unknown rotating-release class: {class_name}")
    if stratum not in release.STRATA:
        raise ValueError(f"unknown rotating-release stratum: {stratum}")
    field = face.make_field()
    inputs = release.ProofInputs()
    sigma = signs[class_name]
    direction = release.position_direction(field, stratum, inputs)
    start = tangent_cones.centres_for_stratum(field, stratum)
    data = face.exact_data(field)
    delta = cast(FieldElement, data["delta"])
    interval_end = delta / 2
    _verify_release_samples(field, stratum, direction, sigma, interval_end)
    return {
        "id": f"{class_name}:{stratum}",
        "mode": "certified-path",
        "class": class_name,
        "stratum": stratum,
        "sigma": sigma,
        "evidence": {
            "status": "exact-universal-feasible-path",
            "source_experiment": "exp-042",
            "source_record": str(EXP042.relative_to(ROOT)),
            "claim": (
                "Display projection of one exact full-interval R4/R5 path; "
                "it is not a global-optimality claim."
            ),
        },
        "parameter": {
            "name": "u",
            "lower": _exact_scalar(field, field.zero),
            "upper": _exact_scalar(field, interval_end),
            "meaning": "rational half-angle parameter, not physical time",
        },
        "container_side": _exact_scalar(field, cast(FieldElement, data["side"])),
        "squares": _release_squares(field, start, direction, sigma),
        "contacts": {name: [list(pair) for pair in pairs] for name, pairs in CONTACTS.items()},
        "formulas": {
            "centres": "c_i(u)=c_i(0)+u*d_i",
            "orientation": (
                "square 1: cos(theta)=(4-u^2)/(4+u^2), sin(theta)=4*sigma*u/(4+u^2)"
            ),
        },
    }


def _w_squares(
    field: NumberField,
    centres: list[tuple[FieldElement, FieldElement]],
    direction: list[FieldElement],
) -> list[dict[str, object]]:
    squares: list[dict[str, object]] = []
    for square_id, centre in enumerate(centres):
        squares.append(
            {
                "id": square_id,
                "stable_id": f"square-{square_id:02d}",
                "label": str(square_id),
                "fill": color_for_square(square_id),
                "centre_start": _exact_point(field, centre),
                "centre_derivative": _exact_point(
                    field,
                    (
                        direction[tangent_cones.x(square_id)],
                        direction[tangent_cones.y(square_id)],
                    ),
                ),
                "orientation": _fixed_orientation(square_id),
                "angle_derivative_at_zero": _exact_scalar(
                    field, direction[tangent_cones.theta(square_id)]
                ),
            }
        )
    return squares


def build_obstruction_scene(stratum: str) -> dict[str, object]:
    """Build the displayed +W tangent and exp-036 obstruction annotations."""
    if stratum not in release.STRATA:
        raise ValueError(f"unknown obstruction stratum: {stratum}")
    field = face.make_field()
    data = face.exact_data(field)
    delta = cast(FieldElement, data["delta"])
    interval_end = delta / 2
    centres = tangent_cones.centres_for_stratum(field, stratum)
    direction = tangent_cones.witness(field, stratum)
    certificate = second_order_obstruction.exact_certificate(field)
    constants = _require_mapping(
        certificate.get("constants_low_degree_first"), "exp-036 exact constants"
    )
    expected_owner4 = [str(value) for value in (field.alpha / 8).coeffs]
    expected_owner3 = [str(value) for value in (-field.rational(1) / 4).coeffs]
    if constants.get("owner4_excess_second_order") != expected_owner4:
        raise ValueError("exp-036 owner-4 coefficient drifted")
    if constants.get("owner3_gap_second_order") != expected_owner3:
        raise ValueError("exp-036 owner-3 coefficient drifted")
    return {
        "id": f"plus-W:{stratum}",
        "mode": "second-order-obstruction",
        "class": "+W",
        "stratum": stratum,
        "evidence": {
            "status": "branch-exhaustive-second-order-obstruction",
            "source_experiment": "exp-036",
            "source_record": str(EXP036.relative_to(ROOT)),
            "geometry_source_experiment": "exp-035",
            "geometry_source_record": str(EXP035.relative_to(ROOT)),
            "claim": (
                "The dashed pose is only the first-order +W extrapolation. "
                "The retained proof rules out every second-order repair for this direction."
            ),
        },
        "parameter": {
            "name": "t",
            "lower": _exact_scalar(field, field.zero),
            "upper": _exact_scalar(field, interval_end),
            "meaning": "display scale for a first-order ghost, not a feasible path interval",
        },
        "container_side": _exact_scalar(field, cast(FieldElement, data["side"])),
        "squares": _w_squares(field, centres, direction),
        "contacts": {
            "base": [list(pair) for pair in CONTACTS["base"]],
            "meaning": "base graph only; no feasible contact evolution is certified",
        },
        "branches": {
            "owner-4": {
                "label": "owner 4",
                "quantity": "required extra side",
                "coefficient": _exact_scalar(field, field.alpha / 8),
                "formula": "(sqrt(2)/8)t^2 + o(t^2)",
                "sign": "positive contradiction",
                "note": "Retained common-angle owner-4 contradiction.",
            },
            "owner-3": {
                "label": "owner 3",
                "quantity": "necessary upper-bound minus lower-bound residual",
                "coefficient": _exact_scalar(field, -field.rational(1) / 4),
                "formula": "common-angle: -(1/4)t^2 + o(t^2)",
                "sign": "negative contradiction",
                "note": (
                    "The full branch also subtracts margin*|theta_3-theta_4|; "
                    "the displayed +W ghost has theta_3=theta_4."
                ),
            },
        },
    }


def build_motion_lab_manifest() -> dict[str, object]:
    """Build every source-bound scene consumed by the standalone motion lab."""
    exp042, _exp036 = _validate_sources()
    scope = _require_mapping(exp042.get("scope_refusals"), "exp-042 scope refusals")
    scenes = [
        build_release_scene(class_name, stratum)
        for class_name, _sigma in release.SIGNS
        for stratum in release.STRATA
    ]
    scenes.extend(build_obstruction_scene(stratum) for stratum in release.STRATA)
    return {
        "contract": CONTRACT,
        "schema_version": SCHEMA_VERSION,
        "title": "n=5 square-packing motion lab",
        "default_scene": "R4:A",
        "field": {
            "name": "Q(sqrt(2))",
            "basis": ["1", "sqrt(2)"],
            "exact_encoding": "coefficients_low_degree_first",
        },
        "theme": {
            "background": PAPER_THEME.background,
            "ink": PAPER_THEME.ink,
            "container": PAPER_THEME.container,
            "contact": PAPER_THEME.contact,
        },
        "source_records": {
            "exp-035": str(EXP035.relative_to(ROOT)),
            "exp-036": str(EXP036.relative_to(ROOT)),
            "exp-042": str(EXP042.relative_to(ROOT)),
        },
        "scope_refusals": scope.get("refused_claims", []),
        "scenes": scenes,
    }


def _decimal_value(value: object) -> float:
    record = _require_mapping(value, "exact scalar")
    decimal_value = record.get("decimal")
    if not isinstance(decimal_value, str):
        raise TypeError("exact scalar decimal projection must be a string")
    return float(decimal_value)


def project_scene(scene: dict[str, object], progress: float) -> tuple[ProjectedPose, ...]:
    """Evaluate the same analytic display projection used by the browser lab."""
    if not 0 <= progress <= 1 or not math.isfinite(progress):
        raise ValueError("motion progress must be finite and lie in [0, 1]")
    parameter = _require_mapping(scene.get("parameter"), "scene parameter")
    u = progress * _decimal_value(parameter.get("upper"))
    mode = scene.get("mode")
    sigma = scene.get("sigma")
    squares = scene.get("squares")
    if not isinstance(squares, list):
        raise TypeError("scene squares must be a list")
    poses: list[ProjectedPose] = []
    for value in squares:
        square = _require_mapping(value, "scene square")
        centre = _require_mapping(square.get("centre_start"), "square centre")
        derivative = _require_mapping(
            square.get("centre_derivative"), "square centre derivative"
        )
        x = _decimal_value(centre.get("x")) + u * _decimal_value(derivative.get("x"))
        y = _decimal_value(centre.get("y")) + u * _decimal_value(derivative.get("y"))
        orientation = _require_mapping(square.get("orientation"), "square orientation")
        radians = float(cast(str, orientation.get("radians", "0")))
        angular_velocity = _decimal_value(square.get("angle_derivative_at_zero"))
        if mode == "certified-path" and orientation.get("kind") == "rational-half-angle":
            if not isinstance(sigma, int):
                raise TypeError("release scene sigma must be an integer")
            radians = 2 * math.atan(sigma * u / 2)
        elif mode == "second-order-obstruction":
            radians += angular_velocity * u
        square_id = square.get("id")
        if not isinstance(square_id, int):
            raise TypeError("square ID must be an integer")
        poses.append(ProjectedPose(square_id, x, y, radians))
    return tuple(poses)


def contact_state(scene: dict[str, object], progress: float) -> tuple[tuple[int, int], ...]:
    """Return the source-declared contact graph at one normalized parameter."""
    if not 0 <= progress <= 1 or not math.isfinite(progress):
        raise ValueError("motion progress must be finite and lie in [0, 1]")
    contacts = _require_mapping(scene.get("contacts"), "scene contacts")
    if scene.get("mode") == "second-order-obstruction" or progress == 0:
        key = "base"
    elif progress == 1:
        key = "endpoint"
    else:
        key = "open_interval"
    values = contacts.get(key)
    if not isinstance(values, list):
        raise TypeError(f"scene contact state is missing: {key}")
    result = []
    for value in values:
        if (
            not isinstance(value, list)
            or len(value) != 2
            or not all(isinstance(item, int) for item in value)
        ):
            raise TypeError("contact pair must contain two integer square IDs")
        result.append((value[0], value[1]))
    return tuple(result)
