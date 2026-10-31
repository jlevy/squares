"""The intake sweep: every source read, every item owned by an open bead or reported.

The misses it exists for, all in the week of 2026-09-30: three Kingbird counts held as
pending intake with no bead, an import held until a pull request merged and never
resumed, and two evidence updates a packet named as imports of their own and nobody
took in. These pin each source's reading on fixtures small enough to read, with the
network replaced, and pin that `--offline` makes no network call at all.
"""

from __future__ import annotations

import gzip
import json
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import pytest
import test_check_requests as requests_tests

from devtools import capture_kingbird_catalogue as capture_tool
from devtools import check_requests
from devtools import intake_sweep as sweep
from devtools.check_bead_tree import BODY
from sqpack.yamlio import safe_load

TODAY = date(2026, 10, 5)
HEAD = "a" * 40
PIN = "b" * 40
LATER = "c" * 40


def _beads(*queue: sweep.QueuedBead, **states: str) -> sweep.Beads:
    return sweep.Beads(dict(states), tuple(queue))


def _coverage(**extra: Any) -> dict[str, Any]:
    return {
        "sources": [
            {
                "id": "repo-source",
                "role": "source-repository",
                "url": f"https://github.com/someone/packings/tree/{PIN}",
                "notes": f"Retained at its head; {LATER} is an import of its own.",
            },
            {
                "id": "release",
                "role": "first-party-release",
                "title": "A Release",
                "url": "https://example.org/",
                "reviewed": "2026-08-25",
                "source_date": "2026-07-29",
            },
        ],
        **extra,
    }


def test_a_repository_is_named_without_its_revision_path_or_git_suffix() -> None:
    assert (
        sweep.repository(f"https://github.com/evand/square-packing/tree/{PIN}")
        == "https://github.com/evand/square-packing"
    )
    assert sweep.repository("https://github.com/a/b.git") == "https://github.com/a/b"
    assert (
        sweep.repository("https://gist.github.com/9e5f27e25607c0966c4f91bc1253ce8b.git")
        == "https://gist.github.com/9e5f27e25607c0966c4f91bc1253ce8b"
    )
    assert sweep.repository("https://doi.org/10.5281/zenodo.1") is None


def test_an_issue_or_pull_request_address_is_not_a_watched_repository() -> None:
    """The SQUISH n153 source is an issue comment; reading it as a repository watched
    jlevy/squares itself, with no packet able to pin it."""
    comment = "https://github.com/jlevy/squares/issues/401#issuecomment-6043191866"
    assert sweep.repository(comment) is None
    assert sweep.repository("https://github.com/a/b/pull/7") is None
    assert sweep.repository("https://github.com/a/b/discussions") is None
    assert sweep.repository("https://github.com/a/issues") == "https://github.com/a/issues"


def test_a_pin_is_structured_and_a_commit_named_in_prose_pins_nothing(tmp_path: Path) -> None:
    """A README that names a commit as "an import of its own" must not make it current."""
    packet = tmp_path / "someone-packings-2026-10-01"
    (packet / "acquisition").mkdir(parents=True)
    record = {
        "sources": [
            {
                "source_url": "https://github.com/someone/packings",
                "source_commit": HEAD,
                "subtree_scope": ["certificates/n59"],
            }
        ]
    }
    (packet / "acquisition" / "sources.json.gz").write_bytes(
        gzip.compress(json.dumps(record).encode())
    )
    (packet / "README.md").write_text(
        f"https://github.com/someone/packings at {LATER} is an import of its own.\n",
        encoding="utf-8",
    )
    found = sweep.watched_repositories(
        _coverage(), tmp_path, projects=["https://github.com/Other/Thing"]
    )
    packets = found["https://github.com/someone/packings"].packets
    assert [(p.name, p.pin, p.scope) for p in packets] == [
        ("repo-source", PIN, ("",)),
        ("someone-packings-2026-10-01", HEAD, ("certificates/n59",)),
    ]
    assert found["https://github.com/other/thing"].packets == []
    assert found["https://github.com/other/thing"].url == "https://github.com/Other/Thing"
    assert packets[1].retains("certificates/n59/README.md")
    assert not packets[1].retains("certificates/n590/README.md")


def _acquisition(packets: Path, name: str, commit: str, scope: list[str] | None) -> None:
    """A packet's acquisition record pinning `commit`, retaining `scope` or the whole tree."""
    (packets / name / "acquisition").mkdir(parents=True)
    source: dict[str, Any] = {
        "source_url": "https://github.com/someone/packings",
        "source_commit": commit,
    }
    if scope is not None:
        source["subtree_scope"] = scope
    (packets / name / "acquisition" / "sources.json").write_text(
        json.dumps({"sources": [source]}), encoding="utf-8"
    )


def test_a_register_pin_on_a_commit_a_packet_pins_takes_the_packets_scope(
    tmp_path: Path,
) -> None:
    """The register cited Hosono's 797bdf6 as a whole tree, which retained every path.

    Its two packets at that commit retain twenty paths between them, so the register's
    pin there is dropped for theirs; a register address with a path is a pin of that path.
    """
    _acquisition(tmp_path, "someone-packings-2026-10-01", PIN, ["certificates/n59"])
    coverage = _coverage()
    coverage["sources"].append(
        {
            "id": "scoped-source",
            "role": "source-repository",
            "url": f"https://github.com/someone/packings/tree/{LATER}/certificates/n60/",
        }
    )
    found = sweep.watched_repositories(coverage, tmp_path, projects=[])
    packets = found["https://github.com/someone/packings"].packets
    assert sorted((p.name, p.pin, p.scope) for p in packets) == [
        ("scoped-source", LATER, ("certificates/n60",)),
        ("someone-packings-2026-10-01", PIN, ("certificates/n59",)),
    ]
    assert found["https://github.com/someone/packings"].cited_by == {
        "repo-source",
        "scoped-source",
        "someone-packings-2026-10-01",
    }


def _repositories(
    tmp_path: Path,
    head: str | Exception,
    watch: dict[str, Any] | None = None,
    beads: sweep.Beads | None = None,
    *,
    offline: bool = False,
    unretained: tuple[str, ...] = (),
) -> sweep.Section:
    def heads(_url: str) -> str:
        if isinstance(head, Exception):
            raise head
        return head

    def history(_url: str, _head: str, _packets: Any, _reads: Any) -> sweep.RepoHistory:
        return sweep.RepoHistory(3, "2026-10-03", "2026-10-04", ("new records",), 1, unretained)

    return sweep.repositories_section(
        _coverage(),
        watch or {"repositories": []},
        beads,
        offline=offline,
        heads=heads,
        history=history,
        packets=tmp_path,
        projects=[],
    )


def test_a_head_a_packet_pins_is_current_and_a_moved_head_needs_an_owner(
    tmp_path: Path,
) -> None:
    current = _repositories(tmp_path, PIN)
    assert current.items == []
    assert current.notes == ["1 of 1 heads are a commit a packet pins."]
    moved = _repositories(tmp_path, HEAD)
    (item,) = moved.items
    assert item.state == sweep.NEEDS_OWNER
    assert item.what == (
        "https://github.com/someone/packings: head aaaaaaaaaaaa, 3 commits past every "
        "retained pin, 2026-10-03 to 2026-10-04; newest: new records"
    )


def test_commits_a_pin_contains_but_no_packet_retains_need_an_owner(tmp_path: Path) -> None:
    section = _repositories(tmp_path, PIN, unretained=("c56b9b7 s(59) >= 8: run records",))
    (item,) = section.items
    assert item.state == sweep.NEEDS_OWNER
    assert "1 commit a pin contains changed paths no packet at or after it retains" in item.what
    assert item.what.endswith("c56b9b7 s(59) >= 8: run records")


def test_a_read_head_is_owned_by_its_bead_or_listed_with_nothing_to_import(
    tmp_path: Path,
) -> None:
    read = {"url": "https://github.com/someone/packings", "read_through": HEAD}
    owned_read = {
        **read,
        "read_on": "2026-10-05",
        "note": "s(58) >= 7.935",
        "bead": "think-aaaa",
    }
    section = _repositories(
        tmp_path, HEAD, {"repositories": [owned_read]}, _beads(**{"think-aaaa": "open"})
    )
    assert [(i.state, i.bead) for i in section.items] == [(sweep.OWNED, "think-aaaa")]
    closed = _repositories(
        tmp_path, HEAD, {"repositories": [owned_read]}, _beads(**{"think-aaaa": "closed"})
    )
    assert closed.items[0].state == sweep.NEEDS_OWNER
    nothing = {**read, "read_on": "2026-10-05", "note": "README edits"}
    quiet = _repositories(tmp_path, HEAD, {"repositories": [nothing]})
    assert [(i.state, i.what.endswith("nothing to import")) for i in quiet.items] == [
        (sweep.LISTED, True)
    ]
    later = _repositories(tmp_path, LATER, {"repositories": [nothing]})
    assert "past the last pass's read" in later.items[0].what


def test_an_unreadable_head_and_offline_are_reported_as_not_checked(tmp_path: Path) -> None:
    failed = _repositories(tmp_path, RuntimeError("repository not found"))
    assert failed.items == []
    assert failed.unchecked == [
        "https://github.com/someone/packings: `git ls-remote` failed: repository not found"
    ]
    offline = _repositories(tmp_path, HEAD, offline=True)
    assert offline.unchecked == ["1 repository heads: skipped by --offline"]
    stray = {"url": "https://github.com/nobody/cites-this", "read_through": HEAD}
    section = _repositories(tmp_path, PIN, {"repositories": [stray]})
    assert "which no record cites" in section.unchecked[0]


def _commit(repo: Path, path: str, text: str) -> str:
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    environment = {
        "GIT_AUTHOR_NAME": "t",
        "GIT_AUTHOR_EMAIL": "t@example.org",
        "GIT_COMMITTER_NAME": "t",
        "GIT_COMMITTER_EMAIL": "t@example.org",
        "GIT_AUTHOR_DATE": "2026-10-04T00:00:00Z",
        "GIT_COMMITTER_DATE": "2026-10-04T00:00:00Z",
        "GIT_CONFIG_NOSYSTEM": "1",
        "HOME": str(repo.parent),
        "PATH": "/usr/bin:/bin",
    }
    for arguments in (("add", "-A"), ("commit", "-q", "--no-verify", "-m", f"change {path}")):
        subprocess.run(("git", "-C", str(repo), *arguments), check=True, env=environment)
    return subprocess.run(
        ("git", "-C", str(repo), "rev-parse", "HEAD"),
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def test_the_history_reads_commits_past_the_pins_and_changes_no_packet_retains(
    tmp_path: Path,
) -> None:
    """A real repository, read through `file://`: the network step with no network.

    `first` is the oldest pin, which retains everything; `second` changes a path the
    later packet does not retain, so only a read can cover it; `head` is past both.
    """
    repo, (first, second, pinned, head) = _upstream(tmp_path)
    packets = [
        sweep.Packet("whole", first),
        sweep.Packet("scoped", pinned, ("certificates/a",)),
    ]
    found = sweep.read_history(f"file://{repo}", head, packets, ())
    assert (found.count, found.first, found.pins_in_history) == (1, "2026-10-04", 2)
    assert found.unretained == (f"{second[:7]} change certificates/b/cert.txt",)
    read = sweep.read_history(f"file://{repo}", head, packets, (second,))
    assert read.unretained == ()
    # No packet pins this head, so no note reads what its read holds, and none is computed.
    unpinned = sweep.read_history(f"file://{repo}", head, packets, (head,))
    assert (unpinned.unretained, unpinned.held_by_head_read) == ((), ())


def _upstream(tmp_path: Path) -> tuple[Path, tuple[str, str, str, str]]:
    """Four commits: `a`, then `b`, then `a` again, then the README."""
    repo = tmp_path / "upstream"
    subprocess.run(("git", "init", "-q", str(repo)), check=True)
    subprocess.run(
        ("git", "-C", str(repo), "config", "uploadpack.allowFilter", "true"), check=True
    )
    return repo, (
        _commit(repo, "certificates/a/cert.txt", "1"),
        _commit(repo, "certificates/b/cert.txt", "2"),
        _commit(repo, "certificates/a/cert.txt", "3"),
        _commit(repo, "README.md", "4"),
    )


def test_a_register_pin_beside_a_scoped_packet_does_not_hide_what_the_packet_left_out(
    tmp_path: Path,
) -> None:
    """The review's reproduction, in small: Hosono's register pinned the head as a whole
    tree, so 1ebd484 and c56b9b7 were reported only with the register's pins removed."""
    repo, (first, second, pinned, head) = _upstream(tmp_path)
    packets = tmp_path / "web"
    _acquisition(packets, "early", first, None)
    _acquisition(packets, "scoped", pinned, ["certificates/a"])
    register = {
        "sources": [
            {"id": "register", "url": f"https://github.com/someone/packings/tree/{pinned}"}
        ]
    }
    watched = sweep.watched_repositories(register, packets, projects=[])
    entry = watched["https://github.com/someone/packings"]
    found = sweep.read_history(f"file://{repo}", head, entry.packets, ())
    assert found.unretained == (f"{second[:7]} change certificates/b/cert.txt",)


@pytest.mark.parametrize("scope", [["certificates/a", "README.md"], None])
def test_a_read_through_a_pinned_head_goes_only_when_nothing_it_covers_is_left_unretained(
    tmp_path: Path, scope: list[str] | None
) -> None:
    """think-bspk, franciscouzo's case in small. couzo-issue678-2026-10-18 pins 7b6c87e,
    the head, but retains 90 of its 543 changed paths, so the read through it is what
    covers the rest and removing it as the sweep advised left 7b6c87e unretained. A
    packet at the head that omits one changed path keeps the read; one that retains the
    whole tree frees it. With no history read, nothing says either way."""
    repo, (first, second, _pinned, head) = _upstream(tmp_path)
    packets = tmp_path / "web"
    _acquisition(packets, "early", first, None)
    _acquisition(packets, "at-head", head, scope)
    url = "https://github.com/someone/packings"
    read = {"url": url, "read_through": head, "read_on": "2026-10-05", "note": "no change"}

    def section(history: sweep.History) -> sweep.Section:
        return sweep.repositories_section(
            {"sources": []},
            {"repositories": [read]},
            None,
            offline=False,
            heads=lambda _url: head,
            history=history,
            packets=packets,
            projects=[],
        )

    def local(_url: str, at: str, pinned: Any, reads: Any) -> sweep.RepoHistory:
        return sweep.read_history(f"file://{repo}", at, pinned, reads)

    found = section(local)
    assert found.items == []
    (note,) = found.notes[1:]
    if scope is None:
        assert note == (
            f"{url}: a packet now pins {head[:12]}, so intake-watch.yaml's read of it can "
            "be removed."
        )
    else:
        assert note == (
            f"{url}: a packet pins {head[:12]}, but intake-watch.yaml's read of it stays: "
            f"1 commit it covers changes paths no packet retains: {second[:7]} change "
            "certificates/b/cert.txt"
        )

    def unreadable(_url: str, _at: str, _pinned: Any, _reads: Any) -> sweep.RepoHistory:
        raise RuntimeError("no history")

    failed = section(unreadable)
    assert failed.notes == ["1 of 1 heads are a commit a packet pins."]
    assert failed.unchecked == [f"{url}: its history could not be read: no history"]


def test_github_differences_each_need_an_owner_and_a_failure_is_not_checked() -> None:
    record = {"repository": "jlevy/squares"}
    differences = ["#350 is not in the record: New result", "#282: unread comment URL (x, t)"]
    section = sweep.github_section(record, offline=False, compare_github=lambda _: differences)
    assert [i.state for i in section.items] == [sweep.NEEDS_OWNER] * 2
    assert "triage: pending" in section.items[0].step
    assert "read_through" in section.items[1].step

    def refused(_: object) -> list[str]:
        raise OSError("gh: not found")

    failed = sweep.github_section(record, offline=False, compare_github=refused)
    assert failed.unchecked == ["GitHub issues: `gh api` failed: gh: not found"]
    skipped = sweep.github_section(record, offline=True, compare_github=refused)
    assert skipped.unchecked == ["GitHub issues: skipped by --offline"]


def test_a_report_without_the_intake_label_needs_action_and_names_the_command() -> None:
    """The pass adds the label under the `github-workflows` grant, so the step is the
    command, and without the grant the issue is listed for the owner. A new issue's step
    gives the label by stage 0's criterion. A comment edited after `read_through` on the
    same issue keeps its own step: read it."""
    record = {"repository": "jlevy/squares"}
    differences = [
        "#529 reports an item for intake without the `intake` label",
        "#529: unread comment URL (x, 2026-10-01T00:00:00Z, edited 2026-10-02T00:00:00Z)",
        "#530 is not in the record: New result",
    ]
    section = sweep.github_section(record, offline=False, compare_github=lambda _: differences)
    assert [i.state for i in section.items] == [sweep.NEEDS_OWNER] * 3
    assert section.items[0].step == (
        "add the label under the github-workflows grant "
        "(gh issue edit 529 --add-label intake); "
        "without the grant, list the issue for the owner"
    )
    assert section.items[1].step.startswith("read it:")
    assert section.items[2].step.endswith(
        "if it reports a new item for intake (a result, a counterexample or a method), "
        "give it the `intake` label, and mark an entry of another kind intake: true"
    )
    assert sweep.needing_action([section]) == section.items


def test_each_kind_of_difference_the_comparison_reports_gets_its_own_step() -> None:
    """The sweep chooses a step by matching `check_requests`'s wording, and a difference
    that matches nothing falls through to "reconcile". These are the comparison's own
    differences on a small fixture, one of each kind, so a message reworded in
    `check_requests` and in its tests fails here instead of reaching a pass with the
    wrong step."""
    issue, reply, comment = requests_tests.issue, requests_tests.reply, requests_tests.comment
    recorded = requests_tests.record(
        issue(
            replies=[reply(1, "2026-10-01"), reply(9, "2026-10-01")],
            read_through="2026-10-01T12:00:00Z",
        ),
        issue(number=8, kind="other", intake=True, state="closed", closed="2026-10-03"),
        issue(number=6),
    )
    live: dict[str, Any] = {
        "repos/owner/repo/issues?state=all&per_page=100": [
            {"number": 7, "state": "open", "title": "A request", "labels": []},
            {"number": 8, "state": "open", "title": "A method", "labels": []},
            {"number": 20, "state": "open", "title": "New", "labels": [requests_tests.INTAKE]},
        ],
        "repos/owner/repo/issues/7/comments?per_page=100": [
            comment(1, "owner", "2026-10-01T10:00:00Z"),
            comment(2, "owner", "2026-10-02T10:00:00Z"),
            comment(4, "someone", "2026-10-02T12:00:00Z"),
            comment(5, "someone", "2026-09-30T12:00:00Z", updated="2026-10-02T09:00:00Z"),
        ],
        "repos/owner/repo/issues/8/comments?per_page=100": [],
    }
    section = sweep.github_section(
        recorded,
        offline=False,
        compare_github=lambda r: check_requests.compare_github(r, live.__getitem__),
    )
    reconcile = "reconcile result-requests.yaml with the issue"
    label = "add the label under the github-workflows grant (gh issue edit {} --add-label"
    expected = [
        ("#20", "enter it in result-requests.yaml with triage: pending"),
        ("#7", label.format(7)),
        ("#7:", "record the reply under the issue's replies"),
        ("#7:", "read it: map any result it reports"),
        ("#7:", "read it: map any result it reports"),
        ("#7:", reconcile),
        ("#8", reconcile),
        ("#8", label.format(8)),
        ("#6", reconcile),
    ]
    assert [item.what.split(" ", 1)[0] for item in section.items] == [n for n, _ in expected]
    for item, (_, step) in zip(section.items, expected, strict=True):
        assert item.step.startswith(step), (item.what, item.step)
        assert item.state == sweep.NEEDS_OWNER
    assert [item.what for item in section.items if item.step == reconcile] == [
        f"#7: recorded reply not on the issue: {requests_tests.URL.format(9)}",
        "#8 is open there and closed here",
        "#6 is in the record and not on owner/repo",
    ]


def test_a_blocker_is_read_only_from_a_sentence_that_says_something_waits() -> None:
    text = (
        "Certificates posted on jlevy/squares#282 from 3 October. Stage 3 (new T-NNN) "
        "waits for jlevy/squares#305. Replays held with think-wpuu; see #290.\n"
        "Taken over after #312 merges. Owned by think-e6ss."
    )
    assert sweep.stated_blockers(text, "jlevy/squares", own="think-e6ss") == [
        "jlevy/squares#305",
        "think-wpuu",
        "jlevy/squares#312",
    ]


def test_a_sentence_that_says_what_a_wait_was_names_no_blocker() -> None:
    """think-e6ss was reported from its own account of a wait that had ended."""
    text = (
        "Stage 3 (new T-NNN) was held for jlevy/squares#305, which merged 2026-10-04; it "
        "is done as T-090 on PR 353. Replays (~124 CPU-h for 14) held with think-wpuu. "
        "The packet waited on #290 until it merged. Stage 2 has been blocked on #291."
    )
    assert sweep.stated_blockers(text, "jlevy/squares", own="think-e6ss") == [
        "think-wpuu",
        "jlevy/squares#291",
    ]


def test_a_beads_notes_are_history_and_only_a_blocked_on_line_there_declares_a_wait() -> None:
    """think-o430's notes recorded the sweep's own example, "think-e6ss/#305", and the
    sweep read it as that bead waiting on think-e6ss."""
    body = (
        "Combine every intake source into one report.\n\n## Notes\n\n"
        "2026-10-05: adds Blocked imports (a bead whose stated blocker merged/closed: "
        "think-e6ss/#305), held until review.\n"
    )
    bead = {"id": "is-01aaaa", "status": "in_progress", "title": "Sweep", BODY: body}
    queued = sweep.queued_bead(bead, "think-o430")
    assert queued.text == "Sweep\nCombine every intake source into one report.\n\n"
    assert "think-e6ss/#305" in queued.notes
    beads = _beads(queued, **{"think-e6ss": "closed"})
    quiet = sweep.blocked_section(beads, _blockers(beads), "jlevy/squares")
    assert quiet.items == []

    declared = sweep.queued_bead(
        {**bead, BODY: body + "\nblocked_on: jlevy/squares#305, think-e6ss\n"}, "think-o430"
    )
    beads = _beads(declared, **{"think-e6ss": "closed"})
    (item,) = sweep.blocked_section(beads, _blockers(beads), "jlevy/squares").items
    assert item.what.endswith(
        "waits on jlevy/squares#305, merged 2026-10-04; think-e6ss, closed"
    )

    waiting = "Stage 3 waits for jlevy/squares#305.\n\n## Notes\n\n"
    ended = sweep.queued_bead(
        {**bead, BODY: waiting + "blocked_on: #400\n\nlater:\nblocked_on: none\n"}, "think-o430"
    )
    assert sweep.declared_blockers(ended, "jlevy/squares") == []
    moved = sweep.queued_bead({**bead, BODY: waiting + "blocked_on: #400\n"}, "think-o430")
    assert sweep.declared_blockers(moved, "jlevy/squares") == ["jlevy/squares#400"]
    prose = sweep.queued_bead({**bead, BODY: waiting}, "think-o430")
    assert sweep.declared_blockers(prose, "jlevy/squares") is None
    beads = _beads(prose)
    (item,) = sweep.blocked_section(beads, _blockers(beads), "jlevy/squares").items
    assert item.what.endswith("waits on jlevy/squares#305, merged 2026-10-04")


ISSUES = {
    "repos/jlevy/squares/issues/305": {
        "state": "closed",
        "closed_at": "2026-10-04T23:00:00Z",
        "pull_request": {"merged_at": "2026-10-04T23:00:00Z"},
    },
    "repos/jlevy/squares/issues/400": {"state": "open"},
}


def _blockers(beads: sweep.Beads | None) -> sweep.Blockers:
    return sweep.Blockers(beads, ISSUES.__getitem__)


def test_an_import_bead_whose_stated_blocker_merged_is_reported() -> None:
    """think-e6ss held stage 3 until #305 merged; #305 merged and nothing resumed it."""
    stalled = sweep.QueuedBead(
        "think-e6ss", "in_progress", "Import wand125", "Stage 3 waits for jlevy/squares#305."
    )
    waiting = sweep.QueuedBead("think-aaaa", "open", "Import x", "Held until #400 merges.")
    children = sweep.QueuedBead(
        "think-bbbb", "open", "Epic", "", blocked_by=("think-cccc", "think-dddd")
    )
    beads = _beads(
        stalled, waiting, children, **{"think-cccc": "closed", "think-dddd": "in_progress"}
    )
    section = sweep.blocked_section(beads, _blockers(beads), "jlevy/squares")
    (item,) = section.items
    assert item.state == sweep.RESOLVED
    assert (
        item.what == "think-e6ss (Import wand125) waits on jlevy/squares#305, merged 2026-10-04"
    )
    assert section.notes == [
        "3 open `result-import` beads name a blocker; 1 of them name one that has resolved."
    ]
    done = _beads(children, **{"think-cccc": "closed", "think-dddd": "closed"})
    (last,) = sweep.blocked_section(done, _blockers(done), "jlevy/squares").items
    assert last.what.endswith("think-cccc, closed; think-dddd, closed")


def test_offline_blockers_on_github_are_not_checked() -> None:
    queued = sweep.QueuedBead("think-e6ss", "open", "Import", "Waits for jlevy/squares#305.")
    beads = _beads(queued)
    section = sweep.blocked_section(beads, sweep.Blockers(beads, None), "jlevy/squares")
    assert section.items == []
    assert section.unchecked == [
        "blockers not read: jlevy/squares#305 (offline, or `gh` failed)"
    ]


#: A count the retained transcription prints once, and a later capture moves below it.
SIDE, LOWER = r"\Nn{5.93383346267692}", r"\Nn{5.93383000000000}"
CASES = {
    29: {"reported_upper_bound": {"value": "5.93383346267692", "source_key": "[Kingbird]"}}
}


def _captured() -> str:
    """A capture date the sweep reads as newer than the record's, whatever the record says.

    The fixture reads the live register, whose Kingbird `reviewed` date moves each time a
    capture is taken in; a capture named for a fixed day stops being newer the day the
    record reaches it, as it did on 2026-10-05.
    """
    live = safe_load(sweep.COVERAGE.read_text(encoding="utf-8"))
    source = next(s for s in live["sources"] if s["id"] == sweep.KINGBIRD)
    return (date.fromisoformat(str(source["reviewed"])) + timedelta(days=1)).isoformat()


def _kingbird(tmp_path: Path, text: str, **coverage: Any) -> sweep.Section:
    capture = tmp_path / f"kingbird-{_captured()}"
    capture.mkdir()
    (capture / f"{capture_tool.STEM}.md").write_text(text, encoding="utf-8")
    live = safe_load(sweep.COVERAGE.read_text(encoding="utf-8"))
    live["pending_catalogue_intake"] = coverage.get("pending", [])
    return sweep.kingbird_section(
        live,
        coverage.get("beads"),
        TODAY,
        capture=sweep.newest_capture(tmp_path),
        cases=CASES,
    )


def _retained() -> str:
    live = safe_load(sweep.COVERAGE.read_text(encoding="utf-8"))
    source = next(s for s in live["sources"] if s["id"] == sweep.KINGBIRD)
    return (sweep.ROOT / source["local"]).with_suffix(".md").read_text(encoding="utf-8")


def test_a_count_a_newer_capture_moves_below_its_record_is_an_intake(tmp_path: Path) -> None:
    text = _retained()
    assert text.count(SIDE) == 1
    section = _kingbird(tmp_path, text.replace(SIDE, LOWER))
    (item,) = section.items
    assert item.state == sweep.NEEDS_OWNER
    assert item.what.startswith(f"n = 29: the capture of {_captured()} prints 5.93383000000000")


def test_a_count_declared_pending_with_its_bead_is_owned(tmp_path: Path) -> None:
    pending = [
        {"n": 29, "catalogue_value": "5.93383", "bead": "think-aaaa", "recorded": "2026-10-05"}
    ]
    section = _kingbird(
        tmp_path,
        _retained().replace(SIDE, LOWER),
        pending=pending,
        beads=_beads(**{"think-aaaa": "open"}),
    )
    assert [(i.state, i.bead) for i in section.items] == [(sweep.OWNED, "think-aaaa")]


def test_an_unchanged_capture_is_clean_and_no_newer_capture_is_not_checked(
    tmp_path: Path,
) -> None:
    same = _kingbird(tmp_path, _retained())
    assert same.items == []
    assert "0 counts read differently" in same.notes[0]
    live = safe_load(sweep.COVERAGE.read_text(encoding="utf-8"))
    none = sweep.kingbird_section(live, None, TODAY, capture=None, cases=CASES)
    assert none.unchecked[0].startswith(
        "Kingbird catalogue: no capture newer than the record's"
    )


def test_catalogues_no_command_reads_are_listed_with_their_age() -> None:
    (line,) = sweep.catalogues_section(_coverage(), TODAY).unchecked
    assert line == (
        "A Release (https://example.org/): read by hand; last reviewed 2026-08-25 "
        "(41 days ago), source dated 2026-07-29"
    )


def _issue(**extra: Any) -> dict[str, Any]:
    return {
        "number": 300,
        "state": "open",
        "triage": "done",
        "opened": "2026-10-01",
        "answer_bead": "think-bbbb",
        "results": [
            {"key": "later", "claim": "a bound", "not_registered": "not yet", "queued": True}
        ],
        "asks": [{"what": "a correction", "state": "queued", "bead": "think-aaaa"}],
        "replies": [],
        **extra,
    }


def _queues(issues: list[dict[str, Any]], beads: sweep.Beads, **coverage: Any) -> sweep.Section:
    register = check_requests.Register(results={}, evidence={})
    return sweep.queues_section(
        _coverage(**coverage),
        {"repository": "jlevy/squares", "issues": issues},
        register,
        beads,
        today=TODAY,
        blockers=_blockers(beads),
    )


def test_a_queued_result_or_ask_needs_its_own_bead_beside_the_answer_bead() -> None:
    """#282's queued result named no bead, and the answer bead owns only the reply."""
    beads = _beads(**{"think-aaaa": "in_progress", "think-bbbb": "open"})
    result, ask, reply = _queues([_issue()], beads).items
    assert (result.what, result.state) == ("#300 queued result later", sweep.NEEDS_OWNER)
    assert (ask.state, ask.bead) == (sweep.OWNED, "think-aaaa")
    assert (reply.what, reply.state, reply.bead) == (
        "#300 owes a reply",
        sweep.OWNED,
        "think-bbbb",
    )


def test_a_queued_item_whose_blocker_merged_is_reported() -> None:
    beads = _beads(**{"think-aaaa": "open", "think-bbbb": "open"})
    held = {
        "key": "later",
        "claim": "a bound",
        "not_registered": "Stage 3 waits for jlevy/squares#305.",
        "queued": True,
        "bead": "think-aaaa",
    }
    result = _queues([_issue(results=[held])], beads).items[0]
    assert result.state == sweep.RESOLVED
    assert result.what.endswith("it waits on jlevy/squares#305, merged 2026-10-04")
    structured = {**held, "not_registered": "not yet", "blocked_on": ["jlevy/squares#400"]}
    still = _queues([_issue(results=[structured])], beads).items[0]
    assert still.state == sweep.OWNED


def test_a_queued_item_waits_until_every_blocker_it_declares_has_resolved() -> None:
    """The schema's `blocked_on`: "the wait is over once every one has" -- not any one."""
    beads = _beads(**{"think-aaaa": "open", "think-bbbb": "open", "think-cccc": "closed"})
    held = {
        "key": "later",
        "claim": "a bound",
        "not_registered": "not yet",
        "queued": True,
        "bead": "think-aaaa",
        "blocked_on": ["jlevy/squares#305", "jlevy/squares#400"],
    }
    one_open = _queues([_issue(results=[held])], beads).items[0]
    assert (one_open.what, one_open.state) == ("#300 queued result later", sweep.OWNED)
    done = {**held, "blocked_on": ["jlevy/squares#305", "think-cccc"]}
    resolved = _queues([_issue(results=[done])], beads).items[0]
    assert resolved.state == sweep.RESOLVED
    assert resolved.what.endswith(
        "it waits on jlevy/squares#305, merged 2026-10-04; think-cccc, closed"
    )


def test_a_pending_intake_is_owned_while_its_bead_is_open() -> None:
    entry = {
        "n": 69,
        "catalogue_value": "8.82",
        "record_value": "8.83",
        "bead": "think-aaaa",
        "recorded": "2026-09-30",
    }
    beads = _beads(**{"think-aaaa": "in_progress"})
    (intake,) = _queues([], beads, pending_catalogue_intake=[entry]).items
    assert (intake.state, intake.since) == (sweep.OWNED, "2026-09-30 (5 days ago)")
    orphan = {key: value for key, value in entry.items() if key != "bead"}
    (bare,) = _queues([], beads, pending_catalogue_intake=[orphan]).items
    assert bare.state == sweep.NEEDS_OWNER


# -- A bead gone quiet owns nothing ----------------------------------------------------
# Section E of the intake review of 26 October 2026: `owned` read any open bead as an
# owner, so think-mbdw, claimed by a session gone since 16 October, held seven owed
# counts out of every report for eight days.


def _quiet(status: str, updated: str, delegate: str = "") -> sweep.Beads:
    return sweep.Beads(
        {"think-aaaa": status},
        (),
        {"think-aaaa": f"{updated}T09:00:00.000Z"},
        {"think-aaaa": delegate},
        date(2026, 10, 26),
    )


@pytest.mark.parametrize(
    ("status", "updated", "delegate", "state", "bead_state"),
    [
        ("open", "2026-10-20", "", sweep.OWNED, "open"),
        (
            "open",
            "2026-10-19",
            "",
            sweep.STALLED,
            "open; no update since 2026-10-19 (7 days)",
        ),
        (
            "blocked",
            "2026-10-12",
            "",
            sweep.STALLED,
            "blocked; no update since 2026-10-12 (14 days)",
        ),
        ("in_progress", "2026-10-25", "w-lane-1025", sweep.OWNED, "in_progress"),
        (
            "in_progress",
            "2026-10-24",
            "w-lane-1024",
            sweep.STALLED,
            (
                "in_progress; claimed by w-lane-1024, whose session is gone: no update since "
                "2026-10-24 (2 days)"
            ),
        ),
        # A claim with no delegate names no session, and an open bead claims nothing.
        ("in_progress", "2026-10-24", "", sweep.OWNED, "in_progress"),
        ("open", "2026-10-22", "w-lane-1022", sweep.OWNED, "open"),
        ("closed", "2026-10-25", "", sweep.NEEDS_OWNER, "closed"),
    ],
)
def test_a_bead_gone_quiet_owns_nothing(
    status: str, updated: str, delegate: str, state: str, bead_state: str
) -> None:
    item = sweep.owned("an item", "think-aaaa", _quiet(status, updated, delegate))
    assert (item.state, item.bead, item.bead_state) == (state, "think-aaaa", bead_state)
    assert (item.state in sweep.ACTION) is (state != sweep.OWNED)


def test_without_the_sweep_day_or_an_update_no_bead_is_quiet() -> None:
    """A store read without the sweep's day, as the tests' `_beads` builds one, or a bead
    with no `updated_at`, judges no staleness: the bead's state alone decides."""
    assert sweep.owned("x", "think-aaaa", _beads(**{"think-aaaa": "open"})).state == sweep.OWNED
    bare = sweep.Beads({"think-aaaa": "open"}, (), {}, {}, date(2026, 10, 26))
    assert sweep.owned("x", "think-aaaa", bare).state == sweep.OWNED


def test_the_store_carries_each_bead_update_and_delegate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from devtools import check_bead_tree  # noqa: PLC0415

    found = [
        {
            "id": "is-01aaaa",
            "status": "in_progress",
            "title": "a claim",
            "updated_at": "2026-10-16T08:00:00.000Z",
            "delegate": "c-lane-1016",
        },
        {"id": "is-01bbbb", "status": "open", "title": "a bead", "updated_at": None},
    ]
    aliases = {"aaaa": "01aaaa", "bbbb": "01bbbb"}
    monkeypatch.setattr(check_bead_tree, "load", lambda: (found, "", aliases))
    beads = sweep.Beads.load(date(2026, 10, 26))
    assert beads is not None
    assert beads.updated == {"think-aaaa": "2026-10-16T08:00:00.000Z", "think-bbbb": ""}
    assert beads.delegates == {"think-aaaa": "c-lane-1016", "think-bbbb": ""}
    assert beads.stalled("think-aaaa") == "no update since 2026-10-16 (10 days)"
    assert beads.stalled("think-bbbb") == ""


def test_offline_reads_no_network_and_reports_what_it_skipped() -> None:
    def network(*_: object) -> Any:
        pytest.fail("--offline made a network call")

    sections = sweep.sweep(
        today=TODAY,
        offline=True,
        capture=None,
        beads=None,
        compare_github=network,
        heads=network,
        history=network,
        fetch=network,
    )
    unchecked = [line for section in sections for line in section.unchecked]
    assert "GitHub issues: skipped by --offline" in unchecked
    assert any(line.endswith("repository heads: skipped by --offline") for line in unchecked)
    report = sweep.markdown(sections, TODAY)
    assert report.startswith("# Intake Sweep, 2026-10-05\n")
    assert "## Not Checked" in report


def test_the_report_leads_with_what_needs_action() -> None:
    sections = [
        sweep.Section(
            "Source",
            items=[
                sweep.Item("orphan", sweep.NEEDS_OWNER, step="open a bead"),
                sweep.Item("stalled", sweep.RESOLVED, step="resume it"),
                sweep.Item("settled", sweep.CLOSEABLE, step="close it"),
                sweep.Item("held", sweep.OWNED, bead="think-aaaa", bead_state="open"),
                sweep.Item("quiet", sweep.STALLED, bead="think-bbbb", bead_state="open"),
                sweep.Item("n = 1 pending on main", sweep.OWED_ON_MAIN, bead="think-cccc"),
            ],
            unchecked=["a source: skipped"],
        )
    ]
    report = sweep.markdown(sections, TODAY)
    assert (
        "1 item without an open bead to own it, 1 item whose bead has gone quiet, "
        "1 regularization owed on main, 1 item whose blocker has resolved, "
        "1 closeable issue still open, 1 item owned by an open bead, and 1 source not "
        "checked." in report
    )
    assert report.index("## Needs Action") < report.index("## Not Checked")
    assert report.index("## Not Checked") < report.index("## Source")
    assert "| Source | orphan | needs an owner |  | open a bead |" in report
    assert "| Source | settled | closeable, still open |  | close it |" in report
    assert "| held | owned | think-aaaa (open) |  |" in report
    assert "| Source | quiet | owned by a stalled bead |  |  |" in report
    items = sections[0].items
    assert sweep.needing_action(sections) == [*items[:3], *items[4:]]


def _settled(**extra: Any) -> dict[str, Any]:
    """An open issue with every result settled and nothing queued: closeable."""
    return _issue(
        results=[
            {"key": "beyond", "claim": "a bound", "not_registered": "a row", "queued": False}
        ],
        asks=[],
        replies=[
            {
                "url": "https://github.com/jlevy/squares/issues/300#issuecomment-1",
                "date": "2026-10-03",
                "kind": "import",
                "reported": [{"result": "beyond"}],
            }
        ],
        **extra,
    )


def test_every_closeable_issue_still_open_needs_action() -> None:
    """The owner's instruction of 23 October 2026: twelve closeable issues were open and
    nothing listed them, so a settled issue's close is owed until it is done."""
    beads = _beads(**{"think-bbbb": "in_progress"})
    (item,) = _queues([_settled()], beads).items
    assert (item.what, item.state, item.bead, item.since) == (
        "#300 is closeable and still open",
        sweep.CLOSEABLE,
        "think-bbbb",
        "2026-10-03",
    )
    assert "check_requests --draft N" in item.step
    assert sweep.needing_action([sweep.Section("queues", items=[item])]) == [item]
    assert _queues([_settled(state="closed")], beads).items == []


def test_a_question_awaiting_the_author_holds_the_issue_open_and_the_answer_bead_owns_it() -> (
    None
):
    asked = {
        "question": "Was the seed T-186's packing?",
        "changes": "lineage",
        "asked": "https://github.com/jlevy/squares/issues/300#issuecomment-1",
        "state": "awaiting",
    }
    beads = _beads(**{"think-bbbb": "in_progress"})
    (item,) = _queues([_settled(awaiting_author=[asked])], beads).items
    assert (item.what, item.state, item.bead, item.since) == (
        "#300 awaits the author (lineage): Was the seed T-186's packing?",
        sweep.OWNED,
        "think-bbbb",
        "2026-10-03",
    )
    orphaned = _queues([_settled(awaiting_author=[asked])], _beads(**{"think-bbbb": "closed"}))
    assert [i.state for i in orphaned.items] == [sweep.NEEDS_OWNER]
    withdrawn = {**asked, "state": "withdrawn", "note": "The manifest settles it."}
    (close,) = _queues([_settled(awaiting_author=[withdrawn])], beads).items
    assert close.state == sweep.CLOSEABLE


HOLD = {
    "by": "owner",
    "basis": "recorded-reservation",
    "since": "2026-10-04",
    "beads": ["think-cccc"],
    "note": "Reserved for the owner (think-cccc).",
}


def test_an_issue_held_for_the_owner_is_listed_for_the_owner_and_never_as_a_close() -> None:
    """Review A1 of #747: the owner reserved #570, and the sweep told every pass to post
    on it and close it. Held, it is listed for the owner and fails nothing."""
    beads = _beads(**{"think-bbbb": "in_progress"})
    (item,) = _queues([_settled(held=HOLD)], beads).items
    assert (item.what, item.state, item.bead, item.since) == (
        (
            "#300 is held for the owner since 2026-10-04, pending the owner's confirmation "
            "(its close otherwise owed): listed for the owner, nothing posted or closed"
        ),
        sweep.LISTED,
        "think-bbbb",
        "2026-10-04",
    )
    assert item.step == "for the owner: Reserved for the owner (think-cccc)."
    assert sweep.needing_action([sweep.Section("queues", items=[item])]) == []
    unanswered = {**_settled(held=HOLD), "replies": []}
    (owed,) = _queues([unanswered], beads).items
    assert "confirmation (a reply and its close otherwise owed)" in owed.what
    _result, queued_ask, held = _queues([_issue(held=HOLD)], beads).items
    assert queued_ask.what == "#300 queued ask: a correction"
    assert "confirmation (a reply otherwise owed)" in held.what


def test_a_close_github_already_shows_is_recorded_not_posted_again() -> None:
    """Review A5 of #747: until the change recording a close merged, the sweep still
    asked for the final comment, and a check-in could post it twice."""
    beads = _beads(**{"think-bbbb": "in_progress"})
    (open_there,) = _queues([_settled()], beads).items
    assert "if the issue is still open there, post the final comment" in open_there.step
    register = check_requests.Register(results={}, evidence={})
    (closed,) = sweep.queues_section(
        _coverage(),
        {"repository": "jlevy/squares", "issues": [_settled()]},
        register,
        beads,
        today=TODAY,
        blockers=_blockers(beads),
        closed_there=frozenset({300}),
    ).items
    assert (closed.what, closed.state) == (
        "#300 is closed on GitHub and open in the record",
        sweep.CLOSEABLE,
    )
    assert closed.step.startswith("post nothing: record the final comment")
    github = sweep.github_section(
        {"repository": "jlevy/squares"},
        offline=False,
        compare_github=lambda _: ["#300 is closed there and open here", "#301 is open there"],
    )
    assert sweep.closed_on_github(github) == frozenset({300})
    assert github.items[0].step.startswith("record the close")


def test_a_question_awaited_past_the_bound_is_listed_for_a_decision() -> None:
    """Review A9 of #747: an awaited question had no age, so #470's waited eleven days
    listed as owned. Past `AWAITED_DAYS` it is listed for a decision; it fails nothing."""
    asked = {
        "question": "Which packing did 180 start from?",
        "changes": "lineage",
        "asked": "https://github.com/jlevy/squares/issues/300#issuecomment-1",
        "state": "awaiting",
    }
    beads = _beads(**{"think-bbbb": "in_progress"})
    entry = _settled(awaiting_author=[asked])
    later = TODAY + timedelta(days=sweep.AWAITED_DAYS + 3)

    def queues(today: date, store: sweep.Beads) -> list[sweep.Item]:
        return sweep.queues_section(
            _coverage(),
            {"repository": "jlevy/squares", "issues": [entry]},
            check_requests.Register(results={}, evidence={}),
            store,
            today=today,
            blockers=_blockers(store),
        ).items

    (fresh,) = queues(TODAY, beads)
    assert fresh.state == sweep.OWNED
    (stale,) = queues(later, beads)
    assert (stale.what, stale.state, stale.bead) == (
        "#300 awaits the author (lineage): Which packing did 180 start from? (awaited 19 days)",
        sweep.STALE,
        "think-bbbb",
    )
    assert stale.step.startswith("decide: chase the author, withdraw the question")
    assert sweep.needing_action([sweep.Section("queues", items=[stale])]) == []
    (orphan,) = queues(later, _beads(**{"think-bbbb": "closed"}))
    assert orphan.state == sweep.NEEDS_OWNER


def test_a_capture_holds_the_page_its_transcription_under_the_archive_header_and_a_receipt(
    tmp_path: Path,
) -> None:
    out = tmp_path / "kingbird-2026-10-05"
    capture = capture_tool.write_capture(
        b"<html>page</html>",
        url="https://kingbird.myphotos.cc/packing/squares_in_squares.html",
        retrieved_utc="2026-10-05T06:00:00Z",
        last_modified="Thu, 01 Oct 2026 10:00:00 GMT",
        out=out,
        transcriber=lambda page: f"body of {page.name}\n",
    )
    text = (out / f"{capture_tool.STEM}.md").read_text(encoding="utf-8")
    assert text.startswith(f"# Archived: {capture_tool.STEM}\n\n**Source:** https://kingbird")
    assert "**Archived:** 2026-10-05, retrieved 06:00:00 UTC; the server reported" in text
    assert text.endswith("---\n\nbody of kingbird-squares-in-squares.html\n")
    receipt = json.loads((out / "capture.json").read_text(encoding="utf-8"))
    assert receipt["html_bytes"] == capture.html_bytes == len(b"<html>page</html>")
    assert sweep.newest_capture(tmp_path) == ("2026-10-05", out / f"{capture_tool.STEM}.md")


def test_another_catalogue_page_is_captured_beside_the_catalogue_under_its_own_name(
    tmp_path: Path,
) -> None:
    out = tmp_path / "kingbird-2026-10-05"
    stem = "kingbird-squares-in-squares-compared"
    capture_tool.write_capture(
        b"<html>older packings</html>",
        url="https://kingbird.myphotos.cc/packing/squares_in_squares__compared.html",
        retrieved_utc="2026-10-05T06:00:00Z",
        last_modified=None,
        out=out,
        transcriber=lambda page: f"body of {page.name}\n",
        stem=stem,
    )
    text = (out / f"{stem}.md").read_text(encoding="utf-8")
    assert text.startswith(f"# Archived: {stem}\n\n**Source:** https://kingbird")
    assert text.endswith(f"---\n\nbody of {stem}.html\n")
    assert (out / f"{stem}.capture.json").is_file()
    assert not (out / "capture.json").exists()
    assert sweep.newest_capture(tmp_path) is None


def test_a_capture_whose_transcription_fails_writes_nothing(tmp_path: Path) -> None:
    """The page used to be written before the transcriber ran, so a failed transcription
    left a capture directory holding a page and no transcription."""

    def refused(_page: Path) -> str:
        raise capture_tool.TranscriptionError("the transcriber exited 1")

    out = tmp_path / "kingbird-2026-10-05"
    with pytest.raises(capture_tool.TranscriptionError):
        capture_tool.write_capture(
            b"<html>page</html>",
            url="https://kingbird.myphotos.cc/packing/squares_in_squares.html",
            retrieved_utc="2026-10-05T06:00:00Z",
            last_modified=None,
            out=out,
            transcriber=refused,
        )
    assert not out.exists()
    assert sweep.newest_capture(tmp_path) is None


@pytest.mark.parametrize(
    ("command", "says"),
    [
        (("no-such-transcriber-on-path",), "is not installed"),
        (("false",), "exited 1"),
        ((sys.executable, "-c", "import time; time.sleep(5)"), "took longer than"),
    ],
)
def test_a_transcriber_that_is_missing_fails_or_hangs_is_a_typed_refusal(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, command: tuple[str, ...], says: str
) -> None:
    monkeypatch.setattr(capture_tool, "TRANSCRIBER", command)
    monkeypatch.setattr(capture_tool, "TRANSCRIBE_TIMEOUT_SECONDS", 0.2)
    page = tmp_path / "page.html"
    page.write_bytes(b"<html>page</html>")
    with pytest.raises(capture_tool.TranscriptionError, match=says):
        capture_tool.transcribe(page)


def test_the_capture_command_reports_a_failed_transcription_and_exits_1(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(capture_tool, "TRANSCRIBER", ("no-such-transcriber-on-path",))
    page = tmp_path / "page.html"
    page.write_bytes(b"<html>page</html>")
    out = tmp_path / "capture"
    assert capture_tool.main(["--html", str(page), "--out", str(out)]) == 1
    assert "capture failed:" in capsys.readouterr().err
    assert not out.exists()


# -- Regularization owed --------------------------------------------------------------


def _deferral_beads(state: str = "in_progress") -> dict[str, str]:
    """Every bead the committed lists defer regularization to, in one state."""
    from devtools import default_drawings as defaults  # noqa: PLC0415

    return {alias: state for _where, alias in defaults.deferrals()}


def _drawings(tmp_path: Path, n: int, state: str) -> Path:
    """The committed default-drawings record with count `n` put in `state`."""
    from devtools import default_drawings as defaults  # noqa: PLC0415

    record = json.loads(defaults.RECORD.read_text(encoding="utf-8"))
    for row in record["states"]:
        if row["n"] == n:
            row["state"] = state
    path = tmp_path / "default-drawings.json"
    path.write_text(defaults.text(record), encoding="utf-8")
    return path


def _corrected(monkeypatch: pytest.MonkeyPatch, n: int) -> None:
    """Declare count `n`'s deferral a corrected witness's, at the record's own witness: since
    the house rule, the only deferral the list may add (`default_drawings.CORRECTED`)."""
    from devtools import default_drawings as defaults  # noqa: PLC0415

    record = json.loads(defaults.RECORD.read_text(encoding="utf-8"))
    witness = next(row["witness"] for row in record["states"] if row["n"] == n)
    fix = defaults.Correction(
        witness["source"], witness.get("path"), "an-earlier-revision", witness["side"]
    )
    monkeypatch.setitem(defaults.CORRECTED, n, fix)


def _beyond_exemptions(items: list[sweep.Item]) -> list[sweep.Item]:
    """The items that are not exemptions, which the live record's four unratified ones
    would otherwise join in every test of another item."""
    return [item for item in items if " is exempt " not in item.what]


def _first(state: str) -> int:
    from devtools import default_drawings as defaults  # noqa: PLC0415

    record = json.loads(defaults.RECORD.read_text(encoding="utf-8"))
    found = next((row["n"] for row in record["states"] if row["state"] == state), None)
    if found is None:
        pytest.skip(f"the data holds no {state} count")
    return int(found)


def test_every_allowed_pending_count_is_owed_on_main_with_its_bead(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """think-9qm5 made regularizing every new house part of the standard intake, and the
    owner, 26 October 2026: "When something lands on our main rendered lists, the
    regularization should be done." A corrected witness's count the list defers is allowed
    on main by the gate, but its regularization is not done, so the sweep lists it as owed
    on main, needing action, with the bead that owns its runs; a bead that closes leaves
    it needing an owner."""
    from devtools import default_drawings as defaults  # noqa: PLC0415

    n = _first(defaults.REGULAR_AS_PUBLISHED)
    record = _drawings(tmp_path, n, defaults.PENDING)
    _corrected(monkeypatch, n)
    allowed = {**defaults.PENDING_ALLOWED, n: "think-aaaa: re-housed by a test adoption"}
    states = {**_deferral_beads(), "think-aaaa": "open"}
    section = sweep.regularization_section(_beads(**states), record=record, allowed=allowed)
    assert section.title == "Regularization owed"
    pending = _beyond_exemptions(section.items)
    assert all(item.state == sweep.OWED_ON_MAIN for item in pending)
    assert sorted(int(item.what.split()[2]) for item in pending) == sorted(allowed)
    added = next(item for item in pending if item.what.startswith(f"n = {n} "))
    assert (added.what, added.bead, added.bead_state) == (
        f"n = {n} pending on main: re-housed by a test adoption",
        "think-aaaa",
        "open",
    )
    assert "When a Witness Changes" in added.step
    for count, entry in defaults.PENDING_ALLOWED.items():
        (item,) = [found for found in pending if found.what.startswith(f"n = {count} ")]
        assert entry.startswith(f"{item.bead}: "), count
    assert set(sweep.needing_action([section])) >= set(pending)
    assert section.notes[0].startswith("Regularization states of 324 counts: ")
    counts = "pending count" if len(allowed) == 1 else "pending counts"
    assert (
        f"On main: {len(allowed)} {counts}, {len(allowed)} of them in PENDING_ALLOWED"
        in section.notes[0]
    )

    closed = sweep.regularization_section(
        _beads(**{**states, "think-aaaa": "closed"}), record=record, allowed=allowed
    )
    orphaned = _beyond_exemptions(sweep.needing_action([closed]))
    assert [(item.what, item.state, item.bead, item.bead_state) for item in orphaned] == [
        (added.what, sweep.NEEDS_OWNER, "think-aaaa", "closed")
    ]


def test_the_section_shows_only_exemptions_on_the_owner_word_without_action() -> None:
    """Section E of the intake review of 26 October 2026: the section listed seven owed
    counts and four exemptions as owned by their open beads, so nothing reached the owner.
    Now it holds nothing that does not need action but an exemption on the owner's word,
    listed for the owner with the quoted words and its review date; an exemption without
    that word needs action, with the bead it names and the day the gate fails it."""
    from devtools import default_drawings as defaults  # noqa: PLC0415

    exempt = sorted(n for n, held in defaults.SETTLED.items() if held.state == defaults.EXEMPT)
    if not exempt:
        pytest.skip("the data holds no exemption")
    states = _deferral_beads()
    section = sweep.regularization_section(_beads(**states), today=TODAY)
    assert [item.state for item in section.items] == [sweep.NEEDS_OWNER] * len(exempt)
    for n, item in zip(exempt, section.items, strict=True):
        held = defaults.SETTLED[n]
        assert item.what == (
            f"n = {n} is exempt {defaults.AWAITING_WORD} {defaults.UNRATIFIED_UNTIL}: "
            f"{held.outcome}"
        )
        bead = defaults.BEAD.search(held.evidence)
        assert bead is not None
        assert (item.bead, item.bead_state) == (bead[0], "in_progress")
        assert item.step.startswith("ask the owner: record the owner's words")
        assert item.step.endswith(f"before {defaults.UNRATIFIED_UNTIL}, when the gate fails it")
    assert "0 exemptions on the owner's word" in section.notes[0]
    assert f"{len(exempt)} exemptions without it" in section.notes[0]

    # The owner's word turns the first into a listing for the owner, which needs no action.
    n = exempt[0]
    word = defaults.OwnerWord(
        "so they look a little chaotic",
        "2026-10-23",
        "docs/project/policies/regularization-policy.md#13-flip-regularization",
    )
    worded = defaults.SETTLED[n]._replace(owner_word=word, review_by="2026-11-06")
    section = sweep.regularization_section(
        _beads(**states),
        settled={**defaults.SETTLED, n: worded},
        unratified=frozenset(exempt) - {n},
        today=date(2026, 10, 26),
    )
    shown = [item for item in section.items if item.state not in sweep.ACTION]
    assert [(item.what, item.state, item.since) for item in shown] == [
        (
            (
                f"n = {n} is exempt on the owner's word of 2026-10-23 ({word.recorded_in}): "
                f"\u201cso they look a little chaotic\u201d; {worded.outcome}"
            ),
            sweep.LISTED,
            "2026-10-23",
        )
    ]
    assert shown[0].step == "review it with the owner by 2026-11-06, or regularize the count"
    assert "1 exemption on the owner's word" in section.notes[0]


def test_an_allowlist_entry_naming_a_bead_the_store_lacks_needs_an_owner(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Review A2 of #650: an entry whose bead the store does not have owns nothing. Where
    the live list is empty, as from #654 up, a regular count is made pending for it, as a
    corrected witness's: since the house rule, the only deferral the list may add."""
    from devtools import default_drawings as defaults  # noqa: PLC0415

    record = defaults.RECORD
    if defaults.PENDING_ALLOWED:
        n = min(defaults.PENDING_ALLOWED)
    else:
        n = _first(defaults.REGULAR_AS_PUBLISHED)
        record = _drawings(tmp_path, n, defaults.PENDING)
        _corrected(monkeypatch, n)
    allowed = {**defaults.PENDING_ALLOWED, n: "think-zzzz: a corrected witness in a test"}
    states = _deferral_beads()
    assert "think-zzzz" not in states
    section = sweep.regularization_section(_beads(**states), record=record, allowed=allowed)
    action = _beyond_exemptions(sweep.needing_action([section]))
    assert [(item.what, item.state, item.bead, item.bead_state) for item in action] == [
        (
            f"n = {n} pending on main: a corrected witness in a test",
            sweep.NEEDS_OWNER,
            "think-zzzz",
            "no such bead",
        )
    ]


@pytest.mark.parametrize("broken", ["record", "index"])
def test_an_unreadable_record_or_index_needs_action_and_does_not_stop_the_sweep(
    tmp_path: Path, broken: str
) -> None:
    """Review A4 of #650: a malformed `default-drawings.json` raised `JSONDecodeError`, and
    a missing index `FileNotFoundError`, and `make intake` ended in a traceback with no
    other section shown. Each is now not checked, and needs action."""
    from devtools import default_drawings as defaults  # noqa: PLC0415

    record, index = defaults.RECORD, defaults.INDEX
    if broken == "record":
        record = tmp_path / "default-drawings.json"
        record.write_text('{"contract": ', encoding="utf-8")
    else:
        index = tmp_path / "missing-index.json"
    section = sweep.regularization_section(
        _beads(**_deferral_beads()), record=record, index=index
    )
    error = "JSONDecodeError" if broken == "record" else "FileNotFoundError"
    (unchecked,) = section.unchecked
    assert unchecked.startswith(
        "regularization: packing/atlas/known-best/default-drawings.json or the layer's "
        f"index could not be read ({error}: "
    )
    (item,) = sweep.needing_action([section])
    assert item.what.startswith(
        f"the regularization record or the layer's index could not be read: {error}: "
    )
    assert section.items == [item]
    assert "default_drawings --check" in item.step


@pytest.mark.parametrize("error", [KeyError("bead"), TypeError("not a bead")])
def test_a_fault_past_the_two_reads_raises_rather_than_reading_as_a_broken_record(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, error: Exception
) -> None:
    """Review B1 of #650: the A4 guard wrapped the whole section, so a fault in sorting the
    record into items, such as a bead store that raises, read as "the record or the
    layer's index could not be read", and its step sent the reader to two checks that
    pass. Only the record's read and the gate's are guarded now; the fault raises. Since
    the four unratified exemptions were settled (31 October 2026) the live record names
    no bead, so a corrected witness's deferral gives the section one to read."""
    from devtools import default_drawings as defaults  # noqa: PLC0415

    n = _first(defaults.REGULAR_AS_PUBLISHED)
    record = _drawings(tmp_path, n, defaults.PENDING)
    _corrected(monkeypatch, n)
    allowed = {**defaults.PENDING_ALLOWED, n: "think-aaaa: re-housed by a test adoption"}
    beads = _beads(**{**_deferral_beads(), "think-aaaa": "open"})

    def faulty(_self: sweep.Beads, _alias: str) -> str:
        raise error

    monkeypatch.setattr(sweep.Beads, "state", faulty)
    with pytest.raises(type(error)) as raised:
        sweep.regularization_section(beads, record=record, allowed=allowed)
    assert raised.value is error


def test_a_pending_count_no_list_names_needs_action_once(tmp_path: Path) -> None:
    """A count a change made pending without allowing it is what the records tier fails
    on; the sweep lists it once, as needing action, not again as the gate's problem."""
    from devtools import default_drawings as defaults  # noqa: PLC0415

    n = _first(defaults.REGULAR_AS_PUBLISHED)
    record = _drawings(tmp_path, n, defaults.PENDING)
    section = sweep.regularization_section(_beads(**_deferral_beads()), record=record)
    action = _beyond_exemptions(sweep.needing_action([section]))
    assert [item.what.split(":")[0] for item in action] == [
        f"n = {n} is pending and PENDING_ALLOWED does not name it"
    ]
    assert "allow it with the open bead that owns the runs" in action[0].step
    # It names `CORRECTED`, which the state gate holds every entry to (review C6 of #660).
    assert "name the witness it replaced in default_drawings.CORRECTED" in action[0].step
    # It points to the house rule rather than restate it (review A14 of #660).
    assert action[0].step.endswith('(result-import.md, "The House Rule")')


def test_anything_else_the_state_gate_fails_on_needs_action(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A listed count that is no longer pending: the list must come down in the change that
    decided it, and a pass that leaves it there has not finished."""
    from devtools import default_drawings as defaults  # noqa: PLC0415

    n = _first(defaults.REGULARIZED_STATE)
    _corrected(monkeypatch, n)
    allowed = {**defaults.PENDING_ALLOWED, n: "think-aaaa: a test"}
    section = sweep.regularization_section(
        _beads(**_deferral_beads(), **{"think-aaaa": "open"}),
        record=defaults.RECORD,
        allowed=allowed,
    )
    assert [item.what for item in _beyond_exemptions(sweep.needing_action([section]))] == [
        (
            "the regularization-state gate fails: "
            f"n={n}: PENDING_ALLOWED names it, but it is regularized; take it off the list"
        )
    ]


def test_a_missing_record_is_not_checked(tmp_path: Path) -> None:
    section = sweep.regularization_section(None, record=tmp_path / "missing.json")
    assert section.items == []
    assert section.unchecked == [
        "regularization: packing/atlas/known-best/default-drawings.json is missing"
    ]


def test_a_record_of_another_contract_needs_action_and_does_not_stop_the_sweep(
    tmp_path: Path,
) -> None:
    record = tmp_path / "default-drawings.json"
    record.write_text(json.dumps({"contract": "something/v1", "states": []}), encoding="utf-8")
    section = sweep.regularization_section(None, record=record)
    assert [item.what for item in sweep.needing_action([section])] == [
        (
            "the regularization-state gate fails: packing/atlas/known-best/"
            "default-drawings.json is not a packing.squares:DefaultDrawings/v2 record"
        )
    ]
    assert section.notes[0].startswith(
        "Regularization states of 0 counts. On main: 0 pending counts"
    )


def test_the_sweep_reports_regularization_with_the_record_side_queues() -> None:
    """The section is part of every sweep, `--offline` and `--json` included, beside the
    queues it follows; with no bead store the beads its items name are unconfirmed."""

    def network(*_: object) -> Any:
        pytest.fail("--offline made a network call")

    sections = sweep.sweep(
        today=TODAY,
        offline=True,
        capture=None,
        beads=None,
        compare_github=network,
        heads=network,
        history=network,
        fetch=network,
    )
    titles = [section.title for section in sections]
    assert titles.index("Regularization owed") == titles.index("Record-side queues") + 1
    (section,) = [section for section in sections if section.title == "Regularization owed"]
    # The live record may owe nothing (no exemption or pending count since 31 October
    # 2026); its notes still give the counts by state, and any item it lists is unconfirmed.
    assert section.notes[0].startswith("Regularization states of 324 counts: ")
    assert {item.bead_state for item in section.items} <= {"unconfirmed: no bead store"}
    assert "## Regularization owed" in sweep.markdown(sections, TODAY)
