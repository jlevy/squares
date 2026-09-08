"""The three rules that decide whether the printed sans is a font or a picture of one.

`sans_instances --check` answers the whole question, and it needs a browser, a rendered
page and eight instanced faces to do it. The rules underneath are small and total, and
they are the parts that fail quietly: a weight the set does not answer is a run that
falls back to the variable font, and a scan that reads nothing is a check that passes on
a file it never looked at.

So the three are exercised directly:

- the coverage rule, over the set the page requests and the one substitution it relies
  on. 400 is the case: the `@page` footer inherits it, and CSS font matching sends a
  request in [400, 500] up before it goes down, so it lands on 410.
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

# `_attribution` reads one node's cascade and is private because nothing outside the
# listing should decide what "set this weight" means. Tested directly rather than through
# a browser: the shape it reads is CDP's, and a fixture of it is exact where a page is not.
# pyright: reportPrivateUsage=false
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from nodejs_wheel import node

from devtools.render_explainer_pdf import (
    embedded_fonts,
    font_findings,
    host_font_bead,
    outline_fonts,
    provenance,
    shipped,
)
from devtools.sans_instances import (
    _PROBE,  # pyright: ignore[reportPrivateUsage]
    PRINT_FACES,
    PSEUDO_ELEMENTS,
    Declared,
    Face,
    Requested,
    _attribution,
    covered,
    distinct_sources,
    gaps,
    generator,
    postscript_prefix,
    print_face_css,
    print_family,
)

#: What the probe found on the rendered page, on 2026-09-07, weight and style only.
#: Every one of them has to be answered. 400 is not among them and is answered anyway:
#: the `@page` margin-box footer inherits it and no probe can reach a margin box.
REQUESTED: list[tuple[int, str]] = [
    (410, "italic"),
    (410, "normal"),
    (550, "normal"),
    (680, "normal"),
]

COVERAGE_CASES: list[tuple[str, int, str, bool]] = [
    ("a declared face, exactly", 410, "normal", True),
    ("a declared face in the other style", 680, "italic", True),
    ("400, which lands on 410 going up", 400, "normal", True),
    ("400 italic, which lands the same way", 400, "italic", True),
    ("a kpress token this page does not print at", 370, "normal", False),
    ("another one", 650, "normal", False),
    ("the weight the footnote controls left behind", 600, "normal", False),
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


def _font(
    number: int,
    subtype: str,
    descriptor: int | None = None,
    face: str = "AAAAAA+PTSerif-Regular",
) -> bytes:
    """A font dictionary in the shape Skia writes it: uncompressed, one object.

    `face` is the `/BaseFont` a Type0 dictionary names, which is where `embedded_fonts`
    reads a family from; a Type3 font has none, and is named through its descriptor.
    """
    reference = f"/FontDescriptor {descriptor} 0 R\n" if descriptor is not None else ""
    base = f"/BaseFont /{face}\n" if subtype == "Type0" else ""
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


def test_the_hosts_own_font_drawn_as_outlines_is_read_as_a_host_face() -> None:
    """The scan reads both dictionaries, and a Type3 says which face it was laid out in.

    `.SFNS-Regular` used to be waved through here: three characters were in no face the
    document carried, so the host drew them, and failing on that would have passed on
    Linux and failed on a Mac for a glyph nobody chose. The relation face closed that,
    and the provenance rule replaced the exemption -- what is tolerated now is a named
    list of families with a bead each, and `.SFNS-Regular` is not on it.
    """
    assert outline_fonts(HOST_OUTLINES) == [".SFNS-Regular"]
    assert embedded_fonts(HOST_OUTLINES) == ["AAAAAA+PTSerif-Regular"]
    unexpected, _ = provenance(HOST_OUTLINES)
    assert unexpected == [".SFNS-Regular"]


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


def test_a_face_the_page_ships_is_not_reported() -> None:
    """The families the document carries, by the names Chromium writes them under.

    The print instances are among them under the name kpress gives them, which is where
    the whole export's sans is: an allow-list that still watched for `SourceSans3` would
    have called every one of them a face off the reader's machine. `SourceSans3` stays
    listed beside it, because a run that missed the instances falls back to the variable
    face and the guard has to know that name too.
    """
    for name in (
        "PTSerif-Bold",
        "SourceSans3-Regular_wght",
        f"{postscript_prefix()}-410Italic",
        "KaTeX_Main-Bold",
        "LocalPunct",
        "KPressQuotes-Regular",
    ):
        assert shipped(name), name
    assert host_font_bead("PTSerif-Bold") is None
    # The screen probe's shape for the same faces: Blink answers with the instance a
    # variable face is at, which is neither the family nor a PostScript name.
    assert shipped("Source Sans 3 ExtraLight")
    assert shipped("PT Serif")


def test_the_atlas_figures_helvetica_is_the_documented_exception() -> None:
    """Page 3's labels are baked into its own SVG by `build_known_best_atlas`.

    Allowed rather than pending: no bead removes it, because the figure is generated by
    another pipeline, is published on its own, and stays as it is by the owner's decision.
    """
    assert shipped("Helvetica-BoldOblique")
    assert host_font_bead("Helvetica-BoldOblique") is None
    # The same figure drawn on a Linux runner, where fontconfig answers Helvetica with
    # Liberation Sans, and on Windows, where the stack falls to Arial.
    assert shipped("LiberationSans-Bold")
    assert shipped("Arial-BoldMT")
    assert host_font_bead("LiberationSans-BoldItalic") is None
    assert not shipped("DejaVuSans-Bold")


def test_the_exception_covers_three_families_and_not_their_namesakes() -> None:
    """A listed name is that family's faces, not every family whose name starts with it.

    Bare `startswith` gave each entry a family tree, and all three of these are fonts a
    machine really has: Helvetica Neue ships with macOS, Arial Unicode MS with Office,
    Liberation Sans Narrow with the Liberation set the runner draws the atlas in. None of
    them is the figure's face, so a page that drew from one would be a finding.

    The rule is the host's names only. A name the page owns stays a prefix, because the
    page owns everything under it and the probes answer in two shapes -- `KaTeX_Size2`
    puts the style in the family, and Blink names a variable instance rather than a face.
    """
    assert not shipped("HelveticaNeue-Bold")
    assert not shipped("ArialUnicodeMS")
    assert not shipped("LiberationSansNarrow")
    assert shipped("Helvetica-BoldOblique")
    assert shipped("KaTeX_Size2-Regular")


def test_the_generic_host_sans_is_a_finding_on_both_platforms() -> None:
    """The face a relation face that stopped loading comes back as, either side of CI.

    macOS draws it as outline paths, because the system sans is variable; a Linux runner
    embeds DejaVu Sans, and `pages.yml` runs both halves of the guard there. Listing the
    Linux name as pending is what made the guard weakest on the machine that gates it,
    so the assertion is that neither name is shipped and neither is waiting on a bead.
    """
    for family in (".SFNS-Regular", ".SF NS", "DejaVuSans-Bold", "DejaVu Sans"):
        assert not shipped(family), family
        assert host_font_bead(family) is None, family


@pytest.mark.parametrize(
    ("family", "bead"),
    [
        ("Menlo-Regular", "kpr-v731"),
        ("DejaVuSansMono", "kpr-v731"),
        ("DejaVu Sans Mono", "kpr-v731"),
    ],
)
def test_a_host_face_a_bead_is_removing_is_pending_rather_than_a_failure(
    family: str, bead: str
) -> None:
    """The one role kpress has not covered yet, and the same role on the Linux runner.

    Spaces come out before the match, so one mapping answers a PDF's `DejaVuSansMono`
    and a browser's `DejaVu Sans Mono`, and a style suffix answers under its family.

    `Georgia` and `LiberationSerif` were here too until `kpr-2tmj` and `kpr-asj4` landed:
    the list marker is drawn in CSS now rather than set as U+25AA, and the quotation marks
    come from the shipped `KPress Quotes`. Neither is pending any more, and
    `test_a_face_kpress_now_ships_is_no_longer_pending` is what says so.
    """
    assert not shipped(family)
    assert host_font_bead(family) == bead


@pytest.mark.parametrize("family", ["Georgia", "LiberationSerif-Italic"])
def test_a_face_kpress_now_ships_is_no_longer_pending(family: str) -> None:
    """A name off the pending list is a face the guard starts looking at again.

    Leaving it listed would be the more comfortable mistake and the worse one: an entry
    here is a family `--check` stops reporting, so a quotation mark that went back to the
    reader's own serif would pass in silence.
    """
    assert not shipped(family)
    assert host_font_bead(family) is None


def test_a_family_no_bead_expects_fails_the_check_and_is_named() -> None:
    """The guard's whole point: a glyph from the reader's machine that nobody chose."""
    stranger = _descriptor(9, "Wingdings") + _font(1, "Type3", 9) + _font(2, "Type0")
    unexpected, pending = provenance(stranger)
    assert unexpected == ["Wingdings"]
    assert pending == {}
    findings = font_findings(stranger)
    assert len(findings) == 1
    assert "Wingdings" in findings[0]


def test_the_pending_faces_pass_and_are_reported_with_their_beads() -> None:
    """`--check` has to pass with these present, or the guard cannot land before them.

    Both are written the way the export carries them: a descriptor with the program in
    it, and a font dictionary naming the subset. `embedded_fonts` takes a `/BaseFont`
    only once its descriptor is found to carry a `/FontFile*`, so a bare name in the
    file would be read as no face at all rather than as the host face it is.
    """
    waiting = (
        _descriptor(7, "Menlo-Regular", program=True)
        + _font(1, "Type0", 7, face="TAAAAA+Menlo-Regular")
        + EMBEDDED_SERIF
    )
    unexpected, pending = provenance(waiting)
    assert unexpected == []
    assert pending == {"Menlo-Regular": "kpr-v731"}
    assert font_findings(waiting) == []


def test_an_outline_font_from_the_host_is_the_same_finding_as_an_embedded_one() -> None:
    """Which of the two a host face becomes depends only on whether it is variable.

    `.SFNS-Regular` is how the three relation glyphs left this page before they were
    given a shipped face: drawn as paths, because the macOS system sans is a variable
    font and Chromium embeds one only at its default position.
    """
    outlined = _descriptor(9, ".SFNS-Regular") + _font(1, "Type3", 9) + _font(2, "Type0")
    unexpected, _ = provenance(outlined)
    assert unexpected == [".SFNS-Regular"]
    assert any(".SFNS-Regular" in finding for finding in font_findings(outlined))


def test_the_weight_listing_reports_one_row_per_source_and_not_per_element() -> None:
    """Two elements at one weight from two rules is the finding the listing is for.

    The caption label and the chip were both the sans at 550 and only one of them was a
    caption; a listing that showed the first element of each combination would have said
    the medium had one source when it had two.
    """
    row: Declared = {
        "family": print_family(),
        "weight": 550,
        "style": "normal",
        "runs": 12,
        "seen": [
            {"marker": 0, "path": "a.chip[0]", "source": ".doc-links .chip { 550 }"},
            {"marker": 1, "path": "a.chip[1]", "source": ".doc-links .chip { 550 }"},
            {"marker": 2, "path": "strong[0]", "source": ".kpress-figcaption strong { 550 }"},
        ],
    }
    assert [sample["path"] for sample in distinct_sources(row)] == ["a.chip[0]", "strong[0]"]


def test_a_weight_set_through_a_token_is_reported_as_the_token() -> None:
    """What `getComputedStyle` cannot answer, and the reason the listing goes through CDP.

    The cascade is read weakest origin first, so the last declaration is the one that
    won; CDP repeats the winner with `disabled` unset, and those duplicates collapse.
    """
    styles = {
        "matchedCSSRules": [
            {
                "rule": {
                    "selectorList": {"text": ".kpress b, .kpress strong"},
                    "style": {"cssProperties": [{"name": "font-weight", "value": "650"}]},
                }
            },
            {
                "rule": {
                    "selectorList": {"text": ".credits strong"},
                    "style": {
                        "cssProperties": [
                            {
                                "name": "font-weight",
                                "value": "var(--kpress-font-weight-sans-bold)",
                                "disabled": False,
                            }
                        ]
                    },
                }
            },
        ]
    }
    assert _attribution(styles) == ".credits strong { var(--kpress-font-weight-sans-bold) }"


def test_a_weight_no_rule_sets_is_reported_as_inherited_or_unset() -> None:
    """Most of this page's text is set by a token on a wrapper, not on the run itself."""
    inherited = {
        "inherited": [
            {
                "matchedCSSRules": [
                    {
                        "rule": {
                            "selectorList": {"text": ".cert-page :is(.credits, .panel)"},
                            "style": {
                                "cssProperties": [
                                    {
                                        "name": "font-weight",
                                        "value": "var(--cert-font-weight-sans-light)",
                                    }
                                ]
                            },
                        }
                    }
                ]
            }
        ]
    }
    assert _attribution(inherited).endswith("(inherited)")
    assert "--cert-font-weight-sans-light" in _attribution(inherited)
    assert _attribution({}) == "unset (the initial 400)"


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
