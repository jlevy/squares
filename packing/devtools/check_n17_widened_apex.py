"""Check a conditional n17 apex cube using retained position duals, without LP solves.

The declared container is fixed at the accepted exact-root side. Feature forcing,
root tightness, slide invariance and the accepted local theorem are explicit premises.
The finite-geometry implication remains a reviewed hand proof, not a formal proof.
Importing this module reads no scientific inputs.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import argparse
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

from devtools import audit_n17_endpoint_receipt as exact
from devtools import check_n17_core_stress as core
from devtools import check_n17_endpoint_feasibility as endpoint
from devtools import check_n17_local_minimum as local
from devtools import check_n17_widened_features as forcing
from devtools.check_n17_endpoint_feasibility import _layout
from devtools.check_n17_local_minimum import _named_lift
from devtools.provenance import provenance
from sqpack import retained_json

SCHEMA = "n17-widened-apex-certificate/v1"
RUN = exact.REPO / exact.RESULTS / "exp-248-n17-local-half-composition/run-002"
DUALS = RUN / "certificates.json"
CONSTANTS = {
    "wall_lipschitz": "1/2",
    "pair_lipschitz": "12/5",
    "local_radius": "1/5000",
    "position_headroom": "1/10000",
    "half_angle_factor": "1/2",
}
SCOPE = (
    "conditional apex cube in fixed exact-root container; feature forcing, root tightness, "
    "slide invariance and local theorem are premises; no annulus or capture claim"
)


def position_names() -> tuple[str, ...]:
    names = tuple(
        name for name in local.coordinate_lifts((Q(1), Q(0))) if not name.startswith("omega")
    )
    exact.require(len(names) == 29, "position coordinate roster differs")
    return names


def row_roster() -> tuple[local.RowKey, ...]:
    keys = []
    for label, wall in local.ANCHORS:
        keys.extend(("wall", label, wall, variant) for variant in range(1 if label == 9 else 2))
    for left, right, _, _ in local.CONTACTS:
        keys.extend(
            ("pair", left, right, variant)
            for variant in range(2 if (left, right) in local.PARALLEL_PAIRS else 1)
        )
    selected = tuple(key for key in keys if key not in local.ZERO_WEIGHT_KEYS)
    exact.require(
        len(selected) == 52 and len(set(selected)) == 52, "positive row roster differs"
    )
    return selected


def project_rows(
    rows: dict[local.RowKey, list[Any]], aux: dict[str, Any]
) -> list[list[core.Dyadic]]:
    """Only position lifts survive: every angle and side-increment column is zero."""
    lifts = [_named_lift(name, aux["u"]) for name in position_names()]
    return [
        [
            sum(
                (
                    core.Dyadic.cast(rows[key][column]) * weight
                    for column, weight in lift.items()
                ),
                core.Dyadic.point(0),
            )
            for lift in lifts
        ]
        for key in row_roster()
    ]


def selected_weights(document: dict[str, Any]) -> tuple[dict[str, Any], tuple[Q, ...]]:
    """Choose the lexicographically first closed origin cell; evaluate its affine dual."""
    exact.require(set(document) == {"direction", "cells"}, "wrong retained direction fields")
    exact.require(type(document["cells"]) is list and document["cells"], "missing dual cells")
    candidates = []
    for item in cast(list[dict[str, Any]], document["cells"]):
        exact.require(set(item) == {"cell", "lambda", "mu"}, "wrong dual fields")
        exact.require(len(item["cell"]) == 3, "wrong slider cell dimension")
        bounds = [exact.read_interval(pair) for pair in item["cell"]]
        exact.require(all(lo < hi for lo, hi in bounds), "degenerate dual cell")
        exact.require(
            len(item["lambda"]) == 52 and len(item["mu"]) == 3, "wrong dual dimensions"
        )
        exact.require(
            all(len(values) == 52 for values in item["mu"]), "wrong affine dual slope width"
        )
        exact.require(
            all(
                type(value) is int
                for values in [item["lambda"], *item["mu"]]
                for value in values
            ),
            "dual numerators must be integers",
        )
        if all(lo <= 0 <= hi for lo, hi in bounds):
            candidates.append((tuple(value for pair in bounds for value in pair), item))
    exact.require(candidates, "no closed dual cell contains origin")
    _, selected = min(candidates, key=lambda candidate: candidate[0])
    dual = local.read_dual(selected)
    weights = tuple(
        dual.lam[i] - sum((dual.cell.centre[k] * dual.mu[k][i] for k in range(3)), Q(0))
        for i in range(52)
    )
    exact.require(all(weight >= 0 for weight in weights), "negative evaluated dual weight")
    return selected, weights


def retained_cell(cell: dict[str, Any]) -> dict[str, Any]:
    """Retain exact dual numerators as canonical strings under the JSON input bounds.

    The source duals use integer numerators at the fixed dual scale. Certificate
    decoding intentionally permits only small bare JSON integers, so these witness
    numerators use the same bounded rational-string representation as other exact data.
    Replay regenerates these strings from the original integer witness.
    """

    def numerator(value: int) -> str:
        text = str(value)
        exact.require(exact.rational(text) == value, "dual numerator encoding differs")
        return text

    return {
        "cell": cell["cell"],
        "lambda": [numerator(value) for value in cell["lambda"]],
        "mu": [[numerator(value) for value in values] for values in cell["mu"]],
    }


def evaluate(
    rows: list[list[core.Dyadic]],
    documents: list[dict[str, Any]],
) -> dict[str, Any]:
    """Compute all 58 row-l1 residual bounds and Lipschitz masses exactly."""
    names, keys = position_names(), row_roster()
    exact.require(len(rows) == 52 and all(len(row) == 29 for row in rows), "wrong T dimensions")
    expected = {f"{sign}{name}" for name in names for sign in ("+", "-")}
    selected = [document for document in documents if document["direction"] in expected]
    exact.require(
        len(selected) == 58 and {row["direction"] for row in selected} == expected,
        "missing or duplicate signed position direction",
    )
    entries = []
    largest_epsilon, largest_mass = Q(0), Q(0)
    columns = [
        [(i, row[j]) for i, row in enumerate(rows) if row[j].lo != 0 or row[j].hi != 0]
        for j in range(29)
    ]
    for document in selected:
        direction = document["direction"]
        sign, column = (1 if direction[0] == "+" else -1), names.index(direction[1:])
        cell, weights = selected_weights(document)
        residuals = [
            sum(
                (weights[i] * value for i, value in columns[j] if weights[i] != 0),
                core.Dyadic.point(sign if j == column else 0),
            )
            for j in range(29)
        ]
        epsilon = sum((max(abs(value.lo), abs(value.hi)) for value in residuals), Q(0))
        mass = sum(
            (
                weight * (Q(1, 2) if key[0] == "wall" else Q(12, 5))
                for weight, key in zip(weights, keys, strict=True)
            ),
            Q(0),
        )
        largest_epsilon, largest_mass = max(largest_epsilon, epsilon), max(largest_mass, mass)
        entries.append(
            {
                "direction": direction,
                "selected_cell": retained_cell(cell),
                "weights_at_origin": [str(weight) for weight in weights],
                "residual_intervals": [[str(value.lo), str(value.hi)] for value in residuals],
                "epsilon": str(epsilon),
                "mass": str(mass),
            }
        )
    exact.require(largest_epsilon < 1, "position residual is not below one")
    exact.require(largest_mass > 0, "nonpositive Lipschitz mass")
    alpha = min(Q(1, 5000), (1 - largest_epsilon) / (10000 * largest_mass))
    return {
        "signed_directions": entries,
        "epsilon": str(largest_epsilon),
        "C": str(largest_mass),
        "alpha0": str(alpha),
        "q0": str(alpha / 2),
        "position_bound_at_alpha0": str(largest_mass * alpha / (1 - largest_epsilon)),
    }


def load_target(
    feature_path: Path,
) -> tuple[dict[str, Any], list[list[core.Dyadic]], list[dict[str, Any]]]:
    feature_packet = exact.decode(exact.read_bytes(feature_path))
    forcing.check(feature_packet)
    inputs, _, _ = forcing.load_root()
    t, beta = (
        core.Dyadic.enclose(*exact.read_interval(pair))
        for pair in inputs["root_inclusion_box_used"]
    )
    _, aux, centres = _layout(t, beta, core.Dyadic.point(Q(1, 2)))
    rows = local.generic_rows(aux, centres, local.FACE_BRANCHES)
    matrix = project_rows(rows, aux)
    # Translation columns are independent of sliders; recompute the projected rows.
    exact.require(
        all(
            project_rows(
                local.generic_rows(
                    aux, local.shifted_centres(centres, aux["v"], vertex), local.FACE_BRANCHES
                ),
                aux,
            )
            == matrix
            for vertex in forcing.vertices()
        ),
        "position projection depends on sliders",
    )
    receipt = exact.decode(exact.read_bytes(RUN / "receipt.json"))
    exact.require(
        receipt["passed"] is True and receipt["schema"] == local.RATIO_SCHEMA,
        "local theorem receipt not accepted",
    )
    exact.require(
        receipt["inputs"]["root_certificate_git_ref"] == exact.ROOT_REF,
        "local theorem root differs",
    )
    exact.require(
        receipt["radius"] == {"coordinates": 45, "uniform": "1/5000"},
        "local theorem radius differs",
    )
    exact.require(
        receipt["slider_box"]
        == {
            name: [str(lo), str(hi)]
            for name, (lo, hi) in zip(local.SLIDER_PARAMETERS, forcing.DOMAIN, strict=True)
        },
        "local theorem slider domain differs",
    )
    documents = json.loads(exact.read_bytes(DUALS), object_pairs_hook=exact.duplicate_refusal)
    exact.require(type(documents) is list, "dual packet must be a list")
    binding = {
        "root": inputs,
        "features_path": str(feature_path.resolve().relative_to(exact.REPO)),
        "feature_margin": feature_packet["final_margin"],
        "retained_duals": str(DUALS.relative_to(exact.REPO)),
        "retained_local_receipt": str((RUN / "receipt.json").relative_to(exact.REPO)),
        "retained_source_revision": "f8c1246b2e6ddf53fd76a6a2f9c5ad060579e081",
        "premises": [
            "H257 root feature tightness",
            "C2 slide invariance",
            "C10 active walls",
            "accepted local theorem at 1/5000",
            "Astra finite-geometry hand proof",
        ],
        "container": "fixed [0,S_exact_root]^2; side increment zero",
    }
    return binding, matrix, documents


def generate(feature_path: Path) -> dict[str, Any]:
    inputs, matrix, documents = load_target(feature_path)
    return {
        "schema": SCHEMA,
        "inputs": inputs,
        "constants": dict(CONSTANTS),
        "slider_box": [[str(lo), str(hi)] for lo, hi in forcing.DOMAIN],
        "position_columns": list(position_names()),
        "row_roster": [list(key) for key in row_roster()],
        "scope": SCOPE,
        **evaluate(matrix, documents),
    }


def check(packet: dict[str, Any], feature_path: Path) -> dict[str, Any]:
    expected = generate(feature_path)
    exact.require(
        exact.exact_structure({name: packet[name] for name in expected}, expected),
        "apex certificate differs from exact replay",
    )
    return {
        "schema": "n17-widened-apex-check/v1",
        "verification_passed": True,
        "epsilon": expected["epsilon"],
        "C": expected["C"],
        "alpha0": expected["alpha0"],
        "q0": expected["q0"],
        "scope": SCOPE,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--features", type=Path, required=True)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        packet = (
            generate(args.features)
            if args.certificate is None
            else exact.decode(exact.read_bytes(args.certificate))
        )
        result = check(packet, args.features)
        packet["checker"] = result
        packet["provenance"] = provenance(
            Path(__file__),
            Path(local.__file__),
            Path(core.__file__),
            Path(forcing.__file__),
            Path(endpoint.__file__),
            Path(exact.__file__),
            Path(forcing.root.__file__),
            Path(forcing.features.__file__),
        )
    except (ValueError, OSError, KeyError, TypeError) as error:
        packet = {"schema": SCHEMA, "verification_passed": False, "error": str(error)}
        result = packet
    if args.output is not None:
        args.output.write_text(retained_json.dumps(packet))
    print(json.dumps(result))
    return 0 if result.get("verification_passed") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
