"""Each date a generated artifact carries has one rule, and the rule is held.

The owner saw "September 29" on a PDF in pull requests made on 1 October 2026 and asked
whether the generated files carry the right dates. That one did. The date beside it,
"This review revised September 30, 2026", had stood still through three changes to the
article on 1 October, the explainer's "Last revised" was the day its edition was first
published, the posters were dated by a release while they showed later results, and
every PDF's properties gave the second a machine drew it. `devtools.artifact_dates`
states the rule for each; these tests hold the rules and rehearse each refusal.
"""

from __future__ import annotations

import importlib
from datetime import date
from pathlib import Path

import pytest

from devtools import (
    artifact_dates,
    render_n11_lower_bounds_explainer,
    render_n11_optimality_review,
)
from devtools.render_composite_pdf import pdf_dates
from devtools.render_n11_lower_bounds_explainer_pdf import (
    date_problem,
    dated,
    publication_date_text,
)
from sqpack import release

#: A PDF's information dictionary as Chromium writes it, between two markers whose
#: offsets must not move.
CHROMIUM = (
    b"%PDF-1.4\n1 0 obj\n<</Title (A paper)\n/Creator (Chromium)\n"
    b"/CreationDate (D:20261001195544+00'00')\n/ModDate (D:20261001195544+00'00')>>\n"
    b"endobj\nMARKER\n"
)


def test_no_derived_date_in_the_tree_is_other_than_its_rule_gives() -> None:
    """The table `python -m devtools.artifact_dates` prints, with nothing wrong in it.

    A row is compared where its date is derived and git can answer. A typed date -- an
    edition's first publication, the register's review -- is listed with what holds it.
    """
    found = artifact_dates.rows()
    assert [row.artifact for row in found if row.wrong] == []
    derived = {row.artifact for row in found if row.expected is not None}
    assert {
        "known-best-1-100.pdf CreationDate, ModDate",
        "known-best-1-324.pdf CreationDate, ModDate",
        "optimality paper, Original proof",
        "threshold-bound review, Original proof",
    } <= derived
    assert artifact_dates.main(["--check"]) == 0


def test_a_papers_revised_date_is_the_day_its_article_last_changed() -> None:
    """Every paper, by one rule: the last commit that changed the article, merges aside.

    This is the check that fails when an article changes and its date does not: the
    explainer's is `release.EXPLAINER_REVISED`, the optimality paper's is
    `release.OPTIMALITY_REVIEW_REVISED`, the threshold-bound review's is
    `release.THRESHOLD_REVIEW_REVISED`, and each is changed in the commit that changes
    the article. The articles are `n11-lower-bounds-explainer-article.md`,
    `n11-optimality-review-article.md` and `n11-threshold-bound-review-article.md`,
    named here so that the pre-push tier selects this file when any changes.
    """
    assert artifact_dates.optimality_dates() == (
        release.OPTIMALITY_PROOF_PUBLISHED,
        release.OPTIMALITY_REVIEW_REVISED,
    )
    for article, stated, constant in (
        (artifact_dates.EXPLAINER_ARTICLE, release.EXPLAINER_REVISED, "EXPLAINER_REVISED"),
        (
            artifact_dates.OPTIMALITY_ARTICLE,
            release.OPTIMALITY_REVIEW_REVISED,
            "OPTIMALITY_REVIEW_REVISED",
        ),
        (
            artifact_dates.THRESHOLD_ARTICLE,
            release.THRESHOLD_REVIEW_REVISED,
            "THRESHOLD_REVIEW_REVISED",
        ),
    ):
        changed = artifact_dates.last_change(article)
        if changed is None:
            pytest.skip("git cannot date the articles here")
        assert stated == artifact_dates.long_date(changed), (
            f"{article.name} last changed on {changed}, and its paper says it was last "
            f"revised {stated}: state {artifact_dates.long_date(changed)!r} in "
            f"release.{constant}"
        )


def test_the_optimality_papers_original_proof_is_the_day_the_register_gives() -> None:
    """The date the owner saw, and it is right: the source published on 29 September.

    Typed in the article, since it is a fact about someone else's work, and held to the
    one place this project records that fact.
    """
    proof, _review = artifact_dates.optimality_dates()
    assert proof == artifact_dates.long_date(artifact_dates.published("T-060"))
    assert proof == "September 29, 2026"


def test_the_threshold_reviews_original_proof_is_the_day_the_register_gives() -> None:
    """Kleddamag published the proof Part II reviews on 22 September, as the register
    records T-037."""
    proof, review = artifact_dates.threshold_dates()
    assert proof == artifact_dates.long_date(artifact_dates.published("T-037"))
    assert proof == release.THRESHOLD_PROOF_PUBLISHED == "September 22, 2026"
    assert artifact_dates.threshold_revised() == artifact_dates.written_date(review)


def test_the_articles_named_here_are_the_ones_the_renderers_read() -> None:
    assert artifact_dates.EXPLAINER_ARTICLE == render_n11_lower_bounds_explainer.MARKDOWN
    assert artifact_dates.OPTIMALITY_ARTICLE == render_n11_optimality_review.ARTICLE
    threshold = importlib.import_module("devtools.render_n11_threshold_bound_review")
    assert artifact_dates.THRESHOLD_ARTICLE == threshold.ARTICLE


def test_a_stale_revised_date_is_reported_and_fails_the_check(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The defect itself, rehearsed: the explainer said September 28 through two changes."""
    if artifact_dates.last_change(artifact_dates.EXPLAINER_ARTICLE) is None:
        pytest.skip("git cannot date the article here")
    monkeypatch.setattr(release, "EXPLAINER_REVISED", "September 5, 2026")
    wrong = [row for row in artifact_dates.rows() if row.wrong]
    assert [row.artifact for row in wrong] == ["explainer, Last revised"]
    assert wrong[0].verdict.startswith("WRONG: the rule gives ")
    assert artifact_dates.main(["--check"]) == 1
    assert "explainer, Last revised" in capsys.readouterr().err
    # Without --check the table is still printed and the command still succeeds.
    assert artifact_dates.main([]) == 0


def test_the_optimality_papers_front_prints_publication_proof_and_revision_dates() -> None:
    """The review's first publication leads its front's dates line, followed by the
    source proof's day and the review's last revision. Each reads from its release
    record, preserving the distinction between the review and the proof it explains."""
    front = render_n11_optimality_review.FRONT
    published = release.OPTIMALITY_REVIEW_HISTORY[-1].first_published
    assert published == "September 30, 2026"
    proof, review = artifact_dates.optimality_dates()
    assert [(dated.label, dated.day) for dated in front.dates] == [
        ("First published", published),
        ("Original proof", proof),
        ("Last revised", review),
    ]
    assert artifact_dates.optimality_revised() == artifact_dates.written_date(review)
    assert "This review revised" not in render_n11_optimality_review.ARTICLE.read_text(
        encoding="utf-8"
    )


def test_dates_are_written_and_read_the_way_the_papers_write_them() -> None:
    assert artifact_dates.long_date("2026-10-01") == "October 1, 2026"
    assert artifact_dates.long_date(date(2026, 9, 5)) == "September 5, 2026"
    assert artifact_dates.written_date("October 1, 2026") == date(2026, 10, 1)
    assert artifact_dates.written_date(release.EXPLAINER_REVISED) <= date.today()  # noqa: DTZ011
    assert artifact_dates.written_date(release.FIRST_PUBLISHED) == date(2026, 9, 5)
    # The explainer's first day is its own history's oldest, and the site began as the
    # explainer, so the two are one day.
    assert artifact_dates.written_date(release.EXPLAINER_FIRST_PUBLISHED) == date(2026, 9, 5)


def test_a_printed_pdf_is_dated_in_place_by_its_revision() -> None:
    """Both of Chromium's clock fields become the revised day, and no byte moves.

    The offsets after the dates are what a PDF's cross-reference table records, so the
    replacement is the length of what it replaces; and it is noon UTC, so the day reads
    the same in every timezone a reader's PDF viewer converts it to.
    """
    day = date(2026, 9, 30)
    result = dated(CHROMIUM, day)
    assert len(result) == len(CHROMIUM)
    assert result.index(b"MARKER") == CHROMIUM.index(b"MARKER")
    assert pdf_dates(result) == {
        "CreationDate": "20260930120000+00'00'",
        "ModDate": "20260930120000+00'00'",
    }
    assert publication_date_text(day) == "20260930120000+00'00'"
    assert result.replace(b"20260930120000", b"20261001195544") == CHROMIUM
    assert dated(result, day) == result
    assert date_problem(result, day) is None
    assert date_problem(CHROMIUM, day) is not None
    assert "not by the clock" in (date_problem(CHROMIUM, date(2026, 10, 1)) or "")


@pytest.mark.parametrize(
    ("pdf", "refusal"),
    [
        (
            CHROMIUM.replace(b"/ModDate (D:20261001195544+00'00')", b""),
            "states one CreationDate",
        ),
        (b"%PDF-1.4\n", "states one CreationDate"),
        (CHROMIUM.replace(b"195544+00'00'", b"195544Z"), "cannot be dated in place"),
        (CHROMIUM + b"/ModDate (D:20261001195544+00'00')", "states one CreationDate"),
    ],
)
def test_a_pdf_of_another_shape_is_refused_rather_than_half_dated(
    pdf: bytes, refusal: str
) -> None:
    with pytest.raises(ValueError, match=refusal):
        dated(pdf, date(2026, 9, 30))


def test_a_built_pdf_is_held_to_its_papers_revised_date(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """`--pdf` is for the papers' PDFs, which are built at deploy and never committed."""
    built = tmp_path / "t-060-explainer.pdf"
    built.write_bytes(CHROMIUM)
    assert artifact_dates.main(["--pdf", str(built), "--revised", "optimality"]) == 1
    assert "not by the clock that drew it" in capsys.readouterr().err

    built.write_bytes(dated(CHROMIUM, artifact_dates.optimality_revised()))
    assert artifact_dates.main(["--pdf", str(built), "--revised", "optimality"]) == 0
    assert artifact_dates.main(["--pdf", str(built), "--revised", "explainer"]) == (
        0 if artifact_dates.optimality_revised().isoformat() == _explainer_revised() else 1
    )
    built.write_bytes(dated(CHROMIUM, artifact_dates.threshold_revised()))
    assert artifact_dates.main(["--pdf", str(built), "--revised", "threshold"]) == 0
    with pytest.raises(SystemExit):
        artifact_dates.main(["--pdf", str(built)])


def _explainer_revised() -> str:
    return artifact_dates.written_date(release.EXPLAINER_REVISED).isoformat()
