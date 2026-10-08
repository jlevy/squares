"""The compact catalogue fetches only the selected metadata and opened coefficients."""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import pytest
from playwright.sync_api import Page, Route, expect, sync_playwright

from sqpack.probes import probe
from tests import site_browser

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "devtools/templates"
SCRIPT = ROOT / "devtools/overview/exact-side-values.js"


def entry(n: int, *, section: str = "current", suffix: str = "") -> dict[str, Any]:
    identity = f"{section}-n{n}{suffix}"
    numeric = n == 2 and section == "current"
    return {
        "id": identity,
        "section": section,
        "kind": "numeric" if numeric else "polynomial",
        "n": n,
        "component": "recorded-side" if numeric else f"P_{n}",
        "title": f"{section.title()} n = {n}{suffix}",
        "status": "open" if section == "current" else "source-invalid",
        "degree": None if numeric else 15,
        "coefficient_digits": None if numeric else 724,
        "metadata_url": f"data/{identity}.json",
        "coefficients_url": None if numeric else f"data/{identity}-coefficients.json",
        "legacy_anchor": f"current-polynomial-for--{n}" if not numeric else None,
        "search_text": "source catalogue invalid"
        if section == "historical"
        else "source catalogue",
    }


class Catalogue:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.requests: list[str] = []
        self.fail: set[str] = set()
        self.held: dict[str, Route] = {}
        self.hold: set[str] = set()
        self.entries = (
            [entry(n) for n in range(1, 31)]
            + [entry(7, section="historical", suffix=f"-s{index}") for index in range(6)]
            + [entry(1850, section="historical", suffix="-s1")]
        )
        self.coefficients = ["1", "0", "-" + "9" * 724, *[str(n) for n in range(12)], "+12"]
        self.data: dict[str, Any] = {
            "/index.json": {"schema_version": 1, "entries": self.entries}
        }
        for row in self.entries:
            identity = row["id"]
            self.data[f"/data/{identity}.json"] = {
                "schema_version": 1,
                "id": identity,
                "section": row["section"],
                "kind": row["kind"],
                "claim": "reported packing upper bound; optimum open",
                "record": {
                    "n": row["n"],
                    "status": row["status"],
                    "kind": "superseded" if row["section"] == "historical" else "polynomial",
                    "source_statuses": ["fixed", "invalid"],
                    "side": {"relation": "upper-bound", "value": "1.234567890123456789"},
                    "checks": {
                        "root": {
                            "unique": True,
                            "source_index": {"stated": 27, "counted": None},
                        },
                    },
                    "sources": [
                        {"url": "https://example.test/source", "source_flags": ["invalid"]}
                    ],
                    "attribution": {
                        "source_text": ["[Explore group](https://example.test/) <b>source</b>"]
                    },
                },
            }
            if row["coefficients_url"]:
                self.data[f"/data/{identity}-coefficients.json"] = {
                    "schema_version": 1,
                    "id": identity,
                    "order": "descending",
                    "coefficients": self.coefficients,
                }
        shell = (TEMPLATES / "exact-side-values-browser-shell.html").read_text()
        values = {
            "BROWSER_STYLE": (TEMPLATES / "exact-side-values-browser.css").read_text(),
            "BROWSER_INDEX_URL": "index.json",
            "BROWSER_SCRIPT_URL": "browser.js",
            "COMPLETE_HTML_URL": "complete.html",
            "COMPLETE_MARKDOWN_URL": "complete.md",
            "COMPLETE_PDF_URL": "complete.pdf",
        }
        for name in (
            "PAGE_HEAD",
            "BROWSER_VERSION",
            "REGISTER_SOURCE_URL",
            "SITE_FAVICON",
            "SITE_NAV",
            "SITE_NAV_CSS",
            "SITE_THEME",
            "THEME_BOOTSTRAP",
            "COLOPHON",
        ):
            values[name] = ""
        for name, value in values.items():
            shell = shell.replace("{{" + name + "}}", value)
        self.shell = shell
        page.route("https://catalogue.test/**", self.route)

    def route(self, route: Route) -> None:
        path = urlparse(route.request.url).path
        self.requests.append(path)
        if path in self.hold:
            self.held[path] = route
        elif path in self.fail:
            route.fulfill(status=503, body="temporarily unavailable")
        elif path == "/browser.js":
            route.fulfill(content_type="text/javascript", body=SCRIPT.read_text())
        elif path == "/":
            route.fulfill(content_type="text/html", body=self.shell)
        elif path in self.data:
            route.fulfill(content_type="application/json", body=json.dumps(self.data[path]))
        else:
            route.fulfill(status=404, body="missing")

    def open(self, hash_value: str = "") -> None:
        self.page.goto("https://catalogue.test/" + hash_value)
        expect(self.page.locator("#index-message")).to_contain_text("entries")


@pytest.fixture
def catalogue() -> Iterator[Catalogue]:
    with sync_playwright() as driver:
        browser = site_browser.launch(driver)
        try:
            yield Catalogue(browser.new_page())
        finally:
            browser.close()


def test_index_is_bounded_searchable_and_keeps_numeric_and_historical_entries(
    catalogue: Catalogue,
) -> None:
    page = catalogue.page
    catalogue.open()
    assert catalogue.requests == ["/", "/browser.js", "/index.json"]
    assert page.locator("#entry-list > li").count() == 25
    expect(page.locator("#entry-list")).to_contain_text("Numeric")
    page.get_by_role("button", name="Next entries").click()
    assert page.locator("#entry-list > li").count() == 5
    page.get_by_label("Search entries").fill("n:7")
    assert page.locator("#entry-list > li").count() == 1
    page.get_by_label("Catalogue section").select_option("historical")
    assert page.locator("#entry-list > li").count() == 6
    page.get_by_label("Search entries").fill("n:1850")
    assert page.locator("#entry-list > li").count() == 1
    page.get_by_label("Search entries").fill("does-not-exist")
    expect(page.locator("#index-message")).to_contain_text("No entries match")
    page.get_by_role("button", name="Clear filters").click()
    assert page.locator("#entry-list > li").count() == 25
    assert not any(path.startswith("/data/") for path in catalogue.requests)


def test_legacy_selection_lazy_coefficients_and_complete_integer_strings(
    catalogue: Catalogue,
) -> None:
    page = catalogue.page
    catalogue.open("#current-polynomial-for--1")
    expect(page.locator("#detail-title")).to_have_text("Current n = 1")
    expect(page.locator("#metadata")).to_contain_text("polynomial")
    expect(page.locator("#metadata")).to_contain_text("[Explore group]")
    assert page.locator("#metadata b").count() == 0
    assert not any("coefficients" in path for path in catalogue.requests)
    page.get_by_role("button", name="Open coefficients").click()
    expect(page.locator("#coefficient-body tr")).to_have_count(12)
    assert (
        page.locator("#coefficient-body code").nth(2).text_content()
        == catalogue.coefficients[2]
    )
    assert page.locator("#coefficient-body code").nth(1).text_content() == "0"
    page.get_by_role("button", name="Next coefficients").click()
    expect(page.locator("#coefficient-body tr")).to_have_count(4)
    assert page.locator("#coefficient-body code").last.text_content() == "+12"
    expect(
        page.get_by_role("link", name="Download complete coefficient JSON")
    ).to_have_attribute("href", "data/current-n1-coefficients.json")


def test_request_and_coefficient_errors_have_working_retries(catalogue: Catalogue) -> None:
    page = catalogue.page
    catalogue.fail.add("/index.json")
    page.goto("https://catalogue.test/")
    expect(page.locator("#index-message")).to_contain_text("HTTP 503")
    catalogue.fail.clear()
    page.get_by_role("button", name="Retry index").click()
    expect(page.locator("#index-message")).to_contain_text("entries")
    catalogue.fail.add("/data/current-n1.json")
    page.get_by_role("link", name="Current n = 1", exact=False).first.click()
    expect(page.locator("#detail-message")).to_contain_text("HTTP 503")
    catalogue.fail.clear()
    page.get_by_role("button", name="Retry entry").click()
    expect(page.locator("#detail-content")).to_be_visible()
    payload = catalogue.data["/data/current-n1-coefficients.json"]
    payload["coefficients"] = [1, *catalogue.coefficients[1:]]
    page.get_by_role("button", name="Open coefficients").click()
    expect(page.locator("#coefficient-message")).to_contain_text("integer strings")
    expect(page.locator("#coefficient-actions")).to_be_hidden()
    payload["coefficients"] = catalogue.coefficients
    page.get_by_role("button", name="Retry coefficients").click()
    expect(page.locator("#coefficient-body tr")).to_have_count(12)
    page.context.grant_permissions(["clipboard-read", "clipboard-write"])
    page.get_by_role("button", name="Copy complete coefficient JSON").click()
    expect(page.locator("#coefficient-message")).to_contain_text("Copied the complete")
    copied = json.loads(
        page.evaluate(probe(ROOT / "tests/probes", "exact_side_values_browser/clipboard"))
    )
    assert copied["coefficients"] == catalogue.coefficients


def test_delayed_requests_cannot_replace_the_new_selection(catalogue: Catalogue) -> None:
    page = catalogue.page
    catalogue.open()
    old_metadata = "/data/current-n1.json"
    catalogue.hold.add(old_metadata)
    with page.expect_request("**/data/current-n1.json"):
        page.get_by_role("link", name="Current n = 1", exact=False).first.click()
    page.get_by_role("link", name="Current n = 2", exact=False).first.click()
    expect(page.locator("#detail-title")).to_have_text("Current n = 2")
    expect(page.locator("#detail-content")).to_be_visible()
    catalogue.held[old_metadata].fulfill(
        content_type="application/json", body=json.dumps(catalogue.data[old_metadata])
    )
    page.wait_for_load_state("networkidle")
    expect(page.locator("#detail-title")).to_have_text("Current n = 2")
    expect(page.locator("#coefficient-section")).to_be_hidden()
    page.get_by_role("link", name="Current n = 3", exact=False).first.click()
    expect(page.locator("#detail-content")).to_be_visible()
    old_coefficients = "/data/current-n3-coefficients.json"
    catalogue.hold.add(old_coefficients)
    with page.expect_request("**/data/current-n3-coefficients.json"):
        page.get_by_role("button", name="Open coefficients").click()
    page.get_by_role("link", name="Current n = 2", exact=False).first.click()
    expect(page.locator("#detail-content")).to_be_visible()
    catalogue.held[old_coefficients].fulfill(
        content_type="application/json", body=json.dumps(catalogue.data[old_coefficients])
    )
    page.wait_for_load_state("networkidle")
    expect(page.locator("#detail-title")).to_have_text("Current n = 2")
    expect(page.locator("#coefficient-body tr")).to_have_count(0)
    expect(page.locator("#coefficient-section")).to_be_hidden()


def test_mobile_keyboard_and_disabled_javascript_fallback(catalogue: Catalogue) -> None:
    page = catalogue.page
    page.set_viewport_size({"width": 390, "height": 844})
    catalogue.open()
    link = page.get_by_role("link", name="Current n = 1", exact=False).first
    link.focus()
    page.keyboard.press("Enter")
    expect(page.locator("#detail-title")).to_be_focused()
    expect(page.locator("#detail-content")).to_be_visible()
    bounds = page.locator("#exact-browser").bounding_box()
    assert bounds is not None
    assert bounds["width"] <= 390
    browser = page.context.browser
    assert browser is not None
    context = browser.new_context(java_script_enabled=False)
    try:
        fallback = Catalogue(context.new_page())
        fallback.page.goto("https://catalogue.test/")
        expect(
            fallback.page.get_by_role("link", name="Read the complete HTML catalogue")
        ).to_have_attribute("href", "complete.html")
        assert fallback.requests == ["/"]
    finally:
        context.close()
