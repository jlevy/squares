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
    """The register cited wand125's 797bdf6 as a whole tree, which retained every path.

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
    """The review's reproduction, in small: wand125's register pinned the head as a whole
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
                sweep.Item("held", sweep.OWNED, bead="think-aaaa", bead_state="open"),
            ],
            unchecked=["a source: skipped"],
        )
    ]
    report = sweep.markdown(sections, TODAY)
    assert (
        "1 item without an open bead to own it, 1 item whose blocker has resolved, "
        "1 item owned by an open bead, and 1 source not checked." in report
    )
    assert report.index("## Needs Action") < report.index("## Not Checked")
    assert report.index("## Not Checked") < report.index("## Source")
    assert "| Source | orphan | needs an owner |  | open a bead |" in report
    assert "| held | owned | think-aaaa (open) |  |" in report
    assert sweep.needing_action(sections) == sections[0].items[:2]


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
