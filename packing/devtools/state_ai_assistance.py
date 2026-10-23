#!/usr/bin/env python3
# ruff: noqa: RUF001 -- this module writes case-record prose, whose typography uses curly
# apostrophes and quotation marks.
"""Find, and write, the sentence each case record owes a source that says AI assisted it.

attribution.md, People, Projects and Assistance requires case records, the register
and README prose to state declared AI assistance in the source's terms.
A case record is hand-written prose, and on 2026-09-29 some fifty of them cited Hosono's
or Tokoharu's releases in their front matter without saying so in their bodies. Writing
one sentence into each by hand is the one-off edit `OR-1` asks to be a tool, and
checking that none is missing afterwards is the measurement that should outlive it.

**The statements live in the bibliography**, as each source's `ai_assistance`: the
sentence to write in the source's own words, the paragraph that describes the source's
result (`anchor`), the words that show the paragraph already says so (`marker`) and,
where the source speaks of some counts only, those `counts`. Keys that make the same
statement share one `Statement`. Until 23 October 2026 the statements were a list in
this module, and four keys records cited were missing from it, their statements carried
by hand (think-j5so); a new source now states its assistance where its key is defined.
A record owes the statement when its front matter cites one of the keys and a body
paragraph matches the anchor; it has it when such a paragraph contains the marker.
`--apply` appends the sentence to the first anchored paragraph of every record that
owes one; the Markdown formatter then reflows it. `--check` also refuses a field whose
anchor is no pattern or whose sentence lacks its marker, and runs in `packing-validate`
with the case prose (`case prose agrees with its own front matter`).

Records whose body never describes the source owe nothing and are listed by `--check`
as such, since where the sentence belongs is then a question for the record rather than
this tool. Statements that differ release by release, as `n-017`'s five successive
external bounds do, are written by hand and carry no `ai_assistance`.

**The Kingbird catalogue states AI assistance entry by entry**, a different sentence at
each count that carries one ("Found by Joost de Winter in August 2026, working with
unspecified AI, ..."), so it is not a `Statement` either. A record whose reported side
is the catalogue's owes every AI statement of the entry it transcribes -- the current
capture's, or the earlier one's at a count pending intake -- quoted whole, and
`--check` holds it to that (`catalogue_owed`).
`devtools.generate_frontier_case` writes those quotations into the packing paragraph of
the records it drafts, which above `n = 100` is all of them; `--apply` does not write
them, so a hand-written record that comes to owe one fails `--check` until its author
places the sentence.

Usage, from `packing/`:

    uv run --frozen --all-extras --group dev python -m devtools.state_ai_assistance --check
    uv run --frozen --all-extras --group dev python -m devtools.state_ai_assistance --apply
    ... --below 68    only the records n < 68
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from strif import atomic_output_file

from devtools.check_source_coverage import COVERAGE, record_catalogue
from devtools.generate_frontier_case import ai_statements_from_credit, quoted_catalogue_sentence
from sqpack.kingbird_catalogue import parse_catalogue
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
RECORD = re.compile(r"^n-(\d{3})\.md$")

BIBLIOGRAPHY = ROOT / "resources" / "bibliography.yaml"


@dataclass(frozen=True, slots=True)
class Statement:
    """What one source says of AI assistance, and where a case record says it.

    `counts`, when given, are the only records that owe it: a source can say something
    of some of its packings alone, as Couzo did of his n = 102 and 103 ones.
    """

    keys: frozenset[str]
    anchor: re.Pattern[str]
    sentence: str
    marker: str
    counts: frozenset[int] | None = None


def load_statements(path: Path = BIBLIOGRAPHY) -> tuple[Statement, ...]:
    """Each statement the bibliography's `ai_assistance` fields make, with every key that
    makes it, in the order the bibliography first gives each.

    Keys whose fields agree in sentence, marker, anchor and counts share one `Statement`,
    as Hosono's seven releases share his README's sentence. A field whose anchor is no
    pattern is left out, so that importing this module cannot fail on the record it
    checks; `statement_problems` reports it.
    """
    grouped: dict[tuple[str, str, str, tuple[int, ...] | None], list[str]] = {}
    for source in safe_load(path.read_text(encoding="utf-8"))["sources"]:
        stated = source.get("ai_assistance")
        if not stated:
            continue
        try:
            re.compile(str(stated["anchor"]))
        except re.error:
            continue
        counts = tuple(sorted(stated["counts"])) if stated.get("counts") else None
        shape = (str(stated["sentence"]), str(stated["marker"]), str(stated["anchor"]), counts)
        grouped.setdefault(shape, []).append(str(source["key"]))
    return tuple(
        Statement(
            keys=frozenset(keys),
            anchor=re.compile(anchor),
            sentence=sentence,
            marker=marker,
            counts=frozenset(counts) if counts else None,
        )
        for (sentence, marker, anchor, counts), keys in grouped.items()
    )


def statement_problems(path: Path = BIBLIOGRAPHY) -> list[str]:
    """What is wrong with a bibliography `ai_assistance` field: an anchor that is not a
    regular expression, or a marker its own sentence lacks, which `--apply` would write
    into every record that owes it and `--check` would still call missing."""
    problems: list[str] = []
    for source in safe_load(path.read_text(encoding="utf-8"))["sources"]:
        stated = source.get("ai_assistance")
        if not stated:
            continue
        try:
            re.compile(str(stated["anchor"]))
        except re.error as error:
            problems.append(f"{source['key']}: ai_assistance.anchor is not a pattern: {error}")
        if str(stated["marker"]) not in str(stated["sentence"]):
            problems.append(f"{source['key']}: ai_assistance.sentence lacks its own marker")
    return problems


#: Every statement, read from the bibliography (think-j5so): until 23 October 2026 these
#: were a list here, and four keys cited by records were missing from it.
STATEMENTS: tuple[Statement, ...] = load_statements()


def statement_of(key: str, statements: Iterable[Statement] = STATEMENTS) -> Statement:
    """The one statement a bibliography key makes."""
    (found,) = [statement for statement in statements if key in statement.keys]
    return found


#: Hosono's statement, which `devtools.apply_wand125_rectangles` also writes into the
#: intake paragraph it owns, so that regenerating a record keeps the sentence this tool added.
WAND125 = statement_of("[wand125 rectangle bounds 2026]")


#: How a case record names the Kingbird catalogue as the source of its reported side.
CATALOGUE_KEY = "[Kingbird]"


class _CreditLined(Protocol):
    @property
    def credit_line(self) -> str | None: ...


def catalogue_owed(text: str, catalogue: Mapping[int, _CreditLined]) -> tuple[str, ...]:
    """The catalogue AI statements a record owes and does not make, as it would quote them."""
    front, lines = split_record(text)
    packing = safe_load(front).get("packing") or {}
    upper = packing.get("reported_upper_bound") or {}
    entry = catalogue.get(int(packing.get("n", 0)))
    if upper.get("source_key") != CATALOGUE_KEY or entry is None:
        return ()
    body = _comparable(" ".join(lines))
    quotations = (
        quoted_catalogue_sentence(sentence)
        for sentence in ai_statements_from_credit(entry.credit_line)
    )
    return tuple(quote for quote in quotations if _comparable(quote) not in body)


#: Quotation marks and apostrophes in either typography. The Markdown formatter curls a
#: straight quote it finds nested inside a quotation -- the catalogue's `with help from
#: "TheMagicAnimals"` at `n = 87` -- and an apostrophe or single quote the same way, so a
#: quotation is the same quotation whichever it has.
_QUOTES = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'"})


def _comparable(text: str) -> str:
    """Text as a quotation is matched: whitespace collapsed, quotes straightened."""
    return " ".join(text.split()).translate(_QUOTES)


def record_catalogue_entries() -> Mapping[int, _CreditLined]:
    """The catalogue entry each record transcribes, as `check_source_coverage` reads it."""
    pending = safe_load(COVERAGE.read_text(encoding="utf-8")).get(
        "pending_catalogue_intake", []
    )
    return record_catalogue(parse_catalogue(), pending)


@dataclass(frozen=True, slots=True)
class Paragraph:
    """A run of prose lines in a record's body, by its first and last line index."""

    first: int
    last: int
    text: str


def split_record(text: str) -> tuple[str, list[str]]:
    """The front matter and the body's lines of a case record."""
    _, front, body = text.split("---\n", 2)
    return front, body.split("\n")


def paragraphs(lines: Sequence[str]) -> list[Paragraph]:
    """The body's prose paragraphs: not headings, tables, comments or fenced code."""
    found: list[Paragraph] = []
    fenced = False
    start: int | None = None
    for index, line in enumerate([*lines, ""]):
        if line.startswith("```"):
            fenced = not fenced
        if fenced or line.startswith("```") or not line.strip():
            if start is not None:
                found.append(Paragraph(start, index - 1, " ".join(lines[start:index])))
                start = None
            continue
        if start is None:
            start = index
    return [
        paragraph
        for paragraph in found
        if not lines[paragraph.first].startswith(("#", "|", "<!--"))
    ]


def record_count(front: str) -> int | None:
    """The `n` a record's front matter names, or None for text that names none."""
    parsed = safe_load(front)
    packing = parsed.get("packing") if isinstance(parsed, Mapping) else None
    n = packing.get("n") if isinstance(packing, Mapping) else None
    return n if isinstance(n, int) else None


def owed(front: str, lines: Sequence[str]) -> list[tuple[Statement, Paragraph | None, bool]]:
    """Each statement the record's citations call for: its anchor paragraph, and whether said.

    The anchor is the first paragraph describing the source, or None where the body never
    does. A statement is said where any anchored paragraph carries its marker.
    """
    prose = paragraphs(lines)
    result: list[tuple[Statement, Paragraph | None, bool]] = []
    for statement in STATEMENTS:
        if not any(key in front for key in statement.keys):
            continue
        if statement.counts is not None and record_count(front) not in statement.counts:
            continue
        anchored = [paragraph for paragraph in prose if statement.anchor.search(paragraph.text)]
        said = any(statement.marker in paragraph.text for paragraph in anchored)
        result.append((statement, anchored[0] if anchored else None, said))
    return result


def state(text: str) -> str:
    """The record with every owed, unsaid statement appended to its anchor paragraph."""
    front, lines = split_record(text)
    insertions = sorted(
        (
            (paragraph.last, statement.sentence)
            for statement, paragraph, said in owed(front, lines)
            if paragraph is not None and not said
        ),
        reverse=True,
    )
    for last, sentence in insertions:
        lines.insert(last + 1, sentence)
    return text.split("---\n", 2)[0] + "---\n" + front + "---\n" + "\n".join(lines)


def records(below: int | None) -> list[Path]:
    """The case records, in `n` order, those under `below` where it is given."""
    found = []
    for path in sorted(FRONTIER.glob("n-*.md")):
        match = RECORD.match(path.name)
        if match and (below is None or int(match.group(1)) < below):
            found.append(path)
    return found


def report(
    paths: Iterable[Path], catalogue: Mapping[int, _CreditLined] | None = None
) -> tuple[list[str], list[str]]:
    """The statements still missing, and the ones no paragraph gives a place to."""
    missing: list[str] = []
    unanchored: list[str] = []
    entries = record_catalogue_entries() if catalogue is None else catalogue
    for path in paths:
        text = path.read_text(encoding="utf-8")
        missing.extend(
            f"{path.name}: {CATALOGUE_KEY} {quote}" for quote in catalogue_owed(text, entries)
        )
        front, lines = split_record(text)
        for statement, paragraph, said in owed(front, lines):
            cited = ", ".join(sorted(key for key in statement.keys if key in front))
            label = f"{path.name}: {cited}"
            if paragraph is None:
                unanchored.append(label)
            elif not said:
                missing.append(label)
    return missing, unanchored


def apply(paths: Iterable[Path]) -> list[str]:
    changed = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        stated = state(text)
        if stated != text:
            with atomic_output_file(path) as temporary:
                temporary.write_text(stated, encoding="utf-8")
            changed.append(path.name)
    return changed


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true", help="fail on a missing statement")
    group.add_argument("--apply", action="store_true", help="write the missing statements")
    parser.add_argument("--below", type=int, help="only the records n < BELOW")
    arguments = parser.parse_args(argv)
    paths = records(arguments.below)
    if arguments.apply:
        changed = apply(paths)
        print(f"stated AI assistance in {len(changed)} records: {', '.join(changed)}")
    missing, unanchored = report(paths)
    missing = [*statement_problems(), *missing]
    for label in unanchored:
        print(f"no paragraph describes the source, so nothing is owed: {label}")
    for label in missing:
        print(f"MISSING: {label}", file=sys.stderr)
    if missing:
        return 1
    print(f"every statement owed by {len(paths)} records is made")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
