"""Target-free controls of complete partner-pose quantifiers and exact boundaries."""

from __future__ import annotations

import copy
import gzip
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pytest
from test_probe_n17_conditional_owned_hull import fixture as parent_fixture
from test_probe_n17_pooled_feasible_center import synthetic as feasible_fixture

from devtools import check_n17_full_square_partner_coupling as sat
from devtools import check_n17_partner_pose_coupling as tool

Q = tool.Q


def deadline() -> float:
    return time.monotonic() + 30


def points(raw: list[tuple[int | Q, int | Q]]) -> list[tool.Point]:
    return [(Q(x), Q(y)) for x, y in raw]


def rows(owner: int = 1, count: int = 64) -> list[dict[str, Any]]:
    return [
        {
            "interval": [str(Q(i, count)), str(Q(i + 1, count))],
            "reference": {"kind": "wall_seed", "owner": owner, "row": i},
            "outer_domain": [],
            "residual_polygons": [],
        }
        for i in range(count)
    ]


@pytest.mark.parametrize("engine", [tool, sat], ids=["strict_core", "full_square"])
def test_amended_closed_row_piece_boundary_preserves_every_piece(engine: Any) -> None:
    assert tool.ROW_PIECE_LIMIT == 1024
    row = rows()[0]
    row["residual_polygons"] = [[["1", "1"]] for _ in range(1024)]
    counter = [0]
    admitted = engine.row_domain(row, counter, deadline())
    assert len(admitted["pieces"]) == 1024
    assert counter == [1024]
    assert admitted["domain"] == [(Q(1), Q(1))]
    row["residual_polygons"].append([["1", "1"]])
    counter = [0]
    with pytest.raises(tool.IncompleteError, match=r"per-row .*piece ceiling"):
        engine.row_domain(row, counter, deadline())
    assert counter == [0]


@pytest.mark.parametrize("engine", [tool, sat], ids=["strict_core", "full_square"])
def test_amended_cumulative_vertex_boundary_refuses_the_next_piece(engine: Any) -> None:
    assert tool.INPUT_VERTICES == 1048576
    row = rows()[0]
    row["residual_polygons"] = [[["1", "1"], ["2", "1"], ["1", "2"]]]
    counter = [tool.INPUT_VERTICES - 3]
    admitted = engine.row_domain(row, counter, deadline())
    assert counter == [tool.INPUT_VERTICES]
    assert len(admitted["domain"]) == 3
    row["residual_polygons"] = [[["1", "1"]]]
    with pytest.raises(tool.IncompleteError, match="used input vertex ceiling"):
        engine.row_domain(row, counter, deadline())
    assert counter == [tool.INPUT_VERTICES + 1]


@pytest.mark.parametrize("interval", [(Q(0), Q(1)), (Q(0), Q(1, 64)), (Q(1), Q(1))])
def test_general_partner_core_not_guard_limited(interval: tuple[Q, Q]) -> None:
    lo, hi = interval
    core = tool.core(lo, hi, strict=True, deadline=deadline())
    assert tool.area2(core) > 0
    assert tool.standing.core_strict(core, lo, hi)
    assert tool.cases.contains(core, (Q(0), Q(0)))


def test_exact_full_singleton_square_and_closed_arc_boundary() -> None:
    body = tool.core(tool.TAU, tool.TAU, strict=False, deadline=deadline())
    c, s = tool.finite.trig(tool.TAU)
    expected = {
        (sx * c / 2 - sy * s / 2, sx * s / 2 + sy * c / 2) for sx in (-1, 1) for sy in (-1, 1)
    }
    assert set(body) == expected
    assert tool.core_closed(body, tool.TAU, tool.TAU)
    assert not tool.standing.core_strict(body, tool.TAU, tool.TAU)
    wider = tool.core(Q(0), Q(1), strict=False, deadline=deadline())
    assert tool.core_closed(wider, Q(0), Q(1))


def test_quadratic_interior_minimum_and_zero_boundary() -> None:
    assert not tool.quadratic_nonnegative(Q(0), Q(-1), Q(1), Q(0), Q(1))
    assert tool.quadratic_nonnegative(Q(1, 4), Q(-1), Q(1), Q(0), Q(1))


@pytest.mark.parametrize("mutation", ["missing", "gap", "overlap", "ref", "owner", "open"])
def test_partition_and_typed_reference_refusal(mutation: str) -> None:
    raw = rows()
    if mutation == "missing":
        raw.pop()
    elif mutation == "gap":
        raw[1]["interval"][0] = "1/32"
    elif mutation == "overlap":
        raw[1]["interval"][0] = "0"
    elif mutation == "ref":
        raw[1]["reference"]["row"] = 2
    elif mutation == "owner":
        raw[1]["reference"]["owner"] = 2
    else:
        raw[-1]["interval"][1] = "63/64"
    with pytest.raises(ValueError, match=r"roster|partition|reference|cover"):
        tool.closed_rows(raw, 1, 64)


def test_complete_32_and64_partitions() -> None:
    tool.closed_rows(rows(12, 32), 12, 32)
    tool.closed_rows(rows(), 1, 64)


def test_each_piece_wall_clipped_before_hull() -> None:
    raw = rows()[0]
    raw["residual_polygons"] = [[["0", "1"]], [["5", "1"]]]
    result = tool.row_domain(raw, [0], deadline())
    assert result["domain"] == []
    assert len(result["pieces"]) == 2
    assert all(p["necessary_domain"] == [] for p in result["pieces"])
    # Convexifying the two impossible alternatives first would create legal centres.
    assert tool.wall_clip(points([(0, 1), (5, 1)]), Q(0), Q(1, 64), deadline())


def test_row_support_uses_minimum_over_all_disconnected_pieces() -> None:
    raw = rows()[0]
    raw["residual_polygons"] = [[["1", "1"]], [["2", "1"]]]
    record = tool.row_domain(raw, [0], deadline())
    body = tool.core(Q(0), Q(0), strict=False, deadline=deadline())
    shifted = list(tool.row_planes(record["domain"], record["core"], body))
    for a, b, rhs in shifted:
        facets = list(
            tool.standing.difference_facets(
                [tool.standing.homogeneous(p) for p in record["core"]],
                [tool.standing.homogeneous(p) for p in body],
            )
        )
        facet = next(f for f in facets if Q(f[0]) == a and Q(f[1]) == b)
        assert rhs == Q(facet[2], facet[3]) + min(a * x + b * y for x, y in record["domain"])


def test_intersect_partner_rows_instead_of_union() -> None:
    own = tool.core(Q(0), Q(0), strict=False, deadline=deadline())
    core = tool.core(Q(0), Q(0), strict=True, deadline=deadline())
    first = {"domain": points([(1, 1)]), "core": core}
    second = {"domain": points([(3, 1)]), "core": core}
    r1 = tool.collision_region([first], own, deadline())
    r2 = tool.collision_region([second], own, deadline())
    assert tool.cases.contains(r1, (Q(1), Q(1)))
    assert tool.cases.contains(r2, (Q(3), Q(1)))
    assert tool.collision_region([first, second], own, deadline()) == []


def test_translation_sign_and_closed_degenerate_domain() -> None:
    own = tool.core(Q(0), Q(0), strict=False, deadline=deadline())
    core = tool.core(Q(0), Q(0), strict=True, deadline=deadline())
    row = {"domain": points([(2, 3), (Q(5, 2), 3)]), "core": core}
    region = tool.collision_region([row], own, deadline())
    assert tool.cases.contains(region, (Q(2), Q(3)))
    assert not tool.cases.contains(region, (Q(0), Q(0)))


def test_resource_deadline_and_used_big_rational() -> None:
    with pytest.raises(tool.IncompleteError):
        tool.core(Q(0), Q(1), strict=True, deadline=time.monotonic() - 1)
    raw = rows()[0]
    raw["residual_polygons"] = [[[str(2**4100), "1"]]]
    with pytest.raises(tool.IncompleteError):
        tool.row_domain(raw, [0], deadline())


def synthetic_state(
    *, positive: bool = False
) -> tuple[dict[str, Any], dict[str, int], list[Any], tool.Point]:
    roles = {str(i): i - 1 for i in range(1, 18)}
    roles["6"], roles["13"] = 12, 5
    centre = (Q(3, 2), Q(3, 2)) if positive else (Q(1), Q(1))
    foreign = centre if positive else (Q(3), Q(3))
    cells, roster = {}, []
    for label in range(1, 18):
        owner = roles[str(label)]
        raw = rows(owner, 32 if label == 6 else 64)
        point = centre if owner == 0 else foreign
        for row in raw:
            row["residual_polygons"] = [tool.finite.serial([point])]
        if owner != 0:
            for row in raw[1:]:
                row["residual_polygons"] = []
        if owner == 0:
            for index in (0, len(raw) - 1):
                raw[index]["residual_polygons"] = [[["1", "1"]]]
        cells[str(owner)] = raw
        endpoint = (Q(1), Q(1)) if owner == 0 else foreign
        roster.append(
            {
                "label": label,
                "owner": owner,
                "centre": [[str(x), str(x)] for x in endpoint],
                "charts": [["0", "0"], ["1", "1"]],
            }
        )
    return cells, roles, roster, centre


def test_full992_foreign_rows_fixed_miss_skips_ladder() -> None:
    cells, roles, roster, centre = synthetic_state()
    result = tool.construct(cells, roles, roster, centre, deadline=deadline())
    assert result["all_rows_checked"] == 1056
    assert result["foreign_rows_checked"] == 992
    assert result["status"] == "criterion_missed"
    assert result["levels"] == []
    assert result["unstarted_ladder"] == list(map(str, tool.LADDER))
    assert len(result["endpoint_control"]["witnesses"]) == 17


def test_nonzero_region_success_preserves_closed_singleton_seams() -> None:
    cells, roles, roster, centre = synthetic_state(positive=True)
    result = tool.construct(cells, roles, roster, centre, deadline=deadline())
    assert result["fixed_witness_excluded"] is True
    assert result["closed_region_exclusion_proved"] is True
    assert result["levels"][0]["half_width"] == "1/128"
    found = result["levels"][0]["rows"]
    assert [r["row_index"] for r in found] == [25, 26, 27]
    assert found[0]["interval"] == ["13/32", "13/32"]
    assert found[2]["interval"] == ["27/64", "27/64"]
    assert all(p["covered"] for r in found for p in r["pieces"])


def test_point_only_all_four_regional_levels_miss(monkeypatch: pytest.MonkeyPatch) -> None:
    cells, roles, roster, centre = synthetic_state(positive=True)
    # This control exercises disposition plumbing; geometric row constraints
    # are covered separately by the MIN and all-row intersection controls.
    monkeypatch.setattr(tool, "collision_region", lambda *_: [centre])
    for row in cells["0"]:
        row["residual_polygons"].append(
            tool.finite.serial(
                points(
                    [
                        (Q(7, 5), Q(7, 5)),
                        (Q(8, 5), Q(7, 5)),
                        (Q(8, 5), Q(8, 5)),
                        (Q(7, 5), Q(8, 5)),
                    ]
                )
            )
        )
    result = tool.construct(cells, roles, roster, centre, deadline=deadline())
    assert result["fixed_witness_excluded"] is True
    assert result["status"] == "fixed_witness_only"
    assert result["criterion_met"] is False
    assert len(result["levels"]) == 4
    assert not result["unstarted_ladder"]


@pytest.mark.parametrize(
    "kind", ["empty_partner", "lost_pose", "witness", "endpoint_angle", "missing_owner"]
)
def test_calibrations_refuse(kind: str) -> None:
    cells, roles, roster, centre = synthetic_state()
    if kind == "empty_partner":
        for row in cells["1"]:
            row["residual_polygons"] = [[["0", "0"]]]
    elif kind == "lost_pose":
        roster[1]["centre"] = [["2", "2"], ["2", "2"]]
    elif kind == "witness":
        centre = (Q(2), Q(2))
    elif kind == "endpoint_angle":
        roster[0]["charts"] = [[str(tool.TAU), str(tool.TAU)]]
    else:
        cells.pop("1")
    with pytest.raises(ValueError, match=r"calibration|witness|endpoint|roster"):
        tool.construct(cells, roles, roster, centre, deadline=deadline())


def test_union_different_partners_covers_closed_segment_and_polygon() -> None:
    first = points([(0, 0), (1, 0), (1, 1), (0, 1)])
    second = points([(1, 0), (2, 0), (2, 1), (1, 1)])
    for domain in (points([(0, 0), (2, 0)]), points([(0, 0), (2, 0), (2, 1), (0, 1)])):
        result = tool.cover_piece(domain, {1: first, 2: second}, deadline())
        assert result["covered"] is True
        assert tool.cover_piece(domain, {1: first}, deadline())["covered"] is False


def test_partner_strictness_prevents_false_touch_contradiction() -> None:
    own = tool.core(Q(0), Q(0), strict=False, deadline=deadline())
    strict = tool.core(Q(0), Q(0), strict=True, deadline=deadline())
    region = tool.collision_region(
        [{"domain": points([(2, 1)]), "core": strict}], own, deadline()
    )
    assert not tool.cases.contains(region, (Q(1), Q(1)))
    assert not tool.standing.core_strict(own, Q(0), Q(0))
    # A contact with the owner's CLOSED boundary can be inside a strict partner core.
    region = tool.collision_region(
        [{"domain": points([(2 - tool.MARGIN / 2, 1)]), "core": strict}], own, deadline()
    )
    assert not tool.cases.contains(region, (Q(1), Q(1)))
    region = tool.collision_region(
        [{"domain": points([(2 - 2 * tool.MARGIN, 1)]), "core": strict}], own, deadline()
    )
    assert tool.cases.contains(region, (Q(1), Q(1)))


def test_large_endpoint_scalar_separate_from_geometry_cap() -> None:
    tiny = "1/" + "1" + "0" * 4500
    assert tool.endpoint_rational(tiny) > 0
    with pytest.raises(tool.IncompleteError, match="rational string"):
        tool.finite.rational(tiny)
    with pytest.raises(ValueError, match="grammar"):
        tool.endpoint_rational("1e999999999")
    with pytest.raises(tool.IncompleteError, match="input rational"):
        tool.endpoint_rational("1/" + "1" + "0" * 5100)
    cells, roles, roster, _ = synthetic_state()
    cache: dict[tuple[Q, Q], list[tool.Point]] = {}
    domains = {
        o: [tool.row_domain(r, [0], deadline(), cache) for r in cells[str(o)]]
        for o in roles.values()
    }
    # The huge denominator is used in exact containment but is not retained in output.
    domains[0][0]["domain"] = points([(1, 1), (2, 1), (2, 2), (1, 2)])
    roster[0]["centre"][0] = ["1", "1" + "0" * 4499 + "1/" + "1" + "0" * 4500]
    result = tool.endpoint_control(roster, domains, roles, deadline())
    assert len(result) == 17


def test_support_cache_counts_actual_products_and_facet_ceiling(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    own = tool.core(Q(0), Q(0), strict=False, deadline=deadline())
    body = tool.core(Q(0), Q(0), strict=True, deadline=deadline())
    domain = points([(1, 1), (2, 1)])
    work = tool.new_work()
    list(tool.row_planes(domain, body, own, work))
    count = work["support_vertex_products"]
    list(tool.row_planes(domain, body, own, work))
    assert work["support_vertex_products"] == count
    assert work["generated_facets"] == 4
    assert work["facet_instances_checked"] == 8
    monkeypatch.setattr(tool, "TOTAL_FACETS", 0)
    with pytest.raises(tool.IncompleteError, match="generated facet"):
        list(tool.row_planes(domain, body, own, tool.new_work()))


@pytest.mark.parametrize("mutation", ["node", "step", "owner"])
def test_phase3_reference_binds_actual_node_step_and_owner(mutation: str) -> None:
    raw = rows()
    context = {"node_id": "accepted-original", "step_owners": [1, 2]}
    raw[0]["reference"] = {"kind": "phase3", "node": context["node_id"], "step": 0, "row": 0}
    tool.closed_rows(raw, 1, 64, context)
    if mutation == "node":
        raw[0]["reference"]["node"] = "unaccepted"
    elif mutation == "step":
        raw[0]["reference"]["step"] = -1
    else:
        raw[0]["reference"]["step"] = 1
    with pytest.raises(ValueError, match="phase3"):
        tool.closed_rows(raw, 1, 64, context)


def test_aggregate_hull_cannot_substitute_for_actual_witness_piece() -> None:
    cells, roles, roster, centre = synthetic_state()
    cells["0"][26]["residual_polygons"] = [[["3/4", "1"]], [["5/4", "1"]]]
    with pytest.raises(ValueError, match="individual accepted owner0 piece"):
        tool.construct(cells, roles, roster, centre, deadline=deadline())


def test_fixedpoint_dense_rows_need_no_irrelevant_global_polygon(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cells, roles, roster, centre = synthetic_state()
    for owner in roles.values():
        if owner:
            for row in cells[str(owner)]:
                row["residual_polygons"] = [[["3", "3"]]]
    monkeypatch.setattr(
        tool,
        "collision_region",
        lambda *_: pytest.fail("miss must not construct regional polygons"),
    )
    result = tool.construct(cells, roles, roster, centre, deadline=deadline())
    assert result["status"] == "criterion_missed"
    assert all(
        r["complete_rows_checked"] == (32 if owner == "12" else 64)
        for owner, r in result["fixed_point_partners"].items()
    )
    assert all(
        r["facets_checked"] > 0 and r["first_failed_facet"] is not None
        for r in result["fixed_point_partners"].values()
    )


def test_ascii_endpoint_grammar_and_arithmetic_cap(monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(ValueError, match="ASCII"):
        tool.endpoint_rational("\u0661/\u0662")
    with pytest.raises(ValueError, match="noncanonical"):
        tool.endpoint_rational("2/4")
    monkeypatch.setattr(tool, "ENDPOINT_ARITHMETIC_BITS", 1)
    with pytest.raises(tool.IncompleteError, match="containment arithmetic"):
        tool.endpoint_checked(Q(3, 2))


def test_caps_stop_without_negative_or_positive_verdict(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    core = tool.core(Q(0), Q(0), strict=True, deadline=deadline())
    own = tool.core(Q(0), Q(0), strict=False, deadline=deadline())
    monkeypatch.setattr(tool, "SUPPORT_PRODUCTS", 0)
    with pytest.raises(tool.IncompleteError, match="MIN-support"):
        tool.point_collision(
            [{"domain": points([(1, 1)]), "core": core}],
            own,
            (Q(1), Q(1)),
            tool.new_work(),
            deadline(),
        )
    monkeypatch.setattr(tool, "EDGE_LIMIT", 0)
    with pytest.raises(tool.IncompleteError, match="sweep edge"):
        tool.cover_piece(points([(0, 0), (1, 0)]), {1: points([(0, 0), (1, 0)])}, deadline())


def write_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """Synthetic accepted-premise grammar, not a physical seventeen-square packing."""
    monkeypatch.setattr(tool.finite, "REPO", tmp_path)
    gate, _ = parent_fixture(tmp_path)
    source, union_cert = feasible_fixture()
    chosen = tool.feasible.construct(union_cert, deadline=deadline())["chosen"]["selection"][
        "center"
    ]
    centre = (Q(chosen[0]), Q(chosen[1]))
    cells, roles, roster, _ = synthetic_state()
    for row in cells["0"]:
        row["residual_polygons"] = [tool.finite.serial(points([(1, 1), centre]))]
    gate["label_to_owner"] = roles
    gate["frame"]["cell_names"][5] = "synthetic-5"
    gate["frame"]["cell_names"][12] = "side-S2"
    seed_path, node_path = (
        next((tmp_path / "objects").glob("seed-*")),
        next((tmp_path / "objects").glob("node-*")),
    )
    seed = json.loads(gzip.decompress(seed_path.read_bytes()))
    node = json.loads(gzip.decompress(node_path.read_bytes()))
    order = [o for o in seed["mask"] if o != 12]
    node["steps"] = [{"owner": o} for o in order]
    node["node_id"] = "synthetic-original-node"
    node["final_state"]["cells"] = cells
    seed_id = tool.finite.identity(seed)
    node_id = tool.finite.identity(node)
    compressed = {}
    for kind, value, identity, old_path in (
        ("seed", seed, seed_id, seed_path),
        ("node", node, node_id, node_path),
    ):
        path = tmp_path / "objects" / f"{kind}-{identity}.json.gz"
        path.write_bytes(gzip.compress(tool.finite.canonical(value), mtime=0))
        old_path.unlink()
        compressed[str(path.relative_to(tmp_path))] = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
    gate.update(seed_sha256=seed_id, node_sha256=node_id, compressed_sha256=compressed)
    receipt = json.loads((tmp_path / "h290.json").read_bytes())
    parent = receipt["custody"]["parent_replay"]
    parent.update(
        frame=gate["frame"],
        step_owners=order,
        seed_sha256=seed_id,
        node_sha256=node_id,
        compressed_object_sha256=compressed,
    )
    receipt["custody"]["fresh_replay"]["receipt"] = copy.deepcopy(parent) | {
        "producer_imported": False
    }
    for pose in receipt["custody"]["endpoint_retention"]["owners"]:
        pose["owner"] = roles[str(pose["label"])]
    receipt["custody"]["input_control"]["endpoint_roster"] = roster
    raw = json.dumps(receipt, sort_keys=True).encode()
    (tmp_path / "h290.json").write_bytes(raw)
    gate["h290_receipt_sha256"] = hashlib.sha256(raw).hexdigest()

    def retain(name: str, value: dict[str, Any]) -> tuple[str, str]:
        raw = json.dumps(value, sort_keys=True).encode()
        path = tmp_path / f"{name}.json"
        path.write_bytes(raw)
        return path.name, hashlib.sha256(raw).hexdigest()

    context = tool.standing.CenteredContainer(tool.cases.U, tool.cases.V).record()
    centered = {
        "schema": "n17-centered-cap-standing-context/v1",
        "status": "centered_stall_control_checked",
        "readiness_passed": True,
        "verification_passed": True,
        "accepted_context": {"accepted_endpoint": {"sha256": gate["h290_receipt_sha256"]}},
        "fresh_standing": {
            "exit_code": 0,
            "receipt": {
                "schema": tool.standing.CENTERED_SCHEMA,
                "mode": "full",
                "status": "PASS_STALL",
                "independent_modules": True,
                "root_cap_join_checked": False,
                "owned_hull_limit": 48,
                "container": context,
                "certificate": {"seed_sha256": seed_id, "node_sha256": node_id},
                "compressed_sha256": tool.cases.conditional.parent_compressed_roles(gate),
                "mask": seed["mask"],
                "counts": {"steps": 16},
                "closed": False,
                "closure": None,
            },
        },
    }
    doc: dict[str, Any] = {"schema": tool.DESCRIPTOR_SCHEMA}
    for role, value in (("parent_descriptor", gate), ("centered_receipt", centered)):
        doc[role], doc[role + "_sha256"] = retain(role, value)
    expected_parent = {
        "schema": "accepted-centered-parent/v1",
        "seed_sha256": seed_id,
        "node_sha256": node_id,
        "compressed_sha256": compressed,
        "h290_receipt": gate["h290_receipt"],
        "h290_receipt_sha256": gate["h290_receipt_sha256"],
        "centered_parent_receipt": doc["centered_receipt"],
        "centered_parent_receipt_sha256": doc["centered_receipt_sha256"],
    }
    union_cert["custody"]["parent"] = expected_parent
    union_cert["custody"]["proof_pool"].update(node_sha256=node_id, seed_sha256=seed_id)
    feasible_doc: dict[str, Any] = {"schema": tool.feasible.DESCRIPTOR_SCHEMA}
    previous_doc: dict[str, Any] = {"schema": tool.feasible.witness.DESCRIPTOR_SCHEMA}
    for role, value in zip(
        tool.feasible.witness.INPUTS,
        (source, union_cert, union_cert | {"verification_passed": True}),
        strict=True,
    ):
        name, digest = retain(role, value)
        for target in (feasible_doc, previous_doc):
            target[role], target[role + "_sha256"] = name, digest
    previous = tool.feasible.witness.generate(previous_doc, deadline=deadline())
    for role, value in zip(
        tool.feasible.INPUTS[3:],
        (previous_doc, previous, previous | {"verification_passed": True}),
        strict=True,
    ):
        feasible_doc[role], feasible_doc[role + "_sha256"] = retain(role, value)
    certificate = tool.feasible.generate(feasible_doc, deadline=deadline())
    for role, value in (
        ("feasible_descriptor", feasible_doc),
        ("feasible_certificate", certificate),
        ("feasible_replay", certificate | {"verification_passed": True}),
    ):
        doc[role], doc[role + "_sha256"] = retain(role, value)
    return doc


def test_full_intake_and_exact_roundtrip_tamper(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = write_fixture(tmp_path, monkeypatch)
    certificate = tool.generate(doc, deadline=deadline())
    assert certificate["status"] == "criterion_missed"
    assert certificate["foreign_rows_checked"] == 992
    assert not certificate["parent_geometry_replayed"]
    decoded = tool.finite.decode(tool.retained_json.dumps(certificate).encode())
    fresh = tool.check(doc, decoded, deadline=deadline())
    assert fresh["verification_passed"] is True
    decoded["rows"]["1"][0]["interval"][0] = "1/1000"
    with pytest.raises(ValueError, match="reconstruction differs"):
        tool.check(doc, decoded, deadline=deadline())


@pytest.mark.parametrize(
    "kind", ["digest", "role", "centered", "feasible_parent", "compressed"]
)
def test_intake_custody_mismatch_refuses(
    kind: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = write_fixture(tmp_path, monkeypatch)
    if kind == "digest":
        doc["parent_descriptor_sha256"] = "f" * 64
    elif kind == "role":
        doc["extra"] = "unsupported"
    elif kind in ("centered", "feasible_parent"):
        role = "centered_receipt" if kind == "centered" else "feasible_certificate"
        path = tmp_path / doc[role]
        value = json.loads(path.read_bytes())
        if kind == "centered":
            value["fresh_standing"]["receipt"]["container"]["inner_V"] = "1"
        else:
            value["parent"]["node_sha256"] = "f" * 64
        raw = json.dumps(value).encode()
        path.write_bytes(raw)
        doc[role + "_sha256"] = hashlib.sha256(raw).hexdigest()
    else:
        node_path = next((tmp_path / "objects").glob("node-*"))
        node_path.write_bytes(node_path.read_bytes() + b"tampered")
    with pytest.raises(ValueError, match=r"identity|schema|differ|payload|premise|required"):
        tool.generate(doc, deadline=deadline())


def test_two_fresh_clean_cli_processes_reconstruct_same_payload(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = write_fixture(tmp_path, monkeypatch)
    descriptor = tmp_path / "coupling.json"
    descriptor.write_text(json.dumps(doc))
    outputs = [tmp_path / "generated.json", tmp_path / "checked.json"]
    code = (
        "from pathlib import Path; import sys; "
        "from devtools import check_n17_partner_pose_coupling as t; "
        "t.finite.REPO=Path(sys.argv[1]); raise SystemExit(t.main(sys.argv[2:]))"
    )
    for index, output in enumerate(outputs):
        args = [
            sys.executable,
            "-c",
            code,
            str(tmp_path),
            "--descriptor",
            str(descriptor),
            "--max-seconds",
            "30",
            "--output",
            str(output),
        ]
        if index:
            args.extend(["--certificate", str(outputs[0])])
        result = subprocess.run(args, capture_output=True, text=True, timeout=40, check=False)
        assert result.returncode == 0, result.stderr
    first, second = (json.loads(p.read_bytes()) for p in outputs)
    assert tool.feasible.witness.payload(first) == tool.feasible.witness.payload(second)
    assert second["verification_passed"] is True
    assert first["invocation"] != second["invocation"]
    assert all(first[key] is False for key in tool.scope())


def test_input_mutation_during_construction_refuses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = write_fixture(tmp_path, monkeypatch)
    original = tool.construct

    def mutate(*args: Any, **kwargs: Any) -> dict[str, Any]:
        result = original(*args, **kwargs)
        node_path = next((tmp_path / "objects").glob("node-*"))
        node_path.write_bytes(node_path.read_bytes() + b"changed")
        return result

    monkeypatch.setattr(tool, "construct", mutate)
    with pytest.raises(ValueError, match="coupling inputs changed"):
        tool.generate(doc, deadline=deadline())


@pytest.mark.parametrize("kind", ["expired", "wrong_descriptor", "output_cap"])
def test_cli_retains_incomplete_or_refused_scoped_receipt(
    kind: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = write_fixture(tmp_path, monkeypatch)
    if kind == "wrong_descriptor":
        doc["schema"] = "wrong"
    descriptor = tmp_path / "input.json"
    descriptor.write_text(json.dumps(doc))
    output = tmp_path / "receipt.json"
    seconds = "0.000001" if kind == "expired" else "30"
    if kind == "output_cap":
        monkeypatch.setattr(tool, "OUTPUT_LIMIT", 1)
    assert (
        tool.main(
            ["--descriptor", str(descriptor), "--max-seconds", seconds, "--output", str(output)]
        )
        == 1
    )
    result = json.loads(output.read_bytes())
    assert result["status"] == ("refused" if kind == "wrong_descriptor" else "incomplete")
    assert result["criterion_met"] is False
    assert all(result[key] is False for key in tool.scope())
    monkeypatch.setattr(tool, "INPUT_VERTICES", 0)
    raw = copy.deepcopy(rows()[0])
    raw["residual_polygons"] = [[["1", "1"]]]
    with pytest.raises(tool.IncompleteError):
        tool.row_domain(raw, [0], deadline())
