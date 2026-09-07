#!/usr/bin/env python3
"""Export a known-best composite to a print-ready vector PDF.

The page keeps the artwork's intrinsic size rather than being scaled into a
stock paper box: the 1-100 composite is 2400 by 2896 CSS pixels, which at the
SVG spec's 96 pixels per inch is 25.00 by 30.17 inches, so the PDF page is
exactly that and the diagram meets its edges with no silent margin or
letterboxing. A composite of another size gets its own size the same way. Print
scaling is then the print dialog's business, not something baked in here.

Output is vector, so text stays selectable and the packings stay sharp at any
zoom.

Staleness is tracked by a receipt rather than by re-rendering and comparing:
cairo assigns font-subset tags per process, so two runs of the same input agree
within one process but not across two. The receipt is the source SVG's sha256,
written as a PDF comment appended after %%EOF, which mirrors the tEXt receipt
the PNG preview already carries. Appending leaves the cross-reference offsets
untouched, and trailing bytes after %%EOF are ignored by readers.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections.abc import Sequence
from pathlib import Path

from strif import atomic_output_file

from sqpack.known_best import KNOWN_BEST_COMPOSITES

ROOT = Path(__file__).resolve().parent.parent
ATLAS_ROOT = ROOT / "atlas/known-best"
#: The composite this tool exports when a caller names none. The atlas builder passes
#: each of its own stems in; this is what a function called without one means.
DEFAULT_STEM = "known-best-1-100"
GENERATOR = "python -m devtools.render_composite_pdf"
# The SVG specification's reference pixel. A user unit maps to 1/96 inch, and a
# PDF point is 1/72 inch, so a user unit is 0.75pt.
CSS_PIXELS_PER_INCH = 96
PDF_SOURCE_KEY = b"sqpack-source-svg-sha256"
PDF_SIGNATURE = b"%PDF-"


def composite_svg(stem: str = DEFAULT_STEM) -> Path:
    """The drawing one composite's PDF is exported from."""
    return ATLAS_ROOT / f"{stem}.svg"


def composite_pdf(stem: str = DEFAULT_STEM) -> Path:
    """Where that export is written."""
    return ATLAS_ROOT / f"{stem}.pdf"


def _source_digest(stem: str = DEFAULT_STEM) -> str:
    return hashlib.sha256(composite_svg(stem).read_bytes()).hexdigest()


def _with_receipt(content: bytes, digest: str) -> bytes:
    return content + b"\n%" + PDF_SOURCE_KEY + b": " + digest.encode("ascii") + b"\n"


def pdf_receipt(content: bytes) -> str | None:
    """Return the source digest recorded in the PDF, if any."""
    if not content.startswith(PDF_SIGNATURE):
        raise ValueError("composite PDF is not a PDF")
    match = re.search(b"%" + PDF_SOURCE_KEY + rb": ([0-9a-f]{64})\s*\Z", content)
    return match.group(1).decode("ascii") if match else None


def render_pdf_bytes(stem: str = DEFAULT_STEM) -> bytes:
    """Render a composite SVG to PDF bytes at the artwork's intrinsic size."""
    # Reading a PDF receipt does not require loading the native renderer.
    import cairosvg  # noqa: PLC0415

    # svg2pdf returns None only when handed a write target, which we never do.
    content = cairosvg.svg2pdf(url=str(composite_svg(stem)), dpi=CSS_PIXELS_PER_INCH)
    if not isinstance(content, bytes):
        raise TypeError("cairosvg did not return PDF bytes")
    return content


def update(stem: str = DEFAULT_STEM) -> None:
    pdf = composite_pdf(stem)
    digest = _source_digest(stem)
    if pdf.is_file() and pdf_receipt(pdf.read_bytes()) == digest:
        print(f"composite PDF already current: {pdf.name}")
        return
    content = _with_receipt(render_pdf_bytes(stem), digest)
    with atomic_output_file(pdf, make_parents=True) as temporary:
        temporary.write_bytes(content)
    print(f"composite PDF updated: {pdf.name} ({len(content)} bytes)")


def check(stem: str = DEFAULT_STEM) -> None:
    pdf = composite_pdf(stem)
    if not pdf.is_file():
        raise ValueError(f"missing {pdf.relative_to(ROOT)}; run with --update")
    recorded = pdf_receipt(pdf.read_bytes())
    if recorded is None:
        raise ValueError(f"{pdf.relative_to(ROOT)} carries no source receipt")
    if recorded != _source_digest(stem):
        raise ValueError(
            f"stale {pdf.relative_to(ROOT)}; regenerate it after changing the composite"
        )
    print(f"composite PDF check passed: {pdf.name} matches the current {stem}.svg")


def published_stems() -> tuple[str, ...]:
    """Every composite the corpus publishes, which is what a bare command means.

    A command that named one stem by default reported on one PDF and passed while
    another was stale, which is the failure the atlas builder's own `--check` was
    widened to cover on the other side. There is no reading of "is the PDF export
    current" that is about one member of a family of two.
    """
    return tuple(composite.stem for composite in KNOWN_BEST_COMPOSITES)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--update", action="store_true", help="write the PDF")
    group.add_argument("--check", action="store_true", help="fail if the PDF is stale")
    parser.add_argument(
        "--stem",
        default=None,
        help="filename stem of one composite to export (default: every published one)",
    )
    arguments = parser.parse_args(argv)
    stems = (arguments.stem,) if arguments.stem else published_stems()
    try:
        for stem in stems:
            if arguments.update:
                update(stem)
            else:
                check(stem)
    except (OSError, RuntimeError, TypeError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
