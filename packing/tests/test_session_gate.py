"""A terminal session names the gate that certified it, and the ancestry claim is real.

The check this covers exists because forty-seven of the first eighty-six terminal records
said something about a gate in `checks` and seven named any commit. A sentence like "the
record gate passed on the closed tree" is a claim about a tree nobody can now identify, and
`OR-13` -- every fast check runs in CI -- means nothing if no record says the run happened
on what was handed over.

Two things here are load-bearing rather than decorative. The first is that the checker
actually fails on the shapes it exists to refuse, `full gate: passed` most of all. The
second is that its ancestry clause is tested **against a real Git graph** rather than a
stub: a temporary repository with a divergent branch and a shallow clone of itself, so that
`orphaned`, `absent-in-a-complete-checkout` and `absent-in-a-shallow-checkout` are three
outcomes and not two. Collapsing the last into the second is the mistake `conventions.md`
§6 names -- a checkout that does not contain a commit is not evidence the commit was
orphaned.
"""

from __future__ import annotations

import json
import pathlib
import shutil
import subprocess

import pytest

import devtools.check_session_gate as checker
from devtools.check_session_gate import (
    CERTIFYING_TIERS,
    GATE_DECLARED_FROM,
    GROUPS,
    SCHEMA,
    GateRun,
    ancestry_problems,
    bead_state,
    commit_state,
    declaration_pattern,
    history_state,
    main,
    parse_declaration,
)
from sqpack.yamlio import safe_load

ABSENT = "0123456789abcdef0123456789abcdef01234567"


def _git(repository: pathlib.Path, *arguments: str) -> str:
    finished = subprocess.run(
        ("git", "-C", str(repository), *arguments),
        capture_output=True,
        text=True,
        check=True,
    )
    return finished.stdout.strip()


def _repository(root: pathlib.Path) -> pathlib.Path:
    """A real two-commit history on `main` with one divergent commit off it."""
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "--initial-branch=main", "--quiet")
    _git(root, "config", "user.email", "gate@example.invalid")
    _git(root, "config", "user.name", "Gate Test")
    for index in ("first", "second"):
        (root / f"{index}.txt").write_text(index, encoding="utf-8")
        _git(root, "add", "-A")
        _git(root, "commit", "--quiet", "-m", index)
    return root


def _record(directory: pathlib.Path, identifier: str, *, status: str, checks: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f"{identifier}-fabricated.md").write_text(
        f"---\nsession:\n  id: {identifier}\n  status: {status}\n{checks}---\n# fabricated\n",
        encoding="utf-8",
    )


def _checks(*items: str) -> str:
    return "  checks:\n" + "".join(f"  - {item!r}\n" for item in items)


def _run(monkeypatch, sessions: pathlib.Path, repository: pathlib.Path) -> int:
    monkeypatch.setattr(checker, "SESSIONS", sessions)
    monkeypatch.setattr(checker, "REPO", repository)
    return main()


def _only_path(monkeypatch, directory: pathlib.Path, *, bead_status: str | None) -> None:
    """A PATH holding `git` and, when a status is given, a `tbd` that answers with it.

    Set rather than prepended, so `bead_status=None` is the real tbd-unavailable case on
    a machine that does have tbd installed. `git` is linked in because the ancestry
    clause still has to run: what varies between these cases is the tracker, not the
    graph.
    """
    directory.mkdir(parents=True, exist_ok=True)
    git = shutil.which("git")
    assert git is not None
    (directory / "git").symlink_to(git)
    if bead_status is not None:
        script = directory / "tbd"
        script.write_text(
            f'#!/bin/sh\nprintf \'{{"status": "{bead_status}"}}\\n\'\n',
            encoding="utf-8",
        )
        script.chmod(0o755)
    monkeypatch.setenv("PATH", str(directory))


# --- the grammar ----------------------------------------------------------------------


def test_the_canonical_declaration_parses_into_its_three_parts() -> None:
    run = parse_declaration("full gate: fast at 07a41a89: passed", declaration_pattern())

    assert run is not None
    assert (run.tier, run.commit, run.verdict) == ("fast", "07a41a89", "passed")
    assert run.certifies


def test_a_declaration_may_carry_a_parenthetical_note() -> None:
    run = parse_declaration(
        "full gate: full at 07a41a89: failed (one shallow-checkout artifact)",
        declaration_pattern(),
    )

    assert run is not None
    assert run.note == "one shallow-checkout artifact"
    assert not run.certifies


def test_a_verdict_with_no_commit_is_not_a_declaration() -> None:
    """The shape the whole check exists to refuse."""
    assert parse_declaration("full gate: passed", declaration_pattern()) is None


def test_the_schema_publishes_the_grammar_this_module_reads() -> None:
    schema = safe_load(SCHEMA.read_text(encoding="utf-8"))
    pattern = schema["$defs"]["full_gate_declaration"]["pattern"]

    assert declaration_pattern().pattern == pattern
    assert declaration_pattern().groups == len(GROUPS)


# --- what the checker refuses ---------------------------------------------------------


def test_a_terminal_session_naming_no_gate_run_is_refused(monkeypatch, tmp_path) -> None:
    _record(tmp_path / "sessions", "session-999", status="completed", checks="")

    assert _run(monkeypatch, tmp_path / "sessions", _repository(tmp_path / "repo")) == 1


def test_an_in_progress_session_is_not_required_to_name_one(monkeypatch, tmp_path) -> None:
    """The gate runs at the close; requiring the declaration earlier would be wrong."""
    _record(tmp_path / "sessions", "session-999", status="in_progress", checks="")

    assert _run(monkeypatch, tmp_path / "sessions", _repository(tmp_path / "repo")) == 0


def test_a_bare_verdict_is_a_failure_rather_than_prose_the_checker_skips(
    monkeypatch, tmp_path
) -> None:
    """A near miss must fail, or the grammar is advisory and the rule is defeated by typos."""
    _record(
        tmp_path / "sessions",
        "session-999",
        status="completed",
        checks=_checks("full gate: passed"),
    )

    assert _run(monkeypatch, tmp_path / "sessions", _repository(tmp_path / "repo")) == 1


def test_a_tier_packing_validate_cannot_select_is_refused(monkeypatch, tmp_path) -> None:
    _record(
        tmp_path / "sessions",
        "session-999",
        status="completed",
        checks=_checks("full gate: turbo at 07a41a89: passed"),
    )

    assert _run(monkeypatch, tmp_path / "sessions", _repository(tmp_path / "repo")) == 1


def test_a_real_but_smaller_tier_does_not_certify_a_handover(monkeypatch, tmp_path) -> None:
    """`--records` is six seconds of record checks; running it is not running the gate."""
    repository = _repository(tmp_path / "repo")
    head = _git(repository, "rev-parse", "HEAD")
    _record(
        tmp_path / "sessions",
        "session-999",
        status="completed",
        checks=_checks(f"full gate: records at {head}: passed"),
    )

    assert _run(monkeypatch, tmp_path / "sessions", repository) == 1
    assert "records" not in CERTIFYING_TIERS


def test_a_failed_verdict_does_not_certify_a_handover(monkeypatch, tmp_path) -> None:
    repository = _repository(tmp_path / "repo")
    head = _git(repository, "rev-parse", "HEAD")
    _record(
        tmp_path / "sessions",
        "session-999",
        status="completed",
        checks=_checks(f"full gate: fast at {head}: failed (three steps red)"),
    )

    assert _run(monkeypatch, tmp_path / "sessions", repository) == 1


# --- ancestry, against a real Git graph -----------------------------------------------


def test_commit_state_separates_reachable_from_orphaned_from_absent(tmp_path) -> None:
    repository = _repository(tmp_path / "repo")
    parent = _git(repository, "rev-parse", "HEAD~1")
    _git(repository, "checkout", "--quiet", "-b", "sidebranch", "HEAD~1")
    (repository / "side.txt").write_text("side", encoding="utf-8")
    _git(repository, "add", "-A")
    _git(repository, "commit", "--quiet", "-m", "side")
    side = _git(repository, "rev-parse", "HEAD")
    _git(repository, "checkout", "--quiet", "main")

    assert history_state(repository) == "complete"
    assert commit_state(repository, parent) == "reachable"
    assert commit_state(repository, side) == "orphaned"
    assert commit_state(repository, ABSENT) == "absent"


def test_a_gate_run_on_an_ancestor_of_head_is_accepted(monkeypatch, tmp_path) -> None:
    repository = _repository(tmp_path / "repo")
    parent = _git(repository, "rev-parse", "HEAD~1")
    _record(
        tmp_path / "sessions",
        "session-999",
        status="completed",
        checks=_checks(f"full gate: fast at {parent}: passed"),
    )

    assert _run(monkeypatch, tmp_path / "sessions", repository) == 0


def test_a_gate_run_off_the_handovers_own_history_is_refused(monkeypatch, tmp_path) -> None:
    """The substance of the cell: present in the repository, not behind HEAD."""
    repository = _repository(tmp_path / "repo")
    _git(repository, "checkout", "--quiet", "-b", "sidebranch", "HEAD~1")
    (repository / "side.txt").write_text("side", encoding="utf-8")
    _git(repository, "add", "-A")
    _git(repository, "commit", "--quiet", "-m", "side")
    side = _git(repository, "rev-parse", "HEAD")
    _git(repository, "checkout", "--quiet", "main")
    _record(
        tmp_path / "sessions",
        "session-999",
        status="completed",
        checks=_checks(f"full gate: fast at {side}: passed"),
    )

    assert _run(monkeypatch, tmp_path / "sessions", repository) == 1


def test_an_absent_commit_in_a_complete_checkout_is_refused(monkeypatch, tmp_path) -> None:
    """Shallowness is the only innocent reading of a missing object, and it is ruled out."""
    repository = _repository(tmp_path / "repo")
    _record(
        tmp_path / "sessions",
        "session-999",
        status="completed",
        checks=_checks(f"full gate: fast at {ABSENT}: passed"),
    )

    assert _run(monkeypatch, tmp_path / "sessions", repository) == 1


def test_an_absent_commit_in_a_shallow_checkout_is_uncheckable_not_false(
    monkeypatch, tmp_path
) -> None:
    """`conventions.md` §6, held to exactly: not finding it is a fact about the checkout."""
    origin = _repository(tmp_path / "origin")
    dropped = _git(origin, "rev-parse", "HEAD~1")
    shallow = tmp_path / "shallow"
    _git(tmp_path, "clone", "--quiet", "--depth", "1", f"file://{origin}", str(shallow))
    _record(
        tmp_path / "sessions",
        "session-999",
        status="completed",
        checks=_checks(f"full gate: fast at {dropped}: passed"),
    )

    assert history_state(shallow) == "shallow"
    assert commit_state(shallow, dropped) == "absent"
    assert _run(monkeypatch, tmp_path / "sessions", shallow) == 0


def test_a_tree_with_no_git_history_leaves_ancestry_unresolved(monkeypatch, tmp_path) -> None:
    """The negative-control sandbox is a source snapshot with no `.git`, and so is a tarball.

    Grammar and presence still bind there; only the ancestry clause goes quiet, and it says
    so on stdout rather than passing in silence.
    """
    plain = tmp_path / "no-git"
    plain.mkdir()
    _record(
        tmp_path / "sessions",
        "session-999",
        status="completed",
        checks=_checks(f"full gate: fast at {ABSENT}: passed"),
    )

    assert history_state(plain) == "unavailable"
    assert _run(monkeypatch, tmp_path / "sessions", plain) == 0


def test_grammar_still_binds_where_ancestry_cannot_be_resolved(monkeypatch, tmp_path) -> None:
    plain = tmp_path / "no-git"
    plain.mkdir()
    _record(
        tmp_path / "sessions",
        "session-999",
        status="completed",
        checks=_checks("full gate: passed"),
    )

    assert _run(monkeypatch, tmp_path / "sessions", plain) == 1


# --- the boundary ---------------------------------------------------------------------


def test_the_start_date_is_a_boundary_not_a_list_and_the_corpus_passes() -> None:
    """A new session is above it by construction, so the exemption cannot quietly grow."""
    assert GATE_DECLARED_FROM == "session-087"
    assert main() == 0


def test_a_session_below_the_boundary_is_exempt_and_one_above_it_is_not(
    monkeypatch, tmp_path
) -> None:
    repository = _repository(tmp_path / "repo")
    _record(tmp_path / "below", "session-086", status="completed", checks="")
    _record(tmp_path / "above", "session-087", status="completed", checks="")

    assert _run(monkeypatch, tmp_path / "below", repository) == 0
    assert _run(monkeypatch, tmp_path / "above", repository) == 1


def test_a_grandfathered_session_that_does_declare_one_is_still_held_to_it(
    monkeypatch, tmp_path
) -> None:
    """The boundary exempts silence, never a false claim.

    Otherwise the eighty-six records below it become a place to write a gate declaration
    nothing will ever read.
    """
    _record(
        tmp_path / "sessions",
        "session-001",
        status="completed",
        checks=_checks("full gate: passed"),
    )

    assert _run(monkeypatch, tmp_path / "sessions", _repository(tmp_path / "repo")) == 1


# --- stopped work whose certification is explicitly outstanding ----------------------


def _pending_record(
    directory: pathlib.Path,
    *,
    status: str = "stopped",
    pending: object = "think-ab12",
    reason: object = "The checkpoint failed; preserve the stopped work.",
    action: str = "Resolve certification under think-ab12 before research admission.",
    checks: str = "",
    phases: str = "",
) -> None:
    fields = (
        f"  certification_pending: {json.dumps(pending)}\n"
        f"  stop_reason: {json.dumps(reason)}\n"
        f"  next_action: {json.dumps(action)}\n"
    )
    _record(directory, "session-999", status=status, checks=fields + phases + checks)


def _phases(*beads: tuple[str, str]) -> str:
    """A `workflow_phases` list holding only the two fields this checker reads."""
    return "  workflow_phases:\n" + "".join(
        f"  - bead: {bead}\n    status: {status}\n" for bead, status in beads
    )


def test_pending_stop_without_a_run_is_valid_but_not_certified(
    monkeypatch, tmp_path, capsys
) -> None:
    _pending_record(tmp_path / "sessions")

    assert _run(monkeypatch, tmp_path / "sessions", _repository(tmp_path / "repo")) == 0
    output = capsys.readouterr().out
    assert "0 terminal sessions name a full-gate run" in output
    assert "UNCERTIFIED" in output
    assert "think-ab12" in output
    assert "which has not closed" not in output


@pytest.mark.parametrize("status", ["completed", "in_progress"])
def test_pending_certification_cannot_hide_another_work_status(
    monkeypatch, tmp_path, status
) -> None:
    _pending_record(tmp_path / "sessions", status=status)

    assert _run(monkeypatch, tmp_path / "sessions", _repository(tmp_path / "repo")) == 1


@pytest.mark.parametrize("pending", ["", "think-", "think-a-b", True, 12, None])
def test_pending_certification_requires_a_well_formed_bead(monkeypatch, tmp_path, pending):
    _pending_record(tmp_path / "sessions", pending=pending)

    assert _run(monkeypatch, tmp_path / "sessions", _repository(tmp_path / "repo")) == 1


@pytest.mark.parametrize("reason", ["", "  ", True, None])
def test_pending_certification_requires_a_stop_reason(monkeypatch, tmp_path, reason):
    _pending_record(tmp_path / "sessions", reason=reason)

    assert _run(monkeypatch, tmp_path / "sessions", _repository(tmp_path / "repo")) == 1


@pytest.mark.parametrize("action", ["", "Continue think-other.", "Continue think-ab12-extra."])
def test_pending_certification_requires_the_same_exact_followup_bead(
    monkeypatch, tmp_path, action
) -> None:
    _pending_record(tmp_path / "sessions", action=action)

    assert _run(monkeypatch, tmp_path / "sessions", _repository(tmp_path / "repo")) == 1


@pytest.mark.parametrize("tier", ["fast", "full"])
def test_pending_cannot_relabel_a_canonical_pass_as_historical(
    monkeypatch, tmp_path, tier
) -> None:
    repository = _repository(tmp_path / "repo")
    head = _git(repository, "rev-parse", "HEAD")
    _pending_record(
        tmp_path / "sessions",
        checks=_checks(f"full gate: {tier} at {head}: passed (historical docs only)"),
    )

    assert _run(monkeypatch, tmp_path / "sessions", repository) == 1


def test_pending_accepts_failed_history_and_later_real_pass_can_certify(
    monkeypatch, tmp_path, capsys
) -> None:
    repository = _repository(tmp_path / "repo")
    head = _git(repository, "rev-parse", "HEAD")
    failed = f"full gate: full at {head}: failed (retained failed checkpoint)"
    _pending_record(tmp_path / "sessions", checks=_checks(failed))

    assert _run(monkeypatch, tmp_path / "sessions", repository) == 0
    assert "UNCERTIFIED" in capsys.readouterr().out
    _record(
        tmp_path / "sessions",
        "session-999",
        status="stopped",
        checks=_checks(failed, f"full gate: full at {head}: passed"),
    )
    assert _run(monkeypatch, tmp_path / "sessions", repository) == 0
    assert "1 terminal sessions name a full-gate run" in capsys.readouterr().out


@pytest.mark.parametrize(
    "declaration", ["full gate: passed", "full gate: turbo at 07a41a89: failed"]
)
def test_pending_does_not_suppress_malformed_or_unknown_declarations(
    monkeypatch, tmp_path, declaration
) -> None:
    _pending_record(tmp_path / "sessions", checks=_checks(declaration))

    assert _run(monkeypatch, tmp_path / "sessions", _repository(tmp_path / "repo")) == 1


def test_pending_failed_receipt_must_resolve_in_complete_history(monkeypatch, tmp_path):
    _pending_record(
        tmp_path / "sessions", checks=_checks(f"full gate: full at {ABSENT}: failed")
    )

    assert _run(monkeypatch, tmp_path / "sessions", _repository(tmp_path / "repo")) == 1


def test_pending_failed_receipt_on_an_orphan_is_unresolved_not_refused(
    monkeypatch, tmp_path, capsys
) -> None:
    """A squash or rebase merge orphans every commit of the branch that recorded it.

    The retained receipt still says `failed`, which is why it was kept, so nothing about
    it was certified and nothing about it can be falsified by the mainline moving. Making
    this a refusal would fail the records gate on `main` because of a merge button.
    """
    repository = _repository(tmp_path / "repo")
    _git(repository, "checkout", "--quiet", "-b", "sidebranch", "HEAD~1")
    _git(repository, "commit", "--quiet", "--allow-empty", "-m", "orphan")
    orphan = _git(repository, "rev-parse", "HEAD")
    _git(repository, "checkout", "--quiet", "main")
    _pending_record(
        tmp_path / "sessions", checks=_checks(f"full gate: full at {orphan}: failed")
    )

    assert _run(monkeypatch, tmp_path / "sessions", repository) == 0
    output = capsys.readouterr().out
    assert "UNCERTIFIED" in output
    assert f"{orphan} (a retained full run that failed" in output
    assert "certifies nothing and refuses nothing" in output


def test_a_certifying_orphan_is_still_refused_where_noncertifying_ones_are_not(
    tmp_path,
) -> None:
    """The split is on what the run claims, and only on that.

    Read against `ancestry_problems` directly because a pending record cannot carry a
    certifying declaration -- `declaration_problems` refuses that first -- so the two
    readings never meet in one record.
    """
    repository = _repository(tmp_path / "repo")
    _git(repository, "checkout", "--quiet", "-b", "sidebranch", "HEAD~1")
    _git(repository, "commit", "--quiet", "--allow-empty", "-m", "orphan")
    orphan = _git(repository, "rev-parse", "HEAD")
    _git(repository, "checkout", "--quiet", "main")
    runs = [
        GateRun(tier="full", commit=orphan, verdict="passed", note=None),
        GateRun(tier="full", commit=orphan, verdict="failed", note=None),
    ]

    problems, unresolved = ancestry_problems(
        "session-999", runs, "complete", repository, include_noncertifying=True
    )

    assert len(problems) == 1
    assert "is not an ancestor of HEAD" in problems[0]
    assert len(unresolved) == 1
    assert "certifies nothing and refuses nothing" in unresolved[0]


@pytest.mark.parametrize("history", ["shallow", "unavailable"])
def test_pending_failed_receipt_with_missing_history_stays_uncheckable(
    monkeypatch, tmp_path, capsys, history
) -> None:
    origin = _repository(tmp_path / "origin")
    commit = _git(origin, "rev-parse", "HEAD~1")
    repository = tmp_path / "snapshot"
    if history == "shallow":
        _git(tmp_path, "clone", "--quiet", "--depth", "1", f"file://{origin}", str(repository))
    else:
        repository.mkdir()
    _pending_record(
        tmp_path / "sessions", checks=_checks(f"full gate: full at {commit}: failed")
    )

    assert _run(monkeypatch, tmp_path / "sessions", repository) == 0
    output = capsys.readouterr().out
    assert "UNCERTIFIED" in output
    assert "UNCHECKABLE" in output
    assert "0 terminal sessions name a full-gate run" in output


def test_unmarked_stopped_record_still_needs_a_certifying_run(monkeypatch, tmp_path):
    _record(tmp_path / "sessions", "session-999", status="stopped", checks="")

    assert _run(monkeypatch, tmp_path / "sessions", _repository(tmp_path / "repo")) == 1


def test_mixed_pending_and_certified_records_have_separate_counts(
    monkeypatch, tmp_path, capsys
) -> None:
    repository = _repository(tmp_path / "repo")
    head = _git(repository, "rev-parse", "HEAD")
    _pending_record(tmp_path / "sessions")
    _record(
        tmp_path / "sessions",
        "session-998",
        status="completed",
        checks=_checks(f"full gate: full at {head}: passed"),
    )

    assert _run(monkeypatch, tmp_path / "sessions", repository) == 0
    output = capsys.readouterr().out
    assert "1 terminal sessions name a full-gate run" in output
    assert "1 stopped sessions remain UNCERTIFIED" in output
    assert "session-999 -> think-ab12" in output


# --- the follow-up bead the debt is owed to -------------------------------------------


def test_pending_certification_cannot_name_a_bead_this_record_completed(
    monkeypatch, tmp_path, capsys
) -> None:
    """A marker naming finished work is the marker discharging itself.

    Answered from the record alone, so it binds on a machine with no tracker installed.
    """
    repository = _repository(tmp_path / "repo")
    _pending_record(tmp_path / "sessions", phases=_phases(("think-ab12", "completed")))
    _only_path(monkeypatch, tmp_path / "bin", bead_status=None)

    assert _run(monkeypatch, tmp_path / "sessions", repository) == 1
    assert "workflow_phases marks completed" in capsys.readouterr().err


@pytest.mark.parametrize("status", ["in_progress", "stopped"])
def test_pending_certification_accepts_a_phase_that_did_not_finish(
    monkeypatch, tmp_path, status
) -> None:
    """`stopped` is the shape that leaves the debt; reading it as discharged inverts it."""
    repository = _repository(tmp_path / "repo")
    _pending_record(tmp_path / "sessions", phases=_phases(("think-ab12", status)))
    _only_path(monkeypatch, tmp_path / "bin", bead_status=None)

    assert _run(monkeypatch, tmp_path / "sessions", repository) == 0


def test_pending_certification_refuses_a_bead_tbd_reports_closed(
    monkeypatch, tmp_path, capsys
) -> None:
    repository = _repository(tmp_path / "repo")
    _pending_record(tmp_path / "sessions")
    _only_path(monkeypatch, tmp_path / "bin", bead_status="closed")

    assert _run(monkeypatch, tmp_path / "sessions", repository) == 1
    assert "tbd reports closed" in capsys.readouterr().err


@pytest.mark.parametrize("status", ["in_progress", "blocked"])
def test_pending_certification_accepts_a_bead_tbd_reports_live(
    monkeypatch, tmp_path, status
) -> None:
    """Only `closed` refuses. A blocked bead is work nobody has finished."""
    repository = _repository(tmp_path / "repo")
    _pending_record(tmp_path / "sessions")
    _only_path(monkeypatch, tmp_path / "bin", bead_status=status)

    assert _run(monkeypatch, tmp_path / "sessions", repository) == 0


def test_pending_certification_does_not_fail_where_tbd_is_unavailable(
    monkeypatch, tmp_path
) -> None:
    """CI, a source tarball and the negative-control sandbox have no tracker.

    A machine that cannot ask has not learned that the bead is closed, which is the same
    line `conventions.md` §6 draws for an unresolvable ancestry.
    """
    repository = _repository(tmp_path / "repo")
    _pending_record(tmp_path / "sessions")
    _only_path(monkeypatch, tmp_path / "bin", bead_status=None)

    assert shutil.which("tbd") is None
    assert bead_state("think-ab12", repository) == "unresolved"
    assert _run(monkeypatch, tmp_path / "sessions", repository) == 0


@pytest.mark.parametrize(
    ("answer", "expected"), [("closed", "closed"), ("in_progress", "open")]
)
def test_bead_state_reads_the_status_tbd_publishes(monkeypatch, tmp_path, answer, expected):
    """No Git repository here on purpose: the tracker and the graph are separate axes."""
    _only_path(monkeypatch, tmp_path / "bin", bead_status=answer)

    assert bead_state("think-ab12", tmp_path) == expected


def test_a_tbd_that_fails_or_answers_nonsense_resolves_nothing(monkeypatch, tmp_path) -> None:
    """Three states, never two: not being able to ask is a fact about the machine."""
    stand_in = tmp_path / "bin"
    _only_path(monkeypatch, stand_in, bead_status="closed")
    (stand_in / "tbd").write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")

    assert bead_state("think-ab12", tmp_path) == "unresolved"

    (stand_in / "tbd").write_text("#!/bin/sh\nprintf 'not json\\n'\n", encoding="utf-8")

    assert bead_state("think-ab12", tmp_path) == "unresolved"
