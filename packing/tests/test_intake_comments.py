"""Report-order verdict comments, on a synthetic ledger and on the committed 2026-10-14 pass."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import yaml

from devtools import intake_comments as comments
from devtools.check_requests import FOOTER

PASS_2026_10_14 = comments.ROOT / "campaign/issue-intake/upper-bounds-20261014/comments.yaml"


def step(report: str, verdict: str, reason: str, against: str, **more: Any) -> dict[str, Any]:
    difference = {"below": "below by 1.00e-03", "above": "above by 2.00e-03"}.get(reason, "")
    return {
        "report": report,
        "side": "10.000000000000",
        "verdict": verdict,
        "reason": reason,
        "decided_against": [against],
        "difference": "equal" if reason == "equal" else difference,
        **more,
    }


def count(n: int, steps: list[dict[str, Any]], best: str = "#2") -> dict[str, Any]:
    return {
        "n": n,
        "start": [{"label": "record T-001", "holders": "ry-xu", "side": "10.5"}],
        "steps": steps,
        "best_now": [{"label": best, "side": "9.9"}],
    }


def ledger(*counts: dict[str, Any]) -> dict[str, Any]:
    return {
        "format": comments.LEDGER_FORMAT,
        "counts": list(counts),
        "reports": [
            {"report": "#1", "holders": "A. Finder (afinder)", "kind": "issue"},
            {"report": "#2", "holders": "B. Holder (bholder)", "kind": "issue"},
            {"report": "#1 comment 99", "holders": "A. Finder (afinder)", "kind": "comment"},
            {"report": "o/r@abc1234", "holders": "C. Pub (cpub)", "kind": "publication"},
        ],
    }


def write_pass(tmp_path: Path, data: dict[str, Any], **raw: Any) -> Path:
    _ = (tmp_path / "ledger.json").write_text(json.dumps(data), encoding="utf-8")
    raw.setdefault("records_pr", "jlevy/squares#999")
    raw.setdefault("handles", {"ry-xu": "Ryan Xu"})
    raw.setdefault("skip", [{"report": "#1 comment 99", "reason": "covered elsewhere"}])
    raw.setdefault("comments", [{"issue": 1}, {"issue": 2}])
    path = tmp_path / "comments.yaml"
    _ = path.write_text(yaml.safe_dump(raw), encoding="utf-8")
    return path


def basic(tmp_path: Path, **raw: Any) -> dict[str, str]:
    data = ledger(
        count(
            100,
            [
                step(
                    "#1", "recorded", "below", "record T-001", packing={"kind": "new packing"}
                ),
                step("#2", "recorded", "below", "#1"),
            ],
        ),
        count(101, [step("#2", "not recorded", "above", "record T-001")], best="record T-001"),
    )
    return comments.drafts(comments.load(write_pass(tmp_path, data, **raw)))


def test_a_comment_opens_with_the_author_and_the_rule_and_ends_with_the_footer(
    tmp_path: Path,
) -> None:
    text = basic(tmp_path)["1.md"]
    assert text.startswith("@afinder, thank you; this is the report-order evaluation")
    assert comments.RULE in text
    assert "the records pull request jlevy/squares#999" in text
    assert text.endswith("\n\n" + FOOTER + "\n")


def test_each_verdict_names_what_it_was_decided_against(tmp_path: Path) -> None:
    out = basic(tmp_path)
    assert (
        "| 100 | 10.000000000000 | recorded: a new packing; 1.00e-03 below the record on main "
        "(Ryan Xu) | #2 (B. Holder) 9.9 |"
    ) in out["1.md"]
    assert (
        "recorded; the source does not say new packing or refinement; 1.00e-03 below #1"
        in (out["2.md"])
    )
    assert "not recorded: 2.00e-03 above the record on main (Ryan Xu)" in out["2.md"]
    assert "| 100 | 10.000000000000 | recorded; " in out["2.md"]
    assert "| this report 9.9 |" in out["2.md"]


def test_a_margin_keeps_its_at_least_or_about_qualifier(tmp_path: Path) -> None:
    # intake_ledger._difference writes "at least" for separated spans and "about" where
    # they meet; the qualifier stays before the number, never in its place.
    data = ledger(
        count(
            100,
            [
                step(
                    "#1",
                    "recorded",
                    "below",
                    "record T-001",
                    difference="below by at least 4.00e-13",
                )
            ],
        ),
        count(
            101,
            [
                step(
                    "#2",
                    "not recorded",
                    "above",
                    "record T-001",
                    difference="above by about 1.23e-15",
                )
            ],
            best="record T-001",
        ),
    )
    out = comments.drafts(comments.load(write_pass(tmp_path, data)))
    assert "; at least 4.00e-13 below the record on main (Ryan Xu)" in out["1.md"]
    assert "not recorded: about 1.23e-15 above the record on main (Ryan Xu)" in out["2.md"]


def test_the_index_lists_each_comment_with_its_verdicts(tmp_path: Path) -> None:
    index = basic(tmp_path)[comments.INDEX]
    assert "| 1.md | #1 | recorded at 100 |" in index
    assert "| 2.md | #2 | recorded at 100; not recorded at 101 |" in index


def test_a_handle_is_named_where_it_stands_as_a_name_and_kept_as_an_identifier(
    tmp_path: Path,
) -> None:
    intake = comments.load(write_pass(tmp_path, ledger(count(100, []))))
    assert (
        intake.clean_holders("ry-xu, improved by B. Holder") == "Ryan Xu, improved by B. Holder"
    )
    assert intake.detag("continuing ry-xu's arrangement (ry-xu)") == (
        "continuing Ryan Xu's arrangement (Ryan Xu)"
    )
    kept = "ry-xu/square-packing, github.com/ry-xu, @ry-xu and `ry-xu`"
    assert intake.detag(kept) == kept


def test_a_note_loses_its_ids_and_lane_names(tmp_path: Path) -> None:
    intake = comments.load(write_pass(tmp_path, ledger(count(100, []))))
    note = "Couzo's arrangement (T-042), after the record T-007 (the couzo lane's README)"
    assert intake.detag(note) == "Couzo's arrangement (on main), after the record on main"


def test_a_refinement_of_the_finders_own_packing_reads_the_wording_from_data(
    tmp_path: Path,
) -> None:
    mine = {"kind": "refinement", "packing_of": "A. Finder (afinder)", "entry": "#1"}
    theirs = {"kind": "refinement", "packing_of": "Ryan Xu (ry-xu)", "entry": "T-001"}
    data = ledger(
        count(100, [step("#1", "recorded", "below", "#2", packing=mine)]),
        count(101, [step("#1 comment 99", "recorded", "below", "#2", packing=mine)]),
        count(102, [step("#1", "recorded", "below", "record T-001", packing=theirs)]),
    )
    raw = {
        "skip": [{"report": "#2", "reason": "covered elsewhere"}],
        "comments": [
            {"issue": 1},
            {
                "issue": 7,
                "author": "afinder",
                "reports": ["#1 comment 99"],
                "wording": {"self_refinement": "a refinement of {finder}'s own packing{via}"},
            },
        ],
    }
    out = comments.drafts(comments.load(write_pass(tmp_path, data, **raw)))
    assert "recorded: a refinement of the finder's own packing as #1 gives it;" in out["1.md"]
    assert "recorded: a refinement of A. Finder's own packing as #1 gives it;" in out["7.md"]
    assert (
        "recorded: a refinement of Ryan Xu's packing; credited to this report's finder, "
        "after Ryan Xu; 1.00e-03 below the record on main (Ryan Xu)"
    ) in out["1.md"]


def test_ties_restatements_and_undecided_claims(tmp_path: Path) -> None:
    data = ledger(
        count(
            100,
            [
                step(
                    "#1",
                    "not recorded",
                    "equal",
                    "#2",
                    restates="restates #2's packing (T-009)",
                ),
                step("#2", "not recorded", "equal", "record T-001"),
            ],
        ),
        count(
            101,
            [
                step(
                    "#1",
                    "undecided",
                    "undecided",
                    "record T-001",
                    decide_by="T-001's exact side",
                )
            ],
        ),
    )
    out = comments.drafts(comments.load(write_pass(tmp_path, data)))
    assert (
        "not recorded: equal to #2 (B. Holder), reported first; restates #2's packing (on main)"
        in (out["1.md"])
    )
    assert "not recorded: equal to the record on main (Ryan Xu) |" in out["2.md"]
    assert (
        "undecided against the record on main (Ryan Xu) at print precision; decided by that "
        "entry's exact side"
    ) in out["1.md"]


def test_publications_comments_rows_and_the_grid_are_described(tmp_path: Path) -> None:
    data = ledger(
        count(100, [step("#1", "recorded", "below", "o/r@abc1234")]),
        count(101, [step("#1", "recorded", "below", "#1 comment 99")]),
        {
            "n": 400,
            "start": [{"label": "the grid", "holders": "", "side": "20"}],
            "steps": [step("#1", "recorded", "below", "the grid")],
            "best_now": [{"label": "#1", "side": "19.9"}],
        },
        {
            "n": 401,
            "start": [{"label": "beyond-horizon row x-2026", "holders": "", "side": "20"}],
            "steps": [step("#1", "recorded", "below", "beyond-horizon row x-2026")],
            "best_now": [{"label": "#1", "side": "19.9"}],
        },
    )
    raw = {
        "comments": [{"issue": 1}],
        "skip": [
            {"report": "#2", "reason": "covered elsewhere"},
            {"report": "#1 comment 99", "reason": "covered elsewhere"},
        ],
    }
    text = comments.drafts(comments.load(write_pass(tmp_path, data, **raw)))["1.md"]
    assert "below C. Pub's publication `o/r@abc1234`" in text
    assert "below A. Finder's update comment on #1" in text
    assert "below the grid bound 20" in text
    assert "below the row on main |" in text


def test_a_draft_that_names_an_id_or_a_tree_or_blob_link_is_refused(tmp_path: Path) -> None:
    # A tree/ or blob/ link is refused into main as well as into a branch.
    for note in (
        "registered as T-123",
        "see https://github.com/o/r/tree/abc",
        "see https://github.com/jlevy/squares/blob/main/README.md",
    ):
        with pytest.raises(comments.CommentsError, match="refused"):
            _ = basic(tmp_path, comments=[{"issue": 1, "notes": [note]}, {"issue": 2}])


def test_a_result_report_with_no_comment_and_no_skip_is_refused(tmp_path: Path) -> None:
    with pytest.raises(comments.CommentsError, match="no comment and no stated skip: #2"):
        _ = basic(tmp_path, comments=[{"issue": 1}])


def test_the_summary_layouts_group_the_verdicts(tmp_path: Path) -> None:
    refines = {"kind": "refinement", "packing_of": "Ryan Xu (ry-xu)", "entry": "T-001"}
    data = ledger(
        count(100, [step("#1", "recorded", "below", "record T-001", packing=refines)]),
        count(101, [step("#1", "recorded", "below", "record T-001", packing=refines)]),
        count(102, [step("#1", "not recorded", "equal", "record T-001")]),
        count(103, [step("#1", "not recorded", "above", "record T-001")]),
        count(104, [step("#1", "undecided", "undecided", "record T-001")]),
    )
    headings = {
        "recorded": "Recorded refinements",
        "equal": "Ties",
        "above": "Above",
        "undecided": "Undecided",
    }
    raw = {
        "skip": [
            {"report": "#2", "reason": "covered elsewhere"},
            {"report": "#1 comment 99", "reason": "covered elsewhere"},
        ],
        "comments": [
            {"issue": 1, "layout": "by-finder", "headings": headings, "undecided_note": "why"},
            {"issue": 5, "reports": ["#1"], "author": "afinder", "layout": "by-count"},
        ],
    }
    out = comments.drafts(comments.load(write_pass(tmp_path, data, **raw)))
    finder = out["1.md"]
    assert "- **Recorded refinements:**\n  - Ryan Xu: 100-101\n- **Ties:** 102.\n" in finder
    assert "- **Above:** 103, 2.00e-03 above the record on main (Ryan Xu).\n" in finder
    assert "- **Undecided:** 104; why.\n" in finder
    assert "<details><summary>Every count</summary>" in finder
    by_count = out["5.md"]
    assert (
        "- **100:** 10.000000000000, recorded: a refinement of Ryan Xu's packing;" in by_count
    )
    assert "- **102:** 10.000000000000, not recorded: equal to the record on main" in by_count
    assert "- **Not recorded, above the record on main (Ryan Xu):** 103.\n" in by_count
    assert "- **Undecided at print precision:** 104.\n" in by_count


def test_by_finder_states_a_claim_above_a_pending_register_entry(tmp_path: Path) -> None:
    data = ledger(
        count(103, [step("#1", "not recorded", "above", "record T-001")]),
        count(106, [step("#1", "not recorded", "above", "register T-121, pending adoption")]),
    )
    headings = dict.fromkeys(comments.BY_FINDER_HEADINGS, "x") | {"above": "Above"}
    raw = {
        "skip": [
            {"report": "#2", "reason": "covered elsewhere"},
            {"report": "#1 comment 99", "reason": "covered elsewhere"},
        ],
        "comments": [{"issue": 1, "layout": "by-finder", "headings": headings}],
    }
    text = comments.drafts(comments.load(write_pass(tmp_path, data, **raw)))["1.md"]
    assert (
        "- **Above:** 103, 2.00e-03 above the record on main (Ryan Xu); "
        "106, 2.00e-03 above a register entry pending adoption.\n"
    ) in text
    # A claim held by another report still has no line its headings can say.
    data["counts"].append(count(107, [step("#1", "not recorded", "above", "#2")]))
    with pytest.raises(comments.CommentsError, match="or a pending register entry only"):
        _ = comments.drafts(comments.load(write_pass(tmp_path, data, **raw)))


def test_by_finder_refuses_what_its_headings_cannot_say(tmp_path: Path) -> None:
    data = ledger(
        count(100, [step("#1", "recorded", "below", "#2", packing={"kind": "new packing"})]),
        count(101, [step("#2", "recorded", "below", "record T-001")]),
    )
    headings = dict.fromkeys(comments.BY_FINDER_HEADINGS, "x")
    raw = {
        "comments": [{"issue": 1, "layout": "by-finder", "headings": headings}, {"issue": 2}]
    }
    with pytest.raises(comments.CommentsError, match="refinements only"):
        _ = comments.drafts(comments.load(write_pass(tmp_path, data, **raw)))


def test_a_comments_file_without_its_records_pull_request_is_refused(tmp_path: Path) -> None:
    path = write_pass(tmp_path, ledger(count(100, [])), records_pr="")
    with pytest.raises(comments.CommentsError, match="records_pr"):
        _ = comments.load(path)


def test_check_reports_a_changed_or_missing_draft(tmp_path: Path) -> None:
    expected = basic(tmp_path)
    out = tmp_path / "out"
    assert comments.main([str(tmp_path / "comments.yaml"), "--out", str(out)]) == 0
    assert comments.main([str(tmp_path / "comments.yaml"), "--check", str(out)]) == 0
    _ = (out / "1.md").write_text(
        expected["1.md"].replace("thank you", "thanks"), encoding="utf-8"
    )
    (out / "2.md").unlink()
    problems = comments.check(expected, out)
    assert problems[0].startswith("--- 1.md (found)")
    assert problems[1] == "2.md: missing"
    assert comments.main([str(tmp_path / "comments.yaml"), "--check", str(out)]) == 1


def test_the_2026_10_14_pass_drafts_one_comment_per_result_issue() -> None:
    intake = comments.load(PASS_2026_10_14)
    # The comments file sits in the intake directory and names no ledger: it reads its own.
    beside = json.loads((PASS_2026_10_14.parent / "ledger.json").read_text(encoding="utf-8"))
    assert intake.ledger == beside
    out = comments.drafts(intake)
    assert len(out) == len(intake.comments) + 1
    for comment in intake.comments:
        text = out[f"{comment.name}.md"]
        assert text.startswith(f"@{comment.author}, thank you;")
        assert comments.RULE in text
        assert "the records pull request jlevy/squares#602" in text
        assert text.endswith(FOOTER + "\n")
