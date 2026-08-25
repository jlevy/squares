#!/usr/bin/env python3
"""Find one exact inclusion-minimal incidence core for a Trump tangent branch.

This is deliberately narrower than an enumeration of every minimal support.  The
primitive tangent rows are kept atomically by their physical incidence: eleven wall
incidences and fourteen pair contacts.  Floating-point linear programs may propose a
stress or direction, but a proposal affects the result only after exact replay in
``Q(u)``.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from dataclasses import dataclass

from cases.trump11 import packing as trump11
from cases.trump11 import tangent_cones


@dataclass(frozen=True)
class IncidenceGroup:
    """All primitive rows contributed by one physical active incidence."""

    identifier: str
    kind: str
    subject: dict
    feature_label: str
    feature_aliases: tuple[str, ...]
    rows: tuple[tangent_cones.LinearRow, ...]


def oriented_row_class_key(row: tangent_cones.LinearRow) -> tuple:
    """Normalize an exact half-space row modulo positive proportionality.

    The first nonzero coefficient is normalized to ``1`` or ``-1`` according to its
    original sign. Thus ``r`` and ``c r`` agree for exact ``c > 0``, while ``-r`` stays
    distinct because it defines the oppositely oriented half-space.
    """

    leading = next(
        (coefficient for coefficient in row.coefficients if not coefficient.is_zero()),
        None,
    )
    if leading is None:
        raise ValueError(f"zero tangent row has no oriented class: {row.label}")
    positive_scale = leading if leading.sign() > 0 else -leading
    return tuple(
        tangent_cones.scalar_key(coefficient / positive_scale)
        for coefficient in row.coefficients
    )


def group_record(group: IncidenceGroup) -> dict:
    return {
        "id": group.identifier,
        "kind": group.kind,
        "subject": group.subject,
        "feature_label": group.feature_label,
        "feature_aliases": list(group.feature_aliases),
        "row_count": len(group.rows),
        "source_row_labels": [row.label for row in group.rows],
    }


def flatten(groups: tuple[IncidenceGroup, ...]) -> tuple[tangent_cones.LinearRow, ...]:
    return tuple(itertools.chain.from_iterable(group.rows for group in groups))


def derive_branch(branch: int):
    squares, side, field = trump11.build()
    walls, incidences, centres = tangent_cones.wall_rows(squares, side, field)
    contacts = tangent_cones.contact_options(squares, centres, field)
    branch_groups = tangent_cones.enumerate_branch_groups(walls, contacts)
    ordered_branches = sorted(branch_groups.items())
    if not 0 <= branch < len(ordered_branches):
        raise ValueError(
            f"branch must be between 0 and {len(ordered_branches) - 1}, got {branch}"
        )
    matrix_key, branch_group = ordered_branches[branch]
    representative = tuple(branch_group["selections"][0])

    groups: list[IncidenceGroup] = []
    offset = 0
    for incidence in incidences:
        count = int(incidence["tangent_rows"])
        rows = tuple(walls[offset : offset + count])
        offset += count
        square = int(incidence["square"])
        wall = str(incidence["wall"])
        identifier = f"wall:{square}:{wall}"
        groups.append(
            IncidenceGroup(
                identifier=identifier,
                kind="wall",
                subject={
                    "square": square,
                    "wall": wall,
                    "support_corners": list(incidence["support_corners"]),
                },
                feature_label=identifier,
                feature_aliases=(),
                rows=rows,
            )
        )
    if offset != len(walls):
        raise AssertionError("wall-incidence slicing did not consume every wall row")

    for contact, option_index in zip(contacts, representative, strict=True):
        option = contact.options[option_index]
        first, second = contact.pair
        groups.append(
            IncidenceGroup(
                identifier=f"pair:{first}-{second}",
                kind="pair",
                subject={"pair": [first, second], "selected_option": option_index},
                feature_label=option.label,
                feature_aliases=option.aliases,
                rows=option.rows,
            )
        )

    grouped_rows = flatten(tuple(groups))
    if tangent_cones.matrix_key(grouped_rows) != matrix_key:
        raise AssertionError("grouped incidence rows do not reproduce the branch matrix")
    return field, tuple(groups), branch_group, representative


def cone_oracle(rows, field) -> dict:
    """Return an exact terminal certificate, or explicitly return unresolved."""

    rows = tuple(rows)
    certificate = tangent_cones.positive_stress_certificate(rows, field)
    if certificate is not None and tangent_cones.replay_certificate(rows, certificate, field):
        return {"verdict": "zero", "certificate": certificate, "direction": None}

    direction = tangent_cones.exact_nonzero_direction(rows, field)
    if direction is not None and tangent_cones.replay_direction(rows, direction, field):
        return {
            "verdict": "nonzero_direction",
            "certificate": None,
            "direction": direction,
        }
    return {"verdict": "unresolved", "certificate": None, "direction": None}


def minimize_groups(groups: tuple[IncidenceGroup, ...], field, *, oracle=cone_oracle) -> dict:
    """Greedily produce one inclusion-minimal grouped support, with exact witnesses."""

    root = oracle(flatten(groups), field)
    if root["verdict"] != "zero":
        return {
            "status": "unresolved" if root["verdict"] == "unresolved" else "root_not_zero",
            "root": root,
            "decisions": [],
            "core_group_ids": [],
            "final_certificate": None,
            "deletion_witnesses": {},
        }

    candidate = list(groups)
    decisions = []
    witnesses: dict[str, dict] = {}
    for group in groups:
        if group not in candidate:
            continue
        trial = tuple(item for item in candidate if item != group)
        trial_result = oracle(flatten(trial), field)
        verdict = trial_result["verdict"]
        if verdict == "zero":
            candidate = list(trial)
            decisions.append({"group_id": group.identifier, "action": "delete"})
        elif verdict == "nonzero_direction":
            witnesses[group.identifier] = trial_result["direction"]
            decisions.append({"group_id": group.identifier, "action": "keep"})
        else:
            decisions.append({"group_id": group.identifier, "action": "unresolved"})
            return {
                "status": "unresolved",
                "root": root,
                "decisions": decisions,
                "core_group_ids": [item.identifier for item in candidate],
                "final_certificate": None,
                "deletion_witnesses": witnesses,
                "unresolved_group_id": group.identifier,
            }

    core = tuple(candidate)
    final = oracle(flatten(core), field)
    if final["verdict"] != "zero":
        raise AssertionError("the greedily retained core lost its exact zero certificate")
    for group in core:
        direction = witnesses.get(group.identifier)
        if direction is None:
            raise AssertionError(f"core group lacks a deletion witness: {group.identifier}")
        trial_rows = flatten(tuple(item for item in core if item != group))
        if not tangent_cones.replay_direction(trial_rows, direction, field):
            raise AssertionError(
                f"deletion witness failed on the final core: {group.identifier}"
            )
    return {
        "status": "completed",
        "root": root,
        "decisions": decisions,
        "core_group_ids": [group.identifier for group in core],
        "final_certificate": final["certificate"],
        "deletion_witnesses": witnesses,
    }


def build_result(branch: int, *, selftest: bool) -> dict:
    field, groups, branch_group, representative = derive_branch(branch)
    wall_groups = tuple(group for group in groups if group.kind == "wall")
    pair_groups = tuple(group for group in groups if group.kind == "pair")
    primitive_rows = flatten(groups)
    positive_two = field.rational(2)
    normalization_control = primitive_rows[0]
    doubled_control = tangent_cones.LinearRow(
        "positive-scale-control",
        tuple(positive_two * coefficient for coefficient in normalization_control.coefficients),
    )
    opposite_control = tangent_cones.LinearRow(
        "orientation-control",
        tuple(-coefficient for coefficient in normalization_control.coefficients),
    )
    checks = {
        "wall_incidence_count_is_11": len(wall_groups) == 11,
        "pair_contact_count_is_14": len(pair_groups) == 14,
        "group_count_is_25": len(groups) == 25,
        "primitive_row_count_is_42": len(primitive_rows) == 42,
        "group_ids_are_unique": len({group.identifier for group in groups}) == len(groups),
        "source_row_labels_are_complete": all(
            len(group.rows) == len(group_record(group)["source_row_labels"]) for group in groups
        ),
        "wall_rows_are_not_called_aliases": all(
            not group.feature_aliases for group in wall_groups
        ),
        "contact_feature_aliases_are_complete": (
            all(group.feature_aliases for group in pair_groups)
            and math.prod(len(group.feature_aliases) for group in pair_groups)
            == branch_group["raw_selection_count"]
        ),
        "positive_row_scaling_has_same_class": (
            oriented_row_class_key(normalization_control)
            == oriented_row_class_key(doubled_control)
        ),
        "opposite_row_has_distinct_class": (
            oriented_row_class_key(normalization_control)
            != oriented_row_class_key(opposite_control)
        ),
        "unresolved_oracle_is_terminal": (
            minimize_groups(
                groups[:1],
                field,
                oracle=lambda _rows, _field: {
                    "verdict": "unresolved",
                    "certificate": None,
                    "direction": None,
                },
            )["status"]
            == "unresolved"
        ),
    }
    if selftest and not all(checks.values()):
        raise AssertionError(f"incidence-core structural selftest failed: {checks}")

    minimization = minimize_groups(groups, field)
    root_classes = {oriented_row_class_key(row) for row in primitive_rows}
    core_ids = set(minimization["core_group_ids"])
    core = tuple(group for group in groups if group.identifier in core_ids)
    core_classes = {oriented_row_class_key(row) for row in flatten(core)}
    removed_classes = root_classes - core_classes
    proper = minimization["status"] == "completed" and bool(removed_classes)
    minimization["root_oriented_row_class_count"] = len(root_classes)
    minimization["core_oriented_row_class_count"] = len(core_classes)
    minimization["proper"] = proper
    if selftest:
        completed = minimization["status"] == "completed"
        checks["minimization_completed"] = completed
        checks["proper_core_found"] = proper
        checks["final_stress_replays"] = completed and tangent_cones.replay_certificate(
            flatten(core), minimization["final_certificate"], field
        )
        checks["all_final_deletions_replay"] = completed and all(
            tangent_cones.replay_direction(
                flatten(tuple(item for item in core if item != group)),
                minimization["deletion_witnesses"][group.identifier],
                field,
            )
            for group in core
        )
        checks["proper_matches_row_class_drop"] = proper == (
            len(core_classes) < len(root_classes)
        )

    if minimization["status"] == "completed" and proper:
        outcome = "criterion_met"
        claim = "one proper exact inclusion-minimal grouped-incidence core was found"
    elif minimization["status"] == "completed":
        outcome = "criterion_missed"
        claim = (
            "the grouped support is inclusion-minimal, but it removes no oriented "
            "half-space row class"
        )
    else:
        outcome = "invalid"
        claim = "the exact grouped-incidence minimization did not terminate"

    return {
        "schema_version": 1,
        "subject": {
            "n": tangent_cones.EXPECTED_SQUARES,
            "field": "Q(u)",
            "variables": tangent_cones.EXPECTED_VARIABLES,
            "fixed_side": True,
        },
        "branch": {
            "index": branch,
            "representative_selection": list(representative),
            "derivative_selections": [
                list(selection) for selection in branch_group["selections"]
            ],
            "raw_selection_count": branch_group["raw_selection_count"],
        },
        "groups": [group_record(group) for group in groups],
        "method": {
            "support_notion": "physical incidences, branchwise and inclusion-minimal",
            "item_order": [group.identifier for group in groups],
            "numeric_role": "propose only",
            "decisive_role": "exact Q(u) rank, stress, direction, and replay",
            "exhaustive_support_enumeration": False,
        },
        "minimization": minimization,
        "determination": {
            "outcome": outcome,
            "claim": claim,
            "proper_requires_oriented_row_class_removal": True,
        },
        "selftests": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch", type=int, required=True)
    parser.add_argument("--selftest", action="store_true")
    arguments = parser.parse_args()
    result = build_result(arguments.branch, selftest=arguments.selftest)
    print(json.dumps(result, indent=2))
    if result["minimization"]["status"] != "completed":
        raise SystemExit(2)
    if arguments.selftest and not all(result["selftests"].values()):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
