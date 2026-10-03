"""Every colour the site and its papers paint with is a named token (`think-zhlc`).

`devtools.check_colour_tokens` holds the served stylesheets to it. A check that finds
nothing proves nothing on its own, so each rule here has a negative control as well: a
stylesheet that smuggles the thing past it.
"""

from __future__ import annotations

from pathlib import Path

from devtools import check_colour_tokens as colours


def _problems(css: str) -> list[str]:
    return [finding.why for finding in colours.stylesheet_findings(css)]


def test_every_served_stylesheet_paints_with_tokens_alone() -> None:
    found, stale = colours.findings()
    assert [str(finding) for finding in found] == []
    assert stale == []
    assert colours.undeclared_paint_tokens(declaring=colours.kpress_stylesheets()) == []
    assert {path.name for path in colours.STYLESHEETS} >= {
        "site.css",
        "site-nav.css",
        "site-result.css",
        "paper-publication.css",
        "n11-optimality-review.css",
    }


def test_a_token_may_hold_any_colour_and_a_rule_may_name_tokens() -> None:
    css = """
    :root { --ink: #17202a; --wash: oklch(95% 0.01 250); --tint: 16%; --red: red; }
    .a { color: var(--ink); background: var(--wash, var(--ink)); }
    .b { background: color-mix(in oklch, var(--ink) var(--tint), var(--wash)); }
    .c { border: 1px solid currentcolor; outline-color: transparent; }
    .d { background: oklch(calc(var(--l) + var(--n) * var(--s)) var(--c) var(--h)); }
    @media (forced-colors: active) { .e { background: CanvasText; } }
    .f { width: 12px; margin: 0 0.5rem; content: "red"; }
    """
    assert _problems(css) == []


def test_a_rule_that_names_a_colour_of_its_own_is_refused() -> None:
    assert _problems(".a { color: #fff; }") == ["hex colour #fff"]
    assert _problems(".a { color: oklch(52% 0.19 25); }") == [
        "oklch() names a value of its own: oklch(52% 0.19 25)"
    ]
    assert _problems(".a { box-shadow: 0 1px 2px rgb(0 0 0 / 0.2); }") == [
        "rgb() names a value of its own: rgb(0 0 0 / 0.2)"
    ]
    # A mix of tokens whose ratio is written in the rule: the ratio is the token's.
    assert _problems(".a { background: color-mix(in oklch, var(--a) 16%, var(--b)); }") == [
        "color-mix() names a value of its own: color-mix(in oklch, 16%, )"
    ]
    assert _problems(".a { border-color: teal; }") == ["named colour teal"]
    # Beside a token is still a colour of its own once the token is set aside.
    assert _problems(".a { color: var(--missing), #000; }") == ["hex colour #000"]
    # Inside an at-rule, and with a comment in the way.
    assert _problems("@media print { .a { /* ink */ color: #000; } }") == ["hex colour #000"]


def test_a_colour_in_a_fallback_is_a_colour_of_its_own() -> None:
    """A `var()`'s fallback paints wherever its token is unset, so it is held to the rule
    too, at any depth; a fallback that is itself a token passes (`think-uer5`)."""
    assert _problems(".a { color: var(--site-ink, #000); }") == ["hex colour #000"]
    assert _problems(".a { color: var(--x, red); }") == ["named colour red"]
    assert _problems(".a { color: var(--a, var(--b, oklch(50% 0.1 20))); }") == [
        "oklch() names a value of its own: oklch(50% 0.1 20)"
    ]
    assert _problems(".a { color: var(--a, var(--b)); border: 1px solid var(--c,); }") == []


def test_a_rule_beside_a_nested_rule_is_read_too() -> None:
    """A rule's own declarations count where it also holds a nested rule, as an `@page`
    holds its margin boxes; the nested rule's prelude is never read as a declaration."""
    assert _problems(".a { color: #123456; .b { margin: 0; } }") == ["hex colour #123456"]
    assert _problems(".a { margin: 0; &:hover { color: teal; } }") == ["named colour teal"]
    css = '@page { color: #000; @bottom-left { content: "x"; } }'
    (finding,) = colours.stylesheet_findings(css)
    assert (finding.selector, finding.declaration) == ("@page", "color: #000")
    assert _problems(".a { #add .b { margin: 0; } }") == []


def test_every_property_that_paints_is_read() -> None:
    """A gradient, a filter's shadow and a text fill paint as a colour does."""
    assert _problems(".a { background-image: linear-gradient(white, black); }") == [
        "named colour white",
        "named colour black",
    ]
    assert _problems(".a { filter: drop-shadow(0 1px 2px black); }") == ["named colour black"]
    assert _problems(".a { -webkit-text-fill-color: navy; }") == ["named colour navy"]


def test_a_finding_names_its_line_and_rule() -> None:
    css = ":root {\n  --a: #000;\n}\n.b {\n  margin: 0;\n  color: #111;\n}\n"
    (finding,) = colours.stylesheet_findings(css, Path("x.css"))
    assert (finding.line, finding.selector, finding.declaration) == (6, ".b", "color: #111")


def test_an_allowed_declaration_names_its_reason_and_a_stale_one_fails(tmp_path: Path) -> None:
    for key, reason in colours.ALLOWED.items():
        assert len(reason.split()) >= 5, key
    sheet = tmp_path / "paper-publication.css"
    sheet.write_text("@page { @bottom-left { color: #000; } }\n.a { color: #fff; }\n")
    allowed = {
        ("paper-publication.css", "@bottom-left", "color"): "a margin box, for the test",
        ("paper-publication.css", ".gone", "color"): "nothing paints here any more",
    }
    found, stale = colours.findings([sheet], allowed)
    assert [finding.selector for finding in found] == [".a"]
    assert stale == [("paper-publication.css", ".gone", "color")]


def test_a_misspelt_paint_token_is_refused(tmp_path: Path) -> None:
    sheet = tmp_path / "x.css"
    sheet.write_text(
        ":root { --site-ink: #000; }\n"
        ".a { color: var(--site-ink); background: var(--site-inc, var(--site-ink)); }\n"
        ".b { width: var(--undeclared-size); }\n"
    )
    assert colours.undeclared_paint_tokens([sheet]) == ["--site-inc"]
