"""The front of a paper, which every paper takes from one place.

A paper opens the same way on the site whichever paper it is: the formats row, three
chips offering the Markdown it is rendered from, its typeset PDF and the project on
GitHub; then the title; then the credits, in the owner's form (2026-10-01), and under
them the series strip (the series plan, 2026-10-05):

    From the original proof by **Queuingtheorydotcom**
    github.com/Queuingtheorydotcom/11SquaresOptimal

    Human oversight: **Joshua Levy**
    Agents: **GPT-6 Astra** and **GPT-6 Sol**
    Draft v0.1.5 (version history)
    Original proof September 29, 2026 · Last revised October 4, 2026

    Part III of 3 in the n = 11 series
    Part I: New Lower Bounds for Square Packing for n = 11
    Part II: A Review of the Certified Lower Bound s(11) > 31/8 for 11 Squares

Names in bold, addresses as plain links, the version plain, a line's space before a
paper's own credits when it explains someone else's work, a line's space before the
dates, and another before the series strip. A paper without a source begins at its own
credits. The version is the paper's own, not the site's (`sqpack.release`, the papers'
own versions), and the version line links the paper's version history where it has one,
which is where each paper's own editions are listed; a paper at its first version has
no history to link. The strip says which part of the series the paper is and names the
other parts by their titles, each linking its paper: page-relative on the page, which
works on the site and in a local preview, and by the site's address in the Markdown
edition, which is read away from the site (`devtools.paper_links` fills a link from one
paper to another the same way). It is written from the site's one list of papers
(`render_overview.PAPERS`), so a paper is named the same way on every other paper's
front.

Each paper describes itself as a `PaperFront`, a small record of the values that differ
between the papers, and everything the reader sees at the top of each page, in its
Markdown edition and in the head its PDF takes its title from, is written from that
record here. The renderers used to carry their own copies of this block, one in an
article and one in a shell, and they drifted: a bold address on one paper and a plain
one on the other, the version before the dates on one and after on the other, chips
rendered by KPress on one and written raw on the other (think-2cqu).
`devtools.paper_structure` measures each rendered paper against the first, and
`tests/test_paper_structure.py` holds them together.
"""

from __future__ import annotations

import re
from datetime import datetime
from html import escape
from typing import NamedTuple

from devtools import render_overview
from devtools.repo_links import REPO_URL

#: The placeholder an article carries where its front goes, exactly once.
FRONT_MATTER = "FRONT_MATTER"
#: The label of the date every paper ends its dates line with: when its own text last
#: changed, which `devtools.artifact_dates` holds to the article's last commit.
REVISED = "Last revised"
#: The GitHub mark on the third chip, drawn in the chip's own colour.
GITHUB_MARK = (
    '<svg viewBox="0 0 16 16" width="15" height="15" aria-hidden="true">'
    '<path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07'
    ".55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82"
    "-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52"
    ".28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08"
    "-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2"
    "-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25"
    ".54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42"
    '-3.58-8-8-8Z"/></svg>'
)
_LONG_DATE = "%B %d, %Y"
_ANCHOR_ID = re.compile(r"[a-z][a-z0-9-]*")


class Person(NamedTuple):
    """Someone credited by name, with the address the name links."""

    name: str
    url: str


class Source(NamedTuple):
    """The work a paper explains, when it is someone else's: credited first, by its
    author's name in bold and then its address as a plain link."""

    author: str
    address: str
    lead: str = "From the original proof by"


class Dated(NamedTuple):
    """One part of the dates line: what happened, and the day it did, written as the
    papers write a day (`October 1, 2026`)."""

    label: str
    day: str


class Part(NamedTuple):
    """One part of a series, as the series strip names it: its number, its slug, which
    its link is written from, and its title in plain text."""

    number: int
    slug: str
    title: str


class Series(NamedTuple):
    """The series a paper is part of: the series' name, as the strip writes it after
    "Part N of M in", its parts in reading order, and the number of this paper's part."""

    name: str
    parts: tuple[Part, ...]
    part: int


#: What the series strip calls the site's series of papers on n = 11.
SERIES_NAME = "the n = 11 series"
#: The numerals a part is numbered with, as the series plan and the papers' cards write
#: them.
_NUMERALS = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X")


def numeral(number: int) -> str:
    """A part's number as the strip writes it: `II` for 2."""
    if not 1 <= number <= len(_NUMERALS):
        raise ValueError(f"no numeral is written for part {number}")
    return _NUMERALS[number - 1]


def series(slug: str) -> Series:
    """The series strip of the site's paper `slug`, from the site's one list of papers
    (`render_overview.PAPERS`): the entries with a part number, in reading order."""
    part = render_overview.paper_record(slug).part
    if part is None:
        raise ValueError(f"{slug}: this standalone paper belongs to no series")
    return Series(
        SERIES_NAME,
        tuple(
            Part(paper.part, paper.slug, paper.title)
            for paper in render_overview.PAPERS
            if paper.part is not None
        ),
        part,
    )


class PaperFront(NamedTuple):
    """What differs between the papers at the top of the page: the record each renderer
    writes its front from."""

    slug: str
    """Names the page, its Markdown and its PDF, which the formats row links."""
    title: str
    """The title as the article's `h1` writes it; the explainer's carries its one
    formula as the page's own math span."""
    oversight: tuple[Person, ...]
    agents: tuple[str, ...]
    version: str
    """The version line, plain: the paper's own version from `sqpack.release`
    (`EXPLAINER_VERSION`, `OPTIMALITY_REVIEW_EDITION`), never the site's edition and
    never the data hash (the owner, 2026-10-01: papers are individually versioned)."""
    dates: tuple[Dated, ...]
    """The dates line, in order; the last is `REVISED`."""
    source: Source | None = None
    history: str = ""
    """The id of the paper's version-history section, which the version line links;
    empty for a paper with one version and so no history."""
    series: Series | None = None
    """The series the paper is part of, which the strip under the credits names
    (`series`); None for a paper in no series."""


def check(front: PaperFront) -> PaperFront:
    """`front`, refused where it would write a line the form has no place for."""
    if not front.slug or "/" in front.slug:
        raise ValueError(f"a paper's slug names its files, and {front.slug!r} cannot")
    if not front.title.strip():
        raise ValueError(f"{front.slug}: a paper has a title")
    if not front.oversight or not all(person.name.strip() for person in front.oversight):
        raise ValueError(f"{front.slug}: human oversight names someone")
    if not front.agents or not all(agent.strip() for agent in front.agents):
        raise ValueError(f"{front.slug}: the agents are named")
    for url in (person.url for person in front.oversight):
        if not url.startswith("https://"):
            raise ValueError(f"{front.slug}: a name links an https address, not {url!r}")
    if not front.version.strip() or "<" in front.version or "*" in front.version:
        raise ValueError(f"{front.slug}: the version line is plain text: {front.version!r}")
    if not front.dates or front.dates[-1].label != REVISED:
        raise ValueError(f"{front.slug}: the dates line ends with {REVISED!r}")
    if len({dated.label for dated in front.dates}) != len(front.dates):
        raise ValueError(f"{front.slug}: each date on the dates line is labelled once")
    for dated in front.dates:
        try:
            datetime.strptime(dated.day, _LONG_DATE)  # noqa: DTZ007
        except ValueError as error:
            raise ValueError(
                f"{front.slug}: {dated.label!r} is dated {dated.day!r}, not `October 1, 2026`"
            ) from error
    if front.source is not None and not front.source.address.startswith("https://"):
        raise ValueError(
            f"{front.slug}: the source's address is https: {front.source.address!r}"
        )
    if front.source is not None and not front.source.author.strip():
        raise ValueError(f"{front.slug}: the source is credited by its author's name")
    if front.history and not _ANCHOR_ID.fullmatch(front.history):
        raise ValueError(f"{front.slug}: the version history is linked by its id")
    if front.series is not None:
        numbers = [part.number for part in front.series.parts]
        if numbers != list(range(1, len(numbers) + 1)) or len(numbers) < 2:
            raise ValueError(f"{front.slug}: a series' parts are numbered 1, 2, … in order")
        mine = [part for part in front.series.parts if part.number == front.series.part]
        if len(mine) != 1 or mine[0].slug != front.slug:
            raise ValueError(f"{front.slug}: the series names this paper as its part")
        if not all(part.title.strip() for part in front.series.parts):
            raise ValueError(f"{front.slug}: each part of a series is named by its title")
    return front


def revised(front: PaperFront) -> str:
    """The day the paper says its text last changed, as its dates line writes it."""
    return check(front).dates[-1].day


def iso_date(day: str) -> str:
    """A day as the papers write one, as an ISO date for the page's head."""
    return datetime.strptime(day, _LONG_DATE).date().isoformat()  # noqa: DTZ007


def _names(names: tuple[str, ...]) -> str:
    """Names joined as a sentence lists them: `A`, `A and B`, `A, B, and C`."""
    if len(names) <= 2:
        return " and ".join(names)
    return ", ".join(names[:-1]) + ", and " + names[-1]


def _shown(address: str) -> str:
    """An address as the credits show it: without its scheme."""
    return address.removeprefix("https://")


def _linked_name(person: Person) -> str:
    """A name in bold, linking its address."""
    return (
        f'<a href="{escape(person.url, quote=True)}"><strong>{escape(person.name)}</strong></a>'
    )


def chips(front: PaperFront) -> tuple[tuple[str, str, str], ...]:
    """The formats row's three chips, in order: each one's label, where it goes and what
    its title says. The Markdown and the PDF are beside the page under its slug; the
    third is the project on GitHub, with its mark."""
    return (
        ("MD", f"{front.slug}.md", "The Markdown this page is rendered from"),
        ("PDF", f"{front.slug}.pdf", "The typeset PDF of this page"),
        ("GITHUB", REPO_URL, "The project on GitHub"),
    )


def formats_row(front: PaperFront) -> str:
    """The row of chips at the top corner of the page, and only the page: it is
    navigation, so the Markdown edition drops it."""
    lines = ['<div class="doc-links screen-only">']
    for label, href, title in chips(check(front)):
        mark = GITHUB_MARK if label == "GITHUB" else ""
        lines.append(
            f'  <a class="chip" href="{escape(href, quote=True)}" '
            f'title="{escape(title, quote=True)}">{mark}{label}</a>'
        )
    lines.append("</div>")
    return "\n".join(lines)


def _credit_lines(front: PaperFront) -> list[tuple[str, str, str]]:
    """Each line of the credits: its class, its HTML and its Markdown, in order."""
    lines: list[tuple[str, str, str]] = []
    if front.source is not None:
        author = escape(front.source.author)
        address = front.source.address
        lines.append(
            (
                "credits-source",
                f"{escape(front.source.lead)} <strong>{author}</strong>",
                f"{front.source.lead} **{author}**",
            )
        )
        lines.append(
            (
                "credits-source",
                f'<a href="{escape(address, quote=True)}">{escape(_shown(address))}</a>',
                f"[{_shown(address)}]({address})",
            )
        )
    lines.append(
        (
            "credits-own",
            "Human oversight: " + _names(tuple(_linked_name(p) for p in front.oversight)),
            "Human oversight: "
            + _names(tuple(f"[**{p.name}**]({p.url})" for p in front.oversight)),
        )
    )
    lines.append(
        (
            "",
            "Agents: " + _names(tuple(f"<strong>{escape(a)}</strong>" for a in front.agents)),
            "Agents: " + _names(tuple(f"**{a}**" for a in front.agents)),
        )
    )
    version = escape(front.version)
    if front.history:
        lines.append(
            (
                "edition",
                f'{version} (<a href="#{front.history}">version history</a>)',
                f"{front.version} ([version history](#{front.history}))",
            )
        )
    else:
        lines.append(("edition", version, front.version))
    dates = " · ".join(f"{dated.label} {dated.day}" for dated in front.dates)
    lines.append(("publication-date", escape(dates), dates))
    if front.series is not None:
        lines.extend(_series_lines(front.series))
    return lines


def _series_lines(series: Series) -> list[tuple[str, str, str]]:
    """The series strip, as credit lines: which part of how many this paper is, then each
    other part by its number and its title, linking its paper, in reading order."""
    count = len(series.parts)
    heading = f"Part {numeral(series.part)} of {count} in {series.name}"
    lines = [("series", escape(heading), heading)]
    for part in series.parts:
        if part.number == series.part:
            continue
        label = f"Part {numeral(part.number)}:"
        page = render_overview.paper_path(part.slug).removeprefix(
            render_overview.PAPERS_DIR + "/"
        )
        address = render_overview.SITE_URL + render_overview.paper_path(part.slug)
        lines.append(
            (
                "series",
                f'{label} <a href="{escape(page, quote=True)}">{escape(part.title)}</a>',
                f"{label} [{part.title}]({address})",
            )
        )
    return lines


def credits_html(front: PaperFront) -> str:
    """The credits block as the page carries it: one span a line, in a centred grid
    the publication layer lays out (`paper-publication.css`, `.credits`)."""
    lines = ['<div class="credits centred">']
    for cls, markup, _ in _credit_lines(check(front)):
        opening = f'<span class="{cls}">' if cls else "<span>"
        lines.append(f"  {opening}{markup}</span>")
    lines.append("</div>")
    return "\n".join(lines)


def credits_markdown(front: PaperFront) -> str:
    """The same credits as the Markdown edition lists them: one item a line, so the
    formatter keeps the lines apart rather than running them into a paragraph."""
    return "\n".join(f"- {markdown}" for _, _, markdown in _credit_lines(check(front)))


def hero(front: PaperFront) -> str:
    """The title block: the title as a Markdown heading, then the credits, in the hero
    the publication layer centres. The blank lines are what let the heading inside an
    HTML block render as Markdown."""
    return f'<div class="hero">\n\n# {check(front).title}\n\n{credits_html(front)}\n\n</div>'


def front_matter(front: PaperFront) -> str:
    """Everything above a paper's first paragraph: the formats row, then the hero."""
    return f"{formats_row(front)}\n\n{hero(front)}"


def markdown_front(front: PaperFront) -> str:
    """The same front as the Markdown edition opens with: the title as its heading and
    the credits as a list; the formats row is the page's and is left out."""
    return f"# {check(front).title}\n\n{credits_markdown(front)}"


def fill(source: str, front: PaperFront) -> str:
    """`source` with its one `{{FRONT_MATTER}}` slot filled from `front`; an article
    that carries the slot any other number of times is refused."""
    slot = "{{" + FRONT_MATTER + "}}"
    if source.count(slot) != 1:
        raise ValueError(f"{front.slug}: the article carries {slot} exactly once")
    return source.replace(slot, front_matter(front))


def published(document: str, front: PaperFront) -> str:
    """`document`, a filled article, with its front in the Markdown edition's form.

    The page's front is replaced whole, so an edition cannot keep a chip row that
    offers the file the reader is holding, or the credits as a grid of spans; a
    document whose front is not exactly what `front_matter` wrote is refused rather
    than published with the page's."""
    page_front = front_matter(front)
    if document.count(page_front) != 1:
        raise ValueError(f"{front.slug}: the document does not carry the paper's front once")
    return document.replace(page_front, markdown_front(front))
