# pyright: reportPrivateUsage=false
"""The PDF publication comparison, failure evidence, and required-image wait.

The check itself needs a browser, a rendered page and about nine seconds a render, and
it lives in the Pages job. What is here is the part that only matters on the day it
fails, and that therefore has to be right before then: a disagreement names its object
or outside-object section without guessing a cause, the exact stored artifact and its
HTML receipt take part in the comparison, and an image that cannot become drawable
refuses capture. A failed comparison retains its raw pair when diagnosis is requested.

On 2026-09-10 this check failed on main for the first time, said `786119 then 786117
bytes` and nothing else, and the renders were gone. The second occurrence, on PR 218's
run 35764316182, arrived with its object named and its pair retained, and that is what
identified the cause: the page re-renders math from its own print handlers, inside the
`page.pdf()` call that is drawing it. `_draw_reproduced` and the cases for it below are
what that bought. The publication job also checked a later pair of draws while shipping
an earlier file; agreement between the later pair could not validate that artifact. The
CLI-to-function join is the one D-488 was made of: a count that argparse accepts and
nothing forwards looks exactly like a count that works. The image wait initially
discarded every decode rejection, which could let two PDFs agree on the same absent
figure. D-509 is the page load deciding one glyph's placement, so the artifact check may
draw up to four loads and the cases below pin when that passes and when it still refuses;
its CI logs named object 144 and nothing readable, so a Flate difference is inflated and
its first differing line quoted.

Nothing here launches a browser. `render_pdf_bytes` is replaced with synthetic
documents in the shapes Chromium writes, and the exact image-wait, settlement and math
trace probes run under Node against small stand-ins, in the scripts under
`tests/node/render_n11_lower_bounds_explainer_pdf/`. The file belongs in the quick lane.
"""

from __future__ import annotations

import hashlib
import json
import zlib
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING, cast

import pytest
from nodejs_wheel import node

from devtools import render_n11_lower_bounds_explainer_pdf as pdf

if TYPE_CHECKING:
    from collections.abc import Sequence

    from playwright.sync_api import Page

NODE = Path(__file__).resolve().parent / "node" / "render_n11_lower_bounds_explainer_pdf"


def _run_node(script: str, *arguments: str) -> None:
    completed = node(
        [str(NODE / script), *arguments],
        return_completed_process=True,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr


#: A document with one object, in the shape the writer emits: the header at a line start,
#: the dictionary declaring what the object is, and a body that the cases below vary.
_HEADER = b"%PDF-1.4\n"


def _run_image_wait(case: str) -> None:
    """Run the exact browser-side image wait against small image-element stand-ins."""
    _run_node("image-wait.mjs", case)


def test_the_image_wait_forces_lazy_images_eager_before_decode() -> None:
    _run_image_wait("lazy-images-go-eager")


def test_a_decode_rejection_is_safe_only_for_an_available_image() -> None:
    """A changed request may reject while its replacement is already drawable."""
    _run_image_wait("rejection-of-an-available-image")


def test_an_image_without_a_drawable_current_request_refuses_the_render() -> None:
    _run_image_wait("no-drawable-current-request")


def _pages(count: int) -> bytes:
    """A render carrying the page count `check` insists on.

    The count is exercised rather than bypassed, because bypassing it is what made this
    file's first version pass on a base where `check` had no page assertion and fail the
    moment it did: a fake render is only a fake of the gates it actually reaches. The
    writer puts `/Type /Page` at the end of a line, which is what `check` counts.
    """
    return b"".join(
        b"%d 0 obj\n<< /Type /Page\n/Contents %d 0 R >>\nendobj\n" % (number, number + 1)
        for number in range(1, count + 1)
    )


def _document(body: bytes, *, number: int = 1, declared: bytes = b"/Type /Page") -> bytes:
    return b"%s%d 0 obj\n<< %s >>\nstream\n%s\nendstream\nendobj\n" % (
        _HEADER,
        number,
        declared,
        body,
    )


def test_a_difference_is_reported_with_the_object_it_happened_in() -> None:
    """The realistic failure: a coordinate that settled differently in its last digits."""
    report = pdf._difference(_document(b"0.35294 0.11764 rg"), _document(b"0.35294 0.1176 rg"))
    assert "object 1, Page" in report
    assert "0.11764" in report
    assert "0.1176 rg" in report
    assert "first difference at byte" in report


def test_the_object_is_named_by_its_subtype_rather_than_its_type() -> None:
    """`/Type /XObject` would not tell a redrawn figure from the form beside it, and the
    writer puts it first, so a single leftmost match would read the wrong one."""
    report = pdf._difference(
        _document(b"aaa", number=417, declared=b"/Type /XObject /Subtype /Image"),
        _document(b"aab", number=417, declared=b"/Type /XObject /Subtype /Image"),
    )
    assert "object 417, Image" in report


@pytest.mark.parametrize("prefix", [b"", _document(b"0.5 rg")], ids=["first", "later"])
def test_a_difference_in_an_object_header_belongs_to_that_object(prefix: bytes) -> None:
    report = pdf._difference(
        prefix + _document(b"aaa", number=417, declared=b"/Type /XObject /Subtype /Image"),
        prefix + _document(b"aaa", number=418, declared=b"/Type /XObject /Subtype /Image"),
    )
    assert "in object 417, Image:" in report


def test_a_short_untyped_object_does_not_borrow_the_next_object_type() -> None:
    """Measured on the real document: of its 1160 objects, 33 declare no type of their own
    while sitting inside the 400-byte window, and an unbounded read labelled every one of
    them with a later object's. `<< /ca 1 /BM /Normal >>` was reported as a Link."""
    alpha = b"3 0 obj\n<< /ca %s /BM /Normal >>\nendobj\n"
    link = (
        b"4 0 obj\n<< /Type /Annot /Subtype /Link"
        b" /Rect [320.24 621.00 389.24 639.00] >>\nendobj\n"
    )
    report = pdf._difference(_HEADER + (alpha % b"1") + link, _HEADER + (alpha % b".9") + link)
    assert "in object 3:" in report


def test_an_untyped_object_does_not_borrow_a_type_from_its_stream() -> None:
    """A stream payload is data, even when its bytes happen to parse like a PDF name."""
    prefix = b"7 0 obj\n<< /Length 18 >>\nstream\n/Type /Link value="
    suffix = b"\nendstream\nendobj\n"
    report = pdf._difference(_HEADER + prefix + b"a" + suffix, _HEADER + prefix + b"b" + suffix)
    assert "in object 7:" in report
    assert "object 7, Link" not in report


def test_a_cross_reference_difference_is_not_assigned_to_the_last_object() -> None:
    document = _document(b"0.5 rg")
    first = document + b"xref\n0 2\n0000000000 65535 f\n0000000010 00000 n\n"
    second = document + b"xref\n0 2\n0000000000 65535 f\n0000000011 00000 n\n"
    report = pdf._difference(first, second)
    assert "in the cross-reference table" in report
    assert "in object 1" not in report


def test_a_trailer_difference_is_not_assigned_to_the_last_object() -> None:
    document = _document(b"0.5 rg") + b"xref\n0 2\ntrailer\n"
    report = pdf._difference(
        document + b"<< /Size 2 /Root 1 0 R /ID [<aaa>] >>\n",
        document + b"<< /Size 2 /Root 1 0 R /ID [<aab>] >>\n",
    )
    assert "in the trailer" in report
    assert "in object 1" not in report


def test_an_inter_object_difference_is_not_assigned_to_the_previous_object() -> None:
    first = _document(b"0.5 rg") + b"% alignment a\n" + _document(b"0.4 rg", number=2)
    second = _document(b"0.5 rg") + b"% alignment b\n" + _document(b"0.4 rg", number=2)
    report = pdf._difference(first, second)
    assert "between PDF objects" in report
    assert "in object 1" not in report


def test_a_difference_before_the_first_object_names_the_file_header() -> None:
    report = pdf._difference(_HEADER + b"a", _HEADER + b"b")
    assert "in the file header" in report


@pytest.mark.parametrize("trailing", [False, True], ids=["shortened", "appended"])
def test_an_exact_prefix_is_reported_without_assigning_a_cause(*, trailing: bool) -> None:
    """A prefix can come from either missing bytes or additional trailing bytes."""
    whole = _document(b"0.5 rg")
    first, second = (
        (whole, whole + b"% trailing comment\n") if trailing else (whole[:-10], whole)
    )
    report = pdf._difference(first, second)
    assert f"first {len(first)} bytes" in report
    assert "exact prefix" in report
    assert "cut short" not in report


def _content(text: bytes, *, number: int = 144, compress: bool = True) -> bytes:
    """A page content stream in the shape Chromium's Skia writer emits: Flate, with
    `stream` after the dictionary's `>>` on the same line rather than on its own."""
    payload = zlib.compress(text) if compress else text
    return (
        b"%s%d 0 obj\n<</Filter /FlateDecode\n/Length %d>> stream\n%s\nendstream\nendobj\n"
        % (
            _HEADER,
            number,
            len(payload),
            payload,
        )
    )


#: Three lines of a KaTeX run, the middle one D-509's `≥`: y 18560.219 on one load and
#: 18560 on another, with the glyph it places on the line after.
_GLYPH = b"BT\n/F7 18.08 Tf\n1 0 0 -1 412.5 %s Tm\n<0021> Tj\nET"


def test_a_flate_difference_names_the_first_decoded_line_that_moved() -> None:
    """D-509's CI logs said `object 144` and quoted deflate output; the moved `Tm` line
    took an artifact download to read. The decoded line is what the log should carry."""
    settled = _content(_GLYPH % b"18560.219")
    moved = _content(_GLYPH % b"18560")
    report = pdf._difference(settled, moved)
    assert "in object 144:" in report
    assert "first differs at line 3 of 5" in report
    assert "b'1 0 0 -1 412.5 18560.219 Tm' against b'1 0 0 -1 412.5 18560 Tm'" in report
    assert "before b'<0021> Tj'" in report


def test_a_difference_in_the_stream_length_still_reaches_the_decoded_line() -> None:
    """Run 36317430319: Length 5237 against 5235. The first differing byte was in the
    dictionary, ahead of any stream byte, and the decoded line is still what moved."""
    settled = _content(_GLYPH % b"18560.219" + b"\n" + b"0 0 1 rg\n" * 40)
    moved = _content(_GLYPH % b"18560" + b"\n" + b"0 0 1 rg\n" * 40)
    report = pdf._difference(settled, moved)
    offset = int(report.split("first difference at byte ", 1)[1].split(",", 1)[0])
    assert settled.index(b"/Length") < offset < settled.index(b"stream"), report
    assert "18560.219 Tm' against b'1 0 0 -1 412.5 18560 Tm'" in report


def test_a_stream_that_will_not_inflate_is_reported_as_such() -> None:
    report = pdf._difference(
        _content(b"garbage one", compress=False), _content(b"garbage two", compress=False)
    )
    assert "in object 144:" in report
    assert "does not inflate" in report


def test_an_uncompressed_stream_gets_no_decoded_report() -> None:
    report = pdf._difference(_document(b"0.5 rg"), _document(b"0.6 rg"))
    assert "inflate" not in report


def test_a_skia_stream_payload_does_not_lend_its_object_a_type() -> None:
    """The writer's own shape, `>> stream` on one line: the declaration scan has to stop
    there too, or payload bytes that read like `/Type /Link` name the object."""
    prefix = b"7 0 obj\n<</Length 18>> stream\n/Type /Link value="
    suffix = b"\nendstream\nendobj\n"
    report = pdf._difference(_HEADER + prefix + b"a" + suffix, _HEADER + prefix + b"b" + suffix)
    assert "in object 7:" in report


def test_two_renders_that_agree_are_not_given_an_invented_difference() -> None:
    """Unreachable from `check`, which only asks about renders it has found to differ.
    Reported honestly anyway: the prefix message would otherwise announce an unequal
    length on two identical files, and send the reader after a bug that is not there."""
    report = pdf._difference(_document(b"0.5 rg"), _document(b"0.5 rg"))
    assert "no byte differs" in report
    assert "cut short" not in report


class _Printer:
    """A page that prints a scripted sequence and answers the two watch probes.

    It also pins the option set, because `_draw_reproduced` compares draws against each
    other: a repeat taken at a different paper size would disagree with the draw before it
    for a reason that has nothing to do with the page moving.
    """

    def __init__(self, documents: Sequence[bytes]) -> None:
        self.documents = list(documents)
        self.drawn: list[bytes] = []
        self.settlements = 0

    def evaluate_handle(self, script: str) -> object:
        assert script == pdf._PRINT_ACTIVITY
        return object()

    def pdf(self, **options: object) -> bytes:
        assert options == {
            "print_background": True,
            "prefer_css_page_size": True,
            "tagged": True,
            "outline": True,
        }
        drawn = self.documents[min(len(self.drawn), len(self.documents) - 1)]
        self.drawn.append(drawn)
        return drawn

    def evaluate(self, script: str, argument: object = None) -> dict[str, object] | None:
        if script == pdf._PRINT_ACTIVITY_REPORT:
            assert isinstance(argument, dict)
            assert "watch" in argument
            return {
                "quiet": False,
                "font_status_when_installed": "loaded",
                "changes": 24,
                "truncated": True,
                "records": [
                    {
                        "at_ms": 27.0,
                        "kind": "attributes",
                        "where": "dl.kv>dd>span.squares-math-variant",
                        "detail": "style",
                    }
                ],
            }
        assert script in (pdf.FONTS_READY, pdf.SETTLED)
        self.settlements += 1
        return None


def _drawn(printer: _Printer, math_trace: dict[str, object] | None = None) -> bytes:
    return pdf._draw_reproduced(cast("Page", printer), math_trace=math_trace)


def test_an_export_keeps_bytes_that_two_consecutive_prints_agreed_on() -> None:
    """Not one draw: every print of this page re-renders math while it is laid out."""
    printer = _Printer([_document(b"0.5 rg")] * 2)
    assert _drawn(printer) == _document(b"0.5 rg")
    assert len(printer.drawn) == 2
    assert printer.settlements == 2


def test_a_draw_that_did_not_reproduce_is_drawn_again_and_the_repeat_is_reported(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """D-490's shape: one coordinate off, in one object, between two draws of one page."""
    settled = _document(b"1 0 0 -1 49.0625 14905.2188 Tm")
    caught = _document(b"1 0 0 -1 49.0625 14906.0000 Tm")
    printer = _Printer([caught, settled, settled])
    assert _drawn(printer) == settled
    assert len(printer.drawn) == 3
    reported = capsys.readouterr().out
    assert "drawing again" in reported
    assert "object 1, Page" in reported


def test_two_draws_that_differ_only_in_the_clock_are_an_agreement() -> None:
    """The two fields Chromium stamps move between any two draws and mean nothing here."""
    stamped = b"%s1 0 obj\n<< /Type /Page /CreationDate (D:%s) >>\nendobj\n"
    printer = _Printer(
        [stamped % (_HEADER, b"20260922180000"), stamped % (_HEADER, b"20260922180007")]
    )
    assert _drawn(printer) == stamped % (_HEADER, b"20260922180007")
    assert len(printer.drawn) == 2


def test_an_export_refuses_when_no_two_prints_of_the_page_agree() -> None:
    """A page that never settles produces no publishable bytes, and says what moved."""
    printer = _Printer([_document(b"%d rg" % number) for number in range(pdf._PRINT_DRAWS)])
    with pytest.raises(RuntimeError) as refused:
        _drawn(printer)
    message = str(refused.value)
    assert f"no two of {pdf._PRINT_DRAWS} consecutive prints" in message
    assert "D-490" in message
    assert "object 1, Page" in message
    assert "squares-math-variant" in message
    assert len(printer.drawn) == pdf._PRINT_DRAWS


def test_the_trace_records_what_moved_under_every_draw() -> None:
    """The watch is diagnosis, not a verdict: it reports on a draw that was kept too."""
    printer = _Printer([_document(b"0.5 rg")] * 2)
    trace: dict[str, object] = {}
    _drawn(printer, trace)
    draws = trace["print_draws"]
    assert isinstance(draws, list)
    assert [draw["draw"] for draw in draws] == [0, 1]
    assert all(draw["changes"] == 24 and draw["quiet"] is False for draw in draws)
    assert "agreed_with_the_draw_before_it" not in draws[0]
    assert draws[1]["agreed_with_the_draw_before_it"] is True


def test_a_disagreement_reaches_the_failure_the_job_reads(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The join: `check` has to put `_difference` in the message, not just compute it."""
    renders = iter([_document(b"0.35294 0.11764 rg"), _document(b"0.35294 0.1176 rg")])
    monkeypatch.setattr(pdf, "render_pdf_bytes", lambda: next(renders))
    with pytest.raises(SystemExit) as refused:
        pdf.check()
    message = str(refused.value)
    assert "explainer PDF does not reproduce itself" in message
    assert "object 1, Page" in message
    assert "length delta 1" in message
    assert "difference between renders" in message


def test_the_check_draws_every_render_it_is_asked_for(monkeypatch: pytest.MonkeyPatch) -> None:
    """The earlier observation used ten renders; the job normally pays for two. A count
    that only reaches the first comparison would pass this file's other cases."""
    drawn: list[int] = []
    document = _HEADER + _pages(pdf.EXPECTED_PAGE_COUNT)
    monkeypatch.setattr(pdf, "render_pdf_bytes", lambda: (drawn.append(1), document)[1])
    monkeypatch.setattr(pdf, "font_findings", lambda _: [])
    pdf.check(5)
    assert len(drawn) == 5


def _artifact(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, raw: bytes) -> bytes:
    page = tmp_path / "index.html"
    page.write_bytes(b"<html>the current publication</html>")
    output = tmp_path / "explainer.pdf"
    stored = pdf._with_receipt(raw, page.read_bytes())
    output.write_bytes(stored)
    monkeypatch.setattr(pdf, "PAGE", page)
    monkeypatch.setattr(pdf, "OUTPUT", output)
    return stored


def test_artifact_check_refuses_a_bad_saved_draw_even_when_later_draws_agree(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Fresh loads agreeing with each other do not validate an artifact none of them drew.

    This case once asserted that a mismatch drew nothing more. D-509 is why it now
    draws `_ARTIFACT_LOADS`: a load can differ from a correct artifact. The stored file
    is still the reference, and agreement among the fresh loads still counts for nothing.
    """
    stored = _artifact(monkeypatch, tmp_path, _document(b"0.5 rg"))
    drawn: list[int] = []
    monkeypatch.setattr(
        pdf, "render_pdf_bytes", lambda: (drawn.append(1), _document(b"0.6 rg"))[1]
    )
    with pytest.raises(SystemExit, match="does not reproduce itself") as refused:
        pdf.check_artifact(3)
    assert len(drawn) == pdf._ARTIFACT_LOADS
    message = str(refused.value)
    assert f"No fresh page load reproduced the stored artifact, in {len(drawn)}" in message
    assert f"{len(drawn)} fresh page loads drew 1 distinct document" in message
    assert "loads 1, 2, 3, 4: 160 bytes, the document compared above" in message
    assert pdf.OUTPUT.read_bytes() == stored


def _loads(monkeypatch: pytest.MonkeyPatch, documents: Sequence[bytes]) -> list[bytes]:
    """Fresh loads drawing `documents` in order; the list records what was drawn."""
    drawn: list[bytes] = []
    remaining = iter(documents)

    def render() -> bytes:
        drawn.append(next(remaining))
        return drawn[-1]

    monkeypatch.setattr(pdf, "render_pdf_bytes", render)
    monkeypatch.setattr(pdf, "font_findings", lambda _: [])
    return drawn


#: Three documents in D-509's shape: the whole paper, with one glyph's `Tm` in one of
#: two placements, and a third placing a different glyph elsewhere.
_PLACED = _HEADER + _pages(pdf.EXPECTED_PAGE_COUNT)
_MAJORITY = _PLACED + _content(_GLYPH % b"18560.219", number=900)[len(_HEADER) :]
_MINORITY = _PLACED + _content(_GLYPH % b"18560", number=900)[len(_HEADER) :]
_ELSEWHERE = _PLACED + _content(_GLYPH % b"18560.2188", number=900)[len(_HEADER) :]


@pytest.mark.parametrize(
    ("renders", "sequence", "expected"),
    [
        (None, [_MINORITY, _MAJORITY], 2),
        (4, [_MINORITY, _MAJORITY, _MINORITY], 3),
        (None, [_MINORITY, _MINORITY, _MINORITY, _MAJORITY], 4),
    ],
    ids=["second-of-two", "second-of-three", "fourth"],
)
def test_artifact_check_passes_when_a_later_fresh_load_reproduces_the_artifact(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    *,
    renders: int | None,
    sequence: list[bytes],
    expected: int,
) -> None:
    """D-509: one load's glyph placement differs from the artifact's, another's does not.
    The extra loads stop at the first that reproduces the artifact once the requested
    count is drawn, and every load that did not is reported with its decoded line."""
    stored = _artifact(monkeypatch, tmp_path, _MAJORITY)
    drawn = _loads(monkeypatch, sequence)
    diagnostics = tmp_path / "diagnostics"
    count = [] if renders is None else ["--renders", str(renders)]
    assert pdf.main(["--check-artifact", *count, "--diagnostics-dir", str(diagnostics)]) == 0
    assert len(drawn) == expected
    out = capsys.readouterr().out
    assert "explainer PDF check passed: stored artifact reproduced by fresh load" in out
    assert f"of {expected}; load" in out
    assert "drew one other document, the per-load placement D-509 records" in out
    assert "fresh load 1 does not reproduce the stored artifact (D-509)" in out
    assert "b'1 0 0 -1 412.5 18560.219 Tm' against b'1 0 0 -1 412.5 18560 Tm'" in out
    assert not diagnostics.exists()
    assert pdf.OUTPUT.read_bytes() == stored


def test_artifact_check_with_a_first_load_that_agrees_draws_no_more(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The extra loads are the failure path's cost, never the passing run's."""
    _artifact(monkeypatch, tmp_path, _MAJORITY)
    drawn = _loads(monkeypatch, [_MAJORITY, _MINORITY])
    pdf.check_artifact()
    assert len(drawn) == 1
    out = capsys.readouterr().out
    assert "stored artifact and 1 fresh render agree" in out
    assert "D-509" not in out


def test_artifact_check_refuses_an_artifact_no_fresh_load_reproduces(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A minority-placement artifact, against loads that all draw the majority: the
    census says so, and the refusal names the moved line."""
    stored = _artifact(monkeypatch, tmp_path, _MINORITY)
    drawn = _loads(monkeypatch, [_MAJORITY] * pdf._ARTIFACT_LOADS)
    diagnostics = tmp_path / "diagnostics"
    with pytest.raises(SystemExit, match="does not reproduce itself") as refused:
        pdf.check_artifact(diagnostics_dir=diagnostics)
    assert len(drawn) == pdf._ARTIFACT_LOADS
    message = str(refused.value)
    assert "No fresh page load reproduced the stored artifact, in 4 drawn" in message
    assert "4 fresh page loads drew 1 distinct document" in message
    assert "b'1 0 0 -1 412.5 18560 Tm' against b'1 0 0 -1 412.5 18560.219 Tm'" in message
    (run,) = diagnostics.glob("pdf-check-*")
    assert (run / "reference.pdf").read_bytes() == stored
    assert (run / "replay.pdf").read_bytes() == pdf._with_receipt(
        _MAJORITY, pdf.PAGE.read_bytes()
    )
    assert not list(run.glob("load-*.pdf")), "one distinct document needs no extra copy"
    assert "fresh page loads drew 1 distinct document" in (run / "report.txt").read_text()


def test_artifact_check_refuses_two_different_documents_even_when_one_would_match(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Two placements of one page is D-509's shape; a third document is not, so the
    check stops at the second different document and refuses, retaining both."""
    _artifact(monkeypatch, tmp_path, _MAJORITY)
    drawn = _loads(monkeypatch, [_MINORITY, _ELSEWHERE, _MAJORITY])
    diagnostics = tmp_path / "diagnostics"
    with pytest.raises(SystemExit, match="does not reproduce itself") as refused:
        pdf.check_artifact(diagnostics_dir=diagnostics)
    assert drawn == [_MINORITY, _ELSEWHERE]
    message = str(refused.value)
    assert "No fresh page load reproduced the stored artifact, in 2 drawn" in message
    assert "2 fresh page loads drew 2 distinct documents" in message
    assert "load 1: " in message
    assert "the document compared above" in message
    assert "b'1 0 0 -1 412.5 18560.219 Tm' against b'1 0 0 -1 412.5 18560.2188 Tm'" in message
    (run,) = diagnostics.glob("pdf-check-*")
    receipt = pdf.PAGE.read_bytes()
    assert (run / "replay.pdf").read_bytes() == pdf._with_receipt(_MINORITY, receipt)
    assert (run / "load-2.pdf").read_bytes() == pdf._with_receipt(_ELSEWHERE, receipt)


def test_artifact_check_refuses_a_second_document_after_a_match(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """With an explicit count every requested load is drawn, and a match does not excuse
    two other documents beside it."""
    _artifact(monkeypatch, tmp_path, _MAJORITY)
    drawn = _loads(monkeypatch, [_MAJORITY, _MINORITY, _ELSEWHERE, _MAJORITY])
    with pytest.raises(SystemExit, match="does not reproduce itself") as refused:
        pdf.check_artifact(5)
    assert len(drawn) == 3
    assert "Fresh load 1 reproduced the stored artifact, but" in str(refused.value)


def test_update_stops_at_the_second_load_when_the_first_two_agree(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The passing run's whole extra cost is one load over the single draw of before."""
    _artifact(monkeypatch, tmp_path, b"an earlier publication")
    drawn = _loads(monkeypatch, [_MAJORITY, _MAJORITY, _MINORITY])
    assert pdf.main(["--update"]) == 0
    assert drawn == [_MAJORITY, _MAJORITY]
    assert pdf.OUTPUT.read_bytes() == pdf._with_receipt(_MAJORITY, pdf.PAGE.read_bytes())
    out = capsys.readouterr().out
    assert "two of 2 page loads agreed" in out
    assert "D-509" not in out


@pytest.mark.parametrize(
    ("sequence", "published"),
    [
        ([_MINORITY, _MAJORITY, _MAJORITY], _MAJORITY),
        ([_MINORITY, _MAJORITY, _MINORITY], _MINORITY),
    ],
    ids=["majority-after-a-minority-first", "first-and-third"],
)
def test_update_publishes_the_document_two_loads_agree_on(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    *,
    sequence: list[bytes],
    published: bytes,
) -> None:
    """D-509: a first load in the minority placement is not what ships. What ships is
    what two loads drew, and the load that agreed with nothing is in the log with the
    line that moved."""
    _artifact(monkeypatch, tmp_path, b"an earlier publication")
    drawn = _loads(monkeypatch, sequence)
    pdf.update()
    assert drawn == sequence
    assert pdf.OUTPUT.read_bytes() == pdf._with_receipt(published, pdf.PAGE.read_bytes())
    out = capsys.readouterr().out
    assert "two of 3 page loads agreed" in out
    assert "page load 2 agrees with no earlier load (D-509)" in out
    assert "b'1 0 0 -1 412.5 18560 Tm' against b'1 0 0 -1 412.5 18560.219 Tm'" in out


def test_update_refuses_when_no_two_loads_agree_and_leaves_the_old_file(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Three different documents are more than D-509's two placements, and none of them
    is confirmed, so nothing is published: never an unconfirmed draw."""
    earlier = _artifact(monkeypatch, tmp_path, b"an earlier publication")
    drawn = _loads(monkeypatch, [_MINORITY, _MAJORITY, _ELSEWHERE, _MAJORITY])
    with pytest.raises(SystemExit, match="no two of 3 page loads agreed") as refused:
        pdf.update()
    assert drawn == [_MINORITY, _MAJORITY, _ELSEWHERE]
    assert pdf.OUTPUT.read_bytes() == earlier
    message = str(refused.value)
    assert "b'1 0 0 -1 412.5 18560 Tm' against b'1 0 0 -1 412.5 18560.219 Tm'" in message
    assert "3 fresh page loads drew 3 distinct documents against load 1's" in message
    assert "load 1: " in message
    assert "load 1's document" in message
    assert "the document compared above" in message
    assert "18560 Tm' against b'1 0 0 -1 412.5 18560.2188 Tm'" in message


@pytest.mark.parametrize("receipt", ["missing", "stale", "duplicate"])
def test_artifact_check_compares_the_source_receipt_as_part_of_the_file(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, receipt: str
) -> None:
    raw = _document(b"0.5 rg")
    stored = _artifact(monkeypatch, tmp_path, raw)
    broken = {
        "missing": raw,
        "stale": pdf._with_receipt(raw, b"an earlier page"),
        "duplicate": pdf._with_receipt(stored, pdf.PAGE.read_bytes()),
    }[receipt]
    pdf.OUTPUT.write_bytes(broken)
    monkeypatch.setattr(pdf, "render_pdf_bytes", lambda: raw)
    with pytest.raises(SystemExit, match="does not reproduce itself"):
        pdf.check_artifact()
    assert pdf.OUTPUT.read_bytes() == broken


def test_artifact_check_requires_the_existing_file_without_drawing_a_fallback(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _artifact(monkeypatch, tmp_path, _document(b"0.5 rg"))
    pdf.OUTPUT.unlink()
    monkeypatch.setattr(pdf, "render_pdf_bytes", lambda: pytest.fail("must not render"))
    with pytest.raises(SystemExit, match=r"missing.*--update"):
        pdf.check_artifact()
    assert not pdf.OUTPUT.exists()


@pytest.mark.parametrize("renders", [None, 2, 4])
def test_artifact_cli_counts_the_saved_draw_and_leaves_its_original_bytes_intact(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    renders: int | None,
) -> None:
    # The stored file carries the publication's date; a fresh draw carries the clock's.
    published = pdf.publication_date_text(pdf.REVISED).encode("ascii")
    raw = _HEADER + _pages(pdf.EXPECTED_PAGE_COUNT)
    raw += b"/CreationDate (D:%s) /ModDate (D:%s)\n" % (published, published)
    stored = _artifact(monkeypatch, tmp_path, raw)
    fresh = raw.replace(published, b"20260913000001+00'00'")
    drawn: list[int] = []
    inspected: list[bytes] = []
    monkeypatch.setattr(pdf, "render_pdf_bytes", lambda: (drawn.append(1), fresh)[1])
    monkeypatch.setattr(pdf, "font_findings", lambda data: (inspected.append(data), [])[1])
    diagnostics = tmp_path / "diagnostics"
    count = [] if renders is None else ["--renders", str(renders)]
    assert pdf.main(["--check-artifact", *count, "--diagnostics-dir", str(diagnostics)]) == 0
    assert len(drawn) == (renders or 2) - 1
    assert inspected == [stored]
    assert pdf.OUTPUT.read_bytes() == stored
    assert not diagnostics.exists(), "a successful check must create no failure artifacts"
    assert "stored artifact" in capsys.readouterr().out


def _clocked(document: bytes, clock: bytes = b"20261001195544") -> bytes:
    """A document as Chromium leaves it: both date fields, from the clock."""
    return document + b"/CreationDate (D:%s+00'00')\n/ModDate (D:%s+00'00')\n" % (clock, clock)


def test_update_dates_the_publication_by_its_revision_and_not_by_the_clock(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """What is published says when the paper was last revised, at noon UTC.

    Two loads agree apart from the second Chromium printed each, which is all a fresh
    draw's dates ever say. The file written carries the page's revised day in both
    fields, at the length Chromium wrote, so nothing after them moves, and the artifact
    check then passes against draws that carry the clock again.
    """
    _artifact(monkeypatch, tmp_path, b"an earlier publication")
    _loads(monkeypatch, [_clocked(_MAJORITY), _clocked(_MAJORITY, b"20261001195551")])
    pdf.update()
    written = pdf.OUTPUT.read_bytes()
    stated = pdf.publication_date_text(pdf.REVISED)
    assert pdf.pdf_dates(written) == {"CreationDate": stated, "ModDate": stated}
    assert written == pdf._with_receipt(
        pdf.dated(_clocked(_MAJORITY), pdf.REVISED), pdf.PAGE.read_bytes()
    )
    assert len(written) == len(pdf._with_receipt(_clocked(_MAJORITY), pdf.PAGE.read_bytes()))

    _loads(monkeypatch, [_clocked(_MAJORITY, b"20261002080000")])
    pdf.check_artifact()


def test_artifact_check_refuses_a_stored_pdf_dated_by_the_clock(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The comparisons ignore the two date fields, so this is the check that reads them.

    The stored file reproduces exactly, and is refused for saying when it was drawn in
    place of when the paper was revised.
    """
    stored = _artifact(monkeypatch, tmp_path, _clocked(_MAJORITY))
    _loads(monkeypatch, [_clocked(_MAJORITY, b"20261002080000")])
    with pytest.raises(SystemExit, match="dated by its last revision") as refused:
        pdf.check_artifact()
    assert "not by the clock that drew it" in str(refused.value)
    assert pdf.OUTPUT.read_bytes() == stored


@pytest.mark.parametrize("failure", ["fonts", "pagination"])
def test_artifact_check_applies_the_content_guards_to_the_stored_pdf(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, failure: str
) -> None:
    pages = pdf.EXPECTED_PAGE_COUNT - (failure == "pagination")
    raw = _HEADER + _pages(pages) + b"/CreationDate (D:20260912000000+00'00')\n"
    stored = _artifact(monkeypatch, tmp_path, raw)
    monkeypatch.setattr(
        pdf, "render_pdf_bytes", lambda: raw.replace(b"20260912000000", b"20260913000000")
    )
    inspected: list[bytes] = []

    def findings(data: bytes) -> list[str]:
        inspected.append(data)
        return ["stored PDF has outlined owned fonts"] if failure == "fonts" else []

    monkeypatch.setattr(pdf, "font_findings", findings)
    diagnostics = tmp_path / "diagnostics"
    expected = (
        "outlined owned fonts" if failure == "fonts" else f"expected {pdf.EXPECTED_PAGE_COUNT}"
    )
    with pytest.raises(SystemExit, match=expected):
        pdf.check_artifact(diagnostics_dir=diagnostics)
    assert inspected == [stored]
    assert pdf.OUTPUT.read_bytes() == stored
    retained = list(diagnostics.glob("pdf-check-*"))
    assert len(retained) == 1
    assert (retained[0] / "reference.pdf").read_bytes() == stored
    assert expected in (retained[0] / "report.txt").read_text(encoding="utf-8")


@pytest.mark.parametrize("mode", ["fresh", "artifact"])
def test_direct_checks_refuse_a_vacuous_count_before_drawing(
    monkeypatch: pytest.MonkeyPatch, mode: str
) -> None:
    monkeypatch.setattr(pdf, "render_pdf_bytes", lambda: pytest.fail("must not render"))
    check = pdf.check_artifact if mode == "artifact" else pdf.check
    with pytest.raises(ValueError, match="at least 2"):
        check(1)


@pytest.mark.parametrize("mode", ["fresh", "artifact"])
def test_failed_comparisons_retain_the_raw_pair_and_report_without_overwriting_prior_runs(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, mode: str
) -> None:
    raw = _document(b"0.5 rg") + b"/CreationDate (D:20260912000000+00'00')\n"
    fresh = _document(b"0.6 rg") + b"/CreationDate (D:20260913000000+00'00')\n"
    stored = _artifact(monkeypatch, tmp_path, raw)
    diagnostics = tmp_path / "diagnostics"
    expected = (
        (stored, pdf._with_receipt(fresh, pdf.PAGE.read_bytes()))
        if mode == "artifact"
        else (raw, fresh)
    )
    for _ in range(2):
        draws = iter([raw, fresh] if mode == "fresh" else [fresh] * pdf._ARTIFACT_LOADS)
        monkeypatch.setattr(pdf, "render_pdf_bytes", draws.__next__)
        check = pdf.check_artifact if mode == "artifact" else pdf.check
        with pytest.raises(SystemExit, match="difference between renders") as refused:
            check(diagnostics_dir=diagnostics)
        assert str(diagnostics) in str(refused.value)
    runs = list(diagnostics.glob("pdf-check-*"))
    assert len(runs) == 2
    for run in runs:
        assert (run / "reference.pdf").read_bytes() == expected[0]
        assert (run / "replay.pdf").read_bytes() == expected[1]
        report = (run / "report.txt").read_text(encoding="utf-8")
        assert "difference between renders" in report
        assert "first difference at byte" in report
        assert "object 1, Page" in report
    assert pdf.OUTPUT.read_bytes() == stored


def test_a_diagnostic_write_failure_keeps_the_original_mismatch_visible(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    diagnostics = tmp_path / "occupied"
    diagnostics.write_bytes(b"preserve this file")
    draws = iter([_document(b"0.5 rg"), _document(b"0.6 rg")])
    monkeypatch.setattr(pdf, "render_pdf_bytes", lambda: next(draws))
    with pytest.raises(SystemExit, match="does not reproduce itself") as refused:
        pdf.check(diagnostics_dir=diagnostics)
    assert "could not retain PDF diagnostics" in str(refused.value)
    assert diagnostics.read_bytes() == b"preserve this file"


def _page(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> list[int]:
    """A page on disk so `main` gets past its own guard, and the count `check` was given."""
    page = tmp_path / "index.html"
    page.write_text("<html></html>", encoding="utf-8")
    monkeypatch.setattr(pdf, "PAGE", page)
    asked: list[int] = []

    def check(renders: int, *, diagnostics_dir: Path | None = None) -> None:
        assert diagnostics_dir is None
        asked.append(renders)

    monkeypatch.setattr(pdf, "check", check)
    return asked


@pytest.mark.parametrize(("argv", "expected"), [([], 2), (["--renders", "7"], 7)])
def test_the_cli_forwards_the_count_it_was_given(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, argv: list[str], expected: int
) -> None:
    asked = _page(monkeypatch, tmp_path)
    assert pdf.main(["--check", *argv]) == 0
    assert asked == [expected]


@pytest.mark.parametrize("mode", ["--check", "--check-artifact"])
def test_one_render_is_refused_because_it_compares_nothing(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, mode: str
) -> None:
    _page(monkeypatch, tmp_path)
    with pytest.raises(SystemExit) as refused:
        pdf.main([mode, "--renders", "1"])
    assert refused.value.code == 2


@pytest.mark.parametrize("mode", ["--update", "--fonts"])
@pytest.mark.parametrize(
    "option", [("--renders", "2"), ("--renders", "10"), ("--diagnostics-dir", "trace")]
)
def test_comparison_options_are_refused_in_the_modes_that_do_not_compare(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, mode: str, option: tuple[str, str]
) -> None:
    """An explicit render count must not be silently ignored, even at the default value."""
    _page(monkeypatch, tmp_path)
    monkeypatch.setattr(pdf, "update", lambda: None)
    monkeypatch.setattr(pdf, "fonts", lambda: None)
    with pytest.raises(SystemExit) as refused:
        pdf.main([mode, *option])
    assert refused.value.code == 2


@pytest.mark.parametrize("mode", ["--check", "--check-artifact"])
@pytest.mark.parametrize("disagree", [False, True])
def test_math_trace_retains_the_exact_draws_and_marks_unobserved_stored_dom(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, mode: str, *, disagree: bool
) -> None:
    raw = _HEADER + _pages(pdf.EXPECTED_PAGE_COUNT)
    stored = _artifact(monkeypatch, tmp_path, raw)
    draws: list[bytes] = []

    def render(*, math_trace: dict[str, object]) -> bytes:
        draw = raw + (b"changed" if disagree and (draws or mode == "--check-artifact") else b"")
        draws.append(draw)
        math_trace.update(browser_version="test-browser", snapshots=[{"phase": "before-pdf"}])
        return draw

    monkeypatch.setattr(pdf, "render_pdf_bytes", render)
    monkeypatch.setattr(pdf, "font_findings", lambda _: [])
    directory = tmp_path / "diagnostics"
    args = [mode, "--renders", "2", "--trace-math", "--diagnostics-dir", str(directory)]
    if disagree:
        with pytest.raises(SystemExit, match="does not reproduce itself"):
            pdf.main(args)
    else:
        assert pdf.main(args) == 0
    runs = list(directory.glob("pdf-math-trace-*"))
    assert len(runs) == 1
    run = runs[0]
    assert (run / "source.html").read_bytes() == pdf.PAGE.read_bytes()
    records = [json.loads(p.read_text()) for p in sorted(run.glob("draw-*.json"))]
    # A stored artifact no load reproduces is compared against D-509's extra loads, and
    # each of them is traced like the first.
    extra = pdf._ARTIFACT_LOADS - 1 if disagree and mode == "--check-artifact" else 0
    assert len(records) == 2 + extra
    assert len(draws) == len(records) - (mode == "--check-artifact")
    assert records[0]["origin"] == (
        "stored artifact" if mode == "--check-artifact" else "fresh"
    )
    if mode == "--check-artifact":
        assert records[0]["observations"] is None
    else:
        assert records[0]["observations"]["browser_version"] == "test-browser"
    for index, record in enumerate(records):
        data = (run / f"draw-{index}.pdf").read_bytes()
        assert record["pdf_sha256"] == hashlib.sha256(data).hexdigest()
        source_digest = hashlib.sha256(pdf.PAGE.read_bytes()).hexdigest()
        assert record["current_source_html_sha256"] == source_digest
        assert record["pdf_source_html_receipts"] == (
            [source_digest] if mode == "--check-artifact" else []
        )
    assert (run / "draw-0.pdf").read_bytes() == (
        stored if mode == "--check-artifact" else draws[0]
    )
    assert (run / "draw-1.pdf").read_bytes() == (
        pdf._with_receipt(draws[-1], pdf.PAGE.read_bytes())
        if mode == "--check-artifact"
        else draws[-1]
    )
    assert pdf.OUTPUT.read_bytes() == stored


@pytest.mark.parametrize("args", [["--check"], ["--update"], ["--fonts"]])
def test_math_trace_requires_a_comparison_and_explicit_destination(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, args: list[str]
) -> None:
    _page(monkeypatch, tmp_path)
    with pytest.raises(SystemExit) as refused:
        pdf.main([*args, "--trace-math"])
    assert refused.value.code == 2


@pytest.mark.parametrize(
    "args",
    [
        ["--check"],
        ["--check", "--trace-math"],
        ["--check", "--diagnostics-dir", "trace"],
        ["--check-artifact", "--trace-math", "--diagnostics-dir", "trace"],
        ["--update", "--trace-math", "--diagnostics-dir", "trace"],
        ["--fonts", "--trace-math", "--diagnostics-dir", "trace"],
    ],
)
def test_prepared_text_replacement_refuses_uncontrolled_modes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, args: list[str]
) -> None:
    _page(monkeypatch, tmp_path)
    with pytest.raises(SystemExit) as refused:
        pdf.main([*args, "--rebuild-prepared-text"])
    assert refused.value.code == 2


def test_prepared_text_treatment_forwards_every_draw_and_retains_failure(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    check = pdf.check
    _page(monkeypatch, tmp_path)
    calls: list[bool] = []
    raw = _HEADER + _pages(pdf.EXPECTED_PAGE_COUNT)

    def render(*, math_trace: dict[str, object], rebuild_prepared_text: bool) -> bytes:
        calls.append(rebuild_prepared_text)
        math_trace["prepared_text_intervention"] = {
            "requested": True,
            "applied": True,
            "status": "applied",
            "selected_count": 1,
            "mutated_count": 1,
        }
        return raw + (b"different" if len(calls) == 2 else b"")

    monkeypatch.setattr(pdf, "render_pdf_bytes", render)
    directory = tmp_path / "diagnostics"
    with pytest.raises(SystemExit, match="does not reproduce itself"):
        check(20, diagnostics_dir=directory, trace_math=True, rebuild_prepared_text=True)
    assert calls == [True, True]
    run = next(directory.glob("pdf-math-trace-*"))
    records = [json.loads(path.read_text()) for path in sorted(run.glob("draw-*.json"))]
    assert len(records) == 2
    assert all(
        record["observations"]["prepared_text_intervention"]["applied"] for record in records
    )
    assert (run / "draw-0.pdf").read_bytes() == raw
    assert (run / "draw-1.pdf").read_bytes() == raw + b"different"


def test_direct_prepared_text_treatment_requires_trace_and_destination(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    render_pdf_bytes = pdf.render_pdf_bytes
    monkeypatch.setattr(pdf, "render_pdf_bytes", lambda **_: pytest.fail("must not render"))
    with pytest.raises(ValueError, match="requires --trace-math and --diagnostics-dir"):
        pdf.check(rebuild_prepared_text=True)
    with pytest.raises(ValueError, match="requires --trace-math and --diagnostics-dir"):
        pdf.check(trace_math=True, rebuild_prepared_text=True)
    with pytest.raises(ValueError, match="requires a math trace"):
        render_pdf_bytes(rebuild_prepared_text=True)
    assert not (tmp_path / "diagnostics").exists()


@pytest.mark.parametrize("requested", [False, True])
def test_early_browser_failure_records_requested_arm_without_claiming_mutation(
    monkeypatch: pytest.MonkeyPatch, *, requested: bool
) -> None:
    import playwright.sync_api as playwright  # noqa: PLC0415

    def unavailable() -> None:
        raise RuntimeError("browser did not start")

    monkeypatch.setattr(playwright, "sync_playwright", unavailable)
    observations: dict[str, object] = {}
    with pytest.raises(RuntimeError, match="browser did not start"):
        pdf.render_pdf_bytes(math_trace=observations, rebuild_prepared_text=requested)
    assert observations["prepared_text_intervention"] == {
        "requested": requested,
        "applied": False,
        "status": "not-reached",
        "selected_count": 0,
        "selected": [],
        "mutated_count": 0,
        "mutated": [],
        "html_unchanged": None,
    }


def test_interrupted_evaluate_keeps_mutation_outcome_unknown(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import playwright.sync_api as playwright  # noqa: PLC0415

    from devtools import sans_instances  # noqa: PLC0415

    def evaluate(script: str, *_: object) -> list[dict[str, str]] | None:
        if script == pdf._TRACED_SETTLED:
            return [{"phase": "settled"}]
        if script == pdf._PREPARED_TEXT_INTERVENTION:
            raise RuntimeError("evaluation interrupted after possible mutation")
        return None

    page = SimpleNamespace(
        viewport_size={"width": 1280, "height": 720},
        emulate_media=lambda **_: None,
        goto=lambda *_, **__: None,
        wait_for_selector=lambda *_, **__: None,
        evaluate=evaluate,
        evaluate_handle=lambda *_: object(),
        add_style_tag=lambda **_: None,
        pdf=lambda **_: pytest.fail("must not capture PDF"),
    )
    session = SimpleNamespace(send=lambda _: {}, detach=lambda: None)
    browser = SimpleNamespace(
        version="test-browser",
        new_browser_cdp_session=lambda: session,
        new_page=lambda: page,
        close=lambda: None,
    )
    driver = SimpleNamespace(chromium=SimpleNamespace(launch=lambda **_: browser))
    monkeypatch.setattr(playwright, "sync_playwright", lambda: nullcontext(driver))
    monkeypatch.setattr(sans_instances, "print_face_css", lambda: "")
    observations: dict[str, object] = {}
    with pytest.raises(RuntimeError, match="evaluation interrupted after possible mutation"):
        pdf.render_pdf_bytes(math_trace=observations, rebuild_prepared_text=True)
    assert observations["snapshots"] == [{"phase": "settled"}]
    assert observations["prepared_text_intervention"] == {
        "requested": True,
        "applied": None,
        "status": "interrupted",
        "selected_count": None,
        "selected": None,
        "mutated_count": None,
        "mutated": None,
        "html_unchanged": None,
    }


def test_math_trace_retains_available_observations_when_a_draw_fails(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    check = pdf.check
    _page(monkeypatch, tmp_path)

    def render(*, math_trace: dict[str, object]) -> bytes:
        math_trace["browser_version"] = "test-browser"
        raise RuntimeError("test PDF capture failed")

    monkeypatch.setattr(pdf, "render_pdf_bytes", render)
    directory = tmp_path / "diagnostics"
    with pytest.raises(RuntimeError, match="test PDF capture failed"):
        check(trace_math=True, diagnostics_dir=directory)
    run = next(directory.glob("pdf-math-trace-*"))
    record = json.loads((run / "draw-0.json").read_text())
    assert record["pdf_sha256"] is None
    assert record["render_error"] == "test PDF capture failed"
    assert record["observations"]["browser_version"] == "test-browser"
    assert not (run / "draw-0.pdf").exists()


def test_traced_settlement_uses_the_existing_frames_and_font_waits() -> None:
    _run_node("settled.mjs")


def test_the_pdf_is_drawn_from_the_page_where_it_is_served_and_beside_it() -> None:
    """The exporter reads the page where the renderer writes it, under `papers/` by the
    paper's slug, and writes the PDF beside it under the same slug. The two modules name
    the site and the page's address the same way."""
    from devtools import render_n11_lower_bounds_explainer as renderer  # noqa: PLC0415

    assert renderer.OUTPUT == pdf.PAGE
    assert pdf.PAGE.relative_to(pdf.ROOT).as_posix() == (
        "site/papers/n11-lower-bounds-explainer.html"
    )
    assert pdf.PAGE.with_suffix(".pdf") == pdf.OUTPUT
    assert renderer.SITE_URL == pdf.SITE_URL
    assert renderer.PAGE_URL == pdf.PAGE_URL


def test_a_relative_link_in_the_pdf_resolves_against_the_pages_own_address() -> None:
    """The page is a level below the site's root, so a link that climbs to the root has
    to land there in the PDF, and a link beside the page has to stay beside it."""
    _run_node("absolute-links.mjs")


@pytest.mark.parametrize("overflow", [False, True])
def test_math_snapshot_tracks_visible_text_without_hiding_omissions(*, overflow: bool) -> None:
    _run_node("math-snapshot.mjs", *(["overflow"] if overflow else []))
