#!/usr/bin/env python3
# ruff: noqa: RUF001 -- this module writes the register's own prose, and its typography
# is the corpus's: curly apostrophes, em dashes, ceiling and root brackets, the
# double-struck rationals, and the U+2212 minus in the display formula. A generated
# body has to match a hand-written one byte for byte.
"""Draft one `frontier/n-NNN.md` case record from the sources the register already trusts.

The first hundred cases were written by hand, one at a time, over several sessions. The
range `101..324` is 224 more of them, and the facts that vary between two neighbouring
cases are few: the catalogue's printed side, its credit line, and which of two rules the
lower bound comes from. Everything else -- the evidence ids, the resource block, the
Nagamochi note, the shape of the prose -- is the same sentence retyped, which is exactly
the kind of work that produces a transcription slip nobody finds. So it is generated,
from three inputs and a fixed set of rules, and a golden test regenerates seven of the
hand-written records to show that the rules are the ones the corpus already follows.

**The three inputs.**

1. `atlas/prospective/source-availability-101-324.json`, which says for each `n` whether
   the best known packing is the trivial grid (`exact-generated-geometry`, carrying the
   grid side) or a drawing (`remote-svg-geometry`), and whose `source_key` names where
   that drawing lives: the catalogue for 123 cases in range, and the UnitSquare release
   for four.
2. The catalogue transcription, read through `sqpack.kingbird_catalogue.parse_catalogue`.
   That module is imported dynamically, and only when a catalogue case is generated, so
   the grid half of the range and every test in this file run without it.
3. `resources/web/unitsquare-release1-2026/results.json`, the retained first-party
   release, read only for the four cases the source map assigns to it.

**The bound rules**, from
`docs/project/specs/active/plan-2026-09-07-atlas-expansion-to-324.md`:

- `reported_upper_bound` is the catalogue's printed decimal, transcribed and not
  endorsed, under `E-kingbird-upper-register`; for a rule-generated grid case it is the
  integer side under `construction_method: trivial-grid`; for a UnitSquare case it is
  the release's own `offered_side` under `E-unitsquare-release1-report`.
- `verified_upper_bound` is `ceil(sqrt(n))` under `E-basic-grid-upper`: a ceiling this
  repository can certify, never a reading of `s(n)`.
- both lower bounds are Nagamochi's closed form under `E-nagamochi-lower`, except that a
  perfect square reports the area bound under `E-basic-area-lower`, which is what the
  hand-written perfect squares do.
- `status` is `proved` only where the verified lower bound meets the reported upper
  bound exactly. In `101..324` that is the 24 cases `k^2`, `k^2 - 1` and `k^2 - 2` for
  `k = 11..18`, and nothing else.
- `rigidity` is `null`. The field means "not assessed", never "the packing can move";
  `devtools/screen_translation_escape.py` and `devtools/assess_frontier_rigidity.py`
  write it later in the promotion path.

**Which Kingbird evidence a grid case cites** depends on which sentence of the catalogue
is doing the work, and the two items say so themselves. `E-kingbird-upper-register` is
the catalogue's *pictured* entries; above `n = 100` its own `limitations` field says so.
`E-kingbird-grid-completeness`, scoped `101..324`, carries the catalogue's separate
statement that every `n` it does not picture takes the trivial grid. So an unpictured
grid case above 100 cites the completeness item **instead of** the register item, not
alongside it: the register makes no claim there. At `n <= 100` the completeness item does
not apply -- it is scoped out, and the hand-written unpictured grid cases (`n = 91`,
`n = 100`) cite the register -- so those keep citing the register, byte for byte.

**Reading `construction_method` and `analytically_optimized` off the credit line.** The
catalogue states neither as a field; both live in the prose under the picture, which
`CatalogueEntry.credit_line` now carries verbatim. The table below is not a guess at what
the page means -- it is measured against the sixty catalogue-sourced pictured entries at
`n <= 100` that a person transcribed by hand. A rule fires on 22 of them and agrees with
the transcription on every one; on the other 38 no rule fires, and the transcription
called those `hand-construction` (22), `trivial-grid` (14) or `unknown` (2), never one of
the four methods a rule is for. The counts are the number of entries each rule reaches:

| The credit line contains | `construction_method` | at `n <= 100` | in `101..324` |
| --- | --- | --- | --- |
| `[Explore group](squares_in_squares__Göbel_strips.html)` | `diagonal-strip` | 6 | 10 |
| `[Explore group](squares_in_squares__Göbel_squares.html)` | `hand-construction` | 3 | 8 |
| `Adds <count> "L"s to`, opening the line | `extension` | 0 | 14 |
| `combining` or `Combines two copies`, opening the line | `composition` | 0 | 3 |
| `simulated annealing` | `simulated-annealing` | 10 | 34 |
| `Extends the` or `Unextends the` | `extension` | 3 | 13 |
| none of the above | `unknown` | 38 | 45 |

Four of the 34 that `simulated annealing` reaches in range are `n = 103, 105, 110` and
`131`, whose records take their bound from the release instead and stay `unknown`, so 49
of the 224 generated records carry `unknown` and `--range` prints their numbers.

The rules are tried in that order, and the order is load-bearing four times. Ten entries
in range carry both the strips group link and an "Extends the" sentence; `n = 67` and
`n = 84` are the same shape at `n <= 100` and were both transcribed `diagonal-strip`, so
group membership wins over the provenance sentence. One entry, `n = 297`, is both an
extension and a later simulated-annealing improvement; `n = 87` is that shape at
`n <= 100` and was transcribed `simulated-annealing`, so the method that produced the
printed side wins over the one that produced its parent. `n = 198` adds an "L" to a
composition, and the L rule wins, because the composition it names is its parent's
construction and the "L" is its own. And both new rules are tried before the substring
rules, because the sentence that opens a credit line is the one describing the packing
the entry is about. The two group links differ only in the page they point at -- their
link text is identical -- which is why `credit_line` keeps Markdown link syntax rather
than unwrapping it.

**Phrases are read outside parentheses, and the two structural rules only in the opening
sentence.** The catalogue describes an ancestor parenthetically -- "(using a simulated
annealing program he wrote, starting from randomness)" -- and a method named there is
the ancestor's. Blanking those spans is what stops `n = 171`, a composition of two
copies of an annealed `s(50)`, and `n = 198`, an "L" added to that composition, from
being filed as annealing runs; it changes nothing else, because the other thirty
in-range annealing matches stand in the finder's own sentence or in a dated improver's.

**The L-augmentation family is `extension`, which departs from `n = 82`.** The fourteen
entries in range whose line opens "Adds <count> 'L's to the s(m)" (`101, 122, 145, 173,
197, 198, 199, 200, 226, 229, 258, 261, 292, 298`) describe one construction, and the
catalogue itself calls that construction an extension at `170`, `257` and `260`
("Extends the s(65) ... augmented by five/eight 'L's"), which is why those three records
already read `extension`. Filing the family any other way would leave `s(65)` plus five
or eight "L"s an extension and `s(65)` plus two, three, four, six or seven an `unknown`.
The one hand precedent points the other way: `n = 82` reads `hand-construction`. Its
page is a different shape -- it opens by naming a human finder, "Found by Frits Göbel in
early 1979", and adds the augmentation as an afterthought -- and this rule reads only
the opening sentence, so it does not reach `n = 82` and `n-082.md` is left as written.

`analytically_optimized` is `false` where the line says "Not yet analytically optimized"
(32 entries, every one of them above `n = 100`), `null` where it ends "Further
improvement pending" (9 entries, `102, 130, 172, 199, 228, 259, 269, 292, 302`, and
again all above `n = 100`), and `true` otherwise, which is what all sixty
hand-transcribed catalogue-sourced pictured entries say. The null is `D-354`'s rule:
"further improvement pending" says the entry is still moving and says nothing about
whether its current side has been analytically optimized, and `true` there would be a
positive claim read from silence. `n = 88`'s "Improvement by Thomas Schadt pending" is a
different sentence, is not read as this one, and `n-088.md` keeps its `true`. A grid case
has no credit line and keeps `null`.

**A printed form that disagrees with its printed decimal is not transcribed.** The
catalogue's `n = 179` entry prints a January-2025 closed form beside a January-2026
decimal it does not equal: the record was improved and the stale form was left standing.
So every form is evaluated against the decimal beside it, and where the two disagree
`exact_form`, `algebraic_degree` and `minimal_polynomial` are all `null` and the case
carries a `stale-source` conflict naming both printed values. The decimal is what the
page's own credit line dates; the form is what it forgot to update.

**`improved_by` is the page's dated "Improved by" sentences, and nothing else.** A
sentence-initial "Improved by <names> in <month> <year>" is recorded, names split on
"and" and on commas and each improver kept once in page order; it reaches 33 records in
range. Measured over the 46 catalogue-sourced pictured records at `n <= 100`, the rule
reproduces 45 of them. The one miss is `n = 29`, where the hand pass read an "Optimized
by" sentence as an improvement and `n = 39, 41, 50, 51, 71` did not read the same
sentence that way, so that form is deliberately not read; "Improved independently by
both ..." at `n = 88` is not this form either, and was not recorded by hand. The
schema closes `additionalProperties` on `reported_upper_bound`, so the improvement's
date has nowhere to live in the front matter and reaches the reader through the body
sentence instead. `found_year` stays the year the packing was *found*.

**Two lineages in one entry.** Five entries in range describe two packings, and the
printed decimal is the side of only one of them. At `170`, `257` and `260` the pictured
file is the page's alternative (`square-170b.svg`, `square-257a.svg`, `square-260b.svg`),
so the alternative's finder is the record's; at `240` and `272` the pictured packing was
"Converted in December 2024 from the s(210)" and the page names nobody as its author, so
`found_by` stays empty rather than crediting the 2015 or 1991-98 original with a packing
made nine years later. Either way the lineage the record sets aside becomes a
`priority_notes` entry quoting the page's own phrase, so nothing the page says is
dropped silently.

**A retained paper behind a credit is cited.** The seven entries the catalogue credits
to all three authors of `resources/papers/arslanov-improved-packings-n-n-1` (`132, 156,
182, 210, 241, 273, 307`) list `[Arslanov et al.]` second, immediately after the
catalogue, which is where `n-013.md` and `n-011.md` list the paper behind a credit. The
rule is keyed on the credit rather than on a list of `n`, because the credit is what the
citation is about.

**The packing paragraph does not join the finder to the method.** `found_by` is the
page's first credit and `construction_method` is what produced the *printed* side, so
"Found by <finder> in <year>, via <method>" -- the sentence the hand-written `n = 53` and
`n = 87` set the template for -- read two different conventions as one claim, and at the
seven Arslanov cases it credited a March 2019 analytic construction to a January 2026
annealing run. The method now hangs off whichever credit the phrase that named it sits
in: the finder's sentence, a dated improvement's, or, where it sits in neither, no credit
at all ("The recorded construction method is ..."). `unknown` is the exception, and stays
on the finder's sentence, because "via an unrecorded method" adds no claim to what
precedes it. `n-053.md` and `n-087.md` are hand-written and are left as written.

**What this tool cannot know**, and does not guess:

- `source_reviewed` and `retrieved_date` are dates, supplied by the caller. `--check`
  reads them back out of the record being checked so that a regeneration months later
  still diffs to nothing, and compares everything but the `rigidity` block for a related
  reason: the promotion path writes that block after this tool has run, and a check that
  insisted on `null` there would report every promoted record as drift and so find none.
- Case-specific evidence is editorial. `priority_notes` is written only for the second
  lineage above, and is otherwise empty.

The record it writes is a draft. It is complete and it validates, and it is not a
substitute for the review that follows it.

Usage, from `packing/`:

    uv run --frozen --all-extras --group dev python -m devtools.generate_frontier_case \\
        --n 101
    uv run --frozen --all-extras --group dev python -m devtools.generate_frontier_case \\
        --range 101 200 --out /tmp/draft
    uv run --frozen --all-extras --group dev python -m devtools.generate_frontier_case \\
        --range 101 324 --check
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import importlib
import json
import math
import re
import tempfile
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, replace
from decimal import ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP, Context, Decimal, localcontext
from pathlib import Path
from typing import Any, Protocol

import yaml
from strif import atomic_output_file

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
AVAILABILITY = ROOT / "atlas" / "prospective" / "source-availability-101-324.json"
UNITSQUARE_RELEASE = ROOT / "resources" / "web" / "unitsquare-release1-2026" / "results.json"

#: `n <= 100` is hand-authored. The generator refuses to write into the register there,
#: and the golden test is the one caller that generates those cases at all -- into a
#: temporary directory, to compare against what a person wrote.
HAND_AUTHORED_MAX = 100

#: Where the catalogue's own completeness statement stops. Past it the catalogue pictures
#: isolated cases and claims nothing about the ones it does not picture, so the grid rule
#: below has no source behind it and this tool will not apply it.
CATALOGUE_COMPLETENESS_MAX = 324

GRID_CLASSIFICATION = "exact-generated-geometry"
CATALOGUE_CLASSIFICATION = "remote-svg-geometry"

#: The source map's key for the four cases in range whose drawing, and whose bound, come
#: from the retained UnitSquare release rather than from the catalogue.
UNITSQUARE_AVAILABILITY_KEY = "unitsquare-release-1"

KINGBIRD_SOURCE_KEY = "[Kingbird]"
UNITSQUARE_SOURCE_KEY = "[UnitSquare 2026]"

KINGBIRD_EVIDENCE = "E-kingbird-upper-register"
GRID_COMPLETENESS_EVIDENCE = "E-kingbird-grid-completeness"
UNITSQUARE_EVIDENCE = "E-unitsquare-release1-report"
GRID_UPPER_EVIDENCE = "E-basic-grid-upper"
AREA_LOWER_EVIDENCE = "E-basic-area-lower"
NAGAMOCHI_EVIDENCE = "E-nagamochi-lower"

NAGAMOCHI_NOTE = (
    "General closed form: s(N) >= min(ceil(sqrt(N)), sqrt(N - 2*floor(sqrt(N)) + 1) + 1)."
)
UPPER_GAP_BLOCKER = "No formal certificate currently supports the tighter reported upper bound."

#: The gap a UnitSquare case carries instead. The mathematics is the same -- a certified
#: ceiling trailing a reported construction -- but what stands between them here is not an
#: unproved inequality: the source states an interval validation and publishes nothing that
#: replays it, which is `source-evidence`. Copied from `n-068.md` and `n-069.md`, the two
#: hand-written records of this shape, and from the evidence item's own `blocker` field.
UNITSQUARE_BLOCKER = (
    "The source reports interval validation but does not publish the interval boxes, "
    "receipt, or replayable checker needed to inspect it."
)

#: The three resources every generated case cites. A perfect square drops the middle one:
#: its lower bound is the area bound, and the hand-written perfect squares list only the
#: two sources they actually lean on.
KINGBIRD_RESOURCE: dict[str, Any] = {
    "key": KINGBIRD_SOURCE_KEY,
    "role": "record-catalogue",
    "local": "web/kingbird-squares-in-squares",
    "url": "https://kingbird.myphotos.cc/packing/squares_in_squares.html",
    "retrieved": True,
}
#: Listed second, immediately after the catalogue, by the two hand-written records that
#: cite it: the catalogue is still where the case is looked up, and the release is where
#: this case's number comes from.
UNITSQUARE_RESOURCE: dict[str, Any] = {
    "key": UNITSQUARE_SOURCE_KEY,
    "role": "upper-bound-report",
    "local": "web/unitsquare-release1-2026/results.json",
    "url": "https://hmbelvedere.com/data/results.json",
    "retrieved": True,
}
NAGAMOCHI_RESOURCE: dict[str, Any] = {
    "key": "[Nagamochi 2005]",
    "role": "lower-bound-proof",
    "local": "papers/nagamochi-2005-packing-unit-squares-in-a-rectangle",
    "url": "https://www.combinatorics.org/ojs/index.php/eljc/article/view/v12i1r37",
    "retrieved": True,
}
FRIEDMAN_RESOURCE: dict[str, Any] = {
    "key": "[Friedman DS7]",
    "role": "survey",
    "local": "papers/friedman-ds7-packing-unit-squares-in-squares",
    "url": "https://erich-friedman.github.io/papers/squares/squares.html",
    "retrieved": True,
}

#: Significant figures each lower-bound lane carries. Both are the corpus's own choice,
#: re-measured against all hundred records rather than assumed: `reported_lower_bound`
#: prints 13 and `verified_lower_bound` 12, each with trailing zeros dropped, which is
#: why `n = 50` reads 7.082762530298 above and 7.0827625303 below.
REPORTED_SIGNIFICANT = 13
VERIFIED_SIGNIFICANT = 12

#: Enough digits that the square root is exact well past either lane's last place.
BOUND_PRECISION = 60

COMMON_DOC_FOOTER = (
    "<!-- This document follows common-doc-guidelines.md.\n"
    "See github.com/jlevy/practical-prose and review guidelines before editing.\n"
    "-->\n"
)

NAGAMOCHI_DISPLAY = "s(N) ≥ min{ ⌈√N⌉,  √(N − 2⌊√N⌋ + 1) + 1 }"

#: The closing sentence of "The lower bound", in the two forms the corpus uses.
#:
#: The first quotes a corpus-wide count, and `devtools/check_nagamochi_bounds.py` owns
#: that count: it re-derives "N of the M open cases" from the case records and fails if
#: any body disagrees. Writing it into 200 new records would put a figure about the first
#: hundred into files that are not part of what it counts, and would move the count on
#: the day the new cases land. So generated records past the hand-authored range say the
#: same thing without the arithmetic, and the counted form is emitted only where the
#: corpus that owns it already carries it.
NAGAMOCHI_DEFAULT_COUNTED = (
    "This is the default across almost the whole open frontier — 58 of the 65 open cases "
    "at `n ≤ 100` are governed by it, and outside this repository’s own displacements it "
    "has not been improved since 2005."
)
NAGAMOCHI_DEFAULT_UNCOUNTED = (
    "This is the default across almost the whole open frontier, and outside this "
    "repository’s own displacements it has not been improved since 2005."
)

#: `construction_method` enum value -> the phrase the corpus's prose uses for it. Read off
#: the hand-written bodies for the five values a credit line can now produce; the other
#: three follow their pattern and are unreachable until a rule is written for them.
CONSTRUCTION_PHRASES = {
    "trivial-grid": "the trivial grid",
    "hand-construction": "a hand construction",
    "diagonal-strip": "a diagonal-strip construction",
    "pattern-family": "a pattern family",
    "extension": "extension of a smaller record",
    "composition": "a composition of smaller packings",
    "simulated-annealing": "simulated annealing",
    "inflation-billiard": "an inflation-billiard search",
    "unknown": "an unrecorded method",
}

#: `construction_method` enum value -> the noun phrase a sentence that names no author
#: uses for it. The same reading as `CONSTRUCTION_PHRASES`, re-articled: "via extension
#: of a smaller record" is a clause hanging off a credit, and "The recorded construction
#: method is an extension of a smaller record" is a sentence standing on its own.
CONSTRUCTION_SUBJECTS = {
    "trivial-grid": "the trivial grid",
    "hand-construction": "a hand construction",
    "diagonal-strip": "a diagonal-strip construction",
    "pattern-family": "a pattern family",
    "extension": "an extension of a smaller record",
    "composition": "a composition of smaller packings",
    "simulated-annealing": "simulated annealing",
    "inflation-billiard": "an inflation-billiard search",
    "unknown": "an unrecorded method",
}


@dataclass(frozen=True, slots=True)
class CreditMethodRule:
    """One row of the credit-line table in this module's docstring.

    `pattern` is searched, not matched, against the credit line with its parenthesised
    spans blanked out. `opening_only` restricts it to the line's first sentence, which
    is where the catalogue describes the packing the entry is about; a rule without it
    reads the whole line, because a method can also arrive with a dated improvement.
    """

    pattern: str
    method: str
    opening_only: bool = False

    @property
    def regex(self) -> re.Pattern[str]:
        return re.compile(self.pattern)


#: What the catalogue's credit line has to say for a `construction_method` to be read off
#: it, in the order the rules are tried. Derived from the hand transcription and measured
#: against it; the module docstring tabulates the counts and argues the ordering. A line
#: matching none of these is `unknown`, which is the honest answer and not a placeholder.
CREDIT_METHOD_RULES: tuple[CreditMethodRule, ...] = (
    CreditMethodRule(
        re.escape("[Explore group](squares_in_squares__Göbel_strips.html)"), "diagonal-strip"
    ),
    CreditMethodRule(
        re.escape("[Explore group](squares_in_squares__Göbel_squares.html)"),
        "hand-construction",
    ),
    CreditMethodRule(r'^Adds\s+\S+\s+"L"s?\s+to\b', "extension", opening_only=True),
    CreditMethodRule(
        r"\b[Cc]ombin(?:es|ing)\s+two\s+copies\b", "composition", opening_only=True
    ),
    CreditMethodRule("simulated annealing", "simulated-annealing"),
    CreditMethodRule("Extends the", "extension"),
    CreditMethodRule("Unextends the", "extension"),
)

#: The catalogue's two sentences about how finished an entry is. The first is a statement
#: ("this side has not been optimized analytically"); the second is a statement that the
#: entry is still moving, and says nothing either way about the first. `D-354` is the
#: standing lesson against reading a source's silence as a value, so a page that carries
#: the second and not the first leaves `analytically_optimized` null.
NOT_ANALYTICALLY_OPTIMIZED = "Not yet analytically optimized"
IMPROVEMENT_PENDING = "Further improvement pending"

#: Credit sentences a parent chain is read from, longest opener first so that "Found
#: first by" is not read as "Found by". Only a credit that names a date is counted: the
#: catalogue also writes bare "Optimized by <name>." sentences, and those are the ones
#: `improved_by` shows no consistent hand reading of.
_CREDIT_ROLES = (
    "Found first by",
    "Found by",
    "Refound and refined by",
    "Refound by",
    "Refined by",
    "Improved by",
    "Optimized by",
    "Proved by",
)
_CREDIT_CHAIN = re.compile(
    rf"\b(?:{'|'.join(_CREDIT_ROLES)})\s+(?P<names>.+?)\s+in\s+(?:[A-Za-z-]+\s+)*\d{{4}}\b"
)

#: A credit line's sentences, and the parenthesised spans inside one. Both are three
#: lines duplicated from `sqpack.kingbird_catalogue` rather than imported, for the reason
#: `CatalogueEntryLike` gives: this module stays importable, and testable, without the
#: catalogue parser. A period ends a sentence only where it does not follow a single
#: capital letter, which keeps "David W. Cantrell" and "M.Z. Arslanov" whole.
_SENTENCE_BREAK = re.compile(r"(?<![A-Z])\.\s+")
#: A parenthesis the page opened, which is never a Markdown link's target: `credit_line`
#: keeps link syntax because "[Explore group](squares_in_squares__Göbel_strips.html)" is
#: the only thing separating the Göbel strips from the Göbel squares, and blanking what
#: follows the bracket would blank the two family rules along with it.
_PARENTHESISED = re.compile(r"(?<!\])\([^()]*\)")

#: The one improvement form the corpus reads, and the only one it reads consistently: a
#: sentence-initial "Improved by <names> in <month> <year>". Measured over the 46
#: catalogue-sourced pictured records at `n <= 100`, it reproduces 45 of them; the miss
#: is `n = 29`, where the hand pass read an "Optimized by" sentence as an improvement and
#: `n = 39, 41, 50, 51, 71` did not read the same sentence that way. "Improved
#: independently by both ..." at `n = 88` is not this form and is not recorded, which is
#: also what the hand pass did.
_IMPROVED_BY = re.compile(
    r"^Improved by\s+(?P<names>.+?)\s+in\s+(?P<when>(?:[A-Za-z-]+\s+)*)(?P<year>\d{4})\b"
)

#: The two lineage shapes the page prints where one entry carries two packings, and the
#: `found by` clause read out of either. Both are structural, both reach exactly the
#: entries the review named, and both leave the record crediting whichever packing the
#: printed decimal is the side of.
#:
#: "This alternative, converting the s(65) augmented by five 'L's into a primitive
#: packing, found by Károly Hajba in November 2024" (`n = 170, 257, 260`): the pictured
#: file is the alternative -- `square-170b.svg`, `square-257a.svg`, `square-260b.svg` --
#: so the alternative's finder is the record's, and the sentence before it, which credits
#: the extension the alternative converts, becomes a priority note.
#:
#: "Originally found by Károly Hajba in September 2015 ... Converted in December 2024
#: from the s(210)" (`n = 240, 272`): the printed decimal is the conversion's, and the
#: page names nobody as its author, so `found_by` stays empty and the original lineage
#: becomes a priority note. Reading the "Originally found by" sentence as this record's
#: credit would date the pictured packing to 2015, nine years before it existed.
_ALTERNATIVE = re.compile(r"\bThis alternative\b")
_CONVERTED = re.compile(r"^Converted in\b")
_ORIGINALLY_FOUND = re.compile(
    r"^Originally found by\s+(?P<names>.+?)"
    r"(?:\s+in\s+(?:[A-Za-z-]+\s+)*(?P<year>\d{4})|\s+between\s+\d{4}|$)"
)
_LOWER_CREDIT = re.compile(
    r"\bfound by\s+(?P<names>.+?)\s+in\s+(?:[A-Za-z-]+\s+)*(?P<year>\d{4})\b"
)
_MATH_DELIMITER = re.compile(r"\$")

#: The three authors of the retained Arslanov paper, as the catalogue spells them. A
#: record whose `found_by` is exactly this credit cites the paper behind it, which is
#: what the hand-written records do wherever this repository retains the paper a credit
#: rests on (`[Bentz 2010]` at 13 and 46, `[Stromquist 2003]` at 10, 11 and 12,
#: `[Kearney-Shiu 2002]` at 6, `[Gensane-Ryckelynck 2005]` at 11).
ARSLANOV_AUTHORS = ("M.Z. Arslanov", "S.A. Mustafin", "Z.K. Shangitbayev")
ARSLANOV_RESOURCE: dict[str, Any] = {
    "key": "[Arslanov et al.]",
    "role": "upper-bound-report",
    "local": "papers/arslanov-improved-packings-n-n-1",
    "url": "https://www.combinatorics.org/ojs/index.php/eljc/article/download/v28i4p22/pdf/",
    "retrieved": True,
}

#: Month names for the one date the prose spells out, fixed here so that the process
#: locale cannot change what a generated record says.
MONTH_NAMES = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)

#: Decimal places the prose quotes a first-party release's own side to before marking the
#: rest with an ellipsis. The two hand-written records of this shape print twenty
#: significant figures of a forty-five figure number, which is this, and no trailing zero
#: is dropped: the ellipsis says the digits continue, so the last place has to be real.
FIRST_PARTY_DISPLAY_PLACES = 19


class GenerationError(Exception):
    """A case cannot be drafted from the inputs given."""


# --------------------------------------------------------------------------------------
# Inputs
# --------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class SourceAvailability:
    """One row of the prospective source map: where this `n`'s best known packing lives."""

    n: int
    classification: str
    source_key: str
    trivial_grid_side: int | None

    @property
    def is_grid(self) -> bool:
        return self.classification == GRID_CLASSIFICATION

    @property
    def is_unitsquare(self) -> bool:
        """Whether the release, rather than the catalogue, is this case's reporting source.

        The source map answers "where is the drawing", and for these four cases the answer
        also settles where the number comes from: the release publishes a side the
        catalogue's own entry no longer matches.
        """
        return self.source_key == UNITSQUARE_AVAILABILITY_KEY


@dataclass(frozen=True, slots=True)
class CreditImprovement:
    """One dated, sentence-initial "Improved by ... in ..." the catalogue prints.

    `when` is the page's own date words -- "November 2024", or a bare year where the page
    gives no month -- and is carried here because the schema has nowhere to put it:
    `reportedUpper` closes `additionalProperties`, and `found_year` means the year the
    packing was found, never the year it was last improved. So the date reaches the reader
    through the body sentence, and the front matter carries only `improved_by`.

    `sentence` indexes `credit_sentences`, which is how `_method_owner` decides whether
    the credit line's construction method belongs to this improvement or to the finder.
    """

    names: tuple[str, ...]
    when: str
    sentence: int


@dataclass(frozen=True, slots=True)
class PriorityNote:
    """One `priority_notes` entry: a lineage the entry carries that the record does not.

    Written only where a catalogue entry describes two packings and the printed decimal
    is the side of one of them; the note records the other, quoting the page's own phrase
    so a reader can see what was set aside and why.
    """

    claim: str
    claimed_by: tuple[str, ...] = ()
    year: int | None = None

    def as_payload(self) -> dict[str, Any]:
        return {
            "claim": self.claim,
            "claimed_by": list(self.claimed_by),
            "published": None,
            "year": self.year,
        }


@dataclass(frozen=True, slots=True)
class CatalogueFacts:
    """Everything a case record takes from the record catalogue, for one `n`.

    The first nine fields come straight off `sqpack.kingbird_catalogue.CatalogueEntry`.
    `construction_method`, `analytically_optimized`, `improved_by`, `improvements` and
    `priority_notes` are read from that entry's credit line by
    `facts_from_catalogue_entry`, under the table in this module's docstring, and default
    to the values that say "no line has been read". `found_by` and `found_year` are the
    parser's, except at the five entries carrying two lineages, where `_lineage` decides
    which of the two the printed decimal belongs to.

    `stale_exact_form` is the one field that records something the catalogue got wrong
    rather than something it says: the form the page prints where that form does not
    evaluate to the decimal beside it. It is set exactly when `exact_form` has been
    dropped for that reason, and it is what the case's `stale-source` conflict quotes.
    """

    n: int
    side_decimal: str
    exact_form: str | None = None
    algebraic_degree: int | None = None
    minimal_polynomial: str | None = None
    found_by: tuple[str, ...] = ()
    found_year: int | None = None
    catalogue_rigid: str = "not-stated"
    catalogue_pictured: bool = True
    construction_method: str = "unknown"
    analytically_optimized: bool | None = None
    improved_by: tuple[str, ...] = ()
    credit_line: str | None = None
    stale_exact_form: str | None = None
    improvements: tuple[CreditImprovement, ...] = ()
    priority_notes: tuple[PriorityNote, ...] = ()


class CatalogueEntryLike(Protocol):
    """The half of `sqpack.kingbird_catalogue.CatalogueEntry` this tool reads.

    Declared structurally so that this module neither imports that one at module scope
    nor duplicates its definition: the catalogue parser is a separate piece of work, and
    a case can be drafted from facts handed in directly, which is what the tests do.
    """

    @property
    def n(self) -> int: ...
    @property
    def side_decimal(self) -> str: ...
    @property
    def exact_form(self) -> str | None: ...
    @property
    def algebraic_degree(self) -> int | None: ...
    @property
    def minimal_polynomial(self) -> str | None: ...
    @property
    def found_by(self) -> Sequence[str]: ...
    @property
    def found_year(self) -> int | None: ...
    @property
    def catalogue_rigid(self) -> str: ...
    @property
    def catalogue_pictured(self) -> bool: ...
    @property
    def credit_line(self) -> str | None: ...


def _normalized_credit(credit_line: str | None) -> str:
    """One credit line as a single space-separated string, Markdown markup intact.

    The transcription breaks a credit sentence across lines wherever the page did, so
    "Found by Maurizio Morandi\\nin June 2010." and the same sentence on one line have to
    read alike. Only whitespace is touched.
    """
    return "" if credit_line is None else re.sub(r"\s+", " ", credit_line).strip()


def credit_sentences(credit_line: str | None) -> tuple[str, ...]:
    """One credit line as the sentences the page wrote, whitespace normalised.

    The first of them is the sentence that describes the packing the entry is about; the
    rest are its history, its family links and the page's own disclaimers.
    """
    text = _normalized_credit(credit_line)
    return tuple(part.strip() for part in _SENTENCE_BREAK.split(text) if part.strip())


def _method_sentences(credit_line: str | None) -> tuple[str, ...]:
    """The credit line's sentences with their parenthesised spans blanked out.

    The catalogue describes an ancestor inside a parenthesis -- "(using a simulated
    annealing program he wrote, starting from randomness)" -- and the method named there
    is the ancestor's, not this entry's. Blanking them is what stops `n = 171`, a
    composition of two copies of an annealed `s(50)`, and `n = 198`, an "L" added to that
    composition, from being recorded as annealing runs. It changes nothing else: the
    other thirty in-range matches stand in the finder's own sentence or in a dated
    improvement's.
    """
    return tuple(
        _PARENTHESISED.sub(" ", sentence) for sentence in credit_sentences(credit_line)
    )


def credit_method_match(credit_line: str | None) -> tuple[str, int | None]:
    """The `construction_method` the credit line states, and the sentence that states it.

    The rules and the evidence for them are in this module's docstring. Nothing is
    inferred from what the line does *not* say: a named human author and no mention of a
    program is `unknown` here, because the catalogue writes exactly that for packings
    found by computer search (`n = 68`). The sentence index is `None` for `unknown`, and
    is what lets the prose attach the method to the credit that owns it.
    """
    sentences = _method_sentences(credit_line)
    if not sentences:
        return "unknown", None
    for rule in CREDIT_METHOD_RULES:
        regex = rule.regex
        scope = sentences[:1] if rule.opening_only else sentences
        for offset, sentence in enumerate(scope):
            if regex.search(sentence):
                return rule.method, offset
    return "unknown", None


def construction_method_from_credit(credit_line: str | None) -> str:
    """The `construction_method` the catalogue's credit line states, or `unknown`."""
    return credit_method_match(credit_line)[0]


def improvements_from_credit(credit_line: str | None) -> tuple[CreditImprovement, ...]:
    """Every dated, sentence-initial "Improved by <names> in <date>", in page order.

    The one improvement form the corpus reads consistently; `_IMPROVED_BY` carries the
    measurement. Names are split on "and" and on commas, exactly as the finder's credit
    is split, and a sentence naming several improvers yields one entry naming all of
    them.
    """
    found: list[CreditImprovement] = []
    for index, sentence in enumerate(credit_sentences(credit_line)):
        match = _IMPROVED_BY.search(sentence)
        if match is None:
            continue
        when = f"{match.group('when').strip()} {match.group('year')}".strip()
        found.append(
            CreditImprovement(
                names=_split_names(match.group("names")), when=when, sentence=index
            )
        )
    return tuple(found)


def improved_by_from_credit(credit_line: str | None) -> tuple[str, ...]:
    """Every improver the credit line names, in page order, each kept once."""
    names: list[str] = []
    for improvement in improvements_from_credit(credit_line):
        for name in improvement.names:
            if name not in names:
                names.append(name)
    return tuple(names)


def analytically_optimized_from_credit(credit_line: str | None) -> bool | None:
    """Whether the catalogue says this side has been optimized analytically.

    `None` where there is no credit line at all -- a rule-generated grid case, which the
    catalogue does not picture and says nothing about -- and `None` again where the page
    ends "Further improvement pending", which says the entry is still moving and says
    nothing about whether its current side has been optimized. `true` there would be a
    positive claim read from silence, which `D-354` is the standing lesson against; the
    nine pages in range that carry it (`102, 130, 172, 199, 228, 259, 269, 292, 302`)
    therefore carry null. `n = 88`'s "Improvement by Thomas Schadt pending" is a
    different sentence and is not read as this one.
    """
    text = _normalized_credit(credit_line)
    if not text:
        return None
    if IMPROVEMENT_PENDING in text:
        return None
    return NOT_ANALYTICALLY_OPTIMIZED not in text


def _split_names(text: str) -> tuple[str, ...]:
    """ "David W. Cantrell and David Ellsworth" as two names, the way the parser splits one."""
    return tuple(
        name.strip() for part in text.split(" and ") for name in part.split(",") if name.strip()
    )


def _quoted_phrase(sentence: str) -> str:
    """One of the page's sentences, ready to be quoted inside a note.

    The catalogue writes its parent packings as `$s(65)$`; the delimiters are LaTeX and
    say nothing, so they come out and the name stays.
    """
    return _MATH_DELIMITER.sub("", sentence).strip().rstrip(".")


def _lineage(
    credit_line: str | None, found_by: tuple[str, ...], found_year: int | None
) -> tuple[tuple[str, ...], int | None, tuple[PriorityNote, ...]]:
    """Whose the printed decimal is, at the five entries that carry two packings.

    Returns the credit and the priority notes for one entry. Everywhere else it returns
    the parser's credit unchanged and no notes, which is all but five of the 107
    catalogue-sourced records in `101..324`; `_ALTERNATIVE` and `_CONVERTED` carry the
    evidence for the two shapes and for which packing each decimal belongs to.
    """
    sentences = credit_sentences(credit_line)
    for index, sentence in enumerate(sentences):
        if not _ALTERNATIVE.search(sentence):
            continue
        credit = _LOWER_CREDIT.search(sentence)
        if credit is None:
            break
        notes: list[PriorityNote] = []
        if index:
            prior = sentences[index - 1]
            prior_credit = _LOWER_CREDIT.search(prior)
            notes.append(
                PriorityNote(
                    claim=(
                        "The catalogue pictures this entry’s alternative construction; its "
                        f"other lineage is the page’s own “{_quoted_phrase(prior)}”."
                    ),
                    claimed_by=(
                        ()
                        if prior_credit is None
                        else _split_names(prior_credit.group("names"))
                    ),
                    year=None if prior_credit is None else int(prior_credit.group("year")),
                )
            )
        return _split_names(credit.group("names")), int(credit.group("year")), tuple(notes)

    converted = any(_CONVERTED.search(sentence) for sentence in sentences)
    for sentence in sentences if converted else ():
        match = _ORIGINALLY_FOUND.search(sentence)
        if match is None:
            continue
        year = match.group("year")
        note = PriorityNote(
            claim=(
                "The catalogue pictures the packing this entry was converted into, not the "
                "one it started as; the original lineage is the page’s own "
                f"“{_quoted_phrase(sentence)}”."
            ),
            claimed_by=_split_names(match.group("names")),
            year=None if year is None else int(year),
        )
        return (), None, (note,)
    return found_by, found_year, ()


def credited_surnames(credit_line: str | None) -> tuple[str, ...]:
    """The surnames of the catalogue's dated credit sentences, in page order.

    "Found by Sigvart Brendberg in June 2023 ... Improved by Thomas Schadt in December
    2025 ... Optimized by David Ellsworth in December 2025" yields
    `("Brendberg", "Schadt", "Ellsworth")`, which is how `n-068.md` names the parent this
    repository's UnitSquare records improve on. Repeats collapse to their first mention.
    """
    names: list[str] = []
    for match in _CREDIT_CHAIN.finditer(_normalized_credit(credit_line)):
        surname = match.group("names").split()[-1]
        if surname not in names:
            names.append(surname)
    return tuple(names)


def _catalogue_module() -> Any:
    """Import the catalogue parser, late and by name, or say why a case cannot be drafted."""
    try:
        return importlib.import_module("sqpack.kingbird_catalogue")
    except ModuleNotFoundError as error:
        raise GenerationError(
            "the catalogue parser sqpack.kingbird_catalogue is not available, so only "
            "grid cases can be drafted"
        ) from error


def exact_form_agrees(exact_form: str, side_decimal: str) -> bool:
    """Whether a printed closed form evaluates to the decimal printed beside it.

    The arithmetic is the parser's, so that this module and
    `devtools/check_source_coverage.py` ask the catalogue the same question. It needs
    SymPy; where SymPy is missing the answer is unknown, and an unknown answer here would
    mean recording a form nothing has checked, so it refuses instead.
    """
    module = _catalogue_module()
    try:
        value = module.evaluate_exact_form(exact_form)
    except ModuleNotFoundError as error:
        raise GenerationError(
            f"cannot check the printed form {exact_form!r} against the decimal "
            f"{side_decimal!r} without SymPy, and an unchecked form is not recorded"
        ) from error
    return bool(module.agrees_with_printed_decimal(value, side_decimal))


def facts_from_catalogue_entry(
    entry: CatalogueEntryLike, *, n: int | None = None
) -> CatalogueFacts:
    """Adapt one parsed catalogue entry to the facts a case record needs.

    `n` overrides the entry's own, and the caller normally passes it. A catalogue row can
    cover two sizes -- "119, 120" is one drawing and one printed side -- and the parser
    keys such an entry under both while `entry.n` names only one of them.

    The readings that happen here rather than in the parser are this repository's
    judgement about the page rather than a transcription of it: the credit line is mapped
    onto the schema's enums, its improvements and its second lineage are read out of it,
    and a closed form that disagrees with its own printed decimal is dropped in favour of
    the decimal.
    """
    exact_form = entry.exact_form
    stale_exact_form: str | None = None
    if exact_form is not None and not exact_form_agrees(exact_form, entry.side_decimal):
        stale_exact_form = exact_form
        exact_form = None
    improvements = improvements_from_credit(entry.credit_line)
    found_by, found_year, priority_notes = _lineage(
        entry.credit_line, tuple(entry.found_by), entry.found_year
    )
    return CatalogueFacts(
        n=entry.n if n is None else n,
        side_decimal=entry.side_decimal,
        exact_form=exact_form,
        algebraic_degree=None if stale_exact_form else entry.algebraic_degree,
        minimal_polynomial=None if stale_exact_form else entry.minimal_polynomial,
        found_by=found_by,
        found_year=found_year,
        catalogue_rigid=entry.catalogue_rigid or "not-stated",
        catalogue_pictured=entry.catalogue_pictured,
        construction_method=construction_method_from_credit(entry.credit_line),
        analytically_optimized=analytically_optimized_from_credit(entry.credit_line),
        improved_by=improved_by_from_credit(entry.credit_line),
        credit_line=entry.credit_line,
        stale_exact_form=stale_exact_form,
        improvements=improvements,
        priority_notes=priority_notes,
    )


@dataclass(frozen=True, slots=True)
class UnitSquareRecord:
    """One row of the retained UnitSquare release, with the release's own header facts."""

    n: int
    offered_side: str
    cited_parent_side: str
    absolute_reduction: str
    creator: str
    published: str

    @property
    def published_year(self) -> int:
        return int(self.published[:4])


def load_unitsquare_release(path: Path | None = None) -> dict[int, UnitSquareRecord]:
    """Read the retained first-party release into one row per `n` it reports."""
    source = path or UNITSQUARE_RELEASE
    document = json.loads(source.read_text(encoding="utf-8"))
    creator = str(document["creator"])
    published = str(document["published"])
    return {
        int(row["n"]): UnitSquareRecord(
            n=int(row["n"]),
            offered_side=str(row["offered_side"]),
            cited_parent_side=str(row["cited_parent_side"]),
            absolute_reduction=str(row["absolute_reduction"]),
            creator=creator,
            published=published,
        )
        for row in document["results"]
    }


def load_availability(path: Path | None = None) -> dict[int, SourceAvailability]:
    """Read the prospective source map into one row per `n`."""
    source = path or AVAILABILITY
    document = json.loads(source.read_text(encoding="utf-8"))
    rows: dict[int, SourceAvailability] = {}
    for entry in document["availability"]["entries"]:
        n = int(entry["n"])
        rows[n] = SourceAvailability(
            n=n,
            classification=str(entry["classification"]),
            source_key=str(entry["source_key"]),
            trivial_grid_side=(
                int(entry["trivial_grid_side"])
                if entry.get("trivial_grid_side") is not None
                else None
            ),
        )
    return rows


def load_catalogue(path: Path | None = None) -> dict[int, CatalogueFacts]:
    """Parse the retained catalogue transcription into per-`n` facts.

    The import is dynamic and late on purpose. `sqpack.kingbird_catalogue` is written
    against the same plan as this module and lands beside it; nothing here needs it until
    a catalogue-sourced case is actually drafted, and no test in this file needs it at
    all, because facts can be handed in directly.
    """
    parsed: Mapping[int, CatalogueEntryLike] = _catalogue_module().parse_catalogue(path)
    return {n: facts_from_catalogue_entry(entry, n=n) for n, entry in parsed.items()}


# --------------------------------------------------------------------------------------
# Bounds
# --------------------------------------------------------------------------------------


def grid_ceiling(n: int) -> int:
    """`ceil(sqrt(n))`, the side of the trivial no-tilt grid."""
    root = math.isqrt(n)
    return root if root * root == n else root + 1


def is_perfect_square(n: int) -> bool:
    return math.isqrt(n) ** 2 == n


def is_nagamochi_exact(n: int) -> bool:
    """Whether `n` is one of Nagamochi's exact cases `m^2`, `m^2 - 1`, `m^2 - 2`."""
    side = grid_ceiling(n)
    return side * side - n <= 2


def nagamochi_exact_form(n: int) -> str:
    """The exact identity of Nagamochi's bound for `n`, spelled as the corpus spells it."""
    if is_nagamochi_exact(n):
        return str(grid_ceiling(n))
    return f"sqrt({n} - 2*floor(sqrt({n})) + 1) + 1"


def _strip_trailing_zeros(text: str) -> str:
    if "." not in text:
        return text
    return text.rstrip("0").rstrip(".")


def nagamochi_value(n: int, significant: int) -> str:
    """Nagamochi's bound for `n`, printed to `significant` figures as the register does."""
    if is_nagamochi_exact(n):
        return str(grid_ceiling(n))
    with localcontext() as context:
        context.prec = BOUND_PRECISION
        root = math.isqrt(n)
        value = Decimal(n - 2 * root + 1).sqrt() + 1
    return _strip_trailing_zeros(format(Context(prec=significant).plus(value), "f"))


def _quantized(value: Decimal, places: int, rounding: str) -> Decimal:
    with localcontext() as context:
        context.prec = BOUND_PRECISION
        return value.quantize(Decimal(1).scaleb(-places), rounding=rounding)


def display_upper(value: str, places: int = 8) -> str:
    """An upper bound at `places`, rounded up so the inequality the prose writes stays true."""
    return _strip_trailing_zeros(format(_quantized(Decimal(value), places, ROUND_CEILING), "f"))


def display_first_party_upper(value: str, places: int = FIRST_PARTY_DISPLAY_PLACES) -> str:
    """A published side quoted at the source's own length, elided only where it runs on.

    A release that publishes forty-five significant figures is quoted to twenty of them
    and marked with an ellipsis, rounded up so the inequality around it stays true; a
    shorter one is quoted whole. Trailing zeros are kept: with an ellipsis after them they
    are digits of the number, not padding, and `n = 68` ends in one.
    """
    quantized = _quantized(Decimal(value), places, ROUND_CEILING)
    if Decimal(value) == quantized:
        return value
    return f"{quantized:f}…"


def display_lower(value: str, places: int = 6) -> str:
    """A lower bound at `places`, rounded down for the same reason."""
    return format(_quantized(Decimal(value), places, ROUND_FLOOR), "f")


def display_gap(upper: str, lower: str, places: int = 4) -> str:
    """The width between two bounds, to nearest, with trailing zeros dropped when safe.

    `check_case_prose` re-derives a quoted gap at whatever precision the prose wrote it
    to, so dropping a trailing zero changes which precision is checked. It is dropped
    only when the shorter form still renders the same width.
    """
    with localcontext() as context:
        context.prec = BOUND_PRECISION
        difference = Decimal(upper) - Decimal(lower)
    full = format(_quantized(difference, places, ROUND_HALF_UP), "f")
    stripped = _strip_trailing_zeros(full)
    shorter = len(stripped.partition(".")[2])
    if Decimal(stripped) == _quantized(difference, shorter, ROUND_HALF_UP):
        return stripped
    return full


def _exact_difference(larger: str, smaller: str) -> str:
    """`larger - smaller` at the register's own 28 digits.

    Pinned rather than inherited: `decimal`'s context is process-global and
    `sqpack.field` raises it while refining an enclosure, so a generator running after
    one of those would otherwise print a longer rendering of the same number than
    `tests/test_verified_upper_bound_contract.py` recomputes.
    """
    with localcontext() as context:
        context.prec = 28
        return str(Decimal(larger) - Decimal(smaller))


# --------------------------------------------------------------------------------------
# The record
# --------------------------------------------------------------------------------------


def _witness_id(n: int) -> str:
    return f"W-known-best-n{n:03d}"


def _join_names(names: Sequence[str]) -> str:
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    return f"{', '.join(names[:-1])} and {names[-1]}"


def _credits_arslanov(facts: CatalogueFacts | None) -> bool:
    """Whether this case's finders are the authors of the retained Arslanov paper.

    Keyed on the credit rather than on a list of `n`, because the credit is what the
    resource is about: the seven entries the catalogue credits to all three authors
    (`132, 156, 182, 210, 241, 273, 307`) are the ones whose packings the paper
    publishes. The paper is dated 2021 and `found_year` stays 2019, which is when the
    page and the paper's own submission date the finding; the two are not in conflict.
    """
    return facts is not None and set(ARSLANOV_AUTHORS) <= set(facts.found_by)


def build_payload(
    n: int,
    *,
    source: SourceAvailability,
    facts: CatalogueFacts | None,
    review_date: str,
    retrieved_date: str,
    release: Mapping[int, UnitSquareRecord] | None = None,
    pictured_grid: bool = False,
) -> dict[str, Any]:
    """The `packing` payload for one case, under `packing.squares:SquarePackingCase/v2`.

    `pictured_grid` marks a grid case the catalogue lists with an integer side -- "119,
    120 ... s = 11, Proved by Hiroshi Nagamochi" -- which the register records exactly as
    it records `n = 47, 48, 62, 63, 79, 80, 98, 99`: a trivial grid, credited to nobody,
    with `catalogue_pictured` false, but vouched for by the register item rather than the
    completeness statement, because the catalogue does list the value.
    """
    if n < 1:
        raise GenerationError(f"n must be positive, got {n}")
    side = grid_ceiling(n)
    if source.is_grid:
        if source.trivial_grid_side is not None and source.trivial_grid_side != side:
            raise GenerationError(
                f"n={n}: source map says the grid side is {source.trivial_grid_side}, "
                f"but ceil(sqrt({n})) is {side}"
            )
        evidence = KINGBIRD_EVIDENCE if pictured_grid else grid_upper_evidence(n)
        reported_upper = _grid_reported_upper(n, side, retrieved_date, evidence=evidence)
    elif source.is_unitsquare:
        reported_upper = _unitsquare_reported_upper(
            n, _unitsquare_record(n, release), retrieved_date
        )
    else:
        if facts is None:
            raise GenerationError(f"n={n}: a catalogue case needs catalogue facts")
        if facts.n != n:
            raise GenerationError(f"n={n}: catalogue facts are for n={facts.n}")
        reported_upper = _catalogue_reported_upper(n, facts, retrieved_date)

    verified_upper = {
        "value": str(side),
        "exact_form": str(side),
        "evidence": [GRID_UPPER_EVIDENCE],
    }
    verified_lower = {
        "value": nagamochi_value(n, VERIFIED_SIGNIFICANT),
        "exact_form": nagamochi_exact_form(n),
        "evidence": [NAGAMOCHI_EVIDENCE],
    }
    reported_lower = _reported_lower(n, side)

    reported_value = str(reported_upper["value"])
    with localcontext() as context:
        context.prec = BOUND_PRECISION
        proved = Decimal(reported_value) == Decimal(str(verified_lower["value"]))
        trails = Decimal(str(verified_upper["value"])) > Decimal(reported_value)
    status = "proved" if proved else "open"

    if proved or source.is_unitsquare:
        # The release states `optimality_claimed: false` and offers a numerical
        # construction, so nothing on record conjectures that its side is the optimum --
        # which is why `n-068.md` and `n-069.md` leave this null.
        conjectured: str | None = None
    elif source.is_grid:
        # The grid case's best known side is an integer and the catalogue does not
        # picture it, so the conjecture on record is that the optimum is that integer --
        # which is what the hand-written grid cases say, in that one word.
        conjectured = "integer"
    else:
        conjectured = reported_value

    # The roll-up leads with whichever source reports the upper bound, which is not always
    # the catalogue: a grid case above 100 cites the completeness statement and a
    # UnitSquare case cites the release. Rebuilt as a new list rather than reusing the
    # bound's own, so that the YAML anchor stays between the bound and its blocker.
    upper_evidence = [str(ref) for ref in reported_upper["evidence"]]
    rollup = (
        [*upper_evidence, AREA_LOWER_EVIDENCE, GRID_UPPER_EVIDENCE, NAGAMOCHI_EVIDENCE]
        if reported_lower["kind"] == "perfect-square"
        else [*upper_evidence, NAGAMOCHI_EVIDENCE, GRID_UPPER_EVIDENCE]
    )
    blockers: list[dict[str, Any]] = []
    if trails:
        # The blocker's evidence is the *same list object* the reported upper bound
        # carries, which is how the hand-written records read and how they serialise
        # (one YAML anchor, one alias). `assurance.check_case_semantics` requires the
        # two to intersect; sharing the object makes that structural.
        blockers.append(
            {
                "kind": "source-evidence" if source.is_unitsquare else "mathematics",
                "detail": UNITSQUARE_BLOCKER if source.is_unitsquare else UPPER_GAP_BLOCKER,
                "evidence": reported_upper["evidence"],
            }
        )
    resources = [KINGBIRD_RESOURCE, FRIEDMAN_RESOURCE]
    if reported_lower["kind"] != "perfect-square":
        resources = [KINGBIRD_RESOURCE, NAGAMOCHI_RESOURCE, FRIEDMAN_RESOURCE]
    if source.is_unitsquare:
        resources = [KINGBIRD_RESOURCE, UNITSQUARE_RESOURCE, *resources[1:]]
    elif _credits_arslanov(facts):
        # Listed second, immediately after the catalogue, which is where `n-013.md` and
        # `n-011.md` list the paper behind a credit: the catalogue is still where the case
        # is looked up, and this is the retained report the credit rests on.
        resources = [KINGBIRD_RESOURCE, ARSLANOV_RESOURCE, *resources[1:]]
    priority_notes = (
        [] if facts is None else [note.as_payload() for note in facts.priority_notes]
    )

    return {
        "n": n,
        "reported_status": status,
        "status": status,
        "source_reviewed": review_date,
        "reported_upper_bound": reported_upper,
        "verified_upper_bound": verified_upper,
        "reported_lower_bound": reported_lower,
        "verified_lower_bound": verified_lower,
        # Not assessed. The escape screen and the rigidity assessment write this field
        # later in the promotion path; `null` here says nobody has looked, and never
        # that the packing can move.
        "rigidity": None,
        "conjectured_optimum": conjectured,
        "priority_notes": priority_notes,
        "evidence": rollup,
        "conflicts": _conflicts(source, facts),
        "blockers": blockers,
        "resources": [dict(resource) for resource in resources],
    }


def grid_upper_evidence(n: int) -> str:
    """Which Kingbird item vouches for an unpictured grid case at this `n`.

    Above the hand-authored range it is the completeness statement, which is what the
    catalogue actually says about a case it does not picture, and which is scoped
    `101..324` for that reason. At or below 100 it is the register, because that is what
    the hand-written unpictured grid cases cite and the completeness item is scoped out.
    The two are alternatives, never a pair: see this module's docstring.
    """
    return GRID_COMPLETENESS_EVIDENCE if n > HAND_AUTHORED_MAX else KINGBIRD_EVIDENCE


def _grid_reported_upper(
    n: int, side: int, retrieved_date: str, *, evidence: str | None = None
) -> dict[str, Any]:
    return {
        "value": str(float(side)),
        "exact_form": str(side),
        "algebraic_degree": None,
        "minimal_polynomial": None,
        "analytically_optimized": None,
        "catalogue_rigid": "not-stated",
        "construction_method": "trivial-grid",
        "tilt_angles_deg": [0],
        "found_by": [],
        "found_year": None,
        "improved_by": [],
        "catalogue_pictured": False,
        "source_key": KINGBIRD_SOURCE_KEY,
        "source_date": None,
        "retrieved_date": retrieved_date,
        "witnesses": [_witness_id(n)],
        "evidence": [grid_upper_evidence(n) if evidence is None else evidence],
    }


def catalogue_integer_side(facts: CatalogueFacts) -> int | None:
    """The catalogue side as an integer covering `facts.n`, else `None`.

    The builder's source plan treats such a case as an exact grid whatever the catalogue
    pictures, and the hand-authored register did the same at `n = 47, 48, 62, 63, 79,
    80, 98, 99`; this is the generator's side of that rule.
    """
    with localcontext() as context:
        context.prec = BOUND_PRECISION
        value = Decimal(facts.side_decimal)
        if value != value.to_integral_value():
            return None
        side = int(value)
    return side if side >= 1 and side * side >= facts.n else None


def _unitsquare_record(
    n: int, release: Mapping[int, UnitSquareRecord] | None
) -> UnitSquareRecord:
    """The release row for `n`, loading the retained release if the caller supplied none.

    Unlike the catalogue, which reaches this module through a dynamic import that may not
    resolve, the release is a retained JSON file in this checkout: there is nothing to
    degrade to, so it is read on demand rather than threaded through every caller.
    """
    rows = load_unitsquare_release() if release is None else release
    row = rows.get(n)
    if row is None:
        raise GenerationError(
            f"n={n} is assigned to {UNITSQUARE_AVAILABILITY_KEY} and the release reports "
            f"no result for it"
        )
    return row


def _unitsquare_reported_upper(
    n: int, record: UnitSquareRecord, retrieved_date: str
) -> dict[str, Any]:
    """The reported bound for a case the release, not the catalogue, is the source of.

    Every field is the release's or is fixed by what the release is. It publishes a side
    and a date and nothing else this schema asks for: no closed form, so the three
    algebraic fields are null; no analytic optimization, which is what
    `analytically_optimized: false` says; no rigidity claim, and `catalogue_rigid`
    transcribes the *catalogue*, which is not this record's source, so it stays
    `not-stated`; and no described method, so `construction_method` is `unknown`.
    """
    return {
        "value": record.offered_side,
        "exact_form": None,
        "algebraic_degree": None,
        "minimal_polynomial": None,
        "analytically_optimized": False,
        "catalogue_rigid": "not-stated",
        "construction_method": "unknown",
        "tilt_angles_deg": None,
        "found_by": [record.creator],
        "found_year": record.published_year,
        "improved_by": [],
        "catalogue_pictured": True,
        "source_key": UNITSQUARE_SOURCE_KEY,
        "source_date": record.published,
        "retrieved_date": retrieved_date,
        "witnesses": [_witness_id(n)],
        "evidence": [UNITSQUARE_EVIDENCE],
    }


def _conflicts(
    source: SourceAvailability, facts: CatalogueFacts | None
) -> list[dict[str, Any]]:
    """The typed conflicts this case's own sources force, which is at most one.

    A catalogue entry whose printed closed form does not evaluate to its printed decimal
    contradicts itself, and the contradiction is recorded rather than resolved: the
    decimal is transcribed, the form is not, and this says so in the record where a reader
    of `exact_form: null` would otherwise assume the page printed nothing.
    """
    if facts is None or source.is_unitsquare or facts.stale_exact_form is None:
        return []
    return [
        {
            "kind": "stale-source",
            "detail": (
                f"The catalogue prints the closed form `{facts.stale_exact_form}` beside "
                f"the decimal `{facts.side_decimal}`, and the form does not evaluate to "
                f"that decimal. The entry contradicts itself, so only the decimal is "
                f"transcribed: `exact_form`, `algebraic_degree` and `minimal_polynomial` "
                f"are left null rather than carrying a form this repository has checked "
                f"and found stale."
            ),
            "evidence": [KINGBIRD_EVIDENCE],
        }
    ]


def _catalogue_reported_upper(
    n: int, facts: CatalogueFacts, retrieved_date: str
) -> dict[str, Any]:
    if facts.construction_method not in CONSTRUCTION_PHRASES:
        raise GenerationError(
            f"n={n}: {facts.construction_method!r} is not a construction_method the "
            f"schema allows"
        )
    return {
        "value": facts.side_decimal,
        "exact_form": facts.exact_form,
        "algebraic_degree": facts.algebraic_degree,
        "minimal_polynomial": facts.minimal_polynomial,
        "analytically_optimized": facts.analytically_optimized,
        "catalogue_rigid": facts.catalogue_rigid,
        "construction_method": facts.construction_method,
        "tilt_angles_deg": None,
        "found_by": list(facts.found_by),
        "found_year": facts.found_year,
        "improved_by": list(facts.improved_by),
        "catalogue_pictured": facts.catalogue_pictured,
        "source_key": KINGBIRD_SOURCE_KEY,
        "source_date": None,
        "retrieved_date": retrieved_date,
        "witnesses": [_witness_id(n)],
        "evidence": [KINGBIRD_EVIDENCE],
    }


def _reported_lower(n: int, side: int) -> dict[str, Any]:
    if is_perfect_square(n):
        return {
            "value": str(float(side)),
            "exact_form": None,
            "kind": "perfect-square",
            "proved_by": [],
            "proved_year": None,
            "source_key": None,
            "note": None,
            "scope": None,
            "evidence": [AREA_LOWER_EVIDENCE],
        }
    return {
        "value": nagamochi_value(n, REPORTED_SIGNIFICANT),
        "exact_form": None,
        "kind": "nagamochi",
        "proved_by": ["Hiroshi Nagamochi"],
        "proved_year": 2005,
        "source_key": "[Nagamochi 2005]",
        "note": NAGAMOCHI_NOTE,
        "scope": None,
        "evidence": [NAGAMOCHI_EVIDENCE],
    }


# --------------------------------------------------------------------------------------
# The prose
# --------------------------------------------------------------------------------------


def _release_date_words(published: str) -> str:
    """`2026-07-29` as `29 July 2026`, the way the two hand-written records date it.

    Assembled rather than formatted with `%-d`, which is a platform extension and is not
    portable, and with the month name taken from a fixed table rather than the process
    locale, which would otherwise decide what this record says.
    """
    date = dt.date.fromisoformat(published)
    return f"{date.day} {MONTH_NAMES[date.month - 1]} {date.year}"


def _unitsquare_packing_section(n: int, record: UnitSquareRecord, parent: str) -> list[str]:
    """The packing paragraph for a case whose number comes from a first-party release.

    It says four things, in the order `n-068.md` says them: what the release improved and
    by how much, what the release claims about its own validation, what it does not
    publish, and what this repository therefore records. `parent` names the catalogue
    credit chain the release cites, which is the one part of the paragraph the release
    itself does not carry.
    """
    side = grid_ceiling(n)
    return [
        (
            f"The UnitSquare Project’s {_release_date_words(record.published)} release "
            f"improves the public {parent} parent by `{record.absolute_reduction}`."
        ),
        (
            "The release classifies the result as a construction-only upper bound and "
            "says it used outward-rounded interval arithmetic, a 300-digit "
            "zero-tolerance recomputation, and an independent published checker."
        ),
        (
            "The public release does not include the interval boxes, governed receipt, "
            "or replayable checker needed to inspect the formal claim."
        ),
        "We therefore record the value as reported.",
        f"The formal lane retains the exact `{side} × {side}` grid construction.",
    ]


def _method_owner(
    facts: CatalogueFacts | None, method: str, found_by: Sequence[str]
) -> str | int | None:
    """Which of the credit line's sentences the construction method belongs to.

    `"finder"` for the sentence that names `found_by`, an index into
    `facts.improvements` for a dated improvement, `None` for a method the line states
    somewhere neither of those, which the prose then writes without an owner.

    The two fallbacks to `"finder"` are the shapes where joining the method to the credit
    asserts nothing false. `unknown` is one: "via an unrecorded method" adds no claim to
    whatever precedes it. A caller with no credit line is the other: nothing can be
    attributed, and this is the reading the corpus already carries.
    """
    if facts is None or facts.credit_line is None or method == "unknown":
        return "finder"
    _, sentence = credit_method_match(facts.credit_line)
    if sentence is None:
        return "finder"
    for index, improvement in enumerate(facts.improvements):
        if improvement.sentence == sentence:
            return index
    sentences = credit_sentences(facts.credit_line)
    if not found_by:
        # No name to miscredit, so the method stays on the opening statement, which is
        # where the corpus has always carried it.
        return "finder"
    credited = next(
        (
            index
            for index, text in enumerate(sentences)
            if all(name in text for name in found_by)
        ),
        None,
    )
    return "finder" if credited is None or credited == sentence else None


def _packing_section(
    n: int, payload: Mapping[str, Any], facts: CatalogueFacts | None = None
) -> list[str]:
    """The "The packing" paragraph for a catalogue case.

    The finder and the method are separate statements unless the page puts them in the
    same sentence. They follow different conventions -- `found_by` is the page's first
    credit, `construction_method` is what produced the *printed* side -- so the one
    sentence the corpus used to write, "Found by <finder> in <year>, via <method>", read
    the two as one claim and asserted something no page says: at the seven Arslanov
    cases it credited a March 2019 analytic construction to a January 2026 annealing run.
    `_method_owner` decides which credit the method hangs off, from where the phrase that
    named it sits, and a method the line states outside any credit is written with no
    owner at all.

    The improvement dates are the page's own words and reach the reader only here: the
    schema closes `additionalProperties` on `reported_upper_bound`, so `improved_by`
    carries the names and nothing carries the date.
    """
    reported = payload["reported_upper_bound"]
    if not reported["catalogue_pictured"]:
        side = grid_ceiling(n)
        return [
            (
                f"The record catalogue does not picture `n = {n}`: no arrangement has "
                f"ever been found that beats the trivial `⌈√{n}⌉ = {side}` grid, so the "
                f"grid is still the best known packing."
            ),
            "That is a statement about what has been searched, not a proof.",
        ]

    method = CONSTRUCTION_PHRASES[reported["construction_method"]]
    names = _join_names(reported["found_by"])
    year = reported["found_year"]
    owner = _method_owner(facts, str(reported["construction_method"]), reported["found_by"])
    if not names:
        credit = "Found by an unrecorded author"
    elif year is None:
        credit = f"Found by {names}"
    else:
        credit = f"Found by {names} in {year}"
    lines = [f"{credit}, via {method}." if owner == "finder" else f"{credit}."]
    improvements = () if facts is None else facts.improvements
    for index, improvement in enumerate(improvements):
        improved = f"Improved by {_join_names(improvement.names)} in {improvement.when}"
        lines.append(f"{improved}, via {method}." if owner == index else f"{improved}.")
    if not improvements and reported["improved_by"]:
        # A caller that handed in facts without the credit line they came from: the names
        # are on record and their dates are not, which is the sentence the corpus wrote
        # before the dates were read.
        lines.append(f"Later improved by {_join_names(reported['improved_by'])}.")
    if owner is None:
        subject = CONSTRUCTION_SUBJECTS[reported["construction_method"]]
        lines.append(f"The recorded construction method is {subject}.")
    if reported["algebraic_degree"] is not None:
        lines.append(
            f"Its side length is algebraic of degree **{reported['algebraic_degree']}** "
            f"over `ℚ`."
        )
    return lines


def _nagamochi_lower_section(n: int) -> list[str]:
    default = (
        NAGAMOCHI_DEFAULT_COUNTED if n <= HAND_AUTHORED_MAX else NAGAMOCHI_DEFAULT_UNCOUNTED
    )
    return [
        "Nothing specific to this `n` has ever been proved.",
        "The bound is Nagamochi’s general closed form, which applies to every `N ≥ 4`:",
        "",
        "```",
        NAGAMOCHI_DISPLAY,
        "```",
        "",
        default,
    ]


def _ceiling_section(n: int, payload: Mapping[str, Any]) -> list[str]:
    verified = str(payload["verified_upper_bound"]["value"])
    reported = str(payload["reported_upper_bound"]["value"])
    return [
        "## The verified upper bound is a ceiling",
        "",
        (
            f"`verified_upper_bound` for this case is `{verified}`, which is **larger** "
            f"than the best known `{reported}` two fields above it."
        ),
        (
            "It is not a tighter reading of the same packing and it is not the value of "
            f"`s({n})`: it is the strongest ceiling this repository can certify from its "
            f"own evidence — the trivial grid bound `⌈√{n}⌉ = {verified}` — and it trails "
            f"the reported construction by `{_exact_difference(verified, reported)}`."
        ),
        "",
        (
            f"Its `exact_form` is the exact form of that ceiling, never of `s({n})`. "
            f"`s({n})` is not known exactly; `status` stays `open`, and the `mathematics` "
            "blocker in the frontmatter names the gap. Read `reported_upper_bound` for "
            "the best known side length."
        ),
        "",
    ]


def render_body(
    n: int,
    payload: Mapping[str, Any],
    *,
    packing_lines: Sequence[str] | None = None,
    facts: CatalogueFacts | None = None,
) -> str:
    """The reader-facing half of the record, wrapped the way every other document here is.

    `packing_lines` replaces the templated "The packing" paragraph for a case whose source
    is not the catalogue. The payload alone cannot write that paragraph: it says nothing
    about how much a release improved on its parent, or whose parent it was. `facts`
    carries the two things the payload also cannot say about a catalogue case -- when each
    improvement happened, and which credit the construction method belongs to.
    """
    side = grid_ceiling(n)
    reported_value = str(payload["reported_upper_bound"]["value"])
    verified_lower_value = str(payload["verified_lower_bound"]["value"])
    first_party = payload["reported_upper_bound"]["source_key"] != KINGBIRD_SOURCE_KEY
    lines: list[str] = []

    if payload["status"] == "proved":
        lines.append(f"# `s({n})` — solved")
        lines.append("")
        if is_perfect_square(n):
            lines.append(f"`s({n}) = {side}`. Established by triviality (a perfect square).")
        else:
            lines.append(
                f"`s({n}) = {side}`. Established by Nagamochi’s general theorem, "
                "Hiroshi Nagamochi (2005)."
            )
            lines.append(f"General closed form: {NAGAMOCHI_NOTE.split(': ', 1)[1]}")
        lines.append("")
    else:
        lines.append(f"# `s({n})` — open")
        lines.append("")
        # A first-party release publishes its own digits, so the sentence quotes them
        # rather than the eight places a catalogue entry prints; "published" is the word
        # the two hand-written records of that shape use for the distinction.
        known = "published packing" if first_party else "packing"
        shown = (
            display_first_party_upper(reported_value)
            if first_party
            else display_upper(reported_value)
        )
        lines.append(
            f"Open. The best known {known} gives `s({n}) ≤ "
            f"{shown}`, and the best proved lower bound is "
            f"`{display_lower(verified_lower_value)}` from Nagamochi’s general theorem, "
            f"leaving a gap of `{display_gap(reported_value, verified_lower_value)}`. "
            f"General closed form: {NAGAMOCHI_NOTE.split(': ', 1)[1]}"
        )
        lines.append("")
        if payload["blockers"]:
            lines.extend(_ceiling_section(n, payload))

    lines.append("## The packing")
    lines.append("")
    lines.extend(
        _packing_section(n, payload, facts) if packing_lines is None else packing_lines
    )
    lines.append("")
    lines.append("## The lower bound")
    lines.append("")
    if is_perfect_square(n):
        lines.append(
            f"`{n}` is a perfect square, so the `{side}×{side}` grid is optimal and the "
            "area bound `√n` is already tight."
        )
    else:
        lines.extend(_nagamochi_lower_section(n))
    lines.append("")
    lines.append(COMMON_DOC_FOOTER)

    # Formatted in process by the Python build of the same formatter the pre-commit hook
    # runs, so a generated record arrives already wrapped the way the register is and the
    # hook has nothing to restage. `render_explainer.py` loads it the same way and for
    # the same reason: a network fetch inside a generator would make it depend on an
    # index being reachable.
    from flowmark import reformat_text  # noqa: PLC0415

    return reformat_text("\n".join(lines), semantic=True, cleanups=True)


def render_record(
    payload: Mapping[str, Any],
    *,
    packing_lines: Sequence[str] | None = None,
    facts: CatalogueFacts | None = None,
) -> str:
    """One complete `n-NNN.md`: front matter, then the prose that restates it."""
    n = int(payload["n"])
    document = {
        "title": f"s({n}) — square packing case",
        "softschema": {
            "contract": "packing.squares:SquarePackingCase/v2",
            "schema": "square-packing-case.schema.yaml",
            "envelope": "packing",
            "status": "enforced",
        },
        "packing": dict(payload),
    }
    front = yaml.safe_dump(document, allow_unicode=True, sort_keys=False, width=96)
    body = render_body(n, payload, packing_lines=packing_lines, facts=facts)
    return f"---\n{front}---\n{body}"


def generate_record(
    n: int,
    *,
    availability: Mapping[int, SourceAvailability],
    catalogue: Mapping[int, CatalogueFacts] | None,
    review_date: str,
    retrieved_date: str,
    release: Mapping[int, UnitSquareRecord] | None = None,
) -> str:
    """Draft the complete record text for one `n`."""
    source = availability.get(n)
    if source is None:
        raise GenerationError(
            f"n={n} has no row in the source map; the map covers "
            f"{min(availability)}..{max(availability)}"
        )
    facts: CatalogueFacts | None = None
    if not source.is_grid:
        # A UnitSquare case still reads the catalogue, for one sentence of prose rather
        # than for its bound: the release names its parent by URL, and the catalogue's
        # credit chain is where that parent's authors are written down.
        if catalogue is None and not source.is_unitsquare:
            raise GenerationError(f"n={n} is a catalogue case and no catalogue was supplied")
        facts = None if catalogue is None else catalogue.get(n)
        if facts is None and not source.is_unitsquare:
            raise GenerationError(f"n={n} is a catalogue case and the catalogue has no entry")
    pictured_grid = False
    if facts is not None and not source.is_unitsquare:
        integer_side = catalogue_integer_side(facts)
        if integer_side is not None:
            # A pictured grid: recorded as the trivial grid, as the hand-authored register
            # records its own pictured integer-side cases (see `build_payload`).
            source = replace(
                source, classification=GRID_CLASSIFICATION, trivial_grid_side=integer_side
            )
            facts = None
            pictured_grid = True
    payload = build_payload(
        n,
        source=source,
        facts=facts,
        review_date=review_date,
        retrieved_date=retrieved_date,
        release=release,
        pictured_grid=pictured_grid,
    )
    packing_lines: list[str] | None = None
    if source.is_unitsquare:
        names = credited_surnames(None if facts is None else facts.credit_line)
        packing_lines = _unitsquare_packing_section(
            n,
            _unitsquare_record(n, release),
            "-".join(names) if names else "cited",
        )
    return render_record(payload, packing_lines=packing_lines, facts=facts)


# --------------------------------------------------------------------------------------
# Writing, and refusing to
# --------------------------------------------------------------------------------------


def record_path(out_dir: Path, n: int) -> Path:
    return out_dir / f"n-{n:03d}.md"


def refuse_reason(n: int, out_dir: Path, *, force: bool) -> str | None:
    """Why this `n` may not be written to `out_dir`, or `None` if it may."""
    into_register = out_dir.resolve() == FRONTIER.resolve()
    if n <= HAND_AUTHORED_MAX and into_register:
        return (
            f"n={n} is hand-authored; the generator does not write n <= "
            f"{HAND_AUTHORED_MAX} into {FRONTIER.name}/. Generate it into another "
            f"directory to compare against what a person wrote."
        )
    if n > CATALOGUE_COMPLETENESS_MAX:
        return (
            f"n={n} is past {CATALOGUE_COMPLETENESS_MAX}, where the catalogue's "
            f"completeness statement stops: no source vouches for the grid there."
        )
    target = record_path(out_dir, n)
    if target.exists() and not force:
        return f"{target} exists; pass --force to overwrite it"
    return None


def _existing_dates(path: Path, review_date: str, retrieved_date: str) -> tuple[str, str]:
    """The review and retrieval dates a record already carries, for `--check`.

    Both are caller-supplied and neither is derivable, so regenerating with today's date
    would report every record as drifted on the day after it landed. Checking a record
    against itself means reusing the dates it declares.
    """
    document = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])
    payload = document.get("packing")
    if not isinstance(payload, Mapping):
        return review_date, retrieved_date
    reported = payload.get("reported_upper_bound")
    retrieved = (
        reported.get("retrieved_date") if isinstance(reported, Mapping) else None
    ) or retrieved_date
    return str(payload.get("source_reviewed") or review_date), str(retrieved)


def without_rigidity(text: str) -> str:
    """One record's text with its `packing.rigidity` block removed.

    The generator writes `rigidity: null` and the promotion path replaces it: the
    translation-escape screen and `devtools/assess_frontier_rigidity.py` run after this
    tool and re-serialise the block at their own YAML width, so a promoted record can
    never be byte-identical to a fresh draft of itself in that one field. `--check`
    therefore compares everything except it. This is the same allowance the golden test
    already makes -- `NOT_REPRODUCED` names `packing.rigidity` and nothing else -- and
    without it every promoted record would report as drift and the check would find none.
    """
    kept: list[str] = []
    dropping = False
    for line in text.splitlines(keepends=True):
        if line.startswith("  rigidity:"):
            dropping = True
            continue
        if dropping:
            if line.startswith("    "):
                continue
            dropping = False
        kept.append(line)
    return "".join(kept)


def write_record(text: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_text(text, encoding="utf-8")


def diff_record(existing: str, generated: str, name: str) -> list[str]:
    return list(
        difflib.unified_diff(
            existing.splitlines(),
            generated.splitlines(),
            fromfile=f"{name} (committed)",
            tofile=f"{name} (generated)",
            lineterm="",
        )
    )


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------


def method_summary(
    cases: Iterable[int],
    availability: Mapping[int, SourceAvailability],
    catalogue: Mapping[int, CatalogueFacts] | None,
) -> list[str]:
    """One line per `construction_method` drafted, and the roll of the ones left `unknown`.

    The unknown roll is the point of it. `unknown` is a real reading -- the catalogue's
    credit line said nothing this tool recognises -- but it is also the value a reviewer
    has to visit, so a run says which cases it is handing them rather than burying the
    count in 224 files.
    """
    methods: dict[str, list[int]] = {}
    for n in cases:
        source = availability.get(n)
        if source is None:
            continue
        if source.is_grid:
            method = "trivial-grid"
        elif source.is_unitsquare:
            method = "unknown"
        else:
            facts = None if catalogue is None else catalogue.get(n)
            method = "unknown" if facts is None else facts.construction_method
        methods.setdefault(method, []).append(n)
    lines = [
        f"construction_method {method}: {len(found)}"
        for method, found in sorted(methods.items(), key=lambda item: (-len(item[1]), item[0]))
    ]
    unknown = methods.get("unknown", [])
    if unknown:
        listed = ", ".join(str(n) for n in unknown)
        lines.append(f"unresolved construction_method at n = {listed}")
    return lines


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--n", type=int, help="generate this single case")
    selection.add_argument(
        "--range",
        nargs=2,
        type=int,
        metavar=("FIRST", "LAST"),
        help="generate every case in this inclusive range",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=FRONTIER,
        help="directory to write into (default: the frontier register)",
    )
    parser.add_argument(
        "--force", action="store_true", help="overwrite records that already exist"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="regenerate into a temporary directory and report any drift; writes nothing",
    )
    parser.add_argument(
        "--review-date",
        default=dt.datetime.now(tz=dt.UTC).date().isoformat(),
        help="source_reviewed for generated records (default: today, UTC)",
    )
    parser.add_argument(
        "--retrieved-date",
        default=None,
        help="reported_upper_bound.retrieved_date (default: the review date)",
    )
    parser.add_argument(
        "--availability", type=Path, default=None, help="override the source map path"
    )
    parser.add_argument(
        "--catalogue", type=Path, default=None, help="override the catalogue transcription path"
    )
    return parser.parse_args(argv)


def selected(args: argparse.Namespace) -> list[int]:
    if args.n is not None:
        return [int(args.n)]
    first, last = (int(value) for value in args.range)
    if last < first:
        raise GenerationError(f"--range {first} {last} is empty")
    return list(range(first, last + 1))


def _check(
    cases: Iterable[int],
    args: argparse.Namespace,
    availability: Mapping[int, SourceAvailability],
    catalogue: Mapping[int, CatalogueFacts] | None,
) -> int:
    """Regenerate each case into a temporary directory and diff it against the register."""
    problems = 0
    checked = 0
    with tempfile.TemporaryDirectory(prefix="frontier-check-") as scratch:
        scratch_dir = Path(scratch)
        for n in cases:
            existing_path = record_path(args.out, n)
            if not existing_path.exists():
                print(f"n={n}: no record at {existing_path} to check")
                problems += 1
                continue
            existing = existing_path.read_text(encoding="utf-8")
            review, retrieved = _existing_dates(
                existing_path, args.review_date, args.retrieved_date or args.review_date
            )
            generated = generate_record(
                n,
                availability=availability,
                catalogue=catalogue,
                review_date=review,
                retrieved_date=retrieved,
            )
            write_record(generated, record_path(scratch_dir, n))
            checked += 1
            comparable = without_rigidity(existing)
            drafted = without_rigidity(generated)
            if drafted != comparable:
                problems += 1
                print("\n".join(diff_record(comparable, drafted, existing_path.name)))
    print(f"checked {checked} record(s); {problems} disagree with the generator")
    return 1 if problems else 0


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        cases = selected(args)
        availability = load_availability(args.availability)
        needs_catalogue = any(n in availability and not availability[n].is_grid for n in cases)
        catalogue = load_catalogue(args.catalogue) if needs_catalogue else None

        if args.check:
            return _check(cases, args, availability, catalogue)

        for line in method_summary(cases, availability, catalogue):
            print(line)
        retrieved = args.retrieved_date or args.review_date
        written = 0
        for n in cases:
            reason = refuse_reason(n, args.out, force=args.force)
            if reason is not None:
                print(f"refused: {reason}")
                return 1
            text = generate_record(
                n,
                availability=availability,
                catalogue=catalogue,
                review_date=args.review_date,
                retrieved_date=retrieved,
            )
            write_record(text, record_path(args.out, n))
            written += 1
    except GenerationError as error:
        print(f"error: {error}")
        return 1
    print(f"wrote {written} record(s) to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
