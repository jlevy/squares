"""The exact-side-values paper is complete, generated, and publication-shaped.

The controls here use a small register for renderer behavior and the retained register
for coverage.  They keep the two central boundaries visible: an exact algebraic identity
does not establish geometric feasibility, and a feasible packing does not establish a
global optimum.
"""

from __future__ import annotations

import json
from copy import deepcopy
from html import escape, unescape
from pathlib import Path
from typing import Any

import pytest

from devtools import build_exact_values as exact
from devtools import check_published_site
from devtools import render_exact_side_values as paper

REVISION = "a" * 40


def _checks(*, digits: int = 15) -> dict[str, Any]:
    return {
        "catalogue": "matches",
        "decimal": "1.4142135623730950488",
        "galois": {"group": "S2", "order": 2, "solvable": True},
        "irreducible": {"method": "factorization", "primes": []},
        "kkt_agreement_digits": 39,
        "recorded_agreement_digits": digits,
        "root": {
            "contains_recorded_side": True,
            "interval": ["1414/1000", "1415/1000"],
            "unique": True,
            "window": "record",
        },
    }


def _polynomial(coefficients: list[str]) -> dict[str, Any]:
    return {
        "coefficients": coefficients,
        "height_digits": max(len(value.lstrip("-")) for value in coefficients),
        "latex": "unused",
        "text": "unused = 0",
    }


def _entry(
    n: int,
    *,
    state: str,
    degree: int | None,
    polynomial: dict[str, Any] | None,
    exact: str | None = None,
    exact_latex: str | None = None,
    relation: str = "upper-bound",
    status: str = "open",
    notes: list[dict[str, Any]] | None = None,
    source_occurrences: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "algebraic_source": "catalogue" if polynomial else None,
        "checks": _checks()
        if polynomial
        else {
            "catalogue": None,
            "decimal": None,
            "galois": None,
            "irreducible": None,
            "kkt_agreement_digits": None,
            "recorded_agreement_digits": None,
            "root": None,
        },
        "degree": degree,
        "exact_form": exact,
        "exact_form_latex": exact_latex if exact_latex is not None else exact,
        "kkt": {"status": "KKT local min", "value": f"{n}.125"},
        "lower": {"value": str(n)},
        "n": n,
        "notes": notes or [],
        "polynomial": polynomial,
        "side": {"relation": relation, "value": f"{n}.25"},
        "source_occurrences": source_occurrences or [],
        "state": state,
        "status": status,
    }


def small_document() -> dict[str, Any]:
    superseded = {
        "bead": None,
        "checks": _checks(digits=16),
        "degree": 2,
        "kind": "superseded-catalogue-polynomial",
        "polynomial": _polynomial(["1", "-4", "2"]),
        "side": "6.414213562373095",
        "text": "The catalogue packing was later improved.",
    }
    source = {
        "kind": "comparison-catalogue",
        "locator": {"line": 73, "section": "6"},
        "path": "packing/resources/web/compared.md",
        "source_flags": ["invalid"],
        "url": "https://example.test/compared.html",
    }
    historical = {
        "algebraic_source": "catalogue",
        "attribution": {
            "date_mentions": ["September 2023"],
            "source_text": ["The source labels this row invalid."],
        },
        "bead": "think-history",
        "checks": _checks(digits=16),
        "current_side": "6.25",
        "degree": 2,
        "kind": "source-invalid",
        "n": 6,
        "polynomial": _polynomial(["1", "-4", "2"]),
        "side": "6.414213562373095",
        "source_statuses": ["invalid"],
        "sources": [source],
    }
    return {
        "softschema": {
            "contract": paper.CONTRACT,
            "envelope": "register",
            "schema": "exact-values.schema.yaml",
            "status": "enforced",
        },
        "register": {
            "entries": [
                _entry(
                    1,
                    state="integer",
                    degree=1,
                    polynomial=_polynomial(["1", "-1"]),
                    exact="1",
                    relation="equality",
                    status="proved",
                ),
                _entry(
                    2,
                    state="rational",
                    degree=1,
                    polynomial=_polynomial(["2", "-5"]),
                    exact="5/2",
                    exact_latex=r"\tfrac{5}{2}",
                ),
                _entry(
                    3,
                    state="closed-form",
                    degree=2,
                    polynomial=_polynomial(["1", "0", "-2"]),
                    exact="sqrt(2)",
                    exact_latex=r"\sqrt{2}",
                    source_occurrences=[source],
                ),
                _entry(
                    4,
                    state="minimal-polynomial",
                    degree=3,
                    polynomial=_polynomial(["1", "0", "-2", "-1"]),
                ),
                _entry(
                    5,
                    state="degree-only",
                    degree=672,
                    polynomial=None,
                    notes=[
                        {
                            "bead": "think-nymu",
                            "degree": 672,
                            "kind": "missing-polynomial-text",
                            "text": "The source text still needs retention.",
                        }
                    ],
                ),
                _entry(
                    6,
                    state="numeric-only",
                    degree=None,
                    polynomial=None,
                    notes=[
                        superseded,
                        {
                            "bead": "think-eu89",
                            "degree": None,
                            "kind": "route",
                            "text": "Re-solve the independent KKT point.",
                        },
                    ],
                ),
            ],
            "generated_by": "python -m devtools.build_exact_values",
            "historical_entries": [historical],
            "range": {"first": 1, "last": 6},
            "sources": {"records": "frontier/n-NNN.md"},
            "totals": {
                "closed-form": 1,
                "degree-only": 1,
                "integer": 1,
                "irreducible-certified": 4,
                "minimal-polynomial": 1,
                "numeric-only": 1,
                "proved": 1,
                "rational": 1,
                "root-isolated": 4,
            },
        },
    }


@pytest.fixture(scope="module")
def rendered() -> tuple[str, str]:
    document = small_document()
    return paper.render(
        paper.ARTICLE.read_text(encoding="utf-8"),
        register=document["register"],
        revision=REVISION,
    )


def test_the_paper_separates_identity_geometry_and_global_optimality(
    rendered: tuple[str, str],
) -> None:
    _html, markdown = rendered
    prose = " ".join(markdown.split())
    for statement in (
        "A polynomial can identify the recorded side exactly.",
        "A feasible geometric realization establishes an upper bound",
        "Only an equal lower bound establishes global optimality.",
        (
            "These checks do not establish a feasible packing, local optimality, "
            "or global optimality."
        ),
        "not an exact contact or geometry certificate",
        "a PSLQ relation by itself remains a numerical candidate",
    ):
        assert statement in prose
    assert "global optimum proved" in markdown
    assert "reported packing upper bound; optimum open" in markdown
    assert "{{" not in markdown


def test_every_register_section_is_derived_from_the_small_control(
    rendered: tuple[str, str],
) -> None:
    _, markdown = rendered
    assert markdown.count("### Current polynomial for") == 4
    assert markdown.count("### Historical polynomial for") == 1
    assert "$\\tfrac{5}{2}$" in markdown
    assert "$\\sqrt{2}$" in markdown
    assert r"Quadratic forms in $\mathbb{Q}(\sqrt{2})$ | 1 | 3" in markdown
    assert "| `records` | `frontier/n-NNN.md` |" in markdown
    assert "catalogue; matches; 1.4142135623730950488" in markdown
    assert "think-nymu" in markdown
    assert "think-eu89" in markdown
    assert "6.414213562373095" in markdown
    assert "printed-side agreement 16 digits" in markdown
    assert "H_{6,1}(s)" in markdown
    assert "source-invalid" in markdown
    assert "does not furnish a valid packing upper bound" in markdown
    assert "packing/resources/web/compared.md:73" in markdown
    assert "think-history" in markdown


def test_an_explicit_empty_historical_collection_does_not_restore_legacy_notes() -> None:
    register = small_document()["register"]
    register["historical_entries"] = []
    assert paper.historical_polynomials_markdown(register) == (
        "No historical polynomial-side pairs are recorded.\n"
    )
    assert "**0** historical polynomial-side pairs" in paper.summary_markdown(register)


def test_a_degree_672_polynomial_is_complete_and_paginated_as_coefficients() -> None:
    constant = -(10**96 + 37)
    coefficients = [1, *([0] * 671), constant]
    rendered = paper.polynomial_markdown(
        "P_{83}",
        _polynomial([str(value) for value in coefficients]),
        degree=672,
        context="degree-672 control",
    )
    assert r"P_{83}(s)=\sum_{k=0}^{672} a_k s^k=0" in rendered
    assert "| 672 | <code>1</code> |" in rendered
    assert f"| 0 | <code>{constant}</code> |" in rendered
    assert rendered.count("<code>") == 673
    assert "…" not in rendered


def test_the_retained_degree_672_polynomial_and_source_identity_are_complete() -> None:
    register = paper.load_register()
    entry = next(row for row in paper.entries(register) if row["n"] == 83)
    coefficients = entry["polynomial"]["coefficients"]
    rendered = paper.polynomial_markdown(
        "P_{83}", entry["polynomial"], degree=entry["degree"], context="n=83"
    )
    assert entry["degree"] == 672
    assert len(coefficients) == 673
    assert rendered.count("<code>") == 673
    assert f"| 672 | <code>{coefficients[0]}</code> |" in rendered
    assert f"| 0 | <code>{coefficients[-1]}</code> |" in rendered
    assert "…" not in rendered
    checks = paper.checks_markdown(register)
    assert "matches-svg" in checks
    assert "source Root index 27, not independently counted" in checks
    sources = paper.sources_markdown(register)
    assert "`svg_facts`" in sources
    assert "kingbird-exact-side-facts-2026-10-07/facts" in sources


def test_a_polynomial_with_a_missing_coefficient_is_refused() -> None:
    with pytest.raises(paper.ExactSideValuesPaperError, match="requires 4 coefficients"):
        paper.polynomial_markdown(
            "P_{4}", _polynomial(["1", "2", "3"]), degree=3, context="bad control"
        )


def test_the_retained_register_renders_every_current_and_historical_polynomial() -> None:
    register = paper.load_register()
    rows = paper.entries(register)
    current = [row for row in rows if row.get("polynomial") is not None]
    historical = paper.historical_entries(register)
    current_markdown = paper.current_polynomials_markdown(register)
    historical_markdown = paper.historical_polynomials_markdown(register)
    assert len(rows) == 324
    assert len(current) == register["totals"]["irreducible-certified"]
    assert current_markdown.count("### Current polynomial for") == len(current)
    assert historical
    assert historical_markdown.count("### Historical polynomial for") == len(historical)
    assert "does not retain its coefficients" not in historical_markdown
    seen: dict[int, int] = {}
    for entry in historical:
        polynomial = entry.get("polynomial")
        assert polynomial is not None, entry["n"]
        coefficients = polynomial["coefficients"]
        assert len(coefficients) == entry["degree"] + 1
        n = int(entry["n"])
        seen[n] = seen.get(n, 0) + 1
        assert (
            f"### Historical polynomial for $n={entry['n']}$ at side `{entry['side']}`"
            in historical_markdown
        )
        assert (
            paper.polynomial_markdown(
                f"H_{{{n},{seen[n]}}}",
                polynomial,
                degree=entry["degree"],
                context=f"historical n={n} control",
            )
            in historical_markdown
        )


def test_historical_source_statuses_attribution_and_invalid_geometry_are_visible() -> None:
    register = paper.load_register()
    historical = paper.historical_entries(register)
    summary = paper.historical_summary_markdown(register)
    catalogue = paper.historical_polynomials_markdown(register)
    assert "KKT" not in summary
    assert "KKT" not in catalogue
    invalid_259 = [
        entry for entry in historical if entry["n"] == 259 and entry["kind"] == "source-invalid"
    ]
    assert len(invalid_259) == 1
    assert invalid_259[0]["degree"] == 12
    assert any(
        entry["n"] == 259 and entry["degree"] == 8 and entry["kind"] != "source-invalid"
        for entry in historical
    )
    assert "does not furnish a valid packing upper bound" in catalogue
    for entry in historical:
        assert entry["kind"] in summary
        if entry.get("bead") is not None:
            assert entry["bead"] in catalogue
        for status in entry["source_statuses"]:
            assert escape(str(status), quote=False) in catalogue
        for source in entry["sources"]:
            locator = source["locator"]
            assert f"{source['path']}:{locator['line']}" in catalogue
            for flag in source.get("source_flags", []):
                assert escape(str(flag), quote=False) in catalogue
        attribution = entry["attribution"]
        for date in attribution["date_mentions"]:
            assert escape(str(date), quote=False) in catalogue
        for text in attribution["source_text"]:
            assert escape(str(text), quote=False).replace("\n", " ") in catalogue


def test_retained_attribution_is_literal_source_text_not_paper_markdown() -> None:
    from kpress.format.markdown import parse_markdown  # noqa: PLC0415

    register = paper.load_register()
    entry = next(
        row
        for row in paper.historical_entries(register)
        if row["n"] == 71
        and row["degree"] == 4
        and any("[Explore group]" in text for text in row["attribution"]["source_text"])
    )
    fragment = paper.historical_attribution_markdown(entry, n=71)
    rendered = parse_markdown(
        fragment, title="literal attribution control", trust_mode="trusted", math="auto"
    ).html
    assert "[Explore group](squares_in_squares__n^2-n-1.html)" in rendered
    assert 'href="squares_in_squares__n^2-n-1.html"' not in rendered
    assert "kpress-math" not in rendered
    assert r"\Nn{8.96028765944389}" in rendered


def test_the_complete_archive_preserves_n258_source_expression_and_derived_origin() -> None:
    source = exact.catalogue_entries()[258]
    current = exact.build_entry(258, exact.load_packing(258), source, exact.kkt_rows().get(258))
    historical = exact.source_closed_form_history(current, source)
    assert historical is not None
    register = small_document()["register"]
    register["historical_entries"] = [historical]
    html, markdown = paper.render(
        paper.ARTICLE.read_text(encoding="utf-8"), register=register, revision=REVISION
    )
    for output in (html, markdown):
        assert "Retained source expression: <code>(19/2) + 5 sqrt(2)</code>." in output
        assert "Polynomial origin: <code>derived-from-source-closed-form</code>." in output
        assert "4s^{2}" in output
        assert "https://kingbird.myphotos.cc/packing/squares_in_squares.html" in output
    historical["exact_form"] = '<span id="source-expression-control">sqrt(2)</span>'
    html, markdown = paper.render(
        paper.ARTICLE.read_text(encoding="utf-8"), register=register, revision=REVISION
    )
    for output in (html, markdown):
        assert '<span id="source-expression-control">' not in output
        assert historical["exact_form"] in unescape(output)
        assert "&lt;span" in output


def test_browser_help_describes_the_certified_upward_display_check() -> None:
    page = paper.render_browser(revision=REVISION)
    assert "rounding or truncation agreement" in page
    assert "For a replay-backed SQUISH rational upper bound" in page
    assert "at least the exact side and less than one final printed unit above it" in page


def test_current_source_occurrences_are_rendered_without_duplicate_polynomials() -> None:
    register = paper.load_register()
    rows = paper.entries(register)
    occurrences = [
        (entry, source) for entry in rows for source in entry.get("source_occurrences", [])
    ]
    assert occurrences
    checks = paper.checks_markdown(register)
    catalogue = paper.current_polynomials_markdown(register)
    for _entry, source in occurrences:
        label = f"{source['path']}:{source['locator']['line']}"
        assert label in checks
        assert label in catalogue


def test_the_retained_register_renders_every_expression_check_and_missing_route() -> None:
    register = paper.load_register()
    rows = paper.entries(register)
    exact = [entry for entry in rows if entry.get("exact_form_latex") is not None]
    current = [entry for entry in rows if entry.get("polynomial") is not None]
    missing = [entry for entry in rows if entry.get("state") in {"degree-only", "numeric-only"}]
    exact_markdown = paper.exact_forms_markdown(register)
    checks_markdown = paper.checks_markdown(register)
    missing_markdown = paper.missing_values_markdown(register)
    assert len(exact_markdown.splitlines()[2:]) == len(exact)
    assert len(checks_markdown.splitlines()[2:]) == len(current)
    for entries, markdown in (
        (exact, exact_markdown),
        (current, checks_markdown),
        (missing, missing_markdown),
    ):
        for entry in entries:
            assert f"| {entry['n']} |" in markdown
    for entry in missing:
        for note in entry["notes"]:
            if note["kind"] not in {
                "route",
                "missing-polynomial-text",
                "relation-search-negative",
            }:
                continue
            expected = escape(str(note["text"]), quote=False).replace("|", "\\|")
            assert expected in missing_markdown
            if note.get("bead") is not None:
                assert note["bead"] in missing_markdown


def test_output_names_follow_the_paper_slug(tmp_path: Path, rendered: tuple[str, str]) -> None:
    html, markdown = rendered
    outputs = paper.output_files(
        tmp_path, html, markdown, register=small_document()["register"]
    )
    assert {
        tmp_path / "papers/exact-side-values.html",
        tmp_path / "papers/exact-side-values-complete.html",
        tmp_path / "papers/exact-side-values.md",
        tmp_path / "papers/exact-side-values-browser.js",
        tmp_path / "papers/exact-side-values-data/index.json",
    }.issubset(outputs)
    assert outputs[tmp_path / "papers/exact-side-values-complete.html"] == html
    assert outputs[tmp_path / "papers/exact-side-values.md"] == markdown
    assert 'src="http' not in html
    assert 'href="http' in html


def test_check_rebuilds_from_the_register_and_catches_drift(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "exact-values.json"
    document = small_document()
    source.write_text(json.dumps(document), encoding="utf-8")
    monkeypatch.setattr(paper, "REGISTER", source)
    site = tmp_path / "site"
    arguments = ["--site", str(site), "--revision", REVISION]
    assert paper.main(arguments) == 0
    assert paper.main([*arguments, "--check"]) == 0
    changed = deepcopy(document)
    changed["register"]["entries"][0]["side"]["value"] = "1.0001"
    source.write_text(json.dumps(changed), encoding="utf-8")
    with pytest.raises(SystemExit, match="stale exact-side-values output"):
        paper.main([*arguments, "--check"])


def test_the_lazy_export_checks_every_payload_and_removes_stale_extras(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "exact-values.json"
    source.write_text(json.dumps(small_document()), encoding="utf-8")
    monkeypatch.setattr(paper, "REGISTER", source)
    site = tmp_path / "site"
    arguments = ["--site", str(site), "--revision", REVISION]
    assert paper.main(arguments) == 0
    browser = site / "papers/exact-side-values.html"
    archive = site / "papers/exact-side-values-complete.html"
    assert "exact-browser" in browser.read_text(encoding="utf-8")
    assert "kpress-math" not in browser.read_text(encoding="utf-8")
    assert "kpress-math" in archive.read_text(encoding="utf-8")
    data = site / "papers/exact-side-values-data"
    index = json.loads((data / "index.json").read_text(encoding="utf-8"))
    coefficient = site / "papers" / index["entries"][0]["coefficients_url"]
    original = coefficient.read_text(encoding="utf-8")
    coefficient.write_text("", encoding="utf-8")
    with pytest.raises(SystemExit, match="stale exact-side-values output"):
        paper.main([*arguments, "--check"])
    coefficient.write_text(original, encoding="utf-8")
    coefficient.unlink()
    with pytest.raises(SystemExit, match="stale exact-side-values output"):
        paper.main([*arguments, "--check"])
    assert paper.main(arguments) == 0
    extra = data / "metadata/old.json"
    extra.write_text("{}", encoding="utf-8")
    with pytest.raises(SystemExit, match="stale exact-side-values output"):
        paper.main([*arguments, "--check"])
    assert paper.main(arguments) == 0
    assert not extra.exists()
    assert paper.main([*arguments, "--check"]) == 0


def test_pdf_uses_the_complete_archive(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "exact-values.json"
    source.write_text(json.dumps(small_document()), encoding="utf-8")
    monkeypatch.setattr(paper, "REGISTER", source)
    site = tmp_path / "site"
    calls: list[tuple[Path, Path]] = []
    monkeypatch.setattr(paper, "_print_pdf", lambda html, pdf: calls.append((html, pdf)))
    assert paper.main(["--site", str(site), "--revision", REVISION, "--pdf"]) == 0
    assert calls == [
        (site / "papers/exact-side-values-complete.html", site / "papers/exact-side-values.pdf")
    ]


def test_failed_publication_preserves_the_previous_complete_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from contextlib import contextmanager  # noqa: PLC0415

    source = tmp_path / "exact-values.json"
    source.write_text(json.dumps(small_document()), encoding="utf-8")
    monkeypatch.setattr(paper, "REGISTER", source)
    site = tmp_path / "site"
    archive = site / "papers/exact-side-values-complete.html"
    archive.parent.mkdir(parents=True)
    archive.write_text("previous complete file", encoding="utf-8")
    atomic = paper.atomic_output_file

    @contextmanager
    def interrupted(path: Path):
        with atomic(path) as temporary:
            yield temporary
            raise OSError("injected publication failure")

    monkeypatch.setattr(paper, "atomic_output_file", interrupted)
    with pytest.raises(OSError, match="injected publication failure"):
        paper.main(["--site", str(site), "--revision", REVISION])
    assert archive.read_text(encoding="utf-8") == "previous complete file"
    assert set(archive.parent.iterdir()) == {archive}


def test_generated_payload_traversal_refuses_symlinks(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "exact-values.json"
    source.write_text(json.dumps(small_document()), encoding="utf-8")
    monkeypatch.setattr(paper, "REGISTER", source)
    site = tmp_path / "site"
    data = site / "papers/exact-side-values-data"
    data.mkdir(parents=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    retained = outside / "retained.json"
    retained.write_text("source evidence", encoding="utf-8")
    (data / "linked").symlink_to(outside, target_is_directory=True)
    with pytest.raises(paper.ExactSideValuesPaperError, match="symlink"):
        paper.main(["--site", str(site), "--revision", REVISION])
    assert retained.read_text(encoding="utf-8") == "source evidence"


def test_browser_keeps_publication_version_and_pinned_source() -> None:
    page = paper.render_browser(revision=REVISION)
    assert paper.FRONT.version in page
    assert (
        f"https://github.com/jlevy/squares/blob/{REVISION}/packing/frontier/exact-values.json"
        in page
    )
    assert "exact-side-values-complete.html" in page


def test_browser_and_complete_archive_have_distinct_publication_identity(
    rendered: tuple[str, str],
) -> None:
    archive, _ = rendered
    pages = {
        paper.SITE_PATH: paper.render_browser(revision=REVISION),
        paper.COMPLETE_PATH: archive,
    }
    for path, page in pages.items():
        assert check_published_site.head_problems(page, paper.SITE_URL + path) == []
    assert check_published_site.shared_descriptions(pages) == []
