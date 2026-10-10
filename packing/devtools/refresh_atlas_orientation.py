"""Refresh only the derived records of registered atlas geometry isometries.

Run the complete registered orientation refresh from ``packing/``::

    python -m devtools.refresh_atlas_orientation --n 211 --refresh-selected

The optional selected step reuses the canonical witness/house renderer, refusing a
manifest fact change before writing. Without it, the current orientation must already
be retained. The command then runs the maintained scoped exact
regularizer and translation screen, redraws only its regularized SVG and updates only
its frontier motion scope. The regularizer independently verifies the reflected exact
view, and the screen replays every reflected slide in the selected numerical pose.

Other case records are preserved. Manifest, composite-figure, release pin and composite
exports belong to the coordinating producer and are never written here. Refresh the
composite-figure record after this command before producing composite exports.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from strif import atomic_output_file

from devtools import assess_frontier_rigidity as rigidity
from devtools import build_known_best_atlas as builder
from devtools import regularize_axis_components as regularizer
from devtools import render_regularized_atlas as renderer
from devtools import screen_translation_escape as screen
from devtools.atlas_orientation import REFLECTED_N, REGISTERED_OPERATION, geometry_transform
from sqpack.witness import load_witness


def _refresh_selected(entries: Sequence[dict], layout: regularizer.AtlasLayout) -> None:
    """Refresh only geometry; an isometry must leave the manifest's facts unchanged."""
    cases = builder.built_cases([entry["n"] for entry in entries], workers=1)
    outputs = []
    for entry, case in zip(entries, cases, strict=True):
        produced = builder._manifest_entry(case)  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
        if produced != entry:
            raise ValueError(f"n={entry['n']}: orientation refresh would change manifest facts")
        outputs.extend(
            (
                (layout.packing / entry["witness"]["path"], case.witness_text),
                (layout.packing / entry["rendering"]["path"], case.rendering_text),
            )
        )
    for path, content in outputs:
        with atomic_output_file(path) as temporary:
            temporary.write_text(content, encoding="utf-8")


def refresh(numbers: Sequence[int], *, refresh_selected: bool = False) -> None:
    """Refresh only registered, already transformed selected arrangements."""
    if not numbers or len(set(numbers)) != len(numbers) or set(numbers) != {REFLECTED_N}:
        raise ValueError("orientation refresh requires unique registered counts (211)")
    layout = regularizer.ATLAS
    entries = json.loads(layout.manifest.read_text(encoding="utf-8"))["atlas"]["entries"]
    selected = [entry for entry in entries if entry["n"] in numbers]
    if len(selected) != len(numbers):
        raise ValueError("registered orientation is absent or duplicated in the manifest")
    if refresh_selected:
        _refresh_selected(selected, layout)
    for entry in selected:
        witness = load_witness(
            layout.packing / entry["witness"]["path"],
            fallback_schema=regularizer.WITNESS_SCHEMA,
        )
        transform = geometry_transform(witness)
        if transform is None or transform["operation"] != REGISTERED_OPERATION:
            raise ValueError(
                f"n={entry['n']}: selected witness lacks the current orientation; "
                "run with --refresh-selected first"
            )
    regularizer.update_atlas(layout, only=numbers, workers=1)
    drawings = {entry["n"]: entry for entry in renderer.regularized_entries()}
    for n in numbers:
        if n not in drawings:
            raise ValueError(f"n={n}: reflected exact view was not retained")
        path = renderer.LAYOUT.rendering(n)
        text = renderer.render(drawings[n])
        with atomic_output_file(path) as temporary:
            temporary.write_text(text, encoding="utf-8")
    screen.update(1, only=numbers)
    for n, path, before, after in rigidity.plan():
        if n in numbers and before != after:
            with atomic_output_file(path) as temporary:
                temporary.write_text(after, encoding="utf-8")
    print(
        f"atlas orientation refreshed: n={', '.join(map(str, numbers))}; other cases preserved"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, nargs="+", required=True, metavar="N")
    parser.add_argument(
        "--refresh-selected",
        action="store_true",
        help="rebuild only the selected witness and house SVG; refuse manifest changes",
    )
    arguments = parser.parse_args(argv)
    refresh(arguments.n, refresh_selected=arguments.refresh_selected)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
