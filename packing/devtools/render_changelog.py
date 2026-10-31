"""Validate retained project history and render its GitHub and News reader views.

Rendering reads committed inputs only. GitHub acquisition belongs to
`devtools.import_changelog`, and publication claims require retained evidence.
"""

from __future__ import annotations

import argparse
import bisect
import html
import re
import subprocess
import sys
from collections.abc import Callable, Mapping, Sequence
from datetime import date, datetime
from functools import cache
from html.parser import HTMLParser
from ipaddress import IPv6Address
from pathlib import Path, PurePosixPath
from typing import Any, Literal, NamedTuple, TypedDict, override
from urllib.parse import SplitResult, quote, unquote, urlsplit

import yaml
from jsonschema_rs import Draft202012Validator
from kpress.format.markdown import parse_markdown
from kpress.format.model import DocumentTree
from markdown_it import MarkdownIt
from markdown_it.common.normalize_url import normalizeLink
from markdown_it.rules_inline import StateInline
from markdown_it.rules_inline.link import link as inline_link
from markdown_it.token import Token
from mdit_py_plugins.attrs import attrs_block_plugin, attrs_plugin
from mdit_py_plugins.dollarmath import dollarmath_plugin
from strif import atomic_output_file

from devtools.github_references import (
    cited_issues,
    issue_opened,
    issue_url,
    issues_reporting,
)
from devtools.migrate_math import classify
from devtools.overview_data import MATH, breakable_quotients, prose_tex
from devtools.repo_links import path_kind, repo_url
from devtools.site_topics import NEWS_TOPICS, topic_chip
from sqpack import release
from sqpack.yamlio import BaseLoader, load_yaml

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
SRC = ROOT / "site-changelog.yaml"
SCHEMA = ROOT / "site-changelog.schema.yaml"
OUT = REPO / "CHANGELOG.md"
Destination = Literal["github", "site"]
Document = dict[str, Any]


class Significance(TypedDict):
    """An editorial importance judgment; it does not change result assurance."""

    score: int
    rationale: str


#: The rubric a News post is scored by: the S labels' table in `result-import.md`,
#: "Label the PR and Prepare News", whose `Short` column is each label's description on
#: GitHub. A News meter and the archive's S buttons say what a level means in it; a
#: result's meter keeps the result ladder in `epistemics.md`.
NEWS_RUBRIC = ROOT / "campaign" / "result-import.md"
NEWS_RUBRIC_SECTION = "### Label the PR and Prepare News"
_NEWS_RUBRIC_ROW = re.compile(r"^\| `S(\d)` \| [^|]+? \| ([^|]+?) \| [^|]+? \|$", re.MULTILINE)
#: The check a selected topic shows: the theme menu's mark for a chosen item
#: (`templates/site-nav.html`), hidden from assistive technology, which reads
#: `aria-pressed`.
NEWS_CHECK = (
    '<svg class="site-news-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
    'focusable="false"><path d="M20 6 9 17l-5-5"/></svg>'
)
#: The lowest significance News announces (`news_entries`); lower scores stay in the
#: GitHub history.
NEWS_FLOOR = 3
#: The levels the News archive opens on, and what an address without `news-s` means
#: there (`news-filters.js`).
NEWS_LEVELS = (4, 5)
#: Where the retained history is served: the page that owns the `changelog` bookmark and
#: an anchor for every entry, whatever its significance
#: (`render_overview.changelog_page`). News shows the S3+ stories and sends a reader here
#: for the rest (the owner, 2026-10-26); before that the section lived on News itself and
#: the only full view was `CHANGELOG.md` on GitHub.
CHANGELOG_PAGE = "changelog.html"
#: Where the stories are served. A change the Changelog lists and News tells links to
#: the story rather than repeating it (`changelog_entry_line`).
NEWS_PAGE = "news.html"


def news_rubric_meanings(text: str) -> dict[int, str]:
    """Each level's short meaning in the text of the News rubric's document: all the site
    reads of it. A document without the section or without a `Short` meaning for S1 to S5
    raises `ValueError`."""
    if NEWS_RUBRIC_SECTION not in text:
        raise ValueError(f"{NEWS_RUBRIC.name} has no {NEWS_RUBRIC_SECTION!r} section")
    section = text.split(NEWS_RUBRIC_SECTION, 1)[1].split("\n#", 1)[0]
    meanings = {int(level): short.strip() for level, short in _NEWS_RUBRIC_ROW.findall(section)}
    if sorted(meanings) != list(range(1, 6)):
        raise ValueError(f"{NEWS_RUBRIC.name}'s News rubric does not define S1 to S5")
    return meanings


@cache
def news_significance_meanings() -> dict[int, str]:
    """Each News significance level's short meaning, read from the rubric's table so a
    tooltip cannot drift from the scale that scored the post."""
    try:
        return news_rubric_meanings(NEWS_RUBRIC.read_text(encoding="utf-8"))
    except ValueError as error:
        raise SystemExit(str(error)) from error


def news_significance_tooltip(score: int) -> str:
    """What a News post's significance level means, without the post's own rationale,
    which its source record keeps."""
    return f"{news_significance_meanings()[score]}."


def entry_significance(entry: Mapping[str, Any]) -> Significance:
    """The typed significance view of a structurally validated entry.

    Any mapping, since it only reads: a `Document` satisfies it, and so does an entry a
    publication audit holds as a read-only mapping.
    """
    return {
        "score": entry["significance"]["score"],
        "rationale": entry["significance"]["rationale"],
    }


BANNER = (
    "<!-- GENERATED by devtools.render_changelog from packing/site-changelog.yaml. "
    "Do not edit by hand. -->"
)
FOOTER = (
    "<!-- This document follows common-doc-guidelines.md.\n"
    "See github.com/jlevy/practical-prose and review guidelines before editing.\n-->"
)


@cache
def _validator() -> Draft202012Validator:
    return Draft202012Validator(load_yaml(SCHEMA.read_text(encoding="utf-8")))


def _markdown() -> MarkdownIt:
    parser = MarkdownIt(
        "commonmark", {"html": True, "store_labels": True, "inline_definitions": True}
    )

    # The default parser leaves unsafe links as plain text. Parse them so authoring
    # fails visibly instead of silently changing how a purported link is displayed.
    def accept_link(url: str) -> bool:
        return bool(url)

    parser.validateLink = accept_link
    parser.use(dollarmath_plugin, allow_space=False, allow_digits=False)
    parser.use(attrs_block_plugin)
    parser.use(attrs_plugin, spans=True)
    return parser


def _walk(tokens: Sequence[Token]) -> list[Token]:
    return [child for token in tokens for child in [token, *_walk(token.children or [])]]


def _target(target: str, *, destination: Destination) -> str:
    decoded = target
    while (expanded := html.unescape(unquote(decoded))) != decoded:
        decoded = expanded
    if any(ord(character) < 32 or ord(character) == 127 for character in decoded) or any(
        character in decoded for character in "\\<>"
    ):
        raise ValueError(f"unsafe link target: {target}")
    parts = urlsplit(decoded)
    if parts.scheme:
        original = urlsplit(target)
        if (
            parts.scheme != "https"
            or original.scheme != "https"
            or not parts.hostname
            or parts.username is not None
            or parts.password is not None
            or not original.hostname
            or original.username is not None
            or original.password is not None
        ):
            raise ValueError(f"unsafe link scheme or authority: {target}")
        _https_authority(original, target)
        _https_authority(parts, target)
        return target
    if parts.netloc or decoded.startswith("/"):
        raise ValueError(f"unsafe absolute link target: {target}")
    if decoded.startswith("#"):
        return target
    path = PurePosixPath(parts.path)
    if not parts.path or ".." in path.parts or ":" in path.parts[0]:
        raise ValueError(f"link must be HTTPS or repository-relative: {target}")
    resolved = (REPO / parts.path).resolve()
    if not resolved.is_relative_to(REPO.resolve()):
        raise ValueError(f"link escapes repository: {target}")
    kind = path_kind(parts.path)
    if kind is None:
        raise ValueError(f"missing repository link target: {target}")
    # Partial Pages checkouts omit research directories; repo_url handles those from
    # the retained Git tree rather than inventing a site-local address.
    fragment = (f"?{parts.query}" if parts.query else "") + (
        f"#{parts.fragment}" if parts.fragment else ""
    )
    if destination == "site":
        if (
            kind == "blob"
            and path.parent == PurePosixPath("packing/contributors/people")
            and path.suffix == ".md"
        ):
            return f"profiles/{path.stem}.html{fragment}"
        return repo_url(parts.path, fragment)
    return target


def _https_authority(parts: SplitResult, target: str) -> None:
    try:
        hostname = parts.hostname or ""
        port = parts.port
        valid_host = (
            bool(IPv6Address(hostname))
            if ":" in hostname
            else bool(re.fullmatch(r"[a-zA-Z0-9.-]+", hostname.encode("idna").decode("ascii")))
        )
    except (ValueError, UnicodeError) as error:
        raise ValueError(f"unsafe HTTPS authority: {target}") from error
    if not valid_host or (port is not None and not 0 < port <= 65535):
        raise ValueError(f"unsafe HTTPS authority: {target}")


class _RenderedURLs(HTMLParser):
    """Apply the changelog URL policy to safe HTML, including generated MathML links."""

    def __init__(self, destination: Destination, *, allow_links: bool = True) -> None:
        super().__init__(convert_charrefs=False)
        self.destination: Destination = destination
        self.allow_links = allow_links
        self.parts: list[str] = []

    def _start(self, tag: str, attrs: list[tuple[str, str | None]], closing: str) -> None:
        if not self.allow_links and (
            tag == "a" or any(name in {"href", "xlink:href"} and value for name, value in attrs)
        ):
            raise ValueError("links are not allowed in News headlines")
        serialized = []
        for name, value in attrs:
            safe_value = (
                serialized_target(value, destination=self.destination)
                if name in {"href", "src", "xlink:href"} and value
                else value
            )
            serialized.append(
                name
                if safe_value is None
                else f'{name}="{html.escape(safe_value, quote=True)}"'
            )
        suffix = " " + " ".join(serialized) if serialized else ""
        self.parts.append(f"<{tag}{suffix}{closing}>")

    @override
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._start(tag, attrs, "")

    @override
    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._start(tag, attrs, "/")

    @override
    def handle_endtag(self, tag: str) -> None:
        self.parts.append(f"</{tag}>")

    @override
    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    @override
    def handle_entityref(self, name: str) -> None:
        self.parts.append(f"&{name};")

    @override
    def handle_charref(self, name: str) -> None:
        self.parts.append(f"&#{name};")

    @override
    def handle_comment(self, data: str) -> None:
        self.parts.append(f"<!--{data}-->")


@cache
def _sanitized_prose(text: str) -> DocumentTree:
    tree = parse_markdown(text, title="Changelog prose", trust_mode="sanitized")
    for diagnostic in tree.diagnostics:
        if diagnostic.type == "html_sanitized_tag" or (
            diagnostic.type == "html_sanitized_attribute"
            and re.search(
                r"attribute '(?:on[^']*|href|src|xlink:href|style|srcdoc|action|"
                r"formaction|background|ping|poster)'",
                diagnostic.message,
            )
        ):
            raise ValueError(f"unsafe generated prose: {diagnostic.message}")
    # Generic normalization warnings and benign MathML presentation attributes (for
    # example `fence`) are not active content. The sanitized output remains authoritative.
    return tree


def _inline_references(text: str, tokens: list[Token], env: dict[str, Any]) -> str:
    """Resolve each field's definitions before unrelated fields share one document."""
    if not env.get("references"):
        return text
    lines = text.splitlines(keepends=True)
    blocks: dict[str, str] = {}
    ranges = [
        token
        for token in tokens
        if token.map and token.type in {"definition", "math_block", "math_block_label"}
    ]
    for token in sorted(
        ranges, key=lambda token: token.map[0] if token.map else -1, reverse=True
    ):
        assert token.map is not None
        start, end = token.map
        if token.type == "definition":
            lines[start:end] = ["\n"]
        else:
            marker = f"\x00MATH{start}\x00"
            blocks[marker] = "".join(lines[start:end])
            lines[start:end] = [marker]
    source = "".join(lines)
    parser = _markdown()
    replacements: list[tuple[int, int, str]] = []

    def reference_link(state: StateInline, silent: bool) -> bool:  # noqa: FBT001 -- parser callback signature
        start = state.pos
        if state.src[start] != "[":
            return inline_link(state, silent)
        label_end = state.md.helpers.parseLinkLabel(state, start, disableNested=True)
        count = len(state.tokens)
        accepted = inline_link(state, silent)
        if accepted and not silent and label_end >= 0:
            link_token = next(
                (token for token in state.tokens[count:] if token.type == "link_open"), None
            )
            if link_token is not None and link_token.meta.get("label"):
                label = state.src[start + 1 : label_end]
                target = serialized_target(
                    str(link_token.attrGet("href")), destination="github"
                )
                title = link_token.attrGet("title")
                quoted = f' "{html.escape(str(title), quote=True)}"' if title else ""
                replacements.append((start, state.pos, f"[{label}]({target}{quoted})"))
        return accepted

    parser.inline.ruler.at("link", reference_link)
    parser.inline.parse(source, parser, env, [])
    for start, end, replacement in sorted(replacements, reverse=True):
        source = source[:start] + replacement + source[end:]
    for marker, block in blocks.items():
        source = source.replace(marker, block)
    return source.strip()


def _prose(
    text: str, *, destination: Destination = "github", rewrite_links: bool = True
) -> str:
    if not text.strip():
        raise ValueError("blank changelog prose")
    env: dict[str, Any] = {}
    parsed = _markdown().parse(text, env)
    tokens = _walk(parsed)
    for token in tokens:
        if set(token.attrs) - {"href", "title", "start"}:
            raise ValueError("Markdown HTML attributes are not allowed in changelog prose")
        if token.type in ("html_block", "html_inline", "image"):
            raise ValueError("raw HTML and images are not allowed in changelog prose")
        if token.type in ("heading_open", "fence", "code_block", "hr"):
            raise ValueError("changelog prose accepts paragraphs, inline code, math, and lists")
        if token.type == "link_open":
            _target(str(token.attrGet("href")), destination=destination)
    for reference in [*env.get("references", {}).values(), *env.get("duplicate_refs", [])]:
        _target(reference["href"], destination=destination)
    tree = _sanitized_prose(text)
    rendered = _RenderedURLs(destination if rewrite_links else "github")
    rendered.feed(tree.html)
    rendered.close()
    if destination == "github":
        return _inline_references(text, parsed, env).strip()
    return "".join(rendered.parts).strip()


def _inline_math(tex: str) -> str:
    # The surrounding inline renderer applies the site URL policy to the completed
    # fragment. Retain authored paths here so profile URLs are converted only once.
    rendered = _prose(f"${tex}$", destination="site", rewrite_links=False)
    return rendered.removeprefix("<p>").removesuffix("</p>")


def _inline_text(text: str) -> str:
    parts: list[str] = []
    last = 0
    for match in MATH.finditer(text):
        parts.append(html.escape(text[last : match.start()], quote=False))
        parts.append(_inline_math(breakable_quotients(prose_tex(match.group(0)))))
        last = match.end()
    parts.append(html.escape(text[last:], quote=False))
    return "".join(parts)


def inline_html(text: str, *, allow_links: bool = True) -> str:
    """Safe inline News Markdown, with authored and legacy register math set by KPress.

    Raw HTML stays visible text. A linked preview headline disables authored links
    so its enclosing article link never contains another anchor.
    """
    parser = _markdown()
    parser.options["html"] = False
    env: dict[str, Any] = {}
    parsed = parser.parseInline(text, env)
    for token in _walk(parsed):
        if set(token.attrs) - {"href", "title"}:
            raise ValueError("Markdown HTML attributes are not allowed in News text")
        if token.type == "image":
            raise ValueError("images are not allowed in News text")
        if token.type == "link_open":
            if not allow_links:
                raise ValueError("links are not allowed in News headlines")
            # Validate the authored repository path here; the final HTML pass also
            # handles MathML links and rewrites every destination exactly once.
            _target(str(token.attrGet("href")), destination="site")

    def render_inline(
        _renderer: object,
        tokens: Sequence[Token],
        index: int,
        _options: Any,
        _env: Any,
    ) -> str:
        token = tokens[index]
        if token.type == "math_inline":
            return _inline_math(token.content.strip())
        if token.type == "code_inline":
            classified = classify(token.content)
            if classified.kind == "math" and classified.latex:
                return _inline_math(breakable_quotients(classified.latex))
            return f"<code>{html.escape(token.content, quote=False)}</code>"
        return _inline_text(token.content)

    for kind in ("text", "math_inline", "code_inline"):
        parser.add_render_rule(kind, render_inline)
    rendered = _RenderedURLs("site", allow_links=allow_links)
    rendered.feed(str(parser.renderer.render(parsed, parser.options, env)))
    rendered.close()
    return "".join(rendered.parts).strip()


def _day(value: str, label: str) -> None:
    try:
        parsed = date.fromisoformat(value).isoformat()
    except ValueError as error:
        raise ValueError(f"{label}: invalid calendar date {value!r}") from error
    if parsed != value:
        raise ValueError(f"{label}: invalid calendar date {value!r}")


@cache
def _public_targets() -> frozenset[str]:
    from devtools.render_overview import SITE_URL  # noqa: PLC0415

    registry = load_yaml((ROOT / "site-urls.yaml").read_text(encoding="utf-8"))
    # Previous main records retain their published host when the freeze check reads
    # them. Recognize that explicit alias without accepting arbitrary hostnames.
    return frozenset(
        root + row["canonical"]
        for root in (SITE_URL, "https://jlevy.github.io/squares/")
        for row in registry["urls"]
        if row.get("status") == "live" and not row.get("pattern")
    )


@cache
def _result_ids() -> frozenset[str]:
    document = load_yaml((ROOT / "frontier/results.yaml").read_text(encoding="utf-8"))
    return frozenset(record["id"] for record in document["results"])


def validate_frozen(document: Document, previous: Document) -> None:
    """Keep existing announcements' dates and PR membership fixed across updates."""
    current = {entry["id"]: entry for entry in document["entries"]}
    for old in previous["entries"]:
        entry = current.get(old["id"])
        if (
            entry is None
            or entry["date"] != old["date"]
            or set(entry["pull_requests"]) != set(old["pull_requests"])
        ):
            raise ValueError(f"frozen entry {old['id']}: date and PR membership cannot change")


def validate_previous_ref(document: Document, ref: str) -> None:
    """Freeze previous public entries independently of editable local snapshots.

    Read a local reference only; missing history is allowed for the first introduction
    of this record, whereas an unknown reference or a corrupt old record fails closed.
    """
    resolved = subprocess.run(
        ["git", "rev-parse", "--verify", "--end-of-options", ref + "^{commit}"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    record = "packing/site-changelog.yaml"
    tree = subprocess.run(
        ["git", "ls-tree", resolved, "--", record],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
    )
    if not tree.stdout.strip():
        return
    previous = load_yaml(
        subprocess.run(
            ["git", "show", f"{resolved}:{record}"],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    )
    previous_schema = load_yaml(
        subprocess.run(
            ["git", "show", f"{resolved}:packing/site-changelog.schema.yaml"],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    )
    validate(previous, schema=previous_schema)
    validate_frozen(document, previous)


def validate(document: Document, *, schema: Document | None = None) -> None:
    """Enforce the structural contract and retained merge/publication semantics."""
    release.validate_release_impacts()
    meta = document.get("softschema")
    if not isinstance(meta, dict) or meta != {
        "contract": "packing.squares:SiteChangelog/v1",
        "schema": "site-changelog.schema.yaml",
        "status": "enforced",
    }:
        raise ValueError(
            "site changelog requires its enforced softschema metadata without an envelope"
        )
    payload = {key: value for key, value in document.items() if key != "softschema"}
    validator = Draft202012Validator(schema) if schema is not None else _validator()
    errors = list(validator.iter_errors(payload))
    if errors:
        error = errors[0]
        location = "/".join(map(str, error.instance_path)) or "<root>"
        raise ValueError(f"{location}: {error.message}")
    frozen = document.get("frozen_entries", [])
    if len({entry["id"] for entry in frozen}) != len(frozen):
        raise ValueError("duplicate frozen entry id")
    validate_frozen(document, {"entries": frozen})
    deliveries: dict[int, Document] = {}
    for delivery in document["deliveries"]:
        number = delivery["number"]
        if number in deliveries:
            raise ValueError(f"duplicate retained delivery PR #{number}")
        try:
            datetime.fromisoformat(delivery["merged_at"])
        except ValueError as error:
            raise ValueError(f"PR #{number}: invalid merged_at timestamp") from error
        if not delivery["title"].strip():
            raise ValueError(f"PR #{number}: blank retained title")
        if not delivery["base_ref"].strip():
            raise ValueError(f"PR #{number}: blank retained base_ref")
        if receipt := delivery.get("delivery_to_main"):
            commit = delivery["merge_commit"]
            if receipt["commit"] != commit or receipt["evidence"] != (
                document["repository"] + "/commit/" + commit
            ):
                raise ValueError(f"PR #{number}: inconsistent delivery_to_main receipt")
        deliveries[number] = delivery
    stacks: dict[int, set[int]] = {}
    for stack in document.get("stacks", []):
        if stack["id"] in stacks:
            raise ValueError(f"duplicate formal stack {stack['id']}")
        _target(stack["evidence"], destination="github")
        stacks[stack["id"]] = set(stack["pull_requests"])
    for number, delivery in deliveries.items():
        if (stack_id := delivery.get("stack_id")) is not None and number not in stacks.get(
            stack_id, set()
        ):
            raise ValueError(
                f"PR #{number}: retained stack membership lacks formal stack evidence"
            )
    seen_ids: set[str] = set()
    represented: set[int] = set()
    for entry in document["entries"]:
        identifier = entry["id"]
        if identifier in seen_ids:
            raise ValueError(f"duplicate entry id {identifier}")
        if identifier == "changelog" or re.fullmatch(r"\d{4}-\d{2}-\d{2}", identifier):
            raise ValueError(f"entry id {identifier} collides with a changelog heading")
        seen_ids.add(identifier)
        _day(entry["date"], identifier)
        if not entry["title"].strip() or "\n" in entry["title"]:
            raise ValueError(f"{identifier}: blank or multiline title")
        inline_html(entry["title"], allow_links=False)
        if "significance" in entry:
            rationale = entry_significance(entry)["rationale"]
            if not rationale.strip() or re.search(r"[\r\n<>`*_\[\]$]", rationale):
                raise ValueError(
                    f"{identifier}: significance rationale must be nonempty plain text"
                )
        _prose(entry["summary"])
        if "details" in entry:
            _prose(entry["details"])
        if entry.get("grouping") == "related" and (
            "stack_id" in entry or len(entry["pull_requests"]) < 2
        ):
            raise ValueError(
                f"{identifier}: related grouping needs multiple PRs and no stack_id"
            )
        if (
            len(entry["pull_requests"]) > 1
            and "stack_id" not in entry
            and entry.get("grouping") != "related"
        ):
            raise ValueError(
                f"{identifier}: grouped PRs require verified formal stack membership "
                "or an explicit related grouping"
            )
        merge_dates: list[str] = []
        for number in entry["pull_requests"]:
            represented.add(number)
            if number not in deliveries:
                raise ValueError(f"PR #{number}: no retained merged main delivery")
            delivery = deliveries[number]
            merge_dates.append(delivery["merged_at"][:10])
            if delivery.get("stack_id") != entry.get("stack_id"):
                raise ValueError(
                    f"PR #{number}: entry stack disagrees with retained formal stack membership"
                )
        if entry["date"] != max(merge_dates):
            raise ValueError(f"{identifier}: date must be latest merge date of included PRs")
        if "stack_id" in entry and not set(entry["pull_requests"]).issubset(
            stacks.get(entry["stack_id"], set())
        ):
            raise ValueError(f"{identifier}: invalid formal stack grouping")
        for reference in entry.get("references", []):
            if not reference["label"].strip():
                raise ValueError(f"{identifier}: blank reference label")
            _target(reference["target"], destination="github")
        if set(entry.get("result_ids", [])) - _result_ids():
            raise ValueError(f"{identifier}: unknown retained result identity")
        if entry.get("artifacts") and "publication" not in entry:
            raise ValueError(f"{identifier}: launched artifacts require publication evidence")
        if "publication" in entry:
            _target(entry["publication"]["evidence"], destination="github")
            if "date" in entry["publication"]:
                _day(entry["publication"]["date"], f"{identifier} publication")
        for artifact in entry.get("artifacts", []):
            _target(artifact["target"], destination="github")
            if artifact["target"].split("#", 1)[0] not in _public_targets():
                raise ValueError(
                    f"{identifier}: artifact is not a registered public destination"
                )
            if not artifact["label"].strip():
                raise ValueError(f"{identifier}: blank artifact label")
        components: set[str] = set()
        for reference in entry.get("releases", []):
            component = reference["component"]
            if component in components:
                raise ValueError(f"{identifier}: duplicate release component {component}")
            components.add(component)
            history = release.component_history(component)
            if reference["version"] not in {item.version for item in history}:
                raise ValueError(
                    f"{identifier}: {component} {reference['version']} "
                    "absent from retained history"
                )
    coverage = set(document["coverage"]["pull_requests"])
    omitted: set[int] = set()
    for omission in document["coverage"]["omissions"]:
        number = omission["pull_request"]
        if number in omitted or number in represented or not omission["reason"].strip():
            raise ValueError(
                f"coverage: duplicate, represented, or blank disposition for PR #{number}"
            )
        omitted.add(number)
    if coverage != set(deliveries) or coverage != represented | omitted:
        raise ValueError(
            "coverage: every retained main delivery must appear in one or more entries "
            "or exactly one omission"
        )


#: A GitHub address written in an entry's prose, up to the Markdown that closes it.
_GITHUB_URL = re.compile(r"https://github\.com/[^\s)\]<>\"']+")
#: An entry's first line in the YAML as written.
_ENTRY_LINE = re.compile(r"^  - id: (\S+)$")


def required_issues(
    document: Document,
    entry: Document,
    reporting: dict[str, tuple[int, ...]] | None = None,
    opened: Mapping[int, str] | None = None,
) -> tuple[int, ...]:
    """The issues an entry must list in `issues`: each issue that reported one of its
    `result_ids` (`campaign/result-requests.yaml`, `github_references.reporting_issues`)
    and was opened by the entry's date, and each issue of this repository its own
    summary, details or references link.

    An entry may list more; editorial links to other issues stay the author's choice."""
    texts = [
        entry["summary"],
        entry.get("details", ""),
        *(item["target"] for item in entry.get("references", [])),
    ]
    linked = cited_issues(
        document["repository"], (url for text in texts for url in _GITHUB_URL.findall(text))
    )
    reported = issues_reporting(
        entry.get("result_ids", ()),
        reporting,
        on_or_before=str(entry["date"]),
        opened=_opening_days(reporting, opened),
    )
    return tuple(sorted({*reported, *linked}))


def _opening_days(
    reporting: dict[str, tuple[int, ...]] | None, opened: Mapping[int, str] | None
) -> Mapping[int, str]:
    """The issues' opening days: the committed record's, unless a caller passes its own
    table, and none for a caller's own `reporting` table with no days of its own."""
    if opened is not None:
        return opened
    return issue_opened() if reporting is None else {}


def issue_findings(
    document: Document,
    reporting: dict[str, tuple[int, ...]] | None = None,
    opened: Mapping[int, str] | None = None,
) -> list[str]:
    """Each entry whose `issues` omits an issue `required_issues` names, or lists one
    opened after the entry's date, which it cannot have come from."""
    findings = []
    days = _opening_days(reporting, opened)
    for entry in document["entries"]:
        listed = set(entry.get("issues", ()))
        if missing := [
            n for n in required_issues(document, entry, reporting, days) if n not in listed
        ]:
            findings.append(
                f"{entry['id']}: issues omits {', '.join(f'#{number}' for number in missing)}"
            )
        if later := sorted(n for n in listed if days.get(n, "") > str(entry["date"])):
            findings.append(
                f"{entry['id']}: issues lists {', '.join(f'#{number}' for number in later)}, "
                "opened after the entry's date"
            )
    return findings


def backfill_issues(
    text: str, document: Document, reporting: dict[str, tuple[int, ...]] | None = None
) -> str:
    """The changelog's YAML with each entry's `issues` widened to `required_issues`.

    The edit is textual so the hand-written layout survives: an existing `issues` field is
    rewritten in place and a missing one goes directly under `pull_requests`, in the same
    flow or block style. Entries already complete, and `frozen_entries`, are untouched."""
    entries = {entry["id"]: entry for entry in document["entries"]}
    lines = text.splitlines(keepends=True)
    start = next(index for index, line in enumerate(lines) if line.rstrip("\n") == "entries:")
    end = next(
        (
            index
            for index in range(start + 1, len(lines))
            if re.match(r"^[a-z_]+:", lines[index])
        ),
        len(lines),
    )
    heads = [
        index for index in range(start + 1, end) if _ENTRY_LINE.match(lines[index].rstrip("\n"))
    ]

    def field(first: int, last: int, key: str) -> tuple[int, int] | None:
        """The lines a top-level field of an entry spans: its key and any block items."""
        for index in range(first, last):
            if lines[index].startswith(f"    {key}:"):
                stop = index + 1
                while stop < last and lines[stop].startswith("      "):
                    stop += 1
                return index, stop
        return None

    edits: list[tuple[int, int, list[str]]] = []
    for head, tail in zip(heads, [*heads[1:], end], strict=True):
        match = _ENTRY_LINE.match(lines[head].rstrip("\n"))
        assert match is not None
        entry = entries[match[1]]
        listed = set(entry.get("issues", ()))
        wanted = sorted(listed | set(required_issues(document, entry, reporting)))
        if wanted == sorted(listed):
            continue
        pulls = field(head, tail, "pull_requests")
        if pulls is None:
            raise ValueError(f"{entry['id']}: no pull_requests to place issues under")
        if "[" in lines[pulls[0]]:
            rendered = [f"    issues: [{', '.join(map(str, wanted))}]\n"]
        else:
            rendered = ["    issues:\n", *(f"      - {number}\n" for number in wanted)]
        span = field(head, tail, "issues") or (pulls[1], pulls[1])
        edits.append((*span, rendered))
    for first, last, replacement in sorted(edits, reverse=True):
        lines[first:last] = replacement
    return "".join(lines)


def inline_comments(text: str) -> list[tuple[int, str]]:
    """The lines on which a `#` after a space, outside every scalar, is read as a comment.

    YAML ends a plain scalar at a space before `#`, so `label: Mathematical review of #845`
    loads as "Mathematical review of", and nothing reports the cut: seven of #852's News
    labels and one of 9 October's rendered that way (#860's review A1), as the lineage
    line of #852's ledger had (its review's M-2). The record holds no inline comments, so
    every such `#` is refused; the value is quoted instead. Whole-line comments stand.
    """
    spans = [
        (token.start_mark.index, token.end_mark.index)
        for token in yaml.scan(text, Loader=BaseLoader)
        if isinstance(token, yaml.ScalarToken)
    ]
    starts = [start for start, _ in spans]
    found: list[tuple[int, str]] = []
    for match in re.finditer(r"[ \t]#", text):
        at = match.end() - 1
        line_start = text.rfind("\n", 0, at) + 1
        if not text[line_start:at].strip():
            continue
        index = bisect.bisect_right(starts, at) - 1
        if index >= 0 and spans[index][0] <= at < spans[index][1]:
            continue
        line_end = text.find("\n", at)
        line = text[line_start : len(text) if line_end < 0 else line_end].strip()
        found.append((text.count("\n", 0, at) + 1, line))
    return found


def load(path: Path = SRC) -> Document:
    """Read one enforced changelog; no network or GitHub metadata discovery."""
    text = path.read_text(encoding="utf-8")
    if cut := inline_comments(text):
        lines = "; ".join(f"line {number}: {line}" for number, line in cut)
        raise ValueError(
            f"{path.name}: a ` #` outside quotes cuts the value off as a comment ({lines}); "
            "quote the value"
        )
    document = load_yaml(text)
    if not isinstance(document, dict):
        raise TypeError("site changelog must be a YAML mapping")
    validate(document)
    return document


#: The register whose significant results News must announce.
RESULTS = ROOT / "frontier" / "results.yaml"
RESULTS_PATH = "packing/frontier/results.yaml"
#: The two records a change can settle an owed announcement in: the register, and News.
ANNOUNCEMENT_RECORDS = (RESULTS_PATH, "packing/site-changelog.yaml")
#: The `--announcement-base` that means main's own delivery: the records tier passes it
#: on a push to main and on the scheduled run, and only there (`validate._synopsis`).
#: The merge under test can no longer act on a failure, so main only reports.
MAIN_DELIVERY_BASE = "HEAD^1"

#: The lowest significance at which a registered result must have a News item: the
#: owner's decision of 22 October 2026, "We need a systematic process for the
#: significant results", then "Let's have it do S4 and S5 then". S3 News stays optional.
ANNOUNCED_FROM = 4

#: S4 and S5 results that landed before the News archive existed, each mapped to its
#: register score, at which it is exempt. `packing/site-changelog.yaml` was created on
#: 13 October 2026 (6279bd0e6), and the first S4 or S5 result with a News item, T-060
#: (30 September), was backfilled on 16 October UTC (#638). These fifteen landed 1
#: September to 3 October and have no item; T-064 and T-081 are named only by an S2
#: entry, which News does not show. Under the decision of 22 October they are exempt
#: rather than given invented backdated News; backfilling them as dated News, as T-060
#: was, is a separate decision. The list only shrinks: an exemption whose result changes
#: score, leaves the register or gains its item is stale, and the gate fails until it
#: is removed (a raised result is then owed like any other).
ANNOUNCEMENT_EXEMPT: dict[str, int] = {
    "T-010": 4,
    "T-017": 4,
    "T-018": 5,
    "T-019": 4,
    "T-020": 4,
    "T-022": 5,
    "T-024": 5,
    "T-025": 5,
    "T-026": 5,
    "T-037": 5,
    "T-047": 4,
    "T-051": 4,
    "T-052": 4,
    "T-064": 4,
    "T-081": 4,
}

_RESULT_SCORE = re.compile(r"\n    significance:\n      score: (\d)\b")
_PULL_REQUEST_MERGE = re.compile(r"^Merge pull request #(\d+) ")


class Landing(TypedDict):
    """The first-parent change that registered a result or raised it to its score."""

    pull_request: int | None
    commit: str
    subject: str


class AnnouncementFindings(NamedTuple):
    """What the announcement gate found, by what it does about each."""

    failures: list[str]
    """Fail the check: an owed item the change can settle, or a stale exemption."""
    owed: list[str]
    """Registered or raised by the change under test, so owed after its merge."""
    unsettled: list[str]
    """Owed on main by an earlier merge; a warning, since this change edits neither
    the register nor News."""


def load_results(path: Path = RESULTS) -> list[Document]:
    """The register's results, read offline."""
    return load_yaml(path.read_text(encoding="utf-8"))["results"]


def news_announced_scores(document: Document) -> dict[str, int]:
    """The highest News significance at which each result is announced.

    Only an entry News shows counts: one with an S3 or higher score and no
    `news_exclusion`, which lists the result in `result_ids`.
    """
    announced: dict[str, int] = {}
    for entry in news_entries(document):
        score = entry_significance(entry)["score"]
        for identifier in entry.get("result_ids", []):
            announced[identifier] = max(announced.get(identifier, 0), score)
    return announced


def owed_announcements(document: Document, results: Sequence[Document]) -> list[Document]:
    """Registered S4 and S5 results that no News entry announces at their own score.

    A result and its announcement share a score (`result-import.md`, "Label the PR and
    Prepare News"), so an S5 result announced only at S4 is still owed. Exempt results
    are owed only once raised above their exempt score.
    """
    announced = news_announced_scores(document)
    return [
        result
        for result in results
        if (score := result["significance"]["score"]) >= ANNOUNCED_FROM
        and announced.get(result["id"], 0) < score
        and ANNOUNCEMENT_EXEMPT.get(result["id"], 0) < score
    ]


def stale_exemptions(document: Document, results: Sequence[Document]) -> list[str]:
    """Exemptions that no longer describe an unannounced result at its exempt score."""
    scores = {result["id"]: result["significance"]["score"] for result in results}
    announced = news_announced_scores(document)
    problems: list[str] = []
    for identifier, exempt in ANNOUNCEMENT_EXEMPT.items():
        score = scores.get(identifier)
        if score is None:
            reason = "is not in the register"
        elif score < ANNOUNCED_FROM:
            reason = f"is S{score} now, below the announcement threshold"
        elif score != exempt:
            reason = f"is S{score} now, not the S{exempt} it is exempt at"
        elif announced.get(identifier, 0) >= score:
            reason = "now has its News item"
        else:
            continue
        problems.append(
            f"{identifier} {reason}: remove it from render_changelog.ANNOUNCEMENT_EXEMPT"
        )
    return problems


def register_score(text: str, identifier: str) -> int:
    """A result's significance score in one revision of the register's text, or 0."""
    start = text.find(f"\n  - id: {identifier}\n")
    if start < 0:
        return 0
    end = text.find("\n  - id: ", start + 1)
    match = _RESULT_SCORE.search(text, start, end if end >= 0 else len(text))
    return int(match.group(1)) if match else 0


def _git(*arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments], cwd=REPO, capture_output=True, text=True, check=True
    ).stdout


def landing(identifier: str, score: int, ref: str) -> Landing | None:
    """The first-parent change on `ref` from which `identifier` has held `score` or more.

    It is the merged PR a News entry announcing the result names. Read from local
    history only; `None` when the history at hand does not reach it.
    """
    found: Landing | None = None
    log = _git("log", "--first-parent", "--format=%H%x00%s", ref, "--", RESULTS_PATH)
    for line in log.splitlines():
        commit, subject = line.split("\0", 1)
        if register_score(_git("show", f"{commit}:{RESULTS_PATH}"), identifier) < score:
            break
        number = _PULL_REQUEST_MERGE.match(subject)
        found = {
            "pull_request": int(number.group(1)) if number else None,
            "commit": commit,
            "subject": subject,
        }
    return found


def _owed_message(
    result: Document,
    change: Landing | None,
    *,
    context: Literal["settle", "unrelated", "main"],
) -> str:
    identifier = result["id"]
    score = result["significance"]["score"]
    if change is None:
        source = (
            "the merged PR that registered or raised it, which this checkout's history "
            "does not reach"
        )
        number = "NNN"
    elif change["pull_request"] is None:
        source = (
            f"commit {change['commit'][:9]} ({change['subject']}), which registered or "
            "raised it"
        )
        number = "NNN"
    else:
        number = str(change["pull_request"])
        source = f"PR #{number}, which registered or raised it (merge {change['commit'][:9]})"
    scored_by = result["significance"].get("by", "the register")
    remedy = (
        f"Its item is an entry in packing/site-changelog.yaml scored {score}, listing "
        f"{identifier} in result_ids and naming {source}; draft it from packing/ with "
        f"`uv run --frozen --all-extras --group dev python -m devtools.import_changelog "
        f'--pr {number} --significance-rationale "..." --output '
        '"$TMPDIR/changelog-candidate.yaml"`, then bring in its delivery and the edited '
        "entry (packing/campaign/result-import.md, stage 7, Announce a Significant "
        f"Result). It was scored by {scored_by}; ask its intake coordinator if the item "
        "is not yours to write."
    )
    owed = f"{identifier} (S{score}) is on main with no News item at S{score}"
    if context == "settle":
        return (
            f"{owed}, and this change edits the register or the News record, so it "
            "settles the debt: add the item in this PR, or land the stage 7 follow-up "
            "first and merge main. " + remedy
        )
    if context == "main":
        return (
            f"{owed}. On main the gate reports and never fails, since the merge under "
            "test can no longer act on it; pull-request CI enforces it, and the next "
            "pull request that changes the register or the News record fails until the "
            "item lands. " + remedy
        )
    return (
        f"{owed}. This change edits neither the register nor the News record, so it is "
        "not failed; the next pull request that does fails until the item lands. " + remedy
    )


def check_announcements(
    document: Document,
    results: Sequence[Document],
    base_results: Sequence[Document] | None = None,
    *,
    locate: Callable[[str, int], Landing | None] | None = None,
    records_changed: bool = True,
    on_main: bool = False,
) -> AnnouncementFindings:
    """Every S4 and S5 result without its News item, sorted by what the gate does.

    An entry can name only merged PRs, so a result registered or raised by the change
    under test (absent from `base_results`, or below its score there) is owed after the
    merge and reported, not failed. A result already owed on main fails only a change
    that edits the register or the News record (`records_changed`), the one change that
    can settle it, since the PR that owes it has merged and its item now validates.
    Any other change gets a warning. On main (`on_main`, a push or the scheduled run),
    an owed result is only ever a warning, records change or not: pull-request CI is
    where the rule is enforced, and the one way main sees an owed result is a records
    merge that raced the S4/S5 merge, which must not turn main red (#738's review A).
    This is option (b) of the decision of 22 October (#735's review A); option (a), an
    item that names its own PR and is stamped at merge, is think-n51k. A stale
    exemption always fails. `locate(identifier, score)` finds the PR that owes an item;
    without `base_results` nothing is in grace.
    """
    base = (
        None
        if base_results is None
        else {result["id"]: result["significance"]["score"] for result in base_results}
    )
    findings = AnnouncementFindings(stale_exemptions(document, results), [], [])
    for result in owed_announcements(document, results):
        identifier, score = result["id"], result["significance"]["score"]
        if base is not None and base.get(identifier, 0) < score:
            findings.owed.append(
                f"{identifier} (S{score}) is registered or raised on this branch and owes "
                "a News item after the merge: draft it in the PR description now, and land "
                "it in the first change after the merge (result-import.md, stage 7). The "
                "next pull request that changes the register or the News record fails "
                "until it does."
            )
            continue
        change = locate(identifier, score) if locate is not None else None
        if on_main:
            findings.unsettled.append(_owed_message(result, change, context="main"))
        elif records_changed:
            findings.failures.append(_owed_message(result, change, context="settle"))
        else:
            findings.unsettled.append(_owed_message(result, change, context="unrelated"))
    return findings


def announcement_base(ref: str) -> tuple[str, list[Document]]:
    """The fork point of HEAD and `ref`, and the register there."""
    base = _git("merge-base", "HEAD", ref).strip()
    return base, load_yaml(_git("show", f"{base}:{RESULTS_PATH}"))["results"]


def edits_announcement_records(base: str) -> bool:
    """Whether the working tree's register or News record differs from `base`'s."""
    return bool(_git("diff", "--name-only", base, "--", *ANNOUNCEMENT_RECORDS).strip())


def _text(value: str) -> str:
    escaped = html.escape(value, quote=True)
    return re.sub(r"([\\`*_{}\[\]#!|])", r"\\\1", escaped)


def serialized_target(target: str, *, destination: Destination = "site") -> str:
    """The canonical URL written to a rendered link, shared with publication audits."""
    resolved = _target(target, destination=destination)
    encoded = quote(resolved, safe=":/?#@!$&*+,;=%-._~[]")
    return normalizeLink(encoded)


def _markdown_link(label: str, target: str, *, destination: Destination) -> str:
    """Keep URL delimiters inside one link before trusted Markdown reaches kpress."""
    return f"[{_text(label)}]({serialized_target(target, destination=destination)})"


def entry_anchor(identifier: str) -> str:
    """Stable entry fragments retain their namespace across News and legacy About links."""
    return f"changelog-entry-{identifier}"


def _component_label(component: str) -> str:
    if component in {"site", "infographics"}:
        return component.capitalize()
    from devtools.render_overview import paper_record  # noqa: PLC0415

    return paper_record(component.removeprefix("paper:")).title


def _entry_lines(
    document: Document,
    entry: Document,
    destination: Destination,
    *,
    include_significance: bool = True,
    include_prose: bool = True,
    multiline_metadata: bool = False,
) -> list[str]:
    """Shared contribution prose and evidence for the complete GitHub and News views."""
    rating = entry_significance(entry)
    label_separator = "  \n" if multiline_metadata else " "
    link_separator = "  \n" if multiline_metadata else " · "
    ending = "" if multiline_metadata else "."
    out: list[str] = []
    if destination == "github" and include_significance:
        out.extend([f"Significance S{rating['score']}: {_text(rating['rationale'])}", ""])
    if include_prose:
        out.extend([_prose(entry["summary"], destination=destination), ""])
        if "details" in entry:
            out.extend([_prose(entry["details"], destination=destination), ""])
    if entry.get("artifacts"):
        links = [
            _markdown_link(item["label"], item["target"], destination=destination)
            for item in entry["artifacts"]
        ]
        out.extend(
            ["Published artifacts:" + label_separator + link_separator.join(links) + ending, ""]
        )
    if entry.get("releases"):
        versions = [
            f"{_text(_component_label(item['component']))} {_text(item['version'])}"
            for item in entry["releases"]
        ]
        separator = "  \n" if multiline_metadata else "; "
        out.extend(
            ["Component editions:" + label_separator + separator.join(versions) + ending, ""]
        )
    publication = entry.get("publication", {})
    if publication:
        evidence = _markdown_link(
            "publication evidence"
            if "date" in publication and not multiline_metadata
            else "Publication evidence",
            publication["evidence"],
            destination=destination,
        )
        if "date" in publication:
            first = f"First public: {publication['date']}"
            out.extend(
                [
                    first + "  \n" + evidence
                    if multiline_metadata
                    else f"{first} ({evidence}).",
                    "",
                ]
            )
        else:
            out.extend([evidence + ending, ""])
    issues = sorted(entry.get("issues", []))
    issue_targets = {issue_url(document["repository"], number) for number in issues}
    links = [
        _markdown_link(
            f"Issue #{number}",
            issue_url(document["repository"], number),
            destination=destination,
        )
        for number in issues
    ]
    links.extend(
        _markdown_link(
            f"PR #{number}", f"{document['repository']}/pull/{number}", destination=destination
        )
        for number in sorted(entry["pull_requests"])
    )
    # A reference to a listed issue's thread is that issue's link, already given.
    links.extend(
        _markdown_link(item["label"], item["target"], destination=destination)
        for item in entry.get("references", [])
        if item["target"].rstrip("/") not in issue_targets
    )
    heading = "Issues, PRs and supporting records:" if issues else "PRs and supporting records:"
    out.extend([heading + label_separator + link_separator.join(links) + ending, ""])
    return out


def render_markdown(
    document: Document,
    *,
    destination: Destination = "github",
    heading_level: int = 2,
    include_heading: bool = True,
) -> str:
    """A shared, date-grouped section; stable anchors are independent of titles.

    `include_heading` writes the section's own Changelog heading and the `changelog`
    anchor with it. The site's Changelog page is titled by its own article, which owns
    that anchor there, so it asks for the days and their entries alone and the days sit
    one level under `heading_level` as they do in a section."""
    if destination not in ("github", "site") or heading_level not in (1, 2, 3, 4):
        raise ValueError("invalid changelog destination or heading depth")
    validate(document)
    out: list[str] = []
    if include_heading:
        out = (
            [f'<h{heading_level} id="changelog">Changelog</h{heading_level}>', ""]
            if destination == "site"
            else ['<a id="changelog"></a>', "", "#" * heading_level + " Changelog", ""]
        )
    last_date = ""
    for entry in ordered_entries(document):
        if entry["date"] != last_date:
            last_date = entry["date"]
            date_anchor = f"changelog-date-{last_date}"
            date_level = heading_level + 1
            if destination == "site":
                out.extend(
                    [
                        f'<h{date_level} id="{date_anchor}">{last_date}</h{date_level}>',
                        "",
                    ]
                )
            else:
                out.extend(
                    [
                        f'<a id="{date_anchor}"></a>',
                        "",
                        "#" * (heading_level + 1) + " " + last_date,
                        "",
                    ]
                )
        level = heading_level + 2
        anchor = entry_anchor(entry["id"])
        if destination == "site":
            out.extend(
                [
                    (
                        f'<h{level} id="{anchor}">'
                        f"{inline_html(entry['title'], allow_links=False)}</h{level}>"
                    ),
                    "",
                ]
            )
        else:
            out.extend(
                [
                    f'<a id="{anchor}"></a>',
                    "",
                    "#" * level + " " + _text(entry["title"]),
                    "",
                ]
            )
        out.extend(_entry_lines(document, entry, destination))
    return "\n".join(out).rstrip() + "\n"


def ordered_entries(document: Document) -> list[Document]:
    """The retained newest-day order, with stable IDs ordering contributions on a day."""
    return sorted(
        document["entries"],
        key=lambda item: (-date.fromisoformat(item["date"]).toordinal(), item["id"]),
    )


def news_entries(document: Document) -> list[Document]:
    """S3 to S5 public announcements; lower scores remain in the GitHub history."""
    return [
        entry
        for entry in ordered_entries(document)
        if "news_exclusion" not in entry and entry_significance(entry)["score"] >= NEWS_FLOOR
    ]


def archived_news_targets(document: Document) -> dict[str, str]:
    """Retired article and day bookmarks still reach their retained changelog entries,
    which the site now serves itself (`CHANGELOG_PAGE`)."""
    public_ids = {entry["id"] for entry in news_entries(document)}
    excluded = [entry for entry in document["entries"] if entry["id"] not in public_ids]
    anchors = [entry_anchor(entry["id"]) for entry in excluded]
    public_days = {entry["date"] for entry in news_entries(document)}
    anchors.extend(
        f"changelog-date-{day}"
        for day in sorted({entry["date"] for entry in excluded} - public_days)
    )
    return {anchor: f"{CHANGELOG_PAGE}#{anchor}" for anchor in anchors}


def news_forward_targets(document: Document) -> dict[str, str]:
    """Every bookmark News keeps without showing it, by anchor: the `changelog` bookmark
    the section answered here before the history took a page of its own, then each entry
    and day below the News floor (`archived_news_targets`)."""
    return {"changelog": f"{CHANGELOG_PAGE}#changelog", **archived_news_targets(document)}


def entry_targets(
    document: Mapping[str, Any], entry: Mapping[str, Any], *, supporting: bool
) -> list[tuple[str, str]]:
    """An entry's GitHub threads as `(label, target)`, issues then pull requests, and
    with `supporting` its artifacts, publication evidence and supporting records too.

    A change News tells carries the second group in its story, so its Changelog line
    asks for `supporting=False` and gives the threads alone. A change News never shows
    has no other reader surface, so its line carries everything it declares and
    `check_published_site.changelog_checks` holds it to that.
    """
    issues = sorted(entry.get("issues", []))
    issue_targets = {issue_url(document["repository"], number) for number in issues}
    pairs = [
        (f"Issue #{number}", issue_url(document["repository"], number)) for number in issues
    ]
    pairs.extend(
        (f"PR #{number}", f"{document['repository']}/pull/{number}")
        for number in sorted(entry["pull_requests"])
    )
    if not supporting:
        return pairs
    pairs.extend((item["label"], item["target"]) for item in entry.get("artifacts", []))
    publication = entry.get("publication", {})
    if publication:
        pairs.append(("Publication evidence", publication["evidence"]))
    # A reference naming a listed issue is that issue's own link, already given.
    pairs.extend(
        (item["label"], item["target"])
        for item in entry.get("references", [])
        if item["target"].rstrip("/") not in issue_targets
    )
    return pairs


def _changelog_link(label: str, target: str) -> str:
    """One link on a Changelog line. A place off the site opens in a new tab, as every
    other off-site link on the site does (`overview_sections.external_link`)."""
    url = serialized_target(target)
    away = ' target="_blank" rel="noopener noreferrer"' if url.startswith("http") else ""
    return f'<a href="{html.escape(url, quote=True)}"{away}>{html.escape(label)}</a>'


def changelog_entry_line(
    document: Mapping[str, Any], entry: Mapping[str, Any], *, in_news: bool
) -> str:
    """One site or project change in its day's block on the Changelog page: its title,
    then on the quieter line its score and every GitHub thread behind it.

    The title links to the change's own News story where it has one, so the detail is one
    click away and is written once. Where News never shows the change this line is its
    only reader surface, so it carries the supporting records as well
    (`entry_targets`). The line holds the entry's anchor, which keeps the retired
    article and day bookmarks that `archived_news_targets` forwards here resolving.

    The Changelog is "concise, mostly complete, linked to github issues and PRs clearly",
    and a story belongs to News rather than to both surfaces (the owner, 26 October 2026).
    """
    anchor = entry_anchor(entry["id"])
    title = inline_html(entry["title"], allow_links=False)
    head = f'<a href="{NEWS_PAGE}#{anchor}">{title}</a>' if in_news else title
    parts = [
        _changelog_link(label, target)
        for label, target in entry_targets(document, entry, supporting=not in_news)
    ]
    # A release News never announces is named here, since this line is then the only
    # reader surface that could carry its component editions.
    if not in_news and entry.get("releases"):
        editions = "; ".join(
            f"{html.escape(_component_label(item['component']))} {html.escape(item['version'])}"
            for item in entry["releases"]
        )
        parts.append(editions)
    score = entry_significance(entry)["score"]
    return (
        f'<li id="{html.escape(anchor, quote=True)}">{head}'
        f"<small>S{score} · {' · '.join(parts)}</small></li>"
    )


def _news_forward_anchors(targets: dict[str, str]) -> str:
    return "".join(
        f'<a class="site-news-legacy-anchor" id="{html.escape(anchor, quote=True)}" '
        f'href="{html.escape(target, quote=True)}" data-news-target '
        'aria-hidden="true" tabindex="-1"></a>'
        for anchor, target in targets.items()
    )


def news_topics(topics: Sequence[str]) -> str:
    """Subject tags reuse result chips without asserting a result kind or status."""
    if not topics:
        return ""
    if any(topic not in NEWS_TOPICS for topic in topics):
        raise ValueError("unknown News topic")
    return (
        '<p class="site-news-topics">'
        + " ".join(topic_chip(topic, attribute="data-news-topic") for topic in topics)
        + "</p>"
    )


def news_rating(rating: Significance) -> str:
    """An archive article uses the same significance meter as a result."""
    from devtools.overview_sections import significance_mark  # noqa: PLC0415

    meaning = news_significance_tooltip(rating["score"])
    return (
        f'<p class="site-news-significance">{significance_mark(rating["score"], meaning)}</p>'
    )


def news_article_header(
    title_html: str, day_text: str, topics: Sequence[str], rating: Significance
) -> str:
    """The reading-card heading, followed by News topics and the importance tooltip."""
    from devtools.overview_sections import article_header  # noqa: PLC0415

    return article_header(
        title_html,
        date.fromisoformat(day_text),
        metadata_html=(
            f'<div class="site-news-metadata">{news_topics(topics)}{news_rating(rating)}</div>'
        ),
        extra_class="site-news-header",
    )


def news_significance_filter(selected: Sequence[int] = NEWS_LEVELS) -> str:
    """The significance choices, one button a level News has, pressed for each level in
    `selected`: the one widget both the archive's filters and the home page's News box
    draw (`news_filters`), and the selection `news-filters.js` starts from."""
    scores = "".join(
        f'<button type="button" data-news-score="{score}" '
        f'title="{html.escape(news_significance_tooltip(score), quote=True)}" '
        f'aria-pressed="{str(score in selected).lower()}">S{score}</button>'
        for score in range(NEWS_FLOOR, 6)
    )
    return (
        '<fieldset><legend class="site-visually-hidden" id="news-significance-label">'
        'Significance</legend><div class="site-tabs site-chooser-small" role="group" '
        f'aria-labelledby="news-significance-label">{scores}</div></fieldset>'
    )


#: What a filtered list says when nothing matches its choices.
NEWS_EMPTY = "<p data-news-empty hidden>No news matches these filters.</p>"
#: What a preview says when News holds no article for it to show (#736's review A,
#: finding A8).
NEWS_NONE = "<p>No news yet.</p>"


def news_filters(
    topics_present: set[str] | None = None,
    *,
    selected: Sequence[int] = NEWS_LEVELS,
    compact: bool = False,
) -> str:
    """Progressive controls, hidden until `news-filters.js` shows them. The archive's
    are the significance choices (`news_significance_filter`), the topics, a reset and a
    count; without the enhancement every article stays visible. The `compact` form, the
    home page's News box's, is the significance choices alone, at the right above the
    cards and quieter than the archive's (`.site-news-filters-compact`), with the
    archive's live count kept for screen readers and hidden from sight (#736's review A,
    finding A5)."""
    if compact:
        return (
            '<div class="site-news-filters site-news-filters-compact sans-text" '
            "data-news-filters data-site-tooltip-outside hidden>"
            f"{news_significance_filter(selected)}{NEWS_EMPTY}"
            '<span class="site-visually-hidden" data-news-count role="status" '
            'aria-live="polite"></span></div>'
        )
    topics = "".join(
        f'<button type="button" class="site-filter-option site-chip" '
        f'data-site-filter-option data-news-topic="{topic}" aria-pressed="true">'
        f"{NEWS_CHECK}<span data-news-topic-label data-site-filter-label>{label}</span>"
        '<span class="site-cell-quiet" data-news-tally> (0)</span></button>'
        for topic, label in NEWS_TOPICS.items()
        if topics_present is None or topic in topics_present
    )
    chevron = (
        '<svg class="site-nav-icon site-filter-chevron" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true" focusable="false">'
        '<path d="m6 9 6 6 6-6"/></svg>'
    )
    return (
        '<div class="site-news-filters sans-text" data-news-filters '
        "data-site-tooltip-outside hidden>"
        f"{news_significance_filter(selected)}"
        '<fieldset><legend class="site-visually-hidden" '
        'id="news-topics-label">Topics</legend>'
        '<div class="site-filter-menu" data-site-filter-menu>'
        '<button type="button" class="site-filter-trigger" data-site-filter-trigger '
        'aria-expanded="false" aria-controls="news-topics-options">'
        "<span>Topics</span> <span data-site-filter-summary>All</span>"
        f'{chevron}</button><div class="site-filter-options" id="news-topics-options" '
        'data-site-filter-options role="group" aria-labelledby="news-topics-label" hidden>'
        '<button type="button" class="site-filter-option" data-site-filter-all '
        'aria-pressed="true">All topics</button>'
        f"{topics}</div></div></fieldset>"
        '<div class="site-table-tools">'
        '<button type="button" class="site-news-reset" data-news-reset>'
        "Reset filters</button>"
        '<span class="site-count" data-news-count role="status" '
        f'aria-live="polite"></span></div>{NEWS_EMPTY}</div>'
    )


def news_card(anchor: str, day_text: str, body: str) -> str:
    """One dated card around already sanitized article HTML, complete without scripts."""
    from devtools.overview_sections import arrow_icon  # noqa: PLC0415

    day = date.fromisoformat(day_text)
    label = f"{day:%B} {day.day}, {day.year}"
    safe_anchor = html.escape(anchor, quote=True)
    return (
        f'<section class="site-news-day" id="{safe_anchor}" '
        f'data-news-day="{day_text}">'
        f'<div class="site-news-body" id="{safe_anchor}-body">{body}</div>'
        f'<footer class="site-news-footer"><button class="site-news-expand" '
        f'type="button" hidden aria-expanded="true" aria-controls="{safe_anchor}-body" '
        f'aria-label="Collapse news for {label}">{arrow_icon("double-up")}</button>'
        f"</footer></section>"
    )


def render_news(
    document: Document,
    *,
    limit: int | None = None,
    entry_ids: set[str] | None = None,
    selected: Sequence[int] | None = None,
) -> str:
    """Complete canonical cards, optionally selected by ID and limited for a preview.

    The archive (no `limit`) opens on `selected`, by default `NEWS_LEVELS`, under its full
    filters pressed at those levels, and hides the cards at any other until a reader
    chooses them. A preview shows `limit` cards. Given `selected` levels, it carries every
    card `entry_ids` names under the compact significance filter preselected to those
    levels, and shows the newest `limit` of them at those levels; the rest are hidden, with
    or without scripts, until a reader widens the choice (`news-filters.js`,
    `data-news-limit`). With no card to carry it says "No news yet." and draws no filter.
    Without `selected` a preview carries its newest `limit` cards alone, unfiltered.

    Their names are plain profile links (`data-contributor-plain`): News navigates to a
    profile rather than opening it in the profile popover (`paper-design.md`).
    """
    validate(document)
    if limit is not None and limit < 1:
        raise ValueError("a News preview needs at least one item")
    entries = [
        entry
        for entry in news_entries(document)
        if entry_ids is None or entry["id"] in entry_ids
    ]
    filtered = limit is not None and selected is not None
    if limit is not None and not filtered:
        entries = entries[:limit]
    levels = NEWS_LEVELS if selected is None else tuple(selected)
    # A filtered preview first shows the newest `limit` cards at its levels.
    first = [entry["id"] for entry in entries if entry_significance(entry)["score"] in levels]
    shown = set(first[:limit]) if filtered else None
    filters, limited = "", ""
    if limit is None:
        filters = news_filters(
            {topic for entry in entries for topic in entry.get("topics", [])}, selected=levels
        )
    elif filtered:
        if not entries:
            return (
                f'<div class="site-news" data-news data-news-limit="{limit}" '
                f"data-contributor-plain>{NEWS_NONE}</div>"
            )
        filters = news_filters(selected=levels, compact=True)
        limited = f' data-news-limit="{limit}"'
    out = [
        filters,
        f'<div class="site-news" data-news{limited} data-contributor-plain>',
    ]
    seen_dates: set[str] = set()
    for entry in entries:
        anchor = entry_anchor(entry["id"])
        title = inline_html(entry["title"], allow_links=False)
        if limit is not None:
            title = f'<a href="news.html#{anchor}">{title}</a>'
        article = []
        if entry["date"] not in seen_dates:
            # Retain the old daily bookmark at the first individual card for that day.
            article.append(f'<div id="changelog-date-{entry["date"]}"></div>')
            seen_dates.add(entry["date"])
        header = news_article_header(
            title, entry["date"], entry.get("topics", []), entry_significance(entry)
        )
        article.append(
            f'<article class="site-news-item" data-news-entry="{entry["id"]}">{header}'
        )
        from devtools.profile_links import link_prose  # noqa: PLC0415

        article.append('<div class="site-news-prose kpress-prose">')
        article.append(link_prose(_prose(entry["summary"], destination="site")))
        if "details" in entry:
            article.append(link_prose(_prose(entry["details"], destination="site")))
        article.append("</div>")
        article.append('<div class="site-news-records sans-text">')
        article.extend(
            _prose(field, destination="site")
            for field in _entry_lines(
                document,
                entry,
                "github",
                include_significance=False,
                include_prose=False,
                multiline_metadata=True,
            )
            if field
        )
        article.append("</div>")
        article.append("</article>")
        card = news_card(anchor, entry["date"], "\n".join(article))
        card = card.replace(
            "data-news-day=",
            f'data-news-score="{entry_significance(entry)["score"]}" '
            f'data-news-topics="{" ".join(entry.get("topics", []))}" data-news-day=',
            1,
        )
        hidden = (
            entry["id"] not in shown
            if shown is not None
            else limit is None and entry_significance(entry)["score"] not in levels
        )
        if hidden:
            card = card.replace(
                '<section class="site-news-day"', '<section hidden class="site-news-day"', 1
            )
        out.append(card)
    out.append("</div>")
    if limit is None:
        out.append(_news_forward_anchors(news_forward_targets(document)))
        source = html.escape(f"{document['repository']}/blob/main/CHANGELOG.md", quote=True)
        from devtools.overview_sections import arrow_icon  # noqa: PLC0415

        # The archive closes on the whole history: this site's Changelog page first, then
        # the generated file on GitHub (the owner, 2026-10-26).
        out.append(
            '<p class="site-action-row">'
            f'<a class="site-action" href="{CHANGELOG_PAGE}">Changelog'
            f"{arrow_icon('right')}</a>"
            f'<a class="site-action" href="{source}" '
            'aria-label="Changelog on GitHub">Changelog on GitHub'
            f"{arrow_icon('external')}</a></p>"
        )
    return "\n".join(out)


def legacy_news_anchors(document: Document) -> str:
    """Keep old About bookmarks navigable without duplicating the history there."""
    anchors = [entry_anchor(entry["id"]) for entry in document["entries"]]
    anchors.extend(
        f"changelog-date-{day}" for day in sorted({e["date"] for e in document["entries"]})
    )
    targets = {anchor: f"news.html#{anchor}" for anchor in anchors}
    targets.update(news_forward_targets(document))
    return _news_forward_anchors(targets)


def render(document: Document) -> str:
    """The generated root view, including its provenance and documentation footer."""
    return (
        BANNER + "\n\n# Project changelog\n\n"
        "Project contributions and public launches, newest merge date first.\n"
        "The authoritative record is [site-changelog.yaml](packing/site-changelog.yaml).\n\n"
        + render_markdown(document)
        + "\n"
        + FOOTER
        + "\n"
    )


def _signature(text: str) -> list[tuple]:
    """Compare Markdown structure and text while allowing Flowmark soft wrapping."""
    signature = []
    for token in _walk(_markdown().parse(text)):
        if token.type in ("inline", "softbreak"):
            continue
        content = (
            token.content
            if token.type in ("code_inline", "code_block", "fence")
            else " ".join(token.content.split())
        )
        if token.type == "text" and not content:
            continue
        if token.type == "text" and signature and signature[-1][0] == "text":
            previous = signature.pop()
            content = previous[-1] + " " + content
        signature.append(
            (token.type, token.nesting, token.tag, sorted(token.attrs.items()), content)
        )
    return signature


def main(argv: Sequence[str] | None = None) -> int:
    """Render atomically, or fail when the committed reader view is stale."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SRC)
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument(
        "--baseline", type=Path, help="Prior published YAML to freeze dates and membership"
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--baseline-ref", help="Local main reference whose published entries are frozen"
    )
    parser.add_argument(
        "--announcement-base",
        metavar="REF",
        help="Require a News item for every registered S4 and S5 result; results new or "
        "raised since HEAD's merge base with REF are owed after the merge, not failed, "
        f"and with {MAIN_DELIVERY_BASE}, main's own delivery, owed results only warn",
    )
    parser.add_argument(
        "--backfill-issues",
        action="store_true",
        help="Write into the source each issue an entry must list and does not "
        "(`required_issues`), then continue",
    )
    options = parser.parse_args(argv)
    try:
        document = load(options.source)
        if options.backfill_issues:
            text = options.source.read_text(encoding="utf-8")
            if (filled := backfill_issues(text, document)) != text:
                with atomic_output_file(options.source) as output:
                    output.write_text(filled, encoding="utf-8")
                print(f"wrote missing issues into {options.source}")
            document = load(options.source)
        if findings := issue_findings(document):
            for finding in findings:
                print(f"changelog: {finding}", file=sys.stderr)
            print(
                "changelog: an entry lists each issue that reported its results or that it "
                "links; run python -m devtools.render_changelog --backfill-issues",
                file=sys.stderr,
            )
            return 1
        if options.baseline:
            validate_frozen(document, load(options.baseline))
        if options.baseline_ref:
            validate_previous_ref(document, options.baseline_ref)
        if options.announcement_base:
            base, base_results = announcement_base(options.announcement_base)
            results = load_results()
            findings = check_announcements(
                document,
                results,
                base_results,
                locate=lambda identifier, score: landing(identifier, score, base),
                records_changed=edits_announcement_records(base),
                on_main=options.announcement_base == MAIN_DELIVERY_BASE,
            )
            significant = sum(
                result["significance"]["score"] >= ANNOUNCED_FROM for result in results
            )
            print(
                f"announcements: {significant} registered S4 and S5 results, "
                f"{len(ANNOUNCEMENT_EXEMPT)} exempt from before the News archive, "
                f"{len(findings.owed)} owed after this merge, {len(findings.unsettled)} "
                f"owed on main and reported, {len(findings.failures)} failing"
            )
            for note in findings.owed:
                print(f"announcement owed after merge: {note}")
            for warning in findings.unsettled:
                print(f"warning: announcement owed on main: {warning}")
            if findings.failures:
                for failure in findings.failures:
                    print(f"changelog: announcement missing: {failure}", file=sys.stderr)
                return 1
        rendered = render(document)
        if options.check:
            current = (
                options.output.read_text(encoding="utf-8") if options.output.exists() else ""
            )
            if _signature(current) != _signature(rendered):
                print(
                    f"{options.output}: stale; run python -m devtools.render_changelog",
                    file=sys.stderr,
                )
                return 1
            print("changelog: enforced record and generated view agree")
        else:
            with atomic_output_file(options.output) as output:
                output.write_text(rendered, encoding="utf-8")
            print(f"wrote {options.output}")
    except (
        OSError,
        TypeError,
        ValueError,
        yaml.YAMLError,
        subprocess.CalledProcessError,
    ) as error:
        print(f"changelog: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
