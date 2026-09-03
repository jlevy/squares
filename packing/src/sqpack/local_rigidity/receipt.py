"""The replayable certificate: canonical bytes, one digest, and a readable rendering.

Two properties are load-bearing and both are deliberate.

**The payload never touches the field's refinement state.** `NumberField` narrows its
isolating interval lazily, so `FieldElement.decimal` returns more digits after some other
computation has refined the same field -- the shape of `D-359`. A receipt whose bytes
depend on what ran before it is not replayable, and would fail the normal-versus-optimized
comparison for a reason that has nothing to do with `-O`. So every number here is printed
from its exact power-basis coefficients, by `element_text` and `element_algebraic`, and
nothing calls `decimal`, `float`, or `root_approx`.

**The digest covers the payload, not the prose.** `digest` hashes the canonical JSON of
the exact record: margins, keys, counts, identities, binding scalars, control outcomes.
`controls.certificate_drift` mutates one margin in a copy of that payload and the digest
must move, which is what makes the receipt a certificate rather than a report.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from typing import Any

from sqpack.field import FieldElement
from sqpack.local_rigidity.instrument import Determination
from sqpack.local_rigidity.system import ConstraintSystem


def element_text(element: FieldElement) -> str:
    """Exact power-basis serialisation, independent of any interval refinement."""
    return element.text()


def _rational_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def element_algebraic(element: FieldElement, symbol: str = "sqrt(2)") -> str:
    """The same number written for a reader, still exactly and still deterministically."""
    parts: list[str] = []
    for power, coefficient in enumerate(element.coeffs):
        if coefficient == 0:
            continue
        if power == 0:
            parts.append(_rational_text(coefficient))
            continue
        basis = symbol if power == 1 else f"{symbol}^{power}"
        if coefficient == 1:
            parts.append(basis)
        elif coefficient == -1:
            parts.append(f"-{basis}")
        else:
            parts.append(f"{_rational_text(coefficient)}*{basis}")
    if not parts:
        return "0"
    rendered = parts[0]
    for part in parts[1:]:
        rendered += f" - {part[1:]}" if part.startswith("-") else f" + {part}"
    return rendered


def sign_word(element: FieldElement) -> str:
    sign = element.sign()
    return "zero" if sign == 0 else ("positive" if sign > 0 else "negative")


def build_payload(
    determination: Determination,
    system: ConstraintSystem,
    controls: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """The exact, canonical record of everything the instrument decided."""
    chart = system.chart
    return {
        "schema_version": 1,
        "subject": {
            "commitment": "BC-152",
            "hypothesis": "H-060",
            "pose": determination.pose_label,
            "side": element_algebraic(chart.pose.side),
            "side_exact": element_text(chart.pose.side),
            "field": chart.field.precondition_certificate(),
            "chart": determination.chart_name,
            "chart_variables": chart.variable_names(),
        },
        "chart_certificates": {
            "denominator_positivity": [
                {
                    "subject": witness.subject,
                    "margin": witness.margin,
                    "sum_of_squares_root": witness.square_root,
                    "verified": witness.verified,
                }
                for witness in chart.denominator_certificate()
            ],
            "orthogonality": [
                {"name": check.name, "statement": check.statement, "holds": check.holds}
                for check in chart.orthogonality_certificate()
            ],
            "unit_base_normals": [
                {"name": check.name, "statement": check.statement, "holds": check.holds}
                for check in chart.base_normal_certificate()
            ],
            "injectivity": [
                {"name": check.name, "statement": check.statement, "holds": check.holds}
                for check in chart.injectivity_certificate()
            ],
        },
        "counts": determination.counts,
        "enumeration_complete": determination.enumeration_complete,
        "expected_cardinality": system.book.expected_cardinality(),
        "actual_cardinality": system.book.actual_cardinality(),
        "walls": [
            {
                "key": constraint.key,
                "describe": constraint.describe(),
                "denominator": constraint.denominator,
                "margin": element_text(constraint.margin),
                "margin_algebraic": element_algebraic(constraint.margin),
                "sign": sign_word(constraint.margin),
                "degree": constraint.polynomial.degree(),
            }
            for constraint in system.walls
        ],
        "pairs": [
            {
                "key": report.key,
                "status": report.status,
                "active_branch": (
                    report.active_branch.key if report.active_branch else None
                ),
                "active_constraint": (
                    report.active_constraint.key if report.active_constraint else None
                ),
                "witness_branch": (
                    report.witness_branch.key if report.witness_branch else None
                ),
                "witness_margin": (
                    element_text(report.witness_margin) if report.witness_margin else None
                ),
                "branches": [
                    {
                        "key": branch.key,
                        "describe": branch.describe(),
                        "minimum_feature": branch.minimum().key,
                        "minimum_margin": element_text(branch.minimum().margin),
                        "minimum_sign": sign_word(branch.minimum().margin),
                        "support_features": [
                            {
                                "key": constraint.key,
                                "denominator": constraint.denominator,
                                "margin": element_text(constraint.margin),
                                "margin_algebraic": element_algebraic(constraint.margin),
                                "sign": sign_word(constraint.margin),
                                "degree": constraint.polynomial.degree(),
                            }
                            for constraint in branch.constraints
                        ],
                    }
                    for branch in report.branches
                ],
            }
            for report in system.pairs
        ],
        "active_system": list(determination.active_keys),
        "neighborhood": {
            "definition": (
                "U = {z : every condition below holds strictly}. Each condition is a "
                "polynomial in the chart variables, hence continuous, and each holds "
                "strictly at the pose, so U is open and contains it. No radius is claimed."
            ),
            "valid": determination.neighborhood_certified,
            "condition_count": len(determination.neighborhood.conditions),
            "conditions": [
                {
                    "key": condition.key,
                    "role": condition.role,
                    "sense": condition.sense,
                    "margin": element_text(condition.margin),
                    "margin_algebraic": element_algebraic(condition.margin),
                    "holds": condition.holds_at_base(),
                }
                for condition in determination.neighborhood.conditions
            ],
            "reduction": (
                "on U a configuration is feasible exactly when the active inequalities "
                "hold: inactive walls stay slack; each noncontact pair keeps a strictly "
                "separating branch; each touching pair has seven branches strictly "
                "refuted, so the separating-axis disjunction collapses to the eighth, "
                "whose three non-touching support features stay slack"
            ),
        },
        "t012_binding": (
            None
            if determination.binding is None
            else {
                "holds": determination.binding.holds,
                "transform": determination.binding.transform,
                "active_key_agreement": determination.binding.active_key_agreement,
                "missing_from_chart": list(determination.binding.missing_from_chart),
                "missing_from_t012": list(determination.binding.missing_from_t012),
                "chart_free_variables": list(determination.binding.chart_free_variables),
                "t012_free_variables": list(determination.binding.t012_free_variables),
                "free_variables_correspond": (
                    determination.binding.free_variables_correspond
                ),
                "directions": list(determination.binding.directions),
                "rows": [
                    {
                        "key": row.key,
                        "t012_index": row.t012_index,
                        "positive_row_scalar": row.scalar,
                        "scalar_is_positive": row.scalar_is_positive,
                        "denominator_at_base": row.denominator_at_base,
                        "gradient_matches": row.gradient_matches,
                        "second_jet_matches": dict(sorted(row.second_jet_matches.items())),
                    }
                    for row in determination.binding.rows
                ],
            }
        ),
        "probe": {
            "tested": determination.probe.tested,
            "witnesses": [
                {"variable": one.variable, "value": one.value}
                for one in determination.probe.witnesses
            ],
            "caveat": determination.probe.probe_is_not_a_proof,
        },
        "controls": controls or [],
        "determination": {
            "instrument_ready": determination.instrument_ready,
            "isolation_decided": determination.isolation_decided,
            "refusals": list(determination.refusals),
            "scope": determination.scope,
        },
    }


def canonical_bytes(payload: dict[str, Any]) -> bytes:
    """One byte sequence per payload: sorted keys, no incidental whitespace."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(payload: dict[str, Any]) -> str:
    """SHA-256 of the canonical bytes."""
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()
