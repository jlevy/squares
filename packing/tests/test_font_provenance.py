"""The rules the on-screen provenance guard decides a page by, without a browser.

`inspect_explainer_typography --check-supporting` answers the whole question -- is every
run of text on the page drawn from a face the page ships -- and it needs a rendered page,
a browser and a CDP session to do it. Two rules underneath it decide every finding, and
both fail quietly if they are wrong: one reads a platform-font answer and says whether it
is acceptable, and one decides which elements are asked about at all. A coverage rule that
skips too much reports a clean page it never looked at, which is the failure mode this
project has a name for.

So the two are exercised on fixtures in the shapes Chromium returns:

- the acceptance rule, over `CSS.getPlatformFontsForNode` answers. A custom face from a
  family the page declares passes; a host face on a bead is not a finding; anything else
  is. The case worth having a test for is `LocalPunct`, which is a real `@font-face` and
  so reports as a custom font, whose source is `local("Georgia")` -- the reader's own
  serif under a name the page chose.
- the coverage rule, over a `DOM.getDocument` tree. Text is attributed to the element it
  sits in and not to an ancestor; scripts, styles and the clipped MathML copy of every
  expression are skipped, and `math` is skipped through a namespace that reports its name
  in lower case where HTML reports capitals.

Nothing here starts a browser, and the whole file runs in milliseconds.
"""

# The two rules are private because nothing outside the probe should decide what counts
# as the page's own face. Testing them directly is what keeps this file off a browser.
# pyright: reportPrivateUsage=false
from __future__ import annotations

import pytest

from devtools import render_explainer_pdf
from devtools.inspect_explainer_typography import _text_bearing, _unshipped


def _face(family: str, *, custom: bool, glyphs: int = 10) -> dict[str, object]:
    """One entry of a `CSS.getPlatformFontsForNode` answer."""
    return {
        "familyName": family,
        "postScriptName": family.replace(" ", ""),
        "isCustomFont": custom,
        "glyphCount": glyphs,
    }


def test_a_face_the_document_carries_is_accepted() -> None:
    """Both halves of the test are needed: the bytes are the page's and the name is too."""
    assert _unshipped([_face("PT Serif", custom=True), _face("KaTeX_Main", custom=True)]) == []


def test_a_font_face_whose_source_is_the_hosts_own_is_not_the_pages() -> None:
    """A `@font-face` is not enough: what the guard asks is which file was opened.

    kpress's `LocalPunct` was the case this rule was written for. It was a real
    `@font-face` whose source was `local("Georgia")`, so Blink reported it as a custom
    font -- a rule declared it -- and as the family `Georgia`, because that is what it
    opened. Trusting `isCustomFont` alone would have passed the reader's own serif as the
    page's.

    kpress ships those six glyphs now (`KPress Quotes`, `kpr-asj4`), so `Georgia` is no
    longer excused by a bead either, and both directions of the rule are here: a name the
    page never chose is a finding whether or not a `@font-face` declared it.
    """
    assert _unshipped([_face("Georgia", custom=True)]) == ["Georgia"]
    assert _unshipped([_face("KPress Quotes", custom=True)]) == []
    assert _unshipped([_face("Wingdings", custom=True)]) == ["Wingdings"]


def test_the_mono_kpress_now_ships_is_the_pages_and_the_hosts_own_is_not() -> None:
    """Inline code was the last role the reader's machine answered, and it is answered here.

    `Menlo` and `DejaVu Sans Mono` are the two names `ui-monospace` resolved to, on the
    developer's machine and on the runner that gates this probe, and both were excused by
    `kpr-v731` while kpress shipped no mono face. It ships one, the page declares it, and
    the excuse is gone -- which is the half of the change that matters, because an excused
    family is one the probe stops looking at: code that fell back to the platform stack
    would have passed in silence on both machines at once.

    Both directions, as everywhere else in this file: the shipped face is not a finding,
    and neither host name is spared by having been listed once.
    """
    assert _unshipped([_face("Planetaire Mono Text", custom=True)]) == []
    assert _unshipped([_face("Menlo", custom=False)]) == ["Menlo"]
    assert _unshipped([_face("DejaVu Sans Mono", custom=False)]) == ["DejaVu Sans Mono"]


def test_a_host_face_a_bead_is_removing_is_not_a_finding(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A guard can land before the fix it waits on, and this is that half on the screen side.

    Over a mapping this test supplies, because the page's own emptied on 2026-09-08 with
    `kpr-v731`. The mechanism outlives its entries: it is what let this probe ship while
    the mono, the list marker and the quotation marks were still the reader's, and it is
    what the next such wait will use. Testing it only through whatever happens to be
    listed deletes the coverage on the day the list empties -- the day the real page stops
    exercising it -- which is what happened here and is why this test is back.

    The twin of `test_a_pending_face_passes_and_is_reported_with_its_bead` on the PDF side,
    in this side's shapes: a platform font Blink names with its spaces in, reported by
    family rather than by PostScript name, and no `@font-face` behind it, since a pending
    face is one the page never declared.
    """
    monkeypatch.setattr(
        render_explainer_pdf, "EXPECTED_HOST_FONTS", {"Menlo": "kpr-v731"}, raising=True
    )
    assert _unshipped([_face("Menlo", custom=False)]) == []
    # The excuse is one family, not an amnesty: everything else still answers as itself.
    assert _unshipped([_face("DejaVu Sans Mono", custom=False)]) == ["DejaVu Sans Mono"]
    assert _unshipped([_face("Menlo", custom=False), _face("Wingdings", custom=True)]) == [
        "Wingdings"
    ]


def test_a_face_from_the_readers_machine_that_nobody_chose_is_a_finding() -> None:
    """The macOS system sans drew the three relation glyphs until they were given one.

    And the generic sans of the Linux runner that gates this probe beside it: that name
    was listed as pending once, which made the same regression a finding on the
    developer's machine and a pass on CI's.
    """
    assert _unshipped([_face(".SF NS", custom=False)]) == [".SF NS"]
    assert _unshipped([_face("DejaVu Sans", custom=False)]) == ["DejaVu Sans"]


def test_each_family_is_reported_once_however_many_faces_of_it_answer() -> None:
    """One answer carries a face per weight; a caption in two weights is one finding."""
    answer = [
        _face(".SF NS", custom=False, glyphs=9),
        _face(".SF NS", custom=False, glyphs=454),
        _face("PT Serif", custom=True),
    ]
    assert _unshipped(answer) == [".SF NS"]


def _element(
    name: str,
    node_id: int,
    *,
    text: str = "",
    children: list[dict[str, object]] | None = None,
    classes: str = "",
) -> dict[str, object]:
    """One element of a `DOM.getDocument` tree, with its attributes flattened as CDP's are."""
    kids: list[dict[str, object]] = list(children or [])
    if text:
        kids.insert(0, {"nodeType": 3, "nodeId": node_id + 500, "nodeValue": text})
    return {
        "nodeType": 1,
        "nodeName": name,
        "nodeId": node_id,
        "attributes": ["class", classes] if classes else [],
        "children": kids,
    }


def test_text_is_attributed_to_the_element_it_sits_in() -> None:
    """A finding names the run rather than the section it is in, which is where to look."""
    tree = _element(
        "DIV",
        1,
        classes="cert-page",
        children=[
            _element("P", 2, text="ordinary prose"),
            _element("P", 3, children=[_element("CODE", 4, text="minimal_verify.py")]),
        ],
    )
    found = _text_bearing(tree, [".cert-page"])
    assert [node for node, _ in found] == [2, 4]
    assert found[1][1].endswith("p[1] > code[0]")


def test_an_element_holding_only_whitespace_is_not_asked_about() -> None:
    """The tree carries the newlines between blocks, and they are drawn by nothing."""
    tree = _element("DIV", 1, children=[_element("P", 2, text="   \n  ")])
    assert _text_bearing(tree, ["body"]) == []


@pytest.mark.parametrize("name", ["SCRIPT", "STYLE", "TITLE", "DESC", "MATH", "math"])
def test_the_subtrees_that_are_not_the_pages_text_are_skipped(name: str) -> None:
    """Two of them are never drawn, and `math` is drawn where no reader can see it.

    KaTeX writes a MathML copy beside every expression it renders, clipped to a pixel for
    a screen reader. Blink still reports platform fonts for it -- Times and STIX Two Math,
    from the reader's machine, 121 times over on this page. `math` is spelled both ways
    because an HTML element reports its tag in capitals and a MathML one reports its own.
    """
    tree = _element("DIV", 1, children=[_element(name, 2, text="1 + 1 = 2")])
    assert _text_bearing(tree, ["body"]) == []


def test_an_element_with_both_its_own_text_and_children_is_asked_about_once() -> None:
    """A paragraph with a link in it is two runs, and the paragraph is one of them."""
    tree = _element("P", 1, text="see ", children=[_element("A", 2, text="the certificate")])
    assert [node for node, _ in _text_bearing(tree, ["body"])] == [1, 2]
