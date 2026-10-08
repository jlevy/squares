"""The reader documents as site pages, with every link made to work off GitHub.

The tutorial is one of the papers the navigation's Papers entry leads to (`papers.html`)
and marks current; the README, `epistemics.md`, the synopsis and the two reference
documents are pages the navigation does not list, reached from the overview's cards,
whose popovers frame them. Each is written to be read on GitHub, where a relative link
to `conventions.md` or to a directory under `packing/` opens that file. Served as pages,
the same links would point at pages that do not exist, so each one is rewritten in the
rendered HTML, never in the Markdown, where a pattern would also match `](` inside a
code span:

- a link to another rendered document becomes its page, anchor kept;
- a link to a record the site shows on a page of its own becomes that page
  (`record_aliases`): the results register is the results table, a result's row there
  when the link's text is its id; the status table is the frontier atlas; a case file
  is that case's record. A link whose text names the register's file, as
  `` `RESULTS.md` `` does, still opens the file (`_record_links`);
- any other relative link becomes the file's link on `main`, `blob/` for a file and
  `tree/` for a directory, and an image becomes its raw file on `main`, all through
  `repo_links`, the one place the site's repository links are made.

Three generated views of the record were pages here until 2026-10-01 and are not now:
`RESULTS.md`, `STATUS.md` and `defects.md` (think-bk2e, and the review of that date
under `docs/project/reviews/`). Their old addresses are forwarders
(`render_overview.MOVED_PAGES`).

A relative link is resolved against the document's own directory, as GitHub resolves
it. Every rewritten repository target is checked against the tree being rendered, which
is the tree `main` holds when the site deploys, read once from git, and every anchor
into a page against the ids the target page actually has. A target that does not
resolve fails the render with the whole list, so a broken link is found when the page is
built rather than by a reader.

One document is also read in part. README's opening is marked as one block, and it is
prose of the overview: the block between the `project-intro` markers is the overview's
first section. The overview's template holds a placeholder where it would be,
`overview_intro` fills it, and `rewrite_overview_blocks` makes the block's links work on
the site, as a document's are made to. The problem is introduced in one text, on GitHub
and on the site. README's next two paragraphs, what the project covers and its newest
major result, were a second shared block, `recent-progress`, that opened the overview's
Recent Results until 2026-10-02; the overview says that in one paragraph of its own
now, and README keeps its fuller account, so the two are not one text (think-ekw5).
"""

from __future__ import annotations

import html
import posixpath
import re
from dataclasses import dataclass, field
from functools import cache
from itertools import pairwise
from pathlib import Path
from urllib.parse import quote, unquote

from devtools import render_overview, repo_links
from devtools.render_overview import REPO, Page
from devtools.repo_links import RepositoryTree, repo_url, repository_tree

TUTORIAL = REPO / repo_links.TUTORIAL
README = REPO / repo_links.README


@dataclass(frozen=True)
class SharedBlock:
    """A block of README that is also prose of the overview.

    It is hand-written in README, between `begin` and `end`, and read from there; nothing
    writes it. In the overview, as Markdown and then as rendered HTML, the same block
    sits between `opened` and `closed`: kpress passes a comment through, so the two mark
    the run whose links `rewrite_overview_blocks` rewrites, and nothing else on the
    overview is touched.
    """

    name: str

    @property
    def begin(self) -> str:
        return f"<!-- BEGIN SHARED: {self.name} (devtools.site_documents) -->"

    @property
    def end(self) -> str:
        return f"<!-- END SHARED: {self.name} -->"

    @property
    def opened(self) -> str:
        return f"<!-- README {self.name} -->"

    @property
    def closed(self) -> str:
        return f"<!-- /README {self.name} -->"


#: README's two opening paragraphs, the problem and its bounds: the overview's first
#: section.
INTRO = SharedBlock("project-intro")
#: README's shared blocks, in the order README writes them: one since 2026-10-02, when
#: the `recent-progress` block stopped being shared (the module's docstring).
SHARED_BLOCKS = (INTRO,)
INTRO_BEGIN, INTRO_END = INTRO.begin, INTRO.end
OVERVIEW_INTRO_OPEN, OVERVIEW_INTRO_CLOSE = INTRO.opened, INTRO.closed
#: The framing the owner refused on 2026-09-30: eleven squares is a central case of the
#: problem, and never the one the project is about.
THE_CENTRAL_CASE = re.compile(
    "\\b(?:the|its|project[\u2019']s)\\s+central\\s+(?:open\\s+)?case\\b", re.IGNORECASE
)


@dataclass(frozen=True)
class SiteDocument:
    """One reader document served as a page."""

    source: Path
    name: str
    current: str
    title: str
    """The page's own name, as its tab and its link preview give it; the site's name
    follows it in `<title>` (`render_overview.page_title`)."""
    description: str
    kind: render_overview.PageKind = "website"
    """`article` for a paper (`render_overview.PageMeta.kind`)."""


def _document(path: str, name: str, title: str, description: str) -> SiteDocument:
    """A repository document served as a page that the navigation does not list: it is
    reached from its card's popover, which frames it, and from links in the others."""
    return SiteDocument(REPO / path, name, "github", title, description)


DOCUMENTS: tuple[SiteDocument, ...] = (
    # A paper, so the bar's Papers entry is current on it, as on the explainer.
    SiteDocument(
        TUTORIAL,
        "tutorial.html",
        "papers",
        "Tutorial",
        "A guided walk through square packing: the problem, the bounds and how each "
        "result here is checked.",
        "article",
    ),
    # The overview's document cards, in their order (`render_overview.DOCUMENT_PAGES`).
    _document(
        repo_links.README,
        "readme.html",
        # The file's name: the page's own would repeat the project's, which follows it.
        "README",
        "The square packing project: current results, operating principles, "
        "reproducible evidence, and guides to its papers and research record.",
    ),
    _document(
        repo_links.EPISTEMICS,
        "epistemics.html",
        "Epistemics",
        "How square packing claims are verified and independently confirmed, "
        "with the evidence and significance levels used in the result register.",
    ),
    _document(
        repo_links.SYNOPSIS,
        "synopsis.html",
        "Synopsis",
        "The square packing research record, organized in chapters: methods, "
        "theoretical results, experiments, defects, and current research priorities.",
    ),
    _document(
        repo_links.CONVENTIONS,
        "conventions.html",
        "Conventions",
        "Formats and naming for square packing records, witnesses, "
        "certificates, hypotheses, sessions, results, and their evidence contracts.",
    ),
    _document(
        repo_links.DEVELOPMENT,
        "development.html",
        "Development",
        "Build and validate the square packing tools and published site: "
        "pinned runtimes, test tiers, browser checks, and research admission gates.",
    ),
)

#: The rendered documents by repository path, which is how the Markdown links them.
_BY_SOURCE = {doc.source.relative_to(REPO).as_posix(): doc for doc in DOCUMENTS}

#: The two generated views of the record that the site shows on a page of its own, built
#: from the same record: the results register is the results table, and the status table
#: is the frontier atlas. Neither file is served as a page, so a link to one leads to the
#: page that shows what it holds.
RECORD_PAGES: dict[str, str] = {
    repo_links.RESULTS: render_overview.RESULTS_PAGE,
    repo_links.STATUS: "frontier.html",
}
#: Where every case's record is served, one address per case (`render_case_pages`).
CASES_DIR = "cases"
_CASE_FILE = re.compile(r"packing/frontier/n-(\d{3})\.md")
#: A link as kpress writes one, with its text plain or one code span.
_TEXT_LINK = re.compile(r'<a href="([^"]*)">(<code>)?([^<]*)(</code>)?</a>')
_RESULT_ID = re.compile(r"T-\d{3}")

_ARTICLE = re.compile(r"<article\b.*?</article>", re.DOTALL)
_TAG = re.compile(r"<(?!/)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>")
_LINK_ATTR = re.compile(r'\s(href|src)="([^"]*)"')
_ID_ATTR = re.compile(r'\s(?:id|name)="([^"]*)"')
_EXTERNAL = re.compile(r"^(?:[a-zA-Z][a-zA-Z0-9+.-]*:|//)")
# A document's own contents list, written for GitHub, which draws no contents rail: a
# `## Contents` heading over nothing but a list of links to the document's headings.
_MANUAL_CONTENTS = re.compile(
    r"^## Contents\n\n(?:[ \t]*(?:\d+\.|[-*])[ \t]+\[[^\]]+\]\(#[^)]+\)[ \t]*\n)+\n?",
    re.MULTILINE,
)


def without_manual_contents(markdown: str) -> str:
    """The document without its hand-written contents list. On the site the contents
    rail lists the headings, and the list would repeat as the rail's first entry."""
    return _MANUAL_CONTENTS.sub("", markdown, count=1)


@dataclass
class LinkReport:
    """What the rewrite found: targets missing from the tree and anchors with no id."""

    missing: list[str] = field(default_factory=list)
    #: (target page, anchor, as written): checked once every page is rendered.
    anchors: list[tuple[str, str, str]] = field(default_factory=list)


@dataclass(frozen=True)
class LinkContext:
    """What a rewrite needs: the page's own name, the tree its links must exist in, and
    where the document sits."""

    page: str
    tree: RepositoryTree
    #: The document's directory in the repository, `""` at the root: what its relative
    #: links are relative to.
    base: str = ""
    #: Served pages a link may already name, such as `frontier.html#n-11` in a page
    #: built from the record rather than from a document: kept as written.
    served: frozenset[str] = frozenset()
    #: Repository files the site shows on a page, and where (`record_aliases`): the
    #: results register is the results table, and a case file is that case's record,
    #: on the same page when it is linked from a case record.
    aliases: dict[str, str] = field(default_factory=dict)


def _repository_link(path: str, fragment: str, *, tag: str, context: LinkContext) -> str | None:
    """A file's or directory's link on `main`; `None` if the tree has neither."""
    if path in context.tree.files:
        if tag == "img":
            return repo_url(path, kind="raw")
        return repo_url(path, fragment, kind="blob")
    if path in context.tree.directories:
        return repo_url(path, fragment, kind="tree")
    for root, (url, commit) in context.tree.submodules.items():
        if path.startswith(root + "/"):
            # Inside a submodule: its own repository at the commit this one pins, since a
            # vendored file is only known to exist at the pin. That is another
            # repository's permalink, not one of this repository's.
            inner = quote(path.removeprefix(root + "/"), safe="/")
            return f"{url}/blob/{commit}/{inner}{fragment}"
    return None


def rewrite_link(url: str, *, tag: str, context: LinkContext, report: LinkReport) -> str:
    """The served URL for one `href` or `src` found in a rendered reader document.

    A relative link is relative to the document's own directory, as GitHub reads it.
    """
    target, _, anchor = url.partition("#")
    if not url or url.startswith("#") or _EXTERNAL.match(url) or target in context.served:
        return url
    target, _, query = target.partition("?")
    relative = unquote(target) if target else "."
    path = posixpath.normpath(posixpath.join(context.base, relative))
    path = "" if path == "." else path
    fragment = f"#{anchor}" if anchor else ""
    document = _BY_SOURCE.get(path)
    if path in context.aliases:
        link = context.aliases[path]
    elif document is not None:
        if anchor:
            report.anchors.append((document.name, unquote(anchor), url))
        if document.name == context.page:
            return fragment or document.name
        link = document.name + fragment
    else:
        link = (
            None
            if path.startswith("../") or path == ".."
            # A query is GitHub's (`?plain=1` before a `#L12` line anchor), so it is kept.
            else _repository_link(
                path, (f"?{query}" if query else "") + fragment, tag=tag, context=context
            )
        )
    if link is None:
        report.missing.append(url)
        return url
    return link


def record_aliases(tree: RepositoryTree) -> dict[str, str]:
    """Where a link to a record the site has a page for leads, by the record's path: the
    results register and the status table (`RECORD_PAGES`), and each case file in `tree`
    to that case's record."""
    cases = {
        path: f"{CASES_DIR}/{int(match.group(1))}.html"
        for path in tree.files
        if (match := _CASE_FILE.fullmatch(path))
    }
    return {**RECORD_PAGES, **cases}


@cache
def _result_ids() -> frozenset[str]:
    """Every registered result's id, which is its row's on the results page."""
    from devtools.overview_data import RESULTS  # noqa: PLC0415
    from sqpack.yamlio import safe_load  # noqa: PLC0415

    register = safe_load(RESULTS.read_text(encoding="utf-8"))
    return frozenset(record["id"] for record in register["results"])


def _record_links(markup: str, *, context: LinkContext, report: LinkReport) -> str:
    """The links to the results register and the status table that the link's own text
    decides, before `rewrite_link` sends the rest to the page for each (`RECORD_PAGES`).

    A link to the results register whose text is a result's id, as README writes
    `[T-060](packing/frontier/RESULTS.md)`, goes to that result's row in the results
    table; an id the register does not hold is reported. A link whose text is a code
    span naming the file, as `epistemics.md` writes `` [`RESULTS.md`](…) `` where it says
    the view is generated, opens the file on `main`: its sentence is about the file.
    """

    def link(match: re.Match[str]) -> str:
        url = html.unescape(match.group(1))
        if not url or url.startswith("#") or _EXTERNAL.match(url):
            return match.group(0)
        target = url.partition("#")[0].partition("?")[0]
        path = posixpath.normpath(posixpath.join(context.base, unquote(target)))
        if path not in RECORD_PAGES:
            return match.group(0)
        opened, text, closed = match.group(2) or "", match.group(3), match.group(4) or ""
        plain = html.unescape(text)
        if path == repo_links.RESULTS and _RESULT_ID.fullmatch(plain):
            if plain not in _result_ids():
                report.missing.append(f"{url} (no result {plain} in the register)")
                return match.group(0)
            href = f"{render_overview.RESULTS_PAGE}#{plain.lower()}"
        elif opened and plain.endswith(posixpath.basename(path)):
            href = repo_url(path, kind="blob")
        else:
            return match.group(0)
        return f'<a href="{html.escape(href, quote=True)}">{opened}{text}{closed}</a>'

    return _TEXT_LINK.sub(link, markup)


def rewrite_links(markup: str, *, context: LinkContext, report: LinkReport) -> str:
    """Rewrite every `href` and `src` in a run of rendered HTML."""
    markup = _record_links(markup, context=context, report=report)

    def attribute(match: re.Match[str], tag: str) -> str:
        url = html.unescape(match.group(2))
        new = rewrite_link(url, tag=tag, context=context, report=report)
        if new == url:
            return match.group(0)
        return f' {match.group(1)}="{html.escape(new, quote=True)}"'

    def element(match: re.Match[str]) -> str:
        tag = match.group(1).lower()
        return _LINK_ATTR.sub(lambda m: attribute(m, tag), match.group(0))

    return _TAG.sub(element, markup)


def rewrite_article(page: str, *, context: LinkContext, report: LinkReport) -> str:
    """Rewrite the links inside the page's article, leaving the nav and scripts alone."""
    article = _ARTICLE.search(page)
    if article is None:
        raise SystemExit(f"{context.page}: the rendered page has no <article>")
    body = rewrite_links(article.group(0), context=context, report=report)
    return page[: article.start()] + body + page[article.end() :]


def element_ids(page: str) -> frozenset[str]:
    """Every `id` and `name` in the page's article: the anchors a link can land on."""
    article = _ARTICLE.search(page)
    return frozenset(
        html.unescape(m) for m in _ID_ATTR.findall(article.group(0) if article else "")
    )


def render_document(
    document: SiteDocument, *, tree: RepositoryTree, report: LinkReport
) -> Page:
    """One reader document as a kpress page with its links rewritten."""
    base = posixpath.dirname(document.source.relative_to(REPO).as_posix())
    context = LinkContext(
        document.name,
        tree,
        base,
        served=frozenset(render_overview.SITE_PAGES),
        aliases=record_aliases(tree),
    )
    return render_overview.kpress_page(
        without_manual_contents(document.source.read_text(encoding="utf-8")),
        name=document.name,
        current=document.current,
        title=document.title,
        description=document.description,
        kind=document.kind,
        structured_data=(
            render_overview.breadcrumb_data(
                ("Home", "index.html"), (document.title, document.name)
            ),
        ),
        # A long report gets the contents rail and a short one does not, by kpress's
        # own length rule, so every report keeps one layout either way.
        toc=False if document.name == "synopsis.html" else "auto",
        trust_mode="sanitized",
        strict_anchors=True,
        rewrite_body=lambda page: rewrite_article(page, context=context, report=report),
    )


def unresolved(pages: dict[str, Page], report: LinkReport) -> list[str]:
    """Every link the render could not resolve, missing files and anchors together."""
    ids = {name: element_ids(page.html) for name, page in pages.items()}
    problems = [f"no such path in the tree: {url}" for url in report.missing]
    problems += [
        f"no heading #{anchor} in {name}: {url}"
        for name, anchor, url in report.anchors
        if anchor not in ids[name]
    ]
    return sorted(set(problems))


def shared_block(readme: str, block: SharedBlock) -> str:
    """One shared block of README: the Markdown between its two markers.

    Raises `ValueError` unless each marker appears once, in order, around prose alone. A
    heading or a comment inside the block would land in the middle of a section of the
    overview, which is also why one block may not hold another's marker; a link to the
    site would point the overview at itself; and no case is called the central one.
    """
    name = block.name
    if readme.count(block.begin) != 1 or readme.count(block.end) != 1:
        raise ValueError(f"the {name} markers must each appear exactly once")
    begin, end = readme.index(block.begin), readme.index(block.end)
    if end < begin:
        raise ValueError(f"the {name} block ends before it begins")
    text = readme[begin + len(block.begin) : end].strip()
    if not text:
        raise ValueError(f"the {name} block is empty")
    if "<!--" in text or re.search(r"^#", text, re.MULTILINE):
        raise ValueError(f"the {name} block holds a heading or a comment")
    if render_overview.SITE_URL in text:
        raise ValueError(f"the {name} block links the site it is rendered on")
    if THE_CENTRAL_CASE.search(text):
        raise ValueError(f"the {name} block calls a case the central one")
    return text


def shared_blocks(readme: str) -> dict[str, str]:
    """Every shared block of README by name, each as `shared_block` reads it.

    Raises `ValueError` for a block `shared_block` refuses, and unless the blocks follow
    one another in README in the order `SHARED_BLOCKS` lists them, with nothing but
    blank lines between, so that README reads them as one introduction; with one block
    the order holds of itself.
    """
    blocks = {block.name: shared_block(readme, block) for block in SHARED_BLOCKS}
    for first, second in pairwise(SHARED_BLOCKS):
        between = readme[readme.index(first.end) + len(first.end) : readme.index(second.begin)]
        if readme.index(second.begin) < readme.index(first.end) or between.strip():
            raise ValueError(
                f"the {second.name} block must follow the {first.name} block directly"
            )
    return blocks


def intro_block(readme: str) -> str:
    """README's two opening paragraphs, the Markdown between its `project-intro` markers."""
    return shared_block(readme, INTRO)


def _overview_block(block: SharedBlock) -> str:
    """One shared block as the overview's Markdown, between the two comments
    `rewrite_overview_blocks` finds it by once the page is rendered."""
    try:
        text = shared_blocks(README.read_text(encoding="utf-8"))[block.name]
    except ValueError as error:
        raise SystemExit(f"{repo_links.README}: {error}") from None
    return f"{block.opened}\n\n{text}\n\n{block.closed}"


def overview_intro() -> str:
    """README's two opening paragraphs as the Markdown of the overview's first section."""
    return _overview_block(INTRO)


def rewrite_overview_blocks(page: str) -> str:
    """The rendered overview with the links of README's shared blocks made to work there.

    The block is written for GitHub, so its links are repository paths. Each becomes
    the site's own page for what it names where the site has one, by the rule every
    document's page follows (`record_aliases`, `_record_links`): a result's row in the
    results table, the results table for the register, the frontier atlas for the status
    table, a case's record for its case file, and a reader document's page. Any other
    path becomes its link on `main`, checked against the tree, as on a document's page.
    Nothing outside a shared block is rewritten.
    """
    for block in SHARED_BLOCKS:
        if page.count(block.opened) != 1 or page.count(block.closed) != 1:
            raise SystemExit(
                f"index.html: README's {block.name} block is not marked in the page"
            )
    tree = repository_tree()
    context = LinkContext(
        "index.html",
        tree,
        served=frozenset(render_overview.SITE_PAGES),
        aliases=record_aliases(tree),
    )
    report = LinkReport()
    for block in SHARED_BLOCKS:
        head, _, rest = page.partition(block.opened)
        body, _, tail = rest.partition(block.closed)
        body = rewrite_links(body, context=context, report=report)
        page = head + block.opened + body + block.closed + tail
    # An anchor into a reader document is checked against that document's page, which
    # is rendered only when a block has such a link.
    problems = unresolved(site_documents() if report.anchors else {}, report)
    if problems:
        listing = "\n  ".join(problems)
        raise SystemExit(
            f"{len(problems)} unresolved links in README's introduction:\n  {listing}"
        )
    return page


@cache
def site_documents() -> dict[str, Page]:
    """Every reader document, rendered once and checked together."""
    tree = repository_tree()
    report = LinkReport()
    pages = {doc.name: render_document(doc, tree=tree, report=report) for doc in DOCUMENTS}
    synopsis, chapters = synopsis_parts(pages["synopsis.html"])
    pages["synopsis.html"] = synopsis
    pages.update({page.name: page for page in chapters})
    problems = unresolved(pages, report)
    if problems:
        listing = "\n  ".join(problems)
        raise SystemExit(
            f"{len(problems)} unresolved links in the reader documents:\n  {listing}"
        )
    return pages


def chapter_names() -> tuple[str, ...]:
    """Stable chapter declarations, derived from the synopsis's section names."""
    text = (REPO / repo_links.SYNOPSIS).read_text(encoding="utf-8")
    headings = re.findall(r"^## (.+)$", text, re.MULTILINE)
    return tuple(
        "synopsis/" + re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-") + ".html"
        for heading in headings
    )


def synopsis_parts(full: Page) -> tuple[Page, list[Page]]:
    """Static thematic chapters and exact visible landings for all published fragments.

    Splitting rendered HTML preserves kpress's heading and footnote identifiers. Each
    historic anchor on synopsis.html names its chapter link, so it works without script.
    """
    article = _ARTICLE.search(full.html)
    if article is None:
        raise SystemExit("synopsis.html has no article")
    opened = re.search(r'<div class="kpress-prose[^"]*">', article[0])
    if opened is None:
        raise SystemExit("synopsis.html has no prose column")
    prose = article[0][opened.end() :].removesuffix("</div></div></article>")
    headings = list(re.finditer(r"<h2\b[^>]*>.*?</h2>", prose, re.DOTALL))
    names = chapter_names()
    if len(names) != len(headings):
        raise SystemExit("synopsis chapter declarations differ from rendered sections")
    chapters = []
    links = []
    introduction = prose[: headings[0].start()]
    used: set[str] = set()
    for index, (name, heading) in enumerate(zip(names, headings, strict=True)):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(prose)
        content = prose[heading.start() : end]
        title = html.unescape(re.sub(r"<[^>]+>", "", heading[0])).strip()
        ids = element_ids("<article>" + content + "</article>")
        links.append(f'<li><a href="{name}">{html.escape(title)}</a></li>')
        labels = {
            match[1]: html.unescape(re.sub(r"<[^>]+>", "", match[2]))
            for match in re.finditer(
                r'<h[1-6]\b[^>]*id="([^"]+)"[^>]*>(.*?)</h[1-6]>', content, re.DOTALL
            )
        }
        for anchor in sorted(ids - used):
            escaped = html.escape(anchor, quote=True)
            label = html.escape(labels.get(anchor, anchor))
            links.append(
                f'<li id="{escaped}"><a href="{name}#{escaped}">'
                f"{html.escape(title)}: {label}</a></li>"
            )
        used.update(ids)
        previous = (
            f'<a rel="prev" href="{names[index - 1]}">Previous chapter</a>' if index else ""
        )
        following = (
            f'<a rel="next" href="{names[index + 1]}">Next chapter</a>'
            if index + 1 < len(names)
            else ""
        )
        nav = (
            f'<nav aria-label="Synopsis chapters">{previous} '
            f'<a href="synopsis.html">All chapters</a> {following}</nav>'
        )
        # Footnotes keep their body in the last source section. A cross-chapter target
        # is resolved after every chapter's anchor map has been collected below.
        body = f"<article><h1>{html.escape(title)}</h1>{nav}{content}{nav}</article>"
        meta = render_overview.PageMeta(
            f"Synopsis: {title}",
            (
                f"Square packing research synopsis: {title.lower()}. "
                "Methods, evidence and the recorded state of the research program."
            )[:160],
            name,
            structured_data=(
                render_overview.breadcrumb_data(
                    ("Home", "index.html"), ("Synopsis", "synopsis.html"), (title, name)
                ),
            ),
        )
        chapters.append(render_overview.static_content_page(body, meta=meta, current="github"))
    targets = {anchor: page.name for page in chapters for anchor in element_ids(page.html)}
    moved = []
    for page in chapters:

        def target(match: re.Match[str], name: str = page.name) -> str:
            anchor = html.unescape(match[1])
            destination = targets.get(anchor)
            if destination is None or destination == name:
                return match[0]
            path = posixpath.relpath(destination, posixpath.dirname(name))
            return f'href="{path}#{html.escape(anchor, quote=True)}"'

        moved.append(Page(page.name, re.sub(r'href="#([^"]+)"', target, page.html)))
    landing = (
        introduction + "<p>The research synopsis is organized in chapters. "
        "A link to an earlier section lands on its chapter below; open the "
        "chapter to read the section.</p><ol>" + "".join(links) + "</ol>"
    )
    meta = next(doc for doc in DOCUMENTS if doc.name == "synopsis.html")
    index = render_overview.static_content_page(
        "<article>" + landing + "</article>",
        meta=render_overview.PageMeta(
            meta.title,
            meta.description,
            meta.name,
            structured_data=(
                render_overview.breadcrumb_data(
                    ("Home", "index.html"), ("Synopsis", "synopsis.html")
                ),
            ),
        ),
        current="github",
    )
    return index, moved


def document_files() -> dict[str, bytes]:
    """Reader documents require no model files; chapter HTML holds complete content."""
    return {}


def chapter_pages() -> list[Page]:
    """The declared synopsis chapters as complete pages."""
    pages = site_documents()
    return [pages[name] for name in chapter_names()]


def tutorial_page() -> Page:
    """`TUTORIAL.md` as `tutorial.html`."""
    return site_documents()["tutorial.html"]


def document_page(name: str) -> Page:
    """One repository document as its page, by served name."""
    return site_documents()[name]
