"""Synthetic accepted-shape dependency controls; no scientific certificate target."""

from __future__ import annotations

import copy
import gzip
import json
import subprocess
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest

from devtools import audit_n17_certificate_dependencies as audit
from devtools import audit_n17_endpoint_receipt as exact
from sqpack import retained_json

TRIANGLE = [["0", "0"], ["1", "0"], ["0", "1"]]


def fixture(
    *,
    groups: tuple[bool, bool, bool] = (False, False, False),
    supplied: tuple[int, ...] = (),
    cited: tuple[int, ...] = (),
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], audit.standing.Cells]:
    cells = audit.standing.Cells(
        ("A", "B", "C"),
        tuple(tuple((Q(x), Q(y)) for x, y in TRIANGLE) for _ in range(3)),
        Q(5),
        {"kind": "synthetic-closed-world"},
    )
    seed_rows = {
        str(i): [
            {
                "interval": ["0", "1"],
                "reference": {"kind": "wall_seed", "owner": i, "row": 0},
                "outer_domain": copy.deepcopy(TRIANGLE),
                "residual_polygons": [copy.deepcopy(TRIANGLE)],
            }
        ]
        for i in range(3)
    }
    seed = {
        "schema": "generic_wall_seed_v1",
        "U": "5",
        "B": "1",
        "mask": [0, 1, 2],
        "bins": 1,
        "world": [copy.deepcopy(TRIANGLE) for _ in range(3)],
        "groups": {str(i): [["0", "0"]] if live else [] for i, live in enumerate(groups)},
        "cells": seed_rows,
    }
    new = {
        "interval": ["0", "1"],
        "reference": {"kind": "phase3", "node": "synthetic", "step": 0, "row": 0},
        "prior_reference": seed_rows["0"][0]["reference"],
        "outer_domain": [],
        "residual_polygons": [],
        "collision_regions": [
            {"partner": p, "vertices": copy.deepcopy(TRIANGLE)} for p in cited
        ],
        "self_hull_cuts": [],
        "common_core_halfplanes": [],
        "outer_bounds": [],
        "core_vertices": copy.deepcopy(TRIANGLE),
    }
    step = {
        "index": 0,
        "owner": 0,
        "complete": True,
        "allowed_half_angle": ["0", "1"],
        "prior_owned_hulls": copy.deepcopy(seed["groups"]),
        "prior_partner_pose_covers": {
            str(i): [
                {
                    "reference": seed_rows[str(i)][0]["reference"],
                    "interval": ["0", "1"],
                    "domain": copy.deepcopy(TRIANGLE),
                    "core": copy.deepcopy(TRIANGLE),
                }
            ]
            for i in supplied
        },
        "rows": [new],
        "common_owned_kernel": [],
    }
    node = {
        "schema": "exact_generic_owned_hull_v1",
        "U": "5",
        "B": "1",
        "mask": [0, 1, 2],
        "node_id": "synthetic",
        "source": {"sha256": audit.saved.content_sha256(seed)},
        "parent": None,
        "guard_source": None,
        "constraints": [],
        "initial": {
            "groups": copy.deepcopy(seed["groups"]),
            "cell_references": {str(i): [seed_rows[str(i)][0]["reference"]] for i in range(3)},
        },
        "steps": [step],
        "contradiction": {"kind": "all_parent_poses_forbidden", "owner": 0, "step": 0},
        "final_state": {
            "groups": copy.deepcopy(seed["groups"]),
            "cells": {**copy.deepcopy(seed_rows), "0": [copy.deepcopy(new)]},
        },
    }
    receipt = {
        "schema": audit.standing.SCHEMA,
        "verifier": "kernel",
        "status": "PASS",
        "mode": "full",
        "sample_rows_per_step": None,
        "sample_seed": None,
        "closed": True,
        "failure": None,
        "certificate": {
            "seed_sha256": audit.saved.content_sha256(seed),
            "node_sha256": audit.saved.content_sha256(node),
        },
        "mask": [0, 1, 2],
        "cells": ["A", "B", "C"],
        "bins": 1,
        "cells_source": cells.source,
        "closure": copy.deepcopy(node["contradiction"]),
        "counts": {"steps": 1},
    }
    return seed, node, receipt, cells


def run(
    data: tuple[dict[str, Any], dict[str, Any], dict[str, Any], audit.standing.Cells],
) -> dict[str, Any]:
    seed, node, receipt, cells = data
    return audit.inventory(
        seed, node, node["steps"], receipt, cells, deadline=time.monotonic() + 20
    )


def rebind(
    data: tuple[dict[str, Any], dict[str, Any], dict[str, Any], audit.standing.Cells],
) -> None:
    seed, node, receipt, _ = data
    node["source"]["sha256"] = receipt["certificate"]["seed_sha256"] = (
        audit.saved.content_sha256(seed)
    )
    receipt["certificate"]["node_sha256"] = audit.saved.content_sha256(node)
    receipt["closure"] = copy.deepcopy(node["contradiction"])
    receipt["counts"]["steps"] = len(node["steps"])


def test_implicit_hull_not_named_in_partner_map_still_propagates() -> None:
    result = run(fixture(groups=(False, True, False)))
    assert result["geometric_owner_set"] == [0, 1]
    assert result["strict_subset_proposal"] is True
    row = next(f for f in result["dag"] if f["kind"] == "updated_row")
    assert any(
        e["reason"] == "implicit_nonempty_foreign_hull"
        for e in row["geometric_dependencies"]["edges"]
    )


def test_unused_supplied_partner_is_validation_only() -> None:
    result = run(fixture(supplied=(1,)))
    assert result["geometric_owner_set"] == [0]
    assert result["validation_owner_set"] == [0, 1]
    assert result["inventory_complete"] is True
    assert all(result[name] is False for name in audit.FALSE_FLAGS)
    assert result["frame"]["world_cell_names"] == ["A", "B", "C"]


def test_cited_partner_propagates_entire_current_roster() -> None:
    result = run(fixture(supplied=(1,), cited=(1,)))
    assert result["geometric_owner_set"] == [0, 1]
    row = next(f for f in result["dag"] if f["kind"] == "updated_row")
    assert any(
        e["reason"] == "explicit_collision_full_partner_cover"
        for e in row["geometric_dependencies"]["edges"]
    )


def test_empty_hull_has_presence_but_no_foreign_forbidden_edge() -> None:
    result = run(fixture())
    assert result["geometric_owner_set"] == [0]
    assert result["typed_fact_counts"]["seed_owned_hull"] == 3
    assert result["typed_fact_counts"]["owner_presence"] == 3
    row = next(f for f in result["dag"] if f["kind"] == "updated_row")
    assert all(
        edge["reason"] != "own_hull_conservative"
        for edge in row["geometric_dependencies"]["edges"]
    )


def test_full_owner_no_reduction_is_honest() -> None:
    result = run(fixture(groups=(True, True, True)))
    assert result["geometric_owner_set"] == [0, 1, 2]
    assert result["strict_subset_proposal"] is False


def test_transitive_predecessor_and_replace_hull_carry() -> None:
    data = fixture(supplied=(1,), cited=(1,))
    seed, node, _, _ = data
    first = node["steps"][0]
    first["rows"][0]["outer_domain"] = copy.deepcopy(TRIANGLE)
    first["rows"][0]["residual_polygons"] = [copy.deepcopy(TRIANGLE)]
    first["common_owned_kernel"] = [["0", "0"]]
    first["inner_grid_compression"] = {"mode": "replace", "vertices": [["0", "0"]]}
    second = copy.deepcopy(first)
    second.update(
        index=1,
        prior_owned_hulls={**copy.deepcopy(seed["groups"]), "0": [["0", "0"]]},
        prior_partner_pose_covers={},
        common_owned_kernel=[],
    )
    second.pop("inner_grid_compression")
    second["rows"][0].update(
        reference={"kind": "phase3", "node": "synthetic", "step": 1, "row": 0},
        prior_reference=first["rows"][0]["reference"],
        residual_polygons=[],
        outer_domain=[],
        collision_regions=[],
    )
    node["steps"].append(second)
    node["contradiction"]["step"] = 1
    node["final_state"]["groups"]["0"] = [["0", "0"]]
    node["final_state"]["cells"]["0"] = [copy.deepcopy(second["rows"][0])]
    rebind(data)
    result = run(data)
    assert result["geometric_owner_set"] == [0, 1]
    hull = next(f for f in result["dag"] if f["id"] == "hull:0:0")
    assert hull["mode"] == "replace"
    assert any(
        e["reason"] == "compression_old_hull_including_replace"
        for e in hull["geometric_dependencies"]["edges"]
    )


def test_two_hull_closure_union() -> None:
    data = fixture(groups=(True, False, True))
    _, node, _, _ = data
    data[0]["groups"]["2"] = copy.deepcopy(TRIANGLE)
    node["initial"]["groups"]["2"] = copy.deepcopy(TRIANGLE)
    node["steps"][0]["prior_owned_hulls"]["2"] = copy.deepcopy(TRIANGLE)
    node["final_state"]["groups"]["2"] = copy.deepcopy(TRIANGLE)
    node["steps"][0]["rows"][0].update(
        outer_domain=copy.deepcopy(TRIANGLE), residual_polygons=[copy.deepcopy(TRIANGLE)]
    )
    node["final_state"]["cells"]["0"] = copy.deepcopy(node["steps"][0]["rows"])
    node["contradiction"] = {"kind": "owned_hulls_intersect", "owners": [0, 2], "step": 0}
    rebind(data)
    assert run(data)["geometric_owner_set"] == [0, 2]


@pytest.mark.parametrize("mutation", ["wrong_pair", "no_intersection"])
def test_declared_two_hull_pair_is_independently_bound(mutation: str) -> None:
    data = fixture(groups=(True, False, True))
    node = data[1]
    node["contradiction"] = {
        "kind": "owned_hulls_intersect",
        "owners": [1, 2] if mutation == "wrong_pair" else [0, 2],
        "step": 0,
    }
    rebind(data)
    with pytest.raises(exact.AuditError, match="closure"):
        run(data)


def test_factored_full_cover_equals_unfactored_transitive_owner_sets() -> None:
    data = fixture(supplied=(1, 2), cited=(1,))
    seed, node, receipt, _ = data
    seed["bins"] = receipt["bins"] = 2
    for owner in range(3):
        old = seed["cells"][str(owner)][0]
        seed["cells"][str(owner)] = []
        for index, interval in enumerate((["0", "1/2"], ["1/2", "1"])):
            row = copy.deepcopy(old)
            row.update(
                interval=interval, reference={"kind": "wall_seed", "owner": owner, "row": index}
            )
            seed["cells"][str(owner)].append(row)
        node["initial"]["cell_references"][str(owner)] = [
            r["reference"] for r in seed["cells"][str(owner)]
        ]
    step = node["steps"][0]
    old = step["rows"][0]
    step["rows"] = []
    for index, row in enumerate(seed["cells"]["0"]):
        new = copy.deepcopy(old)
        new.update(
            interval=row["interval"],
            reference={"kind": "phase3", "node": "synthetic", "step": 0, "row": index},
            prior_reference=row["reference"],
        )
        step["rows"].append(new)
    for owner in (1, 2):
        step["prior_partner_pose_covers"][str(owner)] = [
            {
                "reference": r["reference"],
                "interval": r["interval"],
                "domain": copy.deepcopy(TRIANGLE),
                "core": copy.deepcopy(TRIANGLE),
            }
            for r in seed["cells"][str(owner)]
        ]
    node["final_state"]["cells"] = {
        **copy.deepcopy(seed["cells"]),
        "0": copy.deepcopy(step["rows"]),
    }
    rebind(data)
    result = run(data)
    facts = {fact["id"]: fact for fact in result["dag"]}
    for channel, partners in (
        ("geometric_dependencies", (1,)),
        ("validation_dependencies", (1, 2)),
    ):
        unfactored = {0}
        for partner in partners:
            cover_fact = facts[f"partner-cover:0:{partner}"]
            assert len(cover_fact["closed_rows"]) == len(cover_fact[channel]["edges"]) == 2
            for edge in cover_fact[channel]["edges"]:
                unfactored.update(facts[edge["fact"]][channel]["owners"])
        field = (
            "geometric_owner_set"
            if channel == "geometric_dependencies"
            else "validation_owner_set"
        )
        assert result[field] == sorted(unfactored)


def test_output_byte_ceiling_is_explicit_incomplete() -> None:
    with pytest.raises(audit.IncompleteError, match="output byte"):
        audit.output_ceiling(run(fixture()), 1)


@pytest.mark.parametrize(
    "mutation",
    [
        "sample",
        "stale_seed",
        "stale_node",
        "missing",
        "future",
        "duplicate",
        "foreign_cover",
        "missing_cover_row",
        "closure",
        "guard",
        "frame",
        "final",
        "open",
        "incomplete",
    ],
)
def test_invalid_or_unsupported_custody_refused(mutation: str) -> None:
    data = fixture(supplied=(1,))
    seed, node, receipt, _ = data
    step = node["steps"][0]
    if mutation == "sample":
        receipt["mode"] = "sample"
    elif mutation.startswith("stale_"):
        receipt["certificate"]["seed_sha256" if mutation == "stale_seed" else "node_sha256"] = (
            "0" * 64
        )
    elif mutation in {"missing", "future"}:
        step["rows"][0]["prior_reference"] = {
            "kind": "phase3",
            "node": "synthetic",
            "step": 99,
            "row": 0,
        }
    elif mutation == "duplicate":
        seed["cells"]["0"].append(copy.deepcopy(seed["cells"]["0"][0]))
    elif mutation == "foreign_cover":
        step["prior_partner_pose_covers"]["1"][0]["reference"]["owner"] = 2
    elif mutation == "missing_cover_row":
        step["prior_partner_pose_covers"]["1"] = []
    elif mutation == "closure":
        node["contradiction"]["kind"] = "unknown"
    elif mutation == "guard":
        node["guard_source"] = "foreign"
    elif mutation == "frame":
        node["B"] = "2"
    elif mutation == "final":
        node["final_state"]["cells"]["0"][0]["reference"]["row"] = 2
    elif mutation == "open":
        step["rows"][0]["interval"][0] = "1/2"
    else:
        step["complete"] = False
    with pytest.raises((exact.AuditError, audit.standing.VerificationError)):
        run(data)


@pytest.mark.parametrize("ceiling", ["time", "facts", "edges"])
def test_resource_ceiling_is_incomplete(ceiling: str) -> None:
    seed, node, receipt, cells = fixture()
    with pytest.raises(audit.IncompleteError):
        audit.inventory(
            seed,
            node,
            node["steps"],
            receipt,
            cells,
            deadline=0 if ceiling == "time" else time.monotonic() + 20,
            max_facts=1 if ceiling == "facts" else 200000,
            max_edges=1 if ceiling == "edges" else 2000000,
        )


@pytest.mark.parametrize("mutation", ["accepted", "truncated", "identity"])
def test_cli_stream_eof_and_canonical_custody(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    mutation: str,
) -> None:
    seed, node, receipt, cells = fixture(supplied=(1,))
    directory = tmp_path / "objects"
    directory.mkdir()
    receipt["directory"] = "objects"
    for name, packet in (("seed", seed), ("node", node)):
        raw = gzip.compress(audit.saved.canonical_bytes(packet))
        (directory / f"{name}-fixture.json.gz").write_bytes(
            raw[:-8] if mutation == "truncated" and name == "node" else raw
        )
    if mutation == "identity":
        receipt["certificate"]["node_sha256"] = "0" * 64
    receipt_path = tmp_path / "receipt.json"
    receipt_path.write_text(retained_json.dumps(receipt))
    output = tmp_path / "inventory.json"
    monkeypatch.setattr(exact, "REPO", tmp_path)
    monkeypatch.setattr(audit.standing, "cover_cells", lambda: cells)
    monkeypatch.setattr(audit, "provenance", lambda *_args: {"synthetic": True})
    code = audit.main(
        [
            "--saved",
            str(directory),
            "--standing-receipt",
            str(receipt_path),
            "--output",
            str(output),
        ]
    )
    saved = exact.decode(output.read_bytes())
    assert code == (0 if mutation == "accepted" else 1)
    assert saved["status"] == ("inventory_complete" if mutation == "accepted" else "refused")
    assert saved["smaller_mask_admitted"] is False
    assert saved["core_minimality_proved"] is False
    assert json.loads(capsys.readouterr().out)["status"] == saved["status"]
    if mutation == "accepted":
        first_identity = saved["deterministic_inventory_sha256"]
        second = tmp_path / "fresh-inventory.json"
        assert (
            audit.main(
                [
                    "--saved",
                    str(directory),
                    "--standing-receipt",
                    str(receipt_path),
                    "--output",
                    str(second),
                ]
            )
            == 0
        )
        replay = exact.decode(second.read_bytes())
        assert replay["deterministic_inventory_sha256"] == first_identity
        assert replay["dag"] == saved["dag"]
        capsys.readouterr()


def test_fresh_cli_processes_preserve_deterministic_core(tmp_path: Path) -> None:
    seed, node, receipt, _ = fixture(supplied=(1,), cited=(1,))
    directory = tmp_path / "objects"
    directory.mkdir()
    receipt["directory"] = "objects"
    for name, packet in (("seed", seed), ("node", node)):
        (directory / f"{name}-fixture.json.gz").write_bytes(
            gzip.compress(audit.saved.canonical_bytes(packet))
        )
    receipt_path = tmp_path / "standing.json"
    receipt_path.write_text(retained_json.dumps(receipt))
    # Only the synthetic repository/cell fixture is injected. Each clean interpreter
    # executes the actual module CLI, loader, streamed inventory and output writer.
    bootstrap = """
import runpy
import sys
from fractions import Fraction as Q
from pathlib import Path
from devtools import audit_n17_endpoint_receipt as exact
from devtools import verify_n17_kernel_certificate as standing
exact.REPO = Path(sys.argv.pop(1))
triangle = ((Q(0), Q(0)), (Q(1), Q(0)), (Q(0), Q(1)))
standing.cover_cells = lambda: standing.Cells(
    ("A", "B", "C"), (triangle,) * 3, Q(5), {"kind": "synthetic-closed-world"}
)
runpy.run_module("devtools.audit_n17_certificate_dependencies", run_name="__main__")
"""
    reports = []
    for index in range(2):
        output = tmp_path / f"fresh-{index}.json"
        command = [
            sys.executable,
            "-c",
            bootstrap,
            str(tmp_path),
            "--saved",
            str(directory),
            "--standing-receipt",
            str(receipt_path),
            "--max-seconds",
            str(15 + index),
            "--output",
            str(output),
        ]
        process = subprocess.run(
            command,
            cwd=Path(audit.__file__).parents[1],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        assert process.returncode == 0, process.stderr
        report = exact.decode(output.read_bytes())
        assert report["status"] == "inventory_complete"
        assert report["execution"]["argv"] == command[4:]
        assert all(report[name] is False for name in audit.FALSE_FLAGS)
        reports.append(report)
    assert reports[0]["execution"]["argv"] != reports[1]["execution"]["argv"]
    cores = [
        {
            key: value
            for key, value in report.items()
            if key not in {"execution", "provenance", "deterministic_inventory_sha256"}
        }
        for report in reports
    ]
    assert cores[0] == cores[1]
    assert (
        audit.saved.content_sha256(cores[0])
        == reports[0]["deterministic_inventory_sha256"]
        == reports[1]["deterministic_inventory_sha256"]
    )


@pytest.mark.parametrize("ceiling", ["compressed", "decoded", "output"])
def test_cli_configured_byte_ceiling_never_silently_truncates(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    ceiling: str,
) -> None:
    seed, node, receipt, cells = fixture()
    directory = tmp_path / "objects"
    directory.mkdir()
    receipt["directory"] = "objects"
    for name, packet in (("seed", seed), ("node", node)):
        (directory / f"{name}-fixture.json.gz").write_bytes(
            gzip.compress(audit.saved.canonical_bytes(packet))
        )
    receipt_path = tmp_path / "receipt.json"
    receipt_path.write_text(retained_json.dumps(receipt))
    monkeypatch.setattr(exact, "REPO", tmp_path)
    monkeypatch.setattr(audit.standing, "cover_cells", lambda: cells)
    monkeypatch.setattr(audit, "provenance", lambda *_args: {})
    flag = {
        "compressed": "--max-node-bytes",
        "decoded": "--max-decoded-node-bytes",
        "output": "--max-output-bytes",
    }[ceiling]
    output = tmp_path / "inventory.json"
    assert (
        audit.main(
            [
                "--saved",
                str(directory),
                "--standing-receipt",
                str(receipt_path),
                flag,
                "1",
                "--output",
                str(output),
            ]
        )
        == 1
    )
    result = exact.decode(output.read_bytes())
    assert result["status"] == "incomplete"
    assert result["inventory_complete"] is False
    assert "dag" not in result
    assert result["smaller_mask_admitted"] is False
    capsys.readouterr()


def test_report_does_not_alias_input_closed_metadata() -> None:
    data = fixture()
    result = run(data)
    data[0]["mask"].append(9)
    data[0]["cells"]["0"][0]["interval"][0] = "1/2"
    assert result["original_mask"] == [0, 1, 2]
    row = next(f for f in result["dag"] if f["id"].startswith("row:") and f["owner"] == 0)
    assert row["closed_interval"] == ["0", "1"]


def test_boolean_or_extra_reference_fields_are_not_typed_integers() -> None:
    for reference in (
        {"kind": "wall_seed", "owner": False, "row": 0},
        {"kind": "phase3", "node": "synthetic", "step": 0, "row": 0, "extra": True},
    ):
        with pytest.raises(exact.AuditError):
            audit.ref_key(reference)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("seconds", float("nan")),
        ("seconds", 0),
        ("max_facts", 25001),
        ("max_edges", 500001),
        ("max_node_bytes", (512 << 20) + 1),
        ("max_decoded_node_bytes", (2 << 30) + 1),
    ],
)
def test_invalid_or_excessive_limits_refuse_before_input_loading(
    field: str, value: Any
) -> None:
    arguments = {
        "seconds": 90,
        "max_facts": 25000,
        "max_edges": 500000,
        "max_node_bytes": 512 << 20,
        "max_decoded_node_bytes": 2 << 30,
    }
    arguments[field] = value
    with pytest.raises(exact.AuditError, match="ceiling"):
        audit.load_inventory(Path("absent"), Path("absent.json"), **arguments)


def test_cli_nonfinite_budget_retains_valid_refusal_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(audit, "provenance", lambda *_args: {})
    output = tmp_path / "refusal.json"
    assert (
        audit.main(
            [
                "--saved",
                "absent",
                "--standing-receipt",
                "absent.json",
                "--max-seconds",
                "nan",
                "--output",
                str(output),
            ]
        )
        == 1
    )
    result = exact.decode(output.read_bytes())
    assert result["status"] == "refused"
    assert result["execution"]["limits"]["inventory_seconds"] == "nan"
    capsys.readouterr()
