# pyright: reportPrivateUsage=false
"""What `render_explainer_pdf --check` says when the page does not draw the same twice.

The check itself needs a browser, a rendered page and about nine seconds a render, and
it lives in the Pages job. What is here is the part that only matters on the day it
fails, and that therefore has to be right before then: that a disagreement is reported
with the object it happened in, and that the number of renders the CLI asks for is the
number `check` takes.

Both are regressions waiting to happen rather than hypotheticals. On 2026-09-10 this
check failed on main for the first time, said `786119 then 786117 bytes` and nothing
else, and the renders were gone -- so the cause had to be guessed between the three the
module docstring names. And the CLI-to-function join is the one D-488 was made of: a
count that argparse accepts and nothing forwards looks exactly like a count that works.

Nothing here launches a browser: `render_pdf_bytes` is replaced with a list of synthetic
documents in the shapes Chromium writes, so the whole file runs in milliseconds and
belongs in the quick lane.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from devtools import render_explainer_pdf as pdf

#: A document with one object, in the shape the writer emits: the header at a line start,
#: the dictionary declaring what the object is, and a body that the cases below vary.
_HEADER = b"%PDF-1.4\n"


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


def test_a_difference_before_the_first_object_names_the_file_header() -> None:
    report = pdf._difference(_HEADER + b"a", _HEADER + b"b")
    assert "in the file header" in report


def test_a_render_cut_short_is_reported_as_cut_short() -> None:
    """The one failure a first-differing-byte scan cannot find, because there isn't one."""
    whole = _document(b"0.5 rg")
    report = pdf._difference(whole[: len(whole) - 10], whole)
    assert "cut short" in report


def test_two_renders_that_agree_are_not_given_an_invented_difference() -> None:
    """Unreachable from `check`, which only asks about renders it has found to differ.
    Reported honestly anyway: the prefix message would otherwise announce a truncation
    on two identical files, and send the next reader after a bug that is not there."""
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


def test_the_check_draws_every_render_it_is_asked_for(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ten renders is the guarantee the module claims; two is what the job pays for. A
    count that only reaches the first comparison would pass this file's other cases."""
    drawn: list[int] = []
    monkeypatch.setattr(pdf, "render_pdf_bytes", lambda: (drawn.append(1), _document(b"x"))[1])
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


def test_the_count_is_refused_in_the_modes_that_do_not_compare(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """`--update --renders 10` asks for something no mode does; silence would look done."""
    _page(monkeypatch, tmp_path)
    with pytest.raises(SystemExit) as refused:
        pdf.main(["--update", "--renders", "10"])
    assert refused.value.code == 2
