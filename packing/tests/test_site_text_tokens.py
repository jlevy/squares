"""The site's pages resolve the explainer's text tokens and faces, in a browser.

`paper-type.css` is the one source of the type base, the reading measure, the h2 scale
and the pinned faces; `test_overview` holds every page to inlining it. This opens a
rendered long report (the tutorial, with a contents rail) and a short one (the
readme) in Chromium and pins what those tokens resolve to, which is what the explainer
resolves (`templates/paper-design.md`, Text). It also injects the host font hook an
embedding viewer might set, and requires the page to keep its own faces.

Skipped where no Chromium can be launched; `SQPACK_CHROMIUM` names one the environment
supplies, as the other browser tools read it.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from devtools.measure_site_pages import TYPOGRAPHY
from devtools.render_n11_lower_bounds_explainer_pdf import BROWSER_OVERRIDE
from tests import site_renders

#: The explainer's resolved values at a 1280px desktop, from `measure_site_pages type`.
EXPLAINER = {
    "--kpress-font-size-base": "18px",
    "--kpress-measure": "calc(18px * 35)",
    "--kpress-font-size-h2": "calc(18px * 1.2)",
}
SANS = '"Source Sans 3 Variable"'
#: A face no page ships, as an embedding viewer's hook would name one.
FOREIGN = "Comic Sans MS"


@pytest.fixture(scope="module")
def browser() -> Iterator[Any]:
    sync_api = pytest.importorskip("playwright.sync_api")
    with sync_api.sync_playwright() as driver:
        try:
            launched = driver.chromium.launch(executable_path=os.environ.get(BROWSER_OVERRIDE))
        except sync_api.Error as error:
            pytest.skip(f"no Chromium to launch: {error.message.splitlines()[0]}")
        yield launched
        launched.close()


@pytest.fixture(scope="module")
def pages(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    return site_renders.write(
        tmp_path_factory.mktemp("site"),
        "tutorial.html",
        "tutorial-advanced.html",
        "readme.html",
    )


def typography(browser: Any, path: Path, *, host_font: bool = False) -> dict[str, Any]:
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    try:
        page.goto(path.as_uri(), wait_until="load")
        if host_font:
            page.add_style_tag(
                content=(
                    ":root, .kpress, .kpress-page-main {"
                    f' --kpress-host-font-sans: "{FOREIGN}";'
                    f' --kpress-host-font-prose: "{FOREIGN}"; }}'
                )
            )
        return page.evaluate(TYPOGRAPHY)
    finally:
        page.close()


@pytest.mark.parametrize("name", ["tutorial.html", "tutorial-advanced.html", "readme.html"])
def test_a_report_resolves_the_explainers_text_tokens(
    browser: Any, pages: dict[str, Path], name: str
) -> None:
    measured = typography(browser, pages[name])
    tokens = measured["column_tokens"]
    for token, value in EXPLAINER.items():
        assert tokens[token].replace(" ", "") == value.replace(" ", ""), token
    assert tokens["--kpress-font-sans"].startswith(SANS)
    roles = measured["roles"]
    assert roles["p"]["size"] == "18px"
    assert roles["p"]["line_height"] == "27px"
    assert roles["p"]["text_width"] == "710px"
    assert roles["h2"]["size"] == "21.6px"


def test_a_viewers_host_font_hook_does_not_replace_the_sites_faces(
    browser: Any, pages: dict[str, Path]
) -> None:
    measured = typography(browser, pages["tutorial-advanced.html"], host_font=True)
    tokens = measured["column_tokens"]
    assert FOREIGN not in tokens["--kpress-font-sans"]
    assert FOREIGN not in tokens["--kpress-font-prose"]
    assert measured["roles"]["h3"]["family"] == SANS.strip('"')
