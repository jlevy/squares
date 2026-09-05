"""Deterministic intake for hash-bound source-serialization declarations.

The module consumes structured provenance and synthetic scalar tokens only. It has no
packing, witness, SVG, geometry, or network dependency.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass, is_dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Literal

E1_REASONS = (
    "source-unavailable",
    "source-hash-or-version-unbound",
    "attribution-unbound",
    "units-frame-or-rotation-undefined",
    "scalar-class-uncovered",
    "serialization-rule-undefined",
    "precision-or-error-bound-undefined",
    "cell-empty-or-nondeterministic",
    "retention-boundary-violated",
)
RESOURCE_ROLES = ("catalogue", "source_svg")
ATTRIBUTION_ROLES = (
    "packing_finder",
    "later_optimizer",
    "source_author",
    "file_publisher",
    "compilation_basis",
)
SCALAR_CLASSES = ("center_x", "center_y", "rotation")
SEMANTICS_KINDS = ("exact", "nearest", "truncate", "interval")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")

type E1Reason = Literal[
    "source-unavailable",
    "source-hash-or-version-unbound",
    "attribution-unbound",
    "units-frame-or-rotation-undefined",
    "scalar-class-uncovered",
    "serialization-rule-undefined",
    "precision-or-error-bound-undefined",
    "cell-empty-or-nondeterministic",
    "retention-boundary-violated",
]


@dataclass(frozen=True, slots=True)
class SourceCell:
    """One deterministic closed cell derived from a declared scalar rule."""

    token_id: str
    scalar_class: str
    lower: str
    upper: str


@dataclass(frozen=True, slots=True)
class IntakeDecision:
    """A successful cell manifest or the first ordered E1 refusal."""

    accepted: bool
    reason: E1Reason | None
    cells: tuple[SourceCell, ...]


def canonical_json(value: object) -> str:
    """Serialize intake data without ambient ordering or whitespace choices."""

    def jsonable(item: object) -> object:
        if is_dataclass(item) and not isinstance(item, type):
            return jsonable(asdict(item))
        if isinstance(item, dict):
            return {key: jsonable(entry) for key, entry in item.items()}
        if isinstance(item, list | tuple):
            return [jsonable(entry) for entry in item]
        return item

    return json.dumps(jsonable(value), sort_keys=True, separators=(",", ":"))


def canonical_sha256(value: object) -> str:
    """Hash the canonical serialization of structured intake data."""

    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def load_receipt(path: Path) -> dict[str, Any]:
    """Load a structured receipt; Markdown and source artifacts are not accepted."""

    if path.suffix != ".json":
        raise ValueError("source-semantics receipts must be JSON")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("source-semantics receipt must be an object")
    return value


def _refuse(reason: E1Reason) -> IntakeDecision:
    return IntakeDecision(accepted=False, reason=reason, cells=())


def _objects(value: object) -> list[dict[str, Any]] | None:
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        return None
    return value


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value)


def _fraction(value: object) -> Fraction | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError):
        return None


def _fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def _resource_map(receipt: dict[str, Any]) -> dict[str, dict[str, Any]] | None:
    resources = _objects(receipt.get("resources"))
    if resources is None or len(resources) != len(RESOURCE_ROLES):
        return None
    mapped: dict[str, dict[str, Any]] = {}
    for item in resources:
        role = item.get("role")
        if not isinstance(role, str):
            return None
        mapped[role] = item
    if set(mapped) != set(RESOURCE_ROLES):
        return None
    return mapped


def _attribution_bound(  # noqa: PLR0911 - returns preserve the frozen reason order.
    receipt: dict[str, Any], resources: dict[str, dict[str, Any]]
) -> bool:
    artifact_hash = receipt.get("attribution_artifact_sha256")
    if not isinstance(artifact_hash, str) or _SHA256.fullmatch(artifact_hash) is None:
        return False
    if artifact_hash not in {item.get("sha256") for item in resources.values()}:
        return False
    role_map = receipt.get("role_map")
    if not isinstance(role_map, dict) or set(role_map) != set(ATTRIBUTION_ROLES):
        return False
    for role in ATTRIBUTION_ROLES:
        binding = role_map[role]
        if not isinstance(binding, dict) or set(binding) != {"name", "evidence_resource"}:
            return False
        if not _nonempty(binding["name"]):
            return False
        resource_role = binding["evidence_resource"]
        if resource_role not in resources:
            return False
        if resources[resource_role].get("sha256") != artifact_hash:
            return False
    return True


def _cells(
    inventory: list[dict[str, Any]], declarations: dict[str, dict[str, Any]]
) -> tuple[SourceCell, ...] | None:
    cells: list[SourceCell] = []
    for token in inventory:
        token_id = token["token_id"]
        scalar_class = token["scalar_class"]
        serialized = _fraction(token["serialized_value"])
        if serialized is None:
            return None
        declaration = declarations[token_id]
        kind = declaration["kind"]
        precision = declaration.get("precision_digits")
        lower_text = declaration.get("lower")
        upper_text = declaration.get("upper")
        if kind == "exact":
            lower = upper = serialized
        elif kind in {"nearest", "truncate"}:
            if not isinstance(precision, int) or isinstance(precision, bool) or precision < 0:
                return None
            unit = Fraction(1, 10**precision)
            if kind == "nearest":
                lower, upper = serialized - unit / 2, serialized + unit / 2
            elif serialized >= 0:
                lower, upper = serialized, serialized + unit
            else:
                lower, upper = serialized - unit, serialized
        else:
            lower = _fraction(lower_text)
            upper = _fraction(upper_text)
            if lower is None or upper is None or lower > upper:
                return None
        cells.append(
            SourceCell(
                token_id=token_id,
                scalar_class=scalar_class,
                lower=_fraction_text(lower),
                upper=_fraction_text(upper),
            )
        )
    return tuple(cells)


def evaluate_receipt(  # noqa: PLR0911 - the ordered returns are the E1 contract.
    receipt: dict[str, Any],
) -> IntakeDecision:
    """Return complete deterministic cells or the first reason in ``E1_REASONS``."""

    resources = _resource_map(receipt)
    if resources is None or any(
        item.get("available") is not True or item.get("http_status") != 200
        for item in resources.values()
    ):
        return _refuse("source-unavailable")

    for item in resources.values():
        digest = item.get("sha256")
        version_bound = _nonempty(item.get("etag")) or _nonempty(
            item.get("last_modified")
        )
        if (
            not isinstance(digest, str)
            or _SHA256.fullmatch(digest) is None
            or not version_bound
        ):
            return _refuse("source-hash-or-version-unbound")

    if not _attribution_bound(receipt, resources):
        return _refuse("attribution-unbound")

    context = receipt.get("semantics_context")
    context_fields = {
        "coordinate_units",
        "coordinate_frame",
        "rotation_convention",
        "exporter_version",
    }
    if not isinstance(context, dict) or set(context) != context_fields:
        return _refuse("units-frame-or-rotation-undefined")
    if any(not _nonempty(context[field]) for field in context_fields):
        return _refuse("units-frame-or-rotation-undefined")

    inventory = _objects(receipt.get("token_inventory"))
    declarations_list = _objects(receipt.get("declarations"))
    if inventory is None or declarations_list is None or not inventory:
        return _refuse("scalar-class-uncovered")
    token_ids: list[str] = []
    for token in inventory:
        if set(token) != {"token_id", "scalar_class", "serialized_value"}:
            return _refuse("scalar-class-uncovered")
        if not _nonempty(token["token_id"]) or token["scalar_class"] not in SCALAR_CLASSES:
            return _refuse("scalar-class-uncovered")
        token_ids.append(token["token_id"])
    declaration_ids: list[str] = []
    for declaration in declarations_list:
        token_id = declaration.get("token_id")
        if not isinstance(token_id, str):
            return _refuse("scalar-class-uncovered")
        declaration_ids.append(token_id)
    if len(set(token_ids)) != len(token_ids) or sorted(declaration_ids) != sorted(token_ids):
        return _refuse("scalar-class-uncovered")
    declarations = {item["token_id"]: item for item in declarations_list}

    declaration_fields = {"token_id", "kind", "precision_digits", "lower", "upper"}
    for declaration in declarations.values():
        if set(declaration) != declaration_fields or declaration["kind"] not in SEMANTICS_KINDS:
            return _refuse("serialization-rule-undefined")
        kind = declaration["kind"]
        if kind == "exact" and any(
            declaration[field] is not None for field in ("precision_digits", "lower", "upper")
        ):
            return _refuse("serialization-rule-undefined")
        if kind in {"nearest", "truncate"} and any(
            declaration[field] is not None for field in ("lower", "upper")
        ):
            return _refuse("serialization-rule-undefined")
        if kind == "interval" and declaration["precision_digits"] is not None:
            return _refuse("serialization-rule-undefined")

    for declaration in declarations.values():
        if declaration["kind"] in {"nearest", "truncate"}:
            precision = declaration["precision_digits"]
            if not isinstance(precision, int) or isinstance(precision, bool) or precision < 0:
                return _refuse("precision-or-error-bound-undefined")
        if declaration["kind"] == "interval" and (
            declaration["lower"] is None or declaration["upper"] is None
        ):
            return _refuse("precision-or-error-bound-undefined")

    cells = _cells(inventory, declarations)
    replayed_cells = _cells(inventory, declarations)
    if (
        cells is None
        or replayed_cells is None
        or canonical_json(cells) != canonical_json(replayed_cells)
    ):
        return _refuse("cell-empty-or-nondeterministic")

    retention = receipt.get("retention")
    if (
        not isinstance(retention, dict)
        or retention.get("policy") != "metadata-and-derived-numerical-facts-only"
        or retention.get("raw_asset_retained") is not False
        or retention.get("license_status") != "no-express-reuse-terms-found"
    ):
        return _refuse("retention-boundary-violated")

    return IntakeDecision(accepted=True, reason=None, cells=cells)


def main(argv: list[str] | None = None) -> int:
    """Enter the separately bound exp-050 runner through the preregistered module."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path, required=True)
    arguments = parser.parse_args(argv)

    from cases.n050_exact.source_semantics_runner import run_exp050  # noqa: PLC0415

    run_exp050(arguments.record)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
