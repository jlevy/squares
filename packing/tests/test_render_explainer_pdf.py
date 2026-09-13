# pyright: reportPrivateUsage=false
"""The PDF difference report, render count, and required-image wait.

The check itself needs a browser, a rendered page and about nine seconds a render, and
it lives in the Pages job. What is here is the part that only matters on the day it
fails, and that therefore has to be right before then: a disagreement names its object
or outside-object section without guessing a cause, the CLI count reaches `check`, and
an image that cannot become drawable refuses capture.

All three are regressions waiting to happen rather than hypotheticals. On 2026-09-10 this
check failed on main for the first time, said `786119 then 786117 bytes` and nothing
else, and the renders were gone -- so the cause had to be guessed between the three the
module docstring names. And the CLI-to-function join is the one D-488 was made of: a
count that argparse accepts and nothing forwards looks exactly like a count that works.
The image wait initially discarded every decode rejection, which could let two PDFs
agree on the same absent figure.

Nothing here launches a browser. `render_pdf_bytes` is replaced with synthetic
documents in the shapes Chromium writes, and the exact image-wait JavaScript runs under
Node against small image-element stand-ins. The file belongs in the quick lane.
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest
from nodejs_wheel import node

from devtools import render_explainer_pdf as pdf

#: A document with one object, in the shape the writer emits: the header at a line start,
#: the dictionary declaring what the object is, and a body that the cases below vary.
_HEADER = b"%PDF-1.4\n"


def _run_image_wait(case: str) -> None:
    """Run the exact browser-side image wait against small image-element stand-ins."""
    script = dedent("""
        const assert = require('node:assert/strict');
        let document;
    """)
    script += f"const waitForImages = {pdf._IMAGES_DECODED};\n"
    script += dedent(f"""
        (async () => {{
          {case}
        }})().catch((error) => {{
          console.error(error.stack || error);
          process.exit(1);
        }});
    """)
    completed = node(
        ["-"], return_completed_process=True, input=script, capture_output=True, text=True
    )
    assert completed.returncode == 0, completed.stderr


def test_the_image_wait_forces_lazy_images_eager_before_decode() -> None:
    _run_image_wait("""
        const calls = [];
        const image = {
          loading: 'lazy', complete: true, naturalWidth: 640, naturalHeight: 480,
          currentSrc: 'file:///atlas.svg',
          async decode() { calls.push(this.loading); },
        };
        document = {images: [image]};
        await waitForImages();
        assert.deepEqual(calls, ['eager']);
    """)


def test_a_decode_rejection_is_safe_only_for_an_available_image() -> None:
    """A changed request may reject while its replacement is already drawable."""
    _run_image_wait("""
        const image = {
          loading: 'lazy', complete: true, naturalWidth: 640, naturalHeight: 480,
          currentSrc: 'file:///atlas.svg',
          async decode() { throw new Error('the request changed'); },
        };
        document = {images: [image]};
        await waitForImages();
    """)


def test_an_image_without_a_drawable_current_request_refuses_the_render() -> None:
    _run_image_wait("""
        document = {images: [
          {
            loading: 'lazy', complete: false, naturalWidth: 0, naturalHeight: 0,
            currentSrc: '', src: 'file:///missing-atlas.svg',
            async decode() { throw new Error('request failed'); },
          },
          {
            loading: 'eager', complete: true, naturalWidth: 0, naturalHeight: 0,
            currentSrc: 'file:///empty-atlas.svg', src: 'file:///empty-atlas.svg',
            async decode() {},
          },
        ]};
        await assert.rejects(waitForImages(), (error) => {
          assert.match(error.message, /2 required images are not drawable after decode/);
          assert.match(
            error.message,
            /missing-atlas[.]svg.*complete=false.*0x0.*request failed/,
          );
          assert.match(error.message, /empty-atlas[.]svg.*complete=true.*0x0/);
          return true;
        });
    """)


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


def test_two_renders_that_agree_are_not_given_an_invented_difference() -> None:
    """Unreachable from `check`, which only asks about renders it has found to differ.
    Reported honestly anyway: the prefix message would otherwise announce an unequal
    length on two identical files, and send the reader after a bug that is not there."""
    report = pdf._difference(_document(b"0.5 rg"), _document(b"0.5 rg"))
    assert "no byte differs" in report
    assert "cut short" not in report


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
    assert "cause is unknown" in message


def test_the_check_draws_every_render_it_is_asked_for(monkeypatch: pytest.MonkeyPatch) -> None:
    """The earlier observation used ten renders; the job normally pays for two. A count
    that only reaches the first comparison would pass this file's other cases."""
    drawn: list[int] = []
    document = _HEADER + _pages(pdf.EXPECTED_PAGE_COUNT)
    monkeypatch.setattr(pdf, "render_pdf_bytes", lambda: (drawn.append(1), document)[1])
    monkeypatch.setattr(pdf, "font_findings", lambda _: [])
    pdf.check(5)
    assert len(drawn) == 5


def _page(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> list[int]:
    """A page on disk so `main` gets past its own guard, and the count `check` was given."""
    page = tmp_path / "index.html"
    page.write_text("<html></html>", encoding="utf-8")
    monkeypatch.setattr(pdf, "PAGE", page)
    asked: list[int] = []
    monkeypatch.setattr(pdf, "check", asked.append)
    return asked


@pytest.mark.parametrize(("argv", "expected"), [([], 2), (["--renders", "7"], 7)])
def test_the_cli_forwards_the_count_it_was_given(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, argv: list[str], expected: int
) -> None:
    asked = _page(monkeypatch, tmp_path)
    assert pdf.main(["--check", *argv]) == 0
    assert asked == [expected]


def test_one_render_is_refused_because_it_compares_nothing(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _page(monkeypatch, tmp_path)
    with pytest.raises(SystemExit) as refused:
        pdf.main(["--check", "--renders", "1"])
    assert refused.value.code == 2


@pytest.mark.parametrize("mode", ["--update", "--fonts"])
@pytest.mark.parametrize("renders", ["2", "10"])
def test_the_count_is_refused_in_the_modes_that_do_not_compare(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, mode: str, renders: str
) -> None:
    """An explicit render count must not be silently ignored, even at the default value."""
    _page(monkeypatch, tmp_path)
    monkeypatch.setattr(pdf, "update", lambda: None)
    monkeypatch.setattr(pdf, "fonts", lambda: None)
    with pytest.raises(SystemExit) as refused:
        pdf.main([mode, "--renders", renders])
    assert refused.value.code == 2
