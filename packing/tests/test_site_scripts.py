"""Unknown scripts and remote/missing application assets fail the published inventory."""

from dataclasses import replace
from pathlib import Path

import pytest

from devtools import check_site_scripts, site_assets, site_urls
from devtools.check_site_scripts import inventory


def test_inventory_includes_application_assets_and_rejects_unknown_scripts(
    tmp_path: Path,
) -> None:
    (tmp_path / "published.0123456789abcdef.js").write_text("/* bundled reviewed loader */")
    (tmp_path / "workbench.0123456789abcdef.js").write_text(
        "/* bundled reviewed application */"
    )
    (tmp_path / "index.html").write_text(
        '<script type="application/json" data-application-src="workbench.0123456789abcdef.js">'
        "{}</script>"
        '<script src="published.0123456789abcdef.js"></script>'
    )
    records, errors = inventory(tmp_path)
    assert not errors
    assert len(records) == 2
    assert {row.category for row in records} == {"workbench-application"}
    (tmp_path / "new-program.js").write_text("/* an undeclared program */")
    _, errors = inventory(tmp_path)
    assert errors == ["unclassified executable script: new-program.js"]


def test_inventory_refuses_remote_missing_and_inline_unclassified_programs(
    tmp_path: Path,
) -> None:
    (tmp_path / "index.html").write_text(
        '<script src="https://example.com/script.js"></script>'
        '<script src="missing.js"></script>'
        "<script>/* undeclared startup */</script>"
    )
    _, errors = inventory(tmp_path)
    assert len(errors) == 3
    assert any("relative first-party" in error for error in errors)
    assert any("missing or outside" in error for error in errors)
    assert any("unclassified" in error for error in errors)


def test_inventory_accepts_the_actual_protocol_font_bootstrap(tmp_path: Path) -> None:
    (tmp_path / "index.html").write_text(site_assets.font_preload_bootstrap_tag())
    records, errors = inventory(tmp_path)
    assert not errors
    assert len(records) == 1
    assert records[0].category == "pre-paint"
    assert records[0].bytes < 4096
    # The reviewed marker does not waive the ordinary inline byte ceiling.
    (tmp_path / "index.html").write_text(
        site_assets.font_preload_bootstrap_tag().replace("</script>", " " * 4096 + "</script>")
    )
    _, errors = inventory(tmp_path)
    assert len(errors) == 1
    assert "exceeds 4096 bytes" in errors[0]


def test_catalogue_browser_requires_its_exact_source_and_published_asset_path() -> None:
    programs = check_site_scripts.publication_programs()
    (browser,) = [program for program in programs if not program.inline]
    source = site_urls.CATALOGUE_BROWSER_PATH
    assert check_site_scripts.classify(source, browser.text, programs=programs).category == (
        "catalogue-application"
    )
    with pytest.raises(ValueError, match="retained publication source"):
        check_site_scripts.classify(source, browser.text + "\n", programs=programs)
    with pytest.raises(ValueError, match="unclassified"):
        check_site_scripts.classify("papers/unowned.js", browser.text, programs=programs)
    oversized = replace(browser, text=browser.text + " " * (browser.limit + 1))
    with pytest.raises(ValueError, match="exceeds"):
        check_site_scripts.classify(source, oversized.text, programs=(oversized,))


def test_template_inline_programs_require_source_identity_owned_pages_and_byte_caps() -> None:
    programs = check_site_scripts.publication_programs()
    source = site_urls.CATALOGUE_ARCHIVE_PATH + "#script-4"
    inline = [program for program in programs if program.inline]
    assert len(inline) == 3
    for program in inline:
        classified = check_site_scripts.classify(
            source, program.text, inline=True, programs=programs
        )
        assert classified.bytes == len(program.text.encode()) <= program.limit
        with pytest.raises(ValueError, match="exceeds 4096"):
            check_site_scripts.classify(
                source, program.text + "\n", inline=True, programs=programs
            )
        with pytest.raises(ValueError, match="exceeds 4096"):
            check_site_scripts.classify(
                "unowned.html#script-1", program.text, inline=True, programs=programs
            )
        oversized = replace(program, text=program.text + " " * (program.limit + 1))
        with pytest.raises(ValueError, match="exceeds"):
            check_site_scripts.classify(
                source, oversized.text, inline=True, programs=(oversized,)
            )


def test_copied_paper_alias_keeps_approved_footer_and_math_programs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    archive = site_urls.SiteURL(
        path=site_urls.CATALOGUE_ARCHIVE_PATH,
        canonical=site_urls.CATALOGUE_ARCHIVE_PATH,
        kind="archive-file",
        generator=site_urls.CATALOGUE_GENERATOR,
        producer=site_urls.CATALOGUE_PRODUCER,
        first_published="2026-10-07",
        lastmod="2026-10-08",
    )
    alias = replace(
        archive,
        path="old-exact-values.html",
        kind="copy",
        producer="assembly",
        generator="fixture:copy",
        target=archive.path,
    )
    monkeypatch.setattr(site_urls, "load_registry", lambda: [archive, alias])
    programs = check_site_scripts.publication_programs()
    for program in programs:
        if program.inline:
            assert (
                check_site_scripts.classify(
                    alias.path + "#script-1", program.text, inline=True, programs=programs
                ).category
                == program.category
            )
