"""Transfer the accepted SAME25 restriction through a fixed uniformly strict owner0 core."""

from __future__ import annotations

import argparse
import copy
import math
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

from devtools import check_n17_collective_row_coverage as collective
from devtools.provenance import provenance
from sqpack import retained_json

parent, finite, cases, guard = (
    collective.parent,
    collective.finite,
    collective.cases,
    collective.guard,
)
sat = guard.sat
require, tick, checked = collective.require, collective.tick, collective.checked
IncompleteError = collective.IncompleteError
type Point = tuple[Q, Q]
SCHEMA = "n17-strict-core-regional-transfer/v1"
DESCRIPTOR_SCHEMA = "n17-strict-core-regional-transfer-context/v1"
ROLES = ("collective_descriptor", "collective_certificate", "collective_replay")
HALF_WIDTH = Q(1, 2**23)
TAU = Q(53, 128)
MARGIN = Q(1, 2**20)
CORE_LIMIT = 32
QUADRATIC_LIMIT = 512
OUTPUT_LIMIT = 1 << 20
ACCEPTED_LIMIT = 64 << 20
TARGET_OWNER = 18
TARGET_INDICES = (*range(19, 24), *range(33, 53))
payload = collective.payload


def parse_core(raw: Any, deadline: float) -> list[Point]:
    finite.opaque_polygon(raw)
    if len(raw) > CORE_LIMIT:
        raise IncompleteError("strict-transfer core vertex ceiling")
    points = [(finite.rational(x), finite.rational(y)) for x, y in raw]
    require(len(points) >= 3 and parent.area2(points) > 0, "positive-area strict core required")
    require(
        all(finite.cross(a, b, p) >= 0 for a, b in cases.edges(points) for p in points),
        "convex strict core required",
    )
    tick(deadline)
    return points


def uniform_owned(core: list[Point], centre: Point, *, deadline: float) -> dict[str, Any]:
    """Check the point reserve and every new closed angle/centre corner exactly."""
    require(HALF_WIDTH == MARGIN / 8 and HALF_WIDTH > 0, "fixed transfer radius differs")
    require(0 < TAU - HALF_WIDTH < TAU + HALF_WIDTH < 1, "guard interval not interior")
    require(
        len(core) <= CORE_LIMIT and parent.area2(core) > 0,
        "positive-area bounded core required",
    )
    lo, hi = checked(TAU - HALF_WIDTH), checked(TAU + HALF_WIDTH)
    c, s = finite.trig(TAU)
    point_limit = Q(1, 2) - MARGIN
    max_u = max_v = Q(0)
    for q in core:
        tick(deadline)
        delta = (checked(q[0] - centre[0]), checked(q[1] - centre[1]))
        u, v = finite.dot(delta, (c, s)), finite.dot(delta, (-s, c))
        require(
            abs(u) <= point_limit and abs(v) <= point_limit, "point strict-margin premise fails"
        )
        max_u, max_v = max(max_u, abs(u)), max(max_v, abs(v))
    corners = [
        (checked(centre[0] + sx * HALF_WIDTH), checked(centre[1] + sy * HALF_WIDTH))
        for sx, sy in ((-1, -1), (-1, 1), (1, -1), (1, 1))
    ]
    threshold = checked(Q(1, 2) - MARGIN / 2)
    require(threshold < Q(1, 2), "positive regional ownership reserve required")
    minima = []
    for index, q in enumerate(core):
        for corner_index, corner in enumerate(corners):
            x, y = checked(q[0] - corner[0]), checked(q[1] - corner[1])
            for axis in ("u", "v"):
                for sign in (-1, 1):
                    tick(deadline)
                    if len(minima) >= QUADRATIC_LIMIT:
                        raise IncompleteError("strict-transfer quadratic ceiling")
                    polynomial = (
                        (
                            checked(threshold - sign * x),
                            checked(-2 * sign * y),
                            checked(threshold + sign * x),
                        )
                        if axis == "u"
                        else (
                            checked(threshold - sign * y),
                            checked(2 * sign * x),
                            checked(threshold + sign * y),
                        )
                    )
                    minimum, where = sat.minimum(polynomial, lo, hi)
                    require(minimum >= 0, "regional uniform ownership fails")
                    minima.append([index, corner_index, axis, sign, str(minimum), str(where)])
    tick(deadline)
    return {
        "point_margin_checked": True,
        "point_axis_absolute_maxima": [str(max_u), str(max_v)],
        "point_threshold": str(point_limit),
        "regional_threshold": str(threshold),
        "core_vertices": len(core),
        "centre_corners": finite.serial(corners),
        "quadratic_checks": len(minima),
        "quadratic_minima": minima,
        "quadratic_record_fields": [
            "core_vertex",
            "centre_corner",
            "axis",
            "sign",
            "minimum",
            "minimizer",
        ],
        "uniform_strict_ownership_checked": True,
        "equality_at_regional_threshold_allowed": True,
    }


def requested_rows(fresh: dict[str, Any]) -> list[dict[str, Any]]:
    require(
        fresh["schema"] == collective.SCHEMA
        and fresh["status"] == "angle_union_restricted"
        and fresh["criterion_met"] is True
        and fresh["verification_passed"] is True
        and fresh["changed_owners"] == [18]
        and fresh["complete_empty_owners"] == []
        and fresh["all_foreign_rows_accounted"] == 992
        and fresh["original_rows_inherited"] == 1056
        and fresh["simultaneous_original_groups_only"] is True
        and fresh["original_owned_sets_unchanged"] is True
        and fresh["point_contradiction_proved"] is False
        and fresh["declared_guard_exclusion_proved"] is False
        and all(fresh.get(k) is False for k in guard.scope()),
        "accepted collective SAME25 premise differs",
    )
    require(
        [entry["owner"] for entry in fresh["owners"]] == list(collective.OWNERS[1:]),
        "complete inherited collective owner roster differs",
    )
    target = next(r for r in fresh["owners"] if r["owner"] == TARGET_OWNER)
    removed = [r for r in target["rows"] if r["covered"] and r["inherited_domain_nonempty"]]
    require(
        [r["row_index"] for r in removed] == list(TARGET_INDICES)
        and target["lost_length"] == "25/64",
        "accepted SAME25 row roster differs",
    )
    require(
        all(
            r["interval"] == [str(Q(r["row_index"], 64)), str(Q(r["row_index"] + 1, 64))]
            for r in removed
        ),
        "accepted SAME25 original interval differs",
    )
    return [
        {k: copy.deepcopy(r[k]) for k in ("row_index", "reference", "interval")}
        for r in removed
    ]


def read_bound(
    role: str,
    document: dict[str, Any],
    held: dict[Path, tuple[str, int]],
    deadline: float,
    ceiling: int,
) -> dict[str, Any]:
    path = finite.retained_path(document[role])
    raw, value = finite.read_json(path, ceiling)
    require(type(value) is dict, "strict-transfer input JSON object required")
    require(
        finite.digest(path, ceiling, deadline) == document[role + "_sha256"]
        and raw == finite.read_json(path, ceiling)[0],
        "strict-transfer input byte custody differs",
    )
    held[path] = (document[role + "_sha256"], ceiling)
    return cast(dict[str, Any], value)


def generate(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    require(
        type(document) is dict
        and document.get("schema") == DESCRIPTOR_SCHEMA
        and set(document) == {"schema", *(k for r in ROLES for k in (r, r + "_sha256"))},
        "strict-transfer descriptor differs",
    )
    frozen = finite.canonical(document)
    held: dict[Path, tuple[str, int]] = {}
    old_doc = read_bound(ROLES[0], document, held, deadline, parent.JSON_LIMIT)
    accepted = read_bound(ROLES[1], document, held, deadline, ACCEPTED_LIMIT)
    replay = read_bound(ROLES[2], document, held, deadline, ACCEPTED_LIMIT)
    require(
        replay.get("verification_passed") is True and payload(accepted) == payload(replay),
        "accepted collective fresh payload differs",
    )
    # Exactly one complete finite collective reconstruction per new phase.
    fresh = collective.check(old_doc, accepted, deadline=deadline)
    selected = requested_rows(fresh)
    for role in collective.ROLES:
        read_bound(
            role,
            old_doc,
            held,
            deadline,
            parent.JSON_LIMIT if role == collective.ROLES[0] else ACCEPTED_LIMIT,
        )
    point = read_bound("guard_certificate", old_doc, held, deadline, ACCEPTED_LIMIT)
    require(
        point["schema"] == guard.SCHEMA
        and point["status"] == "criterion_missed"
        and point["regional_context_started"] is False
        and len(point["contexts"]) == 1,
        "accepted point context differs",
    )
    context = point["contexts"][0]
    witness = point["matched_owned_point_witness"]
    require(
        witness["tau"] == str(TAU) and len(witness["centre"]) == 2,
        "matched witness shape differs",
    )
    centre = (finite.rational(witness["centre"][0]), finite.rational(witness["centre"][1]))
    require(
        context["guard"]
        == {
            "half_width": "0",
            "centre_box": [[str(x), str(x)] for x in centre],
            "angle_interval": [str(TAU), str(TAU)],
        },
        "accepted point guard identity differs",
    )
    require(
        context["all_original_rows_checked"] == 1056
        and context["all_foreign_rows_conditioned"] == 992
        and context["owner0_owned"] == context["owned_groups"]["0"]
        and point["parent_custody"] == fresh["parent_custody"]
        and point["container"] == guard.standing.CenteredContainer(cases.U, cases.V).record(),
        "fixed owner0 core/parent/container premise differs",
    )
    endpoint = point["original_endpoint_control"]
    require(
        endpoint == fresh["original_endpoint_control"]
        and endpoint["all17_retained"] is True
        and endpoint["family_disjoint"] is True
        and [r["label"] for r in endpoint["witnesses"]] == list(range(1, 18))
        and {r["owner"] for r in endpoint["witnesses"]} == set(collective.OWNERS)
        and endpoint["witnesses"][0]["owner"] == 0
        and endpoint["witnesses"][5]["owner"] == 12
        and endpoint["witnesses"][10]["owner"] == 18,
        "full17 fixed-label inherited endpoint premise differs",
    )
    core = parse_core(context["owner0_owned"], deadline)
    ownership = uniform_owned(core, centre, deadline=deadline)
    lo, hi = checked(TAU - HALF_WIDTH), checked(TAU + HALF_WIDTH)
    require(
        all(not (lo <= endpoint_t <= hi) for endpoint_t in (Q(0), Q(1))),
        "new regional guard meets endpoint family",
    )
    for path, (sha, ceiling) in held.items():
        require(finite.digest(path, ceiling, deadline) == sha, "strict-transfer inputs changed")
    require(finite.canonical(document) == frozen, "strict-transfer descriptor changed")
    tick(deadline)
    return {
        "schema": SCHEMA,
        "status": "same25_regional_rows_restricted",
        "criterion_met": True,
        **guard.scope(),
        "declared_guard_exclusion_proved": False,
        "regional_necessary_domain_restriction_proved": True,
        "point_guard_exclusion_proved": False,
        "point_contradiction_proved": False,
        "point_guard_necessary_domain_restriction_proved": False,
        "accepted_inputs": copy.deepcopy(document),
        "parent_custody": copy.deepcopy(point["parent_custody"]),
        "container": copy.deepcopy(point["container"]),
        "guard": {
            "half_width": str(HALF_WIDTH),
            "angle_interval": [str(lo), str(hi)],
            "centre_box": [
                [str(checked(x - HALF_WIDTH)), str(checked(x + HALF_WIDTH))] for x in centre
            ],
        },
        "owner": TARGET_OWNER,
        "same25_rows_excluded": True,
        "requested_rows": selected,
        "new_uniform_ownership": ownership,
        "collective_finite_reconstructions": 1,
        "collective_rows_rechecked": 992,
        "collective_work": copy.deepcopy(fresh["work"]),
        "original_rows_inherited": 1056,
        "original_parent_proof_replayed": False,
        "root_proof_replayed": False,
        "original17_endpoint_retention_inherited": True,
        "endpoint_witnesses": copy.deepcopy(endpoint["witnesses"]),
        "endpoint_chart_alternatives_inherited": ["0", "1"],
        "endpoint_family_disjoint_checked_now": True,
        "foreign_domains_inherited_under_uniform_core_theorem": True,
        "foreign_regional_domains_reconstructed": False,
        "old_owner0_target_rows_transferred": False,
        "inherited_point_core_source": {
            "path": old_doc["guard_certificate"],
            "sha256": old_doc["guard_certificate_sha256"],
            "json_paths": ["contexts[0].owner0_owned", "contexts[0].owned_groups.0"],
        },
        "mathematical_assurance": (
            "sole-Astra fixed-core hand transfer plus fresh finite reconstruction"
        ),
        "limits": {
            "geometry_bits": finite.BIT_LIMIT,
            "core_vertices": CORE_LIMIT,
            "quadratic_checks": QUADRATIC_LIMIT,
            "margin": str(MARGIN),
            "input_descriptor_bytes": parent.JSON_LIMIT,
            "accepted_receipt_bytes": ACCEPTED_LIMIT,
            "output_bytes": OUTPUT_LIMIT,
            "collective_caps_unchanged": True,
        },
    }


def check(
    document: dict[str, Any], certificate: dict[str, Any], *, deadline: float
) -> dict[str, Any]:
    expected = generate(document, deadline=deadline)
    require(payload(certificate) == expected, "fresh strict-transfer reconstruction differs")
    tick(deadline)
    return copy.deepcopy(expected) | {"verification_passed": True}


def failure(exc: Exception) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": "incomplete" if isinstance(exc, IncompleteError) else "refused",
        "error": str(exc),
        "criterion_met": False,
        "verification_passed": False,
        **guard.scope(),
        "declared_guard_exclusion_proved": False,
        "regional_necessary_domain_restriction_proved": False,
        "same25_rows_excluded": False,
        "point_guard_exclusion_proved": False,
        "point_contradiction_proved": False,
        "point_guard_necessary_domain_restriction_proved": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--descriptor", type=Path, required=True)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--max-seconds", type=float, default=60)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or args.max_seconds <= 0:
        parser.error("max-seconds must be finite and positive")
    deadline = time.monotonic() + args.max_seconds
    try:
        require(
            not any(
                n == p or n.startswith(p + ".")
                for n in sys.modules
                for p in (*finite.FORBIDDEN, "devtools.produce_n17_conditional_owned_hull")
            ),
            "producer/kernel/root import in strict-transfer checker",
        )
        raw, doc = finite.read_json(args.descriptor, parent.JSON_LIMIT)
        if args.certificate:
            saved, certificate = finite.read_json(args.certificate, OUTPUT_LIMIT)
            result = check(doc, certificate, deadline=deadline)
            require(
                saved == finite.read_json(args.certificate, OUTPUT_LIMIT)[0],
                "certificate changed",
            )
        else:
            result = generate(doc, deadline=deadline)
        require(
            raw == finite.read_json(args.descriptor, parent.JSON_LIMIT)[0], "descriptor changed"
        )
    except (
        IncompleteError,
        ValueError,
        KeyError,
        TypeError,
        OSError,
        EOFError,
        guard.standing.VerificationError,
    ) as exc:
        result = failure(exc)
    result.update(
        provenance=provenance(
            *(
                Path(cast(str, m.__file__))
                for m in (
                    sys.modules[__name__],
                    collective,
                    collective.prior,
                    guard,
                    parent,
                    finite,
                    cases,
                    sat,
                    guard.standing,
                )
            )
        ),
        invocation={
            "argv": argv if argv is not None else sys.argv[1:],
            "executable": sys.executable,
        },
    )
    text = retained_json.dumps(result, sort_keys=True)
    if len(text.encode()) > OUTPUT_LIMIT or time.monotonic() >= deadline:
        result = failure(IncompleteError("strict-transfer output byte or wall ceiling"))
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)
    return 0 if result["status"] == "same25_regional_rows_restricted" else 1


if __name__ == "__main__":
    raise SystemExit(main())
