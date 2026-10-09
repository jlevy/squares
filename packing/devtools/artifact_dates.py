#!/usr/bin/env python3
"""Every date a generated artifact prints or embeds: what it says, why, and its rule.

The owner asked on 2026-10-01 whether the PDFs and generated files carry the right date,
having seen "September 29" on a PDF in pull requests made on 1 October. That one was
right -- it is the day the proof the paper reviews was published -- and four others were
not: two "revised" lines that stood still while their articles changed, a poster dated
by a release while it showed later results, and three PDFs whose properties gave the
second a machine drew them. Each date now has one rule, and this is where the rules are
written down, read from the tree and checked.

The rules:

- **A date derived from a commit is that commit's author date, on the author's own
  calendar** (`sqpack.release.commit_date`), the day a reader would say the change was
  made. The commit records its offset, so every machine reads the same day.
- **A paper's "revised" date is the date of the last commit that changed its article**,
  merges excluded (`sqpack.release.last_change_date`). It is stated in `sqpack.release`,
  where the paper's front reads it (`EXPLAINER_REVISED`, `THRESHOLD_REVIEW_REVISED`,
  `OPTIMALITY_REVIEW_REVISED`),
  and held to git here, so it is changed in the commit that changes the article and
  cannot stand still under one.
- **A composite's visible date is the date of the data commit it was drawn from**,
  which it records (`build_known_best_atlas.CompositeIdentity`). The grid figure
  prints a dateline; the triangle poster puts the date beside its closing edition.
- **A PDF's `CreationDate` and `ModDate` are the date its face gives, at noon UTC**, and
  never the build clock: the poster's data date, the paper's revised date.
- **A date a person asserts stays typed**, and is listed here with what holds it: an
  edition's first publication, the day a source published its proof, the day the
  register was reviewed.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.artifact_dates
    uv run --frozen --all-extras --group dev python -m devtools.artifact_dates --check
    uv run --frozen --all-extras --group dev python -m devtools.artifact_dates \
        --pdf site/papers/n11-optimality-review.pdf --revised optimality
    uv run --frozen --all-extras --group dev python -m devtools.artifact_dates \
        --pdf site/papers/n11-threshold-bound-review.pdf --revised threshold

With no option it prints the table. `--check` exits 1 when a derived date is not what
its rule gives; where git cannot answer, a row says so and fails nothing. `--pdf` holds
one built PDF's two dates to a paper's revised date, for the PDFs that are built at
deploy and never committed.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from sqpack import release
from sqpack.yamlio import safe_load

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
TEMPLATES = PACKING / "devtools/templates"
#: The papers' articles: the text whose last change is a paper's "revised" date.
EXPLAINER_ARTICLE = TEMPLATES / "n11-lower-bounds-explainer-article.md"
THRESHOLD_ARTICLE = TEMPLATES / "n11-threshold-bound-review-article.md"
OPTIMALITY_ARTICLE = TEMPLATES / "n11-optimality-review-article.md"
PACKING_METHODS_ARTICLE = TEMPLATES / "packing-methods-article.md"
RESULTS = PACKING / "frontier/results.yaml"
SYNOPSIS = REPO / "SYNOPSIS.md"
#: The result each review reviews, whose publication is its "Original proof".
THRESHOLD_RESULT = "T-037"
OPTIMALITY_RESULT = "T-060"
SYNOPSIS_DATE = re.compile(r"^\*\*Date:\*\* (\d{4}-\d{2}-\d{2})$", re.MULTILINE)


def long_date(day: date | str) -> str:
    """A day as the papers write it: October 1, 2026."""
    day = date.fromisoformat(day) if isinstance(day, str) else day
    return f"{day:%B} {day.day}, {day.year}"


def written_date(text: str) -> date:
    """The day a paper's `October 1, 2026` names."""
    return datetime.strptime(text, "%B %d, %Y").date()  # noqa: DTZ007


def optimality_dates() -> tuple[str, str]:
    """The optimality paper's two dates as its front states them: the day the proof it
    reviews was published, then the day the review itself was last revised, both from
    `sqpack.release`, where the paper's renderer reads them."""
    return release.OPTIMALITY_PROOF_PUBLISHED, release.OPTIMALITY_REVIEW_REVISED


def optimality_revised() -> date:
    """The day the optimality paper says it was last revised."""
    return written_date(optimality_dates()[1])


def threshold_dates() -> tuple[str, str]:
    """The threshold-bound review's two dates as its front states them, as the
    optimality paper's are: the day Kleddamag published the proof it reviews, then the
    day the review was last revised, both from `sqpack.release`."""
    return release.THRESHOLD_PROOF_PUBLISHED, release.THRESHOLD_REVIEW_REVISED


def threshold_revised() -> date:
    """The day the threshold-bound review says it was last revised."""
    return written_date(threshold_dates()[1])


def published(result: str) -> str:
    """The day the register says `result` was published by its source, as ISO."""
    register = safe_load(RESULTS.read_text(encoding="utf-8"))
    record = next(entry for entry in register["results"] if entry["id"] == result)
    return str(record["attribution"]["published"])


def last_change(path: Path) -> str | None:
    """The ISO date of the last change to `path`, or `None` where git cannot say."""
    try:
        return release.last_change_date(REPO, path.relative_to(REPO).as_posix())
    except RuntimeError:
        return None


@dataclass(frozen=True)
class Row:
    """One date: where it is, what it says, where that comes from, and the rule."""

    artifact: str
    shows: str
    source: str
    rule: str
    #: What the rule gives, or `None` when the date is a person's assertion or git
    #: cannot answer; then nothing is compared.
    expected: str | None = None
    #: Why nothing is compared, where nothing is.
    held_by: str = ""

    @property
    def verdict(self) -> str:
        if self.expected is None:
            return self.held_by or "not compared"
        return (
            "right" if self.shows == self.expected else f"WRONG: the rule gives {self.expected}"
        )

    @property
    def wrong(self) -> bool:
        return self.expected is not None and self.shows != self.expected


def _poster_rows() -> list[Row]:
    from devtools import build_known_best_atlas as atlas  # noqa: PLC0415
    from devtools import render_composite_pdf  # noqa: PLC0415

    rows = []
    for canvas in atlas.COMPOSITES:
        stem = canvas.spec.stem
        identity = atlas.retained_identity(canvas.svg_path.read_text(encoding="utf-8"))
        try:
            day: str | None = release.commit_date(REPO, identity.data_revision)
        except RuntimeError:
            day = None
        expected_identity = (
            None if day is None else atlas.CompositeIdentity(identity.data_revision, day)
        )
        date_label = "edition date" if canvas.information_in_corner else "dateline"
        shown_date = (
            identity.formatted_date if canvas.information_in_corner else identity.dateline
        )
        expected_date = (
            None
            if expected_identity is None
            else (
                expected_identity.formatted_date
                if canvas.information_in_corner
                else expected_identity.dateline
            )
        )
        rows.append(
            Row(
                f"{stem} {date_label} (SVG, PNG, PDF)",
                shown_date,
                f"its record: data of {identity.data_revision[:12]}",
                "the date of the data commit it was drawn from",
                expected_date,
                "git cannot date the commit here",
            )
        )
        stated = render_composite_pdf.pdf_dates(
            render_composite_pdf.composite_pdf(stem).read_bytes()
        )
        expected = render_composite_pdf.pdf_date_text(date.fromisoformat(identity.data_date))
        rows.append(
            Row(
                f"{render_composite_pdf.composite_pdf(stem).name} CreationDate, ModDate",
                ", ".join(sorted(set(stated.values()))) or "none",
                "set by render_composite_pdf from the SVG's record",
                "the poster's data date, at noon UTC",
                expected if set(stated) == {"CreationDate", "ModDate"} else f"{expected} twice",
            )
        )
    return rows


def _paper_rows() -> list[Row]:
    from devtools.render_n11_lower_bounds_explainer_pdf import (  # noqa: PLC0415
        publication_date_text,
    )

    explainer_changed = last_change(EXPLAINER_ARTICLE)
    proof, review = optimality_dates()
    optimality_changed = last_change(OPTIMALITY_ARTICLE)
    threshold_proof, threshold_review = threshold_dates()
    threshold_changed = last_change(THRESHOLD_ARTICLE)
    methods_changed = last_change(PACKING_METHODS_ARTICLE)
    unknown = "git cannot date the article here"
    return [
        Row(
            "explainer, First published",
            release.EXPLAINER_FIRST_PUBLISHED,
            "release.EXPLAINER_HISTORY, oldest edition",
            "the first Pages deployment, in UTC; typed, with the deployment beside it",
            held_by="typed; test_release holds the paper's history to the site's",
        ),
        Row(
            "explainer, Last revised",
            release.EXPLAINER_REVISED,
            "release.EXPLAINER_REVISED",
            f"the last commit that changed {EXPLAINER_ARTICLE.name}",
            None if explainer_changed is None else long_date(explainer_changed),
            unknown,
        ),
        Row(
            "explainer PDF CreationDate, ModDate",
            publication_date_text(written_date(release.EXPLAINER_REVISED)),
            "set by render_n11_lower_bounds_explainer_pdf --update",
            "Last revised, at noon UTC",
            held_by=(
                "built at deploy; render_n11_lower_bounds_explainer_pdf --check-artifact "
                "refuses another"
            ),
        ),
        Row(
            "threshold-bound review, Original proof",
            threshold_proof,
            "release.THRESHOLD_PROOF_PUBLISHED",
            f"the day the register says {THRESHOLD_RESULT} was published",
            long_date(published(THRESHOLD_RESULT)),
        ),
        Row(
            "threshold-bound review, Last revised",
            threshold_review,
            "release.THRESHOLD_REVIEW_REVISED",
            f"the last commit that changed {THRESHOLD_ARTICLE.name}",
            None if threshold_changed is None else long_date(threshold_changed),
            unknown,
        ),
        Row(
            "threshold-bound review PDF CreationDate, ModDate",
            publication_date_text(written_date(threshold_review)),
            "set by render_n11_threshold_bound_review --pdf",
            "Last revised, at noon UTC",
            held_by="built at deploy; artifact_dates --pdf holds a built file",
        ),
        Row(
            "optimality paper, Original proof",
            proof,
            "release.OPTIMALITY_PROOF_PUBLISHED",
            f"the day the register says {OPTIMALITY_RESULT} was published",
            long_date(published(OPTIMALITY_RESULT)),
        ),
        Row(
            "optimality paper, Last revised",
            review,
            "release.OPTIMALITY_REVIEW_REVISED",
            f"the last commit that changed {OPTIMALITY_ARTICLE.name}",
            None if optimality_changed is None else long_date(optimality_changed),
            unknown,
        ),
        Row(
            "optimality paper PDF CreationDate, ModDate",
            publication_date_text(written_date(review)),
            "set by render_n11_optimality_review --pdf",
            "Last revised, at noon UTC",
            held_by="built at deploy; artifact_dates --pdf holds a built file",
        ),
        Row(
            "packing methods, First published",
            release.PACKING_METHODS_FIRST_PUBLISHED,
            "release.PACKING_METHODS_HISTORY, oldest edition",
            "the standalone tutorial's first edition",
            held_by="typed in the paper's own publication history",
        ),
        Row(
            "packing methods, Last revised",
            release.PACKING_METHODS_REVISED,
            "release.PACKING_METHODS_REVISED",
            f"the last commit that changed {PACKING_METHODS_ARTICLE.name}",
            None if methods_changed is None else long_date(methods_changed),
            unknown,
        ),
        Row(
            "packing methods PDF CreationDate, ModDate",
            publication_date_text(written_date(release.PACKING_METHODS_REVISED)),
            "set by render_packing_methods --pdf",
            "Last revised, at noon UTC",
            held_by="built at deploy; artifact_dates --pdf holds a built file",
        ),
    ]


def _record_rows() -> list[Row]:
    from devtools import render_overview  # noqa: PLC0415

    register = safe_load(RESULTS.read_text(encoding="utf-8"))
    stated = SYNOPSIS_DATE.search(SYNOPSIS.read_text(encoding="utf-8"))
    film = next(
        entry
        for entry in release.PUBLICATION_HISTORY
        if entry.version == render_overview.FILM_RELEASE
    )
    film_day = written_date(film.first_published)
    return [
        Row(
            f"films, caption date and release {render_overview.FILM_RELEASE}",
            render_overview.film_release_date(),
            "release.PUBLICATION_HISTORY at render_overview.FILM_RELEASE",
            "the day the release the films were cut for was first published",
            f"{film_day.day} {film_day:%B}",
        ),
        Row(
            "RESULTS.md, Register reviewed",
            str(register["last_reviewed"]),
            "results.yaml last_reviewed",
            "the day a reviewer says; no entry may be dated after it",
            held_by="typed; check_results refuses a later entry",
        ),
        Row(
            "SYNOPSIS.md, Date",
            stated.group(1) if stated else "none",
            "typed in SYNOPSIS.md",
            "the day its author says; one ISO date and nothing else",
            held_by=(
                "typed; check_synopsis holds its shape; the file last changed "
                f"{last_change(SYNOPSIS) or 'on a day git cannot give here'}"
            ),
        ),
    ]


def rows() -> list[Row]:
    """Every date this tool knows, in the order a reader meets the artifacts."""
    return [*_poster_rows(), *_paper_rows(), *_record_rows()]


def report(found: Sequence[Row]) -> None:
    for row in found:
        print(row.artifact)
        print(f"  shows   {row.shows}")
        print(f"  source  {row.source}")
        print(f"  rule    {row.rule}")
        print(f"  verdict {row.verdict}")


def check_pdf(pdf: Path, paper: str) -> int:
    """Hold one built PDF's dates to the revised date of the paper it is."""
    from devtools.render_n11_lower_bounds_explainer_pdf import date_problem  # noqa: PLC0415

    day = {
        "explainer": lambda: written_date(release.EXPLAINER_REVISED),
        "threshold": threshold_revised,
        "optimality": optimality_revised,
        "packing-methods": lambda: written_date(release.PACKING_METHODS_REVISED),
    }[paper]()
    problem = date_problem(pdf.read_bytes(), day)
    if problem is not None:
        print(f"FAIL: {pdf}: {problem}", file=sys.stderr)
        return 1
    print(f"{pdf.name} is dated {day.isoformat()} at noon UTC, its paper's revised date")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="exit 1 if a derived date is wrong"
    )
    parser.add_argument("--pdf", type=Path, help="a built PDF whose dates to hold")
    parser.add_argument(
        "--revised",
        choices=("explainer", "threshold", "optimality", "packing-methods"),
        help="with --pdf: the paper whose revised date the PDF's dates must be",
    )
    arguments = parser.parse_args(argv)
    if (arguments.pdf is None) != (arguments.revised is None):
        parser.error("--pdf and --revised go together")
    if arguments.pdf is not None:
        return check_pdf(arguments.pdf, arguments.revised)
    found = rows()
    report(found)
    wrong = [row for row in found if row.wrong]
    if wrong:
        print(
            f"{len(wrong)} date{'s are' if len(wrong) > 1 else ' is'} not what the rule "
            "gives: " + "; ".join(row.artifact for row in wrong),
            file=sys.stderr,
        )
    return 1 if arguments.check and wrong else 0


if __name__ == "__main__":
    raise SystemExit(main())
