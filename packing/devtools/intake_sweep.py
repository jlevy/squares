#!/usr/bin/env python3
"""List every input the record has not taken in, across every standing intake source.

An intake pass (`campaign/result-import.md`, Running an Intake Pass) starts here. The
result import process used to start from "a GitHub issue, or a link", so an input that
arrived any other way waited on someone remembering it. On 2026-09-30 a Kingbird capture
found three September improvements and held them as `pending_catalogue_intake`, a plan
listed registering them, and no open bead owned the work. `check_requests --backlog`
reads issues and the register, `check_source_coverage` accepted the deferral with no end
date, and the record trailed the catalogue for five days until the owner noticed. The
same week an import held "until jlevy/squares#305 merges" stayed queued after #305
merged, and two evidence updates a packet README named as imports of their own were
never imported. This command reads every source the process takes results from and
every queue the record keeps, and says for each item which open bead owns it, or that
none does, or that what it waits on has already happened.

The sources, one section of the report each:

- **GitHub issues**: `check_requests --github`'s comparison through `gh`: issues the
  record lacks, replies missing from it, and comments after an entry's `read_through`.
- **Watched repositories**: every repository the source register, a packet's acquisition
  record, or the site's list of other projects names. `git ls-remote` reads each head,
  and a fetch of commits and trees (no blobs) reads two things. Commits past every
  packet's pin and every read in `campaign/intake-watch.yaml` are new to the record.
  Commits a packet's pin already contains but whose changed paths no packet at or after
  them retains are evidence nobody took in, such as wand125's `c56b9b7` and `1ebd484`.
  A pin is structured: an acquisition record's commit with the paths it declares, or a
  revision in a register source's address with the path the address names after it,
  the whole tree when it names none. Where both pin one commit the acquisition record's
  scope stands, since the register's address says what it cites, not what was retained.
  A commit named only in prose pins nothing.
- **The Kingbird catalogue**: the newest capture `devtools.capture_kingbird_catalogue`
  wrote, when it is newer than the record's, compared count by count through
  `devtools.diff_kingbird_catalogue`. A count it moves below its record is an intake.
- **Other catalogues**: the register's other catalogue and release sources, which no
  command reads, with the day each was last reviewed.
- **Record-side queues**: counts pending catalogue intake, deferred conflicts, the
  results and asks queued on open issues (each needs its own bead; the answer bead owns
  the reply, not the import), triage and replies owed, and the validation backlog.
- **Blocked imports**: a queued result or ask's `blocked_on`, and what an open
  `result-import` bead says it waits on: a `blocked_on:` line in its description or
  notes, the last one standing, else a present-tense sentence with a waiting word in its
  description, or a `blocks` dependency. Notes are history, so their prose is not read.
  A pull request or issue that has merged or closed, or a bead that has closed, is a
  blocker that has resolved, and nothing resumes the wait on its own.
- **Manual reports**: they have no machine source. The runbook makes each a bead
  labelled `result-import` first, so the open ones are listed as the bead queue.

An item **needs action** when the record is behind a source and no open bead owns the
difference, when the bead a deferral names is no longer open, or when a wait's blocker
has resolved. The command then exits 1. Items an open bead owns, the backlog and the bead
queue are listed and do not fail it. A source this run could not read is listed under
**Not Checked**, so a quiet report is not mistaken for a clean one.

Usage, from `packing/`, or `make intake` at the root, which captures the catalogue first::

    uv run --frozen --all-extras --group dev python -m devtools.intake_sweep
    uv run --frozen --all-extras --group dev python -m devtools.intake_sweep --offline
    uv run --frozen --all-extras --group dev python -m devtools.intake_sweep --json

`--offline` skips GitHub and the remote repositories, the network steps; everything else
reads the tree, the bead store and the capture directory. The command writes nothing
outside a temporary directory, and no validation tier runs it: refreshing a public source
is a dated research survey, not a network operation inside ordinary validation
(`frontier/README.md`, Source Coverage and Freshness).
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import subprocess
import sys
import tempfile
from collections.abc import Callable, Iterable, Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field, replace
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from devtools import check_bead_tree, check_requests
from devtools.audit_kingbird_catalogue import load_frontier_cases
from devtools.bead_state import LIVE
from devtools.capture_kingbird_catalogue import CAPTURE_PREFIX, CAPTURES, STEM
from devtools.diff_kingbird_catalogue import compare, record_standings
from devtools.overview_sections import OTHER_PROJECTS
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
COVERAGE = ROOT / "frontier" / "source-coverage.yaml"
FRONTIER = ROOT / "frontier"
WATCH = ROOT / "campaign" / "intake-watch.yaml"
PACKETS = ROOT / "resources" / "web"

NEEDS_OWNER = "needs an owner"
RESOLVED = "blocker resolved"
OWNED = "owned"
LISTED = "listed"
#: The states that make the sweep exit 1: work nobody owns, or a wait that is over.
ACTION = frozenset({NEEDS_OWNER, RESOLVED})

#: The register's roles for a source that publishes many results and is read as a whole.
CATALOGUE_ROLES = frozenset({"current-catalogue", "first-party-release"})
KINGBIRD = "kingbird-current"
IMPORT_LABEL = "result-import"
_GITHUB = re.compile(r"https://github\.com/([\w.-]+)/([\w.-]+)")
_GIST = re.compile(r"https://gist\.github\.com/(?:[\w.-]+/)?([0-9a-f]+)(?:\.git)?")
#: An issue, pull request or discussion: a page read by hand, not a repository to watch.
#: The SQUISH n153 source's address is an issue comment, and the sweep once watched
#: jlevy/squares itself because of it.
_TRACKER = re.compile(
    r"https://github\.com/[\w.-]+/[\w.-]+/(?:issues|pull|discussions)(?:[/#?]|$)"
)
#: A register address's pinned revision, and the path within it the address names.
_TREE = re.compile(r"/tree/([0-9a-f]{40})(?![0-9a-f])(?:/([^?#]*))?")
_CAPTURE_DIR = re.compile(rf"{re.escape(CAPTURE_PREFIX)}(\d{{4}}-\d{{2}}-\d{{2}})")
#: A sentence that says something waits: the blockers it names are read as blockers.
_WAITING = re.compile(
    r"\b(?:waits?|waiting|until|blocked|held|holds?|pending)\b"
    r"|\bafter\b(?=[^.;]*\b(?:merges|lands|closes)\b)",
    re.IGNORECASE,
)
#: A sentence that says what a wait was rather than what it is: "was held for #305,
#: which merged", "waited on #290". "Has been blocked" still waits, so it is not here.
_PAST_WAIT = re.compile(
    r"\b(?:was|were|had\s+been)\s+(?:\w+\s+)?(?:held|blocked|waiting|pending)\b|\bwaited\b",
    re.IGNORECASE,
)
#: A bead's declared wait, on a line of its own: `blocked_on: jlevy/squares#305,
#: think-wpuu`, or `blocked_on: none` once nothing is awaited. The last one stands.
_BLOCKED_ON = re.compile(r"^[ \t]*blocked_on:(?P<refs>.*)$", re.MULTILINE)
#: The heading `tbd` puts between a bead's description and its accumulated notes.
_NOTES = re.compile(r"^## Notes[ \t]*$", re.MULTILINE)
_ISSUE_REF = re.compile(r"(?<![\w/#])(?:(?P<repo>[\w.-]+/[\w.-]+))?#(?P<number>\d+)\b")
_BEAD_REF = re.compile(r"\bthink-[a-z0-9]{4}\b")
_SENTENCE = re.compile(r"(?<=[.;!?])\s+|\n+")
NETWORK_TIMEOUT_SECONDS = 60
#: Read without a terminal, so a repository that has gone private fails instead of asking.
GIT_ENV = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}

Mapped = Mapping[str, Any]


@dataclass(frozen=True)
class Item:
    """One thing the record has not taken in, or a queue entry, and who owns it."""

    what: str
    state: str
    bead: str = ""
    bead_state: str = ""
    since: str = ""
    step: str = ""


@dataclass
class Section:
    """One source's items, what the run noted about it, and what it could not read."""

    title: str
    items: list[Item] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    unchecked: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class QueuedBead:
    """An open `result-import` bead: its alias, status, title and what it says.

    `text` is the title and the description, which say what the bead is now; `notes` are
    what was appended to it since, read only for a `blocked_on:` line.
    """

    alias: str
    status: str
    title: str
    text: str
    blocked_by: tuple[str, ...] = ()
    notes: str = ""


def queued_bead(bead: Mapped, alias: str, blocked_by: Iterable[str] = ()) -> QueuedBead:
    """One parsed bead as the queue holds it, its description apart from its notes."""
    body = str(bead.get(check_bead_tree.BODY, ""))
    heading = _NOTES.search(body)
    description, notes = (
        (body[: heading.start()], body[heading.end() :]) if heading else (body, "")
    )
    return QueuedBead(
        alias=alias,
        status=str(bead.get("status")),
        title=str(bead.get("title", "")),
        text=f"{bead.get('title', '')}\n{description}",
        blocked_by=tuple(blocked_by),
        notes=notes,
    )


@dataclass(frozen=True)
class Beads:
    """Bead states by `think-` alias, and the open beads labelled `result-import`."""

    states: dict[str, str]
    queue: tuple[QueuedBead, ...]

    @classmethod
    def load(cls) -> Beads | None:
        found = check_bead_tree.load()
        if found is None:
            return None
        beads, _, aliases = found
        alias_of = {tail: f"think-{short}" for short, tail in aliases.items()}
        alias_by_id = {
            str(b["id"]): alias_of.get(str(b["id"]).rpartition("-")[2], str(b["id"]))
            for b in beads
        }
        blocked_by: dict[str, list[str]] = {}
        for bead in beads:
            for dependency in bead.get("dependencies") or ():
                if dependency.get("type") == "blocks" and dependency.get("target"):
                    target = alias_by_id.get(str(dependency["target"]), "")
                    blocked_by.setdefault(target, []).append(alias_by_id[str(bead["id"])])
        states = {alias_by_id[str(b["id"])]: str(b.get("status")) for b in beads}
        queue = tuple(
            sorted(
                (
                    queued_bead(
                        b,
                        alias_by_id[str(b["id"])],
                        blocked_by.get(alias_by_id[str(b["id"])], ()),
                    )
                    for b in beads
                    if str(b.get("status")) in LIVE and IMPORT_LABEL in (b.get("labels") or ())
                ),
                key=lambda queued: queued.alias,
            )
        )
        return cls(states, queue)

    def state(self, alias: str) -> str:
        return self.states.get(alias, "no such bead")


def owned(
    what: str, alias: str, beads: Beads | None, *, since: str = "", step: str = ""
) -> Item:
    """An item a bead is named to own: owned while that bead is open, else orphaned."""
    if not alias:
        return Item(what, NEEDS_OWNER, since=since, step=step)
    if beads is None:
        return Item(what, OWNED, alias, "unconfirmed: no bead store", since, step)
    state = beads.state(alias)
    return Item(what, OWNED if state in LIVE else NEEDS_OWNER, alias, state, since, step)


def age(since: str, today: date) -> str:
    """`since` and how many days ago it was, for a reader deciding what is stale."""
    try:
        days = (today - date.fromisoformat(since[:10])).days
    except ValueError:
        return since
    return f"{since[:10]} ({days} day{'' if days == 1 else 's'} ago)"


# -- Blockers -------------------------------------------------------------------------


def stated_blockers(text: str, repository: str, own: str = "") -> list[str]:
    """The pull requests, issues and beads a text says something waits on.

    Only a sentence with a waiting word counts ("waits for jlevy/squares#305", "held until
    think-ab12 closes", "after #305 merges"), so an issue the text merely cites is not
    read as a blocker. A sentence that tells what a wait was ("was held for #305, which
    merged") names nothing still awaited. A bare `#N` is on `repository`.
    """
    found: list[str] = []
    for sentence in _SENTENCE.split(text):
        if not _WAITING.search(sentence) or _PAST_WAIT.search(sentence):
            continue
        found.extend(_refs(sentence, repository, own))
    return list(dict.fromkeys(found))


def _refs(text: str, repository: str, own: str = "") -> list[str]:
    """Every pull request, issue and bead `text` names, other than `own`."""
    issues = (f"{m['repo'] or repository}#{m['number']}" for m in _ISSUE_REF.finditer(text))
    return [*issues, *(bead for bead in _BEAD_REF.findall(text) if bead != own)]


def declared_blockers(queued: QueuedBead, repository: str) -> list[str] | None:
    """What an open bead declares it waits on now, or None when it declares nothing.

    A `blocked_on:` line, in the description or the notes, declares it, and the last
    such line stands, so a later one replaces an earlier and `blocked_on: none` ends the
    wait. Without one, the description's sentences are read by `stated_blockers`. The
    notes' prose is never read: notes accumulate, and a sentence there that once said
    the bead waited, or that cited another bead's wait as an example, says nothing about
    what it waits on now.
    """
    declared = _BLOCKED_ON.findall(f"{queued.text}\n{queued.notes}")
    if not declared:
        return None
    return list(dict.fromkeys(_refs(declared[-1], repository, queued.alias)))


IssueFetch = Callable[[str], Mapped]


@dataclass
class Blockers:
    """Whether each blocker has resolved, read once each: beads from the store, pull
    requests and issues through `gh`, unless the run is offline."""

    beads: Beads | None
    fetch: IssueFetch | None
    seen: dict[str, str | None] = field(default_factory=dict)
    unread: set[str] = field(default_factory=set)

    def resolution(self, ref: str) -> str | None:
        """How `ref` resolved ("merged 2026-10-04"), "" while it holds, None if unknown."""
        if ref not in self.seen:
            self.seen[ref] = self._read(ref)
        return self.seen[ref]

    def _read(self, ref: str) -> str | None:
        if _BEAD_REF.fullmatch(ref):
            return self._bead(ref)
        if self.fetch is None:
            self.unread.add(ref)
            return None
        repository, _, number = ref.partition("#")
        try:
            issue = self.fetch(f"repos/{repository}/issues/{number}")
        except subprocess.CalledProcessError, OSError, ValueError:
            self.unread.add(ref)
            return None
        merged = str((issue.get("pull_request") or {}).get("merged_at") or "")
        if merged:
            return f"merged {merged[:10]}"
        if issue.get("state") == "closed":
            return f"closed {str(issue.get('closed_at') or '')[:10]}".strip()
        return ""

    def _bead(self, alias: str) -> str | None:
        state = None if self.beads is None else self.beads.state(alias)
        if state is None or state == "no such bead":
            return None
        return "" if state in LIVE else state

    def resolved(self, refs: Iterable[str]) -> list[str]:
        """Each of `refs` that has resolved, with how."""
        return [f"{ref}, {how}" for ref in refs if (how := self.resolution(ref))]

    def all_resolved(self, refs: Sequence[str]) -> list[str]:
        """Each of `refs` with how it resolved, once every one has; else nothing.

        A wait on several things is over at the last of them, so one that holds, or one
        this run could not read, keeps the whole wait open.
        """
        resolved = self.resolved(refs)
        return resolved if len(resolved) == len(refs) else []


# -- GitHub issues --------------------------------------------------------------------


def github_section(
    record: Mapped, *, offline: bool, compare_github: Callable[[Mapped], list[str]]
) -> Section:
    section = Section(f"GitHub issues on {record['repository']}")
    if offline:
        section.unchecked.append("GitHub issues: skipped by --offline")
        return section
    try:
        differences = compare_github(record)
    except (subprocess.CalledProcessError, OSError, ValueError) as error:
        detail = getattr(error, "stderr", "") or str(error)
        section.unchecked.append(f"GitHub issues: `gh api` failed: {str(detail).strip()[:200]}")
        return section
    section.items.extend(
        Item(difference, NEEDS_OWNER, step=_github_step(difference))
        for difference in differences
    )
    if not differences:
        section.notes.append("The record holds every issue, reply and comment.")
    return section


def _github_step(difference: str) -> str:
    """What `result-import.md`'s After the Merge does with one kind of difference."""
    if "is not in the record" in difference:
        return "enter it in result-requests.yaml with triage: pending, and an import bead"
    if "unread comment" in difference:
        return "read it: map any result it reports, then move the entry's read_through"
    if "reply missing" in difference:
        return "record the reply under the issue's replies"
    return "reconcile result-requests.yaml with the issue"


# -- Watched repositories -------------------------------------------------------------


def repository(url: str) -> str | None:
    """A source's address as its repository's, with no revision, path or `.git`.

    An issue, pull request or discussion is no repository's address: it is read by hand.
    """
    if _TRACKER.match(url):
        return None
    if match := _GITHUB.match(url):
        name = match[2].rstrip(".").removesuffix(".git")
        return f"https://github.com/{match[1]}/{name}"
    if match := _GIST.match(url):
        return f"https://gist.github.com/{match[1]}"
    return None


@dataclass(frozen=True)
class Packet:
    """A retained copy of a repository: where it is, the commit it pins, and the paths it
    retains there. An empty path retains the whole tree, which is what a packet without
    a declared scope is taken to do, so it can only hide a change, never invent one."""

    name: str
    pin: str
    scope: tuple[str, ...] = ("",)

    def retains(self, path: str) -> bool:
        return any(
            not prefix or path == prefix or path.startswith(prefix.rstrip("/") + "/")
            for prefix in self.scope
        )


@dataclass
class Watched:
    """A repository the record cites, and every packet that pins a commit of it."""

    url: str
    packets: list[Packet] = field(default_factory=list)
    cited_by: set[str] = field(default_factory=set)

    @property
    def pins(self) -> set[str]:
        return {packet.pin for packet in self.packets}


def _acquisition_sources(packets: Path) -> Iterable[tuple[str, Mapped]]:
    for path in sorted(packets.glob("*/acquisition/sources.json*")):
        raw = gzip.decompress(path.read_bytes()) if path.suffix == ".gz" else path.read_bytes()
        for source in json.loads(raw).get("sources") or ():
            yield path.parent.parent.name, source


def _scope(source: Mapped) -> tuple[str, ...]:
    if source.get("subtree_scope"):
        return tuple(str(path) for path in source["subtree_scope"])
    if source.get("files"):
        return tuple(str(entry["path"]) for entry in source["files"] if entry.get("path"))
    return ("",)


def watched_repositories(
    coverage: Mapped, packets: Path = PACKETS, projects: Iterable[str] | None = None
) -> dict[str, Watched]:
    """Every repository the record names, keyed in lower case, with the packets that pin it.

    A pin is structured: the commit a packet's acquisition record names, with the paths
    it declares, or a revision in a register source's address. The register's revision
    retains the path its address names after it (`/tree/<commit>/<path>`), or the whole
    tree when it names none, and is dropped where an acquisition record pins the same
    commit, whose declared scope is what was retained there. Most register addresses
    pin the commit of a scoped packet, so taking them as the whole tree retained every
    earlier commit's changes and hid every one no packet took in. A commit a README or
    a note names in prose pins nothing, since prose that names a commit is as likely to
    say it was not taken in.
    """
    found: dict[str, Watched] = {}

    def watch(url: str | None, cited_by: str) -> Watched | None:
        if url is None:
            return None
        entry = found.setdefault(url.lower(), Watched(url))
        entry.cited_by.add(cited_by)
        return entry

    acquired: list[tuple[Watched, Packet]] = []
    for name, source in _acquisition_sources(packets):
        entry = watch(repository(str(source.get("source_url", ""))), name)
        commit = str(source.get("source_commit") or source.get("source_ref") or "")
        if entry is not None and re.fullmatch(r"[0-9a-f]{40}", commit):
            acquired.append((entry, Packet(name, commit, _scope(source))))
    # A register address names what the register cites, not what a packet retains, so
    # where a packet pins the same commit its declared scope stands for both.
    retained = {(id(entry), packet.pin) for entry, packet in acquired}
    for source in coverage["sources"]:
        entry = watch(repository(source["url"]), source["id"])
        pin = _TREE.search(source["url"])
        if entry is not None and pin and (id(entry), pin[1]) not in retained:
            path = (pin[2] or "").strip("/")
            entry.packets.append(Packet(source["id"], pin[1], (path,)))
    for entry, packet in acquired:
        entry.packets.append(packet)
    for url in projects if projects is not None else (u for u, _, _ in OTHER_PROJECTS):
        watch(repository(url), "the site's other projects")
    return found


def remote_head(url: str) -> str:
    """The commit a repository's default branch points at now; network."""
    shown = subprocess.run(
        ("git", "ls-remote", url, "HEAD"),
        capture_output=True,
        text=True,
        timeout=NETWORK_TIMEOUT_SECONDS,
        env=GIT_ENV,
        check=False,
    )
    head = shown.stdout.split()[:1]
    if shown.returncode or not head:
        raise RuntimeError((shown.stderr.strip().splitlines() or ["no HEAD"])[-1])
    return head[0]


@dataclass(frozen=True)
class RepoHistory:
    """What a repository's history holds that the record has not taken in.

    `count` commits, dated `first` to `last`, are past every pin and read in the head's
    history (`pins_in_history` of them are in it). `unretained` are commits the pins
    already contain whose changes no packet at or after them retains and no read covers,
    each as its short id and subject.
    """

    count: int
    first: str
    last: str
    subjects: tuple[str, ...]
    pins_in_history: int
    unretained: tuple[str, ...] = ()


def read_history(
    url: str, head: str, packets: Sequence[Packet], reads: Iterable[str]
) -> RepoHistory:
    """Read a repository's commits and trees, never its blobs, and compare them; network.

    `--filter=blob:none` takes about two seconds and under a megabyte for a repository of
    560 commits, into a directory removed on return. Which pins and reads the head's
    history holds is read from its commit list, never by asking for an object, since a
    partial clone fetches a missing object from the remote, one round trip each: the first
    version of this sweep did that and took minutes.
    """
    with tempfile.TemporaryDirectory(prefix="intake-sweep-") as scratch:

        def git(*arguments: str) -> str:
            shown = subprocess.run(
                ("git", "-C", scratch, *arguments),
                capture_output=True,
                text=True,
                timeout=NETWORK_TIMEOUT_SECONDS,
                env=GIT_ENV,
                check=False,
            )
            if shown.returncode:
                raise RuntimeError((shown.stderr.strip().splitlines() or ["git failed"])[-1])
            return shown.stdout

        git("init", "--quiet", "--bare")
        git("fetch", "--quiet", "--no-tags", "--filter=blob:none", url, head)
        history = set(git("rev-list", head).split())
        pinned = [packet for packet in packets if packet.pin in history]
        read = sorted({commit for commit in reads if commit in history})
        stops = sorted({packet.pin for packet in pinned} | set(read))
        listed = git("log", "--format=%cI%x09%s", head, "--not", *stops, "--")
        lines = [line.split("\t", 1) for line in listed.splitlines() if "\t" in line]
        return RepoHistory(
            count=len(lines),
            first=lines[-1][0][:10] if lines else "",
            last=lines[0][0][:10] if lines else "",
            subjects=tuple(subject for _, subject in lines[:3]),
            pins_in_history=len({packet.pin for packet in pinned}),
            unretained=_unretained(git, pinned, read),
        )


def _unretained(
    git: Callable[..., str], pinned: Sequence[Packet], read: Sequence[str]
) -> tuple[str, ...]:
    """Commits between the oldest and newest pins whose changed paths nothing retains.

    A change is retained when a packet whose pin contains the commit declares its path; a
    read in `intake-watch.yaml` that contains the commit covers it either way. Commits
    before the oldest pin are the history the first packet took as given.
    """
    pins = sorted({packet.pin for packet in pinned})
    if not pins:
        return ()
    reach = {pin: set(git("rev-list", pin).split()) for pin in pins}
    covered = set().union(*(set(git("rev-list", commit).split()) for commit in read))
    oldest = min(pins, key=lambda pin: len(reach[pin]))
    log = git(
        "log", "--no-renames", "--name-only", "--format=%x1e%H%x09%s", *pins, "--not", oldest
    )
    found: list[str] = []
    for block in log.split("\x1e")[1:]:
        header, _, names = block.partition("\n")
        commit, _, subject = header.partition("\t")
        if commit in covered:
            continue
        paths = [path for path in names.splitlines() if path]
        if any(
            not any(commit in reach[p.pin] and p.retains(path) for p in pinned)
            for path in paths
        ):
            found.append(f"{commit[:7]} {subject}")
    return tuple(found)


Heads = Callable[[str], str]
History = Callable[[str, str, Sequence[Packet], Iterable[str]], RepoHistory]


def repositories_section(
    coverage: Mapped,
    watch: Mapped,
    beads: Beads | None,
    *,
    offline: bool,
    heads: Heads = remote_head,
    history: History = read_history,
    packets: Path = PACKETS,
    projects: Iterable[str] | None = None,
) -> Section:
    repos = watched_repositories(coverage, packets, projects)
    section = Section(f"Watched repositories ({len(repos)})")
    reads: dict[str, list[Mapped]] = {}
    for entry in watch.get("repositories") or ():
        reads.setdefault(str(entry["url"]).lower(), []).append(entry)
    section.unchecked.extend(
        f"intake-watch.yaml reads {url}, which no record cites; remove the entry"
        for url in sorted(set(reads) - set(repos))
    )
    if offline:
        section.unchecked.append(f"{len(repos)} repository heads: skipped by --offline")
        return section
    keys = sorted(repos)
    with ThreadPoolExecutor(max_workers=8) as pool:
        found = dict(
            zip(keys, pool.map(_try(heads), (repos[k].url for k in keys)), strict=True)
        )
        jobs = [
            (repos[k], head, [str(r["read_through"]) for r in reads.get(k, ())])
            for k in keys
            if isinstance(head := found[k], str)
        ]
        histories = dict(
            zip(
                [entry.url.lower() for entry, _, _ in jobs],
                pool.map(lambda job: _try_history(history, *job), jobs),
                strict=True,
            )
        )
    current = 0
    for key in keys:
        entry, head = repos[key], found[key]
        if isinstance(head, Exception):
            section.unchecked.append(f"{entry.url}: `git ls-remote` failed: {head}")
            continue
        commits = histories[key]
        if isinstance(commits, Exception):
            section.unchecked.append(f"{entry.url}: its history could not be read: {commits}")
        matching = [r for r in reads.get(key, ()) if str(r["read_through"]) == head]
        if head in entry.pins:
            current += 1
            section.notes.extend(
                f"{entry.url}: a packet now pins {head[:12]}, so intake-watch.yaml's read of "
                "it can be removed."
                for _ in matching
            )
        elif matching:
            section.items.extend(_read_item(entry.url, head, read, beads) for read in matching)
        else:
            section.items.append(_new_head(entry, head, commits, reads.get(key, ())))
        if isinstance(commits, RepoHistory) and commits.unretained:
            section.items.append(_unretained_item(entry.url, commits.unretained))
    section.notes.insert(0, f"{current} of {len(repos)} heads are a commit a packet pins.")
    return section


def _try(function: Callable[[str], str]) -> Callable[[str], str | Exception]:
    def attempt(argument: str) -> str | Exception:
        try:
            return function(argument)
        except (RuntimeError, OSError, subprocess.SubprocessError) as error:
            return error

    return attempt


def _try_history(
    history: History, entry: Watched, head: str, reads: list[str]
) -> RepoHistory | Exception:
    try:
        return history(entry.url, head, entry.packets, reads)
    except (RuntimeError, OSError, subprocess.SubprocessError) as error:
        return error


def _read_item(url: str, head: str, read: Mapped, beads: Beads | None) -> Item:
    if read.get("bead"):
        return owned(
            f"{url} at {head[:12]}: {read['note']}",
            str(read["bead"]),
            beads,
            since=str(read["read_on"]),
            step="import it: a packet at the head, then stages 2 and 3",
        )
    return Item(
        f"{url}: read through {head[:12]} on {read['read_on']}, nothing to import",
        LISTED,
        since=str(read["read_on"]),
    )


_REPOSITORY_STEP = (
    "read it: an import bead and a packet for a new result, else a read in intake-watch.yaml"
)


def _new_head(
    entry: Watched, head: str, commits: RepoHistory | Exception, reads: Sequence[Mapped]
) -> Item:
    past = "the last pass's read" if reads else "every retained pin"
    if isinstance(commits, Exception):
        what = f"{entry.url}: head {head[:12]} is past {past}; its commits could not be read"
        return Item(what, NEEDS_OWNER, step=_REPOSITORY_STEP)
    if not entry.packets and not reads:
        where = "no packet pins it"
    elif commits.pins_in_history or reads:
        where = f"{commits.count} commit{'' if commits.count == 1 else 's'} past {past}"
    else:
        where = "no retained pin is in its history"
    span = f", {commits.first}" if commits.first else ""
    if commits.last != commits.first:
        span += f" to {commits.last}"
    newest = (
        f"; newest: {commits.subjects[0]}" if commits.subjects and commits.subjects[0] else ""
    )
    return Item(
        f"{entry.url}: head {head[:12]}, {where}{span}{newest}",
        NEEDS_OWNER,
        since=commits.first,
        step=_REPOSITORY_STEP,
    )


def _unretained_item(url: str, unretained: Sequence[str]) -> Item:
    shown = "; ".join(unretained[:3]) + ("; …" if len(unretained) > 3 else "")
    count = len(unretained)
    return Item(
        f"{url}: {count} commit{'' if count == 1 else 's'} a pin contains changed paths no "
        f"packet at or after {'it' if count == 1 else 'them'} retains: {shown}",
        NEEDS_OWNER,
        step="an evidence update or an import bead for each, else a read in intake-watch.yaml",
    )


# -- The Kingbird catalogue and the other catalogues ----------------------------------


def newest_capture(captures: Path = CAPTURES) -> tuple[str, Path] | None:
    """The newest dated capture `capture_kingbird_catalogue` wrote, as (date, transcription)."""
    dated = [
        (match[1], path / f"{STEM}.md")
        for path in captures.glob(f"{CAPTURE_PREFIX}*")
        if (match := _CAPTURE_DIR.fullmatch(path.name)) and (path / f"{STEM}.md").is_file()
    ]
    return max(dated) if dated else None


def kingbird_section(
    coverage: Mapped,
    beads: Beads | None,
    today: date,
    *,
    capture: tuple[str, Path] | None,
    cases: Mapping[int, Mapping[str, object]] | None = None,
) -> Section:
    source = next(s for s in coverage["sources"] if s["id"] == KINGBIRD)
    reviewed = str(source["reviewed"])
    section = Section("The Kingbird catalogue")
    command = "`make intake`, or `python -m devtools.capture_kingbird_catalogue` from packing/"
    if capture is None or capture[0] <= reviewed:
        section.unchecked.append(
            f"Kingbird catalogue: no capture newer than the record's, {age(reviewed, today)}; "
            f"capture one with {command}"
        )
        return section
    captured, path = capture
    retained = (ROOT / str(source["local"])).with_suffix(".md")
    changes = compare(retained.read_text(encoding="utf-8"), path.read_text(encoding="utf-8"))
    standings = record_standings(
        changes, load_frontier_cases(FRONTIER) if cases is None else cases
    )
    pending = {int(e["n"]): e for e in coverage.get("pending_catalogue_intake") or ()}
    other: list[int] = []
    for change in changes:
        standing = standings.get(change.n)
        if standing is None or standing.relation != "below" or change.after is None:
            other.append(change.n)
            continue
        what = (
            f"n = {change.n}: the capture of {captured} prints {change.after.side}, below the "
            f"record's {standing.value} ({standing.source_key})"
        )
        declared = pending.get(change.n)
        if declared is not None and Decimal(declared["catalogue_value"]) == Decimal(
            change.after.side
        ):
            section.items.append(
                owned(what, str(declared["bead"]), beads, since=str(declared["recorded"]))
            )
        else:
            section.items.append(
                Item(
                    what,
                    NEEDS_OWNER,
                    since=captured,
                    step="an intake: a bead, then register it or declare it pending intake",
                )
            )
    section.notes.append(
        f"Compared the capture of {captured} with the record's of {reviewed}: "
        f"{len(changes)} count{'' if len(changes) == 1 else 's'} read differently, "
        f"{len(changes) - len(other)} below the record."
    )
    if other:
        section.notes.append(
            "Changed and not below the record, for the refresh to classify with "
            f"`diff_kingbird_catalogue`: n = {', '.join(map(str, other))}."
        )
    return section


def catalogues_section(coverage: Mapped, today: date) -> Section:
    """The register's other catalogue and release sources: no command reads them."""
    section = Section("Other catalogues and releases")
    for source in coverage["sources"]:
        if source["role"] not in CATALOGUE_ROLES or source["id"] == KINGBIRD:
            continue
        section.unchecked.append(
            f"{source['title']} ({source['url']}): read by hand; last reviewed "
            f"{age(str(source['reviewed']), today)}, source dated {source['source_date']}"
        )
    return section


# -- Record-side queues ---------------------------------------------------------------


def queues_section(
    coverage: Mapped,
    record: Mapped,
    register: check_requests.Register,
    beads: Beads | None,
    *,
    today: date,
    blockers: Blockers,
) -> Section:
    section = Section("Record-side queues")
    for entry in coverage.get("pending_catalogue_intake") or ():
        section.items.append(
            owned(
                f"n = {entry['n']} pending catalogue intake: the catalogue prints "
                f"{entry['catalogue_value']}, the record reports {entry['record_value']}",
                str(entry.get("bead") or ""),
                beads,
                since=age(str(entry.get("recorded") or ""), today),
                step="register the result and take the side into the record",
            )
        )
    for claim in coverage.get("beyond_horizon_claims") or ():
        if claim.get("disposition") == "deferred-conflict":
            section.items.append(
                owned(
                    f"n = {claim['n']} deferred conflict with {claim['source_id']}",
                    str(claim.get("bead") or ""),
                    beads,
                )
            )
    repository = str(record.get("repository", ""))
    for issue in record["issues"]:
        if issue["state"] != "open":
            continue
        number = issue["number"]
        for result in issue.get("results") or ():
            if result.get("queued"):
                section.items.append(
                    _queued(
                        f"#{number} queued result {result['key']}",
                        result,
                        str(result.get("not_registered") or ""),
                        repository,
                        beads=beads,
                        blockers=blockers,
                        since=str(issue["opened"]),
                    )
                )
        for ask in issue.get("asks") or ():
            if ask["state"] == "queued":
                section.items.append(
                    _queued(
                        f"#{number} queued ask: {ask['what']}",
                        ask,
                        str(ask.get("note") or ""),
                        repository,
                        beads=beads,
                        blockers=blockers,
                        since=str(issue["opened"]),
                    )
                )
        state = check_requests.issue_state(issue, register)
        owed = [
            *(["triage"] if issue["triage"] == "pending" else []),
            *(["a reply"] if state.replies_due else []),
        ]
        if owed:
            section.items.append(
                owned(
                    f"#{number} owes {' and '.join(owed)}",
                    str(issue["answer_bead"]),
                    beads,
                    since=str(issue["opened"]),
                    step="triage by stage 1; draft the reply with check_requests --draft",
                )
            )
    return section


def _queued(
    what: str,
    entry: Mapped,
    text: str,
    repository: str,
    *,
    beads: Beads | None,
    blockers: Blockers,
    since: str,
) -> Item:
    """A queued result or ask: owned by its own bead, and held by what it waits on.

    The issue's answer bead owns the reply, not the import, and `beads` may name several,
    so an item with no bead of its own is unowned. Its blockers are its `blocked_on`,
    whose wait is over once every one has resolved, as the schema says; without one, a
    blocker its text says it waits on counts once it resolves.
    """
    declared = [str(ref) for ref in entry.get("blocked_on") or ()]
    item = owned(
        what,
        str(entry.get("bead") or ""),
        beads,
        since=since,
        step="name the bead that imports it, as `bead` on the entry",
    )
    resolved = (
        blockers.all_resolved(declared)
        if declared
        else blockers.resolved(stated_blockers(text, repository))
    )
    if resolved:
        detail = f"{item.what}; it waits on {'; '.join(resolved)}"
        state = RESOLVED if item.state == OWNED else item.state
        return replace(
            item, what=detail, state=state, step="resume it, or say what it waits on"
        )
    return item


def blocked_section(beads: Beads | None, blockers: Blockers, repository: str) -> Section:
    """Open import beads whose stated blocker has merged, closed or been closed.

    A bead's `blocked_on:` line (`declared_blockers`) counts once every blocker it lists
    has resolved. Without one, a blocker its description names counts once it resolves,
    since the sentence that names it says the bead waits on it. Its `blocks` dependencies
    count once all of them have closed, because a bead with several children waits on
    the last.
    """
    section = Section("Blocked imports")
    if beads is None:
        section.unchecked.append("blocked imports: no bead store")
        return section
    waiting = 0
    for queued in beads.queue:
        declared = declared_blockers(queued, repository)
        stated = (
            declared
            if declared is not None
            else stated_blockers(queued.text, repository, queued.alias)
        )
        if not stated and not queued.blocked_by:
            continue
        waiting += 1
        resolved = (
            blockers.all_resolved(stated) if declared is not None else blockers.resolved(stated)
        )
        if queued.blocked_by:
            dependencies = blockers.all_resolved(queued.blocked_by)
            resolved += [ref for ref in dependencies if ref not in resolved]
        if resolved:
            section.items.append(
                Item(
                    f"{queued.alias} ({queued.title}) waits on {'; '.join(resolved)}",
                    RESOLVED,
                    bead=queued.alias,
                    bead_state=queued.status,
                    step="resume it, or rewrite what the bead says it waits on",
                )
            )
    section.notes.append(
        f"{waiting} open `{IMPORT_LABEL}` bead{'' if waiting == 1 else 's'} name a blocker; "
        f"{len(section.items)} of them name one that has resolved."
    )
    if blockers.unread:
        section.unchecked.append(
            f"blockers not read: {', '.join(sorted(blockers.unread))} (offline, or `gh` failed)"
        )
    return section


def backlog_section(
    record: Mapped, register: check_requests.Register, beads: Beads | None
) -> Section:
    section = Section("Validation backlog: register entries below V3 or C3")
    for row in check_requests.backlog_rows(record, register):
        named = [f"{b} ({beads.state(b) if beads else '?'})" for b in row.beads]
        section.items.append(
            Item(
                f"{row.id} at {row.rungs}, {row.status}"
                + (f", {row.activity}" if row.activity else "")
                + (f"; issues {', '.join(f'#{n}' for n in row.issues)}" if row.issues else ""),
                LISTED,
                bead=", ".join(named) or "none named",
                step=row.next_rung[:160],
            )
        )
    return section


def bead_queue_section(beads: Beads | None) -> Section:
    section = Section(f"Open `{IMPORT_LABEL}` beads, manual reports included")
    if beads is None:
        section.unchecked.append(
            "bead queue: no bead store (no tbd sync worktree, no tbd-sync branch)"
        )
        return section
    section.items.extend(
        Item(queued.title, LISTED, bead=queued.alias, bead_state=queued.status)
        for queued in beads.queue
    )
    return section


# -- The report -----------------------------------------------------------------------


def sweep(
    *,
    today: date,
    offline: bool,
    capture: tuple[str, Path] | None,
    beads: Beads | None,
    compare_github: Callable[[Mapped], list[str]] = check_requests.compare_github,
    heads: Heads = remote_head,
    history: History = read_history,
    fetch: IssueFetch | None = check_requests.gh_fetch,
) -> list[Section]:
    coverage = safe_load(COVERAGE.read_text(encoding="utf-8"))
    watch = safe_load(WATCH.read_text(encoding="utf-8"))
    record = check_requests.load_record()
    register = check_requests.load_register()
    blockers = Blockers(beads, None if offline else fetch)
    repository = str(record["repository"])
    return [
        github_section(record, offline=offline, compare_github=compare_github),
        repositories_section(
            coverage, watch, beads, offline=offline, heads=heads, history=history
        ),
        kingbird_section(coverage, beads, today, capture=capture),
        catalogues_section(coverage, today),
        queues_section(coverage, record, register, beads, today=today, blockers=blockers),
        blocked_section(beads, blockers, repository),
        backlog_section(record, register, beads),
        bead_queue_section(beads),
    ]


def needing_action(sections: Sequence[Section]) -> list[Item]:
    return [item for section in sections for item in section.items if item.state in ACTION]


def _count(number: int, noun: str) -> str:
    return f"{number} {noun}{'' if number == 1 else 's'}"


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def markdown(sections: Sequence[Section], today: date) -> str:
    """The report: what needs action and what was not checked first, then each source."""
    action = [(s.title, i) for s in sections for i in s.items if i.state in ACTION]
    orphans = sum(item.state == NEEDS_OWNER for _, item in action)
    owned_count = sum(item.state == OWNED for s in sections for item in s.items)
    unchecked = [line for section in sections for line in section.unchecked]
    summary = (
        f"{_count(orphans, 'item')} without an open bead to own it, "
        f"{_count(len(action) - orphans, 'item')} whose blocker has resolved, "
        f"{_count(owned_count, 'item')} owned by an open bead, and "
        f"{_count(len(unchecked), 'source')} not checked."
    )
    lines = [f"# Intake Sweep, {today.isoformat()}", "", summary, ""]
    if action:
        lines += [
            "## Needs Action",
            "",
            "| source | item | state | since | next |",
            "| --- | --- | --- | --- | --- |",
        ]
        lines += [
            f"| {title} | {_cell(i.what)} | {i.state} | {i.since} | {_cell(i.step)} |"
            for title, i in action
        ]
        lines.append("")
    if unchecked:
        lines += ["## Not Checked", "", *(f"- {line}" for line in unchecked), ""]
    for section in sections:
        lines += [f"## {section.title}", ""]
        lines += [*section.notes, ""] if section.notes else []
        shown = [item for item in section.items if item.state not in ACTION]
        if len(shown) < len(section.items):
            hidden = len(section.items) - len(shown)
            lines += [f"{_count(hidden, 'item')} above need action.", ""]
        if shown:
            lines += ["| item | state | bead | since |", "| --- | --- | --- | --- |"]
            for item in shown:
                bead = f"{item.bead} ({item.bead_state})" if item.bead_state else item.bead
                lines.append(
                    f"| {_cell(item.what)} | {item.state} | {_cell(bead)} | {item.since} |"
                )
            lines.append("")
        if section.unchecked:
            lines += ["Not checked: see above.", ""]
        elif not section.items and not section.notes:
            lines += ["Nothing.", ""]
    return "\n".join(lines).rstrip() + "\n"


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    command.add_argument("--offline", action="store_true", help="skip GitHub and remote heads")
    command.add_argument("--json", action="store_true", help="print the sweep as JSON")
    command.add_argument("--capture", type=Path, help="a Kingbird capture directory to compare")
    command.add_argument("--today", type=date.fromisoformat, help=argparse.SUPPRESS)
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    today = args.today or datetime.now(UTC).date()
    if args.capture is not None:
        match = _CAPTURE_DIR.search(args.capture.name)
        capture = (match[1] if match else today.isoformat(), args.capture / f"{STEM}.md")
    else:
        capture = newest_capture()
    sections = sweep(today=today, offline=args.offline, capture=capture, beads=Beads.load())
    if args.json:
        document = {
            "date": today.isoformat(),
            "needs_action": len(needing_action(sections)),
            "sections": [asdict(section) for section in sections],
        }
        json.dump(document, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        sys.stdout.write(markdown(sections, today))
    return 1 if needing_action(sections) else 0


if __name__ == "__main__":
    raise SystemExit(main())
