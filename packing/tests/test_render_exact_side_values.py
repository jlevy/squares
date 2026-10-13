"""The exact-side-values paper is complete, generated, and publication-shaped.

The controls here use a small register for renderer behavior and the retained register
for coverage.  They keep the two central boundaries visible: an exact algebraic identity
does not establish geometric feasibility, and a feasible packing does not establish a
global optimum.
"""

from __future__ import annotations

import gzip
import json
from copy import deepcopy
from fractions import Fraction
from html import escape, unescape
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

import pytest
from kpress.format.markdown import parse_markdown

from devtools import build_exact_values as exact
from devtools import (
    check_published_site,
    check_site_scripts,
    exact_catalogue,
    exact_house_sources,
    site_assets,
    site_urls,
)
from devtools import render_exact_side_values as paper
from devtools import upper_bound_houses as houses
from devtools.render_exact_side_values import WEB_LAYOUT
from devtools.render_overview import SITE_URL
from tests.exact_side_values_fixture import adopted_current

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


def test_report_omits_superseded_sources_without_changing_the_register() -> None:
    register = small_document()["register"]
    superseded = deepcopy(register["historical_entries"][0])
    superseded["kind"] = "superseded"
    register["historical_entries"].append(superseded)
    original = deepcopy(register)
    _, markdown = paper.render(
        paper.ARTICLE.read_text(encoding="utf-8"), register=register, revision=REVISION
    )
    assert markdown.count("### Current polynomial for") == 4
    assert markdown.count("### Historical polynomial for") == 1
    assert "Kind: `superseded`" not in markdown
    assert "source-invalid" in markdown
    assert register == original

    del register["historical_entries"]
    _, legacy_markdown = paper.render(
        paper.ARTICLE.read_text(encoding="utf-8"), register=register, revision=REVISION
    )
    assert "### Superseded polynomial" not in legacy_markdown
    assert "### Historical polynomial" not in legacy_markdown


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


def test_a_wide_single_term_retains_every_coefficient_in_a_printable_table() -> None:
    coefficient = "9" * 48
    rendered = paper.polynomial_markdown(
        "P_{4}", _polynomial(["1", coefficient, "-2"]), degree=2, context="wide-term control"
    )
    assert "The complete coefficient vector" in rendered
    assert "| 2 | <code>1</code> |" in rendered
    assert f"| 1 | <code>{coefficient}</code> |" in rendered
    assert "| 0 | <code>-2</code> |" in rendered
    assert rendered.count("<code>") == 3


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
    retained = paper.load_register()
    original = deepcopy(retained)
    register = exact_catalogue.publication_register(retained)
    reported = [row for row in retained["historical_entries"] if row.get("reported_source")]
    assert [row["n"] for row in reported] == [102, 106, 152, 177]
    superseded_102 = reported[0]
    assert superseded_102["kind"] == "superseded"
    assert superseded_102["assurance"] == {
        "algebraic_identity": "independently-checked",
        "confirmation": "C0",
        "current_pose_identity": "not-established",
        "geometry_replay": "not-attempted",
        "global_optimality": "not-established",
        "lean_replay": "not-attempted",
        "verification": "V0",
    }
    current_102 = next(row for row in register["entries"] if row["n"] == 102)
    assert current_102["state"] == "rational"
    source_102 = houses.source_for(102)
    native_102 = exact_house_sources.scoped_certificate(source_102, 102)
    assert current_102["source_certificate"] == exact_house_sources.custody_for(
        source_102, 102, "adopted"
    )
    assert source_102.result == "T-146"
    assert current_102["exact_form"] == (
        "10605828696431578360490734944053/1000000000000000000000000000000"
    )
    assert Fraction(current_102["exact_form"]) == native_102.side
    assert current_102["side"]["value"] == superseded_102["current_side"]
    (prior_102,) = [
        row
        for row in retained["historical_entries"]
        if row["n"] == 102 and row.get("source_certificate", {}).get("result") == "T-125"
    ]
    assert prior_102["kind"] == "superseded"
    assert prior_102["source_certificate"]["adoption"] == "not-selected"
    assert prior_102["source_certificate"]["source_key"] == "[ry-xu square packing 2026]"
    assert prior_102["polynomial"]["coefficients"] == [
        "2000000000000000000000",
        "-21211657393021211657393",
    ]
    assert Fraction(prior_102["side"]) == Fraction(
        "21211657393021211657393/2000000000000000000000"
    )
    assert not any(
        row["n"] == 102 and row.get("source_certificate", {}).get("result") == "T-125"
        for row in register["historical_entries"]
    )
    assert [
        row["n"] for row in register["historical_entries"] if row.get("reported_source")
    ] == [106, 152, 177]
    historical = paper.historical_entries(register)
    summary = paper.historical_summary_markdown(register)
    catalogue = paper.historical_polynomials_markdown(register)
    assert "KKT" not in summary
    source_roots = {
        "historical_entries": [row for row in historical if row.get("reported_source")]
    }
    assert "KKT" not in paper.historical_polynomials_markdown(source_roots)
    invalid_259 = [
        entry for entry in historical if entry["n"] == 259 and entry["kind"] == "source-invalid"
    ]
    assert len(invalid_259) == 1
    assert invalid_259[0]["degree"] == 12
    valid_259 = [
        entry
        for entry in retained["historical_entries"]
        if entry["n"] == 259 and entry["degree"] == 8
    ]
    assert valid_259
    assert all(entry["kind"] == "superseded" for entry in valid_259)
    assert not any(entry["n"] == 259 and entry["degree"] == 8 for entry in historical)
    assert "does not furnish a valid packing upper bound" in catalogue
    assert (
        f"### Historical polynomial for $n=102$ at side `{superseded_102['side']}`"
        not in catalogue
    )
    assert retained == original
    retained_summary = paper.historical_summary_markdown(retained)
    retained_catalogue = paper.historical_polynomials_markdown(retained)
    assert "KKT" not in retained_summary
    retained_roots = {"historical_entries": reported}
    assert "KKT" not in paper.historical_polynomials_markdown(retained_roots)
    for entry in paper.historical_entries(retained):
        assert entry["kind"] in retained_summary
        if entry.get("reported_source") and entry["kind"] == "unreconciled-source":
            heading = (
                f"### Historical polynomial for $n={entry['n']}$ at side `{entry['side']}`"
            )
            section = catalogue.split(heading, 1)[1].split("### Historical polynomial", 1)[0]
            assurance = entry["assurance"]
            level = f"{assurance['verification']}/{assurance['confirmation']}"
            assert level in section
        if entry.get("bead") is not None:
            assert entry["bead"] in retained_catalogue
        for status in entry["source_statuses"]:
            assert escape(str(status), quote=False) in retained_catalogue
        for source in entry["sources"]:
            locator = source["locator"]
            assert f"{source['path']}:{locator['line']}" in retained_catalogue
            for flag in source.get("source_flags", []):
                assert escape(str(flag), quote=False) in retained_catalogue
        attribution = entry["attribution"]
        for date in attribution["date_mentions"]:
            assert escape(str(date), quote=False) in retained_catalogue
        for text in attribution["source_text"]:
            assert escape(str(text), quote=False).replace("\n", " ") in retained_catalogue


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


def test_superseded_n258_expression_is_archived_without_returning_to_the_report() -> None:
    source = exact.catalogue_entries()[258]
    current = exact.build_entry(258, exact.load_packing(258), source, exact.kkt_rows().get(258))
    historical = exact.source_closed_form_history(current, source)
    assert historical is not None
    register = small_document()["register"]
    register["historical_entries"] = [historical]
    assert historical["kind"] == "superseded"
    raw_markdown = paper.historical_polynomials_markdown(register)
    assert "Retained source expression: <code>(19/2) + 5 sqrt(2)</code>." in raw_markdown
    assert "Polynomial origin: <code>derived-from-source-closed-form</code>." in raw_markdown
    assert "4s^{2}" in raw_markdown
    assert "https://kingbird.myphotos.cc/packing/squares_in_squares.html" in raw_markdown
    html, markdown = paper.render(
        paper.ARTICLE.read_text(encoding="utf-8"), register=register, revision=REVISION
    )
    for output in (html, markdown):
        assert "(19/2) + 5 sqrt(2)" not in output
        assert "Historical polynomial for" not in output
        assert "Current polynomial for" in output
    assert register["historical_entries"] == [historical]
    historical["exact_form"] = '<span id="source-expression-control">sqrt(2)</span>'
    raw_markdown = paper.historical_polynomials_markdown(register)
    assert '<span id="source-expression-control">' not in raw_markdown
    assert historical["exact_form"] in unescape(raw_markdown)
    assert "&lt;span" in raw_markdown


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
            assert (
                f'id="current-n{entry["n"]}"' in markdown
                if markdown == missing_markdown
                else f"| {entry['n']} |" in markdown
            )
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
    published = outputs[tmp_path / "papers/exact-side-values-complete.html"]
    assert isinstance(published, str)
    assert '<script src="../assets/' in published
    assert '<link rel="stylesheet" href="../assets/' in published
    assert "data:font/woff2" not in published
    assert (
        published.partition("<article")[2].partition("</article>")[0]
        == (html.partition("<article")[2].partition("</article>")[0])
    )
    assert next(iter(outputs)).is_relative_to(tmp_path / "assets")
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
    coefficient = (
        site
        / "papers"
        / exact_catalogue.DATA_DIRECTORY
        / "coefficients"
        / f"{index['entries'][0]['id']}.json"
    )
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


def test_web_only_export_refuses_a_pdf_build() -> None:
    with pytest.raises(SystemExit) as error:
        paper.main(["--pdf"])
    assert error.value.code == 2


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


@pytest.mark.parametrize("storage", ["plain", "gzip", "both", "gzip-path"])
def test_load_register_keeps_every_record_and_coefficient_from_retained_storage(
    storage: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = small_document()
    source = tmp_path / "exact-values.json"
    raw = json.dumps(document, ensure_ascii=False).encode()
    if storage in {"plain", "both"}:
        source.write_bytes(raw)
    packed = source.with_name(source.name + ".gz")
    if storage in {"gzip", "both", "gzip-path"}:
        packed.write_bytes(gzip.compress(raw, mtime=0))
    monkeypatch.setattr(paper, "REGISTER", packed if storage == "gzip-path" else source)
    assert paper.load_register() == document["register"]


def test_load_register_refuses_disagreeing_plain_and_compressed_copies(
    tmp_path: Path,
) -> None:
    source = tmp_path / "exact-values.json"
    source.write_text(json.dumps(small_document()), encoding="utf-8")
    source.with_name(source.name + ".gz").write_bytes(gzip.compress(b"{}", mtime=0))
    with pytest.raises(paper.ExactSideValuesPaperError, match="differs from its compressed"):
        paper.load_register(source)


def test_published_register_source_is_the_declared_compressed_input(
    rendered: tuple[str, str],
) -> None:
    stored = paper.REGISTER.with_name(paper.REGISTER.name + ".gz")
    assert stored in paper.RENDER_INPUTS
    assert Path(site_assets.__file__) in paper.RENDER_INPUTS
    assert site_assets.FONT_PRELOAD_PROGRAM in paper.RENDER_INPUTS
    _html, markdown = rendered
    source = paper.ARTICLE.read_text(encoding="utf-8")
    citations = {
        (paper.ARTICLE.parent / match.group("url").partition("#")[0]).resolve()
        for pattern in (paper.RELATIVE_LINK, paper.RELATIVE_REFERENCE, paper.RELATIVE_ANCHOR)
        for match in pattern.finditer(source)
    }
    assert set(paper.CITATION_SOURCES) == citations
    assert citations <= set(paper.RENDER_INPUTS)
    for target in citations:
        assert target.is_file()
        relative = target.relative_to(paper.REPO).as_posix()
        assert f"https://github.com/jlevy/squares/blob/{REVISION}/{relative}" in markdown
    with pytest.raises(paper.ExactSideValuesPaperError, match="linked source does not exist"):
        paper.expanded_markdown(
            source + "\n[Missing](../../resources/web/missing-exact-report-source.md)\n",
            register=small_document()["register"],
            revision=REVISION,
        )


def test_browser_keeps_publication_version_and_pinned_source() -> None:
    page = paper.render_browser(revision=REVISION)
    assert paper.FRONT.version in page
    assert (
        f"https://github.com/jlevy/squares/blob/{REVISION}/packing/frontier/exact-values.json.gz"
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
        assert check_published_site.head_problems(page, SITE_URL + path) == []
    assert check_published_site.shared_descriptions(pages) == []


@pytest.mark.parametrize("mutation", ["missing", "changed"])
def test_publication_refuses_missing_or_changed_linked_assets(
    mutation: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = tmp_path / "exact-values.json"
    source.write_text(json.dumps(small_document()), encoding="utf-8")
    monkeypatch.setattr(paper, "REGISTER", source)
    site = tmp_path / "site"
    arguments = ["--site", str(site), "--revision", REVISION]
    assert paper.main(arguments) == 0
    asset = next((site / "assets/js").glob("*.js"))
    if mutation == "missing":
        asset.unlink()
    else:
        asset.write_bytes(asset.read_bytes() + b"\n")
    with pytest.raises(SystemExit, match="stale exact-side-values output"):
        paper.main([*arguments, "--check"])
    if mutation == "changed":
        archive = site / paper.COMPLETE_PATH
        original = archive.read_bytes()
        with pytest.raises(ValueError, match="asset collision"):
            paper.main(arguments)
        assert archive.read_bytes() == original
    else:
        assert paper.main(arguments) == 0
        assert paper.main([*arguments, "--check"]) == 0


def test_complete_publication_preserves_the_article_under_the_physical_html_cap(
    tmp_path: Path,
) -> None:
    register = paper.load_register()
    html, markdown = paper.render(
        paper.ARTICLE.read_text(encoding="utf-8"),
        register=register,
        revision=REVISION,
    )
    outputs = paper.output_files(tmp_path, html, markdown, register=register, revision=REVISION)
    for path, content in outputs.items():
        if path.suffix == ".html":
            assert isinstance(content, str)
            assert len(content.encode("utf-8")) <= site_urls.HARD_HTML_LIMIT
    complete = outputs[tmp_path / paper.COMPLETE_PATH]
    assert isinstance(complete, str)
    assert (
        complete.partition("<article")[2].partition("</article>")[0]
        == (html.partition("<article")[2].partition("</article>")[0])
    )
    assert outputs[tmp_path / "papers/exact-side-values.md"] == markdown
    assert not any(path.suffix == ".pdf" for path in outputs)


def test_linked_publication_script_inventory_keeps_unknown_program_refusal(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = tmp_path / "exact-values.json"
    source.write_text(json.dumps(small_document()), encoding="utf-8")
    monkeypatch.setattr(paper, "REGISTER", source)
    site = tmp_path / "site"
    assert paper.main(["--site", str(site), "--revision", REVISION]) == 0
    records, failures = check_site_scripts.inventory(site)
    assert not failures
    assert {"deferred-math", "catalogue-application"} <= {row.category for row in records}
    assert all(row.bytes <= 4096 for row in records if "#script-" in row.source)
    assert all(path.read_bytes() for path in (site / "assets/js").glob("*.js"))
    (site / "assets/js/unknown.js").write_text("/* undeclared program */", encoding="utf-8")
    _, failures = check_site_scripts.inventory(site)
    assert failures == ["unclassified executable script: assets/js/unknown.js"]


@pytest.mark.parametrize("n", [1, 70, 263])
def test_web_linear_mathml_keeps_real_coefficients_names_and_markdown(n):
    retained = paper.load_register()
    register = exact_catalogue.publication_register(retained)
    entry = next(row for row in register["entries"] if row["n"] == n)
    name = f"P_{{{n}}}"
    if entry.get("source_certificate"):
        source = houses.source_for(n)
        native = exact_house_sources.scoped_certificate(source, n)
        assert entry["source_certificate"] == exact_house_sources.custody_for(
            source, n, "adopted"
        )
        assert Fraction(entry["exact_form"]) == native.side
        assert entry["polynomial"]["coefficients"] == [
            str(native.side.denominator),
            str(-native.side.numerator),
        ]
    if n == 263:
        (prior,) = [
            row
            for row in retained["historical_entries"]
            if row["n"] == n and row.get("source_certificate", {}).get("result") == "T-134"
        ]
        assert prior["kind"] == "superseded"
        assert prior["source_certificate"]["adoption"] == "not-selected"
        assert not any(
            row["n"] == n and row.get("source_certificate", {}).get("result") == "T-134"
            for row in register["historical_entries"]
        )
    polynomial = entry["polynomial"]
    markdown = paper.polynomial_markdown(name, polynomial, degree=1, context=name)
    native = paper.polynomial_markdown(name, polynomial, degree=1, context=name, web=True)
    assert name in markdown
    assert "<math " not in markdown
    assert "native-polynomial-math" in native
    assert 'tabindex="0"' in native
    assert 'aria-label="Polynomial equation"' in native
    assert "kpress-math-semantic" in native
    assert "kpress-math-render" not in native
    for coefficient in polynomial["coefficients"]:
        magnitude = abs(int(coefficient))
        if magnitude != 1:
            assert f"<mn>{magnitude}</mn>" in native
        assert str(magnitude) in markdown or magnitude == 1
    assert f"<mn>{n}</mn>" in native
    assert paper.polynomial_markdown(name, polynomial, degree=1, context=name) == markdown


def _web_coefficient_rows(native):
    fragment = native.split('<table class="kpress-table coefficient-table">', 1)[1]
    table = ET.fromstring("<table>" + fragment.split("</table>", 1)[0] + "</table>")
    headers = table.findall("./thead/tr/th")
    assert [header.get("scope") for header in headers] == ["col", "col"]
    assert ["".join(header.itertext()) for header in headers] == ["Power k", "Coefficient ak"]
    values = []
    for row in table.findall("./tbody/tr"):
        cells = row.findall("td")
        assert len(cells) == 2
        code = cells[1].find("code")
        assert code is not None
        values.append((cells[0].text, code.text))
    return values


@pytest.mark.parametrize("n", [5, 83])
def test_web_nonlinear_equations_keep_complete_coefficients_and_markdown(n):
    entry = next(row for row in paper.load_register()["entries"] if row["n"] == n)
    arguments = {"degree": entry["degree"], "context": f"n={n}"}
    markdown = paper.polynomial_markdown(f"P_{{{n}}}", entry["polynomial"], **arguments)
    native = paper.polynomial_markdown(f"P_{{{n}}}", entry["polynomial"], **arguments, web=True)
    assert "native-polynomial-math" in native
    assert "<math " not in markdown
    if n == 83:
        expected = [
            (str(entry["degree"] - index), value)
            for index, value in enumerate(entry["polynomial"]["coefficients"])
        ]
        assert _web_coefficient_rows(native) == expected
        for power, coefficient in expected:
            assert f"| {power} | <code>{coefficient}</code> |" in markdown
        assert "<mn>672</mn></msubsup>" in native
    else:
        assert markdown == "$$\nP_{5}(s) ={} 2s^{2} - 8s + 7 = 0\n$$"
        assert "<msup><mi>s</mi><mn>2</mn></msup>" in native


def test_shared_source_quotes_preserve_every_literal_and_record_association():
    register = exact_catalogue.publication_register(paper.load_register())
    history = register["historical_entries"]
    web = paper.historical_polynomials_markdown(register, web=True)
    markdown = paper.historical_polynomials_markdown(register)
    texts = [str(text) for row in history for text in row["attribution"]["source_text"]]
    unique = list(dict.fromkeys(texts))
    appendix = web.split("## Source Attribution Notes", 1)[1]
    for number, text in enumerate(unique, 1):
        literal = escape(text, quote=False)
        quote = f'<blockquote class="source-quote"><p><code>{literal}</code></p></blockquote>'
        assert appendix.count(quote) == 1
        assert f'id="source-attribution-note-{number}"' in appendix
        assert escape(text, quote=False).replace("\n", " ") in markdown
    seen = {}
    for row in history:
        n = row["n"]
        seen[n] = seen.get(n, 0) + 1
        anchor = f'<span id="historical-n{n}-occurrence{seen[n]}"></span>'
        section = (
            web.split(anchor, 1)[1]
            .split('<span id="historical-', 1)[0]
            .split("## Source Attribution Notes", 1)[0]
        )
        for text in row["attribution"]["source_text"]:
            number = unique.index(str(text)) + 1
            assert f"](#source-attribution-note-{number})" in section
        assert "Attribution date mentions:" in section
        certificate = row.get("source_certificate")
        if certificate:
            assert escape(certificate["facts"], quote=False) in section
            assert escape(certificate["original_certificate"], quote=False) in section
    assert web.count("](#source-attribution-note-") == len(texts)
    assert "## Source Attribution Notes" not in markdown


def test_native_linear_mathml_survives_trusted_kpress_without_a_js_renderer():
    native = paper.polynomial_markdown(
        "H_{132,4}", _polynomial(["2", "-5"]), degree=1, context="native control", web=True
    )
    document = parse_markdown(native, title="native control", trust_mode="trusted", math="auto")
    assert not document.diagnostics
    assert "<mi>H</mi>" in document.html
    assert "<mn>132</mn><mo>,</mo><mn>4</mn>" in document.html
    assert "<mn>2</mn><mi>s</mi><mo>&#x2212;</mo><mn>5</mn>" in document.html
    assert 'tabindex="0"' in document.html
    assert 'kpress-math-render"' not in document.html


def test_html_byte_measurement_reports_sections_without_publishing(tmp_path, capsys):
    assert paper.main(["--site", str(tmp_path), "--revision", REVISION, "--measure"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["published_html_bytes"][paper.COMPLETE_PATH] > 0
    assert report["generated_section_html_bytes"]["CURRENT_POLYNOMIALS"] > 0
    assert report["generated_section_html_bytes"]["HISTORICAL_POLYNOMIALS"] > 0
    assert list(tmp_path.iterdir()) == []


def test_native_equations_reconstruct_every_published_coefficient_and_exponent():
    register = exact_catalogue.publication_register(paper.load_register())
    rows = [(row, f"P_{{{row['n']}}}") for row in register["entries"] if row.get("polynomial")]
    seen = {}
    for row in register["historical_entries"]:
        n = row["n"]
        seen[n] = seen.get(n, 0) + 1
        rows.append((row, f"H_{{{n},{seen[n]}}}"))
    namespace = "{http://www.w3.org/1998/Math/MathML}"
    for entry, name in rows:
        expected = [int(value) for value in entry["polynomial"]["coefficients"]]
        degree = entry["degree"]
        native = paper.polynomial_markdown(
            name, entry["polynomial"], degree=degree, context=f"n={entry['n']}", web=True
        )
        label = native.split("<msub>", 1)[1].split("</msub>", 1)[0]
        assert f"<mi>{name[0]}</mi>" in label
        for index in name.split("{", 1)[1].rstrip("}").split(","):
            assert f"<mn>{index}</mn>" in label
        if 'class="kpress-table coefficient-table"' in native:
            assert _web_coefficient_rows(native) == [
                (str(degree - index), str(value)) for index, value in enumerate(expected)
            ]
            assert f"<mn>{degree}</mn></msubsup>" in native
            continue
        found = [0] * (degree + 1)
        # Renderer-authored names and integers cannot introduce XML declarations.
        for fragment in native.split('<math display="block">')[1:]:
            tree = ET.fromstring(
                '<math xmlns="http://www.w3.org/1998/Math/MathML">'
                + fragment.split("</math>", 1)[0]
                + "</math>"
            )
            body = tree.find(namespace + "mrow")
            assert body is not None
            children = list(body)
            if children[0].tag == namespace + "mphantom":
                terms = children[1:]
            else:
                equals = next(
                    index
                    for index, node in enumerate(children)
                    if node.tag == namespace + "mo" and node.text == "="
                )
                terms = children[equals + 1 :]
            if terms[-2].tag == namespace + "mo" and terms[-2].text == "=":
                terms = terms[:-2]
            cursor = 0
            while cursor < len(terms):
                sign = 1
                node = terms[cursor]
                if node.tag == namespace + "mo":
                    sign = -1 if node.text == "\u2212" else 1
                    cursor += 1
                    node = terms[cursor]
                magnitude = 1
                if node.tag == namespace + "mn":
                    assert node.text is not None
                    magnitude = int(node.text)
                    cursor += 1
                power = 0
                if cursor < len(terms) and terms[cursor].tag == namespace + "mi":
                    assert terms[cursor].text == "s"
                    power = 1
                    cursor += 1
                elif cursor < len(terms) and terms[cursor].tag == namespace + "msup":
                    base, exponent = list(terms[cursor])
                    assert base.text == "s"
                    assert exponent.text is not None
                    power = int(exponent.text)
                    cursor += 1
                found[degree - power] += sign * magnitude
        assert found == expected, entry["n"]


def test_web_integer_cells_keep_exact_values_and_markdown_tex():
    register = paper.load_register()
    web = paper.exact_forms_markdown(register, web=True)
    markdown = paper.exact_forms_markdown(register)
    for entry in register["entries"]:
        value = entry.get("exact_form_latex")
        if entry["state"] == "integer":
            assert f"<math><mn>{value}</mn></math>" in web
            assert f"${value}$" in markdown


def test_web_legacy_headings_keep_the_actual_old_record_associations():
    register = exact_catalogue.publication_register(paper.load_register())
    current = [entry for entry in register["entries"] if entry.get("polynomial")]
    minimal = "\n\n".join(f"### Current polynomial for $n={entry['n']}$" for entry in current)
    legacy = parse_markdown(
        minimal, title="legacy headings", trust_mode="trusted", math="auto"
    ).headings
    web = paper.current_polynomials_markdown(register, web=True)
    for entry, old in zip(current, legacy, strict=True):
        section = web.split(f'<span id="current-n{entry["n"]}"></span>', 1)[1].split(
            '<span id="current-n', 1
        )[0]
        assert f'<h3 id="{old.id}">' in section
        assert f"<var>n</var>={entry['n']}" in section
    assert legacy[0].id == "current-polynomial-for-"
    assert (
        next(old.id for entry, old in zip(current, legacy, strict=True) if entry["n"] == 83)
        == "current-polynomial-for--79"
    )
    historical = register["historical_entries"]
    headings = "\n\n".join(
        f"### Historical polynomial for $n={entry['n']}$ at side `{entry['side']}`"
        for entry in historical
    )
    old = parse_markdown(
        headings, title="legacy historical headings", trust_mode="trusted", math="auto"
    ).headings
    web = paper.historical_polynomials_markdown(register, web=True)
    seen = {}
    for entry, heading in zip(historical, old, strict=True):
        n = entry["n"]
        seen[n] = seen.get(n, 0) + 1
        section = web.split(f'<span id="historical-n{n}-occurrence{seen[n]}"></span>', 1)[
            1
        ].split('<span id="historical-n', 1)[0]
        assert f'<h3 id="{heading.id}">' in section


def test_web_source_associations_remain_attached_to_every_published_record():
    register = exact_catalogue.publication_register(paper.load_register())
    checks = paper.checks_markdown(register)
    missing = paper.missing_values_markdown(register)
    for row in register["entries"]:
        if not row.get("polynomial"):
            assert f'id="current-n{row["n"]}"' in missing
            assert not row.get("source_occurrences")
            continue
        line = next(line for line in checks.splitlines() if line.startswith(f"| {row['n']} |"))
        for source in row.get("source_occurrences", []):
            assert source["path"] in line
            if source.get("url"):
                assert source["url"] in line
    history = paper.historical_polynomials_markdown(register, web=True)
    seen = {}
    for row in register["historical_entries"]:
        n = row["n"]
        seen[n] = seen.get(n, 0) + 1
        section = history.split(f'<span id="historical-n{n}-occurrence{seen[n]}"></span>', 1)[
            1
        ].split('<span id="historical-n', 1)[0]
        for source in row["sources"]:
            assert source["path"] in section
            if source.get("url"):
                assert source["url"] in section
        certificate = row.get("source_certificate")
        if certificate:
            for value in certificate.values():
                assert escape("none" if value is None else str(value), quote=False) in section
        for date in row["attribution"]["date_mentions"]:
            assert date in section


@pytest.mark.parametrize("adopted", [False, True], ids=["historical", "adopted-current"])
def test_native_web_mathml_and_custody_are_readable_without_javascript(adopted):
    from tests import site_browser  # noqa: PLC0415

    register = paper.load_register()
    selected = [row for row in register["entries"] if row["n"] in {1, 5, 83}]
    historical = deepcopy(
        next(
            row
            for row in register["historical_entries"]
            if row.get("source_certificate", {}).get("result") == "T-146"
        )
    )
    # Keep the pending-state display control even after the native offers are adopted.
    historical["kind"] = "unreconciled-source"
    historical["source_certificate"]["adoption"] = "pending"
    fixture = deepcopy(dict(register))
    certificate_record = adopted_current() if adopted else historical
    fixture["entries"] = [*selected, certificate_record] if adopted else selected
    fixture["historical_entries"] = [] if adopted else [historical]
    html, _markdown = paper.render(
        paper.ARTICLE.read_text(encoding="utf-8"), register=fixture, revision=REVISION
    )
    with site_browser.api().sync_playwright() as driver:
        browser = site_browser.launch(driver)
        try:
            context = browser.new_context(
                java_script_enabled=False, viewport={"width": 320, "height": 844}
            )
            page = context.new_page()
            page.set_content(html)
            math = page.locator(".native-polynomial-math math, .native-polynomial-math math *")
            assert math.count() > 0
            for element in math.element_handles():
                assert (
                    element.get_property("namespaceURI").json_value()
                    == "http://www.w3.org/1998/Math/MathML"
                )
            assert page.get_by_role("region", name="Polynomial equation").count() > 0
            layout = page.evaluate(WEB_LAYOUT, {"settle": False})
            assert layout["currentPolynomials"] == (4 if adopted else 3)
            assert layout["historicalPolynomials"] == (0 if adopted else 1)
            assert layout["coefficients"] >= 673
            assert not paper.web_findings(layout), layout["lostInk"]
            custody = page.locator(".source-custody")
            assert custody.locator("dt").count() == 12
            keys = (
                "result",
                "source_key",
                "revision",
                "facts",
                "original_certificate",
                "receipt",
                "verification",
                "confirmation",
                "algebraic_identity",
                "geometry_replay",
                "adoption",
                "global_optimality",
            )
            assert custody.locator("dd").all_text_contents() == [
                "none"
                if certificate_record["source_certificate"][key] is None
                else str(certificate_record["source_certificate"][key])
                for key in keys
            ]
            for element in custody.locator("dt, dd").all():
                assert element.is_visible()
                box = element.bounding_box()
                assert box is not None
                assert 0 < box["width"] <= 288
                assert box["x"] + box["width"] <= 320
        finally:
            browser.close()


def test_adopted_current_quotes_and_custody_keep_every_record_association():
    register = small_document()["register"]
    current = adopted_current()
    register["entries"].append(current)
    historical = register["historical_entries"][0]
    historical["attribution"]["source_text"] = list(current["attribution"]["source_text"])
    original = deepcopy(register)
    sections = paper.generated_sections(register, web=True)
    current_text = sections["CURRENT_POLYNOMIALS"].split('<span id="current-n155"></span>', 1)[
        1
    ]
    historical_text = sections["HISTORICAL_POLYNOMIALS"]
    assert "adopted (V3/C3)" in current_text
    assert "Global optimality remains open" in current_text
    assert current_text.count("<dt>") == 12
    for value in current["source_certificate"].values():
        assert f"<dd>{escape(value, quote=False)}</dd>" in current_text
    for status in current["source_statuses"]:
        assert status in current_text
    for number, text in enumerate(current["attribution"]["source_text"], 1):
        assert f"](#source-attribution-note-{number})" in current_text
        assert f"](#source-attribution-note-{number})" in historical_text
        quote = (
            '<blockquote class="source-quote"><p><code>'
            f"{escape(text, quote=False)}</code></p></blockquote>"
        )
        assert (current_text + historical_text).count(quote) == 1
    markdown = paper.current_polynomials_markdown(register)
    for text in current["attribution"]["source_text"]:
        assert escape(text, quote=False) in markdown
    assert register == original


def test_adopted_current_only_quotes_have_targets_without_history():
    register = {"entries": [adopted_current()], "historical_entries": []}
    text = paper.current_polynomials_markdown(register, web=True)
    assert '<span id="source-attribution-note-1"></span>' in text
    assert "](#source-attribution-note-1)" in text
