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

Nothing here launches a browser or reads a real font: the fixture writes stand-in files
of a few bytes, and the whole file runs in milliseconds.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from devtools.render_explainer_pdf import embedded_fonts, font_findings, outline_fonts
from devtools.sans_instances import (
    PRINT_FACES,
    Face,
    Requested,
    covered,
    gaps,
    generator,
    print_face_css,
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
    The family is the one kpress's print stack names first, so a face declared under any
    other name would be inert. And every source is inline, because the page is drawn
    from a `file://` URL with nothing to fetch from.
    """
    css = print_face_css(fonts=instances)
    assert css.startswith("@media print {\n")
    assert css.endswith("}\n")
    assert css.count("@font-face") == len(PRINT_FACES)
    assert css.count('font-family: "Source Sans 3";') == len(PRINT_FACES)
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


def _descriptor(number: int, name: str) -> bytes:
    """The descriptor a Type3 font points at, which is where its face is named."""
    return (
        f"\n{number} 0 obj\n<</Type /FontDescriptor\n/FontName /AAAAAA+{name}\n"
        f"/Flags 4>>\nendobj\n"
    ).encode()


#: The three readings the scan has to tell apart, as whole files.
OWNED_OUTLINES = _descriptor(9, "SourceSans3-Regular_wght") + _font(1, "Type3", 9)
HOST_OUTLINES = _descriptor(9, ".SFNS-Regular") + _font(1, "Type3", 9) + _font(2, "Type0")
NO_FONTS = b"%PDF-1.7\n1 0 obj\n<</Type /Page>>\nendobj\n"


def test_an_owned_face_drawn_as_outlines_fails() -> None:
    """The defect the instances exist to remove, named by the face it was drawn from."""
    findings = font_findings(OWNED_OUTLINES)
    assert len(findings) == 1
    assert "SourceSans3-Regular_wght" in findings[0]


def test_the_hosts_own_font_drawn_as_outlines_passes_and_is_still_reported() -> None:
    """Three characters on the page are in no face it ships, so the host draws them.

    Failing on those would pass on Linux and fail on a Mac, for a glyph nobody here
    chose. The scan still names them, which is how a fallback that grew becomes visible.
    """
    assert font_findings(HOST_OUTLINES) == []
    assert outline_fonts(HOST_OUTLINES) == [".SFNS-Regular"]
    assert embedded_fonts(HOST_OUTLINES) == ["AAAAAA+PTSerif-Regular"]


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
