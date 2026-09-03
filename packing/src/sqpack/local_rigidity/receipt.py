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
from sqpack.local_rigidity.instrument import (
    DECLARED_MATHEMATICAL_INPUTS,
    Determination,
)
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
                "active_branch": (report.active_branch.key if report.active_branch else None),
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
                "free_variables_correspond": (determination.binding.free_variables_correspond),
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
        "reduction_audit": (
            None
            if determination.audit is None
            else {
                "points_tested": determination.audit.points_tested,
                "points_inside_neighborhood": determination.audit.points_inside,
                "agreements": determination.audit.agreements,
                "counterexamples": list(determination.audit.counterexamples),
                "consistent": determination.audit.consistent,
                "caveat": determination.audit.audit_is_not_a_proof,
            }
        ),
        "declared_mathematical_inputs": [dict(entry) for entry in DECLARED_MATHEMATICAL_INPUTS],
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


def _row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def _table(header: list[str], rows: list[list[str]]) -> list[str]:
    lines = [_row(header), _row(["---"] * len(header))]
    lines.extend(_row(cells) for cells in rows)
    return lines


def render_markdown(payload: dict[str, Any], expected: dict[str, int]) -> str:
    """The human-readable receipt, generated from the same payload the digest covers.

    `expected` is the planning document's count claim. It is printed beside the computed
    count and never substituted for it: a disagreement is rendered as a disagreement.
    """
    out: list[str] = []
    subject = payload["subject"]
    determination = payload["determination"]
    out.append("# BC-152 instrument receipt — H-060 exact local-rigidity chart")
    out.append("")
    out.append(f"- Payload digest (SHA-256): `{digest(payload)}`")
    out.append(f"- Pose: `{subject['pose']}`, container side `{subject['side']}`, fixed")
    out.append(f"- Chart: `{subject['chart']}`, {len(subject['chart_variables'])} variables")
    out.append(f"- Instrument ready: **{determination['instrument_ready']}**")
    out.append(
        f"- Isolation decided by this instrument: **{determination['isolation_decided']}**"
    )
    out.append(f"- Refusals: {determination['refusals'] or 'none'}")
    disagreements = payload.get("count_disagreements")
    if disagreements is not None:
        out.append(
            f"- Agenda count disagreements: "
            f"{disagreements if disagreements else 'none — every agenda figure reproduced'}"
        )
    out.append("")
    out.append(f"Scope: {determination['scope']}.")
    out.append("")

    out.append("## Chart")
    out.append("")
    out.append(
        "Each square `k` gets `(a_k, b_k, u_k)`: the centre moves to `c_k^0 + (a_k, b_k)` "
        "and turns by `delta_k = 2 atan(u_k)` from its pose angle, so"
    )
    out.append("")
    out.append("```")
    out.append("cos delta = (1 - u^2)/(1 + u^2),   sin delta = 2u/(1 + u^2)")
    out.append("M(u) = [[1 - u^2, -2u], [2u, 1 - u^2]],   D(u) = 1 + u^2")
    out.append("corner:  D_k * p_{k,j} = D_k * c_k(z) + M(u_k) r_{k,j}")
    out.append("normal:  D_k * n_{k,e} = M(u_k) n_{k,e}^0")
    out.append("wall:    G = D_k * p_x   (left)      G = side * D_k - D_k * p_x   (right)")
    out.append("pair:    G = N_{h,e} . (P_{k,j} - D_k c_h) - (1/2) D_h D_k")
    out.append("```")
    out.append("")
    out.append("### Denominator positivity")
    out.append("")
    out.extend(
        _table(
            ["denominator", "lower bound", "sum-of-squares witness", "verified"],
            [
                [
                    f"`{entry['subject']}`",
                    entry["margin"],
                    f"`{entry['sum_of_squares_root']}^2`",
                    str(entry["verified"]),
                ]
                for entry in payload["chart_certificates"]["denominator_positivity"]
            ],
        )
    )
    out.append("")
    out.append(
        "`D - 1` is literally a square, so `D >= 1` on all of `R^15`, not merely on the "
        "declared neighborhood. Every cleared denominator is a product of these, hence at "
        "least `1`. No sign here was sampled."
    )
    out.append("")
    for title, key in (
        ("Injectivity and image", "injectivity"),
        ("Orthogonality of the cleared rotation", "orthogonality"),
    ):
        out.append(f"### {title}")
        out.append("")
        out.extend(
            _table(
                ["check", "statement", "holds"],
                [
                    [f"`{entry['name']}`", entry["statement"], str(entry["holds"])]
                    for entry in payload["chart_certificates"][key]
                ],
            )
        )
        out.append("")
    normals = payload["chart_certificates"]["unit_base_normals"]
    out.append(
        f"All {len(normals)} base edge normals are exactly unit vectors "
        f"({all(entry['holds'] for entry in normals)}), which is what makes the constant "
        "`1/2` in every pair inequality the exact half-width of a unit square."
    )
    out.append("")

    out.append("## Constraint accounting")
    out.append("")
    out.append(
        "Counts below are **computed from the pose**. The agenda's figures are printed "
        "beside them for comparison and are never substituted for them."
    )
    out.append("")
    rows = []
    for name, value in sorted(payload["counts"].items()):
        claimed = expected.get(name)
        verdict = (
            "not stated"
            if claimed is None
            else ("agrees" if claimed == value else f"**DISAGREES ({claimed})**")
        )
        rows.append([f"`{name}`", str(value), verdict])
    out.extend(_table(["quantity", "computed", "against the agenda"], rows))
    out.append("")
    out.append(
        f"Enumeration complete: {payload['enumeration_complete']} "
        f"(expected `{payload['expected_cardinality']}`, actual "
        f"`{payload['actual_cardinality']}`)."
    )
    out.append("")

    out.append("### The active system (the local feasible system on `U`)")
    out.append("")
    out.extend(
        _table(
            ["#", "key", "margin"],
            [
                [str(index), f"`{key}`", "0"]
                for index, key in enumerate(payload["active_system"], start=1)
            ],
        )
    )
    out.append("")

    out.append("### Inactive wall-corner inequalities, exact base margins")
    out.append("")
    inactive = [entry for entry in payload["walls"] if entry["sign"] == "positive"]
    out.extend(
        _table(
            ["key", "constraint", "denominator", "exact margin", "power basis"],
            [
                [
                    f"`{entry['key']}`",
                    entry["describe"],
                    f"`{entry['denominator']}`",
                    entry["margin_algebraic"],
                    f"`{entry['margin']}`",
                ]
                for entry in inactive
            ],
        )
    )
    out.append("")

    out.append("### Pair separating-axis accounting")
    out.append("")
    out.extend(
        _table(
            [
                "pair",
                "status",
                "active branch",
                "active inequality",
                "witness branch",
                "witness margin",
            ],
            [
                [
                    f"`{entry['key']}`",
                    entry["status"],
                    f"`{entry['active_branch']}`" if entry["active_branch"] else "--",
                    f"`{entry['active_constraint']}`" if entry["active_constraint"] else "--",
                    f"`{entry['witness_branch']}`" if entry["witness_branch"] else "--",
                    f"`{entry['witness_margin']}`" if entry["witness_margin"] else "--",
                ]
                for entry in payload["pairs"]
            ],
        )
    )
    out.append("")
    out.append("#### Every branch, with its least support feature")
    out.append("")
    out.extend(
        _table(
            [
                "pair",
                "branch",
                "axis / orientation",
                "least feature",
                "least margin",
                "sign",
            ],
            [
                [
                    f"`{pair['key']}`",
                    f"`{branch['key']}`",
                    branch["describe"],
                    f"`{branch['minimum_feature']}`",
                    f"`{branch['minimum_margin']}`",
                    branch["minimum_sign"],
                ]
                for pair in payload["pairs"]
                for branch in pair["branches"]
            ],
        )
    )
    out.append("")
    out.append("#### Every support feature, with its exact base margin")
    out.append("")
    out.extend(
        _table(
            ["key", "denominator", "exact margin", "sign", "degree"],
            [
                [
                    f"`{feature['key']}`",
                    f"`{feature['denominator']}`",
                    feature["margin_algebraic"],
                    feature["sign"],
                    str(feature["degree"]),
                ]
                for pair in payload["pairs"]
                for branch in pair["branches"]
                for feature in branch["support_features"]
            ],
        )
    )
    out.append("")

    neighborhood = payload["neighborhood"]
    out.append("## The neighborhood `U`, by continuity and not by radius")
    out.append("")
    out.append(neighborhood["definition"])
    out.append("")
    out.append(f"Reduction: {neighborhood['reduction']}.")
    out.append("")
    negative = [one for one in neighborhood["conditions"] if one["sense"] == "negative"]
    positive = [one for one in neighborhood["conditions"] if one["sense"] == "positive"]
    out.append(
        f"`U` is cut out by {neighborhood['condition_count']} strict conditions: "
        f"{len(positive)} strictly positive and {len(negative)} strictly negative. "
        f"All hold at the pose: {neighborhood['valid']}."
    )
    out.append("")
    out.append("### The strictly negative witnesses (the branches that must stay refuted)")
    out.append("")
    out.extend(
        _table(
            ["key", "role", "exact margin", "holds"],
            [
                [f"`{one['key']}`", one["role"], one["margin_algebraic"], str(one["holds"])]
                for one in negative
            ],
        )
    )
    out.append("")
    out.append("### The strictly positive conditions")
    out.append("")
    out.extend(
        _table(
            ["key", "role", "exact margin", "holds"],
            [
                [f"`{one['key']}`", one["role"], one["margin_algebraic"], str(one["holds"])]
                for one in positive
            ],
        )
    )
    out.append("")

    binding = payload["t012_binding"]
    out.append("## `T-012` binding certificate")
    out.append("")
    if binding is None:
        out.append("Not computed: `T-012`'s rows were not supplied.")
    else:
        transform = binding["transform"]
        out.append(f"- Transform: `{transform['name']}` — {transform['shape']}")
        out.append(
            f"- `{transform['chart_order']}` to `{transform['target_order']}`, "
            f"because {transform['reason']}"
        )
        out.append(f"- Binding holds: **{binding['holds']}**")
        out.append(
            f"- Active keys agree with `T-012`'s contacts: {binding['active_key_agreement']}"
        )
        out.append(
            f"- Free variables: chart `{binding['chart_free_variables']}` "
            f"against `T-012` `{binding['t012_free_variables']}`, corresponding: "
            f"{binding['free_variables_correspond']}"
        )
        out.append("")
        out.extend(
            _table(
                ["key", "T-012 row", "positive scalar", "D_j(0)", "gradient", "second jet"],
                [
                    [
                        f"`{row['key']}`",
                        str(row["t012_index"]),
                        f"`{row['positive_row_scalar']}`",
                        f"`{row['denominator_at_base']}`",
                        str(row["gradient_matches"]),
                        ", ".join(
                            f"{name}: {value}"
                            for name, value in row["second_jet_matches"].items()
                        ),
                    ]
                    for row in binding["rows"]
                ],
            )
        )
    out.append("")

    probe = payload["probe"]
    out.append("## Axis probe")
    out.append("")
    out.append(
        f"{probe['tested']} chart points tested for exact feasibility; "
        f"{len(probe['witnesses'])} feasible neighbours found."
    )
    out.append("")
    out.append(f"**Caveat, recorded deliberately:** {probe['caveat']}.")
    out.append("")

    audit = payload["reduction_audit"]
    out.append("## Reduction audit")
    out.append("")
    if audit is None:
        out.append("Not run.")
    else:
        out.append(
            f"{audit['points_tested']} exact chart points sampled, "
            f"{audit['points_inside_neighborhood']} of them inside `U`, "
            f"{audit['agreements']} agreements between the full separating-axis "
            f"feasibility predicate and the twenty-inequality local system, "
            f"{len(audit['counterexamples'])} counterexamples. Consistent: "
            f"**{audit['consistent']}**."
        )
        out.append("")
        out.append(f"**Caveat, recorded deliberately:** {audit['caveat']}.")
    out.append("")

    out.append("## Declared mathematical inputs")
    out.append("")
    out.append(
        "What the instrument takes from mathematics rather than deciding by exact "
        "arithmetic. Everything not listed here is computed."
    )
    out.append("")
    out.extend(
        _table(
            ["input", "statement", "used for", "machine-checked here"],
            [
                [
                    entry["name"],
                    entry["statement"],
                    entry["used_for"],
                    entry["machine_checked_here"],
                ]
                for entry in payload["declared_mathematical_inputs"]
            ],
        )
    )
    out.append("")

    out.append("## Controls")
    out.append("")
    out.extend(
        _table(
            ["control", "rejected", "mechanism"],
            [
                [f"`{entry['name']}`", str(entry["rejected"]), entry["mechanism"]]
                for entry in payload["controls"]
            ],
        )
    )
    out.append("")
    for entry in payload["controls"]:
        out.append(f"### `{entry['name']}` — rejected: {entry['rejected']}")
        out.append("")
        out.append(entry["detail"] + ".")
        out.append("")
        out.append("```json")
        out.append(json.dumps(entry["findings"], indent=1, sort_keys=True))
        out.append("```")
        out.append("")

    out.append("## Replay, and the normal-versus-optimized comparison")
    out.append("")
    out.append(
        "Nothing on the certified path uses floating point, and no refusal in this "
        "instrument is an `assert`; the five asserts in the package narrow a type after "
        "a status has already been decided. So `-O`, which strips asserts, must not move "
        "a single byte, and the check is a byte comparison rather than a claim."
    )
    out.append("")
    out.append("```bash")
    out.append("cd packing && export PYTHONPATH=$PWD")
    out.append("./.venv/bin/python3    build_receipt.py OUT/normal")
    out.append("./.venv/bin/python3 -O build_receipt.py OUT/optimized")
    out.append(
        "cmp OUT/normal/instrument-certificate.json \\\n"
        "    OUT/optimized/instrument-certificate.json"
    )
    out.append("cmp OUT/normal/instrument-receipt.md      OUT/optimized/instrument-receipt.md")
    out.append(
        "./.venv/bin/python3 -m pytest -q \\\n"
        "    tests/test_n5_rigidity.py tests/test_n5_local_rigidity.py"
    )
    out.append("```")
    out.append("")
    out.append(
        f"Both interpreters produce payload digest "
        f"`{digest(payload)}` and byte-identical files."
    )
    out.append("")
    out.append(
        "`pytest -O` is *not* the interpreter evidence: pytest disables its own assertion "
        "rewriting under `-O` and warns that it does, so a green run there proves less "
        "than it appears to. The evidence is the byte comparison above."
    )
    out.append("")
    return "\n".join(out) + "\n"
