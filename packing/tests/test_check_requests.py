"""The result requests record joins each issue to the register; the tool says what each is owed.

`devtools.check_requests` derives each reported result's state, whether a reply is due
and whether the issue can be closed from `campaign/result-requests.yaml` and the
register, and stores none of it. These hold the live record to its schema and ids, each
derivation to a synthetic register, the draft to its footer and its refusal off `main`,
and the GitHub comparison to a recorded fetch.
"""

from __future__ import annotations

import copy
import re
from collections.abc import Mapping
from typing import Any

import pytest

from devtools import check_requests
from devtools.check_requests import (
    CONFIRMED,
    DEFECT,
    FOOTER,
    OPEN,
    QUEUED,
    REFUTED,
    Register,
)

Record = dict[str, Any]
URL = "https://github.com/owner/repo/issues/7#issuecomment-{}"


def result_entry(
    rid: str, verification: str, confirmation: str, *evidence: str, **more: Any
) -> Record:
    return {
        "id": rid,
        "verification": verification,
        "confirmation": confirmation,
        "evidence": list(evidence),
        "next_rung": f"{rid}'s next rung (think-abcd).",
        **more,
    }


REGISTER = Register(
    results={
        "T-001": result_entry("T-001", "V3", "C3", "E-replay"),
        "T-002": result_entry("T-002", "V0", "C1", "E-report"),
        "T-003": result_entry("T-003", "V3", "C1", "E-defect"),
        "T-004": result_entry(
            "T-004",
            "V3",
            "C3",
            "E-replay",
            reviews=[{"path": "docs/r.md", "date": "2026-10-01", "verdict": "refuted"}],
        ),
        "T-005": result_entry(
            "T-005",
            "V0",
            "C0",
            "E-report",
            activity={
                "state": "in-analysis",
                "what": "a replay",
                "since": "2026-10-01",
                "link": "think-abcd",
            },
        ),
    },
    evidence={
        "E-report": {
            "origin": "external",
            "assurance": "reported",
            "replay_status": "not-attempted",
        },
        "E-replay": {
            "origin": "replayed-here",
            "assurance": "verified",
            "replay_status": "passed",
            "relationship_to_generator": "same-implementation",
            "verifiers": ["V-zmx2"],
        },
        "E-defect": {
            "origin": "external",
            "assurance": "verified",
            "external_review": {"state": "defect-found", "date": "2026-10-01"},
        },
    },
    verifiers={"V-zmx2": "zmx2", "V-sqpack": "sqpack.fractional"},
)


def issue(**over: Any) -> Record:
    base: Record = {
        "number": 7,
        "title": "A request",
        "author": "someone",
        "opened": "2026-10-01",
        "state": "open",
        "kind": "result-report",
        "triage": "done",
        "summary": "It reports a bound.",
        "read_through": "2026-10-01T00:00:00Z",
        "results": [{"key": "bound", "claim": "s(9) >= 3", "register": ["T-001"]}],
        "beads": ["think-abcd"],
        "answer_bead": "think-efgh",
        "replies": [],
        "close_when": "T-001 is confirmed.",
    }
    base.update(over)
    return base


def record(*issues: Record) -> Record:
    return {
        "softschema": {
            "contract": "packing.squares:ResultRequests/v1",
            "schema": "schemas/result-requests.schema.yaml",
            "status": "enforced",
        },
        "repository": "owner/repo",
        "owner": "owner",
        "last_reviewed": "2026-10-02",
        "issues": list(issues) or [issue()],
    }


def reply(number: int, date: str = "2026-10-02", **over: Any) -> Record:
    return {
        "url": URL.format(number),
        "date": date,
        "by": "owner",
        "kind": "import",
        "reported": [],
        **over,
    }


def test_the_live_record_holds_its_schema_and_every_id_it_names_exists(
    capsys: pytest.CaptureFixture[str],
) -> None:
    live = check_requests.load_record()
    assert check_requests.problems(live, check_requests.load_register()) == []
    assert check_requests.main([]) == 0
    assert "every id resolves" in capsys.readouterr().out


def test_the_live_record_has_one_entry_an_issue_and_names_its_answer_bead() -> None:
    live = check_requests.load_record()
    numbers = [entry["number"] for entry in live["issues"]]
    assert len(numbers) == len(set(numbers))
    assert {170, 227, 238, 247, 256, 279, 280, 281, 282, 294, 295, 296, 308} <= set(numbers)
    assert all(entry["answer_bead"].startswith("think-") for entry in live["issues"])


@pytest.mark.parametrize(
    ("mutate", "expected"),
    [
        (
            lambda r: r["issues"][0]["results"][0].update(register=["T-999"]),
            "T-999 is not in results.yaml",
        ),
        (
            lambda r: r["issues"][0]["results"][0].update(evidence=["E-none"]),
            "E-none is not in evidence.yaml",
        ),
        (
            lambda r: r["issues"][0]["replies"].append(
                reply(1) | {"url": "https://github.com/owner/repo/issues/8#issuecomment-1"}
            ),
            "is not a comment on this issue",
        ),
        (
            lambda r: r["issues"][0]["replies"].append(
                reply(1, reported=[{"result": "bound", "id": "T-002"}])
            ),
            "record a renumbered id as `as`",
        ),
        (
            lambda r: r["issues"][0]["replies"].append(
                reply(1, reported=[{"result": "other"}])
            ),
            "unknown result 'other'",
        ),
        (
            lambda r: r["issues"][0]["replies"].extend(
                [reply(1, "2026-10-03"), reply(2, "2026-10-02")]
            ),
            "dated before the one above it",
        ),
        (
            lambda r: r["issues"][0]["replies"].append(reply(1, corrects=[URL.format(9)])),
            "which is not an earlier reply here",
        ),
        (
            lambda r: r["issues"].append(copy.deepcopy(r["issues"][0])),
            "issue #7 is recorded twice",
        ),
        (lambda r: r["issues"][0].update(state="closed"), "closed"),
        (lambda r: r["issues"][0].update(answer_bead="other-1234"), "answer_bead"),
    ],
)
def test_the_check_refuses_an_unknown_id_a_misplaced_reply_and_a_broken_schema(
    mutate: Any, expected: str
) -> None:
    broken = record(issue())
    mutate(broken)
    found = check_requests.problems(broken, REGISTER)
    assert any(expected in problem for problem in found), found


def test_a_result_is_confirmed_at_v3_c3_and_open_below_it() -> None:
    confirmed = check_requests.result_state(
        {"key": "a", "claim": "c", "register": ["T-001"]}, REGISTER
    )
    assert (confirmed.state, confirmed.settled) == (CONFIRMED, True)
    reviewed = check_requests.result_state(
        {"key": "a", "claim": "c", "register": ["T-002"]}, REGISTER
    )
    assert (reviewed.state, reviewed.settled) == (OPEN, False)
    both = check_requests.result_state(
        {"key": "a", "claim": "c", "register": ["T-001", "T-002"]}, REGISTER
    )
    assert both.state == OPEN


def test_a_defect_or_refutation_decides_a_result_and_settles_only_a_refutation() -> None:
    defect = check_requests.result_state(
        {"key": "a", "claim": "c", "register": ["T-003"]}, REGISTER
    )
    assert (defect.state, defect.settled) == (DEFECT, False)
    refuted = check_requests.result_state(
        {"key": "a", "claim": "c", "register": ["T-004"]}, REGISTER
    )
    assert (refuted.state, refuted.settled) == (REFUTED, True)


def test_a_reported_defect_is_settled_when_the_record_holds_it() -> None:
    held = {"key": "a", "claim": "c", "evidence": ["E-defect"], "defect": True}
    assert check_requests.result_state(held, REGISTER).settled
    unheld = {"key": "a", "claim": "c", "register": ["T-002"], "defect": True}
    assert not check_requests.result_state(unheld, REGISTER).settled


def test_a_report_entry_beside_a_confirmed_register_entry_does_not_hold_it_open() -> None:
    beside = {"key": "a", "claim": "c", "register": ["T-001"], "evidence": ["E-report"]}
    assert check_requests.result_state(beside, REGISTER).state == CONFIRMED
    evidence_only = {"key": "a", "claim": "c", "evidence": ["E-replay"]}
    assert check_requests.result_state(evidence_only, REGISTER).state == CONFIRMED


def test_a_result_not_registered_is_settled_unless_it_is_queued() -> None:
    queued = {"key": "a", "claim": "c", "not_registered": "later", "queued": True}
    assert (
        check_requests.result_state(queued, REGISTER).state,
        check_requests.result_state(queued, REGISTER).settled,
    ) == (QUEUED, False)
    declined = {"key": "a", "claim": "c", "not_registered": "below the bound", "queued": False}
    assert check_requests.result_state(declined, REGISTER).settled


def due(entry: Record) -> list[str]:
    return list(check_requests.issue_state(entry, REGISTER).replies_due)


def test_an_issue_with_no_reply_is_owed_an_acknowledgement_and_the_import() -> None:
    reasons = due(issue())
    assert reasons[0].startswith("an acknowledgement")
    assert any(
        "T-001 at V3/C3" in reason and "no reply has said so" in reason for reason in reasons
    )


def test_a_pending_triage_is_owed_only_the_acknowledgement() -> None:
    assert due(issue(triage="pending", results=[])) == [
        "an acknowledgement, once triage has mapped the claims"
    ]


def test_a_reply_that_states_the_current_state_leaves_nothing_due() -> None:
    said = [
        {
            "result": "bound",
            "id": "T-001",
            "verification": "V3",
            "confirmation": "C3",
            "status": "confirmed",
        }
    ]
    assert due(issue(replies=[reply(1, reported=said)])) == []


def test_a_moved_rung_a_renumbered_id_and_an_unnamed_entry_are_each_due() -> None:
    said = [
        {
            "result": "bound",
            "id": "T-001",
            "as": "T-058",
            "verification": "V4",
            "confirmation": "C4",
        }
    ]
    reasons = due(issue(replies=[reply(1, reported=said)]))
    assert any("named T-001 as T-058" in reason for reason in reasons)
    assert any("stated T-001 at V4/C4; it is now V3/C3" in reason for reason in reasons)
    acknowledged = due(issue(replies=[reply(1, reported=[{"result": "bound"}])]))
    assert acknowledged == ["bound: T-001 at V3/C3: confirmed since the reply of 2026-10-02"]


def test_an_outdated_statement_is_due_until_a_later_reply_corrects_it() -> None:
    said = [{"result": "bound", "id": "T-001", "verification": "V3", "confirmation": "C3"}]
    first = reply(1, "2026-10-01", reported=said, outdated=["a link into a branch"])
    assert due(issue(replies=[first])) == [
        "a follow-up: the reply of 2026-10-01 said a link into a branch"
    ]
    unrelated = reply(2, "2026-10-02")
    assert len(due(issue(replies=[first, unrelated]))) == 1
    fixed = reply(2, "2026-10-02", corrects=[URL.format(1)])
    assert due(issue(replies=[first, fixed])) == []


def test_closeable_needs_every_result_settled_triage_done_and_no_ask_queued() -> None:
    assert check_requests.issue_state(issue(), REGISTER).closeable
    asked = issue(asks=[{"what": "change the text", "state": "queued"}])
    state = check_requests.issue_state(asked, REGISTER)
    assert not state.closeable
    assert state.blockers == ("asked: change the text",)
    assert not check_requests.issue_state(issue(triage="pending"), REGISTER).closeable
    open_result = issue(results=[{"key": "b", "claim": "c", "register": ["T-002"]}])
    assert check_requests.issue_state(open_result, REGISTER).blockers == ("b is open",)


@pytest.mark.parametrize(
    ("relation", "expected"),
    [
        (
            {"relationship_to_generator": "same-implementation", "verifiers": ["V-zmx2"]},
            "reproduced here with the author's own checker (zmx2)",
        ),
        (
            {
                "relationship_to_generator": "independent-implementation",
                "verifiers": ["V-sqpack", "V-zmx2"],
            },
            "re-verified here by an independent implementation (sqpack.fractional, zmx2)",
        ),
        (
            {"relationship_to_generator": "same-implementation"},
            "reproduced here with the author's own checker",
        ),
        (
            {
                "relationship_to_generator": "independent-implementation",
                "verifiers": ["V-gone"],
            },
            "re-verified here by an independent implementation",
        ),
        (
            {
                "relationship_to_generator": "same-implementation",
                "origin": "independently-external",
            },
            "reproduced by a third party with the author's own checker",
        ),
        ({"relationship_to_generator": "unknown-historical"}, ""),
        ({}, ""),
    ],
)
def test_a_confirmation_says_whose_code_reproduced_it(
    relation: Mapping[str, Any], expected: str
) -> None:
    entry = {"origin": "replayed-here", **relation}
    assert check_requests.verifier_phrase(entry, REGISTER.verifiers) == expected


def test_verifier_names_come_from_the_verifiers_file_and_nothing_without_it(
    tmp_path: Any,
) -> None:
    assert check_requests.load_verifiers(tmp_path / "absent.yaml") == {}
    listed = tmp_path / "listed.yaml"
    listed.write_text(
        "verifiers:\n  - id: V-a\n    name: zmx2\n  - id: V-b\n", encoding="utf-8"
    )
    assert check_requests.load_verifiers(listed) == {"V-a": "zmx2", "V-b": "V-b"}
    mapped = tmp_path / "mapped.yaml"
    mapped.write_text("V-c:\n  program: zm_mixed.py\n", encoding="utf-8")
    assert check_requests.load_verifiers(mapped) == {"V-c": "zm_mixed.py"}


def test_an_exact_value_is_described_by_its_lower_half_and_not_by_the_grid() -> None:
    grid = {
        "claim": "upper-bound",
        "origin": "replayed-here",
        "replay_status": "passed",
        "relationship_to_generator": "independent-implementation",
    }
    lower = {**REGISTER.evidence["E-replay"], "claim": "lower-bound"}
    exact = Register(
        results={
            "T-001": result_entry("T-001", "V3", "C3", "E-lower", "E-grid", kind="optimality")
        },
        evidence={"E-lower": lower, "E-grid": grid},
        verifiers=REGISTER.verifiers,
    )
    assert check_requests.entry_state("T-001", exact).how == (
        "reproduced here with the author's own checker (zmx2)"
    )


def test_a_confirmation_without_the_relation_says_it_is_not_yet_recorded() -> None:
    bare = Register(
        results={"T-001": result_entry("T-001", "V3", "C3", "E-bare")},
        evidence={"E-bare": {"origin": "replayed-here", "replay_status": "passed"}},
    )
    assert (
        check_requests.entry_state("T-001", bare).how
        == "how it was re-verified is not yet recorded"
    )
    assert "not yet recorded" in check_requests.draft(issue(), bare, "owner/repo")


def test_the_draft_states_each_result_links_main_and_ends_in_the_footer() -> None:
    entry = issue(
        results=[
            {"key": "bound", "claim": "s(9) >= 3", "register": ["T-001"]},
            {"key": "open", "claim": "s(10) >= 3", "register": ["T-005"]},
            {
                "key": "later",
                "claim": "s(11) >= 3",
                "not_registered": "Queued for import.",
                "queued": True,
            },
        ]
    )
    text = check_requests.draft(entry, REGISTER, "owner/repo")
    assert text.endswith(FOOTER)
    assert (
        "T-001, confirmed at V3/C3: reproduced here with the author's own checker (zmx2)."
        in text
    )
    assert "registered as reported" in text
    assert "Under way here since 2026-10-01: a replay" in text
    assert "T-005: T-005's next rung." in text, "bead ids are this project's and are left out"
    assert "https://github.com/owner/repo/blob/main/packing/frontier/RESULTS.md" in text
    assert "stays open" in text
    closing = check_requests.draft(issue(), REGISTER, "owner/repo")
    assert "closed with this comment" in closing


def test_a_recorded_result_is_told_what_was_run_on_it_here_and_not_only_its_rung() -> None:
    """A complete replay can be retained beside a report entry while it waits for review,
    as T-128's, T-130's and T-131's were at `C0`, and the draft told their authors that
    nothing had been read or replayed here. The words follow the evidence: a cited
    replay that passed, or receipts retained with the entry."""
    packet = "packing/resources/web/a-packet"
    register = Register(
        results={
            "T-001": result_entry("T-001", "V0", "C0", "E-report"),
            "T-002": result_entry(
                "T-002",
                "V0",
                "C0",
                "E-report",
                artifacts=[
                    f"{packet}/README.md",
                    f"{packet}/receipts/exact-certification.json.xz",
                    f"{packet}/receipts/custody.json",
                ],
            ),
            "T-003": result_entry("T-003", "V0", "C0", "E-report", "E-passed"),
        },
        evidence={
            **REGISTER.evidence,
            "E-passed": {
                "origin": "external",
                "assurance": "reported",
                "replay_status": "passed",
            },
        },
    )

    def drafted(rid: str) -> str:
        results = [{"key": "a", "claim": "s(9) >= 3", "register": [rid]}]
        return check_requests.draft(issue(results=results), register, "owner/repo")

    untouched = drafted("T-001")
    assert (
        "T-001, registered as reported: nothing has been read or replayed here yet (V0/C0)."
    ) in untouched
    retained = drafted("T-002")
    assert "nothing has been read or replayed" not in retained
    assert (
        f"T-002, registered as reported (V0/C0); receipts of what has been run on it here are "
        f"retained in `{packet}/receipts/`, none of it yet counted toward confirmation."
    ) in retained
    passed = drafted("T-003")
    assert "nothing has been read or replayed" not in passed
    assert (
        "T-003, registered as reported (V0/C0); the replay of E-passed has passed, none of it "
        "yet counted toward confirmation."
    ) in passed


def test_a_claim_that_ends_in_a_full_stop_takes_its_colon_without_it() -> None:
    entry = issue(
        results=[
            {"key": "bound", "claim": "s(9) >= 3.", "register": ["T-001"]},
            {
                "key": "flaw",
                "claim": "A defect in it.",
                "evidence": ["E-defect"],
                "defect": True,
            },
            {
                "key": "later",
                "claim": "s(11) >= 3.",
                "not_registered": "Below the bound.",
                "queued": False,
            },
            {"key": "decimal", "claim": "s(12) > 3.875...", "register": ["T-001"]},
        ]
    )
    text = check_requests.draft(entry, REGISTER, "owner/repo")
    assert not re.search(r"(?<!\.)\.:", text)
    assert "- s(9) >= 3:\n" in text
    assert "- A defect in it: the record holds this defect." in text
    assert "- s(11) >= 3: Below the bound." in text
    assert "- s(12) > 3.875...:\n" in text, "an ellipsis is part of the claim"


def test_an_entry_two_results_map_to_is_queued_once() -> None:
    """Issue 375's two status reports both map to T-129, and its draft queued T-129 twice."""
    entry = issue(
        results=[
            {"key": "a", "claim": "s(10) >= 3", "register": ["T-002"]},
            {"key": "b", "claim": "s(11) >= 3", "register": ["T-002", "T-005"]},
        ]
    )
    text = check_requests.draft(entry, REGISTER, "owner/repo")
    assert text.count("  - T-002, ") == 2, "each result still names the entries it maps to"
    queued = text.split("**What is still queued, and how it will be completed.**")[1]
    assert [line for line in queued.splitlines() if line.startswith("- ")] == [
        "- T-002: T-002's next rung.",
        "- T-005: T-005's next rung.",
    ]


def test_no_live_draft_says_nothing_ran_beside_a_receipt_doubles_a_colon_or_a_queued_line() -> (
    None
):
    live = check_requests.load_record()
    register = check_requests.load_register()
    for entry in live["issues"]:
        text = check_requests.draft(entry, register, str(live["repository"]))
        number = entry["number"]
        assert not re.search(r"(?<!\.)\.:", text), number
        queued = [line for line in text.splitlines() if line.startswith("- T-")]
        assert len(queued) == len(set(queued)), number
        for line in text.splitlines():
            if "nothing has been read or replayed here" in line:
                rid = line.split(",", 1)[0].removeprefix("  - ")
                artifacts = register.results[rid].get("artifacts") or ()
                assert not any("/receipts/" in path for path in artifacts), (number, rid)


def test_the_draft_corrects_what_earlier_replies_said() -> None:
    said = [
        {
            "result": "bound",
            "id": "T-001",
            "as": "T-058",
            "verification": "V4",
            "confirmation": "C4",
        }
    ]
    earlier = reply(1, reported=said, outdated=["a link into a branch; it is on main"])
    text = check_requests.draft(issue(replies=[earlier]), REGISTER, "owner/repo")
    assert "**Corrections to earlier replies.**" in text
    assert "- The reply of 2026-10-02 said a link into a branch; it is on main." in text
    assert "- The reply of 2026-10-02 named this result T-058; it is T-001." in text
    assert "- The reply of 2026-10-02 gave T-001 as V4/C4; it now reads V3/C3." in text


def test_the_draft_refuses_off_main(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    live = check_requests.load_record()
    number = str(live["issues"][0]["number"])
    monkeypatch.setattr(check_requests, "head_on_main", lambda: False)
    assert check_requests.main(["--draft", number]) == 2
    assert "refusing to draft" in capsys.readouterr().err
    monkeypatch.setattr(check_requests, "head_on_main", lambda: True)
    assert check_requests.main(["--draft", number]) == 0
    assert capsys.readouterr().out.rstrip().endswith(FOOTER)
    assert check_requests.main(["--draft", "1"]) == 2


def comment(number: int, login: str, created: str, body: str = "thanks") -> Record:
    return {
        "html_url": URL.format(number),
        "user": {"login": login},
        "created_at": created,
        "body": body,
    }


def test_the_github_comparison_lists_missing_replies_unread_comments_and_unknown_issues() -> (
    None
):
    recorded = record(
        issue(replies=[reply(1, "2026-10-01")], read_through="2026-10-01T12:00:00Z")
    )
    live = {
        "repos/owner/repo/issues?state=all&per_page=100": [
            {"number": 7, "state": "open", "title": "A request"},
            {"number": 8, "state": "open", "title": "Another"},
            {"number": 9, "state": "open", "title": "A pull request", "pull_request": {}},
        ],
        "repos/owner/repo/issues/7/comments?per_page=100": [
            comment(1, "owner", "2026-10-01T10:00:00Z"),
            comment(2, "owner", "2026-10-02T10:00:00Z"),
            comment(3, "agent", "2026-10-02T11:00:00Z", f"text\n\n{FOOTER}\n"),
            comment(4, "someone", "2026-10-02T12:00:00Z", f"the author's own\n\n{FOOTER}"),
            comment(5, "someone", "2026-09-30T12:00:00Z"),
        ],
    }
    differences = check_requests.compare_github(recorded, live.__getitem__)
    assert differences == [
        "#8 is not in the record: Another",
        f"#7: reply missing from the record: {URL.format(2)} (owner, 2026-10-02)",
        f"#7: reply missing from the record: {URL.format(3)} (agent, 2026-10-02)",
        f"#7: unread comment {URL.format(4)} (someone, 2026-10-02T12:00:00Z)",
    ]


def test_the_backlog_lists_every_entry_below_v3_or_c3_with_its_beads_and_issues() -> None:
    lines = check_requests.backlog(
        record(issue(results=[{"key": "a", "claim": "c", "register": ["T-002"]}])), REGISTER
    )
    rows = [line for line in lines if line.startswith("| T-")]
    assert [row.split(" | ")[0] for row in rows] == ["| T-002", "| T-003", "| T-005"]
    assert "think-abcd" in rows[0]
    assert "#7" in rows[0]
    assert "in analysis since 2026-10-01" in rows[2]


def test_the_live_backlog_and_report_render() -> None:
    live = check_requests.load_record()
    register = check_requests.load_register()
    backlog = "\n".join(check_requests.backlog(live, register))
    below = [
        rid
        for rid, entry in register.results.items()
        if int(entry["verification"][1]) < 3 or int(entry["confirmation"][1]) < 3
    ]
    assert all(f"| {rid} |" in backlog for rid in below)
    report = check_requests.report(live, register, None)
    assert report[0] == "# Result Requests"
    assert sum(line.startswith("## #") for line in report) == len(live["issues"])


class _Pages:
    """A listing served page by page, as GitHub serves `?per_page=N&page=K`."""

    def __init__(self, items: list[int], size: int) -> None:
        self.items, self.size, self.asked = items, size, []

    def __call__(self, path: str) -> Any:
        self.asked.append(path)
        page = int(path.rpartition("&page=")[2])
        return self.items[(page - 1) * self.size : page * self.size]


def test_a_listing_is_read_page_by_page_until_a_short_or_empty_page() -> None:
    """A short final page ends the read, and so does the empty page after a full one."""
    short = _Pages(list(range(250)), 100)
    assert check_requests.gh_fetch("repos/a/b/issues?per_page=100", short) == list(range(250))
    assert [path.rpartition("=")[2] for path in short.asked] == ["1", "2", "3"]
    full = _Pages(list(range(200)), 100)
    assert check_requests.gh_fetch("repos/a/b/issues?state=all&per_page=100", full) == list(
        range(200)
    )
    assert full.asked[-1] == "repos/a/b/issues?state=all&per_page=100&page=3"


def test_a_response_that_is_not_a_listing_is_returned_on_the_first_page_and_refused_later() -> (
    None
):
    """An object on page 1 is the answer (an error, or a path that is not a listing);
    an object after it would drop the pages already read, so it is refused."""
    error = {"message": "Not Found"}
    assert check_requests.gh_fetch("repos/a/b/issues?per_page=2", lambda _: error) == error
    pages = iter([[1, 2], {"message": "rate limited"}])
    with pytest.raises(ValueError, match="page 2"):
        check_requests.gh_fetch("repos/a/b/issues?per_page=2", lambda _: next(pages))


@pytest.mark.parametrize("size", ["0", "101", "250"])
def test_a_page_size_github_does_not_serve_is_refused(size: str) -> None:
    """GitHub serves at most 100 a page, so `per_page=250` came back 100 long, read as a
    short page, and stopped after the first; `per_page=0` would never end."""

    def never(_: str) -> Any:
        pytest.fail("a refused page size made a request")

    with pytest.raises(ValueError, match="per_page"):
        check_requests.gh_fetch(f"repos/a/b/issues?per_page={size}", never)
