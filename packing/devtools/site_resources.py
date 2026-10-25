"""Curated external resources shared by homepage cards and person profiles.

These records describe cited work, independently of each person's account links.
Only the curated byline establishes a person/resource relationship.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from functools import cache
from typing import Any, Literal
from urllib.parse import urlsplit

from devtools.profile_links import ProfileIndex, named_profile_ids, public_index
from sqpack.contributors import record_metadata

#: The other public square-packing projects on GitHub that the research frontier cites:
#: each repository's home (a gist's, at no revision, for a source published as a gist),
#: its author as the record credits them (the GitHub handle where the record names no
#: one), and what it holds. A test holds this list to cover every source repository in
#: the source-coverage register.
OTHER_PROJECTS: tuple[tuple[str, str, str], ...] = (
    (
        "https://github.com/SidG2k1/square-packing-refinements",
        "Siddharth Gupta",
        (
            "Seventeen rational refinements of Nate Chaoweeraprasit's SQUISH packings, "
            "using Evan Daniel's optimizer; fourteen finite upper-bound improvements selected "
            "here (T-127) and three withdrawn. Exact feasibility is confirmed with "
            "independently re-implemented code; optimality is not established."
        ),
    ),
    (
        "https://github.com/ry-xu/square_packing",
        "Ryan Xu",
        (
            "Complete rational packings and an undilated radical n = 51 construction; "
            "finite feasibility is confirmed here (T-125, T-126)."
        ),
    ),
    (
        "https://github.com/ry-xu/square_packing/blob/8dc415296f697f5140caea27c7a0193d52deb4e6/square_packing_records.json",
        "Ryan Xu",
        "The complete source report retained for the rational packing comparisons.",
    ),
    (
        "https://github.com/wand125/square-packing",
        "Hiroaki Hosono",
        "Canonical certificate and checker repository; historical source pins remain valid.",
    ),
    (
        "https://github.com/wand125/square-packing-tools",
        "Hiroaki Hosono",
        (
            "Tools for Tokoharu's rectangle-density solver, and an exact point and "
            "threshold-charge row checker."
        ),
    ),
    (
        "https://github.com/lollipoll/couzo-five-exact-certificates",
        "Seth Rehwaldt",
        (
            "Rational refinements of Couzo's packings; complete finite certificates at "
            "n = 105 and 292 are replayed here (T-117)."
        ),
    ),
    (
        "https://github.com/lollipoll/certified-square-packing-68",
        "Seth Rehwaldt",
        (
            "An exact finite rational refinement of Couzo's n = 68 packing, replayed "
            "here (T-118). Its analytic root and dual programs remain outside that replay."
        ),
    ),
    (
        "https://github.com/evand/square-packing",
        "Evan Daniel",
        (
            "Exact covers settling n = 21, 32, 45 and 60, and s(k\u00b2 \u2212 3) = k for every"
            " k \u2265 6; s(k\u00b2 \u2212 4) = k awaits its replay here."
        ),
    ),
    (
        "https://github.com/squarepacker/s12-lower-bound",
        "Ryu Sungjoon",
        (
            "Evan Daniel's s(12) points rescaled and then re-weighted, the lower bound"
            " s(12) \u2265 7943/2000 for twelve squares."
        ),
    ),
    (
        "https://github.com/wand125/square-packing-bounds",
        "Hiroaki Hosono",
        "Weighted point and rectangle-density lower-bound certificates across many n.",
    ),
    (
        "https://github.com/wand125/valid7-independent-check",
        "Hiroaki Hosono",
        "A second, independent exact checker of Valid7, the finite step of s(k² \u2212 3) = k.",
    ),
    (
        "https://github.com/tokoharu/square-packing-density-bounds",
        "Tokoharu",
        "Rectangle-density lower-bound certificates.",
    ),
    (
        "https://github.com/franciscouzo/square-packing",
        "Francisco Couzo",
        (
            "Improved packings for 49 counts from n = 68 to 307. "
            "Exact rational certificates at 204 and 260 (T-223), replayed and reviewed "
            "here, supplied earlier house packings; Daniel's regularized views (T-225) "
            "have since replaced them. The earlier refinements of issue451 (T-128) and "
            "their follow-up (T-130), replayed here, have also been superseded."
        ),
    ),
    (
        "https://github.com/itsnaka/squish-certs",
        "Nate Chaoweeraprasit",
        "Exact rational certificates for SQUISH upper-bound packings.",
    ),
    (
        "https://github.com/TheSnakeFang/squarepack-certs",
        "Kevin Fang",
        (
            "Two-wedge packings of 308, 343 and 344 squares with exact certificates; the"
            " 308, below the grid, is replayed here (T-135)."
        ),
    ),
    (
        "https://github.com/TheSnakeFang/squarepack-lean",
        "Kevin Fang",
        (
            "A Lean 4 proof of Fang\u2019s Theorem 1, s(n\u00b2 \u2212 n + 1) < n for every"
            " n \u2265 15, and of the single-step bounds of his Theorem 2 (T-163); not built"
            " here."
        ),
    ),
    (
        "https://github.com/ebdeleeuw/square-packing-n70",
        "Eric Deleeuw",
        "An exact rational refinement of Ryan Xu's packing of 70 squares (T-137).",
    ),
    (
        "https://github.com/Mishapolk/square-packing-records",
        "Mishapolk",
        (
            "Decimal packings at 48 counts; exact witnesses derived here prove the printed"
            " sides at the 30 within the corpus (T-138)."
        ),
    ),
    (
        "https://github.com/Mishapolk/square-packing-records/blob/12fc46678fa8eefa3f156ff37dfffd84c8f3a580/certificates/n204.cert",
        "Mykhailo Polkovskyi",
        (
            "The lower of the two 204 certificates issue 719's release published, retained"
            " and replayed here, and the house best packing at 204 (T-231)."
        ),
    ),
    (
        "https://github.com/BuddenPing/square-packing-certificates",
        "PingYou Ltd",
        (
            "Exact rational packings of 207 and 153 squares built from Ryan Xu's packing of"
            " 70, both replayed here (T-147, T-148)."
        ),
    ),
    (
        "https://github.com/dostashev/square-packing",
        "Daniil Ostashev",
        (
            "New packings of 155, 156, 175, 211, 232 and 264 squares with exact"
            " certificates and a GMP checker; all six are replayed here (T-149, T-158)."
        ),
    ),
    (
        "https://github.com/riocalle/my-repo",
        "Rio Calle",
        (
            "A decimal layout of 102 squares, another arrangement of Ryan Xu's design;"
            " certified here from the layout (T-159)."
        ),
    ),
    (
        "https://github.com/BuddenPing/squares",
        "PingYou Ltd",
        (
            "Pull request #574's tighter certificates of others' packings, recorded at 68"
            " counts and replayed at every one of them here (T-174)."
        ),
    ),
    (
        "https://github.com/bengreff/s76-certificate",
        "Benjamin Greff",
        (
            "A mixed cover of points and grid-line segments for s(76) = 9, with the run"
            " records of both checkers; reported, its census replayed in triage (T-184)."
        ),
    ),
    (
        "https://github.com/bengreff/s95-certificate",
        "Benjamin Greff",
        (
            "A mixed cover of points and grid-line segments for s(95) = 10, with the run"
            " records of both checkers; reported, both checkers replayed in triage (T-191)."
        ),
    ),
    (
        "https://github.com/RobertBarnettProjects/square-packing-research",
        "Robert Barnett",
        (
            "Exact rational refinements of Ryan Xu's packings of 146 and 261 squares,"
            " replayed here (T-150)."
        ),
    ),
    (
        "https://github.com/griffcass/square-packing",
        "Griffin Casson",
        "Improved packings for n = 103, 105 and other cases.",
    ),
    (
        "https://github.com/JoostdeWinter/square-packing-211",
        "Joost de Winter",
        "A packing of 211 squares in a square of side under 15.",
    ),
    (
        "https://github.com/JoostdeWinter/square-packing",
        "Joost de Winter",
        (
            "Exact rational certificates for 227, 229 and 260 squares, replayed and "
            "reviewed here (T-196). The house packing at 260 was replaced by T-223 on "
            "21 October; Daniel's regularized views (T-225) now supply the house "
            "packings at 227, 229 and 260."
        ),
    ),
    (
        "https://github.com/JoostdeWinter/joostdewinter.github.io",
        "Joost de Winter",
        (
            "Nineteen exact rational certificates beyond 324 squares, at 464 and from 509"
            " to 1568 below the integer grid (#666); the eleven at or below 1024 are"
            " replayed here as dated rows beyond the case corpus."
        ),
    ),
    (
        "https://github.com/Queuingtheorydotcom/11SquaresOptimal",
        "Manasseh Ahmed",
        "A computer-assisted proof that Trump's packing of eleven squares is optimal.",
    ),
    (
        "https://github.com/Queuingtheorydotcom/11SquaresFormalized",
        "Manasseh Ahmed et al.",
        "A Lean 4 formalization of that proof, trusting Lean's compiler for its certificates.",
    ),
    (
        "https://github.com/Kleddamag/11-squares-certified-bound",
        "Marc Leonard Overbeck",
        "A certified lower bound for eleven squares.",
    ),
    (
        "https://github.com/Esummins/packing",
        "E. Summins",
        (
            "The n = 11 lab's simple-square stratification series, with a replay of "
            "Overbeck's eleven-square certificate."
        ),
    ),
    (
        "https://github.com/chelokot/square-packing-archive",
        "chelokot",
        "A counterexample to Nagamochi's scoring lemma, and a Lean proof that s(k^2 - 2) = k.",
    ),
    (
        "https://github.com/Kleddamag/17-squares-certified-bound",
        "Marc Leonard Overbeck",
        "Certified lower bounds for seventeen squares.",
    ),
    (
        "https://github.com/Kleddamag/the-seventeenth-square-candidate",
        "Marc Leonard Overbeck",
        "A candidate proof that Bidwell's packing of seventeen squares is optimal.",
    ),
    (
        "https://github.com/ofitzharding/sq17-lean",
        "Oscar Fitzharding",
        (
            "A Lean 4 proof that Bidwell's packing of seventeen squares is optimal, "
            "trusting Lean's compiler for its certificates."
        ),
    ),
    (
        "https://github.com/ofitzharding/sq19",
        "Oscar Fitzharding",
        (
            "A Lean 4 proof that Wainwright's packing of nineteen squares is optimal, "
            "trusting Lean's compiler for its certificates."
        ),
    ),
    (
        "https://github.com/Guzhou0806/n17-square-packing",
        "Guzhou0806",
        "Strict lower bounds for seventeen squares.",
    ),
    (
        "https://github.com/Guzhou0806/n40-square-packing",
        "Guzhou0806",
        "Strict lower bounds for forty squares, on densities grown from Hosono's.",
    ),
    (
        "https://github.com/DRMacIver/square-packing-research",
        "David R. MacIver",
        "A lower bound for seventeen squares, with its paper and a Lean check.",
    ),
    (
        "https://github.com/ahyangyi/17squares",
        "ahyangyi",
        "A lower-bound proof for seventeen squares.",
    ),
    (
        "https://github.com/anabologyco-maker/square17-lower-bound",
        "anabologyco-maker",
        "A weighted fractional lower bound for seventeen squares.",
    ),
    (
        "https://github.com/BalthasarStrauss/Squares-packing_S-29-_New-Record",
        "Thomas Schadt",
        "A record packing of 29 squares.",
    ),
    (
        "https://gist.github.com/amundsk/78f9f0e7b4669f2f509a281845081768",
        "Amund Kristiansen",
        (
            "An exact certificate for 303 squares, another arrangement of Evan Daniel's"
            " packing found from it, replayed and reviewed here (T-239)."
        ),
    ),
    (
        "https://gist.github.com/amundsk/e4df936fb09c68446598d4c8309d0166",
        "Amund Kristiansen",
        (
            "Exact certificates for fourteen counts from 334 to 504, each, the author says,"
            " found from the packing at the count in Francisco Couzo's 964ee2b index (#763);"
            " twelve are rows beyond the corpus."
        ),
    ),
)

#: David Ellsworth's Squares in Squares catalogue, the record's `[Kingbird]`.
KINGBIRD = "https://kingbird.myphotos.cc/packing/squares_in_squares.html"

#: The catalogues of the record packings, which lead the Other Square Packing
#: Projects section in this order, ahead of the ranked cards (the owner, 2026-10-05,
#: `think-lvhh`): each one's address, its name, its maintainer as the record credits
#: them, and what it holds. Ellsworth's catalogue is the baseline of every upper bound
#: (`kingbird-current` in the source-coverage register). Erich Friedman's original page
#: is the one the catalogue's header credits, at the archived address that header links
#: (`resources/web/kingbird-squares-in-squares.md`). Evan Daniel's atlas is the
#: bibliography's `[evand square packing atlas 2026-10-04]`.
CATALOGUE_SITES: tuple[tuple[str, str, str, str], ...] = (
    (
        KINGBIRD,
        "Squares in Squares",
        "David Ellsworth after Erich Friedman",
        (
            "The catalogue of record packings, with their exact sides and histories: the"
            " baseline of every upper bound here."
        ),
    ),
    (
        "https://web.archive.org/web/20230530194618/https://erich-friedman.github.io/packing/squinsqu/",
        "Erich\u2019s Packing Center",
        "Erich Friedman",
        (
            "The original Squares in Squares page, as archived on 30 May 2023, which"
            " Ellsworth\u2019s catalogue continues."
        ),
    ),
    (
        "https://evand.github.io/square-packing/",
        "Square Packing Atlas",
        "Evan Daniel",
        (
            "Every record packing drawn beside the proven floor beneath it, with a page of"
            " open problems."
        ),
    ),
)

#: Other cited result pages, including first-party GitHub issue reports, ranked with the
#: projects on GitHub: each one's address, its name (a post's is its title, as the post
#: gives it), its author as the record credits them, and what it holds. They are the
#: source-coverage register's three sources off GitHub that are not a catalogue,
#: UnitSquare's release and Wang and Li's and Fang's Zenodo records, and the two posts behind
#: Burns's and Massaccesi's n = 17 bound, whose key the register credits with T-015 and
#: T-016 and the case records cite. A test holds every source the coverage register
#: reviews to a card, here or in `OTHER_PROJECTS`, and every address here and in
#: `CATALOGUE_SITES` to one the record cites.
OTHER_SITES: tuple[tuple[str, str, str, str], ...] = (
    (
        "https://github.com/jlevy/squares/issues/401#issuecomment-6031977107",
        "SQUISH Packing of 153 Squares",
        "Nate Chaoweeraprasit",
        "The supplemental rational certificate submitted with the SQUISH packings.",
    ),
    (
        "https://github.com/jlevy/squares/issues/401#issuecomment-6043191866",
        "SQUISH dated source follow-up",
        "Nate Chaoweeraprasit",
        (
            "Dated SQUISH update, including a pinned copy of the original rational "
            "n153 certificate."
        ),
    ),
    (
        "https://github.com/jlevy/squares/issues/686",
        "100 Certified Larger-Count Square Packings",
        "Darius Muglich",
        (
            "Exact rational upper-bound certificates for n = 328 to 998, in an archive"
            " attached to the issue."
        ),
    ),
    (
        "https://sam-burns.com/posts/proposing-better-lower-bound-for-n17-square-packing/",
        "Proposing a Better Lower Bound for n = 17 Square Packing",
        "Sam Burns",
        (
            "A weighted certificate for s(17) \u2265 4.4811, the method Massaccesi\u2019s"
            " bound builds on."
        ),
    ),
    (
        "https://gus-massa.blogspot.com/2026/08/another-better-lower-bound-for-n17.html",
        "Another Better Lower Bound for n = 17 Square Packing",
        "Gustavo Massaccesi",
        "s(17) \u2265 4.5058, by linear programming on Burns\u2019s certificate architecture.",
    ),
    (
        "https://doi.org/10.5281/zenodo.23038546",
        "Zenodo 23038546",
        "Ke Wang and Can Li",
        (
            "An exact lower bound for eleven squares, a reweighting of Overbeck\u2019s"
            " certificate."
        ),
    ),
    (
        "https://doi.org/10.5281/zenodo.23463481",
        "Zenodo 23463481",
        "Kevin Fang",
        (
            "The note, draft v0.9, with the proof of Fang\u2019s Theorems 1 and 2 on n\u00b2"
            " \u2212 n + 1 squares below side n (T-163)."
        ),
    ),
    (
        "https://arxiv.org/abs/2609.37410",
        "arXiv 2609.37410",
        "Hakan Karaku\u015f",
        (
            "A counterexample to Nagamochi\u2019s scoring lemma, and a strip-measure lower"
            " bound for every nonsquare count from eight."
        ),
    ),
    (
        "https://hmbelvedere.com/",
        "UnitSquare",
        "the UnitSquare Project",
        (
            "Results Release 1, reported packings for six counts from n = 68 to 131, each"
            " since superseded."
        ),
    ),
)


@dataclass(frozen=True)
class Resource:
    url: str
    title: str
    description: str
    byline: str
    profile_ids: tuple[str, ...]
    kind: Literal["repository", "catalogue", "website"]
    byline_label: Literal["By", "Contributors"] = "By"


def profile_ids_for_byline(byline: str, index: ProfileIndex) -> tuple[str, ...]:
    """Resolve curated whole labels, otherwise exact unique full names in a byline."""
    key = " ".join(byline.split()).casefold()
    matches = tuple(
        identifier for identifier, labels in index.personal_labels.items() if key in labels
    )
    if matches:
        return matches if len(matches) == 1 else ()
    return named_profile_ids(byline, index)


# Retained 11SquaresFormalized/ACKNOWLEDGEMENTS.md, lines 5-10. These mixed
# proof/support relationships establish resource membership, not primary authorship.
RESOURCE_CONTRIBUTORS = {
    "https://github.com/Queuingtheorydotcom/11SquaresFormalized": (
        "ctjlewis",
        "hiroaki-hosono",
        "benjamin-gurevitch",
        "julian-jj",
        "guzhou0806",
        "manasseh-ahmed",
    ),
}


def resource_records(index: ProfileIndex) -> tuple[Resource, ...]:
    """Project the existing curated source lists without guessing URL ownership."""
    sites: tuple[
        tuple[Literal["catalogue", "website"], tuple[tuple[str, str, str, str], ...]], ...
    ] = (("catalogue", CATALOGUE_SITES), ("website", OTHER_SITES))
    records = [
        Resource(url, title, note, author, profile_ids_for_byline(author, index), kind)
        for kind, sources in sites
        for url, title, author, note in sources
    ]
    records.extend(
        Resource(
            url,
            urlsplit(url).path.rstrip("/").rsplit("/", 1)[-1],
            note,
            author,
            profile_ids_for_byline(author, index),
            "repository",
        )
        for url, author, note in OTHER_PROJECTS
    )
    unique: dict[str, Resource] = {}
    for original in records:
        record = original
        if identifiers := RESOURCE_CONTRIBUTORS.get(record.url):
            if any(identifier not in index.people for identifier in identifiers):
                raise ValueError(f"resource contributor has no profile: {record.url}")
            record = Resource(
                record.url,
                record.title,
                record.description,
                ", ".join(index.people[identifier].full_name for identifier in identifiers),
                identifiers,
                record.kind,
                "Contributors",
            )
        if record.url in unique and unique[record.url] != record:
            raise ValueError(f"conflicting external resource: {record.url}")
        unique[record.url] = record
    return tuple(unique.values())


@cache
def resources() -> tuple[Resource, ...]:
    """The shared resource inventory, requiring only lightweight identity metadata."""
    return resource_records(public_index())


def resources_for_profile(
    identifier: str, records: Sequence[Resource] | None = None
) -> tuple[Resource, ...]:
    """Each exact resource URL once for every explicitly credited person."""
    selected = resources() if records is None else records
    return tuple(
        {record.url: record for record in selected if identifier in record.profile_ids}.values()
    )


@cache
def _resource_metadata() -> dict[str, dict[str, Any]]:
    return record_metadata()


def profile_resources(
    identifier: str,
    records: Sequence[Resource] | None = None,
    *,
    metadata: Mapping[str, Mapping[str, Any]] | None = None,
) -> tuple[Resource, ...]:
    """Curated work and evidenced personal/publication websites, each exact URL once."""
    selected = resources_for_profile(identifier, records)
    person = (_resource_metadata() if metadata is None else metadata).get(identifier, {})
    combined = {record.url: record for record in selected}
    for link in person.get("links", ()):
        if link["kind"] not in {"personal", "publication"}:
            continue
        url = str(link["url"])
        combined.setdefault(
            url,
            Resource(
                url,
                "Personal website" if link["kind"] == "personal" else "Publication website",
                "",
                person["display_name"],
                (identifier,),
                "website",
            ),
        )
    return tuple(combined.values())
