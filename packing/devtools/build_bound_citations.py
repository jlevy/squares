#!/usr/bin/env python3
"""Derive the stage's citation lines from the frontier register and the bibliography.

Under its PROVEN values the stage names where each bound it shows comes from. It shows the
same two numbers `devtools.build_composite_figure_data` draws, so those are the two cited
here: the lower bound is the case's `verified_lower_bound`, what the register itself
certifies, and the upper bound is its `reported_upper_bound`, the best construction on
record. An upper bound the register has not certified is marked `reported`; only a
certified one is `verified`, and that is decided by the register's own rule,
`sqpack.assurance.bounds_agree_at_declared_precision`, so this record, the case checks and
the stage cannot disagree about which ceilings are proven.

**Every rule reads a typed field, never `n`.** Deciding from `n` what the record already
states is how `D-385` happened, and the same four questions recur for each bound:

1. *Is it derived?* A bound the register certifies with `common-knowledge` evidence alone
   -- the grid, the area bound, center counting, which the evidence schema describes as
   "nobody claims it and no citation is owed" -- has no line. For the upper bound that
   also needs the reported construction to be the certified one at the printed precision:
   a grid ceiling under a better reported packing is not what the stage shows.
2. *Is it this project's?* A first-party entry whose novelty the register scores as new is
   the same test that puts the star on the stage, and it cites this project with the one
   result in `frontier/results.yaml` that carries that evidence for this `n`. The year is
   the year the register dated the result's significance. For an upper bound only the
   construction's own evidence, `reported_upper_bound.evidence`, is asked: a new
   certificate of someone else's packing confirms it and does not make it ours, which is
   exactly `n = 29`, whose interval certificate `T-009` is scored new.
3. *Otherwise, whose is it?* A lower bound's previously-published entries must share one
   source key, and that key's authors, year and short venue come from
   `resources/bibliography.yaml`. Where the source's credit is joint with the work it
   builds on, the entry's `credit` is printed in place of the joined authors, and it, or
   where it is too wide its `short_credit`, must fit the line with its year and venue
   however the case uses it. An upper bound credits
   the case's own `found_by` and `improved_by`, with the venue of its `source_key`; where
   the register credits nobody, the line cites the source itself.
4. *What has this project recorded about it?* Every result for this `n` that carries one
   of the bound's own evidence entries is listed in `results`. Those that carry one this
   project performed -- a replay, an audit, an interval certificate -- confirm the
   external bound and are listed in `confirmed_by`. An upper certificate confirms the
   displayed report only when the verified lane agrees at its declared precision;
   certificates of earlier ceilings remain relevant results. A result that only cites
   the source's own proof is relevant and listed, and confirms nothing. The shared checker
   behind several first-party certificates is not the bound's own evidence, so a project line
   lists only the results that carry its novel entries, not every earlier rung that used
   the same checker.

The reference says where the bound comes from and nothing else. **Everything this project
has to say about it is one parenthesis at the end of the line, `note`**: `(reported)`
where the register has not certified the bound, `(confirmed T-009)` where a result of ours
checks it, `(reported; confirmed T-009)` where both are true. `note` is composed here
rather than at the stage, so one place spells these words and the width below counts them.

**Nothing is read from prose.** Where the structured record lacks a year or an author it is
left out, not recovered from a body sentence or a credit line: an improved construction's
line carries no year, because `found_year` dates the find and the schema has no field for
the improvement's date. `--review` lists every such case, and every omitted line with the
reason, so a gap is reported rather than filled.

**A lower bound is starred as a recent result** where it is recent (the owner,
2026-09-27): "we ultimately want these graphics and charts to be a full representation of
the current state of understanding ... and they should show recent changes to be new."
The star says when, not whose. A line credits case by case: another's work under its
authors, joint work that builds on this project as `credit` in the bibliography (`Kleddamag
after Levy, Mira, Guzhou0806`), and this project's sole work as `Squares Project (Levy)`.
Recent is a typed date, never a year or a source key read as text: this project's own new
bounds are recent by construction, and an external bound is recent where its source's
`dated` is on or after `RECENT_SINCE`. A source from that year that carries no date fails
the build, so a recent bound cannot go unstarred because its key happens not to name the
year, as n = 17's does not. The `recent` field is the lower citation's alone; the stage
stars no upper bound.

**A lower bound that corrects a published result says which** (the owner, 2026-10-02): it
is still new, and starred as any recent bound is, and it also carries `corrects`, the
published work it stands in for, so every surface can say "corrects Nagamochi 2005" beside
the star. It is read from the `corrects` field of the results that carry the bound, the
line's own `results`, never from a source key or a year: `check_results.corrects_problems`
holds that field to a bibliography source and to the register's record of that publication,
now V0. Two results behind one bound that name different corrected works fail the build
rather than one being chosen. This is not a correction to this project's own record, which
is a defect entry in `defects.yaml`; the tag names someone else's published work. The stage
sets it on the lower line, `corrects Nagamochi 2005` between the reference and the note, so
it counts toward the line's width like the note does.

A line must fit in `TEXT_LIMIT` characters, the width the stage sets it in, the reference
and its note together. Where it does not, the source's `short_venue` is used if the
bibliography gives one, and then its `short_credit`: the credit's authors and the first of
its links, ending in `et al.`, a shape `check_short_credit` holds so that a shortened line
can drop links from the end but never an author, and never misstate a link. The stage is
the only surface that shortens a credit; every other renderer prints it whole. A line that
still does not fit fails the build rather than being cut, `--review` names every line that
was shortened, and `--check` names every line a bibliography edit has moved.

Usage, from `packing/`:

    uv run --frozen --all-extras --group dev python -m devtools.build_bound_citations --update
    uv run --frozen --all-extras --group dev python -m devtools.build_bound_citations --check
    uv run --frozen --all-extras --group dev python -m devtools.build_bound_citations --review
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from sqpack import retained_json
from sqpack.assurance import bounds_agree_at_declared_precision
from sqpack.known_best import KNOWN_BEST_CORPUS
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
EVIDENCE = FRONTIER / "evidence.yaml"
RESULTS = FRONTIER / "results.yaml"
BIBLIOGRAPHY = ROOT / "resources" / "bibliography.yaml"
RECORD = ROOT / "atlas" / "known-best" / "bound-citations.json"
GENERATOR = "devtools.build_bound_citations"
CONTRACT = "packing.squares:BoundCitations/v1"
SCHEMA = "bound-citations.schema.yaml"

#: The cases this record carries, one entry each: the composite's corpus, so the two
#: records cover the same `n` by construction.
CORPUS = KNOWN_BEST_CORPUS

#: The widest line the stage sets, in characters: the reference and its note together,
#: which is what a reader sees on one line. The note used to sit outside this count, drawn
#: as a bare word after the reference, so a line could be checked as fitting and drawn as
#: not (`think-qzmf`).
TEXT_LIMIT = 66

#: The register's two words for a bound's standing. `VERIFIED` is one it certifies at the
#: printed precision; `REPORTED` is one it carries from a source without certifying.
VERIFIED = "verified"
REPORTED = "reported"

#: How a line credits this project's own bound: the project and its human author, as a
#: brief note does (the owner, 2026-09-27). The longest project line is well inside
#: `TEXT_LIMIT`, so the bare "Levy" the credit rules allow where room is short is not needed.
PROJECT_NAME = "Squares Project (Levy)"

#: The novelty the evidence schema gives the grid, area and center-counting bounds.
COMMON_KNOWLEDGE = "common-knowledge"

#: The novelty scores that make a first-party bound this project's. The same set
#: `build_composite_figure_data` stars, which the contract test holds it to.
NOVEL = frozenset({"apparently-novel", "confirmed-novel"})

#: Who performed an entry this project did itself: a replay, an audit, a certificate.
FIRST_PARTY = "repository"

#: The first day of a recent result: the day this project's square-packing work began
#: (`e5daa2d24`, the s(11) study, 2026-08-22). The repository is older, but its first six
#: weeks were research on other subjects, since moved to jlevy/thinking. A lower bound
#: whose source is dated on or after it is starred, whoever proved it.
RECENT_SINCE = date(2026, 8, 22)

#: What joins a credit's authors to the work they build on: `Daniel after Burns, Massaccesi`.
AFTER = " after "

#: What ends a shortened credit: the links it leaves out, as a citation says of authors.
ET_AL = "et al."

#: The word a correcting bound's tag starts with: `corrects Nagamochi 2005`.
CORRECTS = "corrects"


@dataclass(frozen=True, slots=True)
class Source:
    """One bibliography entry: what a citation of the source itself prints."""

    key: str
    authors: tuple[str, ...]
    year: int | None
    venue: str
    #: The venue a line falls back to when its confirmation would not otherwise fit.
    short_venue: str | None = None
    #: What a line prints in place of the joined authors, where the credit is joint with
    #: the lineage the source builds on: Kleddamag's n = 17 releases continue this
    #: project's, Mira's and Guzhou0806's methods, which the authors field has no place for
    #: (the owner, 2026-09-27). Last names, or handles where no name is published; human
    #: authors and projects only, since an AI agent is never a credited author.
    credit: str | None = None
    #: What the stage prints where the whole `credit` does not fit its line: the credit's
    #: authors and the first of its links, ending in `et al.` (`Tokoharu after Levy,
    #: wand125 et al.`). The stage's alone; every other renderer prints `credit` whole.
    #: `check_short_credit` holds it to that shape.
    short_credit: str | None = None
    #: The source's own date for the version cited, where the bibliography gives one.
    dated: date | None = None
    #: How the source stands to this project, where the bibliography types it:
    #: `builds-on-project`, `credits-project` or `independent`. Read by the recent
    #: rows (`devtools.render_recent_results`); no line here prints it.
    lineage: str | None = None

    @property
    def credited(self) -> str:
        """Who a citation of this source names: its `credit`, else its joined authors.

        Always the whole credit. The stage alone may fall back to `short_credit`, through
        `compose`, and only where the whole line does not fit.
        """
        return self.credit if self.credit is not None else join_authors(self.authors)


@dataclass(frozen=True, slots=True)
class Register:
    """The records every citation is derived from, loaded once per build."""

    evidence: Mapping[str, Mapping[str, Any]]
    results: Sequence[Mapping[str, Any]]
    sources: Mapping[str, Source]
    names: Mapping[str, str]


def load_register() -> Register:
    evidence = safe_load(EVIDENCE.read_text(encoding="utf-8"))["evidence"]
    results = safe_load(RESULTS.read_text(encoding="utf-8"))["results"]
    bibliography = safe_load(BIBLIOGRAPHY.read_text(encoding="utf-8"))
    sources = {
        str(entry["key"]): Source(
            key=str(entry["key"]),
            authors=tuple(str(author) for author in entry["authors"]),
            year=entry["year"],
            venue=str(entry["venue"]),
            short_venue=entry.get("short_venue"),
            credit=entry.get("credit"),
            short_credit=entry.get("short_credit"),
            dated=date.fromisoformat(entry["dated"]) if "dated" in entry else None,
            lineage=entry.get("lineage"),
        )
        for entry in bibliography["sources"]
    }
    check_credits(sources.values())
    check_dates(sources.values())
    return Register(
        evidence={str(entry["id"]): entry for entry in evidence},
        results=results,
        sources=sources,
        names={
            str(name): str(surname) for name, surname in bibliography["credited_names"].items()
        },
    )


def credit_parts(credit: str) -> tuple[str, list[str]]:
    """A credit's authors and its links, in order: `A, B after C, D` is `A, B` and C, D."""
    authors, after, links = credit.partition(AFTER)
    return authors, links.split(", ") if after else []


def short_credits(credit: str) -> list[str]:
    """Every shortening the stage may print for `credit`, longest first.

    The credit's authors whole, then `after` and a proper prefix of its links, at least
    one, then `et al.`: `Tokoharu after Levy, wand125 et al.` for `Tokoharu after Levy,
    wand125, Stromquist, Nagamochi, Burns, Massaccesi`. A shortened line therefore keeps
    every author, names each link it keeps in the place the credit names it, and says that
    links follow. A credit with one link or none has no shortening: `A et al.` would read
    as coauthors.
    """
    authors, links = credit_parts(credit)
    return [
        f"{authors}{AFTER}{', '.join(links[:kept])} {ET_AL}"
        for kept in range(len(links) - 1, 0, -1)
    ]


def check_short_credit(source: Source) -> None:
    """Fail on a `short_credit` that is not one of its credit's `short_credits`.

    Held here rather than trusted to whoever writes the bibliography, because the stage
    prints the short form in the credit's place: one that dropped an author, or named a
    link out of order or not at all in the credit, would misstate the credit on the one
    surface a reader cannot check against the full line.
    """
    if source.short_credit is None:
        return
    if source.credit is None:
        raise ValueError(f"{source.key}: `short_credit` shortens a `credit` it does not have")
    allowed = short_credits(source.credit)
    if source.short_credit not in allowed:
        raise ValueError(
            f"{source.key}: `short_credit` {source.short_credit!r} is not the credit's "
            f"authors and a prefix of its links ending in {ET_AL!r}; it may be one of "
            f"{allowed}"
        )


def check_credits(sources: Iterable[Source]) -> None:
    """Fail on a `credit` whose line, `credit year, venue`, would not fit the stage.

    The whole credit, or where that is too wide its `short_credit`, must fit. Checked for
    every credited source, not only the ones a case cites today, so a joint credit is known
    to fit before a bound first carries it. The note is left out: it is this project's to
    shorten, through `short_venue` and `short_credit`, and `_checked` still counts it.
    """
    for source in sources:
        check_short_credit(source)
        if source.credit is None:
            continue
        line = cite(source.credit, source.year, source.venue)
        if len(line) <= TEXT_LIMIT:
            continue
        if source.short_credit is None:
            raise ValueError(
                f"{source.key}: credit line {line!r} is {len(line)} characters, "
                f"over {TEXT_LIMIT}, and the source gives no `short_credit`"
            )
        short = cite(source.short_credit, source.year, source.venue)
        if len(short) > TEXT_LIMIT:
            raise ValueError(
                f"{source.key}: short credit line {short!r} is {len(short)} characters, "
                f"over {TEXT_LIMIT}"
            )


def check_dates(sources: Iterable[Source]) -> None:
    """Fail on a source from the year recent results begin that does not say its date.

    Without the date the star cannot be decided, and deciding it from the year would star a
    source from before `RECENT_SINCE` as readily as one after it.
    """
    for source in sources:
        if source.dated is None and (source.year or 0) >= RECENT_SINCE.year:
            raise ValueError(
                f"{source.key}: a {source.year} source needs `dated`, the date of the "
                f"version cited, to decide whether its bounds are recent"
            )


def is_recent(source: Source) -> bool:
    """Whether a bound this source establishes is a recent result."""
    return source.dated is not None and source.dated >= RECENT_SINCE


def record_name(n: int) -> str:
    """The frontier case record a line comes from, as its file stem."""
    return f"n-{n:03d}"


def load_case(n: int) -> dict[str, Any]:
    text = (FRONTIER / f"{record_name(n)}.md").read_text(encoding="utf-8")
    return safe_load(text.split("---", 2)[1])["packing"]


def join_authors(surnames: Sequence[str]) -> str:
    """One name, two joined by an ampersand, three or more as the first and et al."""
    if not surnames:
        raise ValueError("a citation needs at least one author")
    if len(surnames) == 1:
        return surnames[0]
    if len(surnames) == 2:
        return f"{surnames[0]} & {surnames[1]}"
    return f"{surnames[0]} et al."


def cite(authors: str | None, year: int | None, venue: str) -> str:
    """`Authors Year, venue`, leaving out whichever of the first two is missing."""
    head = short_cite(authors, year)
    return f"{head}, {venue}" if head else venue


def short_cite(authors: str | None, year: int | None) -> str:
    """`Authors Year`, a citation's head without its venue: `Nagamochi 2005`."""
    return " ".join(part for part in (authors, None if year is None else str(year)) if part)


def note(assurance: str, confirmed_by: Sequence[str]) -> str | None:
    """What this project has to say about the bound, or None where it is nothing.

    One parenthesis at the end of the line, in one vocabulary, holding both of the things
    that were said in two shapes before: the register's standing on the bound, and this
    project's own confirming results. The stage drew `reported` as a bare word after the
    reference and baked `(confirmed, T-009)` into the reference itself, so at `n = 29`,
    the one case that is both, the line read "Squares in Squares (confirmed, T-009)
    reported" -- two annotations of one bound, formatted two ways, saying what looks like
    two contradictory things (the owner, 2026-09-22).

    They do not contradict. `reported` is the register's: it carries this construction's
    value from the catalogue and has not certified it at the printed precision. The
    confirmation is ours: a result of this project's that checks the same bound.
    A certificate of a different ceiling does not confirm the displayed report.
    The semicolon separates the two statements, so the comma is left to separate results.
    """
    said = []
    if assurance == REPORTED:
        said.append(REPORTED)
    if confirmed_by:
        said.append(f"confirmed {', '.join(confirmed_by)}")
    return f"({'; '.join(said)})" if said else None


def compose(
    authors: str | None,
    year: int | None,
    source: Source,
    room: int,
    short_authors: str | None = None,
) -> str:
    """The reference alone: authors, year and venue, with nothing of this project's in it.

    The first form that fits the `room` the note leaves: the whole credit with the source's
    full venue, then with its short venue, then the `short_authors` with each venue in
    turn. Who did the work outranks where it appeared, so a venue gives way before a credit
    does, and where no form with a venue fits, the venue goes before the line fails: the
    credit and year alone, whole and then short. `n = k^2 - 1`'s lower line is the case,
    Karakuş's bound confirmed by two results and correcting Nagamochi's (2026-10-06).
    Where no form fits, the narrowest is returned and the caller fails it.
    """
    who = [authors] if short_authors is None else [authors, short_authors]
    where = [source.venue] if source.short_venue is None else [source.venue, source.short_venue]
    forms = [cite(name, year, venue) for name in who for venue in where]
    forms += [head for name in who if (head := short_cite(name, year))]
    return next((text for text in forms if len(text) <= room), forms[-1])


def credit(
    reported: Mapping[str, Any], names: Mapping[str, str]
) -> tuple[str | None, int | None]:
    """Who the reported construction is credited to, and the year that credit is dated.

    Finders first, then any improver not already among them: the printed side is the last
    improvement's, and the lineage is what built it. The year is `found_year` only where
    nothing improved the packing since, because it dates the find and the schema carries
    no date for an improvement; an improved line leaves the year out rather than print one
    that belongs to an earlier side.
    """
    finders = [str(name) for name in reported.get("found_by") or []]
    improvers = [str(name) for name in reported.get("improved_by") or []]
    lineage = finders + [name for name in dict.fromkeys(improvers) if name not in finders]
    if not lineage:
        return None, None
    missing = [name for name in lineage if name not in names]
    if missing:
        raise ValueError(f"credited names missing from {BIBLIOGRAPHY.name}: {missing}")
    year = None if improvers else reported.get("found_year")
    return join_authors([names[name] for name in lineage]), year


def in_scope(scope: Mapping[str, Any], n: int) -> bool:
    if "n_values" in scope:
        return n in scope["n_values"]
    return int(scope["n_min"]) <= n <= int(scope["n_max"])


def result_order(result_id: str) -> int:
    """`T-032` sorts as 32, so `T-100` will follow `T-099` rather than `T-010`."""
    return int(result_id.split("-", 1)[1])


def is_novel_first_party(entry: Mapping[str, Any], claim: str) -> bool:
    """The star's test: this project's bound, scored new by the register."""
    return (
        entry.get("claim") == claim
        and entry.get("performed_by") == FIRST_PARTY
        and entry.get("novelty") in NOVEL
    )


def results_carrying(
    n: int, evidence_ids: Iterable[str], results: Sequence[Mapping[str, Any]]
) -> list[str]:
    """The results for this `n` that carry any of these evidence ids, in id order."""
    wanted = set(evidence_ids)
    return sorted(
        (
            str(result["id"])
            for result in results
            if in_scope(result["scope"], n) and wanted & set(result.get("evidence") or [])
        ),
        key=result_order,
    )


def project_result(
    n: int, novel: Sequence[str], results: Sequence[Mapping[str, Any]]
) -> Mapping[str, Any]:
    """The one result that carries every novel entry behind this bound, for this `n`.

    Exactly one or the build fails: two would make the line's result id a choice, and none
    would mean a first-party bound the results register has not recorded.
    """
    matches = [
        result
        for result in results
        if set(novel) <= set(result.get("evidence") or []) and in_scope(result["scope"], n)
    ]
    if len(matches) != 1:
        found = [str(result["id"]) for result in matches]
        raise ValueError(f"n={n}: novel evidence {list(novel)} is carried by results {found}")
    return matches[0]


def own_evidence(ids: Iterable[str], register: Register) -> list[str]:
    """The entries that are this bound's own, rather than the grid or area bound."""
    return [
        item
        for item in dict.fromkeys(str(item) for item in ids)
        if register.evidence[item].get("novelty") != COMMON_KNOWLEDGE
    ]


def corrects_tag(corrects: Mapping[str, Any] | None) -> str | None:
    """The tag a correcting bound carries, `corrects Nagamochi 2005`, or None."""
    return None if corrects is None else f"{CORRECTS} {corrects['credit']}"


def drawn(citation: Mapping[str, Any]) -> str:
    """The line as the stage sets it: the reference, the published work a lower bound
    corrects where it corrects one, then its note where there is one."""
    parts = (citation["text"], corrects_tag(citation.get("corrects")), citation["note"])
    return " ".join(part for part in parts if part)


def correction(n: int, results: Sequence[str], register: Register) -> dict[str, str] | None:
    """The published work a lower bound corrects, from the results that carry it, or None.

    Each result's `corrects` names the corrected work's bibliography key and the register's
    record of it; the line repeats both, with the work's short citation as the bibliography
    prints it (`Nagamochi 2005`), which is what a page writes after "corrects". Two results
    naming different works fail the build: the tag names one publication, and choosing
    between two would be the record's call, not this tool's.
    """
    by_id = {str(result["id"]): result for result in register.results}
    named = {
        (str(corrects["source_key"]), str(corrects["result"]))
        for result_id in results
        if (corrects := by_id[result_id].get("corrects"))
    }
    if not named:
        return None
    if len(named) > 1:
        raise ValueError(
            f"n={n} lower: results {list(results)} correct {len(named)} published works, "
            f"{sorted(named)}, not one"
        )
    ((key, result),) = named
    source = _source(key, register, f"n={n} lower corrects")
    return {
        "source_key": key,
        "credit": short_cite(source.credited, source.year),
        "result": result,
    }


def _checked(n: int, label: str, citation: dict[str, Any]) -> dict[str, Any]:
    line = drawn(citation)
    if len(line) > TEXT_LIMIT:
        raise ValueError(
            f"n={n} {label}: {line!r} is {len(line)} characters, over {TEXT_LIMIT}"
        )
    return citation


def _lower_fields(
    n: int, results: Sequence[str], register: Register, *, recent: bool | None
) -> dict[str, Any]:
    """What a lower line carries that an upper one does not: whether it is recent, and the
    published work it corrects. Nothing where `recent` is None, which is an upper line."""
    if recent is None:
        return {}
    return {"corrects": correction(n, results, register), "recent": recent}


def _project(
    n: int,
    label: str,
    novel: Sequence[str],
    *,
    value: str,
    assurance: str,
    register: Register,
    recent: bool | None = None,
) -> dict[str, Any]:
    """This project's line. `recent` is given for a lower line alone, which then also
    carries what it corrects (`_lower_fields`)."""
    result = project_result(n, novel, register.results)
    year = int(str(result["significance"]["scored"])[:4])
    results = results_carrying(n, novel, register.results)
    return _checked(
        n,
        label,
        {
            "text": f"{PROJECT_NAME} {year}, result {result['id']}",
            "note": note(assurance, []),
            "basis": "project",
            "assurance": assurance,
            "source_key": None,
            "result": str(result["id"]),
            "results": results,
            "confirmed_by": [],
            "value": value,
            **_lower_fields(n, results, register, recent=recent),
        },
    )


def _source(key: str | None, register: Register, where: str) -> Source:
    if key is None:
        raise ValueError(f"{where}: no source key to cite")
    if key not in register.sources:
        raise ValueError(f"{where}: {key} is not in {BIBLIOGRAPHY.name}")
    return register.sources[key]


def _external(
    n: int,
    label: str,
    *,
    source: Source,
    credited: tuple[str | None, int | None],
    own: Sequence[str],
    value: str,
    assurance: str,
    register: Register,
    short_credit: str | None = None,
    recent: bool | None = None,
    confirming: Sequence[str] | None = None,
) -> dict[str, Any]:
    """An external source's line, and what this project has recorded about the bound.

    `short_credit` is the shortening of `credited`'s names the line may fall back to, which
    only a line that credits the source's own `credit` has. `recent` is given for a lower
    line alone, which then also carries what it corrects, and the reference gives way to
    that tag as it does to the note. `confirming` limits confirmation to evidence about
    the displayed value while `own` preserves all relevant result links.
    """
    performed = [
        item
        for item in (own if confirming is None else confirming)
        if register.evidence[item].get("performed_by") == FIRST_PARTY
    ]
    confirmed_by = results_carrying(n, performed, register.results)
    results = results_carrying(n, own, register.results)
    lower = _lower_fields(n, results, register, recent=recent)
    authors, year = credited
    said = note(assurance, confirmed_by)
    asides = [part for part in (corrects_tag(lower.get("corrects")), said) if part]
    room = TEXT_LIMIT - sum(len(part) + 1 for part in asides)
    return _checked(
        n,
        label,
        {
            "text": compose(authors, year, source, room, short_credit),
            "note": said,
            "basis": "external",
            "assurance": assurance,
            "source_key": source.key,
            "result": None,
            "results": results,
            "confirmed_by": confirmed_by,
            "value": value,
            **lower,
        },
    )


@dataclass(frozen=True, slots=True)
class LowerOrigin:
    """Whose a lower bound is, read from its own evidence, and so whether it is recent.

    Either this project's (`novel` names the first-party entries the register scores new,
    and `source` is None) or one external source's. The star's test lives here once, so
    the stage's line and the site's recent rows, which ask it of the reported
    lane as well as the verified one, cannot disagree about which bounds are new.
    """

    own: tuple[str, ...]
    novel: tuple[str, ...]
    source: Source | None

    @property
    def recent(self) -> bool:
        # This project's own new bounds are recent by construction: its work began on
        # RECENT_SINCE.
        return self.source is None or is_recent(self.source)


def lower_origin(
    n: int, bound: Mapping[str, Any], register: Register, label: str = "lower"
) -> LowerOrigin | None:
    """Where a lower bound, of either lane, comes from; None where it is derived."""
    own = own_evidence(bound["evidence"], register)
    if not own:
        return None
    novel = [
        item for item in own if is_novel_first_party(register.evidence[item], "lower-bound")
    ]
    if novel:
        return LowerOrigin(own=tuple(own), novel=tuple(novel), source=None)
    # A replay of a published bound is still that source's bound; the entries this project
    # performed but did not originate carry the source's key like the author's own do.
    keys = {register.evidence[item].get("source_key") for item in own}
    if len(keys) == 1:
        source = _source(keys.pop(), register, f"n={n} {label}")
        return LowerOrigin(own=tuple(own), novel=(), source=source)
    return LowerOrigin(own=tuple(own), novel=(), source=first_source(n, own, register, label))


def first_source(
    n: int, own: Sequence[str], register: Register, label: str = "lower"
) -> Source:
    """The source whose own proof a bound's lane cites, where the lane names several.

    A value proved by one source and proved again by a later one, whose replay here the
    lane cites beside the first proof, is still the first source's result: the line
    credits it, and names the results that carry the replays as confirming it. Bentz
    proved s(13) = 4 in 2010 and s(33) = 6 in 2016; Evan Daniel's case-free cover of
    [0,4]^2 (T-006) and his s(k^2 - 3) = k family (T-064) prove them again, and since
    2026-10-06 their replays here sit in those lanes beside Bentz's proofs, which nobody
    here had replayed. Until then a lane named exactly one source.

    So the one source credited is the one whose author's own entry the lane cites; the
    entries this project performed from other sources confirm it. Two published sources
    behind one bound, or replays of two sources and no published proof, still fail: the
    credit would then be this tool's choice."""
    authored = {
        register.evidence[item].get("source_key")
        for item in own
        if register.evidence[item].get("performed_by") != FIRST_PARTY
    }
    if len(authored) != 1:
        keys = {register.evidence[item].get("source_key") for item in own}
        raise ValueError(
            f"n={n} {label}: evidence {list(own)} names {len(keys)} sources, not one"
        )
    return _source(authored.pop(), register, f"n={n} {label}")


def lower_citation(
    n: int, case: Mapping[str, Any], register: Register
) -> dict[str, Any] | None:
    """The line for the certified lower bound, or None where it is derived."""
    bound = case["verified_lower_bound"]
    origin = lower_origin(n, bound, register)
    if origin is None:
        return None
    value = str(bound["value"])
    if origin.source is None:
        return _project(
            n,
            "lower",
            origin.novel,
            value=value,
            assurance="verified",
            register=register,
            recent=origin.recent,
        )
    source = origin.source
    return _external(
        n,
        "lower",
        source=source,
        credited=(source.credited, source.year),
        own=origin.own,
        value=value,
        assurance="verified",
        register=register,
        short_credit=source.short_credit,
        recent=origin.recent,
    )


def upper_citation(
    n: int, case: Mapping[str, Any], register: Register
) -> dict[str, Any] | None:
    """The line for the reported upper bound, or None where it is the certified grid."""
    reported = case["reported_upper_bound"]
    verified = case["verified_upper_bound"]
    certified = bounds_agree_at_declared_precision(reported, verified)
    certificate = own_evidence(verified["evidence"], register)
    if certified and not certificate:
        return None
    value = str(reported["value"])
    assurance = VERIFIED if certified else REPORTED
    construction = own_evidence(reported["evidence"], register)
    novel = [
        item
        for item in construction
        if is_novel_first_party(register.evidence[item], "upper-bound")
    ]
    if novel:
        return _project(n, "upper", novel, value=value, assurance=assurance, register=register)
    source = _source(reported.get("source_key"), register, f"n={n} upper")
    names, year = credit(reported, register.names)
    return _external(
        n,
        "upper",
        source=source,
        credited=(names, year) if names else (source.credited, source.year),
        own=own_evidence([*construction, *certificate], register),
        value=value,
        assurance=assurance,
        register=register,
        # The register's finders are not the source's credit, so they have no shortening.
        short_credit=None if names else source.short_credit,
        confirming=own_evidence([*construction, *(certificate if certified else [])], register),
    )


def build_entry(n: int, case: Mapping[str, Any], register: Register) -> dict[str, Any]:
    return {
        "n": n,
        "record": record_name(n),
        "upper": upper_citation(n, case, register),
        "lower": lower_citation(n, case, register),
    }


def build_record() -> dict[str, Any]:
    register = load_register()
    return {
        "softschema": {
            "contract": CONTRACT,
            "schema": SCHEMA,
            "envelope": "citations",
            "status": "enforced",
        },
        "citations": {
            "generated_by": GENERATOR,
            "entries": [build_entry(n, load_case(n), register) for n in CORPUS.numbers],
        },
    }


def lower_citations() -> dict[int, dict[str, Any] | None]:
    """Every case's lower line, built afresh from the register: what the record will say."""
    register = load_register()
    return {n: lower_citation(n, load_case(n), register) for n in CORPUS.numbers}


def recent_lower_bounds() -> frozenset[int]:
    """The cases whose lower bound is a recent result: what the stage and the atlas star.

    `build_composite_figure_data` reads its star from here rather than deciding it again,
    so the two records cannot disagree about which bounds are new.
    """
    return frozenset(
        n for n, citation in lower_citations().items() if citation and citation["recent"]
    )


def corrected_lower_bounds() -> dict[int, dict[str, str]]:
    """The cases whose lower bound corrects a published result, with the work it corrects.

    `build_composite_figure_data` counts these beside the starred cases, from here, so the
    figure's count and the lines' tags are one decision.
    """
    return {
        n: citation["corrects"]
        for n, citation in lower_citations().items()
        if citation and citation["corrects"]
    }


def load_record() -> dict[str, Any]:
    """The citation data, as committed."""
    return json.loads(RECORD.read_text(encoding="utf-8"))["citations"]


def _text(record: Mapping[str, Any]) -> str:
    return retained_json.dumps(record, sort_keys=True, ensure_ascii=False)


def update() -> None:
    content = _text(build_record())
    if RECORD.is_file() and RECORD.read_text(encoding="utf-8") == content:
        print(f"bound citations already current: {RECORD.name}")
        return
    with atomic_output_file(RECORD, make_parents=True) as temporary:
        temporary.write_text(content, encoding="utf-8")
    print(f"bound citations updated: {RECORD.name}")


def stale_lines(committed: Mapping[str, Any], built: Mapping[str, Any]) -> list[str]:
    """Each line the committed record states differently from a fresh build, as drawn.

    A bibliography edit moves stage lines that are rendered into the atlas, and the
    atlas is re-rendered once for many edits; this names the lines that re-render will
    change, so the check says which rather than only that some did.
    """
    before = {entry["n"]: entry for entry in committed["entries"]}
    after = {entry["n"]: entry for entry in built["entries"]}
    found: list[str] = []
    for n in sorted(before.keys() | after.keys()):
        for label in ("upper", "lower"):
            old = (before.get(n) or {}).get(label)
            new = (after.get(n) or {}).get(label)
            if old == new:
                continue
            shown = [None if line is None else drawn(line) for line in (old, new)]
            if shown[0] == shown[1]:
                fields = sorted(
                    key
                    for key in (old or {}).keys() | (new or {}).keys()
                    if (old or {}).get(key) != (new or {}).get(key)
                )
                found.append(f"n={n} {label}: {shown[0]!r}, fields {fields} changed")
            else:
                found.append(f"n={n} {label}: {shown[0]!r} -> {shown[1]!r}")
    return found


def check() -> None:
    if not RECORD.is_file():
        raise ValueError(f"missing {RECORD.relative_to(ROOT)}; run with --update")
    built = build_record()
    if RECORD.read_text(encoding="utf-8") != _text(built):
        lines = stale_lines(load_record(), built["citations"])
        listed = "".join(f"\n  {line}" for line in lines)
        raise ValueError(f"stale {RECORD.relative_to(ROOT)}; re-run with --update{listed}")
    print("bound citations check passed: matches the frontier register and bibliography")


def coverage(entries: Sequence[Mapping[str, Any]]) -> dict[str, Counter[str]]:
    """Each bound's lines by basis and assurance, with `none` for an omitted line."""
    tally: dict[str, Counter[str]] = {"upper": Counter(), "lower": Counter()}
    for entry in entries:
        for label, counts in tally.items():
            citation = entry[label]
            counts[
                "none" if citation is None else f"{citation['basis']} {citation['assurance']}"
            ] += 1
    return tally


def omissions(
    entries: Sequence[Mapping[str, Any]], cases: Mapping[int, Mapping[str, Any]]
) -> dict[str, list[int]]:
    """Every `n` where a line, or a part of one, was left out, by the reason for it."""

    def credited(n: int, field: str) -> bool:
        return bool(cases[n]["reported_upper_bound"].get(field))

    external_upper = [
        e["n"] for e in entries if e["upper"] is not None and e["upper"]["basis"] == "external"
    ]
    return {
        "upper omitted: the certified grid": [e["n"] for e in entries if e["upper"] is None],
        "upper credits nobody, so the line cites the source without author or year": [
            n
            for n in external_upper
            if not credited(n, "found_by") and not credited(n, "improved_by")
        ],
        "upper improved since found, so the year is left out": [
            n for n in external_upper if credited(n, "improved_by")
        ],
        "upper reported and not certified": [
            e["n"]
            for e in entries
            if e["upper"] is not None and e["upper"]["assurance"] == REPORTED
        ],
        "lower omitted: common-knowledge evidence alone": [
            e["n"] for e in entries if e["lower"] is None
        ],
    }


def linked_results(entries: Sequence[Mapping[str, Any]]) -> dict[str, dict[int, list[str]]]:
    """Which lines this project's results confirm, and which they are only relevant to."""
    links: dict[str, dict[int, list[str]]] = {}
    for entry in entries:
        for label in ("upper", "lower"):
            line = entry[label]
            if line is None:
                continue
            confirming = line["confirmed_by"]
            other = [item for item in line["results"] if item not in confirming]
            if line["basis"] == "project":
                links.setdefault(f"{label} established by", {})[entry["n"]] = line["results"]
            else:
                if confirming:
                    links.setdefault(f"{label} confirmed by", {})[entry["n"]] = confirming
                if other:
                    links.setdefault(f"{label} relevant, not confirming", {})[entry["n"]] = (
                        other
                    )
    return links


def shortened(entries: Sequence[Mapping[str, Any]], register: Register) -> list[str]:
    """The lines set in their source's short venue or short credit, so they would fit."""
    found: list[str] = []
    for entry in entries:
        for label in ("upper", "lower"):
            line = entry[label]
            if line is None or line["source_key"] is None:
                continue
            source = register.sources[line["source_key"]]
            where = f"n={entry['n']} {label}: {line['text']!r}"
            if source.venue not in line["text"]:
                found.append(f"to the source's short venue: {where}")
            if source.short_credit is not None and line["text"].startswith(
                f"{source.short_credit} "
            ):
                found.append(f"to the source's short credit: {where}")
    return found


def review() -> None:
    """Report what every line cites and every place a line or a year was left out."""
    register = load_register()
    cases = {n: load_case(n) for n in CORPUS.numbers}
    entries = [build_entry(n, cases[n], register) for n in CORPUS.numbers]
    for label, counts in coverage(entries).items():
        tallies = ", ".join(f"{key} {value}" for key, value in sorted(counts.items()))
        print(f"{label}: {tallies}")
    print()
    for reason, numbers in omissions(entries, cases).items():
        print(f"{reason} ({len(numbers)}): n = {numbers}")
    print()
    cited: dict[str, list[int]] = {}
    for entry in entries:
        if entry["lower"] is not None:
            key = entry["lower"]["source_key"] or entry["lower"]["result"]
            cited.setdefault(key, []).append(entry["n"])
    for key, numbers in sorted(cited.items(), key=lambda item: (-len(item[1]), item[0])):
        shown = "" if len(numbers) > 12 else f": n = {numbers}"
        print(f"lower cites {key} ({len(numbers)}){shown}")
    recent = [entry["n"] for entry in entries if entry["lower"] and entry["lower"]["recent"]]
    print(f"lower recent, since {RECENT_SINCE.isoformat()} ({len(recent)}): n = {recent}")
    corrected: dict[tuple[str, str], list[int]] = {}
    for entry in entries:
        if entry["lower"] and (corrects := entry["lower"]["corrects"]):
            key = (corrects["source_key"], corrects["result"])
            corrected.setdefault(key, []).append(entry["n"])
    for (key, result), numbers in sorted(corrected.items()):
        unstarred = [n for n in numbers if n not in recent]
        print(
            f"lower corrects {key} ({result}) ({len(numbers)}), of them not recent "
            f"{unstarred}: n = {numbers[0]}..{numbers[-1]}"
        )
    print()
    for kind, by_n in linked_results(entries).items():
        grouped: dict[tuple[str, ...], list[int]] = {}
        for n, ids in by_n.items():
            grouped.setdefault(tuple(ids), []).append(n)
        for ids, numbers in grouped.items():
            span = (
                f"n = {numbers[0]}..{numbers[-1]} ({len(numbers)})"
                if len(numbers) > 12
                else f"n = {numbers}"
            )
            print(f"{kind} {', '.join(ids)}: {span}")
    for line in shortened(entries, register):
        print(f"shortened {line}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--update", action="store_true", help="write the record")
    group.add_argument("--check", action="store_true", help="fail if the record is stale")
    group.add_argument("--review", action="store_true", help="report coverage and omissions")
    arguments = parser.parse_args(argv)
    try:
        if arguments.update:
            update()
        elif arguments.check:
            check()
        else:
            review()
    except (OSError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
