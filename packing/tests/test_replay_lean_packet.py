# ruff: noqa: RUF001 -- the Lean statements are written with Lean's own Unicode signs.
"""Staging and receipting three packets' Lean proofs from retained bytes.

``devtools.replay_lean_packet`` stages chelokot's and Daniel's small-n proofs (T-238) and
Hosono's s(21) = 5 (T-234) from the retained packets, binding each file that has an
upstream identity to its Git blob, and accepts a build only with the registered
statements, the three standard axioms and every negative control refused for its own
reason. These tests hold the staging, the acceptance, ``run`` against a stub ``lake``
that records its calls, and the offline checks; a real build needs Lean and the Mathlib
cache, and no test does.
"""

from __future__ import annotations

import hashlib
import json
import os
import shlex
import shutil
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


def test_a_substituted_file_not_at_its_upstream_blob_is_refused(tmp_path: Path) -> None:
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
    assert any(p.startswith("s12/search/zeromargin.py: Git blob") for p in problems)
    assert "the manifest's package revisions are not the closure receipt's" in problems


def test_the_generator_oracle_and_theorem_module_are_bound_by_upstream_git_blob() -> None:
    """Review A1: Git identities only, no SHA-256 pin, and no integrity-ceremony entry."""
    spec = rlp.route("wand125-n21")
    staged = {s.path: s for s in spec.files}
    generator = staged["s12/lean/scripts/gen_zmtree.py"]
    assert generator.blob == "06f22b4de2497b723e73f760dbb58125cd400336"
    # Staged from the 28 September packet, whose pin is 6aa82ba4 itself.
    assert "/evand-square-packing-2026-09-28/" in generator.origin
    oracle = staged["s12/search/zeromargin.py"]
    manifest = rlp.WEB / "evand-square-packing-2026-10-01/source-manifest.tsv"
    rows = [line.split("\t") for line in manifest.read_text(encoding="utf-8").splitlines()]
    assert oracle.blob == next(r[1] for r in rows if r[0] == "s12/search/zeromargin.py")
    assert staged["s12/lean/Sqpack/N21PtsLower.lean"].blob == (
        "356ce914107db7c522d979e09c5df1f5ac4c1e63"
    )
    assert staged["s12/lean/Sqpack/ZMTree.lean"].blob
    assert set(rlp.Staged.__dataclass_fields__) == {"path", "origin", "blob"}
    register = (rlp.REPO / "packing/devtools/integrity-ceremony.yaml").read_text(
        encoding="utf-8"
    )
    assert "packing/devtools/replay_lean_packet.py" not in register


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


def test_checked_statements_parse_across_wrapped_lines_and_compare_by_their_tokens() -> None:
    """Review A3: `#check @thm` prints `Name : type`, wrapped by the pretty-printer."""
    text = (
        "SquarePacking.n21pts_ge_5 : 5 ≤ SquarePacking.minSide 21\n"
        "SquarePacking.rect2_iff : ∀ {w h : ℝ},\n"
        "  SquarePacking.RectPacks 2 w h ↔ 1 ≤ w ∧ 1 ≤ h ∧ (2 ≤ w ∨ 2 ≤ h)\n"
        f"'SquarePacking.n21pts_ge_5' depends on axioms: {STANDARD}\n"
    )
    names = ("SquarePacking.n21pts_ge_5", "SquarePacking.rect2_iff")
    printed = rlp.parse_statements(text, names)
    assert printed["SquarePacking.n21pts_ge_5"] == "5 ≤ SquarePacking.minSide 21"
    assert printed["SquarePacking.rect2_iff"].endswith("(2 ≤ w ∨ 2 ≤ h)")
    assert rlp.same_statement("2 + Real.sqrt 2 / 2", "2 + √2 / 2")
    assert not rlp.same_statement("1 ≤ w ∧ (2 ≤ w ∨ 2 ≤ h)", "1 ≤ w ∧ 2 ≤ w ∨ 2 ≤ h")


@pytest.mark.parametrize(
    "line",
    [
        "private axiom bad : False",
        "@[simp] axiom bad : False",
        '@[inline, extern "c_bad"] def bad : Nat := 0',
        "noncomputable axiom bad : False",
    ],
)
def test_modifier_prefixed_axioms_and_late_externs_are_escapes(
    line: str, tmp_path: Path
) -> None:
    """Review A6: the narrow `^axiom` and `@[extern` patterns missed these."""
    path = tmp_path / "X.lean"
    path.write_text(f"theorem ok : True := trivial\n{line}\n", encoding="utf-8")
    assert sum(rlp.escape_counts([path]).values()) >= 1


def test_a_lakefile_that_switches_off_the_kernel_is_refused(tmp_path: Path) -> None:
    """Review A6: `[leanOptions]` can carry what no `.lean` file shows."""
    spec = rlp.route("evand-rect-small-n")
    assert rlp.stage(spec, tmp_path)["ok"]
    lakefile = tmp_path / "lean/lakefile.toml"
    lakefile.write_text(
        lakefile.read_text(encoding="utf-8").replace(
            "[leanOptions]\n", "[leanOptions]\ndebug.skipKernelTC = true\n"
        ),
        encoding="utf-8",
    )
    problems = rlp.verify(spec, tmp_path)["problems"]
    assert any("lakefile" in p and "skipKernelTC" in p for p in problems)


def test_an_escape_injected_into_the_theorem_module_is_found_by_the_scan(
    tmp_path: Path,
) -> None:
    """Review A7: the scan, not only the blob, catches it."""
    spec = rlp.route("wand125-n21")
    assert rlp.stage(spec, tmp_path)["ok"]
    lower = tmp_path / "s12/lean/Sqpack/N21PtsLower.lean"
    lower.write_text(
        lower.read_text(encoding="utf-8") + "\nprivate axiom cheat : False\n", encoding="utf-8"
    )
    problems = rlp.verify(spec, tmp_path)["problems"]
    assert any("in the staged sources" in p and "axiom" in p for p in problems)


def test_the_lean_options_become_d_flags() -> None:
    """Review A2: controls and probe run with the package's own options."""
    chelokot = rlp.route("chelokot-small-n")
    lakefile = rlp.REPO / next(
        s.origin for s in chelokot.files if s.path.endswith("lakefile.toml")
    )
    assert rlp.lean_option_flags(lakefile) == []
    rect = rlp.route("evand-rect-small-n")
    lakefile = rlp.REPO / next(s.origin for s in rect.files if s.path.endswith("lakefile.toml"))
    flags = rlp.lean_option_flags(lakefile)
    assert "-DmaxSynthPendingDepth=3" in flags
    assert "-DrelaxedAutoImplicit=false" in flags


def _log(path: Path, body: str, code: int, command: str = "lake env lean X.lean") -> None:
    """A log in ``devtools.replay_receipt``'s shape."""
    path.write_text(
        f"# command: {command}\n# cwd: test\n# python3: not used by this command\n"
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


#: A stand-in for lake, after the one review A's probe used: it records each call and
#: replays, for `lake env lean ... FILE`, the output and exit code the test left for
#: FILE's stem in $STUB_DIR.
STUB_LAKE = """#!/bin/sh
d="$STUB_DIR"
echo "$*" >> "$d/calls.txt"
case "$1" in
  --version) echo "Lake version 5.0.0-stub"; exit 0 ;;
  exe) echo "cache ok"; exit 0 ;;
  build) shift; echo "$*" >> "$d/builds.txt"; echo "Build completed successfully."; exit 0 ;;
  env)
    shift; shift
    last=""
    for a in "$@"; do last="$a"; done
    if [ "$last" = "--version" ]; then cat "$d/version.out"; exit 0; fi
    key=$(basename "$last" .lean)
    if [ -f "$d/$key.out" ]; then cat "$d/$key.out"; fi
    if [ -f "$d/$key.code" ]; then exit "$(cat "$d/$key.code")"; fi
    exit 0 ;;
esac
echo "stub lake: unhandled $*" >&2
exit 2
"""


class Stub:
    """A stub lake on PATH and the canned outputs a passing run of ``spec`` needs."""

    def __init__(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, spec: rlp.Route
    ) -> None:
        self.dir = tmp_path / "stub"
        self.dir.mkdir()
        lake = self.dir / "lake"
        lake.write_text(STUB_LAKE, encoding="utf-8")
        lake.chmod(0o755)
        monkeypatch.setenv("PATH", f"{self.dir}{os.pathsep}{os.environ['PATH']}")
        monkeypatch.setenv("STUB_DIR", str(self.dir))
        monkeypatch.setattr(rlp, "resolved_mathlib", lambda _project: spec.mathlib)
        self.spec = spec
        version = spec.toolchain.split(":v")[1]
        self.put(
            "version",
            f"Lean (version {version}, x86_64-unknown-linux-gnu, commit {spec.lean_commit}, "
            "Release)\n",
        )
        self.put(
            "Probe",
            "".join(f"{n} : {spec.statements.get(n, 'True')}\n" for n in spec.theorems)
            + "".join(f"'{n}' depends on axioms: {STANDARD}\n" for n in spec.theorems),
        )
        for control in spec.controls:
            stem = Path(control.path).stem
            if control.kind == "sorry":
                self.put(
                    stem,
                    f"{control.path}:3:8: warning: declaration uses 'sorry'\n"
                    "'control_sorry' depends on axioms: "
                    "[propext, sorryAx, Classical.choice, Quot.sound]\n",
                )
            elif control.source:
                line = rlp.mutated_line(control, rlp.REPO / spec_origin(spec, control.source))
                self.put(stem, f"{control.path}:{line}:2: error: linarith failed\n", 1)
                self.put(f"{stem}Twin", "")
            else:
                self.put(stem, f"{control.path}:3:2: error: type mismatch\n  x\n", 1)

    def put(self, stem: str, text: str, code: int = 0) -> None:
        (self.dir / f"{stem}.out").write_text(text, encoding="utf-8")
        (self.dir / f"{stem}.code").write_text(f"{code}\n", encoding="utf-8")

    def lines(self, name: str) -> list[str]:
        path = self.dir / name
        return path.read_text(encoding="utf-8").splitlines() if path.is_file() else []


def spec_origin(spec: rlp.Route, staged_path: str) -> str:
    return next(s.origin for s in spec.files if s.path == staged_path)


def _run(spec: rlp.Route, tmp_path: Path, *, jobs: int = 1) -> tuple[dict, Path]:
    receipts = tmp_path / "receipts"
    report = rlp.run(
        spec, tmp_path / "stage", receipts, cpus=None, jobs=jobs, cpu_hours_cap=1.0
    )
    return report, receipts


def test_run_against_a_stub_lake_passes_and_its_receipt_checks(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Review A7: the sequence, the probe, the controls and their twins, the verdict."""
    spec = rlp.route("chelokot-small-n")
    stub = Stub(tmp_path, monkeypatch, spec)
    assert rlp.stage(spec, tmp_path / "stage")["ok"]
    report, receipts = _run(spec, tmp_path)
    assert report["verdict"] == "passed", report["problems"]
    assert [step["name"] for step in report["steps"]] == ["cache", "build-0", "probe"]
    assert report["statements"]["SquarePackingArchive.Records.Square5.s5_eq_goebel"]
    twins = [c["twin"] for c in report["controls"] if c.get("twin")]
    assert len(twins) == 1
    assert twins[0]["exit"] == 0
    assert any("Square5MutantTwin.lean" in line for line in stub.lines("calls.txt"))
    assert rlp.check(spec, receipts) == []


def test_run_passes_the_lakefiles_lean_options_to_probe_and_controls(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Review A2: no bare `lake env lean` for evand's options-bearing package."""
    spec = rlp.route("evand-rect-small-n")
    stub = Stub(tmp_path, monkeypatch, spec)
    rlp.stage(spec, tmp_path / "stage")
    report, _ = _run(spec, tmp_path)
    assert report["verdict"] == "passed", report["problems"]
    leans = [line for line in stub.lines("calls.txt") if line.startswith("env lean -D")]
    assert len(leans) == 1 + len(spec.controls) + 1  # probe, controls, one twin
    assert all("-DmaxSynthPendingDepth=3" in line for line in leans)


@pytest.mark.parametrize(
    ("stem", "text", "code", "twin_code"),
    [
        # A mutated module that fails for a setup reason, the review's probe.
        (
            "Square5Mutant",
            "error: unknown identifier 'SquarePackingArchive.IsMinimumSide'\n",
            1,
            0,
        ),
        # An error located before the mutated declaration says nothing about it.
        ("Square5Mutant", "controls/Square5Mutant.lean:1:0: error: unexpected token\n", 1, 0),
        # A mutant whose unmutated twin fails too.
        ("Square5Mutant", None, 1, 1),
        # A mutated statement refused for a reason other than its type.
        (
            "MutatedStatement",
            "controls/MutatedStatement.lean:3:2: error: unknown constant\n",
            1,
            0,
        ),
        # A sorry control without the warning Lean gives a sorry.
        ("Sorry", "'control_sorry' depends on axioms: [sorryAx]\n", 0, 0),
    ],
)
def test_a_control_counts_only_when_refused_for_its_intended_reason(
    stem: str,
    text: str | None,
    *,
    code: int,
    twin_code: int,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Review A2: any error used to count as a refusal."""
    spec = rlp.route("chelokot-small-n")
    stub = Stub(tmp_path, monkeypatch, spec)
    if text is not None:
        stub.put(stem, text, code)
    stub.put("Square5MutantTwin", "controls/Square5MutantTwin.lean:9:0: error: x\n", twin_code)
    rlp.stage(spec, tmp_path / "stage")
    report, receipts = _run(spec, tmp_path)
    assert report["verdict"] == "failed"
    assert any(p.startswith("control ") for p in report["problems"])
    assert rlp.check(spec, receipts)


def test_a_printed_statement_that_is_not_the_registered_one_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Review A3: the receipt binds what was proved, not only its axioms."""
    spec = rlp.route("chelokot-small-n")
    stub = Stub(tmp_path, monkeypatch, spec)
    name = "SquarePackingArchive.Records.Square5.s5_eq_goebel"
    probe = (stub.dir / "Probe.out").read_text(encoding="utf-8")
    stub.put("Probe", probe.replace(f"{name} : {spec.statements[name]}", f"{name} : True"))
    rlp.stage(spec, tmp_path / "stage")
    report, receipts = _run(spec, tmp_path)
    assert report["verdict"] == "failed"
    assert any(p.startswith(f"{name}: printed") for p in report["problems"])
    assert any(p.startswith(f"{name}: printed") for p in rlp.check(spec, receipts))


def test_a_lean_from_another_commit_fails_the_run_and_the_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Review A5: the measured toolchain is checked, not a copy of the declared one."""
    spec = rlp.route("chelokot-small-n")
    stub = Stub(tmp_path, monkeypatch, spec)
    stub.put(
        "version", "Lean (version 4.33.0, x86_64-unknown-linux-gnu, commit 0000, Release)\n"
    )
    rlp.stage(spec, tmp_path / "stage")
    report, receipts = _run(spec, tmp_path)
    assert report["verdict"] == "failed"
    assert any("lean_version" in p for p in rlp.check(spec, receipts))
    monkeypatch.setattr(rlp, "resolved_mathlib", lambda _project: "0" * 40)
    report, receipts = _run(spec, tmp_path)
    assert any("Mathlib resolved at" in p for p in rlp.check(spec, receipts))


def test_run_stops_before_any_lake_call_when_the_stage_is_wrong(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Review A9: a known-bad stage costs nothing."""
    spec = rlp.route("chelokot-small-n")
    stub = Stub(tmp_path, monkeypatch, spec)
    rlp.stage(spec, tmp_path / "stage")
    square5 = tmp_path / "stage/formal/SquarePackingArchive/Records/Square5.lean"
    square5.write_text(square5.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    report, _ = _run(spec, tmp_path)
    assert report["verdict"] == "failed"
    assert report["steps"] == []
    assert stub.lines("calls.txt") == []


def _fake_generation(spec: rlp.Route, out: Path, parts: int) -> Path:
    """Generated files and a listing of them in place of the 66 real ones."""
    assert spec.generation is not None
    outdir = out / spec.generation.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    rows = []
    for name in ["Pts.lean", "Cov.lean", *(f"Part{i}.lean" for i in range(parts))]:
        text = f"-- {name}\ntheorem t : True := trivial\n"
        (outdir / name).write_text(text, encoding="utf-8")
        rows.append(f"{hashlib.sha256(text.encode()).hexdigest()}  {name}")
    (out / spec.generation.listing).write_text("\n".join(rows) + "\n", encoding="utf-8")
    return outdir


def test_run_builds_each_generated_part_in_batches_after_rehashing_it(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Review A4 and A7: the parts are the listed ones before anything builds."""
    spec = rlp.route("wand125-n21")
    stub = Stub(tmp_path, monkeypatch, spec)
    rlp.stage(spec, tmp_path / "stage")
    _fake_generation(spec, tmp_path / "stage", parts=5)
    report, _ = _run(spec, tmp_path, jobs=2)
    assert report["verdict"] == "passed", report["problems"]
    assert report["generated"]["matched"] == report["generated"]["listed"] == 7
    assert stub.lines("builds.txt") == [
        "Sqpack.N21PtsZ.Pts",
        "Sqpack.N21PtsZ.Part0 Sqpack.N21PtsZ.Part1",
        "Sqpack.N21PtsZ.Part2 Sqpack.N21PtsZ.Part3",
        "Sqpack.N21PtsZ.Part4",
        "Sqpack.N21PtsLower",
    ]


@pytest.mark.parametrize("fault", ["differing", "escape"])
def test_run_refuses_generated_parts_before_building(
    fault: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Review A4: a part not on the listing, or one carrying an escape, stops the run."""
    spec = rlp.route("wand125-n21")
    stub = Stub(tmp_path, monkeypatch, spec)
    rlp.stage(spec, tmp_path / "stage")
    outdir = _fake_generation(spec, tmp_path / "stage", parts=3)
    part = outdir / "Part1.lean"
    if fault == "differing":
        part.write_text(part.read_text(encoding="utf-8") + "-- edited\n", encoding="utf-8")
    else:
        text = "theorem t : False := by sorry\n"
        part.write_text(text, encoding="utf-8")
        listing = tmp_path / "stage/data-sha256.txt"
        rows = [
            f"{hashlib.sha256(text.encode()).hexdigest()}  Part1.lean"
            if row.endswith("  Part1.lean")
            else row
            for row in listing.read_text(encoding="utf-8").splitlines()
        ]
        listing.write_text("\n".join(rows) + "\n", encoding="utf-8")
    report, _ = _run(spec, tmp_path)
    assert report["verdict"] == "failed"
    assert stub.lines("builds.txt") == []
    assert any("generated" in p for p in report["problems"])


def test_check_generation_rederives_its_facts_and_refuses_a_forged_log(tmp_path: Path) -> None:
    """Review A4: the reviewer's forged gen.log printed OK."""
    spec = rlp.route("wand125-n21")
    retained = rlp.WEB / spec.packet / rlp.RECEIPT_DIR
    receipts = tmp_path / "receipts"
    shutil.copytree(retained, receipts)
    assert rlp.check_generation(spec, receipts) == []
    _log(receipts / "gen.log", "", 0, command="true")
    problems = rlp.check_generation(spec, receipts)
    assert any("command" in p for p in problems)
    assert any("gen.log" in p and "times" in p for p in problems)
    gen = json.loads((receipts / rlp.GENERATION_NAME).read_text(encoding="utf-8"))
    gen["listing_blob"] = "0" * 40
    (receipts / rlp.GENERATION_NAME).write_text(json.dumps(gen), encoding="utf-8")
    assert any("listing" in p for p in rlp.check_generation(spec, receipts))


def test_compare_finds_a_generated_file_that_differs_from_the_listing(tmp_path: Path) -> None:
    spec = rlp.route("wand125-n21")
    assert spec.generation is not None
    out, receipts = tmp_path / "stage", tmp_path / "receipts"
    out.mkdir()
    receipts.mkdir()
    outdir = _fake_generation(spec, out, parts=2)
    command = shlex.join(["python3", *(a.format(nproc=2) for a in spec.generation.argv)])
    _log(receipts / "gen.log", "  625/625 cells 1s\n", 0, command=command)
    report = rlp.compare(spec, out, receipts)
    assert report["ok"]
    assert (report["listed"], report["matched"]) == (4, 4)

    (outdir / "Part1.lean").write_text("c\n", encoding="utf-8")
    (outdir / "Part2.lean").write_text("d\n", encoding="utf-8")
    report = rlp.compare(spec, out, receipts)
    assert not report["ok"]
    assert report["differing"] == ["Part1.lean"]
    assert report["extra"] == ["Part2.lean"]
    problems = rlp.check_generation(spec, receipts)
    # The fixture's listing is not the retained one, which lists 66 files.
    assert any("listing" in p for p in problems)
    assert "the generated files are not exactly the listed ones" in problems


def test_the_retained_generation_receipt_shows_every_listed_part_regenerated() -> None:
    spec = rlp.route("wand125-n21")
    receipts = rlp.WEB / spec.packet / rlp.RECEIPT_DIR
    assert rlp.check_generation(spec, receipts) == []
    gen = json.loads((receipts / rlp.GENERATION_NAME).read_text(encoding="utf-8"))
    assert (gen["listed"], gen["matched"], gen["generated"], gen["exit"]) == (66, 66, 66, 0)
    assert gen["census"] == {"chunks": 2076, "parts": 64, "Z": 59433, "E": 5876, "C": 5591}
    assert set(gen["escapes"].values()) == {0}
