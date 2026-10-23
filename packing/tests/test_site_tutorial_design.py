"""Published tutorials use the paper figure and caption roles without changing prose."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

import pytest

from devtools import paper_structure, repo_links
from sqpack.probes import probe
from tests import site_browser, site_renders


@pytest.fixture(scope="module")
def pages(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    return site_renders.write(
        tmp_path_factory.mktemp("tutorial-design"), "tutorial.html", "tutorial-advanced.html"
    )


def test_tutorial_figures_have_attached_captions_and_preserve_their_links(
    pages: dict[str, Path],
) -> None:
    for name, path in pages.items():
        tree = paper_structure.parse(path.read_text())
        figures = tree.find_all("figure")
        assert len(tree.find_all("img", "site-packing-diagram")) == 1
        assert len(figures) == (1 if name == "tutorial.html" else 4)
        for figure in figures:
            image = figure.find("img")
            caption = figure.find("figcaption")
            assert image is not None
            assert image.attrs.get("alt")
            if "site-packing-diagram" in image.classes:
                assert image.attrs["src"].startswith("assets/images/")
                svg = ET.parse(path.parent / image.attrs["src"]).getroot()
                x, y, width, height = (float(value) for value in svg.attrib["viewBox"].split())
                outline = svg.find('.//*[@data-feature="container-outline"]')
                assert outline is not None
                assert x + width / 2 == pytest.approx(
                    float(outline.attrib["x"]) + float(outline.attrib["width"]) / 2
                )
                assert y + height / 2 == pytest.approx(
                    float(outline.attrib["y"]) + float(outline.attrib["height"]) / 2
                )
            assert caption is not None
            assert caption.text().strip()
            assert not any(
                isinstance(child, paper_structure.Node) and child.tag == "em"
                for child in caption.children
            )
        # Existing source-derived fragments and mathematical exposition stay available.
        assert tree.find_all("h2")
        assert any(node.attrs.get("id") for node in tree.find_all("h3"))


def test_tutorial_diagrams_are_centred_and_captions_use_shared_paper_type(
    pages: dict[str, Path],
) -> None:
    measure = probe(Path(__file__).with_name("probes"), "site_tutorial/design")
    with site_browser.api().sync_playwright() as driver:
        browser = site_browser.launch(driver)
        page = browser.new_page()

        def local_image(route: Any) -> None:
            source = unquote(urlsplit(route.request.url).path.partition("/main/")[2])
            route.fulfill(
                content_type="image/svg+xml", body=(repo_links.REPO / source).read_bytes()
            )

        page.route("https://raw.githubusercontent.com/**/*.svg", local_image)
        for path in pages.values():
            page.goto(path.as_uri(), wait_until="load")
            for width in (1280, 390):
                page.set_viewport_size({"width": width, "height": 900})
                found = page.evaluate(measure)
                assert found["figures"]
                assert found["measure"] <= 630.5
                assert not found["overflow"]
                for figure in found["figures"]:
                    assert figure["loaded"]
                    assert abs(figure["imageCentre"] - figure["figureCentre"]) < 0.5
                    assert figure["imageWidth"] <= figure["figureWidth"] + 0.5
                    assert "Source Sans" in figure["font"]
                    assert figure["style"] == "normal"
                    assert figure["weight"] == "410"
                    assert figure["size"] == pytest.approx(found["noteSize"], abs=0.05)
                    assert figure["leading"] == pytest.approx(1.4, abs=0.005)
                assert "PT Serif" in found["bodyFont"]
                assert "PT Serif" in found["sectionFont"]
                assert found["sectionStyle"] == "italic"
        browser.close()
