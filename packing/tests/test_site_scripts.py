"""Unknown scripts and remote/missing application assets fail the published inventory."""

from dataclasses import replace
from pathlib import Path

import pytest

from devtools import (
    check_published_site,
    check_site_scripts,
    render_overview,
    site_assets,
    site_urls,
)
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


@pytest.mark.parametrize(
    ("family", "linked_name"),
    [
        ("headroom", "headroom.0123456789abcdef.js"),
        ("headroom", "page.0123456789abcdef.js"),
        ("rating-tooltips", "rating-tooltips.0123456789abcdef.js"),
        ("rating-tooltips", "page.0123456789abcdef.js"),
    ],
)
def test_inventory_accepts_reviewed_shared_interaction_programs(
    tmp_path: Path, family: str, linked_name: str
) -> None:
    source = Path(__file__).parents[1] / "devtools" / "overview" / f"{family}.js"
    (tmp_path / linked_name).write_text(source.read_text())
    (tmp_path / "index.html").write_text(f'<script src="{linked_name}"></script>')
    records, errors = inventory(tmp_path)
    assert not errors
    assert len(records) == 1
    assert records[0].category == "input-response"


def test_catalogue_browser_requires_its_exact_source_and_published_asset_path() -> None:
    programs = check_site_scripts.publication_programs()
    (browser,) = [
        program for program in programs if site_urls.CATALOGUE_BROWSER_PATH in program.paths
    ]
    source = site_urls.CATALOGUE_BROWSER_PATH
    assert check_site_scripts.classify(source, browser.text, programs=programs).category == (
        "catalogue-application"
    )
    with pytest.raises(ValueError, match="retained publication source"):
        check_site_scripts.classify(source, browser.text + "\n", programs=programs)
    with pytest.raises(ValueError, match="unclassified"):
        check_site_scripts.classify("papers/unowned.js", browser.text, programs=programs)
    oversized = replace(browser, text=browser.text + " " * ((browser.limit or 0) + 1))
    with pytest.raises(ValueError, match="exceeds"):
        check_site_scripts.classify(source, oversized.text, programs=(oversized,))


def test_template_programs_are_linked_and_require_their_complete_source() -> None:
    programs = check_site_scripts.publication_programs()
    linked = [program for program in programs if program.limit is None]
    assert len(linked) == 3
    assert all(not program.inline for program in programs)
    for program in linked:
        (source,) = program.paths
        assert source.startswith("assets/js/page.")
        assert check_site_scripts.classify(
            source, program.text, programs=programs
        ).category == (program.category)
        with pytest.raises(ValueError, match="retained publication source"):
            check_site_scripts.classify(source, program.text + "\n", programs=programs)
        with pytest.raises(ValueError, match="exceeds 4096"):
            check_site_scripts.classify(
                site_urls.CATALOGUE_ARCHIVE_PATH + "#script-1",
                program.text,
                inline=True,
                programs=programs,
            )
    math = [program for program in linked if program.category == "deferred-math"]
    assert len(math) == 2
    assert any("viewport" in program.reason for program in math)
    assert all("prepared primary" not in program.reason for program in math)


def test_registered_forwarder_marker_cannot_waive_the_inline_limit() -> None:
    with pytest.raises(ValueError, match="exceeds 4096"):
        check_site_scripts.classify(
            "old.html#script-1",
            "// Input response and registered forwarding:" + " " * 4096,
            inline=True,
        )


def test_actual_forwarders_publish_their_registered_script(tmp_path: Path) -> None:
    pages = render_overview.forwarder_pages()
    assert [page.name for page in pages] == [old for old, _ in render_overview.MOVED_PAGES]
    files = render_overview.asset_files(pages)
    for page in pages:
        target = tmp_path / page.name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page.html)
        assert len(page.html.encode()) <= site_urls.HARD_HTML_LIMIT
    site_assets.write_assets(tmp_path, files)
    records, errors = inventory(tmp_path)
    assert errors == []
    assert len(records) == 1
    (record,) = records
    assert record.category == "registered-forwarder"
    source = render_overview.FORWARD_SCRIPT.read_bytes()
    assert record.bytes == len(source)
    assert (tmp_path / record.source).read_bytes() == source
    for page in pages:
        relative = "../" * page.name.count("/") + record.source
        tag = f'<script src="{relative}"></script>'
        assert page.html.count(tag) == 1
        assert page.html.index(tag) < page.html.index("</head>")
    pages_by_name = {page.name: page.html for page in pages}
    [(ok, _)] = check_published_site.asset_checks(
        pages_by_name, lambda name: (tmp_path / name).read_bytes()
    )
    assert ok
    (tmp_path / record.source).write_bytes(source + b"\n")
    [(ok, reason)] = check_published_site.asset_checks(
        pages_by_name, lambda name: (tmp_path / name).read_bytes()
    )
    assert not ok
    assert "not the bytes" in reason
    (tmp_path / record.source).unlink()
    _, errors = inventory(tmp_path)
    assert set(errors) == {
        f"script asset missing or outside publication: {prefix}{record.source}"
        for prefix in ("", "../")
    }
