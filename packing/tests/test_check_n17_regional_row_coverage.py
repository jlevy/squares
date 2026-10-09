"""Target-free regional selection, complete reconstruction and custody controls."""

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
import test_check_n17_partner_pose_coupling as inherited
from test_check_n17_collective_row_coverage import context as point_context

from devtools import check_n17_regional_row_coverage as tool

Q = tool.Q
ORIGINAL_STATE = inherited.synthetic_state


def deadline() -> float:
    return time.monotonic() + 30


def owner_mapping() -> dict[int, int]:
    mapping: dict[int, int] = dict(zip(range(17), tool.collective.OWNERS, strict=True))
    mapping[11], mapping[12] = mapping[12], mapping[11]
    mapping[10], mapping[14] = mapping[14], mapping[10]
    return mapping


def synthetic_state() -> tuple[Any, ...]:
    """Complete grammar fixture; no feasible seventeen-square packing is asserted."""
    cells, roles, roster, centre = ORIGINAL_STATE()
    mapping = owner_mapping()
    cells = {str(mapping[int(k)]): v for k, v in cells.items()}
    roles = {label: mapping[owner] for label, owner in roles.items()}
    for owner, raw in cells.items():
        count = 32 if int(owner) == 12 else 64
        raw[:] = inherited.rows(int(owner), count)
        for index, row in enumerate(raw):
            row["residual_polygons"] = [[["1", "1"]] if owner == "0" else [["3", "3"]]]
            if owner != "0" and index:
                row["residual_polygons"] = []
    roster = [{**p, "owner": roles[str(p["label"])]} for p in roster]
    return cells, roles, roster, centre


def selected(cells: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "row_index": i,
            "reference": copy.deepcopy(cells["18"][i]["reference"]),
            "interval": list(cells["18"][i]["interval"]),
        }
        for i in tool.TARGET_INDICES
    ]


def accepted_selection(cells: dict[str, Any]) -> dict[str, Any]:
    owners = []
    for owner in tool.collective.OWNERS[1:]:
        owners.append(  # noqa: PERF401 - parallel row roster fixture
            {
                "owner": owner,
                "lost_length": "25/64" if owner == 18 else "0",
                "rows": [
                    {
                        "row_index": i,
                        "reference": copy.deepcopy(r["reference"]),
                        "interval": list(r["interval"]),
                        "inherited_domain_nonempty": True,
                        "covered": owner == 18 and i in tool.TARGET_INDICES,
                    }
                    for i, r in enumerate(cells[str(owner)])
                ],
            }
        )
    return {
        "schema": tool.collective.SCHEMA,
        "status": "angle_union_restricted",
        "criterion_met": True,
        "all_foreign_rows_accounted": 992,
        "simultaneous_original_groups_only": True,
        "original_owned_sets_unchanged": True,
        "changed_owners": [18],
        "complete_empty_owners": [],
        "point_contradiction_proved": False,
        "declared_guard_exclusion_proved": False,
        "point_guard_necessary_domain_restriction_proved": True,
        "original_rows_inherited": 1056,
        "original_endpoint_control": {"all17_retained": True, "family_disjoint": True},
        **tool.guard.scope(),
        "owners": owners,
    }


def reference() -> dict[str, Any]:
    return {
        "node_id": "synthetic-original-node",
        "step_owners": [o for o in tool.collective.OWNERS if o != 12],
    }


def fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    original_fixture = inherited.parent_fixture

    def remapped_parent(path: Path) -> tuple[Any, ...]:
        doc, descriptor = original_fixture(path)
        seed_path = path / "objects/seed-synthetic.json.gz"
        node_path = path / "objects/node-synthetic.json.gz"
        seed = json.loads(gzip.decompress(seed_path.read_bytes()))
        node = json.loads(gzip.decompress(node_path.read_bytes()))
        mapping = owner_mapping()
        seed["mask"] = list(tool.collective.OWNERS)
        seed_id = tool.finite.identity(seed)
        node["mask"] = seed["mask"]
        node["source"] = {"sha256": seed_id}
        node["final_state"].update(mask=seed["mask"], source=node["source"])
        for key in ("cells", "groups"):
            node["final_state"][key] = {
                str(mapping[int(k)]): v for k, v in node["final_state"][key].items()
            }
        for p, value in ((seed_path, seed), (node_path, node)):
            p.write_bytes(gzip.compress(tool.finite.canonical(value), mtime=0))
        receipt_path = path / "h290.json"
        receipt = json.loads(receipt_path.read_text())
        receipt["custody"]["parent_replay"]["mask"] = seed["mask"]
        receipt_path.write_text(json.dumps(receipt))
        return doc, descriptor

    monkeypatch.setattr(inherited, "parent_fixture", remapped_parent)
    monkeypatch.setattr(inherited, "synthetic_state", synthetic_state)
    original_feasible = inherited.feasible_fixture

    def remapped_feasible() -> tuple[Any, ...]:
        source, certificate = original_feasible()
        certificate["mask"] = list(tool.collective.OWNERS)
        pool = certificate["custody"]["proof_pool"]
        mapping = owner_mapping()
        pool["pools"] = {str(mapping[int(k)]): v for k, v in pool["pools"].items()}
        for row in certificate["rows"]:
            for piece in row["pieces"]:
                for kind in ("pooled", "ordinary"):
                    saved = piece.get(kind, {})
                    if "regions" in saved:
                        saved["regions"] = {
                            str(mapping[int(k)]): v for k, v in saved["regions"].items()
                        }
        return source, certificate

    monkeypatch.setattr(inherited, "feasible_fixture", remapped_feasible)
    doc = inherited.write_fixture(tmp_path, monkeypatch)
    doc["schema"] = tool.DESCRIPTOR_SCHEMA
    base = {
        "schema": tool.parent.DESCRIPTOR_SCHEMA,
        **{k: doc[k] for r in tool.parent.INPUTS for k in (r, r + "_sha256")},
    }
    held: dict[Path, tuple[str, int]] = {}
    final, custody, _roster, _centre = tool.parent.intake(base, held, deadline())
    accepted = accepted_selection(final["cells"])
    historical = {**base, "schema": tool.guard.DESCRIPTOR_SCHEMA}

    def retain(name: str, value: dict[str, Any]) -> tuple[str, str]:
        raw = json.dumps(value, sort_keys=True).encode()
        path = tmp_path / (name + ".json")
        path.write_bytes(raw)
        return path.name, hashlib.sha256(raw).hexdigest()

    name, sha = retain("historical_guard_descriptor", historical)
    accepted.update(
        parent_custody={k: custody[k] for k in tool.CUSTODY_KEYS},
        accepted_inputs={
            "schema": tool.collective.DESCRIPTOR_SCHEMA,
            "guard_descriptor": name,
            "guard_descriptor_sha256": sha,
        },
    )
    for role, value in (
        ("collective_certificate", accepted),
        ("collective_replay", accepted | {"verification_passed": True}),
    ):
        doc[role], doc[role + "_sha256"] = retain(role, value)
    return doc


def regional_context(*, miss: bool = False) -> dict[str, Any]:
    ctx = point_context()
    ctx.update(context_nonzero=True, closure=None)
    for i in range(64):
        ctx["conditional_rows"]["18"][i]["domain"] = (
            [["1", "1"]]
            if i in tool.TARGET_INDICES and not (miss and i == 19)
            else [["3", "3"]]
        )
    return ctx


@pytest.mark.parametrize(
    "mutation", ["count", "interval", "reference", "selection", "other_owner"]
)
def test_same25_original_identity_refuses(mutation: str) -> None:
    cells, *_ = synthetic_state()
    accepted = accepted_selection(cells)
    entry = next(r for r in accepted["owners"] if r["owner"] == 18)
    if mutation == "count":
        entry["rows"].pop()
    elif mutation == "interval":
        entry["rows"][19]["interval"][0] = "0"
    elif mutation == "reference":
        entry["rows"][19]["reference"]["owner"] = 21
    elif mutation == "selection":
        entry["rows"][19]["covered"] = False
    else:
        accepted["owners"][0]["rows"][0]["covered"] = True
    with pytest.raises(ValueError, match="differs"):
        tool.selected_rows(accepted, cells, reference())


def test_exact_same25_refs_and_adjacent_closed_seams() -> None:
    cells, *_ = synthetic_state()
    result = tool.selected_rows(accepted_selection(cells), cells, reference())
    assert [r["row_index"] for r in result] == list(tool.TARGET_INDICES)
    assert result[0]["interval"] == ["19/64", "5/16"]
    assert cells["18"][18]["interval"][1] == result[0]["interval"][0]


@pytest.mark.parametrize("miss", [False, True])
def test_real_collective_same25_primary_not_any_angle_loss(*, miss: bool) -> None:
    cells, *_ = synthetic_state()
    result = tool.regional_decision(
        regional_context(miss=miss),
        selected(cells),
        deadline=deadline(),
        reference_context=reference(),
    )
    assert result["criterion_met"] is (not miss)
    assert result["same25_coverage_checks_performed"] == 25
    assert result["collective"]["all_foreign_rows_accounted"] == 992
    assert result["declared_guard_exclusion_proved"] is False
    assert result["regional_necessary_domain_restriction_proved"] is (not miss)
    if miss:
        assert result["collective"]["changed_owners"] == [18]


@pytest.mark.parametrize("kind", ["conditional_owner_cover_empty", "owned_hulls_intersect"])
def test_stronger_context_closure_after_full_conditioning(
    kind: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    cells, *_ = synthetic_state()
    ctx = regional_context()
    ctx["closure"] = {"kind": kind, "owner": 18}
    monkeypatch.setattr(
        tool.collective, "construct", lambda *_a, **_k: pytest.fail("collective after closure")
    )
    result = tool.regional_decision(
        ctx, selected(cells), deadline=deadline(), reference_context=reference()
    )
    assert result["status"] == "regional_guard_excluded"
    assert result["same25_coverage_checks_performed"] == 0
    assert result["declared_guard_exclusion_proved"]
    ctx["all_foreign_rows_conditioned"] = 991
    with pytest.raises(ValueError, match="conditioning differs"):
        tool.regional_decision(
            ctx, selected(cells), deadline=deadline(), reference_context=reference()
        )


def test_collective_owner_empty_stronger_and_live_seam_prevents_it() -> None:
    cells, *_ = synthetic_state()
    ctx = regional_context()
    for row in ctx["conditional_rows"]["18"]:
        row["domain"] = [["1", "1"]]
    closed = tool.regional_decision(
        ctx, selected(cells), deadline=deadline(), reference_context=reference()
    )
    assert closed["collective_closure"]["kind"] == "collective_owner_cover_empty"
    assert len(closed["collective_closure"]["rows"]) == 64
    ctx["conditional_rows"]["18"][0]["domain"] = [["3", "3"]]
    open_result = tool.regional_decision(
        ctx, selected(cells), deadline=deadline(), reference_context=reference()
    )
    assert open_result["collective_closure"] is None


def test_direct_regional_reconstruction_never_point_shortcut(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cells, roles, roster, centre = synthetic_state()
    widths = []
    original = tool.guard.condition_context

    def counted(*args: Any, **kwargs: Any) -> dict[str, Any]:
        widths.append(kwargs["half_width"])
        return original(*args, **kwargs)

    monkeypatch.setattr(tool.guard, "condition_context", counted)
    result = tool.construct(
        cells,
        roles,
        roster,
        centre,
        selected(cells),
        deadline=deadline(),
        reference_context=reference(),
    )
    assert widths == [Q(1, 512)]
    assert result["original_rows_reconstructed"] == 1056
    assert result["regional_foreign_rows_conditioned"] == 992
    assert result["original_endpoint_control"]["all17_retained"]


def test_full_generate_custody_roundtrip_and_tamper(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    result = tool.generate(doc, deadline=deadline())
    assert tool.check(doc, result, deadline=deadline())["verification_passed"]
    assert result["accepted_point_domains_used_as_regional_domains"] is False
    assert result["point_context_constructed"] is False
    result["same25_coverage_checks_performed"] += 1
    with pytest.raises(ValueError, match="reconstruction differs"):
        tool.check(doc, result, deadline=deadline())


def test_positive_complete_generate_and_fresh_scope(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Synthetic finite-context boundary; this is not a physical17 packing."""
    doc = fixture(tmp_path, monkeypatch)

    def injected_context(*args: Any, **kwargs: Any) -> dict[str, Any]:
        centre = args[2]
        half = kwargs["half_width"]
        ctx = regional_context()
        ctx["guard"] = {
            "half_width": str(half),
            "centre_box": [[str(x - half), str(x + half)] for x in centre],
            "angle_interval": [str(tool.guard.TAU - half), str(tool.guard.TAU + half)],
        }
        return ctx

    monkeypatch.setattr(tool.guard, "condition_context", injected_context)
    result = tool.generate(doc, deadline=deadline())
    assert result["status"] == "same25_regional_rows_restricted"
    assert result["criterion_met"]
    assert result["same25_coverage_checks_performed"] == 25
    assert not result["point_guard_necessary_domain_restriction_proved"]
    assert not result["declared_guard_exclusion_proved"]
    assert tool.check(doc, result, deadline=deadline())["verification_passed"]


@pytest.mark.parametrize(
    "role", ["collective_certificate", "collective_replay", "centered_receipt"]
)
def test_byte_custody_changes_refuse(
    role: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    path = tmp_path / doc[role]
    path.write_bytes(path.read_bytes() + b" ")
    with pytest.raises(ValueError, match=r"custody|identity"):
        tool.generate(doc, deadline=deadline())


@pytest.mark.parametrize("exc", [ValueError("identity"), tool.IncompleteError("limit")])
def test_failure_clears_every_scope_flag(exc: Exception) -> None:
    result = tool.failure(exc)
    assert not result["criterion_met"]
    assert not any(v for k, v in result.items() if k.endswith("_proved"))
    assert not result["verification_passed"]


def test_deadline_original_endpoint_controls() -> None:
    cells, roles, roster, centre = synthetic_state()
    with pytest.raises(tool.IncompleteError):
        tool.construct(
            cells,
            roles,
            roster,
            centre,
            selected(cells),
            deadline=time.monotonic() - 1,
            reference_context=reference(),
        )


def test_fixed_witness_requires_actual_restricted_piece() -> None:
    cells, roles, roster, _centre = synthetic_state()
    with pytest.raises(ValueError, match="fixed witness absent"):
        tool.construct(
            cells,
            roles,
            roster,
            (Q(2), Q(2)),
            selected(cells),
            deadline=deadline(),
            reference_context=reference(),
        )


def test_restricted_wall_work_ceiling_never_returns_a_proof(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cells, roles, roster, centre = synthetic_state()
    monkeypatch.setattr(tool.guard, "GENERATED_VERTEX_LIMIT", 0)
    with pytest.raises(tool.IncompleteError, match="clip"):
        tool.construct(
            cells,
            roles,
            roster,
            centre,
            selected(cells),
            deadline=deadline(),
            reference_context=reference(),
        )


def test_inherited_global_scope_tamper_refuses() -> None:
    cells, *_ = synthetic_state()
    accepted = accepted_selection(cells)
    accepted["global_optimality_proved"] = True
    with pytest.raises(ValueError, match="premise differs"):
        tool.selected_rows(accepted, cells, reference())


@pytest.mark.parametrize("value", [[], {"schema": "wrong"}])
def test_clean_cli_malformed_descriptor_retains_refusal(value: Any, tmp_path: Path) -> None:
    descriptor, output = tmp_path / "bad.json", tmp_path / "refusal.json"
    descriptor.write_text(json.dumps(value))
    run = subprocess.run(
        [
            sys.executable,
            "-m",
            "devtools.check_n17_regional_row_coverage",
            "--descriptor",
            str(descriptor),
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    assert run.returncode == 1
    result = json.loads(output.read_text())
    assert result["status"] == "refused"
    assert not result["criterion_met"]
    assert not result["verification_passed"]


def test_original_endpoint_refusal() -> None:
    cells, roles, roster, centre = synthetic_state()
    roster[1]["centre"] = [["2", "2"], ["2", "2"]]
    with pytest.raises(ValueError, match="endpoint"):
        tool.construct(
            cells,
            roles,
            roster,
            centre,
            selected(cells),
            deadline=deadline(),
            reference_context=reference(),
        )


def test_two_clean_processes_reconstruct_full_payload(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    descriptor = tmp_path / "descriptor.json"
    descriptor.write_text(json.dumps(doc))
    outputs = [tmp_path / "certificate.json", tmp_path / "fresh.json"]
    bootstrap = (
        "import sys; from pathlib import Path; "
        "from devtools import check_n17_regional_row_coverage as m; "
        "m.finite.REPO=Path(sys.argv.pop(1)); raise SystemExit(m.main(sys.argv[1:]))"
    )
    for index, output in enumerate(outputs):
        argv = [
            sys.executable,
            "-c",
            bootstrap,
            str(tmp_path),
            "--descriptor",
            str(descriptor),
            "--max-seconds",
            "30",
            "--output",
            str(output),
        ]
        if index:
            argv += ["--certificate", str(outputs[0])]
        run = subprocess.run(argv, capture_output=True, text=True, timeout=35, check=False)
        assert run.returncode == 0, run.stderr + output.read_text()
    first, fresh = [json.loads(p.read_text()) for p in outputs]
    assert tool.payload(first) == tool.payload(fresh)
    assert fresh["verification_passed"]
