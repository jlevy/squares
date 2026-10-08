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
