"""Target-free one-round cover/recovery composition and fresh-process controls."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pytest
from test_check_n17_strict_core_regional_transfer import fixture as transfer_fixture

from devtools import check_n17_one_round_owned_domain_propagation as tool

Q = tool.Q


def deadline() -> float:
    return time.monotonic() + 60


def fixture(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, regional: bool = False
) -> dict[str, Any]:
    """A synthetic inherited premise, not a physical seventeen-square packing."""
    base = transfer_fixture(tmp_path, monkeypatch)
    doc = {
        "schema": tool.DESCRIPTOR_SCHEMA,
        "mode": "point",
        **{k: v for k, v in base.items() if k != "schema"},
    }
    if regional:
        doc["mode"] = "fixed_core_regional"
        certificate = tool.transfer.generate(base, deadline=deadline())
        replay = tool.transfer.check(base, certificate, deadline=deadline())
        for role, value in zip(
            tool.REGIONAL_ROLES[3:], (base, certificate, replay), strict=True
        ):
            raw = json.dumps(value, sort_keys=True).encode()
            path = tmp_path / (role + ".json")
            path.write_bytes(raw)
            doc[role], doc[role + "_sha256"] = path.name, hashlib.sha256(raw).hexdigest()
    return doc


def load_geometry(doc: dict[str, Any], tmp_path: Path) -> tuple[Any, ...]:
    old_doc = json.loads((tmp_path / doc["collective_descriptor"]).read_text())
    prior = json.loads((tmp_path / doc["collective_replay"]).read_text())
    rows, groups, *_ = tool.collective.intake(old_doc, deadline=deadline())
    return rows, groups, prior


def test_full992_pruning_matches_prior_and_keeps_closed_seams(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    rows, _groups, prior = load_geometry(doc, tmp_path)
    effective, roster = tool.prune_prior(rows, prior, deadline())
    assert sum(map(len, effective.values())) == 992
    assert len(effective[12]) == 32
    assert len(effective[18]) == 64
    assert all(not effective[18][i]["domain"] for i in tool.transfer.TARGET_INDICES)
    assert effective[18][18]["interval"][1] == effective[18][19]["interval"][0]
    target = next(r for r in roster if r["owner"] == 18)
    assert target["baseline_closed_interval_union"] == [
        ["0", "19/64"],
        ["3/8", "33/64"],
        ["53/64", "1"],
    ]
    assert rows[18][19]["domain"]  # The original premise was not modified.


@pytest.mark.parametrize(
    "kind", ["reference", "interval", "nonempty", "missing", "duplicate", "baseline"]
)
def test_prior_decisions_cannot_change_original_row_identity(
    kind: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    rows, _groups, prior = load_geometry(doc, tmp_path)
    target = next(r for r in prior["owners"] if r["owner"] == 18)
    row = target["rows"][24]
    if kind == "reference":
        row["reference"]["owner"] = 5
    elif kind == "interval":
        row["interval"] = ["0", "1"]
    elif kind == "nonempty":
        row["inherited_domain_nonempty"] = False
    elif kind == "missing":
        target["rows"].pop()
    elif kind == "duplicate":
        target["rows"][24] = copy.deepcopy(target["rows"][25])
    else:
        target["new_closed_interval_union"] = [["0", "1"]]
    with pytest.raises(ValueError, match=r"prior|roster|union"):
        tool.prune_prior(rows, prior, deadline())


def test_helper_union_retains_singletons_overlaps_and_seams() -> None:
    assert tool.collective.union_intervals(
        [(Q(0), Q(1, 2)), (Q(1, 2), Q(1)), (Q(1), Q(1))]
    ) == [(Q(0), Q(1))]
    assert tool.collective.length([(Q(0), Q(3, 4)), (Q(1, 4), Q(1))]) == 1


def test_recovery_row_deletion_is_monotone_and_freshly_strict() -> None:
    rows = [
        {"interval": ["0", "1/64"], "domain": [(Q(1), Q(1))]},
        {"interval": ["1/64", "1/32"], "domain": [(Q(6, 5), Q(1))]},
    ]
    full = tool.guard.common_owned(rows, tool.guard.new_work(), deadline())
    fewer = copy.deepcopy(rows)
    fewer[1]["domain"] = []
    expanded = tool.guard.common_owned(fewer, tool.guard.new_work(), deadline())
    assert full
    assert expanded
    assert all(tool.cases.contains(expanded, p) for p in full)
    assert tool.guard.strictly_owned(
        expanded, fewer[0]["domain"], Q(0), Q(1, 64), tool.guard.new_work(), deadline()
    )


def test_empty_recovered_group_is_allowed_but_empty_owner_cover_refuses() -> None:
    rows = [{"interval": ["0", "1"], "domain": [(Q(0), Q(0)), (Q(4), Q(4))]}]
    assert tool.guard.common_owned(rows, tool.guard.new_work(), deadline()) == []
    with pytest.raises(ValueError, match="empty owner cover"):
        tool.guard.common_owned([{**rows[0], "domain": []}], tool.guard.new_work(), deadline())


def test_shared_singleton_touch_and_lexicographic_owner_pair() -> None:
    groups = {o: [] for o in tool.OWNERS}
    groups[0], groups[1], groups[2] = [(Q(1), Q(1))], [(Q(1), Q(1))], [(Q(1), Q(1))]
    result = tool.shared_intersection(groups, tool.guard.new_work(), deadline())
    assert result == {
        "kind": "shared_strictly_owned_point",
        "owners": [0, 1],
        "intersection": [["1", "1"]],
    }


def test_intersection_products_stop_before_unbounded_primitive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    groups = {o: [] for o in tool.OWNERS}
    groups[0] = groups[1] = [(Q(1), Q(1))]
    monkeypatch.setattr(tool, "INTERSECTION_PRODUCTS", 0)
    monkeypatch.setattr(
        tool.cases.conditional,
        "intersection",
        lambda *_: pytest.fail("unbounded intersection executed"),
    )
    with pytest.raises(tool.IncompleteError, match="cumulative intersection"):
        tool.shared_intersection(groups, tool.guard.new_work(), deadline())


def test_intersection_output_limit_is_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    groups = {o: [] for o in tool.OWNERS}
    monkeypatch.setattr(tool.guard, "INTERSECTION_LIMIT", 0)
    monkeypatch.setattr(tool.cases.conditional, "intersection", lambda *_: [(Q(0), Q(0))])
    with pytest.raises(tool.IncompleteError, match="output vertex"):
        tool.shared_intersection(groups, tool.guard.new_work(), deadline())


@pytest.mark.parametrize("mode", ["point", "fixed_core_regional"])
def test_completed_recovery_shared_point_has_only_selected_scope(
    mode: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    rows, groups, prior = load_geometry(doc, tmp_path)
    result = tool.construct(rows, groups, prior, mode=mode, deadline=deadline())
    assert result["status"] == "context_excluded"
    assert result["prior_effective_rows_accounted"] == 992
    assert result["all_foreign_recoveries_and_strict_checks_completed"]
    assert result["owner0_core_unchanged"]
    assert result["new_collective"] is None
    assert result["point_guard_exclusion_proved"] is (mode == "point")
    assert result["declared_guard_exclusion_proved"] is (mode == "fixed_core_regional")
    assert all(result[k] is False for k in tool.guard.scope())


def synthetic_pass(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, positive: bool
) -> tuple[Any, ...]:
    """Isolate simultaneous-pass plumbing; the recovery boundary is supplied synthetically."""
    doc = fixture(tmp_path, monkeypatch)
    rows, groups, _ = load_geometry(doc, tmp_path)
    for owner in rows:
        for row in rows[owner]:
            row["domain"] = [(Q(4), Q(4))]
    for index in tool.transfer.TARGET_INDICES:
        rows[18][index]["domain"] = [(Q(1), Q(1))]
    rows[18][24]["domain"] = [(Q(3), Q(3))] if positive else [(Q(4), Q(4))]
    old_groups = {o: [] for o in tool.OWNERS}
    old_groups[0] = groups[0]
    prior = tool.collective.construct(rows, old_groups, deadline=deadline())
    prior.update(
        schema=tool.collective.SCHEMA,
        verification_passed=True,
        original_rows_inherited=1056,
        **tool.guard.scope(),
    )
    prior["declared_guard_exclusion_proved"] = False
    recovered = {o: [] for o in tool.OWNERS}
    recovered[0], recovered[1] = groups[0], [(Q(3), Q(3))]
    visited = []

    def recover(
        snapshot: list[dict[str, Any]], _work: dict[str, int], _deadline: float
    ) -> list[tool.Point]:
        owner = next(o for o in rows if snapshot[0]["reference"]["owner"] == o)
        visited.append(owner)
        assert (
            not any(snapshot[i]["domain"] for i in tool.transfer.TARGET_INDICES)
            if owner == 18
            else True
        )
        return recovered[owner]

    monkeypatch.setattr(tool.guard, "common_owned", recover)
    return rows, groups, prior, visited


@pytest.mark.parametrize("positive", [False, True])
def test_one_simultaneous_pass_additional_loss_does_not_recount_old25(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, positive: bool
) -> None:
    rows, groups, prior, visited = synthetic_pass(tmp_path, monkeypatch, positive=positive)
    result = tool.construct(rows, groups, prior, mode="point", deadline=deadline())
    assert visited == list(tool.OWNERS[1:])
    assert result["new_collective_rows_accounted"] == 992
    assert result["criterion_met"] is positive
    target = next(r for r in result["additional_restrictions"] if r["owner"] == 18)
    assert target["additional_lost_length"] == ("1/64" if positive else "0")
    assert target["newly_excluded_rows"] == ([24] if positive else [])
    assert result["new_collective"]["recovered_groups_frozen_during_collective_pass"]
    assert "original_owned_sets_unchanged" not in result["new_collective"]


def test_complete_owner_empty_secondary_keeps_point_scope(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    rows, groups, _prior, _visited = synthetic_pass(tmp_path, monkeypatch, positive=True)
    for index, row in enumerate(rows[18]):
        if index not in tool.transfer.TARGET_INDICES:
            row["domain"] = [(Q(3), Q(3))]
    old_groups = {o: [] for o in tool.OWNERS}
    old_groups[0] = groups[0]
    prior = tool.collective.construct(rows, old_groups, deadline=deadline())
    prior.update(
        schema=tool.collective.SCHEMA,
        verification_passed=True,
        original_rows_inherited=1056,
        declared_guard_exclusion_proved=False,
        **tool.guard.scope(),
    )
    result = tool.construct(rows, groups, prior, mode="point", deadline=deadline())
    assert result["closure"]["kind"] == "collective_owner_cover_empty"
    assert result["closure"]["owners"] == [18]
    assert result["point_contradiction_proved"]
    assert not result["declared_guard_exclusion_proved"]
    assert result["new_collective_rows_accounted"] == 992


def test_already_empty_input_owner_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    rows, _groups, prior = load_geometry(doc, tmp_path)
    entry = next(o for o in prior["owners"] if o["owner"] == 5)
    for row in entry["rows"]:
        row["covered"] = True
        row["domain_retained_unchanged"] = False
    entry["new_closed_interval_union"] = []
    with pytest.raises(ValueError, match="already-empty input"):
        tool.prune_prior(rows, prior, deadline())


def test_recovery_work_ceiling_is_incomplete_not_a_miss(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    rows, groups, prior = load_geometry(doc, tmp_path)
    monkeypatch.setattr(tool.guard, "RECOVERY_SUPPORT_LIMIT", 0)
    with pytest.raises(tool.IncompleteError, match="MIN-support ceiling"):
        tool.construct(rows, groups, prior, mode="point", deadline=deadline())


def test_prior_proof_reconstructed_once_and_transitive_bytes_retained(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    count = [0]
    original = tool.collective.check

    def replay(*args: Any, **kwargs: Any) -> Any:
        count[0] += 1
        return original(*args, **kwargs)

    monkeypatch.setattr(tool.collective, "check", replay)
    result = tool.generate(doc, deadline=deadline())
    assert count == [1]
    assert result["prior_collective_finite_reconstructions"] == 1
    assert result["old_owner0_target_rows_transferred"] is False
    assert result["original17_endpoint_retention_inherited"]
    assert tool.check(doc, result, deadline=deadline())["verification_passed"]
    assert count == [2]


def test_regional_mode_uses_transfer_once_not_a_second_prior_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch, regional=True)
    count = [0]
    original = tool.collective.check

    def replay(*args: Any, **kwargs: Any) -> Any:
        count[0] += 1
        return original(*args, **kwargs)

    monkeypatch.setattr(tool.collective, "check", replay)
    result = tool.generate(doc, deadline=deadline())
    assert count == [1]
    assert result["uniform_transfer_rechecked"]
    assert result["guard"]["half_width"] == str(tool.transfer.HALF_WIDTH)
    assert result["point_guard_exclusion_proved"] is False


@pytest.mark.parametrize("kind", ["digest", "extra_role", "payload", "fresh_geometry"])
def test_custody_or_fresh_payload_tamper_refuses(
    kind: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    result = tool.generate(doc, deadline=deadline())
    if kind == "digest":
        doc["collective_certificate_sha256"] = "0" * 64
    elif kind == "extra_role":
        doc["transfer_certificate"] = "invented.json"
    elif kind == "payload":
        saved = tmp_path / doc["collective_replay"]
        data = json.loads(saved.read_text())
        data["owners"][0]["rows"][0]["covered"] = True
        raw = json.dumps(data).encode()
        saved.write_bytes(raw)
        doc["collective_replay_sha256"] = hashlib.sha256(raw).hexdigest()
    else:
        result["recovered_owned_groups"]["0"] = []
    with pytest.raises(ValueError, match=r"differs|roles"):
        tool.check(doc, result, deadline=deadline())


def test_resource_and_deadline_outputs_never_claim_proof() -> None:
    for exc in (tool.IncompleteError("resource"), ValueError("custody")):
        result = tool.failure(exc)
        assert not result["criterion_met"]
        assert not result["verification_passed"]
        assert all(value is False for key, value in result.items() if key.endswith("_proved"))
    with pytest.raises(tool.IncompleteError):
        tool.shared_intersection(
            {o: [] for o in tool.OWNERS}, tool.guard.new_work(), time.monotonic() - 1
        )


def direct_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """Synthetic accepted regional premises; no original conditioning proof is claimed."""
    doc = fixture(tmp_path, monkeypatch)
    point_doc = json.loads((tmp_path / doc["collective_descriptor"]).read_text())
    point = json.loads((tmp_path / point_doc["guard_certificate"]).read_text())
    context = point["contexts"][0]
    centre = (Q(1), Q(1))
    h = tool.regional.HALF_WIDTH
    context.update(
        guard={
            "half_width": str(h),
            "angle_interval": [str(tool.guard.TAU - h), str(tool.guard.TAU + h)],
            "centre_box": [[str(x - h), str(x + h)] for x in centre],
        },
        context_nonzero=True,
        closure=None,
    )
    for owner in tool.OWNERS[1:]:
        context["owned_groups"][str(owner)] = []
    for index, row in enumerate(context["conditional_rows"]["18"]):
        row["domain"] = [["1", "1"]] if index in tool.DIRECT_TARGET_INDICES else [["3", "3"]]
    selected = [
        {
            "row_index": i,
            **{
                k: copy.deepcopy(context["conditional_rows"]["18"][i][k])
                for k in ("reference", "interval")
            },
        }
        for i in tool.transfer.TARGET_INDICES
    ]
    decision = tool.regional.regional_decision(
        context,
        selected,
        deadline=deadline(),
        reference_context=point["parent_custody"]["typed_reference_context"],
    )
    assert decision["status"] == "criterion_missed"

    def retain(name: str, value: dict[str, Any]) -> tuple[str, str]:
        raw = json.dumps(value, sort_keys=True).encode()
        path = tmp_path / (name + ".json")
        path.write_bytes(raw)
        return path.name, hashlib.sha256(raw).hexdigest()

    regional_doc = {"schema": tool.regional.DESCRIPTOR_SCHEMA}
    custody = copy.deepcopy(point["parent_custody"])
    custody.update(seed_sha256="a" * 64, node_sha256="b" * 64)
    custody["compressed_sha256"] = {}
    for role in ("seed", "node"):
        path = tmp_path / (role + "-synthetic.json.gz")
        path.write_bytes(b"opaque accepted synthetic native bytes:" + role.encode())
        custody["compressed_sha256"][path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    custody["h290_receipt"], custody["h290_receipt_sha256"] = retain(
        "h290", {"synthetic_accepted_premise": True}
    )
    gate = {
        k: copy.deepcopy(custody[k])
        for k in (
            "seed_sha256",
            "node_sha256",
            "compressed_sha256",
            "h290_receipt",
            "h290_receipt_sha256",
        )
    }
    regional_doc["parent_descriptor"], regional_doc["parent_descriptor_sha256"] = retain(
        "gate", gate
    )
    regional_doc["centered_receipt"], regional_doc["centered_receipt_sha256"] = retain(
        "centered", {"synthetic_accepted_premise": True}
    )
    feasible = {}
    for role in tool.parent.feasible.INPUTS:
        feasible[role], feasible[role + "_sha256"] = retain("feasible-" + role, {"role": role})
    for role, value in (
        ("feasible_descriptor", feasible),
        ("feasible_certificate", {"synthetic_accepted_premise": True}),
        ("feasible_replay", {"synthetic_accepted_premise": True}),
    ):
        regional_doc[role], regional_doc[role + "_sha256"] = retain(role, value)
    historical = {
        "schema": tool.guard.DESCRIPTOR_SCHEMA,
        **{k: regional_doc[k] for r in tool.parent.INPUTS for k in (r, r + "_sha256")},
    }
    prior_inputs = {"schema": tool.collective.DESCRIPTOR_SCHEMA}
    for role in tool.collective.ROLES:
        prior_inputs[role], prior_inputs[role + "_sha256"] = retain(
            "historical-" + role,
            historical if role == "guard_descriptor" else {"synthetic_accepted_premise": True},
        )
    for role in ("collective_certificate", "collective_replay"):
        regional_doc[role], regional_doc[role + "_sha256"] = retain(
            role, {"accepted_inputs": prior_inputs}
        )
    accepted = {
        "schema": tool.regional.SCHEMA,
        **tool.guard.scope(),
        **decision,
        "point_guard_exclusion_proved": False,
        "point_guard_necessary_domain_restriction_proved": False,
        "accepted_inputs": regional_doc,
        "regional_context": context,
        "point_context_constructed": False,
        "accepted_point_domains_used_as_regional_domains": False,
        "original_rows_reconstructed": 1056,
        "regional_foreign_rows_conditioned": 992,
        "regional_contexts_constructed": 1,
        "matched_owned_point_witness": {"centre": ["1", "1"], "tau": str(tool.guard.TAU)},
        "parent_custody": custody,
        "container": point["container"],
        "original_endpoint_control": point["original_endpoint_control"],
    }
    result = {"schema": tool.DESCRIPTOR_SCHEMA, "mode": "direct_regional"}
    for role, value in zip(
        tool.DIRECT_ROLES,
        (regional_doc, accepted, accepted | {"verification_passed": True}),
        strict=True,
    ):
        result[role], result[role + "_sha256"] = retain("direct-" + role, value)
    return result


def test_direct_regional_replays_complete_component_without_reconditioning(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = direct_fixture(tmp_path, monkeypatch)
    for name in ("check", "generate", "intake"):
        monkeypatch.setattr(
            tool.regional, name, lambda *_a, **_k: pytest.fail("conditioning replay forbidden")
        )
    calls = [0]
    original = tool.regional.regional_decision

    def repeat(*args: Any, **kwargs: Any) -> Any:
        calls[0] += 1
        return original(*args, **kwargs)

    monkeypatch.setattr(tool.regional, "regional_decision", repeat)
    result = tool.generate(doc, deadline=deadline())
    assert calls == [1]
    assert result["mode"] == "direct_regional"
    assert result["regional_conditioning_reconstructed"] is False
    assert result["accepted_regional_conditioning_inherited"]
    assert result["prior_primary_same25_criterion_met"] is False
    assert result["prior_component_parameter_loss"] == "11/32"
    assert result["guard"]["half_width"] == "1/512"
    assert result["point_guard_exclusion_proved"] is False
    assert tool.check(doc, result, deadline=deadline())["verification_passed"]
    assert calls == [2]


@pytest.mark.parametrize(
    "kind",
    ["guard", "extra_row", "component_work", "native", "seven_role", "missing_typed_row"],
)
def test_direct_regional_premise_and_component_tampering_refuses(
    kind: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = direct_fixture(tmp_path, monkeypatch)
    accepted_path = tmp_path / doc["regional_certificate"]
    accepted = json.loads(accepted_path.read_text())
    if kind == "native":
        (tmp_path / "node-synthetic.json.gz").write_bytes(b"changed")
    elif kind == "seven_role":
        (tmp_path / "feasible_certificate.json").write_text("{}")
    else:
        if kind == "guard":
            accepted["regional_context"]["guard"]["half_width"] = "0"
        elif kind == "extra_row":
            next(o for o in accepted["collective"]["owners"] if o["owner"] == 18)["rows"][33][
                "covered"
            ] = True
        elif kind == "component_work":
            accepted["collective"]["work"]["sweep_rows"] += 1
        else:
            accepted["regional_context"]["conditional_rows"]["12"].pop()
        for role, data in (
            ("regional_certificate", accepted),
            ("regional_replay", accepted | {"verification_passed": True}),
        ):
            raw = json.dumps(data).encode()
            (tmp_path / doc[role]).write_bytes(raw)
            doc[role + "_sha256"] = hashlib.sha256(raw).hexdigest()
    with pytest.raises(
        ValueError, match=r"differs|fields|roster|incomplete|closed|required|byte"
    ):
        tool.generate(doc, deadline=deadline())


def test_conflicting_byte_alias_is_refused_before_replacing_held_identity(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(tool.finite, "REPO", tmp_path)
    path = tmp_path / "one.json"
    path.write_text("{}")
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    held = {path: (sha, 10)}
    with pytest.raises(ValueError, match="conflicting"):
        tool.hold_file(path.name, "0" * 64, 100, held, deadline())


def test_two_fresh_clean_processes_match_full_new_payload(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = fixture(tmp_path, monkeypatch)
    descriptor = tmp_path / "descriptor.json"
    descriptor.write_text(json.dumps(doc))
    generated, fresh = tmp_path / "generated.json", tmp_path / "fresh.json"
    argv = [
        sys.executable,
        "-m",
        "devtools.check_n17_one_round_owned_domain_propagation",
        "--descriptor",
        str(descriptor),
        "--max-seconds",
        "60",
    ]
    # The fixture's paths require a private retained root in each child.
    runner = tmp_path / "runner.py"
    runner.write_text(
        "import sys\nfrom pathlib import Path\n"
        "from devtools import check_n17_one_round_owned_domain_propagation as t\n"
        "t.finite.REPO=Path(sys.argv[1])\nraise SystemExit(t.main(sys.argv[2:]))\n"
    )
    argv = [sys.executable, str(runner), str(tmp_path), *argv[3:]]
    for tail in (
        ["--output", str(generated)],
        ["--certificate", str(generated), "--output", str(fresh)],
    ):
        process = subprocess.run(
            [*argv, *tail], capture_output=True, text=True, timeout=90, check=False
        )
        assert process.returncode == 0, process.stderr + process.stdout
    left, right = json.loads(generated.read_text()), json.loads(fresh.read_text())
    assert tool.payload(left) == tool.payload(right)
    assert right["verification_passed"]
    assert (
        left["new_collective_rows_accounted"] == 0
    )  # Complete recovery gave a shared-point contradiction.
