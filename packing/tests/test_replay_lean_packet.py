"""Staging and receipting three packets' Lean proofs from retained bytes.

``devtools.replay_lean_packet`` stages chelokot's and Daniel's small-n proofs (T-238) and
Hosono's s(21) = 5 (T-234) from the retained packets, binding every file to its upstream
digest, and accepts a build only with the three standard axioms and every negative
control refused. These tests hold the staging, the acceptance and the offline check;
the build itself needs Lean and the Mathlib cache.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from devtools import replay_lean_packet as rlp

STANDARD = "[propext, Classical.choice, Quot.sound]"


@pytest.mark.parametrize("name", sorted(rlp.ROUTES))
def test_each_route_stages_bound_to_its_upstream_digests(name: str, tmp_path: Path) -> None:
    spec = rlp.route(name)
    report = rlp.stage(spec, tmp_path)
    assert report["ok"], report["problems"]
    assert set(report["kernel_escapes"].values()) == {0}
    assert report["toolchain"] == spec.toolchain
    assert report["mathlib"] == spec.mathlib
    assert all(staged.sha256 or staged.blob for staged in spec.files)
    probe = (tmp_path / spec.project / "Probe.lean").read_text(encoding="utf-8")
    for theorem in spec.theorems:
        assert f"#print axioms {theorem}\n" in probe
    assert {control.kind for control in spec.controls} == {"refused", "sorry"}
    assert {control.name for control in spec.controls} >= {
        "mutated-statement",
        "mutated-module",
        "sorry",
    }


def test_a_changed_byte_is_refused_with_the_control_built_from_it(tmp_path: Path) -> None:
    spec = rlp.route("chelokot-small-n")
    assert rlp.stage(spec, tmp_path)["ok"]
    square5 = tmp_path / "formal/SquarePackingArchive/Records/Square5.lean"
    square5.write_text(
        square5.read_text(encoding="utf-8").replace("Real.sqrt 2 / 2", "Real.sqrt 2 / 2 ", 1),
        encoding="utf-8",
    )
    problems = rlp.verify(spec, tmp_path)["problems"]
    assert any("Square5.lean: SHA-256" in p for p in problems)
    assert any("Square5.lean: Git blob" in p for p in problems)
    assert any("Square5Mutant.lean is not the route's control" in p for p in problems)


def test_a_mutation_that_does_not_occur_exactly_once_is_refused(tmp_path: Path) -> None:
    spec = rlp.route("evand-rect-small-n")
    rlp.stage(spec, tmp_path)
    control = next(c for c in spec.controls if c.source)
    broken = rlp.Control(
        name=control.name,
        kind=control.kind,
        path=control.path,
        what=control.what,
        source=control.source,
        old="no such text",
        new="x",
    )
    with pytest.raises(SystemExit, match="occurs 0 times"):
        rlp.control_text(broken, tmp_path)


def test_axiom_lines_parse_across_wrapped_lists() -> None:
    text = (
        "'A.b' depends on axioms: [propext,\n Classical.choice,\n Quot.sound]\n"
        f"'A.c' depends on axioms: {STANDARD}\n"
        "'A.d' does not depend on any axioms\n"
    )
    found = rlp.parse_axioms(text)
    assert found["A.b"] == ["propext", "Classical.choice", "Quot.sound"]
    assert found["A.d"] == []
    assert rlp.axiom_problems(["A.b", "A.c"], found) == []
    assert rlp.axiom_problems(["A.d", "A.e"], found) == [
        "A.d: axioms []",
        "A.e: no axiom line printed",
    ]


def test_only_the_three_standard_axioms_are_accepted() -> None:
    found = rlp.parse_axioms(
        "'A.b' depends on axioms: [propext, sorryAx, Classical.choice, Quot.sound]\n"
        "'A.c' depends on axioms: [propext, Classical.choice, Lean.ofReduceBool, Quot.sound]\n"
    )
    assert len(rlp.axiom_problems(["A.b", "A.c"], found)) == 2


@pytest.mark.parametrize(
    ("kind", "exit_code", "text", "refused"),
    [
        ("refused", 1, "Controls.lean:3:2: error: type mismatch", True),
        ("refused", 0, "", False),
        ("refused", 1, "error: unknown module prefix 'Sqpack'", False),
        ("refused", 1, "error: object file .lake/build/lib/X.olean does not exist", False),
        ("sorry", 0, "'control_sorry' depends on axioms: [propext, sorryAx, Quot.sound]", True),
        ("sorry", 0, f"'control_sorry' depends on axioms: {STANDARD}", False),
        ("sorry", 1, "error: unknown identifier", False),
    ],
)
def test_a_control_counts_only_when_refused_for_its_own_reason(
    kind: str, exit_code: int, text: str, *, refused: bool
) -> None:
    assert rlp.control_refused(kind, exit_code, text) is refused


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _receipt(tmp_path: Path, spec: rlp.Route) -> Path:
    """A synthetic passing receipt for ``spec``, in the shape ``run`` writes."""
    receipts = tmp_path / "receipts"
    receipts.mkdir()
    probe = "".join(f"'{name}' depends on axioms: {STANDARD}\n" for name in spec.theorems)
    (receipts / "probe.log").write_text(probe, encoding="utf-8")
    (receipts / "build-0.log").write_text("Build completed successfully.\n", encoding="utf-8")
    steps = [
        {"name": name, "log": f"{name}.log", "exit": 0, "cpu_seconds": 1.0, "wall_seconds": 1.0}
        for name in ("build-0", "probe")
    ]
    for step in steps:
        step["log_sha256"] = _sha256(receipts / str(step["log"]))
    controls = []
    for control in spec.controls:
        log = receipts / f"control-{control.name}.log"
        if control.kind == "sorry":
            log.write_text(
                "warning: declaration uses 'sorry'\n'control_sorry' depends on axioms: "
                "[propext, sorryAx, Classical.choice, Quot.sound]\n",
                encoding="utf-8",
            )
            code = 0
        else:
            log.write_text("error: type mismatch\n", encoding="utf-8")
            code = 1
        controls.append(
            {
                "name": f"control-{control.name}",
                "control": control.name,
                "kind": control.kind,
                "log": log.name,
                "log_sha256": _sha256(log),
                "exit": code,
                "refused": True,
            }
        )
    receipt = {
        "kind": rlp.KIND,
        "route": spec.name,
        "result": spec.result,
        "toolchain": spec.toolchain,
        "mathlib": spec.mathlib,
        "mathlib_checked_out": spec.mathlib,
        "theorems": list(spec.theorems),
        "axioms": rlp.parse_axioms(probe),
        "steps": steps,
        "controls": controls,
        "verdict": "passed",
    }
    (receipts / rlp.RECEIPT_NAME).write_text(json.dumps(receipt), encoding="utf-8")
    return receipts


def test_a_passing_receipt_checks_and_each_tampering_is_caught(tmp_path: Path) -> None:
    spec = rlp.route("chelokot-small-n")
    receipts = _receipt(tmp_path, spec)
    assert rlp.check(spec, receipts) == []

    probe = receipts / "probe.log"
    probe.write_text(
        probe.read_text(encoding="utf-8").replace("Quot.sound]", "Quot.sound, sorryAx]", 1),
        encoding="utf-8",
    )
    problems = rlp.check(spec, receipts)
    assert "probe: log probe.log does not match its digest" in problems
    assert any("sorryAx" in p for p in problems)


def test_a_control_that_was_not_refused_fails_the_check(tmp_path: Path) -> None:
    spec = rlp.route("evand-rect-small-n")
    receipts = _receipt(tmp_path, spec)
    data = json.loads((receipts / rlp.RECEIPT_NAME).read_text(encoding="utf-8"))
    mutated = next(c for c in data["controls"] if c["control"] == "mutated-statement")
    mutated["exit"] = 0
    data["controls"] = [c for c in data["controls"] if c["control"] != "sorry"]
    (receipts / rlp.RECEIPT_NAME).write_text(json.dumps(data), encoding="utf-8")
    problems = rlp.check(spec, receipts)
    assert "control mutated-statement: its log does not show it refused" in problems
    assert "control sorry did not run" in problems


def test_a_route_with_a_generator_needs_its_generation_receipt(tmp_path: Path) -> None:
    spec = rlp.route("wand125-n21")
    receipts = _receipt(tmp_path, spec)
    assert rlp.check(spec, receipts) == [
        "the generation receipt does not show the listed digests matched"
    ]
    assert rlp.check_generation(spec, receipts) == [
        f"{receipts / rlp.GENERATION_NAME}: no generation receipt"
    ]
