"""One render of each site page, and of each result's overview, per test process.

Rendering a page of the site costs seconds: the overview and the frontier atlas about
two each, the case records about five (one render of every record, which the record page
and the 324 record files are cut from), every page together about ten, and the
sixty-one result overviews about eight. Rendering is deterministic
(`test_overview.test_the_render_is_deterministic` renders afresh to say so), and the
site's test modules only read what is rendered, so they share one render of each, kept
here for the life of the process. Before this, `test_overview`, `test_repo_links`,
`test_case_pages`, `test_frontier_page`, `test_site_documents`, `test_result_overview`,
`test_site_math_faces` and `test_site_text_tokens` each rendered their own, and the
overview was rendered five times in one run of the suite (think-lfnl).

A test module takes these in a module-scoped fixture, never in a test's body, for two
reasons. A fixture's time is setup time, so no check carries a 9 MB render in its own
call time. And a module-scoped fixture is built before a test's own `monkeypatch`
applies, so a test that patches a renderer cannot leave a patched page in the cache; a
test that needs a page rendered under a patch calls the renderer itself.

A worker of a parallel run is a process of its own and renders its own.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from functools import cache
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch

import pytest

from devtools import overview_data, render_overview, result_overview
from devtools.repo_links import REPO

#: What the Pages jobs' partial checkouts leave out, as `pages.yml` writes the patterns
#: (`!/packing/resources/*/`, `!/packing/campaign/*/`, which
#: `test_pages_workflow` holds): every directory directly under either, with all it
#: holds. The files directly under them, `bibliography.yaml` among them, are kept.
PARTIAL_CHECKOUT_OMITS = (REPO / "packing" / "resources", REPO / "packing" / "campaign")


def leave_out_the_archive_and_the_campaign(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make the working tree answer as a Pages job's checkout does: nothing under a
    directory of `PARTIAL_CHECKOUT_OMITS` is a file, is a directory or exists. Git still
    has every path, as it does there. A renderer that reads the content of such a file
    is not caught here; the Pages job itself fails on that."""
    asked = {name: getattr(Path, name) for name in ("is_file", "is_dir", "exists")}

    def omitted(path: Path) -> bool:
        for root in PARTIAL_CHECKOUT_OMITS:
            if not path.is_absolute() or root not in path.parents:
                continue
            below = path.relative_to(root).parts
            if len(below) > 1 or asked["is_dir"](path):
                return True
        return False

    def patched(name: str) -> Callable[..., bool]:
        def answer(self: Path, *args: object, **kwargs: object) -> bool:
            return False if omitted(self) else asked[name](self, *args, **kwargs)

        return answer

    for name in asked:
        monkeypatch.setattr(Path, name, patched(name))


@cache
def page(name: str) -> render_overview.Page:
    """The page `render_overview.PAGES` builds as `name`, rendered once."""
    return render_overview.PAGES[name]()


def html(name: str) -> str:
    """That page's text."""
    return page(name).html


class _FrontierMath(HTMLParser):
    """Count the complete canonical page before any browser or font mutation."""

    VOID = frozenset(
        (
            "area",
            "base",
            "br",
            "col",
            "embed",
            "hr",
            "img",
            "input",
            "link",
            "meta",
            "param",
            "source",
            "track",
            "wbr",
        )
    )
    MATH_CLASSES = frozenset(("kpress-math", "tex", "tex-d"))
    TOKENS = frozenset(("mi", "mn", "mo", "mtext", "ms"))

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, dict[str, str | None]]] = []
        self.rows: list[str] = []
        self.total = 0
        self.native = 0
        self.native_depth: int | None = None
        self.roots = 0
        self.token = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        classes = set((values.get("class") or "").split())
        if classes & self.MATH_CLASSES and not any(
            set((item.get("class") or "").split()) & self.MATH_CLASSES for _, item in self.stack
        ):
            self.total += 1
        in_frontier = any(item.get("id") == "frontier-table" for _, item in self.stack)
        if tag == "tr" and in_frontier and any(name == "tbody" for name, _ in self.stack):
            self.rows.append(values.get("id") or "")
        if values.get("data-site-native-math") == "frontier":
            assert self.native_depth is None
            assert in_frontier
            assert {"tbody", "td"} <= {name for name, _ in self.stack}
            assert any(
                name == "tr" and item.get("id") == self.rows[-1] for name, item in self.stack
            )
            assert classes & self.MATH_CLASSES
            self.native_depth = len(self.stack) + 1
            self.roots, self.token = 0, False
        if self.native_depth is not None:
            assert tag != "merror"
            if tag == "math":
                assert values.get("xmlns") == "http://www.w3.org/1998/Math/MathML"
                self.roots += 1
                assert self.roots == 1
        if tag not in self.VOID:
            self.stack.append((tag, values))

    def handle_endtag(self, tag: str) -> None:
        assert self.stack
        assert self.stack[-1][0] == tag
        if len(self.stack) == self.native_depth:
            assert self.roots == 1
            assert self.token
            self.native += 1
            self.native_depth = None
        self.stack.pop()

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_data(self, data: str) -> None:
        if (
            self.native_depth is not None
            and data.strip()
            and any(tag == "math" for tag, _ in self.stack)
            and self.stack[-1][0] in self.TOKENS
        ):
            self.token = True

    def counts(self) -> tuple[int, int]:
        assert not self.stack
        assert self.native_depth is None
        assert self.rows == [f"n-{n}" for n in range(1, 325)]
        assert self.native > 0
        assert self.total - self.native == 9
        return self.native, self.total


def count_frontier_math(source: str) -> tuple[int, int]:
    """Require the complete row roster and structurally readable native formulas."""
    parser = _FrontierMath()
    parser.feed(source)
    parser.close()
    return parser.counts()


@cache
def frontier_math_counts() -> tuple[int, int]:
    """Native and total formulas from every canonical frontier row and its prose."""
    return count_frontier_math(html("frontier.html"))


def served(name: str) -> str:
    """That page as a reader's browser assembles it: with every shared asset it links
    put back in it (`site_assets.SiteAssets.inlined`), for a test of what the page
    carries rather than of how it names it."""
    from devtools import site_assets  # noqa: PLC0415

    return site_assets.shared().assets.inlined(html(name))


def write(root: Path, *names: str) -> dict[str, Path]:
    """Write the pages `names` under `root` as the site serves them, with every shared
    asset they name under `root`'s `assets/` and every declared support file. Return each
    page's path, with its browser dependencies present. Pages written into
    the same `root` by several calls keep each other's assets."""
    from devtools import site_assets  # noqa: PLC0415

    written = {}
    for name in names:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html(name), encoding="utf-8")
        written[name] = path
    support = render_overview.support_files()
    for output in render_overview.support_file_paths():
        target = root / output
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(support[output])
    files = site_assets.shared().assets.referenced(html(name) for name in names)
    for output, data in files.items():
        target = root / site_assets.ASSETS_DIR / output
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return written


def pages() -> dict[str, str]:
    """Every page `render_overview.PAGES` builds, by name."""
    return {name: html(name) for name in render_overview.PAGES}


@cache
def overview() -> overview_data.Overview:
    """The record as the site reads it, loaded once."""
    return overview_data.load()


@cache
def result_bodies() -> dict[str, str]:
    """Every registered result's overview, by id, in the register's order."""
    loaded = overview()
    return {
        result.id: result_overview.result_popover_html(result, loaded)
        for result in loaded.results
    }


@cache
def case_records() -> dict[str, str]:
    """Every case's record file (`render_overview.case_records`), by served name."""
    return {record.name: record.html for record in render_overview.case_records()}


@cache
def result_pages() -> tuple[render_overview.Page, ...]:
    """Every complete result document, immutable and rendered once per process."""
    return tuple(render_overview.result_fragments())


@cache
def forwarders() -> tuple[render_overview.Page, ...]:
    """The actual forwarders, including the validated case-routing inventory."""
    return tuple(render_overview.forwarder_pages())


@pytest.fixture(scope="module")
def prepared_forwarders() -> Iterator[tuple[render_overview.Page, ...]]:
    """Prepare immutable renderer input before per-test patches, then give each
    checker invocation a fresh list. Its parsing and every mutated-page check still
    run; repeated fake deploys need not revalidate 324 unchanged case records."""
    rendered = forwarders()
    with patch.object(render_overview, "forwarder_pages", side_effect=lambda: list(rendered)):
        yield rendered
