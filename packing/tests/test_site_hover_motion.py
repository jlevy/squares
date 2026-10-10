"""Every hover on the site eases on one transition (paper-design.md, Motion; think-g9cu).

A hover or keyboard focus that changes a colour, a wash, a text colour, a border or a
shadow, changes it over `--site-hover-transition`, one value declared in `site-nav.css`,
which every page carries: 140ms, ease-out, and nothing under reduced motion. The table
rows' wash used to snap, since no rule gave a row a transition, while the cards and the
bar beside them eased; a new hover rule could do the same again without anyone noticing.
So this reads the stylesheets and holds every rule whose selector has a hover or focus
state, and that changes one of those properties, to the element it styles carrying the
token at rest, where it eases both in and out: in a rule of the same selector without
the state, in a broader rule that matches every element it does, or in the shared rule
`SHARED` names for it. A last check reads, in Chromium, what the browser makes of the
token, with motion and without.
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
import tinycss2
from tinycss2.ast import LiteralToken, WhitespaceToken

from devtools import render_overview
from devtools.render_n11_lower_bounds_explainer import PUBLICATION_STYLE
from sqpack.probes import probe
from tests import site_browser, site_renders

PROBES = Path(__file__).resolve().parent / "probes"
TRANSITION = probe(PROBES, "site_hover_motion/transition")

#: The stylesheets that carry the site's hovers: the site's own four and the papers'
#: publication layer, which runs on the same token.
SHEETS = (
    render_overview.SITE_CSS,
    render_overview.SITE_NAV_CSS,
    render_overview.SITE_RESULT_CSS,
    render_overview.PAPER_TYPE_CSS,
    PUBLICATION_STYLE,
)
TOKEN = "var(--site-hover-transition)"
TIMING = "var(--site-hover-duration) var(--site-hover-easing)"
#: What the token eases, in the order it names them.
EASED = ("background-color", "color", "border-color", "box-shadow")
#: The declarations whose change the token eases: a fill, a text colour, a border, a
#: shadow. An outline is a focus ring, which shows at once, and a text decoration is
#: discrete.
CHANGES = re.compile(
    r"background(-color)?|color|box-shadow"
    r"|border(-(block|inline|top|right|bottom|left)(-(start|end))?)?(-color)?"
)
#: The pseudo-classes of a hover or a focus: the states a rule is written for.
STATES = frozenset({":hover", ":focus-visible", ":focus", ":focus-within", ":active"})

#: Where a hover's element takes the token from a rule broader than its own selector
#: names, and broader in a way the stylesheet cannot show: the hover's selector without
#: its state, and the selector of the rule that gives it the token. Each says why.
SHARED = {
    # A card with a foot is always a `div.site-card` (`link_card(foot=)`); it washes
    # while its link is hovered or focused (`:has()`).
    ".kpress .site-card-footed": ".kpress div.site-card.site-card-footed",
    # The site's name is the bar's first link.
    ".site-nav .site-name": ".site-nav a",
    # A paper's source chips are links on its page.
    ".doc-links .chip": ".cert-page a",
    # The probe's rotation handle is a button the explainer's script places on its page.
    ".cert-page .rotation-handle": ".cert-page button",
    # On a paper's page the `.kpress` root is the `.cert-page`.
    ".kpress a.kpress-footnote-backref": ".cert-page a.kpress-footnote-backref",
}

type Compound = tuple[str, frozenset[str]]
type Rule = tuple[str, list[str], dict[str, str]]


def _rules(nodes: list[Any], context: str = "") -> Iterator[Rule]:
    """Each style rule: the at-rules it is nested in, its selectors and its
    declarations."""
    for node in nodes:
        if node.type == "qualified-rule":
            declarations = tinycss2.parse_declaration_list(
                node.content, skip_whitespace=True, skip_comments=True
            )
            yield (
                context,
                _selectors(node.prelude),
                {
                    d.lower_name: tinycss2.serialize(d.value).strip()
                    for d in declarations
                    if d.type == "declaration"
                },
            )
        elif node.type == "at-rule" and node.content is not None:
            inner = tinycss2.parse_rule_list(
                node.content, skip_whitespace=True, skip_comments=True
            )
            prelude = tinycss2.serialize(node.prelude).strip()
            yield from _rules(inner, f"{context}@{node.lower_at_keyword} {prelude}")


def _sheet(path: Path) -> list[Rule]:
    text = path.read_text(encoding="utf-8")
    return list(
        _rules(tinycss2.parse_stylesheet(text, skip_whitespace=True, skip_comments=True))
    )


def _selectors(prelude: list[Any]) -> list[str]:
    """A selector list split at its top-level commas."""
    selectors = [""]
    for token in prelude:
        if token == ",":
            selectors.append("")
        else:
            selectors[-1] += token.serialize()
    return [" ".join(selector.split()) for selector in selectors]


def _compounds(selector: str) -> list[Compound]:
    """The selector as its compound selectors, each a set of simple selectors with the
    combinator before it ("" for the first, " " for a descendant)."""
    compounds: list[Compound] = []
    simple: list[str] = []
    combinator = ""
    prefix = ""

    def close() -> None:
        nonlocal simple, combinator
        if simple:
            compounds.append((combinator if compounds else "", frozenset(simple)))
            simple = []
            combinator = " "

    for token in tinycss2.parse_component_value_list(selector):
        if isinstance(token, WhitespaceToken):
            close()
        elif isinstance(token, LiteralToken) and token.value in {">", "+", "~"}:
            close()
            combinator = token.value
        elif isinstance(token, LiteralToken) and token.value in {".", ":"}:
            prefix += token.value
        else:
            simple.append(prefix + token.serialize())
            prefix = ""
    close()
    return compounds


def _is_state(simple: str) -> bool:
    """Whether a simple selector is a hover or focus state: one of `STATES`, a
    `:has()` that holds one, or an `:is()` or `:where()` of states and attributes, such
    as `:is(:hover, :focus-visible, [aria-expanded="true"])`, that names at least one."""
    if simple in STATES:
        return True
    function = re.fullmatch(r":(is|where|has)\((.*)\)", simple)
    if function is None:
        return False
    if function.group(1) == "has":
        return any(state in function.group(2) for state in STATES)
    arguments = [argument.strip() for argument in function.group(2).split(",")]
    return any(argument in STATES for argument in arguments) and all(
        argument in STATES or argument.startswith("[") for argument in arguments
    )


def _rest(compounds: list[Compound]) -> list[Compound]:
    """The selector without its states: what it styles at rest."""
    return [
        (combinator, frozenset(s for s in simple if not _is_state(s)))
        for combinator, simple in compounds
    ]


def _pseudo_element(compound: Compound) -> frozenset[str]:
    return frozenset(simple for simple in compound[1] if simple.startswith("::"))


def _covers(broader: list[Compound], selector: list[Compound]) -> bool:
    """Whether every element `selector` matches is one `broader` matches, as far as the
    selectors show it: each compound of `broader` is a part of one of `selector`'s, in
    order, its last of `selector`'s last, with the same pseudo-element if either names
    one. A `broader` with a combinator other than the descendant's must be the same
    selector."""
    if any(combinator not in {"", " "} for combinator, _ in broader):
        return broader == selector
    if not broader or not selector or not broader[-1][1] <= selector[-1][1]:
        return False
    if _pseudo_element(broader[-1]) != _pseudo_element(selector[-1]):
        return False
    place = len(selector) - 2
    for _, simple in reversed(broader[:-1]):
        while place >= 0 and not simple <= selector[place][1]:
            place -= 1
        if place < 0:
            return False
        place -= 1
    return True


def _text(compounds: list[Compound]) -> str:
    return "".join(
        f"{combinator}{''.join(sorted(simple, key=_order))}" for combinator, simple in compounds
    ).strip()


def _order(simple: str) -> tuple[int, str]:
    """A type selector first, then the rest as written."""
    return (0 if simple[:1].isalpha() or simple == "*" else 1, simple)


def _hovers() -> Iterator[tuple[str, str, list[Compound], list[str]]]:
    """Each selector, with a hover or focus state, of a rule that changes what the token
    eases, outside print: its sheet, the selector, what it styles at rest and the
    declarations it changes. A selector whose rule also names it at rest holds a value
    steady through the hover and changes nothing."""
    for sheet in SHEETS:
        for context, selectors, declarations in _sheet(sheet):
            changed = sorted(name for name in declarations if CHANGES.fullmatch(name))
            if not changed or "print" in context:
                continue
            plain = [_compounds(selector) for selector in selectors]
            for selector, compounds in zip(selectors, plain, strict=True):
                rest = _rest(compounds)
                if rest != compounds and rest not in plain:
                    yield sheet.name, selector, rest, changed


def _eased() -> list[list[Compound]]:
    """Every selector of a rule that gives its elements the token, outside the
    reduced-motion blocks."""
    return [
        _compounds(selector)
        for sheet in SHEETS
        for context, selectors, declarations in _sheet(sheet)
        if declarations.get("transition") == TOKEN and "reduced-motion" not in context
        for selector in selectors
    ]


def test_the_hover_transition_is_one_token_declared_once() -> None:
    """The token names the four colour properties on the one timing, 140ms ease-out,
    and is `none` under reduced motion; the timing is declared only in `site-nav.css`,
    which every page carries, and KPress's own hover timing takes the same value."""
    nav = render_overview.SITE_NAV_CSS.read_text(encoding="utf-8")
    declared = {
        context: declarations
        for context, selectors, declarations in _sheet(render_overview.SITE_NAV_CSS)
        if selectors == [":root"] and "--site-hover-transition" in declarations
    }
    assert list(declared) == ["", "@media (prefers-reduced-motion: reduce)"]
    motion, still = declared.values()
    eased = ", ".join(f"{name} {TIMING}" for name in EASED)
    assert " ".join(motion["--site-hover-transition"].split()) == eased
    assert still["--site-hover-transition"] == "none"
    assert motion["--site-hover-duration"] == "140ms"
    assert 120 <= int(motion["--site-hover-duration"].removesuffix("ms")) <= 160
    assert motion["--site-hover-easing"] == "ease-out"
    assert still["--site-hover-duration"] == "0ms"
    header = {
        context: declarations["--site-header-duration"]
        for context, selectors, declarations in _sheet(render_overview.SITE_NAV_CSS)
        if selectors == [":root"] and "--site-header-duration" in declarations
    }
    assert header == {"": "180ms", "@media (prefers-reduced-motion: reduce)": "0ms"}
    assert f"--kpress-transition-fast: {TIMING};" in nav
    for sheet in SHEETS:
        if sheet != render_overview.SITE_NAV_CSS:
            text = sheet.read_text(encoding="utf-8")
            for name in ("--site-hover-transition:", "--site-hover-duration:"):
                assert name not in text, (sheet.name, name)


def test_every_transition_is_the_token_or_one_property_on_its_timing() -> None:
    """A colour eases on the token alone, never listed beside anything, so it composes
    under reduced motion, where the token is `none`; anything else a hover moves, an
    arrow's nudge or an icon's fade, names its one property on the token's timing. No
    transition names a time of its own or `all`. The scroll-driven header uses its
    separate travel token, verified above, rather than the hover timing."""
    for sheet in SHEETS:
        for _, selectors, declarations in _sheet(sheet):
            value = declarations.get("transition")
            if value is None or value in {"none", TOKEN}:
                continue
            if sheet == render_overview.SITE_NAV_CSS and selectors == [".site-headroom"]:
                assert value == "transform var(--site-header-duration) ease-out"
                continue
            for entry in (" ".join(part.split()) for part in value.split(",")):
                name, _, timing = entry.partition(" ")
                assert timing == TIMING, (sheet.name, selectors, entry)
                assert name not in {*EASED, "background", "all"}, (sheet.name, selectors, entry)


def test_every_colour_hover_eases_on_the_token() -> None:
    """Every rule that changes a colour, a border or a shadow on hover or focus styles
    an element that carries the token at rest, so the change eases in and out."""
    eased = _eased()
    missing = [rule for rule in SHARED.values() if _compounds(rule) not in eased]
    assert not missing, f"a rule SHARED names does not carry the token: {missing}"
    shared = {_text(_compounds(rest)) for rest in SHARED}
    unused = set(shared)
    snapping = []
    for sheet, selector, rest, changed in _hovers():
        if any(_covers(rule, rest) for rule in eased):
            continue
        if _text(rest) in shared:
            unused.discard(_text(rest))
            continue
        snapping.append(f"{sheet}: {selector} changes {', '.join(changed)}")
    assert not snapping, "\n".join(snapping)
    assert not unused, f"SHARED names a hover no rule has: {sorted(unused)}"


def test_the_hover_contract_reads_selectors_as_written() -> None:
    """What the contract makes of a selector: its states, what it styles at rest, and
    which broader rule covers it."""
    themed = _compounds('.site-theme-button:is(:hover, :focus-visible, [aria-expanded="true"])')
    assert _text(_rest(themed)) == ".site-theme-button"
    row = _compounds(
        ".kpress .site-table tbody tr:is([data-row-popover], [data-case-row])"
        ':is(:focus-visible, [aria-expanded="true"])'
    )
    assert (
        _text(_rest(row))
        == ".kpress .site-table tbody tr:is([data-row-popover], [data-case-row])"
    )
    assert _covers(_compounds(".kpress .site-table tbody tr"), _rest(row))
    footed = _compounds(
        ".kpress .site-card-footed:has(> .site-card-main:is(:hover, :focus-visible))"
    )
    assert _text(_rest(footed)) == ".kpress .site-card-footed"
    close = _compounds(".site-popover.site-case-pop .site-popover-close:hover")
    assert _covers(_compounds(".site-popover .site-popover-close"), _rest(close))
    assert not _covers(
        _compounds(".site-nav a"), _rest(_compounds(".site-nav .site-name:hover"))
    )
    assert not _covers(
        _compounds(".site-popover > .close"), _compounds(".site-popover div .close")
    )
    assert _compounds("a.x > b") == [("", frozenset({"a", ".x"})), (">", frozenset({"b"}))]


@pytest.fixture(scope="module")
def frontier(tmp_path_factory: pytest.TempPathFactory) -> str:
    """The frontier page, written with its assets where a browser can open it."""
    root = tmp_path_factory.mktemp("hover-motion")
    return site_renders.write(root, "atlas.html")["atlas.html"].as_uri()


@pytest.fixture(scope="module")
def browser() -> Iterator[Any]:
    sync_api = site_browser.api()
    with sync_api.sync_playwright() as driver:
        launched = site_browser.launch(driver)
        yield launched
        launched.close()


@pytest.mark.parametrize("motion", ["no-preference", "reduce"])
def test_the_browser_reads_the_token_as_the_transition(
    browser: Any, frontier: str, motion: str
) -> None:
    """In Chromium a frontier row, the bar's links and the case popover's close cross
    ease the four colour properties over 140ms, ease-out; a reader who asked for reduced
    motion gets no transition at all."""
    context = browser.new_context(reduced_motion=motion)
    try:
        page = context.new_page()
        page.goto(frontier, wait_until="load")
        for selector in ("tr[data-case-row]", ".site-nav a", "#pop-case .site-popover-close"):
            found = page.evaluate(TRANSITION, {"selector": selector})
            assert found is not None, selector
            if motion == "reduce":
                assert found["property"] == "none", (selector, found)
                continue
            assert found["property"] == ", ".join(EASED), (selector, found)
            assert found["duration"] == ", ".join(["0.14s"] * len(EASED)), (selector, found)
            assert found["easing"] == ", ".join(["ease-out"] * len(EASED)), (selector, found)
    finally:
        context.close()
