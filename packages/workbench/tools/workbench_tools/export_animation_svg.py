"""Export one explicit packing-animation record as a self-contained SVG, with a receipt.

The SVG is written to a sibling temporary file and renamed into place, and the receipt
`<stem>.receipt.json` is written beside it last, so neither a half-written figure nor a
receipt for a figure that does not exist is ever left at the destination. An SVG that
carries a script is refused before anything is written.

The receipt says `transitions_are_packings: false`, with the reason: the SVG interpolates
between the animation's frames, so what it shows in between is an illustration. When a
frame is guided or not numerically checked, the SVG's own `<desc>` says so as well. Nothing
is drawn on the figure to say it.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m workbench_tools.export_animation_svg \
        run.json --out run.svg
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any, cast

from strif import atomic_output_file

from sqpack.render.svg import write_svg_atomic
from workbench_tools.animation_records import AnimationDocument, decode_animation
from workbench_tools.animation_render import (
    INTERPOLATION_REASON,
    export_svg,
    transitions_reason,
)


def export_receipt(
    document: AnimationDocument,
    svg: str,
    *,
    animation: Path,
    animation_bytes: bytes,
    out: Path,
    width: int,
) -> dict[str, Any]:
    """What an exported SVG shows and why its motion is not a sequence of packings."""
    specific = transitions_reason(document)
    reason = INTERPOLATION_REASON if specific is None else f"{specific} {INTERPOLATION_REASON}"
    return {
        "svg": out.name,
        "svg_sha256": hashlib.sha256(svg.encode("utf-8")).hexdigest(),
        "animation": str(animation),
        "animation_sha256": hashlib.sha256(animation_bytes).hexdigest(),
        "animation_contract": document.contract,
        "frames": len(document.frames),
        "width": width,
        "transitions_are_packings": False,
        "intermediate_frames": "illustrative-tween",
        "reason": reason,
    }


def main(argv: Sequence[str] | None = None) -> int:
    """Run the strict v1 animation-to-SVG command."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("animation", type=Path)
    # The output was `--out` and became positional in the move to the package, which broke
    # every old invocation without a word. Both spellings work; giving both is refused.
    parser.add_argument("out", type=Path, nargs="?", help="the SVG to write")
    parser.add_argument("--out", dest="out_option", type=Path, help="the SVG to write")
    parser.add_argument("--width", type=int, default=960)
    options = parser.parse_args(argv)
    positional = cast(Path | None, options.out)
    flagged = cast(Path | None, options.out_option)
    if positional is not None and flagged is not None:
        parser.error("give the output path once: positionally or with --out, not both")
    out = positional or flagged
    if out is None:
        parser.error("an output path is required: positionally or with --out")
    source = cast(Path, options.animation)
    width = cast(int, options.width)

    raw_bytes = source.read_bytes()
    document = decode_animation(cast(object, json.loads(raw_bytes.decode("utf-8"))))
    svg = export_svg(document, width=width)
    receipt = export_receipt(
        document, svg, animation=source, animation_bytes=raw_bytes, out=out, width=width
    )
    write_svg_atomic(out, svg)
    receipt_path = out.with_suffix(".receipt.json")
    with atomic_output_file(receipt_path, make_parents=True) as temporary:
        temporary.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    guided = any(document.frame_is_guided(frame) for frame in document.frames)
    tag = " [GUIDED]" if guided else ""
    print(f"{out}  {len(svg):,} bytes  {len(document.frames)} frames{tag}")
    print(f"  {receipt_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
