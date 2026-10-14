#!/usr/bin/env python3
"""Draw a regularization run for review: each count's source witness beside its views.

Usage, from `packing/`, each after `uv run --frozen --all-extras --group dev`:

    python -m devtools.regularize_gallery --run-dir RUN --output gallery.html \
        [--n N ...] [--with-current-layer] [--title TEXT] [--workers K]
    python -m devtools.regularize_gallery --current-layer --output layer.html \
        [--n N ...] [--title TEXT] [--workers K]

The regularization policy (`docs/project/policies/regularization-policy.md`, section 5,
"What the reviewer sees") asks for a gallery a reviewer decides from. This writes it as
one self-contained HTML page: inline SVG, the stylesheet `regularize_gallery.css` beside
this file inlined, and no script. It reads a run directory in the layout
`devtools.regularize_evand` writes (`n-NNN/report.json`, `view-same.yaml`,
`view-solved.yaml`) and draws, for each count, side by side:

- **Source**: the atlas witness the report names (`packing/witnesses/known-best/` by
  default), with a note when its scalar kind or side is no longer what the report
  recorded, which means the record changed after the run;
- **Regularized**: the run's chosen view, `view-same.yaml` when the same-side re-solve
  succeeded and `view-solved.yaml` otherwise, labelled with its side relation; a
  same-side view the report keeps under `same_above_bound`, set aside because the
  witness's side is above `U`, is noted as such and not drawn, and any other view file
  the count's report records no output for is an earlier run's, noted and not drawn;
- **Current layer**, with `--with-current-layer`: the view
  `atlas/known-best/regularized/index.json` holds for the count, which is the other
  generator's (`regularize_axis_components/2`), when the index has one.

`--current-layer` draws the layer alone, each regularized record's source against its
layer view, with no run: the before-and-after of the drawings the site shows now.

**Drawings.** Every panel is the house renderer's drawing, `frame_from_witness` and
`sqpack.render.render_packing_svg` at the settings `devtools.render_regularized_atlas`
uses; the current-layer panel is that module's own `render`. A view is drawn under the
source's evidence tier, as that module draws one, so no panel promotes anything. Hue is a
square's angle class and shade is how many of its four sides it shares whole with a wall
or a same-angle neighbour (`sqpack.render.color`): a regular structure reads as few hue
families in dark shades, slack as stray light squares, angle noise as extra hue classes.
The page inlines a reduction of each drawing read back from the renderer's SVG: the fill
the renderer chose for each square, its corners rounded to a hundredth of a drawing pixel
(a tenth above n = 150, which keeps a full run of three panels well under the 16 MB a
published page may hold), the outlines and the container, and nothing else. The renderer
draws every container at one pixel size, so panels of one width are at one scale to
within the relative difference of their sides, which the table prints. A view is drawn
in its own frame; when it matches its source only under a symmetry of the box other than
the identity, the table says which, rather than the drawing hiding it.

**Measurements**, per panel and from the drawings unless the report is named:

- hue classes: the distinct angle classes the renderer assigned (`data-angle-class`),
  split into right angles, 45-degree tilts and the rest, the renderer's pinned hues;
- house shades: squares by full-side contact count, 0 to 4, as drawn
  (`data-contact-sides`), and whether the census's float replica of that rule
  (`census_atlas_contact_shades.edge_rule_contacts`) agrees square by square;
- stage counts: the workbench rule, `centre_rule_contacts` at gap 0.01 and half a degree;
- sides: the policy's s_W (a rational witness's side; for a decimal witness the side of
  its 36-digit rational promotion at dilation 1, which is not always the printed side)
  and each view's exact `s_V - s_W`. In `--current-layer` mode the side relation is
  derived from that difference, `same` only when it is exactly zero;
- moves and turns: each source square matched to the nearest view centre under the best
  of the box's eight symmetries, the matching `check_half_angle_area.arrangement_gap`
  makes, here in binary64 on the drawn frames. A square moved beyond `1e-3` or turned by
  a sine above `1e-6` is outlined in its panel and listed under it. The outlines are a
  drawing aid; the identity the policy decides on is the report's exact measurement,
  printed beside them, and a disagreement between the two is flagged.

The report's own fields (side relation, the verified upper bound, identity, shade
histograms and regressions, generator, variant, level, symmetry, angle changes, the
decision row) are shown as the run recorded them. The page decides nothing: its verdict
chip is the report's decision, and in `--current-layer` mode the index's status.
"""

from __future__ import annotations

import argparse
import gzip
import html
import json
import math
import sys
from collections.abc import Callable, Iterable, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, replace
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Literal
from xml.etree import ElementTree as ET

import yaml
from strif import atomic_output_file

from devtools import census_atlas_contact_shades as shades
from devtools import render_regularized_atlas as layer
from devtools.build_known_best_atlas import frame_from_witness
from devtools.regularize_axis_components import ALGORITHM, HOUSE_RULE, STAGE_RULE, histogram
from devtools.upper_bound_packets import RATIONAL_DIGITS
from sqpack.render import render_packing_svg
from sqpack.render.color import DIAGONAL_HUE, RIGHT_ANGLE_HUE, square_fill_palette
from sqpack.render.model import PackingFrame, RenderSpec
from sqpack.witness import (
    WitnessError,
    _promoted_candidate,  # pyright: ignore[reportPrivateUsage]
)
from sqpack.workers import worker_count
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
STYLESHEET = Path(__file__).resolve().with_suffix(".css")
GENERATOR = "python -m devtools.regularize_gallery"
DEFAULT_TITLE = "Regularization Review Gallery"
WITNESSES = "packing/witnesses/known-best"

SPEC = RenderSpec(overlays=frozenset())
"""The house atlas's drawing settings, as `build_known_best_atlas` and
`render_regularized_atlas` pass them; title and description do not change a drawing."""
MOVED_BEYOND = 1e-3
"""A square whose centre moved farther than this is outlined: the policy's `moved`."""
TURN_SINE = 1e-6
"""A square whose orientation changed by a sine above this turned (obligation 3)."""
LARGE_N = 150
"""Above this count a drawing's corners keep a tenth of a pixel rather than a hundredth."""
PAGE_LIMIT = 16_000_000
"""Bytes: the most a published page may hold. A larger page is refused, not written."""
PAD = Decimal(8)
"""Drawing pixels of paper kept around the container."""
LIST_LIMIT = 40
"""Square numbers listed under a panel before the rest are counted."""
SVG = "{http://www.w3.org/2000/svg}"
DASH = "\u2013"
"""An en dash: what an empty cell shows."""
MINUS = "\u2212"
"""A minus sign, for differences written as formulas."""
DECISION_CHIPS = {
    "admit": ("admitted", "admit"),
    "no-change": ("no change", "unchanged"),
    "no-view": ("no view", "unchanged"),
    "held": ("held", "candidate"),
    "review": ("review", "review"),
    "alternate": ("alternate", "alternate"),
    "refuse": ("refused", "refuse"),
    # The words runs wrote before the owner's reporting vocabulary of 11 October 2026.
    "candidate": ("held", "candidate"),
    "unchanged": ("no change", "unchanged"),
}
"""How each reported decision (policy section 4, "How a decision is reported") reads as a
chip: its text and its colour class. "Refused" is red only for a view that would change
the drawing and fails an obligation; no change and no view are neutral."""
LAYER_CHIPS = {
    "regularized": ("in layer", "admit"),
    # The axis tool's "refused" means it made no view of the record: nothing was rejected.
    "refused": ("no view", "unchanged"),
    "unchanged": ("no change", "unchanged"),
}
"""How an index status reads as a chip in `--current-layer` mode."""

Role = Literal["source", "view", "layer"]
HEADINGS: dict[Role, str] = {
    "source": "Source",
    "view": "Regularized",
    "layer": "Current layer",
}


class GalleryError(ValueError):
    """An input the gallery cannot read or draw; it is shown on the page in its place."""


# --------------------------------------------------------------------------------------
# Reading inputs
# --------------------------------------------------------------------------------------


def display_path(path: Path) -> str:
    """Repository-relative when the path is inside the repository, else as given."""
    try:
        return path.resolve().relative_to(REPO.resolve()).as_posix()
    except ValueError:
        return str(path)


def resolve(text: str) -> Path:
    """A path a report records: absolute, or relative to the repository root."""
    path = Path(text)
    return path if path.is_absolute() else REPO / path


def read_witness(path: Path) -> dict[str, Any]:
    """The `witness` body of a Witness/v2 file, plain or gzipped."""
    try:
        raw = path.read_bytes()
        text = (gzip.decompress(raw) if path.suffix == ".gz" else raw).decode("utf-8")
        document = load_yaml(text)
    except (OSError, ValueError, yaml.YAMLError) as error:
        raise GalleryError(f"{display_path(path)}: {error}") from error
    if not isinstance(document, dict) or not isinstance(document.get("witness"), dict):
        raise GalleryError(f"{display_path(path)} is not a witness document")
    return document["witness"]


def read_json(path: Path) -> dict[str, Any]:
    """A JSON object, or an empty one when the file is absent."""
    if not path.is_file():
        return {}
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise GalleryError(f"{display_path(path)}: {error}") from error
    if not isinstance(document, dict):
        raise GalleryError(f"{display_path(path)} is not a JSON object")
    return document


def field(record: Any, *keys: str) -> Any:
    """`record[k1][k2]...`, or None where any step is missing or not a mapping."""
    for key in keys:
        if not isinstance(record, Mapping):
            return None
        record = record.get(key)
    return record


def exact_side(witness: Mapping[str, Any]) -> Fraction | None:
    """The side a witness states, as a rational: exact for a rational witness, the printed
    side for a decimal one, and None for a number-field side."""
    side = witness.get("side")
    if field(witness, "scalar", "kind") == "algebraic-number-field" or not isinstance(
        side, str | int
    ):
        return None
    try:
        return Fraction(str(side))
    except ValueError, ZeroDivisionError:
        return None


def source_side(witness: Mapping[str, Any]) -> Fraction | None:
    """The policy's s_W: a rational witness's exact side, and for a decimal centre-angle
    witness the side of its 36-digit rational promotion at centre dilation 1, which can
    differ from the printed side in the fifteenth decimal. A decimal witness written as
    corners has no promotion and keeps its printed side."""
    if field(witness, "scalar", "kind") == "decimal":
        try:
            _squares, side = _promoted_candidate(
                witness, rational_digits=RATIONAL_DIGITS, dilation=Fraction(1)
            )
        except WitnessError, KeyError, ValueError:
            return exact_side(witness)
        return side
    return exact_side(witness)


def rational(text: Any) -> Fraction | None:
    """A decimal or `p/q` text as a rational, or None."""
    if not isinstance(text, str | int):
        return None
    try:
        return Fraction(str(text))
    except ValueError, ZeroDivisionError:
        return None


# --------------------------------------------------------------------------------------
# The house drawing, read back
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class DrawnSquare:
    """One square as the house renderer drew it: drawing-pixel corners and its colour."""

    square_id: str
    corners: tuple[tuple[Decimal, Decimal], ...]
    fill: str
    hue: int
    angle_class: int | None
    contacts: int


@dataclass(frozen=True)
class HouseDrawing:
    """What `render_packing_svg` drew for one frame, read back from its SVG."""

    paper: str
    container: tuple[Decimal, Decimal, Decimal]
    """The container's top-left corner and side, in drawing pixels."""
    stroke: str
    stroke_width: str
    fill_opacity: str
    squares: tuple[DrawnSquare, ...]
    caption: str

    def contact_counts(self) -> list[int]:
        return [square.contacts for square in self.squares]

    def class_split(self) -> tuple[int, int, int, int]:
        """Angle classes in all, then those on the right-angle hue, the 45-degree hue and
        the rest: the renderer pins the first two hues to those orientations."""
        hues: dict[int | None, int] = {}
        for square in self.squares:
            hues.setdefault(square.angle_class, square.hue)
        right = sum(1 for hue in hues.values() if hue == RIGHT_ANGLE_HUE)
        diagonal = sum(1 for hue in hues.values() if hue == DIAGONAL_HUE)
        return len(hues), right, diagonal, len(hues) - right - diagonal


def _corners(points: str) -> tuple[tuple[Decimal, Decimal], ...]:
    pairs = (pair.split(",") for pair in points.split())
    return tuple((Decimal(x), Decimal(y)) for x, y in pairs)


def read_house_svg(text: str) -> HouseDrawing:
    """The fills, contact counts, angle classes and geometry the renderer emitted."""
    root = ET.fromstring(text)
    rects = list(root.iter(f"{SVG}rect"))
    paper = next((rect.get("fill") for rect in rects if rect.get("data-feature") is None), None)
    container = next(
        (rect for rect in rects if rect.get("data-feature") == "container-outline"), None
    )
    polygons = list(root.iter(f"{SVG}polygon"))
    fills = [polygon for polygon in polygons if polygon.get("data-feature") == "square-fill"]
    outline = next(
        (polygon for polygon in polygons if polygon.get("data-feature") == "square-outline"),
        None,
    )
    if container is None or outline is None or not fills:
        raise GalleryError("the renderer's SVG has no container, outline or fills")
    squares = tuple(
        DrawnSquare(
            square_id=str(polygon.get("data-square")),
            corners=_corners(str(polygon.get("points"))),
            fill=str(polygon.get("fill")),
            hue=int(str(polygon.get("data-hue-index"))),
            angle_class=(
                int(str(polygon.get("data-angle-class")))
                if polygon.get("data-angle-class") is not None
                else None
            ),
            contacts=int(str(polygon.get("data-contact-sides", "0"))),
        )
        for polygon in fills
    )
    caption = next(
        (node.text or "" for node in root.iter(f"{SVG}text") if node.get("data-evidence")),
        "",
    )
    return HouseDrawing(
        paper=paper or "#ffffff",
        container=(
            Decimal(str(container.get("x"))),
            Decimal(str(container.get("y"))),
            Decimal(str(container.get("width"))),
        ),
        stroke=str(outline.get("stroke", "#000000")),
        stroke_width=str(outline.get("stroke-width", "1")),
        fill_opacity=str(fills[0].get("fill-opacity", "1")),
        squares=squares,
        caption=caption,
    )


def _number(value: Decimal, decimals: int) -> str:
    text = f"{value:.{decimals}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return "0" if text in {"", "-0"} else text


def drawing_svg(
    drawing: HouseDrawing,
    *,
    ident: str,
    label: str,
    decimals: int,
    marked: Iterable[str] = (),
) -> str:
    """The drawing as a compact inline `<svg>`: one path per fill colour, the outlines
    drawn over them by reference, the container, and the marked squares outlined.

    Paint order is the renderer's: every fill, then every outline, then the container.
    Strokes keep the renderer's width in screen pixels (`non-scaling-stroke`).
    """
    x0, y0, size = drawing.container

    def path(square: DrawnSquare) -> str:
        points = (
            f"{_number(x - x0 + PAD, decimals)} {_number(y - y0 + PAD, decimals)}"
            for x, y in square.corners
        )
        return "M" + "L".join(points) + "Z"

    groups: dict[str, list[str]] = {}
    for square in drawing.squares:
        groups.setdefault(square.fill, []).append(path(square))
    extent = _number(size + 2 * PAD, decimals)
    pad = _number(PAD, decimals)
    side = _number(size, decimals)
    fills: list[str] = []
    uses: list[str] = []
    for index, (fill, paths) in enumerate(groups.items()):
        identifier = f"{ident}-f{index}"
        fills.append(
            f'<g fill="{fill}"><path id="{identifier}" vector-effect="non-scaling-stroke" '
            f'd="{"".join(paths)}"/></g>'
        )
        uses.append(f'<use href="#{identifier}"/>')
    wanted = set(marked)
    marks = "".join(path(square) for square in drawing.squares if square.square_id in wanted)
    stroke = f'stroke="{drawing.stroke}" stroke-width="{drawing.stroke_width}"'
    parts = [
        (
            f'<svg class="drawing" viewBox="0 0 {extent} {extent}" role="img" '
            f'aria-labelledby="{ident}-title">'
        ),
        f'<title id="{ident}-title">{html.escape(label)}</title>',
        f'<rect width="{extent}" height="{extent}" fill="{drawing.paper}"/>',
        f'<g fill-opacity="{drawing.fill_opacity}">{"".join(fills)}</g>',
        f'<g fill="none" {stroke} stroke-linejoin="round">{"".join(uses)}</g>',
        (
            f'<rect x="{pad}" y="{pad}" width="{side}" height="{side}" fill="none" {stroke} '
            'vector-effect="non-scaling-stroke"/>'
        ),
    ]
    if marks:
        parts.append(f'<path class="mark-halo" d="{marks}"/><path class="mark" d="{marks}"/>')
    parts.append("</svg>")
    return "".join(parts)


# --------------------------------------------------------------------------------------
# Measurements
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Motion:
    """Where each source square went in a view, matched as `arrangement_gap` matches."""

    symmetry: int
    """The box symmetry, numbered as `check_half_angle_area.symmetric` numbers them."""
    partner: tuple[int, ...]
    """For each source square, the index of the view square matched to it."""
    move: tuple[float, ...]
    turn_degrees: tuple[float, ...]

    def moved(self) -> list[int]:
        return [index for index, move in enumerate(self.move) if move > MOVED_BEYOND]

    def turned(self) -> list[int]:
        return [
            index
            for index, turn in enumerate(self.turn_degrees)
            if math.sin(math.radians(turn)) > TURN_SINE
        ]


Pose = tuple[float, float, float]


def frame_poses(frame: PackingFrame) -> tuple[float, list[Pose]]:
    """The frame's side, and each square's centre and orientation in degrees modulo 90,
    in binary64 from its drawn corners."""
    poses: list[Pose] = []
    for square in frame.squares:
        xs = [float(point.x.projected) for point in square.corners]
        ys = [float(point.y.projected) for point in square.corners]
        angle = math.degrees(math.atan2(ys[1] - ys[0], xs[1] - xs[0])) % 90.0
        poses.append((sum(xs) / len(xs), sum(ys) / len(ys), angle))
    return float(frame.container_side.projected), poses


def symmetric(side: float, pose: Pose, k: int) -> Pose:
    """`pose` under the `k`-th symmetry of `[0, side]^2`: a reflection in `x = side/2`
    when `k >= 4`, then `k mod 4` quarter turns about the centre, as
    `check_half_angle_area.symmetric` numbers them."""
    x, y, angle = pose
    if k >= 4:
        x, angle = side - x, -angle
    for _turn in range(k % 4):
        x, y = side - y, x
    return x, y, angle % 90.0


def square_motions(source: PackingFrame, view: PackingFrame) -> Motion | None:
    """Each source square's move and turn into `view` under the best box symmetry: the
    one that pairs the squares one to one with the smallest largest move. None when no
    symmetry pairs them one to one."""
    _side, left = frame_poses(source)
    other_side, right = frame_poses(view)
    if len(left) != len(right):
        return None
    best: tuple[float, int, list[Pose], list[tuple[float, int]]] | None = None
    for k in range(8):
        mapped = [symmetric(other_side, pose, k) for pose in right]
        nearest = [
            min(((x - u) ** 2 + (y - v) ** 2, j) for j, (u, v, _a) in enumerate(mapped))
            for x, y, _angle in left
        ]
        if len({j for _distance, j in nearest}) != len(left):
            continue
        largest = max(distance for distance, _j in nearest)
        if best is None or largest < best[0]:
            best = (largest, k, mapped, nearest)
    if best is None:
        return None
    _largest, k, mapped, nearest = best
    turns: list[float] = []
    for (_x, _y, angle), (_distance, j) in zip(left, nearest, strict=True):
        difference = (mapped[j][2] - angle) % 90.0
        turns.append(min(difference, 90.0 - difference))
    return Motion(
        symmetry=k,
        partner=tuple(j for _distance, j in nearest),
        move=tuple(math.sqrt(distance) for distance, _j in nearest),
        turn_degrees=tuple(turns),
    )


def census_counts(witness: Mapping[str, Any]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Each square's contact count under the census's float replica of the house rule
    and under the workbench stage rule, in witness order."""
    exact, framed, _degrees = shades.packings_from_witness(dict(witness))
    house = tuple(min(4, len(found)) for found in shades.edge_rule_contacts(exact, HOUSE_RULE))
    stage = tuple(
        min(4, len(found)) for found in shades.centre_rule_contacts(framed, STAGE_RULE)
    )
    return house, stage


# --------------------------------------------------------------------------------------
# Panels and counts
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Panel:
    """One drawing of a count, with what was measured on it."""

    role: Role
    detail: str
    drawing: HouseDrawing | None = None
    side: Fraction | None = None
    house_replica: tuple[int, ...] | None = None
    stage: tuple[int, ...] | None = None
    motion: Motion | None = None
    error: str | None = None


@dataclass(frozen=True)
class CountCase:
    """Everything one count's section shows."""

    n: int
    mode: Literal["run", "layer"]
    """Whether the count comes from a run, or from the current layer with no run."""
    report: dict[str, Any]
    panels: tuple[Panel, ...]
    relation: str | None = None
    """The drawn view's side relation, `same`, `bound` or `solved`."""
    layer_status: str | None = None
    """The current layer's index status for the count, when the layer was consulted."""
    notes: tuple[str, ...] = ()

    def panel(self, role: Role) -> Panel | None:
        return next((panel for panel in self.panels if panel.role == role), None)

    def after(self) -> Panel | None:
        """The panel the before-and-after measurements compare with the source: the run's
        view, or the current layer's when there is no run view."""
        return self.panel("view") or self.panel("layer")


DRAW_ERRORS = (GalleryError, KeyError, ValueError, TypeError)
"""What reading or drawing a malformed witness raises; shown in the panel's place."""


def source_panel(witness: Mapping[str, Any]) -> tuple[Panel, PackingFrame]:
    frame = frame_from_witness(dict(witness))
    house, stage = census_counts(witness)
    panel = Panel(
        role="source",
        detail=str(witness.get("id", "")),
        drawing=read_house_svg(render_packing_svg(frame, spec=SPEC)),
        side=source_side(witness),
        house_replica=house,
        stage=stage,
    )
    return panel, frame


def view_panel(
    view: Mapping[str, Any], relation: str, source_frame: PackingFrame | None
) -> Panel:
    """A run view drawn as `render_regularized_atlas.regularized_frame` draws a layer
    view: its geometry under the record's tier and check, never its own."""
    frame = frame_from_witness(dict(view))
    if source_frame is not None:
        frame = replace(
            frame,
            evidence=source_frame.evidence,
            check=source_frame.check,
            source_url=source_frame.source_url,
        )
    house, stage = census_counts(view)
    return Panel(
        role="view",
        detail=f"{view.get('id', '')}, side relation {relation}",
        drawing=read_house_svg(render_packing_svg(frame, spec=SPEC)),
        side=exact_side(view),
        house_replica=house,
        stage=stage,
        motion=square_motions(source_frame, frame) if source_frame is not None else None,
    )


def layer_panel(entry: dict[str, Any], source_frame: PackingFrame | None) -> Panel:
    """The current layer's drawing of the count, by `render_regularized_atlas` itself."""
    try:
        text = layer.render(entry)
        frame = layer.regularized_frame(entry)
        view = layer.view_witness(entry)
    except SystemExit as error:
        raise GalleryError(str(error.code)) from error
    house, stage = census_counts(view)
    return Panel(
        role="layer",
        detail=f"{view.get('id', '')}, by {ALGORITHM}",
        drawing=read_house_svg(text),
        side=exact_side(view),
        house_replica=house,
        stage=stage,
        motion=square_motions(source_frame, frame) if source_frame is not None else None,
    )


def _failed(role: Role, error: Exception) -> Panel:
    return Panel(role=role, detail="", error=str(error) or type(error).__name__)


SIDE_AGREEMENT = Fraction(1, 10**25)
"""Relative: a recorded s_W within this of the witness's side is the same side, so a
rational side the report printed as a long decimal still reads as itself."""


def _changed_source(witness: Mapping[str, Any], recorded: Any) -> str | None:
    """Why the witness is not the one the report recorded, by the semantic identity the
    report carries (its scalar kind and s_W), or None when it agrees or nothing was
    recorded. Drift is reported beside the drawing, never refused (`OR-16`)."""
    kind, side = field(witness, "scalar", "kind"), source_side(witness)
    recorded_kind, recorded_side = field(recorded, "kind"), rational(field(recorded, "s_W"))
    if isinstance(recorded_kind, str) and recorded_kind != kind:
        return f"the run read a {recorded_kind} witness; the record now holds a {kind} one"
    if (
        recorded_side is not None
        and side is not None
        and abs(recorded_side - side) > SIDE_AGREEMENT * side
    ):
        return (
            f"the run read s_W = {_side_text(recorded_side)}; the witness's side is now "
            f"{_side_text(side)}"
        )
    return None


def _source(path: Path, recorded: Any, notes: list[str]) -> tuple[Panel, PackingFrame | None]:
    try:
        witness = read_witness(path)
        changed = _changed_source(witness, recorded)
        if changed is not None:
            notes.append(
                f"{display_path(path)} has changed since the run: {changed}. The source "
                "drawn is today's witness, not the run's input."
            )
        return source_panel(witness)
    except DRAW_ERRORS as error:
        return _failed("source", error), None


def run_case(count_dir: Path, layer_index: Mapping[int, dict[str, Any]] | None) -> CountCase:
    """One count of a run: its report, source, chosen view and, when asked, the layer's."""
    n = int(count_dir.name.removeprefix("n-"))
    notes: list[str] = []
    try:
        report = read_json(count_dir / "report.json")
    except GalleryError as error:
        report, notes = {}, [str(error)]
    if not report:
        notes.append("no report.json: the run's measurements and decision are missing.")
    source_text = field(report, "source", "path") or f"{WITNESSES}/n-{n:03d}.yaml"
    source, source_frame = _source(resolve(str(source_text)), field(report, "source"), notes)
    panels = [source]
    relation = None
    for relation_name in ("same", "solved"):
        path = count_dir / f"view-{relation_name}.yaml"
        if not path.is_file():
            continue
        if report and field(report, "outputs", relation_name) is None:
            if relation_name == "same" and field(report, "outputs", "same_above_bound"):
                # This run's own same-side view, which `yield_to_bound` set aside.
                notes.append(
                    f"{path.name} is this run's same-side view, set aside: the witness's "
                    "side is above U, so the view at the bound is decided and drawn."
                )
                continue
            # A view the report does not name is an earlier run's, left on disk.
            notes.append(
                f"{path.name} is on disk but the report records no {relation_name} "
                "output: an earlier run's file, not drawn."
            )
            continue
        # The report's relation where it has one: the solved view may be `bound`.
        stored = field(report, "outputs", relation_name, "relation")
        relation = str(stored) if stored else relation_name
        try:
            panels.append(view_panel(read_witness(path), relation, source_frame))
        except DRAW_ERRORS as error:
            panels.append(_failed("view", error))
        break
    view, source_side = panels[-1], source.side
    if (
        relation == "same"
        and view.side is not None
        and source_side is not None
        and view.side != source_side
    ):
        difference = difference_text(view.side - source_side)
        notes.append(
            f"view-same.yaml's side differs from s_W by {difference}: by the policy's "
            "definitions it is not a same-side view."
        )
    layer_status = None
    if layer_index is not None:
        entry = layer_index.get(n)
        layer_status = str(entry["status"]) if entry else "absent"
        if entry is not None and entry["status"] == "regularized":
            try:
                panels.append(layer_panel(entry, source_frame))
            except DRAW_ERRORS as error:
                panels.append(_failed("layer", error))
    return CountCase(
        n=n,
        mode="run",
        report=report,
        panels=tuple(panels),
        relation=relation,
        layer_status=layer_status,
        notes=tuple(notes),
    )


def layer_case(entry: dict[str, Any]) -> CountCase:
    """One record of the current layer: its source and, when it has one, its view."""
    notes: list[str] = []
    source, source_frame = _source(resolve(str(entry["source"]["witness"])), None, notes)
    panels = [source]
    relation = None
    if entry["status"] == "regularized":
        try:
            panel = layer_panel(entry, source_frame)
        except DRAW_ERRORS as error:
            panel = _failed("layer", error)
        panels.append(panel)
        if panel.side is not None and source.side is not None:
            relation = "same" if panel.side == source.side else "solved"
    return CountCase(
        n=int(entry["n"]),
        mode="layer",
        report={},
        panels=tuple(panels),
        relation=relation,
        layer_status=str(entry["status"]),
        notes=tuple(notes),
    )


def index_entries(path: Path = layer.INDEX) -> dict[int, dict[str, Any]]:
    """Every record of the current layer's index, by count, whatever its status."""
    layer.regularized_entries(replace(layer.LAYOUT, index=path))
    index = json.loads(path.read_text(encoding="utf-8"))
    return {int(entry["n"]): entry for entry in index["entries"]}


# --------------------------------------------------------------------------------------
# The page
# --------------------------------------------------------------------------------------


def _e(value: Any) -> str:
    return html.escape(str(value), quote=True)


def short(value: Any, limit: int = 220) -> str:
    """A report value as one line of text."""
    if value is None:
        return "not recorded"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, list | tuple) and not value:
        return "none"
    if isinstance(value, list | tuple):
        text = ", ".join(
            json.dumps(item, separators=(",", ":"))
            if isinstance(item, dict | list)
            else str(item)
            for item in value
        )
    elif isinstance(value, dict):
        text = json.dumps(value, separators=(", ", ": "))
    else:
        text = str(value)
    return text if len(text) <= limit else text[: limit - 1] + "…"


def difference_text(value: Fraction) -> str:
    """An exact difference as a short signed decimal; zero is written `0`."""
    if value == 0:
        return "0"
    with localcontext() as context:
        context.prec = 3
        quotient = Decimal(value.numerator) / Decimal(value.denominator)
    return f"{quotient:+.2e}"


def _side_text(side: Fraction | None) -> str:
    if side is None:
        return "not rational"
    with localcontext() as context:
        context.prec = 12
        return str(Decimal(side.numerator) / Decimal(side.denominator))


def _arrow(before: Any, after: Any) -> str:
    if after is None:
        return str(before)
    return f"{before} → {after}"


def _square_list(indices: Sequence[int]) -> str:
    if not indices:
        return "none"
    shown = ", ".join(str(index + 1) for index in indices[:LIST_LIMIT])
    rest = len(indices) - LIST_LIMIT
    return shown if rest <= 0 else f"{shown} and {rest} more"


def chip(case: CountCase) -> tuple[str, str]:
    """The verdict chip's text and colour class."""
    if case.mode == "run":
        decision = field(case.report, "decision", "decision")
        if isinstance(decision, str) and decision in DECISION_CHIPS:
            return DECISION_CHIPS[decision]
        status = field(case.report, "status")
        if isinstance(status, str) and status != "ok":
            # A count the run could not decide made no view: neutral, never "refused".
            return status.replace("-", " "), "unchanged"
        return "no decision", "none"
    status = case.layer_status or "absent"
    return LAYER_CHIPS.get(status, (status, "unchanged"))


def _chip_html(case: CountCase) -> str:
    text, tone = chip(case)
    return f'<span class="chip chip-{_e(tone)}">{_e(text)}</span>'


def _hist(counts: Sequence[int] | None) -> str:
    if counts is None:
        return '<span class="muted">not measured</span>'
    cells = "".join(f"<span>{count}</span>" for count in counts)
    return f'<span class="hist" title="squares with 0, 1, 2, 3, 4 sides">{cells}</span>'


def _classes(panel: Panel | None) -> str:
    if panel is None or panel.drawing is None:
        return DASH
    total, right, diagonal, other = panel.drawing.class_split()
    parts = [f"{right} at 0°"] if right else []
    if diagonal:
        parts.append(f"{diagonal} at 45°")
    if other:
        parts.append(f"{other} other")
    return f"{total} ({', '.join(parts)})" if parts else str(total)


def _dark(panel: Panel | None) -> int | None:
    if panel is None or panel.drawing is None:
        return None
    return sum(1 for count in panel.drawing.contact_counts() if count == 4)


def _dark_text(panel: Panel | None) -> str:
    dark = _dark(panel)
    return DASH if dark is None else str(dark)


def _moved_count(case: CountCase) -> str:
    recorded = field(case.report, "identity", "moved")
    if recorded is not None:
        return str(recorded)
    after = case.after()
    if after is None or after.motion is None:
        return DASH
    return str(len(after.motion.moved()))


def summary_rows(cases: Sequence[CountCase]) -> str:
    rows: list[str] = []
    for case in cases:
        source, after = case.panel("source"), case.after()
        before_classes = source.drawing.class_split()[0] if source and source.drawing else DASH
        after_classes = after.drawing.class_split()[0] if after and after.drawing else None
        rows.append(
            "<tr>"
            f'<td class="num"><a href="#n-{case.n:03d}">{case.n}</a></td>'
            f"<td>{_chip_html(case)}</td>"
            f'<td class="num">{_e(_arrow(before_classes, after_classes))}</td>'
            f'<td class="num">{_e(_arrow(_dark_text(source), _dark(after)))}</td>'
            f'<td class="num">{_e(_moved_count(case))}</td>'
            f"<td>{_e(case.relation or DASH)}</td>"
            "</tr>"
        )
    return "".join(rows)


def summary_line(case: CountCase) -> str:
    """One count's before-and-after as a line of text, the page's numbers for a terminal."""
    source, after = case.panel("source"), case.after()
    text, _tone = chip(case)

    def pair(measure: Callable[[Panel | None], Any]) -> str:
        return _arrow(measure(source), measure(after) if after is not None else None)

    motion = after.motion if after is not None else None
    moved = (
        f"moved {len(motion.moved())}, turned {len(motion.turned())}, "
        f"largest {max(motion.move, default=0.0):.3e}"
        if motion is not None
        else "no matching"
    )
    sides = DASH
    if after is not None and after.side is not None and source and source.side is not None:
        sides = difference_text(after.side - source.side)
    return (
        f"n={case.n} {text}: hue classes {pair(_class_total)}; house 0-4 "
        f"{pair(_drawn_histogram)}; four-side {pair(_dark)}; stage 0-4 "
        f"{pair(_stage_histogram)}; {moved}; relation {case.relation or DASH}, "
        f"s - s_W {sides}"
    )


def summary_table(cases: Sequence[CountCase]) -> str:
    return (
        '<div class="table-scroll"><table class="summary">'
        "<thead><tr>"
        '<th class="num" scope="col">n</th><th scope="col">Decision</th>'
        '<th class="num" scope="col">Hue classes</th>'
        '<th class="num" scope="col">Four-side squares</th>'
        '<th class="num" scope="col">Moved</th><th scope="col">Side relation</th>'
        "</tr></thead>"
        f"<tbody>{summary_rows(cases)}</tbody></table></div>"
    )


def _panel_figure(case: CountCase, panel: Panel) -> str:
    heading = HEADINGS[panel.role]
    if panel.role == "view" and case.relation:
        heading = f"{heading}, {case.relation}"
    ident = f"n{case.n:03d}-{panel.role}"
    if panel.drawing is None:
        return (
            f'<figure class="panel"><div class="missing">'
            f'<p class="error">Not drawn: {_e(panel.error)}</p></div>'
            f'<figcaption><span class="role">{_e(heading)}</span></figcaption></figure>'
        )
    motion = panel.motion
    after = case.after()
    marked: list[str] = []
    if motion is not None:
        changed = sorted(set(motion.moved()) | set(motion.turned()))
        marked = [panel.drawing.squares[motion.partner[index]].square_id for index in changed]
    elif panel.role == "source" and after is not None and after.motion is not None:
        changed = sorted(set(after.motion.moved()) | set(after.motion.turned()))
        marked = [panel.drawing.squares[index].square_id for index in changed]
    svg = drawing_svg(
        panel.drawing,
        ident=ident,
        label=f"{heading}, n = {case.n}: {panel.detail}",
        decimals=2 if case.n <= LARGE_N else 1,
        marked=marked,
    )
    lines = [
        f'<span class="role">{_e(heading)}</span>',
        f'<span class="muted">{_e(panel.detail)}</span>',
        f'<span class="muted">{_e(panel.drawing.caption)}</span>',
    ]
    if motion is not None:
        lines.append(
            '<span class="marks">Outlined, by source number: moved beyond 1e-3, '
            f"{_e(_square_list(motion.moved()))}; turned, {_e(_square_list(motion.turned()))}"
            "</span>"
        )
    elif panel.role == "source" and marked:
        lines.append(
            '<span class="marks">Outlined: the squares that move or turn in the '
            f"{_e(HEADINGS[after.role].lower() if after else '')} view</span>"
        )
    elif panel.role != "source":
        lines.append(
            '<span class="marks">No symmetry pairs it one to one with the source.</span>'
        )
    return f'<figure class="panel">{svg}<figcaption>{"".join(lines)}</figcaption></figure>'


def _cell(value: str, *, numeric: bool = False) -> str:
    return f'<td class="num">{value}</td>' if numeric else f"<td>{value}</td>"


def _drawn_histogram(panel: Panel | None) -> list[int] | None:
    if panel is None or panel.drawing is None:
        return None
    return histogram(panel.drawing.contact_counts())


def _stage_histogram(panel: Panel | None) -> list[int] | None:
    if panel is None or panel.stage is None:
        return None
    return histogram(panel.stage)


def _class_total(panel: Panel | None) -> int | None:
    if panel is None or panel.drawing is None:
        return None
    return panel.drawing.class_split()[0]


def _replica_text(panel: Panel) -> str:
    if panel.drawing is None or panel.house_replica is None:
        return DASH
    drawn = panel.drawing.contact_counts()
    differ = [
        index
        for index, (left, right) in enumerate(zip(drawn, panel.house_replica, strict=True))
        if left != right
    ]
    if not differ:
        return "agrees"
    return f'<span class="flag">differs on {_e(_square_list(differ))}</span>'


def measure_table(case: CountCase) -> str:
    panels = [panel for panel in case.panels if panel.drawing is not None]
    source = case.panel("source")
    head = "".join(f'<th scope="col">{_e(HEADINGS[panel.role])}</th>' for panel in panels)

    def row(label: str, cells: Iterable[str]) -> str:
        return f'<tr><th scope="row">{label}</th>{"".join(cells)}</tr>'

    def side_cell(panel: Panel) -> str:
        if panel.role == "source" or source is None or source.side is None:
            return _cell(_e(f"s_W = {_side_text(panel.side)}"), numeric=True)
        if panel.side is None:
            return _cell("not rational", numeric=True)
        difference = difference_text(panel.side - source.side)
        return _cell(_e(f"s {MINUS} s_W = {difference}"), numeric=True)

    def motion_cell(panel: Panel) -> str:
        motion = panel.motion
        if panel.role == "source":
            return _cell(DASH)
        if motion is None:
            return _cell('<span class="flag">not one to one</span>')
        largest = max(motion.move, default=0.0)
        turn = max(motion.turn_degrees, default=0.0)
        return _cell(
            _e(
                f"{len(motion.moved())} moved, {len(motion.turned())} turned; "
                f"largest {largest:.3e}, {turn:.3g}°; symmetry {motion.symmetry}"
            )
        )

    rows = [
        row("Hue classes", (_cell(_e(_classes(panel))) for panel in panels)),
        row(
            'House shades <span class="sub">squares with 0 to 4 sides, as drawn</span>',
            (_cell(_hist(_drawn_histogram(panel))) for panel in panels),
        ),
        row("Four-side squares", (_cell(_dark_text(panel), numeric=True) for panel in panels)),
        row(
            'Stage counts <span class="sub">gap 0.01, half a degree</span>',
            (
                _cell(_hist(None if panel.stage is None else histogram(panel.stage)))
                for panel in panels
            ),
        ),
        row(
            "Census replica of the house rule",
            (_cell(_replica_text(panel)) for panel in panels),
        ),
        row("Side", (side_cell(panel) for panel in panels)),
        row(
            'Moves and turns <span class="sub">measured on the drawings</span>',
            (motion_cell(panel) for panel in panels),
        ),
    ]
    return (
        '<div class="table-scroll"><table class="measures">'
        f'<thead><tr><th scope="col">Measured</th>{head}</tr></thead>'
        f"<tbody>{''.join(rows)}</tbody></table></div>"
    )


def _identity_text(case: CountCase) -> str:
    identity = field(case.report, "identity")
    if not isinstance(identity, dict):
        return "not recorded"
    text = (
        f"of the {identity.get('of', '?')} view: one to one "
        f"{short(identity.get('one_to_one'))}, "
        f"moved {identity.get('moved', '?')}, largest move {identity.get('max_move', '?')}, "
        f"largest turn {identity.get('max_turn_deg', '?')}°, symmetry "
        f"{identity.get('symmetry', '?')}"
    )
    after = case.panel("view")
    measured = after.motion if after else None
    disagreements: list[str] = []
    if after is not None and after.drawing is not None:
        if (measured is not None) != bool(identity.get("one_to_one")):
            disagreements.append("one to one")
        if measured is not None and identity.get("moved") is not None:
            if int(identity["moved"]) != len(measured.moved()):
                disagreements.append(f"moved ({len(measured.moved())} measured here)")
            if (
                identity.get("symmetry") is not None
                and int(identity["symmetry"]) != measured.symmetry
            ):
                disagreements.append(f"symmetry ({measured.symmetry} measured here)")
    flag = (
        f' <span class="flag">The drawings disagree on {_e(", ".join(disagreements))}.</span>'
        if disagreements
        else ""
    )
    return _e(text) + flag


def _shades_text(case: CountCase) -> str:
    recorded = field(case.report, "shades")
    if not isinstance(recorded, dict):
        return "not recorded"
    parts: list[str] = []
    for rule in ("house", "stage"):
        before, after = field(recorded, rule, "before"), field(recorded, rule, "after")
        if before is not None or after is not None:
            parts.append(f"{rule} {_hist(before)} → {_hist(after)}")
    measured = [_drawn_histogram(case.panel("source")), _drawn_histogram(case.panel("view"))]
    house = [field(recorded, "house", "before"), field(recorded, "house", "after")]
    flag = ""
    if None not in measured and None not in house and house != measured:
        flag = (
            ' <span class="flag">The report\'s house histograms differ from the '
            "drawings'.</span>"
        )
    return ("; ".join(parts) or "no histograms") + flag


def _regressions_text(case: CountCase) -> str:
    found = field(case.report, "shades", "regressions")
    if found is None:
        return "not recorded"
    if not found:
        return "none"
    items = [
        f"square {item.get('square')} {item.get('rule')} "
        f"{item.get('before')} → {item.get('after')}"
        if isinstance(item, dict)
        else str(item)
        for item in found
    ]
    return f'<span class="flag">{_e(short(items, 400))}</span>'


def _upper_bound_text(case: CountCase) -> str:
    bound = field(case.report, "verified_upper_bound")
    if bound is None:
        return "not recorded"
    after = case.panel("view")
    value = rational(bound)
    if after is None or after.side is None or value is None:
        return _e(bound)
    relation = (
        "at or above U" if after.side >= value else "below U: a register-result candidate"
    )
    difference = difference_text(after.side - value)
    return _e(f"U = {bound}; s_V {MINUS} U = {difference}, {relation}")


def _generator_text(report: dict[str, Any]) -> str:
    generator = field(report, "generator")
    if not isinstance(generator, dict):
        return "not recorded"
    patches = generator.get("patches")
    return (
        f"{generator.get('name', '?')} at {generator.get('pin', '?')}, patches "
        f"{short(patches)}; variant {generator.get('variant', '?')}, style "
        f"{generator.get('style', '?')}, orientation {generator.get('orient', '?')}"
    )


def _routes_text(case: CountCase) -> str:
    chosen = case.relation or field(case.report, "identity", "of")
    routes = field(case.report, "outputs", str(chosen), "routes") if chosen else None
    if not isinstance(routes, dict):
        return "not recorded"
    return ", ".join(f"{name} {short(verdict)}" for name, verdict in routes.items())


def facts(case: CountCase) -> str:
    """The report's fields, as the run recorded them."""
    report = case.report
    regularize = field(report, "regularize") or {}
    entries: list[tuple[str, str]] = []
    if report:
        decision = field(report, "decision") or {}
        row = _e(decision.get("row", "?"))
        record = _e(short(decision.get("index_record")))
        entries += [
            ("Decision", f"{_chip_html(case)} row {row}, index record {record}"),
            ("Reason", _e(short(decision.get("reason"), 600))),
            ("Status", _e(f"{report.get('status', '?')}; error {short(report.get('error'))}")),
            ("Side relation", _e(case.relation or "no view drawn")),
            ("Verified upper bound", _upper_bound_text(case)),
            ("Identity (report)", _identity_text(case)),
            ("Shades (report)", _shades_text(case)),
            ("Regressions", _regressions_text(case)),
            ("Generator", _e(_generator_text(report))),
            (
                "Level",
                _e(f"{short(regularize.get('level'))}: {short(regularize.get('level_text'))}"),
            ),
            ("Symmetry imposed", _e(short(regularize.get("symmetry")))),
            ("Angle changes", _e(short(regularize.get("angle_changes"), 600))),
            (
                "Rotation groups",
                _e(
                    _arrow(regularize.get("groups_before", "?"), regularize.get("groups_after"))
                    + f"; merged {short(regularize.get('merged'))}"
                ),
            ),
            ("Exact routes", _e(_routes_text(case))),
        ]
        refusal = field(report, "outputs", "same_refusal")
        if refusal:
            entries.append(("Same side refused", _e(short(refusal, 600))))
    if case.layer_status is not None:
        entries.append(("Current layer", _e(case.layer_status)))
    entries.extend(("Note", f'<span class="flag">{_e(note)}</span>') for note in case.notes)
    if not entries:
        return ""
    body = "".join(f"<dt>{label}</dt><dd>{value}</dd>" for label, value in entries)
    return f'<dl class="facts">{body}</dl>'


def changes_table(case: CountCase) -> str:
    """Every source square that moved, turned or changed a count, with its counts."""
    source, after = case.panel("source"), case.after()
    if (
        source is None
        or after is None
        or source.drawing is None
        or after.drawing is None
        or after.motion is None
    ):
        return ""
    motion = after.motion
    before_house, after_house = source.drawing.contact_counts(), after.drawing.contact_counts()
    rows: list[str] = []
    for index, partner in enumerate(motion.partner):
        house = (before_house[index], after_house[partner])
        stage = (
            (source.stage[index], after.stage[partner])
            if source.stage is not None and after.stage is not None
            else None
        )
        moved = motion.move[index] > MOVED_BEYOND
        turned = index in set(motion.turned())
        if not (moved or turned or house[0] != house[1] or (stage and stage[0] != stage[1])):
            continue

        def count(pair: tuple[int, int] | None) -> str:
            if pair is None:
                return DASH
            text = _e(f"{pair[0]} → {pair[1]}")
            return f'<span class="flag">{text}</span>' if pair[1] < pair[0] else text

        rows.append(
            "<tr>"
            f'<td class="num">{index + 1}</td><td class="num">{partner + 1}</td>'
            f'<td class="num">{motion.move[index]:.3e}</td>'
            f'<td class="num">{motion.turn_degrees[index]:.3g}</td>'
            f'<td class="num">{count(house)}</td><td class="num">{count(stage)}</td>'
            "</tr>"
        )
    label = HEADINGS[after.role].lower()
    if not rows:
        return (
            '<p class="muted">No square moved, turned or changed a count in the '
            f"{_e(label)} view.</p>"
        )
    return (
        f"<details><summary>{len(rows)} squares moved, turned or changed a count in the "
        f"{_e(label)} view</summary>"
        '<div class="table-scroll"><table class="changes"><thead><tr>'
        '<th class="num" scope="col">Square</th><th class="num" scope="col">In view</th>'
        '<th class="num" scope="col">Move</th><th class="num" scope="col">Turn (°)</th>'
        '<th class="num" scope="col">House</th><th class="num" scope="col">Stage</th>'
        f"</tr></thead><tbody>{''.join(rows)}</tbody></table></div></details>"
    )


def section(case: CountCase) -> str:
    reason = field(case.report, "decision", "reason")
    figures = "".join(_panel_figure(case, panel) for panel in case.panels)
    return (
        f'<section class="count" id="n-{case.n:03d}" aria-labelledby="n-{case.n:03d}-title">'
        f'<header class="count-head"><h2 id="n-{case.n:03d}-title"><i>n</i> = {case.n}</h2>'
        f"{_chip_html(case)}"
        + (f'<p class="reason">{_e(short(reason, 600))}</p>' if reason else "")
        + f'</header><div class="panels">{figures}</div>'
        f"{measure_table(case)}{facts(case)}{changes_table(case)}</section>"
    )


def legend() -> str:
    """The house palette's two pinned families, darkest (four sides) first."""
    palette = square_fill_palette(
        hue_count=SPEC.hue_count,
        shades_per_hue=SPEC.shades_per_hue,
        lightness_span=SPEC.shade_lightness_span,
    )
    rows: list[str] = []
    for label, hue in (("0°", RIGHT_ANGLE_HUE), ("45°", DIAGONAL_HUE)):
        cells = "".join(
            f'<rect x="{index * 22}" y="0" width="20" height="16" fill="{fill}"/>'
            for index, fill in enumerate(palette[hue])
        )
        rows.append(
            f'<span class="swatch-row"><span class="swatch-label">{label}</span>'
            f'<svg class="swatches" width="108" height="16" viewBox="0 0 108 16" role="img" '
            f'aria-label="{label} family, shades for 4 down to 0 sides">{cells}</svg></span>'
        )
    return (
        '<div class="legend"><span>Shade by sides shared whole, 4 to 0:</span>'
        f"{''.join(rows)}"
        '<span class="swatch-row"><svg class="swatches" width="24" height="16" '
        'viewBox="0 0 24 16" role="img" '
        'aria-label="outlined square"><path class="mark-halo" d="M4 2h16v12H4z"/>'
        '<path class="mark" d="M4 2h16v12H4z"/></svg>moved beyond 1e-3 or turned</span></div>'
    )


def _tally(cases: Sequence[CountCase]) -> str:
    counts: dict[str, int] = {}
    for case in cases:
        text, _tone = chip(case)
        counts[text] = counts.get(text, 0) + 1
    return ", ".join(f"{text} {count}" for text, count in sorted(counts.items()))


def run_facts(cases: Sequence[CountCase], source: str, receipt: dict[str, Any]) -> str:
    entries = [("Drawn from", _e(source)), ("Counts", _e(f"{len(cases)}: {_tally(cases)}"))]
    generator = field(receipt, "generator")
    if isinstance(generator, dict):
        entries.append(
            (
                "Generator",
                _e(
                    f"{generator.get('name', '?')} at {generator.get('pin', '?')}, patches "
                    f"{short(generator.get('patches'))}; interpreter "
                    f"{short(generator.get('interpreter'))}"
                ),
            )
        )
    if field(receipt, "parameters") is not None:
        entries.append(("Parameters", _e(short(receipt["parameters"], 400))))
    cost = field(receipt, "cost")
    if isinstance(cost, dict):
        entries.append(
            (
                "Cost",
                _e(
                    f"{cost.get('cpu_seconds', '?')} CPU seconds, "
                    f"{cost.get('wall_seconds', '?')} wall"
                ),
            )
        )
    body = "".join(f"<dt>{label}</dt><dd>{value}</dd>" for label, value in entries)
    return f'<dl class="run-facts">{body}</dl>'


def render_page(
    cases: Sequence[CountCase],
    *,
    title: str,
    source: str,
    receipt: dict[str, Any] | None = None,
) -> str:
    """The whole page: a title and stylesheet, then the summary and one section a count.

    It opens with `<title>` and `<style>` and carries no document skeleton of its own,
    which is the shape a published page takes; nothing in it is a script.
    """
    stylesheet = STYLESHEET.read_text(encoding="utf-8")
    lede = (
        "Each count draws the source witness beside its regularized view with the house "
        "renderer, at one scale. Hue is a square's angle class; shade is how many of its "
        "four sides it shares whole with a wall or a same-angle neighbour, darkest at four. "
        "A regular structure reads as a few hue families in dark shades; slack shows as "
        "light squares and angle noise as extra hues. The chips are the run's decisions: "
        "this page decides nothing."
    )
    return (
        f"<title>{_e(title)}</title>\n<style>\n{stylesheet}</style>\n"
        '<main class="page">'
        '<header class="masthead"><p class="eyebrow">Regularization policy, section 5: '
        "what the reviewer sees</p>"
        f'<h1>{_e(title)}</h1><p class="lede">{_e(lede)}</p>'
        f"{run_facts(cases, source, receipt or {})}{legend()}</header>"
        '<section class="summary" aria-labelledby="summary-title">'
        '<h2 id="summary-title" class="section-title">Counts</h2>'
        f"{summary_table(cases)}</section>"
        f"{''.join(section(case) for case in cases)}"
        f'<footer class="colophon">Written by <code>{_e(GENERATOR)}</code>. Drawings by '
        "<code>sqpack.render</code>; contact counts by "
        "<code>devtools.census_atlas_contact_shades</code>.</footer>"
        "</main>\n"
    )


# --------------------------------------------------------------------------------------
# Command line
# --------------------------------------------------------------------------------------


def _drawn(
    function: Callable[[Any], CountCase], units: Sequence[Any], workers: int | None
) -> list[CountCase]:
    """Each unit drawn and measured, in worker processes when there is more than one.
    `workers` defaults to `sqpack.workers.worker_count`: the gate's `PACK_JOBS` cap, and
    the whole machine from a shell."""
    workers = worker_count(len(units)) if workers is None else workers
    if workers > 1 and len(units) > 1:
        with ProcessPoolExecutor(max_workers=min(workers, len(units))) as pool:
            return list(pool.map(function, units))
    return [function(unit) for unit in units]


def _run_unit(unit: tuple[Path, Mapping[int, dict[str, Any]] | None]) -> CountCase:
    return run_case(*unit)


def run_cases(
    run_dir: Path,
    numbers: Sequence[int] | None,
    *,
    with_current_layer: bool,
    workers: int | None = 1,
) -> list[CountCase]:
    directories = {
        int(path.name.removeprefix("n-")): path
        for path in sorted(run_dir.glob("n-[0-9][0-9][0-9]"))
        if path.is_dir()
    }
    wanted = sorted(set(numbers)) if numbers else sorted(directories)
    missing = [n for n in wanted if n not in directories]
    if missing:
        print(f"no count directory in {run_dir} for n = {', '.join(map(str, missing))}")
    layer_index = index_entries() if with_current_layer else None
    units = [(directories[n], layer_index) for n in wanted if n in directories]
    return _drawn(_run_unit, units, workers)


def layer_cases(numbers: Sequence[int] | None, *, workers: int | None = 1) -> list[CountCase]:
    entries = index_entries()
    if numbers:
        wanted = sorted(set(numbers))
    else:
        wanted = sorted(n for n, entry in entries.items() if entry["status"] == "regularized")
    missing = [n for n in wanted if n not in entries]
    if missing:
        raise SystemExit(f"the layer's index has no record for n = {missing}")
    return _drawn(layer_case, [entries[n] for n in wanted], workers)


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--run-dir", type=Path, help="a run directory regularize_evand wrote")
    mode.add_argument(
        "--current-layer",
        action="store_true",
        help="draw the current regularized layer against its sources, with no run",
    )
    command.add_argument("--output", type=Path, required=True, help="the HTML page to write")
    command.add_argument("--n", type=int, nargs="+", help="draw only these counts")
    command.add_argument(
        "--with-current-layer",
        action="store_true",
        help="add the current layer's view of each count as a third panel",
    )
    command.add_argument("--title", default=DEFAULT_TITLE, help="the page's name")
    command.add_argument(
        "--workers",
        type=int,
        default=None,
        help="processes to draw with (default: the gate's PACK_JOBS cap, or every core)",
    )
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    workers: int | None = args.workers
    if args.current_layer:
        cases = layer_cases(args.n, workers=workers)
        source = display_path(layer.INDEX)
        receipt: dict[str, Any] = {}
    else:
        run_dir: Path = args.run_dir
        if not run_dir.is_dir():
            raise SystemExit(f"{run_dir} is not a directory")
        cases = run_cases(
            run_dir, args.n, with_current_layer=args.with_current_layer, workers=workers
        )
        source = display_path(run_dir)
        receipt = read_json(run_dir / "receipt.json")
    if not cases:
        raise SystemExit("no counts to draw")
    page = render_page(cases, title=args.title, source=source, receipt=receipt)
    size = len(page.encode("utf-8"))
    if size > PAGE_LIMIT:
        print(
            f"the page would be {size:,} bytes, over the {PAGE_LIMIT:,} a published page "
            "holds; draw fewer counts with --n",
            file=sys.stderr,
        )
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(args.output) as temporary:
        temporary.write_text(page, encoding="utf-8")
    for case in cases:
        print(summary_line(case))
    counts = f"{len(cases)} count" + ("" if len(cases) == 1 else "s")
    print(f"wrote {display_path(args.output)}: {counts}, {size:,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
