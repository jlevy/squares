"""The three rules that decide whether the printed sans is a font or a picture of one.

`sans_instances --check` answers the whole question, and it needs a browser, a rendered
page and eight instanced faces to do it. The rules underneath are small and total, and
they are the parts that fail quietly: a weight the set does not answer is a run that
falls back to the variable font, and a scan that reads nothing is a check that passes on
a file it never looked at.

So the three are exercised directly:

- the coverage rule, over the set the page requests and the one substitution it relies
  on. 400 is the case: `.rel` names it and the `@page` footer inherits it, and CSS font
  matching sends a request in [400, 500] up before it goes down, so both land on 410.
- `print_face_css`, over stand-in files, for the shape `render_explainer_pdf` injects:
  one `@media print` block, the family the print stack names, every face's bytes inline.
- the PDF font scan, over synthetic dictionaries in the shapes Chromium writes. Both
  failures are here -- an owned face drawn as outlines, and a file the scan can see no
  font in at all -- because the second is the one that would otherwise look like a pass.
  The scan's two ways of reading the wrong thing are here beside them: a face the file
  only names, and an object number that also occurs inside a stream.
- the probe's generated-content rule, run as the shipped JavaScript under node against
  the `content` values a browser computes. Type on this page comes from pseudo-elements
  as well as from text nodes -- `li.kpress-footnote-item::before` numbers the footnotes
  -- and this is the rule that decides which of those count as a request.

Nothing here launches a browser or reads a real font: the fixture writes stand-in files
of a few bytes, and the whole file runs in milliseconds.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from nodejs_wheel import node

from devtools.render_explainer_pdf import embedded_fonts, font_findings, outline_fonts
from devtools.sans_instances import (
    _PROBE,  # pyright: ignore[reportPrivateUsage]
    PRINT_FACES,
    PSEUDO_ELEMENTS,
    Face,
    Requested,
    covered,
    gaps,
    generator,
    postscript_prefix,
    print_face_css,
    print_family,
)

#: What the probe found on the rendered page, on 2026-09-07, weight and style only.
#: Every one of them has to be answered, and 400 is answered by 410.
REQUESTED: list[tuple[int, str]] = [
    (400, "normal"),
    (410, "italic"),
    (410, "normal"),
    (550, "normal"),
    (600, "normal"),
    (680, "normal"),
]

COVERAGE_CASES: list[tuple[str, int, str, bool]] = [
    ("a declared face, exactly", 410, "normal", True),
    ("a declared face in the other style", 680, "italic", True),
    ("400, which lands on 410 going up", 400, "normal", True),
    ("400 italic, which lands the same way", 400, "italic", True),
    ("a kpress token this page does not print at", 370, "normal", False),
    ("another one", 650, "normal", False),
    ("a weight below the substitution", 300, "normal", False),
    ("a style no instance carries", 410, "oblique 14deg", False),
]


@pytest.mark.parametrize(
    ("weight", "style", "answered"),
    [pytest.param(w, s, a, id=name) for name, w, s, a in COVERAGE_CASES],
)
def test_only_a_weight_an_instance_draws_counts_as_covered(
    weight: int, style: str, *, answered: bool
) -> None:
    """The substitution is one entry wide, and everything else needs its own face.

    A weight outside the set is not a near miss. The browser answers it from the
    variable font, and that run goes back to Type3 outline paths while every other run
    on the page is set in a font: the mixed case, which reads worse than the uniform one
    the whole change replaced.
    """
    assert covered(weight, style) is answered


def test_the_declared_set_answers_everything_the_page_asks_for() -> None:
    """The set against the requests the probe recorded, without launching a browser."""
    rows: list[Requested] = [
        {"weight": weight, "style": style, "path": "p[0]"} for weight, style in REQUESTED
    ]
    assert gaps(rows) == []


def test_a_request_outside_the_set_is_reported_with_the_element_that_makes_it() -> None:
    """A gap names where to look. A bare weight would send a reader through the page."""
    rows: list[Requested] = [
        {"weight": 410, "style": "normal", "path": "div.hero[2] > span[0]"},
        {"weight": 370, "style": "normal", "path": "nav.tabs[0] > button[1]"},
    ]
    assert [row["path"] for row in gaps(rows)] == ["nav.tabs[0] > button[1]"]


@pytest.fixture
def instances(tmp_path: Path) -> Path:
    """A stand-in file per declared face. Any bytes will do; nothing here parses a font."""
    for weight, style in PRINT_FACES:
        name = generator().instance_name(weight, style)
        (tmp_path / name).write_bytes(f"{weight}-{style}-stand-in".encode())
    return tmp_path


def test_the_injected_css_is_one_print_block_of_self_contained_faces(instances: Path) -> None:
    """The shape `render_explainer_pdf` adds to the loaded page, and nothing else.

    Three properties, and each is load-bearing. `@media print` is what keeps the screen
    on the variable font when the same rules are added to a page that is not printing.
    The family is the one kpress's print stack names first, asked of kpress rather than
    written out here, so a face declared under any other name would be inert. And every
    source is inline, because the page is drawn from a `file://` URL with nothing to
    fetch from.
    """
    css = print_face_css(fonts=instances)
    assert css.startswith("@media print {\n")
    assert css.endswith("}\n")
    assert css.count("@font-face") == len(PRINT_FACES)
    assert css.count(f'font-family: "{print_family()}";') == len(PRINT_FACES)
    assert css.count('url("data:font/woff2;base64,') == len(PRINT_FACES)
    assert '.woff2")' not in css


@pytest.mark.parametrize("face", list(PRINT_FACES), ids=lambda f: f"{f[0]}-{f[1]}")
def test_every_declared_face_reaches_the_page_at_its_own_weight(
    face: Face, instances: Path
) -> None:
    """A rule per face, at the weight and style it was instanced at."""
    css = print_face_css(fonts=instances)
    assert f"font-weight: {face[0]};" in css
    assert f"font-style: {face[1]};" in css


def test_a_missing_instance_stops_the_export(instances: Path) -> None:
    """Not a silently thinner page: without the file, the run falls back to outlines."""
    (instances / generator().instance_name(*PRINT_FACES[0])).unlink()
    with pytest.raises(SystemExit, match=re.escape("run `python -m devtools.sans_instances`")):
        print_face_css(fonts=instances)


def _font(number: int, subtype: str, descriptor: int | None = None) -> bytes:
    """A font dictionary in the shape Skia writes it: uncompressed, one object."""
    reference = f"/FontDescriptor {descriptor} 0 R\n" if descriptor is not None else ""
    base = "/BaseFont /AAAAAA+PTSerif-Regular\n" if subtype == "Type0" else ""
    return (
        f"\n{number} 0 obj\n<</Type /Font\n/Subtype /{subtype}\n{base}{reference}>>\nendobj\n"
    ).encode()


def _descriptor(number: int, name: str, *, program: bool = False) -> bytes:
    """The descriptor a font points at, which is where its face is named.

    `program` is the `/FontFile2` that makes the descriptor an embedding rather than a
    reference to a face the reader is expected to own. A Type3 font never has one -- its
    glyphs are drawing procedures -- which is why the default is off.
    """
    embedded = "/FontFile2 99 0 R\n" if program else ""
    return (
        f"\n{number} 0 obj\n<</Type /FontDescriptor\n/FontName /AAAAAA+{name}\n"
        f"{embedded}/Flags 4>>\nendobj\n"
    ).encode()


#: The readings the scan has to tell apart, as whole files. The first two are both the
#: sans in outlines, one step apart: the variable face is the print run that never
#: reached the instances at all, and the instance is one Chromium declined to embed
#: even so. The instance's name comes from kpress, through `postscript_prefix`, so the
#: scan and the case move together when the family is renamed.
OWNED_OUTLINES = _descriptor(9, "SourceSans3-Regular_wght") + _font(1, "Type3", 9)
INSTANCE_OUTLINES = _descriptor(9, f"{postscript_prefix()}-410") + _font(1, "Type3", 9)
EMBEDDED_SERIF = _descriptor(8, "PTSerif-Regular", program=True) + _font(2, "Type0", 8)
REFERENCED_SERIF = _descriptor(8, "PTSerif-Regular") + _font(2, "Type0", 8)
HOST_OUTLINES = _descriptor(9, ".SFNS-Regular") + _font(1, "Type3", 9) + EMBEDDED_SERIF
NO_FONTS = b"%PDF-1.7\n1 0 obj\n<</Type /Page>>\nendobj\n"

#: An object header at a line start inside a compressed stream, with the number the
#: Type3 font's descriptor reference names. Flate output is arbitrary bytes and can
#: hold this; what it cannot hold and still be a decoy is `/Type /FontDescriptor`.
DECOY = (
    b"\n7 0 obj\n<</Length 48>>\nstream\n"
    b"\n9 0 obj\n<</FontName /AAAAAA+Decoy>>\nendobj\n"
    b"endstream\nendobj\n"
)


def test_an_owned_face_drawn_as_outlines_fails() -> None:
    """The defect the instances exist to remove, named by the face it was drawn from."""
    findings = font_findings(OWNED_OUTLINES)
    assert len(findings) == 1
    assert "SourceSans3-Regular_wght" in findings[0]


def test_a_print_instance_drawn_as_outlines_fails_too() -> None:
    """The scan follows the instances' own name, not only the face they come from.

    They are declared under a family of kpress's own, so the PostScript name in the PDF
    is nothing like `SourceSans3`; a scan that watched only for the original would have
    waved the renamed instances through and reported a clean file.
    """
    findings = font_findings(INSTANCE_OUTLINES)
    assert len(findings) == 1
    assert f"{postscript_prefix()}-410" in findings[0]


def test_the_hosts_own_font_drawn_as_outlines_passes_and_is_still_reported() -> None:
    """Three characters on the page are in no face it ships, so the host draws them.

    Failing on those would pass on Linux and fail on a Mac, for a glyph nobody here
    chose. The scan still names them, which is how a fallback that grew becomes visible.
    """
    assert font_findings(HOST_OUTLINES) == []
    assert outline_fonts(HOST_OUTLINES) == [".SFNS-Regular"]
    assert embedded_fonts(HOST_OUTLINES) == ["AAAAAA+PTSerif-Regular"]


def test_a_face_the_file_only_names_is_not_reported_as_embedded() -> None:
    """`/BaseFont` names a face; `/FontFile2` is what says the file carries it.

    The two dictionaries here are identical but for the font program, and the whole
    claim this scan backs is that the page ships its faces. Counting a referenced font
    would have `--check` announce as embedded a face the reader has to supply.
    """
    assert embedded_fonts(EMBEDDED_SERIF) == ["AAAAAA+PTSerif-Regular"]
    assert embedded_fonts(REFERENCED_SERIF) == []


def test_an_object_header_inside_a_stream_is_not_mistaken_for_the_descriptor() -> None:
    """The descriptor is resolved by type, not by the first matching header.

    Compressed streams carry arbitrary bytes, and `9 0 obj` at a line start is a
    sequence they can hold. Reading one would name the outline font after a decoy: a
    failure the file does not have, on a check whose findings have to be trusted.
    """
    file = DECOY + _descriptor(9, "SourceSans3-Regular_wght") + _font(1, "Type3", 9)
    assert outline_fonts(file) == ["SourceSans3-Regular_wght"]


def test_the_current_definition_of_a_descriptor_wins_over_the_superseded_one() -> None:
    """A file written in increments carries the old object first and the new one after."""
    file = (
        _descriptor(9, "Superseded-Regular")
        + _font(1, "Type3", 9)
        + _descriptor(9, "SourceSans3-Regular_wght")
    )
    assert outline_fonts(file) == ["SourceSans3-Regular_wght"]


def test_a_file_the_scan_can_see_no_font_in_is_a_failure() -> None:
    """The shortcut's cost, stated as a finding.

    The scan reads font dictionaries out of the bytes because Chromium leaves them
    uncompressed. A writer that started compressing them would show a file with no
    Type3 fonts anywhere, which is exactly what a clean file looks like.
    """
    findings = font_findings(NO_FONTS)
    assert len(findings) == 1
    assert "cannot see font dictionaries" in findings[0]


def test_an_outline_font_whose_face_cannot_be_read_counts_as_ours() -> None:
    """No descriptor, no attribution, no pass: an unreadable Type3 is not waved through."""
    findings = font_findings(_font(1, "Type3") + _font(2, "Type0"))
    assert len(findings) == 1


def probe_function(name: str) -> str:
    """One helper's shipped source, so what runs here is what runs in the browser."""
    source = re.search(rf"  function {name}\([^)]*\) \{{.*?\n  \}}", _PROBE, re.DOTALL)
    assert source is not None, f"{name} is no longer a helper of its own in the probe"
    return source.group() + "\n"


def draws(content: str) -> bool:
    """Run the shipped generated-content rule under node, without browser setup."""
    script = (
        probe_function("draws")
        + f"\nconsole.log(JSON.stringify(draws({json.dumps(content)})));\n"
    )
    completed = node(
        ["-"], return_completed_process=True, input=script, capture_output=True, text=True
    )
    assert completed.returncode == 0, completed.stderr
    return bool(json.loads(completed.stdout))


#: What `getComputedStyle(el, pseudo).content` returns, and whether it puts type on the
#: page. The counter is the case the probe was extended for: kpress numbers footnote
#: items with `li.kpress-footnote-item::before`, a sans run in no text node, and a walk
#: over text alone left the weight it asks for outside `--check` entirely.
CONTENT_CASES: list[tuple[str, str, bool]] = [
    ("a footnote counter, which is the case this exists for", 'counter(footnote) ". "', True),
    ("a literal string", '"Figure "', True),
    ("an attribute", "attr(data-label)", True),
    ("no pseudo-element at all", "none", False),
    ("the default, which draws the element's own marker", "normal", False),
    ("an empty double-quoted string: a rule or a spacer", '""', False),
    ("an empty single-quoted one", "''", False),
    ("nothing computed", "", False),
]


@pytest.mark.parametrize(
    ("content", "typeset"),
    [pytest.param(c, t, id=name) for name, c, t in CONTENT_CASES],
)
def test_only_generated_content_that_sets_type_counts_as_a_request(
    content: str, *, typeset: bool
) -> None:
    """An empty box asks for no face, and counting it would declare an instance for it.

    The other direction is the one that matters more: a pseudo-element that does set
    type asks for a weight like any run, and if the set does not answer it the PDF draws
    it from the variable font as outline paths -- invisibly, because nothing walks it.
    """
    assert draws(content) is typeset


def test_the_probe_reads_every_pseudo_element_that_can_carry_type() -> None:
    """The three the page can put a face on, handed in rather than spelled in the JS."""
    assert PSEUDO_ELEMENTS == ("::before", "::after", "::marker")
    assert "getComputedStyle(el, pseudo)" in _PROBE
