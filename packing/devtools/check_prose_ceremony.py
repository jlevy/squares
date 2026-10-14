#!/usr/bin/env python3
"""Reader-facing prose credits a result and links its source; it carries no audit mechanics.

The owner, on 2026-10-01, of a register claim that read "certified at commit c8b36419
on 26 September 2026 by the author's clock": "The point is not certifying timezones or
commits, it is proper credit and having a link to the appropriate sources. Hashes can
be recorded at the point of ingestion but should not appear in text." Of the sentence
that closed twenty-four claims, "An externally produced, previously published result, not
peer reviewed; no new first-party mathematics is claimed": "this is externally produced
if it says that ... it should just be a clear citation." And of the claims themselves:
"long blocks like this should be broken into paragraphs."

So a sentence a reader meets says who established what, on which plain date, with a link
to the source. A commit id, a digest, a clock or timezone qualifier, a packet's byte
count, and a disclaimer the credit line already makes are audit mechanics. Their home is
a field written at ingestion: an evidence entry, a source packet's README, acquisition
record and receipts, a bibliography note, a case record's `resources[].url` and
`priority_notes[].published`.

This module holds three things to that.

- **Register prose**: `headline`, `claim`, `composition`, `notes`, `next_rung` and
  `significance.rationale` of every entry in `frontier/results.yaml`, which
  `RESULTS.md`, the synopsis and the site print word for word.
- **Reader documents**: the root reader documents, the frontier README and status table,
  the site's article templates, and each case record's body and the front-matter fields
  the site's case pages print: every `note`, the rigidity `scope`, and the `detail` of a
  conflict or blocker and the `claim` of a priority note.
- **Paragraphs**: a paragraph of a register prose field that runs past
  `PARAGRAPH_CHARS` in more than one sentence is a finding. A blank line in the field
  divides paragraphs, and the renderers keep it (`devtools.register_prose`).

What it does not read, because each is a structured or historical home: evidence
entries, the bibliography, source packets and receipts under `resources/`, the rest of
a case record's front matter, session, agenda and campaign records, dated reviews, the
defect log, development documentation (where a commit tells a developer where a rule
came from), and the synopsis's working record: its status, contracts, handoffs,
sessions, experiments and defects. A link target is never prose, so a pinned revision
inside a URL is where a reader should find it.

`prose-ceremony.yaml` beside this module lists the sentences that keep a flagged word
for a stated reason. An entry that no longer matches anything fails the check, so the
list cannot outlive what it excuses.

`--retained` answers the question an editor has before deleting a hash from a sentence:
where else the record keeps it. It searches the structured homes above for each
hexadecimal run given, or for every one the inventory finds.

Usage, from `packing/`:

    uv run --frozen --all-extras --group dev python -m devtools.check_prose_ceremony
    uv run --frozen --all-extras --group dev python -m devtools.check_prose_ceremony --inventory
    uv run --frozen --all-extras --group dev python -m devtools.check_prose_ceremony \\
        --retained c8b36419 144f4d3f
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from devtools.register_prose import paragraphs as register_paragraphs
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
FRONTIER = ROOT / "frontier"
REGISTER = FRONTIER / "results.yaml"
ALLOWLIST = Path(__file__).with_name("prose-ceremony.yaml")

#: The register fields a reader is shown as sentences. Everything else in an entry is a
#: structured field: ids, dates, rungs, evidence references, artifact paths, attribution.
REGISTER_PROSE = ("headline", "claim", "composition", "notes", "next_rung")

#: The longest a paragraph of register prose may run: about five sentences of the
#: register's usual length. Past that a field is a wall of text on the page that prints
#: it. One sentence may run longer, since a theorem's statement has nowhere to break.
PARAGRAPH_CHARS = 800
#: Where one sentence ends and the next begins, as `check_rung_figures` reads it: a
#: period that is not inside a decimal, then a capital.
_SENTENCE_BOUNDARY = re.compile(r"(?<=[a-z0-9)\]\"'])[.:]\s+(?=[A-Z`\[])")


@dataclass(frozen=True, slots=True)
class Document:
    """A reader document, or a glob of them, and the part of each that is read.

    `spans` are `(first heading, heading that ends it)` pairs, each a whole heading
    line; `None` reads the whole document.
    """

    pattern: str
    spans: tuple[tuple[str, str], ...] | None = None


#: The reader documents, repository-relative. `RESULTS.md` prints register prose word
#: for word, so the register is read in its place.
DOCUMENTS: tuple[Document, ...] = (
    Document("README.md"),
    Document("TUTORIAL.md"),
    Document("TUTORIAL-ADVANCED.md"),
    Document(
        "SYNOPSIS.md",
        # The reader's account: the opening and the results, then the mathematics. What
        # lies between and after is the program's working record.
        spans=(
            ("# Synopsis: The `s(n)` Program", "### Research Program Status and Roadmap"),
            ("## The Problem", "## The Cell Decomposition"),
        ),
    ),
    Document("conventions.md"),
    Document("epistemics.md"),
    Document("docs/project/policies/regularization-policy.md"),
    Document("packing/frontier/README.md"),
    Document("packing/frontier/STATUS.md"),
    Document("packing/devtools/templates/*-article.md"),
    Document("packing/frontier/n-*.md"),
)

#: A hexadecimal run long enough to be an abbreviated commit id or a digest: seven or
#: more characters, with at least one digit and one letter, so that neither a decimal
#: (`4426213`) nor a word (`defaced`) is one. A run joined to an identifier by `-`, `_`,
#: `/` or `.` is part of a name or a path, which the lookarounds leave alone.
HEX = re.compile(r"(?<![\w/.\-])(?=[0-9a-f]*[0-9])(?=[0-9a-f]*[a-f])[0-9a-f]{7,64}(?![\w/\-])")

#: What is never prose: a Markdown link's target and a bare URL.
_LINK_TARGET = re.compile(r"\]\([^)\s]*\)")
_URL = re.compile(r"https?://[^\s)>\]]+")


@dataclass(frozen=True, slots=True)
class Kind:
    """One kind of ceremony: its name, what finds it, and what to write instead."""

    name: str
    pattern: re.Pattern[str]
    remedy: str


KINDS: tuple[Kind, ...] = (
    Kind(
        "commit-or-digest",
        HEX,
        "name the source and link it; the revision is the evidence entry's or the packet's",
    ),
    Kind(
        "commit-phrase",
        # "commit" followed by a revision, digits-only ones included, which the hex
        # pattern above does not read as a hash. "At commit time" is not ceremony.
        re.compile(r"\bcommits?\s+`?[0-9a-f]{7,40}\b", re.IGNORECASE),
        "say when, as a plain date, and link the source",
    ),
    Kind(
        "clock",
        re.compile(
            # Anyone's clock, named or not ("the author's clock", "Couzo's clock", "the
            # authors' clocks"), with either apostrophe: the register writes ASCII, the
            # documents typographic. A wall clock has no owner and is not one.
            "\\b\\w+(?:['\u2019]s|s['\u2019]) clocks?\\b"
            r"|\bby (?:his|her|their) clocks?\b"
            r"|\bUTC\b|\bGMT\b|\bP[DS]T\b|\bE[DS]T\b|\bCES?T\b"
            # An ISO timestamp: a date with its time of day.
            r"|\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?Z?"
        ),
        "a plain date",
    ),
    Kind(
        "digest-word",
        re.compile(r"\bsha-?256\b|\bdigest-bound\b|\bhash-bound\b", re.IGNORECASE),
        "the digest stays in the packet's manifest or the evidence entry",
    ),
    Kind(
        "packet-bytes",
        re.compile(r"\b\d[\d,]* bytes\b"),
        "a packet's size is its manifest's",
    ),
    Kind(
        "disclaimer",
        re.compile(
            r"\bfirst-party mathematics\b|\bnot peer[- ]reviewed\b"
            r"|\bexternally (?:produced|proposed)\b|\bpreviously[- ]published result\b",
            re.IGNORECASE,
        ),
        "the credit line and the citation say whose result it is",
    ),
)
REMEDY = {kind.name: kind.remedy for kind in KINDS}


@dataclass(frozen=True, slots=True)
class Finding:
    """One piece of ceremony: where, of which kind, and the words themselves."""

    path: str
    """Repository-relative."""
    where: str
    """`T-051 claim` in the register, `line 42` or `front matter ...note` in a document."""
    kind: str
    words: str
    context: str

    def line(self) -> str:
        return f"{self.path}: {self.where}: {self.kind}: {self.words!r} in: {self.context}"


def _blank(match: re.Match[str]) -> str:
    return " " * len(match.group(0))


def prose_only(text: str) -> str:
    """`text` with every link target and URL blanked, positions kept."""
    return _URL.sub(_blank, _LINK_TARGET.sub(_blank, text))


def _context(text: str, start: int, end: int, width: int = 60) -> str:
    return " ".join(text[max(0, start - width) : min(len(text), end + width)].split())


def scan(text: str) -> Iterator[tuple[Kind, re.Match[str]]]:
    """Every piece of ceremony in a run of prose."""
    visible = prose_only(text)
    for kind in KINDS:
        for match in kind.pattern.finditer(visible):
            yield kind, match


def _findings(path: str, where: str, text: str) -> list[Finding]:
    return [
        Finding(
            path, where, kind.name, match.group(0), _context(text, match.start(), match.end())
        )
        for kind, match in scan(text)
    ]


def _relative(path: Path, repo: Path) -> str:
    return path.relative_to(repo).as_posix() if path.is_relative_to(repo) else path.name


# ---------- The register ----------


def register_prose(record: dict[str, Any]) -> Iterator[tuple[str, str]]:
    """The prose fields of one register entry, by name."""
    for name in REGISTER_PROSE:
        if record.get(name):
            yield name, str(record[name])
    rationale = (record.get("significance") or {}).get("rationale")
    if rationale:
        yield "significance.rationale", str(rationale)


def load_register(register: Path = REGISTER) -> list[dict[str, Any]]:
    return safe_load(register.read_text(encoding="utf-8"))["results"]


def register_findings(register: Path = REGISTER, repo: Path = REPO) -> list[Finding]:
    path = _relative(register, repo)
    return [
        finding
        for record in load_register(register)
        for name, text in register_prose(record)
        for finding in _findings(path, f"{record['id']} {name}", " ".join(text.split()))
    ]


def walls(register: Path = REGISTER) -> list[str]:
    """Each paragraph of register prose that runs past `PARAGRAPH_CHARS` in more than
    one sentence. A headline is one line by its schema and is not read."""
    problems: list[str] = []
    for record in load_register(register):
        for name, text in register_prose(record):
            if name == "headline":
                continue
            paragraphs = register_paragraphs(text)
            for index, paragraph in enumerate(paragraphs, start=1):
                if len(paragraph) > PARAGRAPH_CHARS and _SENTENCE_BOUNDARY.search(paragraph):
                    problems.append(
                        f"{record['id']} {name}: paragraph {index} of {len(paragraphs)} runs "
                        f"to {len(paragraph)} characters, over {PARAGRAPH_CHARS}; break it "
                        "by topic with a blank line"
                    )
    return problems


# ---------- The reader documents ----------


def _is_case_record(path: Path) -> bool:
    return re.fullmatch(r"n-\d{3}\.md", path.name) is not None


#: The front-matter fields of a case record that are sentences the site's case page
#: prints (`render_case_pages`): every `note`, and these four by their place. A path's
#: list indices are dropped before it is compared. `priority_notes[].published` and
#: `resources[].url` are beside them and are structured homes, so they are not read.
FRONT_MATTER_PROSE = (
    "rigidity.scope",
    "conflicts.detail",
    "blockers.detail",
    "priority_notes.claim",
)


def _notes(node: Any, trail: str = "") -> Iterator[tuple[str, str]]:
    """Every prose field in a case record's front matter (`FRONT_MATTER_PROSE` and each
    `note`), with the path to it."""
    if isinstance(node, dict):
        for key, value in node.items():
            here = f"{trail}.{key}" if trail else str(key)
            placed = re.sub(r"\[\d+\]", "", here)
            if isinstance(value, str) and (
                key == "note" or placed.endswith(FRONT_MATTER_PROSE)
            ):
                yield here, value
            else:
                yield from _notes(value, here)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _notes(value, f"{trail}[{index}]")


def _in_spans(lines: Sequence[str], spans: tuple[tuple[str, str], ...] | None) -> list[bool]:
    """Which lines a document's spans read. A span that never opens is an error: a
    renamed heading must not silently stop the check reading a section."""
    if spans is None:
        return [True] * len(lines)
    read = [False] * len(lines)
    for first, last in spans:
        if first not in lines:
            raise SystemExit(f"check_prose_ceremony: no heading {first!r} to begin reading at")
        begin = lines.index(first)
        end = lines.index(last, begin) if last in lines[begin:] else len(lines)
        for index in range(begin, end):
            read[index] = True
    return read


def document_paths(repo: Path = REPO) -> list[tuple[Path, Document]]:
    return [
        (path, document)
        for document in DOCUMENTS
        for path in sorted(repo.glob(document.pattern))
        if path.is_file()
    ]


def document_findings(
    path: Path, spans: tuple[tuple[str, str], ...] | None = None, repo: Path = REPO
) -> list[Finding]:
    """The ceremony in one reader document: its prose lines outside fenced code, and for
    a case record its body and its front matter's `note` fields only."""
    relative = _relative(path, repo)
    text = path.read_text(encoding="utf-8")
    findings: list[Finding] = []
    offset = 0
    if _is_case_record(path) and text.startswith("---\n"):
        _, front, text = text.split("---\n", 2)
        offset = front.count("\n") + 2
        for trail, note in _notes(safe_load(front)):
            findings += _findings(relative, f"front matter {trail}", " ".join(note.split()))
    lines = text.split("\n")
    fenced = False
    for number, (line, read) in enumerate(zip(lines, _in_spans(lines, spans), strict=True)):
        if line.startswith("```"):
            fenced = not fenced
            continue
        if read and not fenced:
            findings += _findings(relative, f"line {offset + number + 1}", line)
    return findings


def all_findings(repo: Path = REPO) -> list[Finding]:
    findings = register_findings(repo / "packing" / "frontier" / "results.yaml", repo)
    for path, document in document_paths(repo):
        findings += document_findings(path, document.spans, repo)
    return findings


# ---------- The allowlist ----------


@dataclass(frozen=True, slots=True)
class Allowed:
    """A sentence that keeps a flagged word, and why."""

    path: str
    words: str
    reason: str

    def covers(self, finding: Finding) -> bool:
        return finding.path == self.path and self.words in finding.context


def allowlist(path: Path = ALLOWLIST) -> list[Allowed]:
    if not path.is_file():
        return []
    entries = (safe_load(path.read_text(encoding="utf-8")) or {}).get("allowed") or []
    return [Allowed(entry["path"], entry["words"], entry["reason"]) for entry in entries]


def unexcused(
    findings: Sequence[Finding], allowed: Sequence[Allowed]
) -> tuple[list[Finding], list[Allowed]]:
    """The findings no allowlist entry covers, and the entries that cover nothing."""
    used: set[int] = set()
    remaining: list[Finding] = []
    for finding in findings:
        covering = [index for index, entry in enumerate(allowed) if entry.covers(finding)]
        used.update(covering)
        if not covering:
            remaining.append(finding)
    return remaining, [entry for index, entry in enumerate(allowed) if index not in used]


# ---------- Where a hash is retained ----------

#: The structured homes of a revision or a digest, repository-relative Git pathspecs.
HOMES = (
    "packing/frontier/evidence.yaml",
    "packing/frontier/source-coverage.yaml",
    "packing/resources/bibliography.yaml",
    "packing/resources/web",
    "packing/witnesses",
    # A certificate this project produced is bound by its experiment's receipt.
    "packing/campaign/series",
)


def retained(value: str, repo: Path = REPO) -> list[str]:
    """Where the record keeps `value` outside prose: the files of `HOMES` that hold it,
    and the case records whose front matter does."""
    listed = subprocess.run(
        ["git", "grep", "-l", "--fixed-strings", value, "--", *HOMES],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    homes = listed.stdout.split()
    for path in sorted((repo / "packing" / "frontier").glob("n-*.md")):
        text = path.read_text(encoding="utf-8")
        if text.startswith("---\n") and value in text.split("---\n", 2)[1]:
            homes.append(f"{_relative(path, repo)} (front matter)")
    return homes


def retention_report(values: Sequence[str], repo: Path = REPO) -> tuple[str, list[str]]:
    """One line per value with the homes that keep it, and the values nothing keeps."""
    lines: list[str] = []
    homeless: list[str] = []
    for value in values:
        homes = retained(value, repo)
        if not homes:
            homeless.append(value)
        more = f", and {len(homes) - 4} more" if len(homes) > 4 else ""
        shown = ", ".join(homes[:4]) + more
        lines.append(f"{value}: {shown or 'NOT RETAINED outside prose'}")
    return "\n".join(lines), homeless


# ---------- The command ----------


def inventory(findings: Sequence[Finding]) -> str:
    """Counts by kind and by file, then every finding."""
    by_kind = Counter(finding.kind for finding in findings)
    by_file = Counter(finding.path for finding in findings)
    lines = [f"{len(findings)} findings", "", "by kind:"]
    lines += [f"  {count:5d}  {kind}" for kind, count in by_kind.most_common()]
    lines += ["", "by file:"]
    lines += [f"  {count:5d}  {path}" for path, count in by_file.most_common()]
    lines += ["", "findings:"]
    lines += [f"  {finding.line()}" for finding in findings]
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n", 1)[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--inventory",
        action="store_true",
        help="list every finding with counts by kind and by file, excused ones included",
    )
    mode.add_argument(
        "--retained",
        nargs="*",
        metavar="HEX",
        help="where the record keeps each hash outside prose; with none given, every "
        "hash the inventory finds",
    )
    arguments = parser.parse_args(argv)
    findings = all_findings()
    if arguments.inventory:
        print(inventory(findings))
        print("\nparagraphs:")
        print("\n".join(f"  {problem}" for problem in walls()) or "  none over the limit")
        return 0
    if arguments.retained is not None:
        values = arguments.retained or sorted(
            {finding.words for finding in findings if finding.kind == "commit-or-digest"}
        )
        report, homeless = retention_report(values)
        print(report)
        return 1 if homeless else 0
    remaining, stale = unexcused(findings, allowlist())
    long_paragraphs = walls()
    for finding in remaining:
        print(f"CEREMONY: {finding.line()} -- {REMEDY[finding.kind]}", file=sys.stderr)
    for entry in stale:
        print(
            f"STALE: prose-ceremony.yaml excuses {entry.words!r} in {entry.path}, which no "
            "longer carries it",
            file=sys.stderr,
        )
    for problem in long_paragraphs:
        print(f"WALL: {problem}", file=sys.stderr)
    if remaining or stale or long_paragraphs:
        return 1
    print(
        f"reader prose carries no audit mechanics: {len(load_register())} register entries "
        f"and {len(document_paths())} reader documents read, "
        f"{len(findings) - len(remaining)} flagged words excused by name"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
