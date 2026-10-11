"""Replayable container isometries for selected atlas arrangements.

Upstream facts and certificates retain their published coordinates. Atlas witnesses
record an isometry of those facts; exact views and motion certificates carry the
same map without changing a bound, evidence tier or scientific determination date.
"""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from decimal import Decimal, localcontext
from fractions import Fraction
from typing import Any, Literal

from sqpack.witness import numerical_check

REFLECTED_N = 211
PARENT_FACTS = "packing/resources/web/de-winter-square-packing-211-2026-09-16/facts/n-211.yaml"
PARENT_SOURCE_KEY = "[de Winter n211 2026-09-16]"
Reflection = Literal["reflect-x-axis", "reflect-y-axis"]
REGISTERED_OPERATION: Reflection = "reflect-y-axis"


def _negate(value: str) -> str:
    number = Decimal(str(value))
    if not number.is_finite():
        raise ValueError("reflection requires finite coordinates")
    return "0" if number == 0 else str(number.copy_negate())


def _difference(side: str, value: str, *, rational: bool) -> str:
    if rational:
        number = Fraction(side) - Fraction(value)
        return str(number.numerator) if number.denominator == 1 else str(number)
    bound, coordinate = Decimal(str(side)), Decimal(str(value))
    if not bound.is_finite() or not coordinate.is_finite():
        raise ValueError("reflection requires finite coordinates")
    # The sum can span both input coefficients and both decimal exponents. Reserve
    # that full range so a caller's context cannot round this exact subtraction.
    precision = (
        sum(
            len(number.as_tuple().digits) + abs(int(number.as_tuple().exponent))
            for number in (bound, coordinate)
        )
        + 4
    )
    with localcontext() as context:
        context.prec = max(precision, 28)
        result = bound - coordinate
    return "0" if result == 0 else str(result)


def _reflect(witness: Mapping[str, Any], operation: Reflection) -> dict[str, Any]:
    """Reflect about a container midline, preserving metadata and square identities.

    Center-angle poses negate their angle exactly, which preserves the principal
    orientation range used by n211. Rational corners reverse their winding after
    reflection so the unit-square verifier continues to see cyclic CCW vertices.
    Callers recheck the returned geometry before retaining a new certificate.
    """
    coordinates = witness["coordinates"]
    if coordinates.get("origin") != "lower-left" or coordinates.get("axes") != "x-right-y-up":
        raise ValueError("reflection requires lower-left coordinates with x-right-y-up axes")
    kind = witness["scalar"]["kind"]
    representation = witness["representation"]
    if kind not in {"decimal", "rational"} or representation not in {"center-angle", "corners"}:
        raise ValueError("reflection supports decimal center-angle or decimal/rational corners")
    if representation == "center-angle" and (
        kind != "decimal" or coordinates.get("angle_unit") not in {"radians", "degrees"}
    ):
        raise ValueError("center-angle reflection requires decimal degrees or radians")
    image = deepcopy(dict(witness))
    side = str(witness["side"])
    component = 1 if operation == "reflect-x-axis" else 0
    for square in image["squares"]:
        if representation == "center-angle":
            square["center"][component] = _difference(
                side, str(square["center"][component]), rational=False
            )
            square["angle"] = _negate(str(square["angle"]))
        else:
            square["corners"] = [
                [
                    _difference(side, str(value), rational=kind == "rational")
                    if index == component
                    else value
                    for index, value in enumerate(corner)
                ]
                for corner in reversed(square["corners"])
            ]
    return image


def reflect_x_axis(witness: Mapping[str, Any]) -> dict[str, Any]:
    """Decode the earlier vertical flip about the horizontal container midline."""
    return _reflect(witness, "reflect-x-axis")


def reflect_y_axis(witness: Mapping[str, Any]) -> dict[str, Any]:
    """Mirror left/right about the vertical container midline, retaining y."""
    return _reflect(witness, "reflect-y-axis")


def _registered_parent(witness: Mapping[str, Any]) -> None:
    """Refuse a source switch rather than attaching this packet's isometry lineage."""
    source = witness.get("source") or {}
    if source.get("key") != PARENT_SOURCE_KEY or source.get("path") not in {
        PARENT_FACTS,
        PARENT_FACTS.removeprefix("packing/"),
    }:
        raise ValueError("the registered atlas orientation requires its de Winter n211 parent")


def geometry_transform(witness: Mapping[str, Any]) -> dict[str, Any] | None:
    """The recorded atlas isometry, or no transform for an ordinary source pose."""
    transform = (witness.get("certificate") or {}).get("geometry_transform")
    if transform is None:
        return None
    if witness["n"] != REFLECTED_N or transform.get("operation") not in {
        "reflect-x-axis",
        "reflect-y-axis",
    }:
        raise ValueError("unrecognized atlas geometry transform")
    _registered_parent(witness)
    return dict(transform)


def _lineage(witness: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "kind": "container-isometry",
        "operation": REGISTERED_OPERATION,
        "map": {"x": "side - x", "y": "y", "angle": "-angle"},
        "orientation": "negated principal angle; signed zero normalized; CCW corners",
        "reference_n": 241,
        "recorded_at": "2026-10-08",
        "parent": {
            "path": PARENT_FACTS,
            "id": "W-de-winter-n211",
            "atlas_receipt_before_transform": deepcopy(
                (witness.get("certificate") or {}).get("result")
            ),
        },
        "claim": (
            "An isometry of the retained arrangement, preserving all packing bounds "
            "and scientific assurance."
        ),
    }


def orient_atlas_witness(witness: dict[str, Any]) -> dict[str, Any]:
    """Apply the registered atlas orientation and recheck its numerical receipt."""
    if witness["n"] != REFLECTED_N:
        return witness
    _registered_parent(witness)
    transform = geometry_transform(witness)
    if transform is not None and transform["operation"] == REGISTERED_OPERATION:
        return witness
    # An earlier atlas edition used a vertical flip. Recover its immutable parent
    # before applying the corrected horizontal mirror, rather than composing flips.
    witness = source_orientation(witness)
    image = reflect_y_axis(witness)
    claim = witness["claim"]
    if claim["method"] != "numerical-multiprecision":
        raise ValueError(
            "the registered atlas reflection requires its numerical source profile"
        )
    result, report = numerical_check(
        image,
        method=claim["method"],
        precision=claim["precision"]["decimal_digits"],
        tolerance=claim["tolerance"],
    )
    if not report.valid:
        raise ValueError(
            f"n={witness['n']}: reflected witness is infeasible: {report.failures[:1]}"
        )
    certificate = image.setdefault("certificate", {})
    certificate["result"] = result
    certificate["geometry_transform"] = _lineage(witness)
    return image


def source_orientation(witness: dict[str, Any]) -> dict[str, Any]:
    """Recover the published pose for deterministic derivation and motion ordering."""
    transform = geometry_transform(witness)
    if transform is None:
        return witness
    source = _reflect(witness, transform["operation"])
    transform = source["certificate"].pop("geometry_transform")
    receipt = transform["parent"].get("atlas_receipt_before_transform")
    if receipt is None:
        source["certificate"].pop("result", None)
    else:
        source["certificate"]["result"] = receipt
    return source


def orient_regularized_view(
    view: dict[str, Any], source: dict[str, Any], *, parent_certificate: str | None
) -> dict[str, Any]:
    """Map an exactly regularized source pose into its selected atlas orientation.

    The view's own exact side defines its midline. Its inherited regularization
    summary describes the parent derivation; the transform describes the next step.
    The retaining caller verifies these transformed rational corners independently.
    """
    transform = geometry_transform(source)
    if transform is None:
        return view
    image = _reflect(view, transform["operation"])
    lineage = deepcopy(transform)
    lineage["parent"]["regularization"] = "regularize_axis_components/2 in source orientation"
    lineage["parent"]["exact_certificate"] = parent_certificate
    image["certificate"]["geometry_transform"] = lineage
    return image


def reflect_escape_case(
    case: dict[str, Any], *, operation: Reflection = REGISTERED_OPERATION
) -> dict[str, Any]:
    """Reflect certified escape directions without reordering discoveries or counts."""
    image = deepcopy(case)
    component = "y" if operation == "reflect-x-axis" else "x"
    for motion in image["movable_squares"]:
        motion["direction"][component] = _negate(motion["direction"][component])
    return image
