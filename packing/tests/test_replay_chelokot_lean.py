# ruff: noqa: RUF001 -- the Lean statement is matched as written, with its natural-number sign.
"""The Lean replay tool: its axiom-output parser and its offline receipt check.

The check is exercised on receipts built here, so each rule is shown to fire on the one
fault it names, and once on the receipt the repository retains.
"""

from __future__ import annotations

import copy
import hashlib
import json
import time
from pathlib import Path
from typing import Any

import pytest

from devtools import replay_chelokot_lean as replay

STANDARD: list[str] = list(replay.STANDARD_AXIOMS)


# --- The axiom-output parser ---------------------------------------------------------


def test_parser_reads_one_standard_report() -> None:
    text = "'Foo.bar' depends on axioms: [propext, Classical.choice, Quot.sound]"
    assert replay.parse_print_axioms(text) == {"Foo.bar": replay.STANDARD_AXIOMS}


def test_parser_reads_a_declaration_with_no_axioms() -> None:
    text = "'Foo.bar' does not depend on any axioms"
    assert replay.parse_print_axioms(text) == {"Foo.bar": ()}


def test_parser_reads_several_reports_among_other_output() -> None:
    text = (
        "Foo.theorem {n : ℕ} : 0 < n\n"
        "'Foo.a' depends on axioms: [propext]\n"
        "'Foo.b' does not depend on any axioms\n"
        "'Foo.c' depends on axioms: [Quot.sound, propext, propext]"
    )
    assert replay.parse_print_axioms(text) == {
        "Foo.a": ("propext",),
        "Foo.b": (),
        "Foo.c": ("Quot.sound", "propext"),
    }


def test_parser_joins_a_report_that_lean_wrapped_across_lines() -> None:
    text = "'Foo.bar' depends on axioms: [propext,\n  Classical.choice,\n  Quot.sound]"
    assert replay.parse_print_axioms(text) == {"Foo.bar": replay.STANDARD_AXIOMS}


def test_parser_keeps_sorryax_and_custom_axioms_visible() -> None:
    text = "'Foo.bar' depends on axioms: [propext, sorryAx, My.axiom]"
    assert replay.parse_print_axioms(text) == {"Foo.bar": ("My.axiom", "propext", "sorryAx")}


def test_parser_round_trips_the_formatter() -> None:
    for axioms in ([], ["propext"], STANDARD, [*STANDARD, "sorryAx"]):
        line = replay.format_axioms_report("Foo.bar", axioms)
        assert replay.parse_print_axioms(line) == {"Foo.bar": tuple(sorted(axioms))}


def test_parser_refuses_a_truncated_report_rather_than_skipping_it() -> None:
    with pytest.raises(ValueError, match="did not match"):
        replay.parse_print_axioms("'Foo.bar' depends on axioms: [propext, sorryAx")


def test_parser_refuses_one_declaration_reported_two_ways() -> None:
    text = "'Foo.bar' depends on axioms: [propext]\n'Foo.bar' depends on axioms: [sorryAx]"
    with pytest.raises(ValueError, match="twice"):
        replay.parse_print_axioms(text)


def test_parser_finds_nothing_in_unrelated_output() -> None:
    assert replay.parse_print_axioms("Build completed successfully (2944 jobs).") == {}


# --- Output handling -----------------------------------------------------------------


def test_tidy_output_keeps_the_last_state_of_a_progress_line() -> None:
    raw = "a\nDownloaded: 1\rDownloaded: 2\r\x1b[KDownloaded: 3\x1b[K\nb\n\n"
    assert replay.tidy_output(raw) == "a\nDownloaded: 3\nb"


def test_trim_output_elides_the_middle_only_when_too_long() -> None:
    short = "\n".join(str(number) for number in range(10))
    long = "\n".join(str(number) for number in range(100))
    trimmed = replay.trim_output(long, head=2, tail=3).split("\n")
    assert trimmed == ["0", "1", "[... 95 lines elided ...]", "97", "98", "99"]
    assert replay.trim_output(short, head=10, tail=0) == short


def test_source_statement_stops_at_the_proof() -> None:
    source = "namespace X\n" + replay.THEOREM_SOURCE + " := by\n  simp\n"
    assert replay.source_statement(source) == replay.THEOREM_SOURCE
    assert replay.source_statement("theorem other : True := trivial") is None


def test_elaborated_statement_is_cut_before_the_next_report_and_joined() -> None:
    wrapped = replay.THEOREM_ELABORATED.replace(" :", " :\n ", 2).replace(
        " (size_lower", "\n  (size_lower"
    )
    output = wrapped + "\n'" + replay.THEOREM + "' depends on axioms: [propext]"
    assert "\n" in wrapped
    assert replay.elaborated_statement(output) == replay.THEOREM_ELABORATED
    assert replay.elaborated_statement("nothing here") is None


def test_scratch_sources_name_the_theorem_and_every_instance() -> None:
    source = replay.axioms_source()
    assert f"#print axioms {replay.THEOREM}" in source
    assert f"assert_standard_axioms {replay.THEOREM}" in source
    for declaration in replay.INSTANCE_DECLARATIONS:
        assert f"#print axioms {declaration}" in source
    for count, size in replay.REPLAY_INSTANCES:
        assert size * size - 2 == count
    assert "#print SquarePackingArchive.Packing\n" in replay.definitions_source()


def test_source_scan_counts_what_the_archive_policy_forbids(tmp_path: Path) -> None:
    library = tmp_path / "SquarePackingArchive"
    library.mkdir()
    (tmp_path / "SquarePackingArchive.lean").write_text("import SquarePackingArchive.A\n")
    (library / "A.lean").write_text(
        "-- the axiom of choice is used; sorry is not\n"
        "theorem t : True := by native_decide\n"
        "private axiom hidden : False\n"
        "axiom open_one : False\n"
        "theorem assert_standard_axioms_clean : True := trivial\n"
        "theorem u : True := by sorry\n"
    )
    scan = replay.scan_sources(tmp_path)
    assert scan == {"lean_files": 2, "sorry": 2, "axiom_declarations": 2, "native_decide": 1}


# --- A receipt built here ------------------------------------------------------------


def make_log(failed: str | None = None) -> bytes:
    sections = []
    for name in replay.STEP_NAMES:
        body = "Build completed successfully (2944 jobs)." if name == "build" else "ok"
        sections.append(f"=== step: {name} ===\n{body}\n=== end: {name} returncode=0 ===\n")
        if name == failed:
            break
    return "\n".join(sections).encode()


def make_axioms_raw(overrides: dict[str, list[str]] | None = None) -> str:
    names = (replay.THEOREM, *replay.INSTANCE_DECLARATIONS)
    reports: dict[str, list[str]] = {name: list(STANDARD) for name in names}
    reports.update(overrides or {})
    lines = [replay.THEOREM_ELABORATED]
    lines += [replay.format_axioms_report(name, found) for name, found in reports.items()]
    return "\n".join(lines)


def seal(receipt: dict[str, Any], log: bytes) -> tuple[dict[str, Any], bytes]:
    receipt["build_log"] = {
        "path": replay.LOG_NAME,
        "sha256": hashlib.sha256(log).hexdigest(),
        "bytes": len(log),
        "lines": log.count(b"\n"),
    }
    return receipt, log


def good_receipt() -> tuple[dict[str, Any], bytes]:
    raw = make_axioms_raw()
    receipt: dict[str, Any] = {
        "schema": replay.SCHEMA,
        "bead": replay.BEAD,
        "status": "passed",
        "failed_step": None,
        "archive": {
            "url": replay.ARCHIVE_URL,
            "commit": replay.ARCHIVE_COMMIT,
            "committed": replay.ARCHIVE_COMMITTED,
            "blobs": dict(replay.PINNED_BLOBS),
        },
        "toolchain": {
            "lean_toolchain": replay.TOOLCHAIN,
            "mathlib_rev": replay.MATHLIB_REV,
            "tool_versions": [
                f"Lean (version {replay.LEAN_VERSION}, x86_64-unknown-linux-gnu)"
            ],
        },
        "steps": [
            {"name": name, "commands": [], "returncode": 0, "seconds": 1.5}
            for name in replay.STEP_NAMES
        ],
        "wall_seconds": 15.0,
        "theorem": {
            "name": replay.THEOREM,
            "statement_source": replay.THEOREM_SOURCE,
            "statement_elaborated": replay.THEOREM_ELABORATED,
        },
        "axioms": {
            "raw": raw,
            "reported": {
                name: list(found) for name, found in replay.parse_print_axioms(raw).items()
            },
        },
        "archive_assertions": {
            "module": "SquarePackingArchive.ManifestEvidence",
            "assert_standard_axioms_count": replay.MANIFEST_ASSERTIONS,
        },
        "policy_test": {"tests_run": 5},
        "source_scan": {
            "lean_files": 278,
            "sorry": 0,
            "axiom_declarations": 0,
            "native_decide": 0,
        },
        "statement_reading": "A reading.",
    }
    return seal(receipt, make_log())


def with_axioms(overrides: dict[str, list[str]]) -> tuple[dict[str, Any], bytes]:
    """A sealed receipt whose retained axiom output reports these declarations differently."""
    receipt, log = good_receipt()
    raw = make_axioms_raw(overrides)
    receipt["axioms"] = {
        "raw": raw,
        "reported": {
            name: list(found) for name, found in replay.parse_print_axioms(raw).items()
        },
    }
    return receipt, log


def failed_receipt(step: str = "build") -> tuple[dict[str, Any], bytes]:
    receipt, _ = good_receipt()
    index = replay.STEP_NAMES.index(step)
    receipt["status"] = "failed"
    receipt["failed_step"] = step
    receipt["steps"] = receipt["steps"][: index + 1]
    receipt["steps"][-1]["returncode"] = 1
    return seal(receipt, make_log(failed=step))


def test_a_good_receipt_validates() -> None:
    assert replay.validate_receipt(*good_receipt()) == []


def test_a_sorryax_dependency_is_refused() -> None:
    receipt, log = with_axioms({replay.THEOREM: [*STANDARD, "sorryAx"]})
    problems = replay.validate_receipt(receipt, log)
    assert any("non-standard axioms ['sorryAx']" in problem for problem in problems)
    assert any("sorryAx appears" in problem for problem in problems)


def test_an_extra_axiom_on_the_theorem_is_refused() -> None:
    receipt, log = with_axioms({replay.THEOREM: [*STANDARD, "Chelokot.unproved"]})
    problems = replay.validate_receipt(receipt, log)
    assert any("non-standard axioms ['Chelokot.unproved']" in problem for problem in problems)


def test_an_extra_axiom_on_an_instance_is_refused() -> None:
    instance = replay.INSTANCE_DECLARATIONS[2]
    receipt, log = with_axioms({instance: [*STANDARD, "Chelokot.unproved"]})
    problems = replay.validate_receipt(receipt, log)
    assert any(instance in problem and "Chelokot.unproved" in problem for problem in problems)


def test_a_missing_standard_axiom_is_not_exactly_the_three() -> None:
    receipt, log = with_axioms({replay.THEOREM: ["propext"]})
    problems = replay.validate_receipt(receipt, log)
    assert any("not exactly" in problem for problem in problems)


def test_a_theorem_with_no_report_is_refused() -> None:
    receipt, log = good_receipt()
    raw = "\n".join(
        replay.format_axioms_report(name, STANDARD) for name in replay.INSTANCE_DECLARATIONS
    )
    receipt["axioms"] = {
        "raw": raw,
        "reported": dict.fromkeys(replay.parse_print_axioms(raw), STANDARD),
    }
    problems = replay.validate_receipt(receipt, log)
    assert any(
        replay.THEOREM in problem and "no axiom report" in problem for problem in problems
    )


def test_reported_axioms_must_match_the_retained_output() -> None:
    receipt, log = good_receipt()
    receipt["axioms"]["reported"][replay.THEOREM] = ["propext"]
    problems = replay.validate_receipt(receipt, log)
    assert any("differ from the retained raw output" in problem for problem in problems)


def test_unparseable_axiom_output_is_refused() -> None:
    receipt, log = good_receipt()
    receipt["axioms"]["raw"] += "\n'Foo' depends on axioms: [propext, sorryAx"
    problems = replay.validate_receipt(receipt, log)
    assert any("did not match" in problem for problem in problems)


@pytest.mark.parametrize(
    "commit",
    ["0" * 40, replay.ARCHIVE_COMMIT[:8], "main", ""],
)
def test_a_wrong_commit_is_refused(commit: str) -> None:
    receipt, log = good_receipt()
    receipt["archive"]["commit"] = commit
    problems = replay.validate_receipt(receipt, log)
    assert any("is not the pinned" in problem for problem in problems)


def test_a_wrong_toolchain_or_mathlib_revision_is_refused() -> None:
    receipt, log = good_receipt()
    receipt["toolchain"]["lean_toolchain"] = "leanprover/lean4:v4.32.0"
    receipt["toolchain"]["mathlib_rev"] = "0" * 40
    problems = replay.validate_receipt(receipt, log)
    assert any("toolchain" in problem for problem in problems)
    assert any("Mathlib" in problem for problem in problems)


def test_a_changed_source_blob_is_refused() -> None:
    receipt, log = good_receipt()
    receipt["archive"]["blobs"][replay.GEOMETRY_FILE] = "0" * 40
    assert any("git blob" in problem for problem in replay.validate_receipt(receipt, log))


def test_a_wrong_theorem_or_statement_is_refused() -> None:
    receipt, log = good_receipt()
    receipt["theorem"]["name"] = "SquarePackingArchive.Records.NearSquare.s14_eq_four"
    receipt["theorem"]["statement_source"] = "theorem s14 : IsMinimumSide 14 4"
    receipt["theorem"]["statement_elaborated"] = "IsMinimumSide 14 4"
    problems = replay.validate_receipt(receipt, log)
    assert any("theorem is" in problem for problem in problems)
    assert any("source statement" in problem for problem in problems)
    assert any("elaborated statement" in problem for problem in problems)


def test_a_tampered_log_fails_its_hash() -> None:
    receipt, log = good_receipt()
    problems = replay.validate_receipt(receipt, log + b"an extra line\n")
    assert any("sha256" in problem for problem in problems)
    assert any("size differs" in problem for problem in problems)


def test_a_log_without_a_successful_build_is_refused() -> None:
    receipt, _ = good_receipt()
    log = make_log().replace(b"Build completed successfully", b"Build failed")
    problems = replay.validate_receipt(*seal(receipt, log))
    assert any("Build completed successfully" in problem for problem in problems)


def test_a_log_missing_a_step_section_is_refused() -> None:
    receipt, _ = good_receipt()
    log = make_log().replace(b"=== step: policy-test ===", b"")
    problems = replay.validate_receipt(*seal(receipt, log))
    assert any("policy-test" in problem for problem in problems)


def test_the_archive_scan_and_assertion_count_are_enforced() -> None:
    receipt, log = good_receipt()
    receipt["source_scan"]["sorry"] = 1
    receipt["archive_assertions"]["assert_standard_axioms_count"] = 78
    problems = replay.validate_receipt(receipt, log)
    assert any("source scan: sorry" in problem for problem in problems)
    assert any("assertion count" in problem for problem in problems)


def test_a_passed_receipt_must_carry_every_step_without_failure() -> None:
    receipt, log = good_receipt()
    del receipt["steps"][-1]
    receipt["steps"][3]["returncode"] = 2
    problems = replay.validate_receipt(receipt, log)
    assert any("every step" in problem for problem in problems)
    assert any("nonzero step" in problem for problem in problems)


def test_a_malformed_receipt_reports_rather_than_raises() -> None:
    assert replay.validate_receipt({}, b"")
    receipt, log = good_receipt()
    receipt["schema"] = "something-else"
    del receipt["steps"]
    problems = replay.validate_receipt(receipt, log)
    assert any("schema" in problem for problem in problems)
    assert any("steps is missing" in problem for problem in problems)


@pytest.mark.parametrize("step", ["clone", "checkout", "cache", "build", "axioms"])
def test_a_failure_receipt_is_valid_and_says_where_it_failed(step: str) -> None:
    receipt, log = failed_receipt(step)
    assert replay.validate_receipt(receipt, log) == []
    assert receipt["failed_step"] == step


def test_a_failure_receipt_must_name_its_last_step_and_a_nonzero_code() -> None:
    receipt, log = failed_receipt("build")
    receipt["failed_step"] = "cache"
    receipt["steps"][-1]["returncode"] = 0
    problems = replay.validate_receipt(receipt, log)
    assert any("failed_step is not the last step" in problem for problem in problems)
    assert any("returncode 0" in problem for problem in problems)


# --- The retained receipt and the command line ---------------------------------------


def test_the_retained_receipt_validates_offline_and_quickly() -> None:
    started = time.monotonic()
    problems = replay.check_retained()
    elapsed = time.monotonic() - started
    assert problems == []
    assert elapsed < 1.0


def test_the_retained_log_is_the_one_the_receipt_hashes() -> None:
    receipt = json.loads((replay.RECEIPT_DIR / replay.RECEIPT_NAME).read_text(encoding="utf-8"))
    log = (replay.RECEIPT_DIR / replay.LOG_NAME).read_bytes()
    assert receipt["build_log"]["sha256"] == hashlib.sha256(log).hexdigest()


def test_check_mode_exits_zero_and_summarizes(capsys: pytest.CaptureFixture[str]) -> None:
    assert replay.main(["--check"]) == 0
    assert replay.THEOREM in capsys.readouterr().out


def test_check_mode_exits_one_on_a_receipt_with_a_fault(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    receipt, log = with_axioms({replay.THEOREM: [*STANDARD, "sorryAx"]})
    (tmp_path / replay.RECEIPT_NAME).write_text(json.dumps(receipt))
    (tmp_path / replay.LOG_NAME).write_bytes(log)
    assert replay.main(["--check", "--receipt-dir", str(tmp_path)]) == 1
    assert "sorryAx" in capsys.readouterr().err


def test_a_missing_receipt_is_one_problem_not_a_traceback(tmp_path: Path) -> None:
    problems = replay.check_retained(tmp_path)
    assert len(problems) == 1
    assert "cannot read" in problems[0]


def test_run_mode_refuses_a_workdir_inside_the_repository(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as raised:
        replay.main(["--run", "--workdir", str(replay.REPO / "packing" / "scratch")])
    assert raised.value.code == 2
    assert "outside the repository" in capsys.readouterr().err


def test_run_mode_needs_a_workdir(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        replay.main(["--run"])
    assert "--workdir" in capsys.readouterr().err


# --- The run, with a fake runner -----------------------------------------------------


def fake_runner(failing: str, output: str, calls: list[tuple[str, ...]]) -> replay.Runner:
    def run(argv: Any, _cwd: Path, _timeout: float) -> replay.CommandResult:
        calls.append(tuple(argv))
        code = 128 if failing in argv else 0
        return replay.CommandResult(tuple(argv), code, output if code else "ok", 0.1)

    return run


def test_a_refused_host_is_retained_as_a_failure_receipt(tmp_path: Path) -> None:
    calls: list[tuple[str, ...]] = []
    error = "fatal: unable to access 'https://github.com/chelokot/square-packing-archive/': 403"
    run = replay.Replay(tmp_path / "work", runner=fake_runner("clone", error, calls))
    (tmp_path / "work").mkdir()
    receipt = run.run()
    replay.retain(receipt, run.sections, tmp_path / "out")
    assert receipt["status"] == "failed"
    assert receipt["failed_step"] == "clone"
    assert [step["name"] for step in receipt["steps"]] == ["clone"]
    assert calls == [
        ("git", "clone", replay.ARCHIVE_URL, str(tmp_path / "work" / "square-packing-archive"))
    ]
    assert error in (tmp_path / "out" / replay.LOG_NAME).read_text()
    assert replay.check_retained(tmp_path / "out") == []
    assert "FAILED at step clone" in replay.summary(tmp_path / "out")


def test_a_failed_checkout_stops_before_any_later_step(tmp_path: Path) -> None:
    calls: list[tuple[str, ...]] = []
    work = tmp_path / "work"
    (work / "square-packing-archive" / ".git").mkdir(parents=True)
    run = replay.Replay(
        work, runner=fake_runner("checkout", "fatal: reference is not a tree", calls)
    )
    receipt = run.run()
    assert receipt["failed_step"] == "checkout"
    assert [step["name"] for step in receipt["steps"]] == ["clone", "checkout"]
    assert all("build" not in call for call in calls)


def test_retain_hashes_the_log_it_writes(tmp_path: Path) -> None:
    receipt, _ = good_receipt()
    replay.retain(copy.deepcopy(receipt), ["=== step: clone ===\nok\n"], tmp_path)
    written = json.loads((tmp_path / replay.RECEIPT_NAME).read_text())
    log = (tmp_path / replay.LOG_NAME).read_bytes()
    assert written["build_log"]["sha256"] == hashlib.sha256(log).hexdigest()
    assert written["build_log"]["bytes"] == len(log)


# --- Rebuilding chosen modules -------------------------------------------------------


def make_build_tree(formal: Path) -> None:
    lean = formal / ".lake" / "build" / "lib" / "lean"
    ir = formal / ".lake" / "build" / "ir"
    for directory in (lean / "Pkg" / "Audit", ir / "Pkg"):
        directory.mkdir(parents=True)
    for name in ("Audit.olean", "Audit.trace", "AuditExtra.olean"):
        (lean / "Pkg" / name).write_text("x")
    (lean / "Pkg" / "Audit" / "Inner.olean").write_text("x")
    (ir / "Pkg" / "Audit.c").write_text("x")
    (ir / "Pkg" / "AuditExtra.c").write_text("x")
    (lean / "Pkg.olean").write_text("x")
    (lean / "Pkg.ilean").write_text("x")


def test_module_products_match_the_stem_and_not_its_neighbours(tmp_path: Path) -> None:
    make_build_tree(tmp_path)
    lean = tmp_path / ".lake" / "build" / "lib" / "lean"
    audit = replay.module_products(tmp_path, "Pkg.Audit")
    assert sorted(path.name for path in audit) == ["Audit.c", "Audit.olean", "Audit.trace"]
    assert lean / "Pkg" / "AuditExtra.olean" not in audit
    assert lean / "Pkg" / "Audit" / "Inner.olean" not in audit
    root = replay.module_products(tmp_path, "Pkg")
    assert sorted(path.name for path in root) == ["Pkg.ilean", "Pkg.olean"]
    assert replay.module_products(tmp_path, "Pkg.Missing") == []


@pytest.mark.parametrize("module", ["", "../Pkg", "Pkg/Audit", "Pkg..Audit", ".Pkg", "Pkg."])
def test_module_products_refuse_a_name_that_is_not_a_module(
    tmp_path: Path, module: str
) -> None:
    with pytest.raises(ValueError, match="not a Lean module name"):
        replay.module_products(tmp_path, module)


def test_build_removes_only_the_named_modules_products_and_says_so(tmp_path: Path) -> None:
    formal = tmp_path / "square-packing-archive" / "formal"
    make_build_tree(formal)
    calls: list[tuple[str, ...]] = []
    run = replay.Replay(tmp_path, runner=fake_runner("never", "", calls), rebuild=["Pkg.Audit"])
    result = run.build()
    lean = formal / ".lake" / "build" / "lib" / "lean"
    assert result.returncode == 0
    assert "removed 3 build products of Pkg.Audit" in result.output
    assert not (lean / "Pkg" / "Audit.olean").exists()
    assert (lean / "Pkg" / "AuditExtra.olean").exists()
    assert (lean / "Pkg.olean").exists()
    assert run.facts["rebuilt_modules"] == ["Pkg.Audit"]
    assert calls == [("lake", "build")]


def test_notes_must_be_a_list_of_strings() -> None:
    receipt, log = good_receipt()
    receipt["notes"] = ["a sentence", 3]
    assert any("notes" in problem for problem in replay.validate_receipt(receipt, log))
    receipt["notes"] = ["a sentence"]
    assert replay.validate_receipt(receipt, log) == []
