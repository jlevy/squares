#!/usr/bin/env python3
"""Census how evenly the atlas draws its grid regions, count by count, for any checkout.

Usage, from `packing/`, each after
`uv run --frozen --all-extras --group dev python -m devtools.census_drawing_regularity`:

    [--tree DIR] [--n N ...] [--workers K] [--output FILE.json] [--json]
    --compare BEFORE.json AFTER.json [--top K] [--markdown FILE.md]

The homepage atlas draws each known-best packing with the house renderer
(`sqpack.render.color`): a square's hue is its angle class, seeded at `1e-6` radians and
merged across full shared sides, and its shade is how many of its four sides it shares
whole with a wall or a same-angle neighbour, both ends within `2e-6`. A grid region reads
as one dark, uniform hue only when every axis-aligned square in it shares its sides and
no square in it sits a hair off the axes. Two things break it:

- **Light axis squares.** An axis-aligned square that shares at most one full side
  (`LIGHT_MAX_SIDES`) is drawn in the two lightest shades. Its other faces have slack, a
  misaligned or staggered neighbour, an open region, or a tilted neighbour.
- **Near-axis squares.** A square tilted past the house's `1e-6` radians but within half a
  degree (`NEAR_AXIS_DEGREES`, the workbench's colour tolerance) of the axes is a class of
  its own: it takes another hue beside the grid, and it shares no full side with it.

For each count this reads the drawing a tree's atlas shows -- the tree's regularized view
where `packing/atlas/known-best/regularized/index.json` gives the count the status
`regularized`, else the known-best witness -- and colours it with the house renderer
itself (`build_known_best_atlas.frame_from_witness`, then `assign_square_colors` at the
default `RenderSpec`), so the counts are the drawing's, not a replica's. It reports the
axis squares (the renderer's orientation within `1e-6` radians of the axes) and their
full-side histogram, the light ones, the near-axis squares and their signed tilts, the
squares tilted between half a degree and two degrees (`SMALL_TILT_DEGREES`, reported but
not counted), and the drawing's distinct angle classes and hues.

**Why a face is open.** For each axis square sharing fewer than four sides, every face
without a full shared side is given its first cause in the order of
`census_atlas_contact_shades.classify` under the house rule (an exact-polygon sweep of
the square alone out through that face: `hole-or-open`, `tilted-neighbour`, `offset`,
`slack`, `misaligned`, then the near-miss bands), with `tilted-neighbour` split by
whether the obstacle is itself near-axis (`near-axis-neighbour`, which straightening could
remove) or a real rotation. A tilted neighbour or an open region (`HARD`) is the edge of
a grid region, and a square there is shaded lighter by the packing itself. Every other
cause (`SOFT`) is unevenness inside the grid: `uneven_axis` counts the axis squares with
at least one such face. `variation`, `uneven_axis` plus the near-axis squares, is what
`--compare` ranks by, with `light_axis` beside it.

The faces come from the census's float replica of the house rule; a square whose replica
count differs from the renderer's is counted in `replica_disagrees` and its faces are not
classified. A sweep moves one square alone: `slack` says the square could slide that far
before meeting anything, not that the drawing can close the gap without opening another,
which only a joint placement can say (`devtools.regularize_grid_slack`).

The census decides nothing and writes only the file it is given. A tree's layer is
read as it stands, a preview tree's scratch layer included; that its views are the
index's is the atlas checks' question, not this census's.
"""

from __future__ import annotations

import argparse
import gzip
import json
import math
from collections import Counter
from collections.abc import Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any, Literal

from strif import atomic_output_file

from devtools import census_atlas_contact_shades as shades
from devtools.build_known_best_atlas import frame_from_witness
from devtools.regularize_axis_components import EVAND_GENERATOR
from sqpack.render.color import assign_square_colors
from sqpack.render.model import RenderSpec
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
GENERATOR = "python -m devtools.census_drawing_regularity"
FORMAT = "drawing-regularity-census-v1"
INDEX = Path("packing/atlas/known-best/regularized/index.json")
WITNESS = "packing/witnesses/known-best/n-{n:03d}.yaml"
COUNTS = range(1, 325)

SPEC = RenderSpec(overlays=frozenset())
"""The house renderer's defaults: angle tolerance `1e-6` radians, contact `2e-6`."""
AXIS_TOLERANCE = SPEC.angle_tolerance_radians
LIGHT_MAX_SIDES = 1
"""An axis square sharing at most this many full sides is drawn light."""
NEAR_AXIS_DEGREES = 0.5
"""Past the house's tolerance and within this of the axes: a hair off the grid."""
SMALL_TILT_DEGREES = 2.0
"""Squares tilted between `NEAR_AXIS_DEGREES` and this are reported, not counted."""
QUARTER = Decimal("1.57079632679489661923132169163975144209858469968755291048747")
HOUSE = shades.RULES[0]
FACE_CAUSES = (
    "near-axis-neighbour",
    "tilted-neighbour",
    "hole-or-open",
    "offset",
    "slack",
    "misaligned",
    "angle-near-miss",
    "near-miss",
    "rule-boundary",
)
HARD = frozenset({"tilted-neighbour", "hole-or-open"})
"""Causes the grid cannot remove by moving: a real rotation beside it, or an open region."""
SOFT = frozenset(FACE_CAUSES) - HARD
"""Every other cause: slack, a misaligned or staggered aligned neighbour, a near miss, or a
near-axis neighbour. A square with one of these is where a grid region reads uneven."""


@dataclass(frozen=True)
class Drawing:
    """What one count's atlas tile is drawn from in one tree."""

    n: int
    kind: Literal["regularized-view", "witness"]
    path: str
    """Repository-relative."""
    generator: str | None
    """The index entry's generator, where it names one."""


def read_index(tree: Path) -> dict[int, dict[str, Any]]:
    """The tree's regularized-layer entries by count; empty when the tree has no layer."""
    path = tree / INDEX
    if not path.is_file():
        return {}
    index = json.loads(path.read_text(encoding="utf-8"))
    return {int(entry["n"]): entry for entry in index.get("entries", [])}


def _text(path: Path) -> str:
    raw = path.read_bytes()
    return (gzip.decompress(raw) if path.suffix == ".gz" else raw).decode("utf-8")


def drawing_for(
    tree: Path, n: int, entries: Mapping[int, Mapping[str, Any]]
) -> tuple[Drawing, dict[str, Any]]:
    """The drawing a tree's atlas shows for `n`, and the witness body it is drawn from."""
    entry = entries.get(n)
    if entry is not None and entry.get("status") == "regularized":
        relative = str(entry["view"]["path"])
        text = _text(tree / relative)
        generator = entry.get("generator")
        drawing = Drawing(
            n, "regularized-view", relative, str(generator) if generator else None
        )
    else:
        relative = WITNESS.format(n=n)
        text = _text(tree / relative)
        drawing = Drawing(n, "witness", relative, None)
    document = load_yaml(text)
    if not isinstance(document, dict) or not isinstance(document.get("witness"), dict):
        raise TypeError(f"{relative} is not a witness document")
    return drawing, document["witness"]


def signed_degrees(orientation: Decimal) -> float:
    """An orientation modulo a quarter turn, in degrees in `(-45, 45]`."""
    degrees = math.degrees(float(orientation))
    return degrees - 90.0 if degrees > 45.0 else degrees


def tilt_of(orientation: Decimal) -> Decimal:
    """Distance from the axes modulo a quarter turn, as the renderer measures it."""
    return min(orientation, QUARTER - orientation)


def _sig(value: float, digits: int = 6) -> float:
    return 0.0 if value == 0 else float(f"{value:.{digits - 1}e}")


def face_causes(
    witness: Mapping[str, Any], squares: Sequence[int], house_counts: Sequence[int]
) -> dict[int, list[str]]:
    """Why each open face of each of `squares` is open, by square; a square whose replica
    count differs from the renderer's is left out."""
    packing, _frame, _degrees = shades.packings_from_witness(dict(witness))
    found = shades.edge_rule_contacts(packing, HOUSE)
    grid = shades.Grid(packing.squares)
    causes: dict[int, list[str]] = {}
    for index in squares:
        contacts = found[index]
        if min(4, len(contacts)) != house_counts[index]:
            continue
        closed = {contact.face for contact in contacts}
        open_faces: list[str] = []
        for face in shades.FACES:
            if face in closed:
                continue
            sweep = shades.sweep_face(packing, grid, index, face)
            cause = shades.classify(sweep, HOUSE)
            if (
                cause == "tilted-neighbour"
                and sweep.obstacle == "square"
                and sweep.obstacle_tilt <= math.radians(NEAR_AXIS_DEGREES)
            ):
                cause = "near-axis-neighbour"
            open_faces.append(cause)
        causes[index] = open_faces
    return causes


def _tally(causes: Mapping[int, Sequence[str]], squares: Sequence[int]) -> dict[str, int]:
    counted = Counter(cause for index in squares for cause in causes.get(index, ()))
    return {cause: counted[cause] for cause in FACE_CAUSES if counted[cause]}


def regularity(witness: Mapping[str, Any]) -> dict[str, Any]:
    """The house renderer's colouring of one drawing, reduced to the grid's evenness."""
    frame = frame_from_witness(dict(witness))
    colors = list(assign_square_colors(frame, SPEC).values())
    tilts = [tilt_of(color.orientation_radians) for color in colors]
    axis = [index for index, tilt in enumerate(tilts) if tilt <= AXIS_TOLERANCE]
    sides = [color.contact_sides or 0 for color in colors]
    histogram = [0] * 5
    for index in axis:
        histogram[sides[index]] += 1
    light = [index for index in axis if sides[index] <= LIGHT_MAX_SIDES]
    near_limit = Decimal(str(math.radians(NEAR_AXIS_DEGREES)))
    small_limit = Decimal(str(math.radians(SMALL_TILT_DEGREES)))
    near = [index for index, tilt in enumerate(tilts) if AXIS_TOLERANCE < tilt < near_limit]
    small = [index for index, tilt in enumerate(tilts) if near_limit <= tilt < small_limit]
    near_classes = {colors[index].angle_class for index in near}
    open_squares = [index for index in axis if sides[index] < 4]
    causes = face_causes(witness, open_squares, sides)
    uneven = [index for index in open_squares if SOFT.intersection(causes.get(index, ()))]
    return {
        "squares": len(colors),
        "axis": len(axis),
        "axis_inexact": sum(1 for index in axis if tilts[index] != 0),
        "axis_sides": histogram,
        "light_axis": len(light),
        "light_squares": [frame.squares[index].label for index in light],
        "near_axis": len(near),
        "near_axis_degrees": sorted(
            _sig(signed_degrees(colors[index].orientation_radians)) for index in near
        ),
        "near_axis_squares": [frame.squares[index].label for index in near],
        "near_axis_classes": len(near_classes),
        "small_tilt": len(small),
        "classes": len({color.angle_class for color in colors}),
        "hues": len({color.hue_index for color in colors}),
        "uneven_axis": len(uneven),
        "variation": len(uneven) + len(near),
        "light_faces": _tally(causes, light),
        "open_faces": _tally(causes, open_squares),
        "replica_disagrees": len(open_squares) - len(causes),
    }


def census_count(unit: tuple[Path, int, Mapping[int, Mapping[str, Any]]]) -> dict[str, Any]:
    tree, n, entries = unit
    drawing, witness = drawing_for(tree, n, entries)
    return {
        "n": n,
        "drawing": {
            "kind": drawing.kind,
            "path": drawing.path,
            "generator": drawing.generator,
        },
        **regularity(witness),
    }


TOTALLED = ("axis", "light_axis", "uneven_axis", "near_axis", "small_tilt", "variation")


def totals(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {key: sum(int(row[key]) for row in rows) for key in TOTALLED}
    result["counts"] = len(rows)
    result["drawn_from_views"] = sum(
        1 for row in rows if row["drawing"]["kind"] == "regularized-view"
    )
    result["counts_with_light_axis"] = sum(1 for row in rows if row["light_axis"])
    result["counts_with_near_axis"] = sum(1 for row in rows if row["near_axis"])
    for key in ("light_faces", "open_faces"):
        faces: Counter[str] = Counter()
        for row in rows:
            faces.update(row[key])
        result[key] = {cause: faces[cause] for cause in FACE_CAUSES if faces[cause]}
    sides = [0] * 5
    for row in rows:
        sides = [total + value for total, value in zip(sides, row["axis_sides"], strict=True)]
    result["axis_sides"] = sides
    return result


def census(tree: Path, counts: Sequence[int], *, workers: int = 1) -> dict[str, Any]:
    """The census document for `counts` of `tree`'s atlas."""
    entries = read_index(tree)
    units = [(tree, n, entries) for n in counts]
    if workers > 1 and len(units) > 1:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            rows = list(pool.map(census_count, units, chunksize=4))
    else:
        rows = [census_count(unit) for unit in units]
    return {
        "format": FORMAT,
        "generated_by": GENERATOR,
        "tree": str(tree),
        "rules": {
            "renderer": "sqpack.render.color.assign_square_colors at the default RenderSpec",
            "axis_tolerance_radians": str(AXIS_TOLERANCE),
            "contact_tolerance": str(SPEC.full_side_contact_tolerance),
            "light_max_sides": LIGHT_MAX_SIDES,
            "near_axis_degrees": NEAR_AXIS_DEGREES,
            "small_tilt_degrees": SMALL_TILT_DEGREES,
            "variation": "uneven_axis + near_axis",
            "hard_causes": sorted(HARD),
        },
        "totals": totals(rows),
        "counts": rows,
    }


# --------------------------------------------------------------------------- comparison


def compare(before: Mapping[str, Any], after: Mapping[str, Any]) -> list[dict[str, Any]]:
    """One row per count in both censuses, worst `after` variation first."""
    earlier = {int(row["n"]): row for row in before["counts"]}
    rows: list[dict[str, Any]] = []
    for row in after["counts"]:
        n = int(row["n"])
        if n not in earlier:
            continue
        old = earlier[n]
        rows.append(
            {
                "n": n,
                "before": {key: old[key] for key in (*TOTALLED, "drawing")},
                "after": {key: row[key] for key in (*TOTALLED, "drawing", "light_faces")},
                "change": int(row["variation"]) - int(old["variation"]),
            }
        )
    rows.sort(key=lambda item: (-item["after"]["variation"], item["n"]))
    return rows


def source_label(drawing: Mapping[str, Any]) -> str:
    """Which generator a drawing's view came from, by its index entry's generator: the
    layer's own name for it, or the driver's command line, which an older tree's index
    and a census written from one record instead."""
    if drawing["kind"] == "witness":
        return "witness"
    generator = str(drawing.get("generator") or "")
    if generator == EVAND_GENERATOR or "regularize_evand" in generator:
        return "Evan view"
    return "grid view" if "regularize_grid_slack" in generator else "axis view"


def ranking_markdown(rows: Sequence[Mapping[str, Any]], *, top: int) -> str:
    """The comparison's worst `top` counts as a Markdown table."""
    lines = [
        (
            "| n | before: drawn from | light / uneven / axis | near-axis "
            "| after: drawn from | light / uneven / axis | near-axis | variation | change "
            "| open faces of light squares |"
        ),
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows[:top]:
        old, new = row["before"], row["after"]
        faces = ", ".join(f"{cause} {count}" for cause, count in new["light_faces"].items())
        lines.append(
            f"| {row['n']} | {source_label(old['drawing'])} "
            f"| {old['light_axis']} / {old['uneven_axis']} / {old['axis']} "
            f"| {old['near_axis']} | {source_label(new['drawing'])} "
            f"| {new['light_axis']} / {new['uneven_axis']} / {new['axis']} "
            f"| {new['near_axis']} | {new['variation']} | {row['change']:+d} | {faces or '-'} |"
        )
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- command line


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_text(text, encoding="utf-8")


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    command.add_argument("--tree", type=Path, default=REPO, help="checkout to read")
    command.add_argument("--n", type=int, nargs="+", help="counts (default 1..324)")
    command.add_argument("--workers", type=int, default=1, help="processes (default 1)")
    command.add_argument("--output", type=Path, help="write the census JSON here")
    command.add_argument("--json", action="store_true", help="print the census JSON")
    command.add_argument(
        "--compare", type=Path, nargs=2, metavar=("BEFORE", "AFTER"), help="rank two censuses"
    )
    command.add_argument("--top", type=int, default=25, help="rows of the ranking")
    command.add_argument("--markdown", type=Path, help="write the ranking table here")
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.compare:
        before, after = (json.loads(path.read_text(encoding="utf-8")) for path in args.compare)
        rows = compare(before, after)
        table = ranking_markdown(rows, top=args.top)
        if args.markdown:
            _write(args.markdown, table)
        print(table, end="")
        return 0
    counts = args.n or list(COUNTS)
    document = census(args.tree.resolve(), counts, workers=args.workers)
    text = json.dumps(document, indent=1) + "\n"
    if args.output:
        _write(args.output, text)
    if args.json:
        print(text, end="")
    else:
        total = document["totals"]
        print(
            f"{total['counts']} counts ({total['drawn_from_views']} from views): "
            f"{total['light_axis']} light of {total['axis']} axis squares in "
            f"{total['counts_with_light_axis']} counts; {total['near_axis']} near-axis "
            f"squares in {total['counts_with_near_axis']} counts"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
