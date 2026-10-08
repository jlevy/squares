"""The site's shared assets: how they are named, written, linked, checked and put back.

`devtools.site_assets` publishes what every site page carries as content-hashed files
under `assets/`; `render_overview` links them, `render_case_pages.rebase_links` moves a
page's links when it stands in a directory, and `check_published_site.asset_checks`
holds a built or deployed site to serving them whole. Each is tested here on fixtures,
with the negative control beside the rule.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from devtools import check_published_site, render_overview, site_assets
from devtools.render_case_pages import rebase_links
from tests import site_renders

FACE = b"wOF2 a face"
#: A page program's bytes, which the bundle only names and copies.
PROGRAM = "a page program"
SCRIPT = site_assets.SiteAssets().script("x.js", PROGRAM)


def _bundle() -> tuple[site_assets.SiteAssets, str, str]:
    assets = site_assets.SiteAssets()
    url = assets.face("pt-serif-latin-400-normal.woff2", FACE)
    sheet = assets.stylesheet("kpress.css", f'@font-face {{ src: url("{url}"); }}')
    script = assets.script("table.js", PROGRAM)
    page = (
        f"<head>{site_assets.preload_tags(assets, 'index.html')}\n"
        f"{site_assets.stylesheet_tag(sheet, 'index.html')}</head>"
        f"<body>{site_assets.script_tag(script, 'index.html')}</body>"
    )
    return assets, url, page


def test_a_file_is_named_by_its_content() -> None:
    assets, url, _ = _bundle()
    digest = hashlib.sha256(FACE).hexdigest()[:16]
    assert url == f"../fonts/pt-serif-latin-400-normal.{digest}.woff2"
    ref = assets.script("table.js", PROGRAM + " again")
    assert ref.output_path is not None
    assert ref.output_path != assets.script("table.js", PROGRAM).output_path


def test_a_page_names_a_file_from_where_it_is_served() -> None:
    ref = site_assets.SiteAssets().script("x.js", "1")
    assert site_assets.asset_href(ref, "index.html") == f"assets/{ref.output_path}"
    assert site_assets.asset_href(ref, "cases/index.html") == f"../assets/{ref.output_path}"


def test_a_page_with_a_closing_tag_in_its_asset_is_refused() -> None:
    with pytest.raises(SystemExit):
        site_assets.SiteAssets().script("x.js", "'</script>'")
    with pytest.raises(SystemExit):
        site_assets.SiteAssets().stylesheet("x.css", "/* </style> */")


def test_what_a_page_names_includes_its_stylesheets_faces() -> None:
    assets, url, page = _bundle()
    files = assets.referenced([page])
    assert url.removeprefix("../") in files
    assert len(files) == 3  # the stylesheet, its face and the script
    with pytest.raises(SystemExit, match="no build wrote"):
        assets.referenced(['<script src="assets/js/gone.0000000000000000.js"></script>'])


def test_independent_builds_keep_each_others_assets(tmp_path: Path) -> None:
    assets, _, page = _bundle()
    files = assets.referenced([page])
    left = tmp_path / "assets" / "js" / "old.0000000000000000.js"
    left.parent.mkdir(parents=True)
    left.write_text("stale", encoding="utf-8")
    assert site_assets.stale_assets(tmp_path, files)
    site_assets.write_assets(tmp_path, files)
    assert left.exists()
    assert site_assets.stale_assets(tmp_path, files) == []
    assert site_assets.stale_assets(tmp_path, files, exact=True) == [
        "assets/js/old.0000000000000000.js"
    ]
    (tmp_path / "assets" / next(iter(files))).write_bytes(b"changed")
    assert site_assets.stale_assets(tmp_path, files) == [f"assets/{next(iter(files))}"]


def test_a_page_put_back_whole_carries_its_assets(tmp_path: Path) -> None:
    assets, _, page = _bundle()
    whole = assets.inlined(page)
    assert PROGRAM in whole
    assert 'url("data:font/woff2;base64,' in whole
    assert "assets/" not in whole
    (tmp_path / "index.html").write_text(page, encoding="utf-8")
    site_assets.write_assets(tmp_path, assets.referenced([page]))
    assert site_assets.inlined_from(tmp_path, "index.html") == whole


def test_a_page_may_fetch_its_shared_assets_and_nothing_else() -> None:
    _, _, page = _bundle()
    render_overview.assert_fetches_only_assets("index.html", page)
    render_overview.assert_fetches_only_assets(
        "cases/index.html", page.replace('"assets/', '"../assets/')
    )
    for fetch in (
        '<script src="vendor/x.js"></script>',
        '<link rel="stylesheet" href="https://example.com/x.css">',
        '<link rel="stylesheet" href="styles/x.css">',
        '<link rel="icon" href="assets/icon.svg">',
        "<style>@import 'x.css';</style>",
        '<style>body { background: url("x.png"); }</style>',
    ):
        with pytest.raises(SystemExit, match="fetches more"):
            render_overview.assert_fetches_only_assets("x.html", fetch)


def test_a_rebase_moves_a_scripts_source_and_not_a_styles_text() -> None:
    markup = (
        f"{site_assets.script_tag(SCRIPT, 'index.html')}"
        "<style>/* assets/css/y.css */</style>"
        '<link rel="stylesheet" href="assets/css/z.0000000000000000.css">'
    )
    moved = rebase_links(markup, "cases")
    assert site_assets.script_tag(SCRIPT, "cases/index.html") in moved
    assert "<style>/* assets/css/y.css */</style>" in moved
    assert 'href="../assets/css/z.0000000000000000.css"' in moved


def test_the_deploy_check_holds_every_named_file_to_its_bytes() -> None:
    assets, _, page = _bundle()
    files = {f"assets/{path}": data for path, data in assets.referenced([page]).items()}
    pages = {"index.html": page, "cases/index.html": page.replace('"assets/', '"../assets/')}
    [(ok, line)] = check_published_site.asset_checks(pages, files.get)
    assert ok, line
    assert "each of 3 files" in line
    face = next(path for path in files if path.endswith(".woff2"))
    missing = {path: data for path, data in files.items() if path != face}
    [(ok, line)] = check_published_site.asset_checks(pages, missing.get)
    assert not ok
    assert "is not served" in line
    altered = {**files, face: b"another face"}
    [(ok, line)] = check_published_site.asset_checks(pages, altered.get)
    assert not ok
    assert "not the bytes" in line
    [(ok, line)] = check_published_site.asset_checks({"x.html": "<p></p>"}, files.get)
    assert ok
    assert "no page here names one" in line


@pytest.fixture(scope="module")
def home() -> tuple[str, str]:
    """The overview as written, and as served with its assets put back."""
    return site_renders.html("index.html"), site_renders.served("index.html")


def test_every_site_page_links_the_shared_design_system(home: tuple[str, str]) -> None:
    """The site's pages carry no face or KaTeX inline, and name the shared files; put
    back whole, they carry what the explainer's functions give."""
    from devtools.render_n11_lower_bounds_explainer import (  # noqa: PLC0415
        katex_js,
        kpress_static,
    )

    page, served = home
    assert "@font-face" not in page
    assert 'rel="preload"' in page
    assert katex_js(kpress_static()) not in page
    assert katex_js(kpress_static()) in served


def test_asset_publication_refuses_changed_content_at_an_existing_path(tmp_path: Path) -> None:
    site_assets.write_assets(tmp_path, {"js/example.1234567890123456.js": b"one"})
    with pytest.raises(ValueError, match="asset collision"):
        site_assets.write_assets(tmp_path, {"js/example.1234567890123456.js": b"two"})
    assert (tmp_path / "assets/js/example.1234567890123456.js").read_bytes() == b"one"


def test_linked_inline_assets_preserve_order_fonts_and_json(tmp_path: Path) -> None:
    inline = "<head><style>@font-face{src:url(data:font/woff2;base64,d09GMg==)}</style>"
    inline += "<script>bootstrap</script></head><body><script>application</script>"
    inline += '<script type="application/json">{"kept":true}</script></body>'
    linked, files = site_assets.link_inline_assets(inline, "papers/example.html")
    assert "base64" not in linked
    assert "<script>bootstrap</script>" in linked
    assert '<script type="application/json">{"kept":true}</script>' in linked
    assert '<script src="../assets/js/' in linked
    assert any(path.endswith(".woff2") for path in files)
    site_assets.write_assets(tmp_path, files)
    page = tmp_path / "papers/example.html"
    page.parent.mkdir()
    page.write_text(linked)
    restored = site_assets.read_inline_page(page)
    assert "<script>application</script>" in restored
    assert "base64,d09GMg==" in restored
