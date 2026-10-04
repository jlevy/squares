#!/usr/bin/env python3
"""Draw the known-best atlas's regularized views with the house renderer.

Usage, from `packing/`:

    uv run --frozen --all-extras --group dev \
        python -m devtools.render_regularized_atlas --update
    uv run --frozen --all-extras --group dev \
        python -m devtools.render_regularized_atlas --check

`atlas/known-best/regularized/index.json`, which `devtools.regularize_axis_components
--update-atlas` writes, names every record that has a regularized view: the record's
exact frame with its near-axis squares straightened and slid into exact contact (X-049,
"Exact Regularization"). This draws each such view to
`atlas/known-best/regularized/rendering/n-NNN.svg` with `sqpack.render`, the renderer
that draws `atlas/known-best/rendering/n-NNN.svg`, at the same settings. A square's
shade is therefore the house rule (`sqpack.render.color`) applied to the regularized
pose, and the homepage's atlas reduces a regularized drawing to a tile by the code that
reduces a house drawing (`render_frontier_page.packing_svg`), so the House/Regularized
toggle compares two drawings made one way.

The set is read from the index, never listed here: a view another run adds is drawn by
the next `--update`, and `--check` fails until it is. A view is drawn only from the
bytes the index recorded a verdict for: the source witness and the decompressed view
must have the digests the index holds (cache keys, as the index says, not integrity
claims), so a stale view is refused rather than drawn.

A drawing never promotes anything. It carries the record's evidence tier and check,
read from the source witness, not the view's own exact verification; its title and
description say it is a regularized derived view; and its source id is the view's
(`W-known-best-nNNN-regularized`). The container side is the view's certified side,
which differs from the record's printed side by at most a unit in the fifteenth
decimal, invisible at any size the drawing is shown.

`--check` re-renders every view and compares bytes, and names a missing, stale or
unexpected file. It takes a few seconds, about a tenth of a second for each of the
largest views.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from collections.abc import Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools.build_known_best_atlas import frame_from_witness
from devtools.regularize_axis_components import ATLAS_CONTRACT, DRAWING_LABEL
from sqpack.render import render_packing_svg
from sqpack.render.model import PackingFrame, RenderSpec
from sqpack.workers import worker_count
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
REGULARIZED = ROOT / "atlas/known-best/regularized"
INDEX = REGULARIZED / "index.json"
RENDER_ROOT = REGULARIZED / "rendering"
GENERATOR = "python -m devtools.render_regularized_atlas"
#: The witness contract a view and its source are written under.
WITNESS_CONTRACT = "packing.squares:Witness/v2"
#: What a view's certificate says it is (`regularize_axis_components.regularized_witness`).
VIEW_KIND = "regularized-view"


@dataclass(frozen=True)
class Layout:
    """Where the drawings are read from and written to; the tests point it at a scratch
    tree. Every path the index records is relative to `repo`."""

    repo: Path
    index: Path
    render_root: Path

    def rendering(self, n: int) -> Path:
        return self.render_root / f"n-{n:03d}.svg"

    def relative(self, path: Path) -> str:
        return path.resolve().relative_to(self.repo.resolve()).as_posix()


LAYOUT = Layout(REPO, INDEX, RENDER_ROOT)


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def regularized_entries(layout: Layout = LAYOUT) -> list[dict[str, Any]]:
    """The index's records with a regularized view, in order of n.

    The index must be the layer's (its contract) and say how a drawing of it is labelled,
    which is the word the homepage's badge and every drawing here carry.
    """
    if not layout.index.is_file():
        raise SystemExit(f"{layout.relative(layout.index)} is missing")
    index = json.loads(layout.index.read_text(encoding="utf-8"))
    if index.get("contract") != ATLAS_CONTRACT:
        raise SystemExit(f"{layout.relative(layout.index)} is not a {ATLAS_CONTRACT} index")
    if index.get("label") != DRAWING_LABEL:
        raise SystemExit(
            f"{layout.relative(layout.index)} labels its drawings {index.get('label')!r}, "
            f"not {DRAWING_LABEL!r}"
        )
    entries = [entry for entry in index["entries"] if entry["status"] == "regularized"]
    numbers = [entry["n"] for entry in entries]
    if numbers != sorted(set(numbers)):
        raise SystemExit("the index's regularized records are not in order of n, once each")
    return sorted(entries, key=lambda entry: entry["n"])


def _witness(text: str, where: str) -> dict[str, Any]:
    document = load_yaml(text)
    if not isinstance(document, dict) or not isinstance(document.get("witness"), dict):
        raise SystemExit(f"{where} is not a witness document")
    if document.get("softschema", {}).get("contract") != WITNESS_CONTRACT:
        raise SystemExit(f"{where} is not a {WITNESS_CONTRACT} document")
    return document["witness"]


def source_witness(entry: dict[str, Any], layout: Layout = LAYOUT) -> dict[str, Any]:
    """The record's own witness, refused unless it is the one the view was derived from."""
    path = entry["source"]["witness"]
    data = (layout.repo / path).read_bytes()
    if _digest(data) != entry["source"]["sha256"]:
        raise SystemExit(f"n={entry['n']}: {path} changed since its view was derived (stale)")
    return _witness(data.decode("utf-8"), path)


def view_witness(entry: dict[str, Any], layout: Layout = LAYOUT) -> dict[str, Any]:
    """The regularized view, refused unless it is the bytes the index recorded a verdict
    for and it says it is a regularized view of this record."""
    path = entry["view"]["path"]
    data = gzip.decompress((layout.repo / path).read_bytes())
    if _digest(data) != entry["view"]["sha256"]:
        raise SystemExit(f"n={entry['n']}: {path} differs from the view its verdict is for")
    if not entry["exact_verification"]["passed"]:
        raise SystemExit(f"n={entry['n']}: the view's recorded exact verification failed")
    view = _witness(data.decode("utf-8"), path)
    certificate = view.get("certificate", {})
    if (
        view.get("n") != entry["n"]
        or certificate.get("kind") != VIEW_KIND
        or certificate.get("label") != DRAWING_LABEL
        or certificate.get("derived_from") != entry["source"]["id"]
    ):
        raise SystemExit(f"n={entry['n']}: {path} is not a regularized view of its record")
    return view


def regularized_frame(entry: dict[str, Any], layout: Layout = LAYOUT) -> PackingFrame:
    """The view's squares and side under the record's own evidence tier and check.

    `frame_from_witness` is the house atlas's reading of a witness. The view's frame
    would state a certified upper bound, which is what its exact verification shows of
    the view; the drawing states the record's tier instead, so it promotes nothing.
    """
    view = view_witness(entry, layout)
    source = frame_from_witness(source_witness(entry, layout))
    return replace(
        frame_from_witness(view),
        evidence=source.evidence,
        check=source.check,
        label=f"n={entry['n']} {DRAWING_LABEL}",
        source_id=str(view["id"]),
        source_url=source.source_url,
    )


def render(entry: dict[str, Any], layout: Layout = LAYOUT) -> str:
    """One view drawn as the house atlas draws its record (`build_known_best_atlas`),
    titled and described as the regularized derived view it is."""
    n = entry["n"]
    return render_packing_svg(
        regularized_frame(entry, layout),
        spec=RenderSpec(
            overlays=frozenset(),
            title=f"Known-best packing of {n} unit squares, {DRAWING_LABEL}",
            description=(
                f"A {DRAWING_LABEL} derived view of the retained known-best n={n} "
                "construction, never the source witness: its exact frame with the "
                "near-axis squares straightened and slid into exact contact, verified "
                "over the rationals (atlas/known-best/regularized/index.json), and "
                "rendered with the repository's deterministic house renderer. It changes "
                "no side, frontier value or evidence tier; the evidence stated here is "
                "the record's."
            ),
        ),
    )


def _render_unit(unit: tuple[dict[str, Any], Layout]) -> str:
    entry, layout = unit
    return render(entry, layout)


def expected_outputs(layout: Layout = LAYOUT, *, workers: int = 1) -> dict[Path, str]:
    """Every drawing the index asks for, by the path it is kept at."""
    entries = regularized_entries(layout)
    units = [(entry, layout) for entry in entries]
    if workers > 1 and len(units) > 1:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            texts = list(pool.map(_render_unit, units))
    else:
        texts = [_render_unit(unit) for unit in units]
    drawn = zip(entries, texts, strict=True)
    return {layout.rendering(entry["n"]): text for entry, text in drawn}


def _summary(count: int) -> str:
    return f"{count} {DRAWING_LABEL} views drawn by the house renderer"


def update(layout: Layout = LAYOUT, *, workers: int = 1) -> int:
    """Write every drawing and remove any the index no longer asks for."""
    expected = expected_outputs(layout, workers=workers)
    layout.render_root.mkdir(parents=True, exist_ok=True)
    for path, text in expected.items():
        if path.is_file() and path.read_text(encoding="utf-8") == text:
            continue
        with atomic_output_file(path) as temporary:
            temporary.write_text(text, encoding="utf-8")
    for stray in sorted(layout.render_root.iterdir()):
        if stray not in expected:
            stray.unlink()
    print(f"regularized renderings updated: {_summary(len(expected))}")
    return 0


def problems(layout: Layout = LAYOUT, *, workers: int = 1) -> list[str]:
    """What differs between the drawings kept and the drawings the index asks for."""
    expected = expected_outputs(layout, workers=workers)
    found: list[str] = []
    for path, text in expected.items():
        if not path.is_file():
            found.append(f"{layout.relative(path)} is missing")
        elif path.read_text(encoding="utf-8") != text:
            found.append(f"{layout.relative(path)} is stale")
    if layout.render_root.is_dir():
        found.extend(
            f"unexpected {layout.relative(path)}"
            for path in sorted(layout.render_root.iterdir())
            if path not in expected
        )
    return found


def check(layout: Layout = LAYOUT, *, workers: int = 1) -> int:
    found = problems(layout, workers=workers)
    if found:
        for problem in found:
            print(f"regularized renderings drift: {problem}")
        print(f"run `{GENERATOR} --update`")
        return 1
    count = len(regularized_entries(layout))
    print(f"regularized renderings check passed: {_summary(count)}")
    return 0


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--update", action="store_true", help="write the drawings")
    mode.add_argument("--check", action="store_true", help="compare them, writing nothing")
    command.add_argument(
        "--workers",
        type=int,
        default=None,
        help="processes to draw with (default: the gate's PACK_JOBS cap, or every core)",
    )
    return command


def main(argv: Sequence[str] | None = None, *, layout: Layout = LAYOUT) -> int:
    args = parser().parse_args(argv)
    units = len(regularized_entries(layout))
    workers = args.workers if args.workers is not None else worker_count(units)
    if args.update:
        return update(layout, workers=workers)
    return check(layout, workers=workers)


if __name__ == "__main__":
    raise SystemExit(main())
