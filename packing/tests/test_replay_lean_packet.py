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
    # Every upstream library module is held to its Git blob; Hosono's two files are his
    # packet's own, whose custody is acquire_source's.
    modules = [s for s in spec.files if s.path.endswith(".lean") and "N21Pts" not in s.path]
    assert modules
    assert all(staged.blob for staged in modules)
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
    assert any("Square5.lean: Git blob" in p for p in problems)
    assert any("Square5Mutant.lean is not the route's control" in p for p in problems)


def test_a_substituted_file_not_the_scripts_pin_is_refused(tmp_path: Path) -> None:
    spec = rlp.route("wand125-n21")
    assert rlp.stage(spec, tmp_path)["ok"]
    oracle = tmp_path / "s12/search/zeromargin.py"
    oracle.write_text(oracle.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    manifest = tmp_path / "s12/lean/lake-manifest.json"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace("0df444a3", "0df444a4", 1),
        encoding="utf-8",
    )
    problems = rlp.verify(spec, tmp_path)["problems"]
    assert "s12/search/zeromargin.py: not the bytes build_zero_margin.sh pins" in problems
    assert "the manifest's package revisions are not the closure receipt's" in problems


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


def _log(path: Path, body: str, code: int) -> None:
    """A log in ``devtools.replay_receipt``'s shape."""
    path.write_text(
        "# command: lake env lean X.lean\n# cwd: test\n# python3: not used by this command\n"
        "# host: 4 cores; load 0.00 0.00 0.00; started 2026-11-02T00:00:00Z\n"
        f"{body}"
        f"# finished 2026-11-02T00:00:01Z; exit {code}; wall 1.000 s; CPU 0.9 s "
        "(user 0.800 + sys 0.100); load 0.00 0.00 0.00\n",
        encoding="utf-8",
    )


def test_the_footer_of_a_receipt_log_is_read_back(tmp_path: Path) -> None:
    _log(tmp_path / "x.log", "error: type mismatch\n", 1)
    assert rlp.footer(tmp_path / "x.log") == {
        "command": "lake env lean X.lean",
        "started_utc": "2026-11-02T00:00:00Z",
        "ended_utc": "2026-11-02T00:00:01Z",
        "exit": 1,
        "wall_seconds": 1.0,
        "cpu_seconds": 0.9,
    }


def _receipt(tmp_path: Path, spec: rlp.Route) -> Path:
    """A synthetic passing receipt for ``spec``, in the shape ``run`` writes."""
    receipts = tmp_path / "receipts"
    receipts.mkdir()
    probe = "".join(f"'{name}' depends on axioms: {STANDARD}\n" for name in spec.theorems)
    _log(receipts / "probe.log", probe, 0)
    _log(receipts / "build-0.log", "Build completed successfully.\n", 0)
    steps = [
        {"name": name, "log": f"{name}.log", "exit": 0, "cpu_seconds": 1.0, "wall_seconds": 1.0}
        for name in ("build-0", "probe")
    ]
    controls = []
    for control in spec.controls:
        log = receipts / f"control-{control.name}.log"
        if control.kind == "sorry":
            body = (
                "warning: declaration uses 'sorry'\n'control_sorry' depends on axioms: "
                "[propext, sorryAx, Classical.choice, Quot.sound]\n"
            )
            code = 0
        else:
            body, code = "error: type mismatch\n", 1
        _log(log, body, code)
        controls.append(
            {
                "name": f"control-{control.name}",
                "control": control.name,
                "kind": control.kind,
                "log": log.name,
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
    assert "the receipt's axioms are not what probe.log prints" in problems
    assert any("sorryAx" in p for p in problems)

    _log(receipts / "build-0.log", "error: build failed\n", 1)
    assert "build-0: its log's exit is not the receipt's" in rlp.check(spec, receipts)


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
        "the generation receipt does not show every listed file generated"
    ]
    assert rlp.check_generation(spec, receipts) == [
        f"{receipts / rlp.GENERATION_NAME}: no generation receipt"
    ]


def test_compare_finds_a_generated_file_that_differs_from_the_listing(tmp_path: Path) -> None:
    spec = rlp.route("wand125-n21")
    assert spec.generation is not None
    out, receipts = tmp_path / "stage", tmp_path / "receipts"
    out.mkdir()
    receipts.mkdir()
    outdir = out / spec.generation.outdir
    outdir.mkdir(parents=True)
    rows = []
    for name, text in (("Part0.lean", "a\n"), ("Part1.lean", "b\n")):
        (outdir / name).write_text(text, encoding="utf-8")
        rows.append(f"{hashlib.sha256(text.encode()).hexdigest()}  {name}")
    (out / spec.generation.listing).write_text("\n".join(rows) + "\n", encoding="utf-8")
    _log(receipts / "gen.log", "  625/625 cells 1s\n", 0)
    report = rlp.compare(spec, out, receipts)
    assert report["ok"]
    assert (report["listed"], report["matched"]) == (2, 2)

    (outdir / "Part1.lean").write_text("c\n", encoding="utf-8")
    (outdir / "Part2.lean").write_text("d\n", encoding="utf-8")
    report = rlp.compare(spec, out, receipts)
    assert not report["ok"]
    assert report["differing"] == ["Part1.lean"]
    assert report["extra"] == ["Part2.lean"]
    # The fixture's listing is not the retained one, which lists 66 files.
    assert "the receipt did not compare all 66 listed files" in rlp.check_generation(
        spec, receipts
    )
    assert "the generated files are not exactly the listed ones" in rlp.check_generation(
        spec, receipts
    )


def test_the_retained_generation_receipt_shows_every_listed_part_regenerated() -> None:
    spec = rlp.route("wand125-n21")
    receipts = rlp.WEB / spec.packet / rlp.RECEIPT_DIR
    assert rlp.check_generation(spec, receipts) == []
    gen = json.loads((receipts / rlp.GENERATION_NAME).read_text(encoding="utf-8"))
    assert (gen["listed"], gen["matched"], gen["generated"], gen["exit"]) == (66, 66, 66, 0)
