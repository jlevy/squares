#!/usr/bin/env python3
"""Export the known-best composite to a print-ready vector PDF.

The page keeps the artwork's intrinsic size rather than being scaled into a
stock paper box: the SVG is 2400 by 2516 CSS pixels, which at the SVG spec's 96
pixels per inch is 25.00 by 26.21 inches, so the PDF page is exactly that and
the diagram meets its edges with no silent margin or letterboxing. Print
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

import cairosvg
from strif import atomic_output_file

ROOT = Path(__file__).resolve().parent.parent
SUMMARY_SVG = ROOT / "atlas/known-best/known-best-1-100.svg"
SUMMARY_PDF = ROOT / "atlas/known-best/known-best-1-100.pdf"
GENERATOR = "python -m devtools.render_composite_pdf"
# The SVG specification's reference pixel. A user unit maps to 1/96 inch, and a
# PDF point is 1/72 inch, so a user unit is 0.75pt.
CSS_PIXELS_PER_INCH = 96
PDF_SOURCE_KEY = b"sqpack-source-svg-sha256"
PDF_SIGNATURE = b"%PDF-"


def _source_digest() -> str:
    return hashlib.sha256(SUMMARY_SVG.read_bytes()).hexdigest()


def _with_receipt(content: bytes, digest: str) -> bytes:
    return content + b"\n%" + PDF_SOURCE_KEY + b": " + digest.encode("ascii") + b"\n"


def pdf_receipt(content: bytes) -> str | None:
    """Return the source digest recorded in the PDF, if any."""
    if not content.startswith(PDF_SIGNATURE):
        raise ValueError("composite PDF is not a PDF")
    match = re.search(b"%" + PDF_SOURCE_KEY + rb": ([0-9a-f]{64})\s*\Z", content)
    return match.group(1).decode("ascii") if match else None


def render_pdf_bytes() -> bytes:
    """Render the composite SVG to PDF bytes at the artwork's intrinsic size."""
    # svg2pdf returns None only when handed a write target, which we never do.
    content = cairosvg.svg2pdf(url=str(SUMMARY_SVG), dpi=CSS_PIXELS_PER_INCH)
    if not isinstance(content, bytes):
        raise TypeError("cairosvg did not return PDF bytes")
    return content


def update() -> None:
    digest = _source_digest()
    if SUMMARY_PDF.is_file() and pdf_receipt(SUMMARY_PDF.read_bytes()) == digest:
        print(f"composite PDF already current: {SUMMARY_PDF.name}")
        return
    content = _with_receipt(render_pdf_bytes(), digest)
    with atomic_output_file(SUMMARY_PDF, make_parents=True) as temporary:
        temporary.write_bytes(content)
    print(f"composite PDF updated: {SUMMARY_PDF.name} ({len(content)} bytes)")


def check() -> None:
    if not SUMMARY_PDF.is_file():
        raise ValueError(f"missing {SUMMARY_PDF.relative_to(ROOT)}; run with --update")
    recorded = pdf_receipt(SUMMARY_PDF.read_bytes())
    if recorded is None:
        raise ValueError(f"{SUMMARY_PDF.relative_to(ROOT)} carries no source receipt")
    if recorded != _source_digest():
        raise ValueError(
            f"stale {SUMMARY_PDF.relative_to(ROOT)}; regenerate it after changing the composite"
        )
    print("composite PDF check passed: receipt matches the current composite SVG")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--update", action="store_true", help="write the PDF")
    group.add_argument("--check", action="store_true", help="fail if the PDF is stale")
    arguments = parser.parse_args(argv)
    try:
        if arguments.update:
            update()
        else:
            check()
    except (OSError, RuntimeError, TypeError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
