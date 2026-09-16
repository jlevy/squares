# pyright: reportPrivateUsage=false
"""The PDF publication comparison, failure evidence, and required-image wait.

The check itself needs a browser, a rendered page and about nine seconds a render, and
it lives in the Pages job. What is here is the part that only matters on the day it
fails, and that therefore has to be right before then: a disagreement names its object
or outside-object section without guessing a cause, the exact stored artifact and its
HTML receipt take part in the comparison, and an image that cannot become drawable
refuses capture. A failed comparison retains its raw pair when diagnosis is requested.

On 2026-09-10 this check failed on main for the first time, said `786119 then 786117
bytes` and nothing else, and the renders were gone. Its cause remains unknown. The
publication job also checked a later pair of draws while shipping an earlier file;
agreement between the later pair could not validate that artifact. The CLI-to-function
join is the one D-488 was made of: a count that argparse accepts and nothing forwards
looks exactly like a count that works. The image wait initially discarded every decode
rejection, which could let two PDFs agree on the same absent figure.

Nothing here launches a browser. `render_pdf_bytes` is replaced with synthetic
documents in the shapes Chromium writes, and the exact image-wait, settlement and math
trace probes run under Node against small stand-ins, in the scripts under
`tests/node/render_explainer_pdf/`. The file belongs in the quick lane.
"""

from __future__ import annotations

import hashlib
import json
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace

import pytest
from nodejs_wheel import node

from devtools import render_explainer_pdf as pdf

NODE = Path(__file__).resolve().parent / "node" / "render_explainer_pdf"


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
    stored = _artifact(monkeypatch, tmp_path, _document(b"0.5 rg"))
    drawn: list[int] = []
    monkeypatch.setattr(
        pdf, "render_pdf_bytes", lambda: (drawn.append(1), _document(b"0.6 rg"))[1]
    )
    with pytest.raises(SystemExit, match="does not reproduce itself"):
        pdf.check_artifact(3)
    assert drawn == [1], "the stored artifact must be the reference, with no retry"
    assert pdf.OUTPUT.read_bytes() == stored


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
    raw = _HEADER + _pages(pdf.EXPECTED_PAGE_COUNT)
    raw += b"/CreationDate (D:20260912000000+00'00') /ModDate (D:20260912000000+00'00')\n"
    stored = _artifact(monkeypatch, tmp_path, raw)
    fresh = raw.replace(b"20260912000000", b"20260913000001")
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
        draws = iter([raw, fresh] if mode == "fresh" else [fresh])
        monkeypatch.setattr(pdf, "render_pdf_bytes", draws.__next__)
        check = pdf.check_artifact if mode == "artifact" else pdf.check
        with pytest.raises(SystemExit, match="cause is unknown") as refused:
            check(diagnostics_dir=diagnostics)
        assert str(diagnostics) in str(refused.value)
    runs = list(diagnostics.glob("pdf-check-*"))
    assert len(runs) == 2
    for run in runs:
        assert (run / "reference.pdf").read_bytes() == expected[0]
        assert (run / "replay.pdf").read_bytes() == expected[1]
        report = (run / "report.txt").read_text(encoding="utf-8")
        assert "cause is unknown" in report
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
    assert len(records) == 2
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


@pytest.mark.parametrize("overflow", [False, True])
def test_math_snapshot_tracks_visible_text_without_hiding_omissions(*, overflow: bool) -> None:
    _run_node("math-snapshot.mjs", *(["overflow"] if overflow else []))
