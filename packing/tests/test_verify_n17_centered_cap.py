"""Target-free standalone centered-wall proof controls; no accepted root is read."""

from __future__ import annotations

import copy
import gzip
import hashlib
import json
import subprocess
import sys
from dataclasses import FrozenInstanceError
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

import pytest

from devtools import verify_n17_kernel_certificate as verifier


def fixture(
    directory: Path, *, closed: bool = False
) -> tuple[verifier.Cells, verifier.CenteredContainer, dict[str, Any], dict[str, Any]]:
    """Synthetic24-cell/17-owner restriction, not the actual cover or a packing."""
    context = verifier.CenteredContainer(Q(4), Q(3))
    polygons = tuple(
        tuple(
            (x, y)
            for x, y in (
                (a, a),
                (a + Q(1, 10), a),
                (a + Q(1, 10), a + Q(1, 10)),
                (a, a + Q(1, 10)),
            )
        )
        for a in (Q(3, 5) if closed else Q(3, 2),) + (Q(3, 2),) * 23
    )
    cells = verifier.Cells(
        tuple(f"synthetic-{i}" for i in range(24)), polygons, Q(4), {"kind": "synthetic"}
    )
    world = [[[str(x), str(y)] for x, y in p] for p in polygons]
    groups = {str(i): [] for i in range(17)}
    rows = {}
    for owner in range(17):
        domain = verifier.intersect_convex(
            list(polygons[owner]), verifier.wall_box(Q(0), Q(1), Q(4), container=context)
        )
        encoded = [[str(x), str(y)] for x, y in domain]
        rows[str(owner)] = [
            {
                "interval": ["0", "1"],
                "reference": {"kind": "wall_seed", "owner": owner, "row": 0},
                "outer_domain": encoded,
                "outer_bounds": [],
                "residual_polygons": [encoded] if encoded else [],
            }
        ]
    seed = {
        "schema": "generic_wall_seed_v1",
        "U": "4",
        "B": "1",
        "mask_index": None,
        "mask": list(range(17)),
        "bins": 1,
        "groups": groups,
        "cells": rows,
        "world": world,
    }
    source = {"sha256": hashlib.sha256(verifier.canonical(seed)).hexdigest()}
    final_rows = copy.deepcopy(rows)
    steps = []
    contradiction = None
    if closed:
        reference = {"kind": "phase3", "node": "synthetic", "step": 0, "row": 0}
        row = {
            **copy.deepcopy(rows["0"][0]),
            "reference": reference,
            "prior_reference": rows["0"][0]["reference"],
            "collision_regions": [],
            "common_core_halfplanes": [],
            "self_hull_cuts": [],
        }
        steps.append(
            {
                "index": 0,
                "owner": 0,
                "complete": True,
                "allowed_half_angle": ["0", "1"],
                "prior_owned_hulls": copy.deepcopy(groups),
                "prior_partner_pose_covers": {},
                "rows": [row],
                "common_owned_kernel": [],
            }
        )
        final_rows["0"][0]["reference"] = reference
        contradiction = {"kind": "all_parent_poses_forbidden", "owner": 0, "step": 0}
    node = {
        "schema": "exact_generic_owned_hull_v1",
        "node_id": "synthetic",
        "U": "4",
        "B": "1",
        "mask_index": None,
        "mask": list(range(17)),
        "parent": None,
        "guard_source": None,
        "constraints": [],
        "source": source,
        "initial": {
            "groups": copy.deepcopy(groups),
            "cell_references": {
                str(i): [r["reference"] for r in rows[str(i)]] for i in range(17)
            },
        },
        "steps": steps,
        "contradiction": contradiction,
        "closed": closed,
        "terminal": closed,
        "mask_exclusion_proved": False,
        "global_optimality_proved": False,
        "final_state": {
            "groups": copy.deepcopy(groups),
            "cells": final_rows,
            "mask_index": None,
            "mask": list(range(17)),
            "U": "4",
            "B": "1",
            "constraints": [],
            "guard": {},
            "guard_source": None,
            "source": source,
            "world": world,
        },
    }
    save(directory, seed, node)
    return cells, context, seed, node


def save(directory: Path, seed: dict[str, Any], node: dict[str, Any]) -> None:
    directory.mkdir(exist_ok=True)
    for kind, obj in (("seed", seed), ("node", node)):
        (directory / f"{kind}-synthetic.json.gz").write_bytes(
            gzip.compress(verifier.canonical(obj), mtime=0)
        )


@pytest.mark.parametrize(
    "interval", [(Q(0), Q(0)), (Q(1), Q(1)), (Q(1, 4), Q(3, 4)), (Q(0), Q(1))]
)
def test_equal_caps_recover_exact_default_walls(interval: tuple[Q, Q]) -> None:
    context = verifier.CenteredContainer(Q(4), Q(4))
    assert context.offset == 0
    assert verifier.wall_box(*interval, Q(4), container=context) == verifier.wall_box(
        *interval, Q(4)
    )


def test_offset_is_derived_and_context_immutable() -> None:
    context = verifier.CenteredContainer(Q(4), Q(3))
    assert context.offset == Q(1, 2)
    assert verifier.wall_box(Q(0), Q(1), Q(4), container=context) == [
        (Q(1), Q(1)),
        (Q(3), Q(1)),
        (Q(3), Q(3)),
        (Q(1), Q(3)),
    ]
    with pytest.raises(FrozenInstanceError):
        context.inner = Q(2)  # pyright: ignore[reportAttributeAccessIssue]
    with pytest.raises(verifier.VerificationError, match="outer cap"):
        verifier.wall_box(Q(0), Q(1), Q(3), container=context)
    with pytest.raises(verifier.VerificationError, match="invalid"):
        verifier.CenteredContainer(Q(3), Q(4))
    assert (
        verifier.wall_box(Q(0), Q(1), Q(4), container=verifier.CenteredContainer(Q(4), Q(1, 2)))
        == []
    )


def test_owned_recursion_keeps_the_context(monkeypatch: pytest.MonkeyPatch) -> None:
    context = verifier.CenteredContainer(Q(4), Q(3))
    original = verifier.wall_box
    calls = []

    def walls(lo: Q, hi: Q, cap: Q, *, container: Any = None) -> list[verifier.Point]:
        calls.append((lo, hi, container))
        return original(lo, hi, cap, container=container)

    monkeypatch.setattr(verifier, "wall_box", walls)
    assert not verifier.owned(
        [(Q(1), Q(1)), (Q(2), Q(1)), (Q(2), Q(2)), (Q(1), Q(2))],
        (Q(3, 2), Q(3, 2)),
        Q(4),
        depth=17,
        container=context,
    )
    assert len(calls) >= 2
    assert all(c is context for _, _, c in calls)


def test_empty_centered_walls_propagate_to_owned_seed_and_updated_rows(tmp_path: Path) -> None:
    cells, _context, seed, node = fixture(tmp_path)
    context = verifier.CenteredContainer(Q(4), Q(1, 2))
    assert verifier.owned(list(cells.polygons[0]), (Q(100), Q(100)), Q(4), container=context)
    for rows in seed["cells"].values():
        rows[0]["outer_domain"] = []
        rows[0]["residual_polygons"] = []
    state = verifier.State(
        [list(p) for p in cells.polygons], Q(4), 1, list(range(17)), container=context
    )
    verifier.check_seed(state, seed, node)
    assert all(row.outer == [] for rows in state.rows.values() for row in rows)
    reference = seed["cells"]["0"][0]["reference"]
    state.rows[0] = [
        verifier.Row(
            (Q(0), Q(1)), reference, list(cells.polygons[0]), [list(cells.polygons[0])]
        )
    ]
    row = {
        "interval": ["0", "1"],
        "reference": {"kind": "phase3", "node": "synthetic", "step": 0, "row": 0},
        "prior_reference": reference,
        "residual_polygons": [],
        "outer_domain": [],
        "outer_bounds": [],
        "collision_regions": [],
        "common_core_halfplanes": [],
    }
    updated, _planes, live = verifier.check_step(
        state, {"owner": 0, "rows": [row], "prior_partner_pose_covers": {}}, 0, "synthetic", {0}
    )
    assert not live
    assert updated[0].outer == []


def test_complete_full17_stall_has_separate_schema_and_default_parity(tmp_path: Path) -> None:
    cells, context, _seed, _node = fixture(tmp_path)
    default = verifier.verify(tmp_path, cells)
    centered = verifier.verify(tmp_path, cells, container=context)
    equal = verifier.verify(tmp_path, cells, container=verifier.CenteredContainer(Q(4), Q(4)))
    assert default["schema"] == verifier.SCHEMA
    assert default["status"] == "FAIL"
    assert centered["schema"] != default["schema"]
    assert centered["status"] == equal["status"] == "PASS_STALL"
    assert centered["certificate"] == equal["certificate"] == default["certificate"]
    assert centered["counts"] == equal["counts"] == default["counts"]
    assert centered["root_cap_join_checked"] is False
    assert centered["centered_exclusion_proved"] is False
    assert centered["existing_U_census_admission"] is False


def test_numeric_wall_closure_cannot_be_reused_at_outer_cap(tmp_path: Path) -> None:
    cells, context, _seed, _node = fixture(tmp_path, closed=True)
    result = verifier.verify(tmp_path, cells, container=context)
    assert result["status"] == "PASS_CLOSED", result.get("failure")
    assert result["centered_exclusion_proved"] is True
    assert result["container"]["offset"] == "1/2"
    assert verifier.verify(tmp_path, cells)["status"] == "FAIL"
    sampled = verifier.verify(tmp_path, cells, container=context, sample=1)
    assert sampled["status"] == "FAIL"
    assert sampled["centered_exclusion_proved"] is False


def test_existing_u_census_refuses_even_a_claimed_pass_centered_receipt(tmp_path: Path) -> None:
    from devtools import census_n17_certified as census  # noqa: PLC0415

    cells, context, _seed, _node = fixture(tmp_path, closed=True)
    receipt = verifier.verify(tmp_path, cells, container=context)
    receipt["status"] = "PASS"
    (tmp_path / "receipt.json").write_text(json.dumps(receipt))
    entry = {"certifier": "kernel", "verification": {"receipt": "receipt.json", "verifier": {}}}
    with pytest.raises(census.RefusedError, match="not a kernel verification receipt"):
        census.check_verification(
            cast(census.Cover, None), entry, (tmp_path, {}, 0, []), "synthetic"
        )


@pytest.mark.parametrize(
    "field",
    [
        "U",
        "B",
        "mask",
        "mask_index",
        "source",
        "world",
        "guard",
        "guard_source",
        "constraints",
        "interval",
        "extra_owner",
    ],
)
def test_new_mode_rejects_final_context_mutations(field: str, tmp_path: Path) -> None:
    cells, context, seed, node = fixture(tmp_path)
    final = node["final_state"]
    if field in {"U", "B"}:
        final[field] = "2"
    elif field == "interval":
        final["cells"]["0"][0]["interval"] = ["0", "1/2"]
    elif field == "extra_owner":
        final["groups"]["23"] = []
    elif field == "world":
        final[field] = final[field][:-1]
    else:
        final[field] = {"foreign": True}
    save(tmp_path, seed, node)
    result = verifier.verify(tmp_path, cells, container=context)
    assert result["status"] == "FAIL"
    assert result["centered_exclusion_proved"] is False


def test_exact_closure_owner_list_join(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cells, context, _seed, _node = fixture(tmp_path, closed=True)
    monkeypatch.setattr(
        verifier,
        "derive_closure",
        lambda *_: {
            "kind": "all_parent_poses_forbidden",
            "owner": 0,
            "step": 0,
            "owners": [0, 1],
        },
    )
    assert verifier.verify(tmp_path, cells, container=context)["status"] == "FAIL"


def test_two_actual_owned_hulls_require_the_exact_declared_pair(tmp_path: Path) -> None:
    cells, context, seed, node = fixture(tmp_path)
    owned = [
        [str(x), str(y)]
        for x, y in verifier.hull(
            [(Q(3, 2), Q(3, 2)), (Q(49, 32), Q(3, 2)), (Q(3, 2), Q(49, 32))]
        )
    ]
    for owner in ("0", "1"):
        seed["groups"][owner] = copy.deepcopy(owned)
    source = {"sha256": hashlib.sha256(verifier.canonical(seed)).hexdigest()}
    node["source"] = source
    node["initial"]["groups"] = copy.deepcopy(seed["groups"])
    node["final_state"]["groups"] = copy.deepcopy(seed["groups"])
    node["final_state"]["source"] = source
    prior = seed["cells"]["0"][0]
    vertices = verifier.poly(prior["outer_domain"])
    core = [
        (Q(-1, 10), Q(-1, 10)),
        (Q(1, 10), Q(-1, 10)),
        (Q(1, 10), Q(1, 10)),
        (Q(-1, 10), Q(1, 10)),
    ]
    planes = []
    for p, q in zip(core, core[1:] + core[:1], strict=True):
        a, b = q[1] - p[1], p[0] - q[0]
        planes.append((a, b, a * p[0] + b * p[1] + min(a * v[0] + b * v[1] for v in vertices)))
    reference = {"kind": "phase3", "node": "synthetic", "step": 0, "row": 0}

    def encoded_planes(items: list[verifier.Plane]) -> list[dict[str, Any]]:
        return [{"normal": [str(a), str(b)], "upper": str(c)} for a, b, c in items]

    row = {
        **copy.deepcopy(prior),
        "reference": reference,
        "prior_reference": prior["reference"],
        "collision_regions": [],
        "self_hull_cuts": [],
        "core_vertices": [[str(x), str(y)] for x, y in core],
        "common_core_halfplanes": encoded_planes(planes),
        "outer_bounds": encoded_planes(verifier.planes_of(vertices) * 2),
    }
    node["steps"] = [
        {
            "index": 0,
            "owner": 0,
            "complete": True,
            "allowed_half_angle": ["0", "1"],
            "prior_owned_hulls": copy.deepcopy(seed["groups"]),
            "prior_partner_pose_covers": {},
            "rows": [row],
            "common_owned_kernel": [],
            "compression_source_hull": copy.deepcopy(owned),
            "inner_grid_compression": {
                "mode": "replace",
                "vertices": copy.deepcopy(owned),
                "witnesses": [
                    {"indices": [i], "weights": ["1"], "point": pt}
                    for i, pt in enumerate(owned)
                ],
            },
        }
    ]
    node["final_state"]["cells"]["0"][0]["reference"] = reference
    node["contradiction"] = {"kind": "owned_hulls_intersect", "owners": [0, 1], "step": 0}
    node["closed"] = node["terminal"] = True
    save(tmp_path, seed, node)
    accepted = verifier.verify(tmp_path, cells, container=context)
    assert accepted["status"] == "PASS_CLOSED", accepted.get("failure")
    assert verifier.verify(tmp_path, cells)["status"] == "PASS"
    node["contradiction"]["owners"] = [0, 2]
    save(tmp_path, seed, node)
    refused = verifier.verify(tmp_path, cells, container=context)
    assert refused["status"] == "FAIL"
    assert "centered closure identities" in refused["failure"]


def test_updated_rows_use_inner_walls_even_for_a_loose_prior_outer(tmp_path: Path) -> None:
    cells, context, seed, _node = fixture(tmp_path, closed=True)
    polygon = list(cells.polygons[0])
    reference = seed["cells"]["0"][0]["reference"]
    state = verifier.State(
        [list(p) for p in cells.polygons], Q(4), 1, list(range(17)), container=context
    )
    state.groups = {i: [] for i in state.mask}
    state.rows = {
        i: [verifier.Row((Q(0), Q(1)), reference, polygon, [polygon])] for i in state.mask
    }
    row = {
        "interval": ["0", "1"],
        "reference": {"kind": "phase3", "node": "synthetic", "step": 0, "row": 0},
        "prior_reference": reference,
        "residual_polygons": [],
        "outer_domain": [],
        "outer_bounds": [],
        "collision_regions": [],
        "common_core_halfplanes": [],
    }
    step = {"owner": 0, "rows": [row], "prior_partner_pose_covers": {}}
    updated, _planes, live = verifier.check_step(state, step, 0, "synthetic", {0})
    assert not live
    assert updated[0].outer == []
    state.container = None
    with pytest.raises(KeyError, match="core_vertices"):
        verifier.check_step(state, step, 0, "synthetic", {0})


@pytest.mark.parametrize("mutation", ["outer_substitution", "trailing_json", "partial_gzip"])
def test_changed_frame_or_incomplete_stream_is_never_accepted(
    mutation: str, tmp_path: Path
) -> None:
    cells, context, seed, node = fixture(tmp_path)
    if mutation == "outer_substitution":
        seed["U"] = node["U"] = "3"
        save(tmp_path, seed, node)
    else:
        path = tmp_path / "node-synthetic.json.gz"
        if mutation == "trailing_json":
            path.write_bytes(gzip.compress(verifier.canonical(node) + b"{}"))
        else:
            path.write_bytes(path.read_bytes()[:-8])
    result = verifier.verify(tmp_path, cells, container=context)
    assert result["status"] == "FAIL"
    assert result["centered_exclusion_proved"] is False


def test_fresh_centered_cli_stays_producer_free(tmp_path: Path) -> None:
    cells, _context, _seed, _node = fixture(tmp_path)
    cell_path, output = tmp_path / "cells.json", tmp_path / "receipt.json"
    cell_path.write_text(
        json.dumps(
            {
                "U": "4",
                "order": list(cells.names),
                "cells": {
                    name: [[str(x), str(y)] for x, y in polygon]
                    for name, polygon in zip(cells.names, cells.polygons, strict=True)
                },
            }
        )
    )
    script = """import sys
from devtools import verify_n17_kernel_certificate as v
code=v.main(sys.argv[1:])
assert not any(name.startswith('sqpack.hull_kernel') for name in sys.modules)
assert 'devtools.pilot_n17_capture' not in sys.modules
raise SystemExit(code)
"""
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            script,
            str(tmp_path),
            "--cells",
            str(cell_path),
            "--cells-sha256",
            hashlib.sha256(cell_path.read_bytes()).hexdigest(),
            "--centered-inner-cap",
            "3",
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    receipt = json.loads(output.read_text())
    assert receipt["status"] == "PASS_STALL"
    assert receipt["schema"] == verifier.CENTERED_SCHEMA
    assert receipt["root_cap_join_checked"] is False
