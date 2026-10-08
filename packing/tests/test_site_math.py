"""Published formulas are readable and accessible without a JavaScript renderer."""

from __future__ import annotations

import pytest
from kpress.format.markdown import parse_markdown

from devtools import site_math


def test_static_math_keeps_semantics_and_uses_the_text_context() -> None:
    fragment = parse_markdown(
        "Inline $x^2 + \\alpha$.\n\n$$\\frac{1}{2}$$", title="Mathematics"
    ).html
    page = site_math.prepare(f'<main>{fragment}<div class="sans-text">{fragment}</div></main>')
    assert page.count('data-kpress-math-rendered="true"') == 4
    assert page.count('class="katex-html"') == 4
    assert page.count("<math") == 4
    assert page.count('data-kpress-math-face="prose"') == 2
    assert page.count('data-kpress-math-face="sans"') == 2
    assert site_math.prepare(page) == page


def test_rendering_rejects_unsupported_tex_and_does_not_interpret_script_text() -> None:
    source = (
        '<span class="kpress-math" data-kpress-math="inline">'
        '<span class="kpress-math-render">\\(\\notACommand{x}\\)</span></span>'
    )
    assert (
        site_math.prepare(f'<script type="application/json">{source}</script>')
        == f'<script type="application/json">{source}</script>'
    )
    with pytest.raises(ValueError, match="static mathematics failed"):
        site_math.prepare(source)


def test_paper_host_math_is_prepared_without_changing_other_inline_markup() -> None:
    source = '<h1><span class="tex">n = 11</span></h1><p><span class="tex-d">x^2</span></p>'
    page = site_math.prepare(source)
    assert page.count('class="katex-html"') == 2
    assert 'data-kpress-math-face="sans"' in page
    assert site_math.prepare(page) == page


@pytest.mark.parametrize(
    "role", ["site-result", "site-case-bound", "site-case-note", "site-detail"]
)
def test_record_support_math_uses_sans_and_preserves_explicit_serif(role: str) -> None:
    fragment = parse_markdown("Math $x^2$", title="Mathematics").html
    prepared = site_math.prepare(
        f'<div class="{role}">{fragment}<div data-math-face="serif">{fragment}</div></div>'
    )
    assert prepared.count('data-kpress-math-face="sans"') == 1
    assert prepared.count('data-kpress-math-face="prose"') == 1


def test_reader_profiles_share_geometry_and_keep_semantics_once() -> None:
    fragment = parse_markdown("Math $x^2 + \\frac{1}{2}$", title="Reader profiles").html
    prepared = site_math.prepare(fragment)
    assert prepared.count('class="katex-html"') == 1
    assert prepared.count("<math") == 1
    assert 'data-site-math="prose"' in prepared
    assert '[data-kpress-prose-font="sans"] [data-site-math="prose"]' in prepared
    assert '[data-kpress-font-set="system"] [data-site-math]' in prepared
    assert site_math.prepare(prepared) == prepared


def test_a_different_profile_topology_keeps_an_exact_fallback() -> None:
    visual = site_math.merge_profiles(
        (
            '<span class="katex-html"><span style="height:1em">x</span></span>',
            '<span class="katex-html"><span style="height:2em">x</span></span>',
            '<span class="katex-html"><span>x</span><span>y</span></span>',
        )
    )
    assert visual.count('class="site-math-variant"') == 3
    assert all(
        f'data-site-math-profile="{profile}"' in visual
        for profile in ("prose", "sans", "katex")
    )


def test_preparation_is_independent_of_prior_cached_contexts() -> None:
    fragment = parse_markdown("Math $x^2$", title="Reader profiles").html
    site_math.clear_cache()
    fresh = site_math.prepare(f'<div class="sans-text">{fragment}</div>')
    site_math.clear_cache()
    site_math.prepare(fragment)
    warmed = site_math.prepare(f'<div class="sans-text">{fragment}</div>')
    assert fresh == warmed


def test_explicit_serif_retains_its_own_prepared_reader_selection() -> None:
    fragment = parse_markdown("Math $x^2$", title="Reader profiles").html
    prepared = site_math.prepare(f'<div data-math-face="serif">{fragment}</div>')
    assert 'data-site-math="serif"' in prepared
    assert 'data-kpress-math-face="prose"' in prepared
    assert prepared.count("<math") == 1


def test_complete_shell_receives_the_prepared_fragments_metric_stylesheet() -> None:
    fragment = parse_markdown("Math $x^2$", title="Record").html
    prepared = site_math.prepare(fragment)
    article = prepared[prepared.index("</style>") + len("</style>") :]
    page = site_math.prepare(
        "<html><head><title>Record</title></head><body>" + article + "</body></html>",
        page_path="cases/11.html",
    )
    assert page.count("data-site-math-styles") == 1
    assert 'href="../assets/css/site-math.' in page
    assert page.count("<math") == 1
    assert site_math.prepare(page, page_path="cases/11.html") == page
