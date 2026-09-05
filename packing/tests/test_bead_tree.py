"""The bead staleness report: two shapes the tree checker prints and never fails on.

The bead tree and the agenda layer are edited by different hands at different times.
Cells name beads through a `think-` alias the store's table resolves; an in-progress
bead named only by terminal cells is work the agenda finished with, and one named by
no cell is work tracked outside the agenda layer. These pin the join and the two
counts on a fixture small enough to read.
"""

from __future__ import annotations

from devtools.check_bead_tree import check, parse_aliases, staleness


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
    table = "schema_version: 1\n---\n1e10: 01aaaa\nnull: 01bbbb\n# note\nrh18: 01cccc\n"
    assert parse_aliases(table) == {
        "schema_version": "1",
        "1e10": "01aaaa",
        "null": "01bbbb",
        "rh18": "01cccc",
    }


def test_a_bead_without_an_alias_is_reported_by_its_id() -> None:
    report = staleness([OUTSIDE], {}, [_cell("BC-001", "ready", "think-bbbb")])
    assert [entry["bead"] for entry in report["untracked"]] == ["is-01bbbb"]


def test_the_report_does_not_change_the_gate_verdict() -> None:
    """Both shapes are reports; the tree's two invariants still decide pass or fail."""
    assert check([FINISHED, OUTSIDE]) == []
