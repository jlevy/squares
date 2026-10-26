"""The bead staleness report: two shapes the tree checker prints and never fails on.

The bead tree and the agenda layer are edited by different hands at different times.
Cells name beads through a `think-` alias the store's table resolves; an in-progress
bead named only by terminal cells is work the agenda finished with, and one named by
no cell is work tracked outside the agenda layer. These pin the join and the two
counts on a fixture small enough to read.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from devtools import check_bead_tree
from devtools.check_bead_tree import (
    NO_BEAD,
    check,
    deferral_problems,
    deferrals,
    parse_aliases,
    staleness,
)
from sqpack.cli import validate


def _bead(bead_id: str, status: str, title: str) -> dict[str, object]:
    return {"id": bead_id, "status": status, "title": title}


def _cell(cell_id: str, state: str, bead: str) -> dict[str, str]:
    return {"id": cell_id, "agenda": "agenda-001", "state": state, "bead": bead}


FINISHED = _bead("is-01aaaa", "in_progress", "finished on the agenda, live on the tree")
OUTSIDE = _bead("is-01bbbb", "in_progress", "tracked outside the agenda layer")
ALIASES = {"aaaa": "01aaaa", "bbbb": "01bbbb"}


def test_an_in_progress_bead_named_only_by_terminal_cells_is_stale() -> None:
    cells = [
        _cell("BC-001", "complete", "think-aaaa"),
        _cell("BC-002", "stopped", "think-aaaa"),
    ]
    report = staleness([FINISHED, OUTSIDE], ALIASES, cells)
    assert [entry["bead"] for entry in report["stale"]] == ["think-aaaa"]
    assert report["stale"][0]["cells"] == ["BC-001 complete", "BC-002 stopped"]
    assert report["stale"][0]["title"] == "finished on the agenda, live on the tree"


def test_an_in_progress_bead_named_by_no_cell_is_untracked() -> None:
    cells = [_cell("BC-001", "complete", "think-aaaa"), _cell("BC-002", "ready", "think-zzzz")]
    report = staleness([FINISHED, OUTSIDE], ALIASES, cells)
    assert [entry["bead"] for entry in report["untracked"]] == ["think-bbbb"]
    assert report["untracked"][0]["cells"] == []


def test_one_live_naming_cell_keeps_a_bead_out_of_both_lists() -> None:
    cells = [
        _cell("BC-001", "complete", "think-aaaa"),
        _cell("BC-002", "blocked", "think-aaaa"),
    ]
    report = staleness([FINISHED], ALIASES, cells)
    assert report == {"stale": [], "untracked": []}


def test_only_in_progress_beads_are_reported() -> None:
    closed = _bead("is-01cccc", "closed", "done and closed")
    open_bead = _bead("is-01dddd", "open", "queued, not started")
    report = staleness([closed, open_bead], {"cccc": "01cccc"}, [])
    assert report == {"stale": [], "untracked": []}


def test_the_alias_table_is_read_without_yaml_retyping() -> None:
    table = (
        "schema_version: 1\n---\n1e10: 01aaaa\nnull: 01bbbb\n# note\nrh18: 01cccc\n"
        '"48e1": 01dddd\n'
    )
    assert parse_aliases(table) == {
        "schema_version": "1",
        "1e10": "01aaaa",
        "null": "01bbbb",
        "rh18": "01cccc",
        "48e1": "01dddd",
    }


def test_a_bead_without_an_alias_is_reported_by_its_id() -> None:
    report = staleness([OUTSIDE], {}, [_cell("BC-001", "ready", "think-bbbb")])
    assert [entry["bead"] for entry in report["untracked"]] == ["is-01bbbb"]


def test_the_report_does_not_change_the_gate_verdict() -> None:
    """Both shapes are reports; the tree's two invariants still decide pass or fail."""
    assert check([FINISHED, OUTSIDE]) == []


def _write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def test_every_deferral_a_record_declares_is_collected_with_its_bead(tmp_path: Path) -> None:
    """Pending intakes, deferred conflicts, open issues and watched-repository reads."""
    coverage = _write(
        tmp_path / "coverage.yaml",
        "pending_catalogue_intake:\n"
        "  - {n: 69, bead: think-aaaa, recorded: '2026-09-30'}\n"
        "beyond_horizon_claims:\n"
        "  - {n: 400, disposition: deferred-conflict, bead: think-bbbb}\n"
        "  - {n: 401, disposition: superseded}\n",
    )
    requests = _write(
        tmp_path / "requests.yaml",
        "issues:\n"
        "  - number: 282\n"
        "    state: open\n"
        "    answer_bead: think-cccc\n"
        "    results: [{key: later, queued: true, bead: think-ffff}, {key: done}]\n"
        "    asks: [{what: a fix, state: queued, bead: think-gggg}]\n"
        "  - {number: 170, state: closed, answer_bead: think-dddd}\n",
    )
    watch = _write(
        tmp_path / "watch.yaml",
        "repositories:\n"
        "  - {url: 'https://github.com/a/b', read_through: 7ff3b2113532, bead: think-eeee}\n"
        "  - {url: 'https://github.com/a/c', read_through: 0123456789ab}\n",
    )
    named = deferrals(coverage, requests, watch)
    assert [alias for _, alias in named] == [
        "think-aaaa",
        "think-bbbb",
        "think-cccc",
        "think-ffff",
        "think-gggg",
        "think-eeee",
    ]
    assert named[3][0] == "result-requests.yaml open issue #282 queued result later"
    assert named[0][0] == "source-coverage.yaml pending_catalogue_intake n=69"
    assert deferrals(tmp_path / "absent", tmp_path / "absent", tmp_path / "absent") == []


def test_a_results_validation_beads_are_held_open_on_an_open_or_a_closed_issue(
    tmp_path: Path,
) -> None:
    """Rule P1 of 26 October 2026: an issue closes once answered while a result's
    validation is still owned by beads, so those beads are held open after the close,
    and closing one fails until the record names its successor or drops the field."""
    requests = _write(
        tmp_path / "requests.yaml",
        "issues:\n"
        "  - number: 420\n"
        "    state: closed\n"
        "    answer_bead: think-cccc\n"
        "    results: [{key: lean, validation: [think-hhhh, think-iiii]}]\n"
        "  - number: 446\n"
        "    state: open\n"
        "    answer_bead: think-jjjj\n"
        "    results: [{key: census, validation: [think-kkkk]}]\n",
    )
    named = deferrals(tmp_path / "absent", requests, tmp_path / "absent")
    assert named == [
        ("result-requests.yaml #420 lean validation", "think-hhhh"),
        ("result-requests.yaml #420 lean validation", "think-iiii"),
        ("result-requests.yaml #446 census validation", "think-kkkk"),
        ("result-requests.yaml open issue #446", "think-jjjj"),
    ]
    beads = [_bead("is-01hhhh", "closed", "a finished replay"), _bead("is-01iiii", "open", "x")]
    problems = deferral_problems(beads, {"hhhh": "01hhhh", "iiii": "01iiii"}, named[:2])
    assert [p["status"] for p in problems] == ["closed"]


def test_a_queued_item_that_names_no_bead_is_collected_as_unowned_and_fails(
    tmp_path: Path,
) -> None:
    """The schema requires a queued result's and ask's bead (think-du1e); a record the
    schema check did not see still fails here rather than only in the sweep's report."""
    requests = _write(
        tmp_path / "requests.yaml",
        "issues:\n"
        "  - number: 282\n"
        "    state: open\n"
        "    answer_bead: think-cccc\n"
        "    results: [{key: later, queued: true}]\n"
        "    asks: [{what: a fix, state: queued}, {what: done, state: done}]\n",
    )
    named = deferrals(tmp_path / "absent", requests, tmp_path / "absent")
    assert named[1:] == [
        ("result-requests.yaml open issue #282 queued result later", NO_BEAD),
        ("result-requests.yaml open issue #282 queued ask", NO_BEAD),
    ]
    beads = [_bead("is-01cccc", "open", "the answer bead")]
    problems = deferral_problems(beads, {"cccc": "01cccc"}, named)
    assert [(p["parent"][-12:], p["status"]) for p in problems] == [
        ("result later", "unowned"),
        ("2 queued ask", "unowned"),
    ]


def test_a_deferral_whose_bead_is_closed_or_missing_fails_and_a_live_one_passes() -> None:
    """The orphan the 2026-09-30 intakes became, by a closed bead instead of none."""
    beads = [
        _bead("is-01aaaa", "open", "the intake"),
        _bead("is-01bbbb", "closed", "an intake closed under its deferral"),
        _bead("is-01cccc", "blocked", "waiting on a source"),
    ]
    aliases = {"aaaa": "01aaaa", "bbbb": "01bbbb", "cccc": "01cccc"}
    named = [
        ("pending n=69", "think-aaaa"),
        ("pending n=83", "think-bbbb"),
        ("issue #1", "think-cccc"),
        ("pending n=87", "think-zzzz"),
    ]
    problems = deferral_problems(beads, aliases, named)
    assert [(p["parent"], p["status"]) for p in problems] == [
        ("pending n=83", "closed"),
        ("pending n=87", "no such bead"),
    ]
    assert {p["kind"] for p in problems} == {"dead_deferral"}


def test_the_live_records_deferrals_are_all_well_formed_aliases() -> None:
    """What the gate resolves against the store is at least a bead alias, the
    regularization record's included."""
    from devtools import default_drawings  # noqa: PLC0415

    regularization = check_bead_tree.regularization_deferrals()
    allowed = [where for where, _alias in regularization if "PENDING_ALLOWED" in where]
    assert len(allowed) == len(default_drawings.PENDING_ALLOWED)
    # The live list is empty since 16 October 2026; a made-up entry is still reported at
    # its own location and alias (review A2 of #654).
    made_up = default_drawings.deferrals(allowed={7: "think-0000: re-housed by an adoption"})
    assert ("default_drawings.py PENDING_ALLOWED n=7", "think-0000") in made_up
    for where, alias in [*deferrals(), *regularization]:
        assert alias.startswith("think-"), where
        assert len(alias) == len("think-aaaa"), where


def test_a_run_that_takes_its_counts_off_the_allowlist_no_longer_defers_to_its_bead() -> None:
    """Review B4 of #636: each regularization run lane takes its counts off
    `PENDING_ALLOWED` in its own pull request, and that change touches the record, so the
    gate holds every bead the record still names open. The lane's bead is named nowhere
    else in the record, so its change passes whether the bead is open or closed, while the
    other lanes' beads, still named, must be open; the bead is closed once that pull
    request has merged (regularization-process.md, "When a Witness Changes")."""
    from devtools import default_drawings  # noqa: PLC0415

    # The live list is empty since 16 October 2026 (think-3zi3), so two lanes are made up
    # where it names none, as two adoptions' deferrals would name them.
    allowed = default_drawings.PENDING_ALLOWED or {
        1: "think-aaaa: re-housed by one adoption",
        2: "think-bbbb: re-housed by another",
    }
    lanes = sorted(
        {found[0] for why in allowed.values() if (found := default_drawings.BEAD.match(why))}
    )
    assert lanes
    for lane in lanes:
        remaining = {n: why for n, why in allowed.items() if not why.startswith(lane)}
        named = default_drawings.deferrals(allowed=remaining)
        others = sorted({alias for _where, alias in named})
        assert lane not in others
        beads = [
            *(_bead(f"is-01{alias[6:]}", "open", alias) for alias in others),
            _bead(f"is-01{lane[6:]}", "closed", lane),
        ]
        aliases = {alias[6:]: f"01{alias[6:]}" for alias in [*others, lane]}
        assert deferral_problems(beads, aliases, named) == []
        # Its counts still listed, the closed bead fails the change: hence closing it
        # only once the pull request taking them off has merged.
        dead = deferral_problems(beads, aliases, default_drawings.deferrals(allowed=allowed))
        assert {problem["bead"] for problem in dead} == {lane}


def test_a_staged_house_adoption_keeps_its_bead_open() -> None:
    """Each count `select_houses.PENDING_ADOPTION` stages names the bead that adopts it,
    and each correction an adoption waits for (`CORRECTIONS_OWED`, review B1 of #658)
    names the bead that makes it, and the gate reads them: closing the bead while a count
    is staged or a correction owed is a dead deferral (result-import.md, "The House
    Rule")."""
    from devtools import select_houses  # noqa: PLC0415

    named = check_bead_tree.adoption_deferrals()
    assert named == select_houses.deferrals()
    assert len(named) == len(select_houses.PENDING_ADOPTION) + len(
        select_houses.CORRECTIONS_OWED
    )
    lanes = sorted({alias for _where, alias in named})
    assert lanes
    beads = [_bead(f"is-01{alias[6:]}", "open", alias) for alias in lanes]
    aliases = {alias[6:]: f"01{alias[6:]}" for alias in lanes}
    assert deferral_problems(beads, aliases, named) == []
    closed = [_bead(f"is-01{alias[6:]}", "closed", alias) for alias in lanes]
    dead = deferral_problems(closed, aliases, named)
    assert {problem["bead"] for problem in dead} == set(lanes)


def _dead_deferral_store(monkeypatch: pytest.MonkeyPatch) -> None:
    """A store whose one deferral names a closed bead, and no agendas."""
    beads = [_bead("is-01aaaa", "closed", "an intake closed under its deferral")]
    monkeypatch.setattr(check_bead_tree, "load", lambda: (beads, "fixture", {"aaaa": "01aaaa"}))
    monkeypatch.setattr(check_bead_tree, "deferrals", lambda: [("pending n=69", "think-aaaa")])
    monkeypatch.setattr(check_bead_tree, "regularization_deferrals", list)
    monkeypatch.setattr(check_bead_tree, "adoption_deferrals", list)
    monkeypatch.setattr(check_bead_tree, "AGENDAS", Path("/nonexistent/agendas"))


def test_a_dead_deferral_fails_the_check_and_is_a_warning_under_the_gates_flag(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Closing a bead a record names turned every pull request red with no tracked change.

    Run directly the check still fails it; the gate passes the flag when the change
    touches no record that declares a deferral, and then it is printed and passes.
    """
    _dead_deferral_store(monkeypatch)
    assert check_bead_tree.main([]) == 1
    assert "FAIL pending n=69 names think-aaaa (closed)" in capsys.readouterr().out
    assert check_bead_tree.main([check_bead_tree.WARN_DEAD_DEFERRALS]) == 0
    shown = capsys.readouterr().out
    assert "WARN pending n=69 names think-aaaa (closed)" in shown
    assert "FAIL" not in shown
    assert check_bead_tree.main(["--json", check_bead_tree.WARN_DEAD_DEFERRALS]) == 0
    report = json.loads(capsys.readouterr().out)
    assert (report["status"], report["problems"]) == ("ok", [])
    assert [w["bead"] for w in report["warnings"]] == ["think-aaaa"]


WARN = ("--warn-dead-deferrals",)


@pytest.mark.parametrize(
    ("changed", "arguments"),
    [
        (["packing/devtools/intake_sweep.py", "README.md"], WARN),
        (["packing/campaign/intake-watch.yaml"], ()),
        (["packing/frontier/source-coverage.yaml", "README.md"], ()),
        # The regularization record's allowlist, exemptions and owed runs (#636 A2).
        (["packing/devtools/default_drawings.py"], ()),
        # The house adoptions staged to a later pull request (the house rule).
        (["packing/devtools/select_houses.py"], ()),
        (None, ()),
    ],
)
def test_the_gate_fails_a_dead_deferral_only_on_a_change_to_a_record_declaring_one(
    monkeypatch: pytest.MonkeyPatch, changed: list[str] | None, arguments: tuple[str, ...]
) -> None:
    """`None` is a checkout where `origin/main` does not resolve: it cannot say what
    changed, so the dead deferral fails it."""
    observed: list[tuple[str, ...]] = []

    def capture(_context: validate.Context, module: str, *given: str) -> str:
        observed.append((module, *given))
        return "  ok"

    def paths(since: str) -> list[str]:
        assert since == "origin/main"
        if changed is None:
            raise validate.UsageError("--since 'origin/main' does not name a commit")
        return changed

    monkeypatch.setattr(validate, "_module", capture)
    monkeypatch.setattr(validate, "changed_paths", paths)
    context = validate.Context(
        deep=False, strict=False, jobs=1, inner_jobs=1, environment=os.environ.copy()
    )
    step = validate._bead_tree  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    assert step(context) == "  ok"
    assert observed == [("devtools.check_bead_tree", *arguments)]
    assert (check_bead_tree.WARN_DEAD_DEFERRALS,) == WARN


def test_the_gate_reads_the_staged_house_adoptions(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Review B7 of #660: removing `adoption_deferrals()` from `main` left every test
    green, so a refactor could unwire the gate and let a bead close while its counts were
    staged. A closed bead under a staged count fails the gate itself."""
    from devtools import select_houses  # noqa: PLC0415

    beads = [_bead("is-01bbbb", "closed", "an adoption closed while its count is staged")]
    monkeypatch.setattr(check_bead_tree, "load", lambda: (beads, "fixture", {"bbbb": "01bbbb"}))
    monkeypatch.setattr(check_bead_tree, "deferrals", list)
    monkeypatch.setattr(check_bead_tree, "regularization_deferrals", list)
    monkeypatch.setattr(check_bead_tree, "AGENDAS", Path("/nonexistent/agendas"))
    staged = select_houses.Pending(
        house="T-174", bead="think-bbbb", why=select_houses.NEXT_PULL_REQUEST
    )
    monkeypatch.setattr(select_houses, "PENDING_ADOPTION", {68: staged})
    assert check_bead_tree.main([]) == 1
    assert "FAIL select_houses.PENDING_ADOPTION n=68 (T-174) names think-bbbb (closed)" in (
        capsys.readouterr().out
    )
