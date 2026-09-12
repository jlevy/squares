#!/usr/bin/env python3
"""Build the v2 transition review candidate: index.html + transition-stats.json.

Deterministic: same inputs, same bytes. No network. Reads the known-best witnesses,
the atlas manifest, the per-n renderings (for house fills, contact counts, angle classes
and full-side contacts), the composite figure record (for the facts panel: side, lower
bound, badges, what is open), four kpress woff2 faces and the KaTeX_Main face for the
relation symbols; the glyph tables also set the badges' alignment, the numeral's box
offset (from the regular face's digit bearings) and supply the drawn approximately-equal
sign.

Revision 5: every square has a persistent identity from the step it arrives, the 158
assignment pairs are matched block first (rigid transforms between clusters of
side-by-side squares of one tilt, then the squares inside them), the new square is the
cost-optimal choice under a stated rule rather than the assignment's leftover, and the
record carries the identity chain, the blocks, the residuals, the rule and the census of
squares the arriving square overlaps before the others have moved.

The page is three files that the build makes one: `template.html` holds the markup,
`assets/workbench.css` the stylesheet and `assets/workbench.js` the script, and each is
inlined at its `__TOKEN__` the way the embedded faces are. Written as one file none of it
could be read by a formatter, a linter or an editor; written as three, all of it can.

Run with the project interpreter:
    packing/.venv/bin/python3 build_candidate.py [--all] [--out DIR]
"""

from __future__ import annotations

import argparse
import base64
import json
import math
import re
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager
from fractions import Fraction
from pathlib import Path

import numpy as np
import yaml
from scipy.optimize import linear_sum_assignment
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

HERE = Path(__file__).resolve().parent
# This file lives at packing/atlas/known-best/video/spikes/v2-transitions, so `packing` is five
# levels up -- the depth `compare_palette.py` and `grade_motion.py` beside it already use. Derived
# rather than written out: it carried an ABSOLUTE path to one worktree, which meant the build ran
# only from that checkout, ran silently against the wrong tree from any other, and failed on CI.
PACKING = HERE.parents[4]
REPO = PACKING.parent
# `devtools` is imported for the explainer's KaTeX inliner and its self-containment check, so the
# packing root has to be importable: this file is run as a script, not as a module.
if str(PACKING) not in sys.path:
    sys.path.insert(0, str(PACKING))
WITNESSES = PACKING / "witnesses" / "known-best"
RENDERINGS = PACKING / "atlas" / "known-best" / "rendering"
MANIFEST = PACKING / "atlas" / "known-best" / "manifest.json"
COMPOSITE = PACKING / "atlas" / "known-best" / "composite-figure.json"
FONTS = REPO / "vendor" / "kpress" / "src" / "kpress" / "format" / "static" / "fonts"
KATEX_FONTS = REPO / "vendor" / "kpress" / "src" / "kpress" / "format" / "static" / "katex" / "fonts"

N_MAX = 324

# Square-level cost: squared centre distance in container-normalised coordinates plus an
# angle term. ANGLE_WEIGHT is stated in unit-square units squared: a full 45 degree turn
# costs the same as sliding sqrt(ANGLE_WEIGHT) unit squares (one square width here;
# experiment_angle_weight.py tabulates the alternatives).
ANGLE_WEIGHT = 1.0
ROTATION_TOLERANCE_DEG = 0.05
CROSSING_DISTANCE = 0.7  # centre distance below which two moving unit squares overlap badly
CROSSING_SAMPLES = 21
MOVE_TOLERANCE = 0.01    # a square that travels less than this and turns less than the rotation tolerance is stationary

# Block-aware matching, revision 5. A frame is clustered into blocks: side-by-side squares
# (centres within 1 + CLUSTER_GAP_TOL) whose tilts agree within CLUSTER_ANGLE_TOL, joined with
# the atlas's own full-side contacts inside one angle class. Every source block and target
# block whose extents can reach each other is searched for rigid transforms - a rotation by
# the blocks' tilt difference and a translation found by consensus of the candidate offsets -
# that carry BLOCK_MIN or more squares of the one onto squares of the other within
# BLOCK_RESIDUAL_TOL, refined by Procrustes on the inliers; a block may split or merge because
# a cluster pair is searched again on what its earlier transforms left over. The transforms'
# inlier pairs enter the square-level assignment as discounted links (travel inside a block
# costs BLOCK_DISCOUNT of the same travel alone, plus the residual), and one rectangular
# assignment settles the conflicts, the remainder and the new square at once: the column it
# leaves out is the square whose removal from n+1 gives the lowest total cost. An infinitesimal
# per-column bonus breaks exact ties by the stated rule (fewest full-side contacts, then the
# highest position), and a sensitivity pass on the optimal assignment reports how many squares
# tied for that choice. experiment_block_matching.py sweeps the discount and the tolerances.
CLUSTER_ANGLE_TOL = 4.0        # degrees: side-by-side squares within this tilt of each other share a block
CLUSTER_GAP_TOL = 0.2          # unit squares: centres within 1 + this are side by side
BLOCK_RESIDUAL_TOL = 0.35      # unit squares: a transform carries a square if it lands within this of a target
BLOCK_MIN = 2                  # squares a transform must carry to count as a block
BLOCK_SLIDE_MAX = 1.5          # unit squares: a block's pivot may travel this far; further is a relabelling, not a move
BLOCK_DRIFT_TOL = 0.75         # unit squares: a square of the same cluster rides a block whose transform lands it within this of its target
BLOCK_DISCOUNT = 0.1           # travel inside a block costs this fraction of the same travel alone
INDIVIDUAL_PENALTY = 1.0       # unit squares squared: what a square pays to move alone at all (blocks and staying put pay nothing)
BLOCK_HOUGH_TOP = 6            # candidate offsets examined per search
BLOCK_REFIT_ROUNDS = 4         # Procrustes refit and recount rounds per candidate
BLOCK_MAX_TRANSFORMS = 6       # transforms searched per cluster pair
NEW_TIE_TOL = 2e-7             # normalised total-cost difference under which two new-square choices tie
NEW_BONUS = 4e-11              # per unit of badness, the column bonus that breaks those ties (range < NEW_TIE_TOL)
CONTACT_BADNESS = 1000.0       # one full-side contact outweighs any position difference in the tie-break
NEW_RULE = "lowest total matching cost after removal from n+1, then fewest full-side contacts, then highest position (y, then x)"

# Timeline defaults, seconds. Revision 2: a little faster (was 1.2 / 1.6 / 0.5).
# The single-step beat, even: a beat to read the packing, a beat to rearrange it, a beat to
# settle. The owner's pacing.
#: The footer `devtools/check_documentation.py` requires on durable Markdown. Written here rather
#: than added by hand afterwards, because this file is regenerated on every build.
#: The banner `devtools/check_generated_markdown.py` requires on a generated view, so that gate
#: can enforce the file's exemption from the auto-formatter rather than trust it. Without it the
#: formatter rewraps what the generator writes unwrapped, and the two never agree again.
STATS_BANNER = "<!-- GENERATED by build_candidate.py. Do not edit by hand; rebuild the spike. -->\n\n"

DOC_FOOTER = (
    "<!-- This document follows common-doc-guidelines.md.\n"
    "See github.com/jlevy/practical-prose and review guidelines before editing.\n"
    "-->\n"
)

TIMING = {"dwell": 0.8, "move": 0.8, "settle": 0.8}
# Revision 5 staging: in the default motion (add, then make room) the new square arrives over
# the first ARRIVAL_FRACTION of the move while the container grows, and the existing squares
# move, as blocks, over the rest; `move-then-add` is the same split the other way round.
ARRIVAL_FRACTION = 0.3
MOTION_PHASES = ["add-then-move", "move-then-add", "simultaneous", "rotate-first", "slide-first"]
# The per-kind schedule NOTES computes for the 165 static appends (prefix and shared-picture),
# which have nothing to move: no move at all, and with a short move for the new square's fade-in.
STATIC_APPEND_TIMINGS = {
    "no move": {"dwell": 0.5, "move": 0.0, "settle": 0.4},
    "short move": {"dwell": 0.5, "move": 0.4, "settle": 0.3},
}

# The poster's badge vocabulary, exactly as composite-figure.json states it (glyph, style); the
# star is `lower.first_proved_here`. A badge outside this set fails the build rather than being drawn.
BADGE_VOCABULARY = {
    ("O", "solid"): "proved optimal",
    ("=", "solid"): "exact value known",
    ("≈", "muted"): "only known numerically",
    ("R", "solid"): "rigid (established here)",
    ("R", "muted"): "annotated rigid by the catalogue",
}
# SUMMARY_STAR_POINTS from packing/devtools/build_known_best_atlas.py: the five-pointed star the
# poster draws as a polygon, apex up, about its own centre, with its inset and the span it fills of
# a badge box. test_candidate.py checks these against the atlas source.
STAR_POINTS = [
    (0, -6), (1.411, -1.942), (5.706, -1.854), (2.283, 0.742), (3.527, 4.854),
    (0, 2.4), (-3.527, 4.854), (-2.283, 0.742), (-5.706, -1.854), (-1.411, -1.942),
]
STAR_INSET = 6
STAR_SPAN = 0.92
BADGE_SIZE = 19
BADGE_FONT_SIZE = 15
# The approximately-equal badge glyph is KaTeX_Main's U+2248 (the embedded latin subsets carry
# none), drawn as a path at a smaller size because its wave is wider than Source Sans's equals,
# and thickened by a stroke in font units to match the weight-650 letters; as the slideshow does.
APPROX_FONT_SIZE = 13
APPROX_STROKE_UNITS = 26
# The type scale, revision 4: four sizes on the 1920 x 1080 stage and nothing below 28 px, so
# the page reads on video. The numeral is PT Serif Regular at 96 px (revision 3 had Bold at
# 132), 3.4 times the smallest size; the `n =` line sits above it at 34. The sizes are in the
# template's CSS; they are stated here so the notes and the test can quote them, and so the
# build can place the numeral's box from the regular face's bearings (see type_metrics).
TYPE_SCALE = [28, 34, 44, 96]
NUMERAL_PX = 96      # .n-val
NUMERAL_WEIGHT = 400
N_LINE_PX = 96       # .nline, the same size as the numeral it labels
N_LINE_LEFT_PX = 6   # .nline left, the panel's text edge
#: The space between the `=` of `n =` and the first digit beside it, ink to ink. The headline is
#: one line, so this is a word space rather than a line break: 16 px at 96 px is a sixth of an em,
#: tighter than the face's own space, which is what makes `n = 11` read as one statement.
HEADLINE_GAP_PX = 16

#: TeX fragments, written as constants so no escaping has to survive an f-string.
BOLD = chr(92) + "boldsymbol{%s}"
LE = chr(92) + "le"
GE = chr(92) + "ge"
#: The two bound colours, as the panel and the gap bar both draw them: scarlet for what is
#: proved from below, green for the best that is known from above. They are the palette's own
#: `--new` and `--met`, written here because KaTeX colours by value rather than by class.
LOWER_INK = "#a3123f"
UPPER_INK = "#17794a"


def colour(ink: str, body: str) -> str:
    """`body` in `ink`, as TeX."""
    return chr(92) + "textcolor{" + ink + "}{" + body + "}"


# Pairs the demonstration must carry, identified by n (the pair is n -> n+1).
REQUIRED_PAIRS = [4, 9, 10, 17, 99, 100, 147, 272]
EXTRA_PAIRS = [110, 260, 307]           # the block-motion showcases: two collapses into a grid and the largest rotation count
OPENING_RUN = list(range(1, 11))        # 1->2 ... 10->11, tiny and continuous with 4->5, 9->10, 10->11
SEQUENCE_RUN = list(range(101, 106))    # 101->102 ... 105->106, continuous with 99->100, 100->101
FINALE = [323]

# (family, weight, style, path). "Atlas Symbols" is the slideshow candidate's name for the
# KaTeX_Main-Regular face restricted to the relation and radical code points the latin subsets
# of PT Serif and Source Sans do not carry (≤ ≥ √ ≈ ∈ and the floor and ceiling brackets); it
# follows PT Serif in the serif stack so those glyphs no longer fall back to Georgia.
FONT_FACES = [
    ("PT Serif", 400, "normal", FONTS / "pt-serif-latin-400-normal.woff2"),
    ("PT Serif", 400, "italic", FONTS / "pt-serif-latin-400-italic.woff2"),
    ("PT Serif", 700, "normal", FONTS / "pt-serif-latin-700-normal.woff2"),
    ("Source Sans 3", "300 900", "normal", FONTS / "source-sans-3-latin-wght-normal.woff2"),
    ("Atlas Symbols", 400, "normal", KATEX_FONTS / "KaTeX_Main-Regular.woff2"),
]
# The latin unicode-range kpress's style-tokens.css gives the PT Serif and Source Sans faces.
LATIN_RANGE = (
    "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, "
    "U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, "
    "U+FEFF, U+FFFD"
)
# Relations, the radical, approximately, element-of and the floor/ceiling brackets.
SYMBOL_RANGE = "U+2208, U+221A, U+2248, U+2264-2265, U+2308-230B"
SYMBOL_SIZE_ADJUST = "102.5%"

Loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


# --------------------------------------------------------------------------- witnesses


def load_witness(n: int) -> dict:
    data = yaml.load((WITNESSES / f"n-{n:03d}.yaml").read_text(), Loader=Loader)["witness"]
    representation = data["representation"]
    side = float(Fraction(data["side"]))
    squares = []
    keys = []
    for square in data["squares"]:
        if representation == "center-angle":
            cx, cy = (float(Fraction(value)) for value in square["center"])
            angle = float(Fraction(square["angle"])) % 90.0
            keys.append(("ca", square["center"][0], square["center"][1], square["angle"]))
        else:
            corners = [(Fraction(x), Fraction(y)) for x, y in square["corners"]]
            cx = float(sum(x for x, _ in corners) / 4)
            cy = float(sum(y for _, y in corners) / 4)
            (x0, y0), (x1, y1) = corners[0], corners[1]
            angle = math.degrees(math.atan2(float(y1 - y0), float(x1 - x0))) % 90.0
            keys.append(("co",) + tuple(v for pair in square["corners"] for v in pair))
        squares.append((cx, cy, angle))
    xy = np.array([(x, y) for x, y, _ in squares], dtype=float).reshape(len(squares), 2)
    angles = np.array([a for _, _, a in squares], dtype=float)
    return {
        "n": n, "side": side, "squares": squares, "keys": keys, "representation": representation,
        "xy": xy, "angles": angles,
    }


FILL_RE = re.compile(r'<polygon data-feature="square-fill" ([^>]*?)/>')
ATTR_RE = re.compile(r'([\w-]+)="([^"]*)"')


def load_rendering(n: int) -> list[dict]:
    """Per square, in witness order: the house fill, the full-side contact count, the hue and
    shade indices, the atlas's angle class and the indices of the squares it shares a full side
    with (walls left out)."""
    text = (RENDERINGS / f"n-{n:03d}.svg").read_text()
    rows: dict[int, dict] = {}
    for match in FILL_RE.finditer(text):
        attrs = dict(ATTR_RE.findall(match.group(1)))
        index = int(attrs["data-square"].split("-")[1]) - 1
        contact_ids = [
            int(token.split("-")[1]) - 1
            for token in attrs.get("data-full-side-contacts", "").split()
            if token.startswith("square-")
        ]
        rows[index] = {
            "fill": attrs["fill"],
            "contacts": int(attrs["data-contact-sides"]),
            "hue": int(attrs["data-hue-index"]),
            "shade": int(attrs["data-shade-index"]),
            "angle_class": int(attrs["data-angle-class"]),
            "contact_ids": contact_ids,
        }
    if sorted(rows) != list(range(n)):
        raise ValueError(f"rendering n={n} does not carry squares 1..{n}")
    return [rows[i] for i in range(n)]


# --------------------------------------------------------------------------- blocks


def angle_delta(a: float, b: float) -> float:
    """Shortest signed rotation from a to b modulo 90 degrees, in (-45, 45]; ties turn counter-clockwise."""
    d = (b - a) % 90.0
    if d > 45.0 + 1e-9:
        d -= 90.0
    return d


def circular_mean_angle(angles: np.ndarray) -> float:
    """The mean tilt of a set of squares, modulo 90 degrees (a square has four-fold symmetry)."""
    a = np.radians(angles * 4.0)
    return float(np.degrees(math.atan2(float(np.sin(a).mean()), float(np.cos(a).mean()))) / 4.0 % 90.0)


def rotation(deg: float) -> np.ndarray:
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    return np.array([[c, -s], [s, c]])


def frame_clusters(witness: dict, rendering: list[dict]) -> list[list[int]]:
    """The frame's blocks: connected components of side-by-side squares of one tilt.

    Two squares are joined when their centres are within 1 + CLUSTER_GAP_TOL and their tilts
    within CLUSTER_ANGLE_TOL modulo 90, or when the atlas records a full-side contact between
    them inside one angle class. Sorted by size, then by first member, so the order is stable.
    """
    n = witness["n"]
    if n == 1:
        return [[0]]
    xy, ang = witness["xy"], witness["angles"]
    d = np.sqrt(((xy[:, None, :] - xy[None, :, :]) ** 2).sum(-1))
    da = np.abs(((ang[None, :] - ang[:, None] + 45.0) % 90.0) - 45.0)
    adj = (d <= 1.0 + CLUSTER_GAP_TOL) & (da <= CLUSTER_ANGLE_TOL)
    for i, row in enumerate(rendering):
        for j in row["contact_ids"]:
            if rendering[j]["angle_class"] == row["angle_class"]:
                adj[i, j] = adj[j, i] = True
    np.fill_diagonal(adj, False)
    count, labels = connected_components(csr_matrix(adj), directed=False)
    clusters = [sorted(np.flatnonzero(labels == k).tolist()) for k in range(count)]
    clusters.sort(key=lambda c: (-len(c), c[0]))
    return clusters


def procrustes(p: np.ndarray, q: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
    """The rotation (degrees) and the two pivots that carry centres p onto centres q with the
    least squared residual: rotate about p's centroid, then place it on q's."""
    cp, cq = p.mean(axis=0), q.mean(axis=0)
    h = (p - cp).T @ (q - cq)
    phi = math.degrees(math.atan2(h[0, 1] - h[1, 0], h[0, 0] + h[1, 1]))
    return phi, cp, cq


def apply_rigid(p: np.ndarray, phi: float, cp: np.ndarray, cq: np.ndarray) -> np.ndarray:
    return (p - cp) @ rotation(phi).T + cq


def nearest_inliers(moved: np.ndarray, targets: np.ndarray) -> list[tuple[int, int]]:
    """Pairs (row of moved, row of targets) within BLOCK_RESIDUAL_TOL, each target claimed once
    by its nearest source. Non-overlapping unit squares of one tilt have centres at least one
    unit apart, so with a tolerance under a half the claim is one-to-one by construction."""
    d = np.sqrt(((moved[:, None, :] - targets[None, :, :]) ** 2).sum(-1))
    nearest = d.argmin(axis=1)
    best_for_target: dict[int, tuple[float, int]] = {}
    for a, b in enumerate(nearest):
        dist = float(d[a, b])
        if dist <= BLOCK_RESIDUAL_TOL and (b not in best_for_target or dist < best_for_target[b][0]):
            best_for_target[int(b)] = (dist, a)
    return sorted((a, b) for b, (_, a) in best_for_target.items())


def rigid_links(p: np.ndarray, q: np.ndarray, src: list[int], dst: list[int], turn: float) -> list[dict]:
    """The rigid transforms that carry parts of source cluster src onto parts of target cluster
    dst, largest first. Each is found by consensus: with the rotation fixed by the clusters'
    tilt difference, every source-target offset votes into a cell of BLOCK_RESIDUAL_TOL, the
    best-voted cells are refined to a translation, its inliers are refit by Procrustes and
    recounted; the transform with the most inliers wins, ties going to the least travel. The
    search repeats on the squares left over, so one cluster pair can yield several blocks."""
    links = []
    free_src, free_dst = np.array(src), np.array(dst)
    R = rotation(turn)
    for _ in range(BLOCK_MAX_TRANSFORMS):
        if len(free_src) < BLOCK_MIN or len(free_dst) < BLOCK_MIN:
            break
        P = p[free_src] @ R.T
        Q = q[free_dst]
        offsets = Q[None, :, :] - P[:, None, :]
        travel_of = np.sqrt(((q[free_dst][None, :, :] - p[free_src][:, None, :]) ** 2).sum(-1)).ravel()
        cells = np.floor(offsets / BLOCK_RESIDUAL_TOL).astype(np.int64)
        keys = (cells[..., 0] + (1 << 20)) * (1 << 21) + (cells[..., 1] + (1 << 20))
        uniq, inverse, counts = np.unique(keys.ravel(), return_inverse=True, return_counts=True)
        # Only transforms that carry the block a short way are moves; a lattice shift of several
        # squares gathers votes too but is a relabelling. The pivot shift a cell implies is
        # measured on its own voters: the mean of their targets less the mean of their sources
        # (the whole cluster's centroid would be wrong for a sub-block off the cluster's centre,
        # which a rotation about the origin carries a long way even when the sub-block stays put).
        src_of_vote = np.repeat(np.arange(len(free_src)), len(free_dst))
        dst_of_vote = np.tile(np.arange(len(free_dst)), len(free_src))
        mean_src = np.stack([np.bincount(inverse, weights=p[free_src][src_of_vote, k], minlength=len(uniq)) / counts for k in (0, 1)], axis=1)
        mean_dst = np.stack([np.bincount(inverse, weights=q[free_dst][dst_of_vote, k], minlength=len(uniq)) / counts for k in (0, 1)], axis=1)
        shift = np.sqrt(((mean_dst - mean_src) ** 2).sum(-1))
        # Against a lattice every lattice translation gathers the same votes, so among equally
        # voted cells the one whose voters travel least comes first.
        cell_travel = np.bincount(inverse, weights=travel_of, minlength=len(uniq)) / counts
        allowed = np.flatnonzero((shift <= BLOCK_SLIDE_MAX) & (counts >= BLOCK_MIN))
        order = allowed[np.lexsort((uniq[allowed], cell_travel[allowed], -counts[allowed]))][:BLOCK_HOUGH_TOP]
        best = None
        for key in uniq[order]:
            kx, ky = int(key // (1 << 21)) - (1 << 20), int(key % (1 << 21)) - (1 << 20)
            near = (np.abs(cells[..., 0] - kx) <= 1) & (np.abs(cells[..., 1] - ky) <= 1)
            t = offsets[near].mean(axis=0)
            pairs = nearest_inliers(P + t, Q)
            if len(pairs) < BLOCK_MIN:
                continue
            ia = free_src[[a for a, _ in pairs]]
            jb = free_dst[[b for _, b in pairs]]
            phi, cp, cq = procrustes(p[ia], q[jb])
            # Refit and recount until the inlier set stops growing (a few rounds at most).
            for _round in range(BLOCK_REFIT_ROUNDS):
                refit = nearest_inliers(apply_rigid(p[free_src], phi, cp, cq), Q)
                if len(refit) < len(pairs) or refit == pairs:
                    break
                pairs = refit
                ia = free_src[[a for a, _ in pairs]]
                jb = free_dst[[b for _, b in pairs]]
                phi, cp, cq = procrustes(p[ia], q[jb])
            if float(np.hypot(*(cq - cp))) > BLOCK_SLIDE_MAX:
                continue
            # The transform is final; keep only the pairs it lands within tolerance (the last
            # refit moved it a little from the transform that chose them), so every member of a
            # block lands within BLOCK_RESIDUAL_TOL of its target under the block's own transform.
            residual = np.sqrt(((q[jb] - apply_rigid(p[ia], phi, cp, cq)) ** 2).sum(-1))
            keep = residual <= BLOCK_RESIDUAL_TOL
            if int(keep.sum()) < BLOCK_MIN:
                continue
            ia, jb, residual = ia[keep], jb[keep], residual[keep]
            travel = float(np.sqrt(((q[jb] - p[ia]) ** 2).sum(-1)).mean())
            candidate = {
                "pairs": [(int(i), int(j)) for i, j in zip(ia, jb, strict=True)],
                "residual": residual,
                "turn": phi, "from": cp, "to": cq, "travel": travel,
            }
            if best is None or (-len(candidate["pairs"]), candidate["travel"]) < (-len(best["pairs"]), best["travel"]):
                best = candidate
        if best is None:
            break
        links.append(best)
        used_src = {i for i, _ in best["pairs"]}
        used_dst = {j for _, j in best["pairs"]}
        free_src = np.array([i for i in free_src if i not in used_src])
        free_dst = np.array([j for j in free_dst if j not in used_dst])
    return links


def cluster_extent(xy: np.ndarray, members: list[int]) -> tuple[np.ndarray, float]:
    pts = xy[members]
    centroid = pts.mean(axis=0)
    return centroid, float(np.sqrt(((pts - centroid) ** 2).sum(-1)).max())


def block_links(prev: dict, nxt: dict, prev_render: list[dict], nxt_render: list[dict]) -> tuple[list[dict], list[list[int]], list[list[int]]]:
    """Every rigid transform between reachable cluster pairs of the two frames, each tagged
    with its source cluster, and the two frames' clusters."""
    A = frame_clusters(prev, prev_render)
    B = frame_clusters(nxt, nxt_render)
    p, q = prev["xy"], nxt["xy"]
    links = []
    for index_a, a in enumerate(A):
        if len(a) < BLOCK_MIN:
            continue
        ca, ra = cluster_extent(p, a)
        theta_a = circular_mean_angle(prev["angles"][a])
        for b in B:
            if len(b) < BLOCK_MIN:
                continue
            cb, rb = cluster_extent(q, b)
            if float(np.hypot(*(cb - ca))) > ra + rb + 1.5:
                continue
            turn = angle_delta(theta_a, circular_mean_angle(nxt["angles"][b]))
            for link in rigid_links(p, q, a, b, turn):
                link["cluster"] = index_a
                links.append(link)
    return links, A, B


# --------------------------------------------------------------------------- matching


def base_cost(prev: dict, nxt: dict) -> tuple[np.ndarray, float, np.ndarray]:
    """Revision 4's square-level cost, n by n+1, the normalising scale, and which pairs move."""
    scale = max(prev["side"], nxt["side"])
    p, q = prev["xy"] / scale, nxt["xy"] / scale
    pa, qa = prev["angles"], nxt["angles"]
    d2 = ((p[:, None, :] - q[None, :, :]) ** 2).sum(-1)
    dang = np.abs(((qa[None, :] - pa[:, None] + 45.0) % 90.0) - 45.0)
    moves = (np.sqrt(d2) * scale > MOVE_TOLERANCE) | (dang > ROTATION_TOLERANCE_DEG)
    return d2 + ANGLE_WEIGHT * (dang / 45.0) ** 2 / scale**2, scale, moves


#: A swap has to save more than this, in the normalised cost's own units, to be taken. It is
#: there only to stop churn on exact ties: any real saving is a shorter journey and is worth having.
CROSSING_TOL = 1e-12


def repair_crossings(mapping: list[int], base: np.ndarray) -> tuple[list[int], int]:
    """Undo any pairing where two squares would be shorter off in each other's place.

    **The assignment does not minimise travel, and it is not meant to.** A block pairing is
    discounted so a shingled row lands as one rigid group, and a square that moves alone pays a
    penalty on top of its distance; both are worth having. But either can buy its coherence with a
    detour, and a detour that two squares take past each other is a swap -- which is what a viewer
    sees, and the one thing the motion cannot explain. At `n = 10 -> 11` the discount sent square 1
    to target 8, 1.425 unit sides away, and square 8 to target 9, 0.872 away; in each other's place
    they travel 0.586 and 0.248. Two squares crossing the packing to trade positions, for 2.3 unit
    sides of motion that buys nothing.

    So every pair of squares is offered the exchange, and it is taken whenever it shortens the two
    journeys together. The measure is `base`, the cost before any discount or penalty: squared
    centre distance plus the angle term, which is what "minimal relative to where the square is"
    means when a square can also turn.

    A block survives this untouched unless it was the thing causing the crossing. Swapping two
    members of a row that shifts by one cell sends each further, not nearer, so the exchange is
    refused; and the blocks are rebuilt from the repaired mapping by the caller, so a member that
    was swapped out simply is not one any more.

    The leftover column cannot change: an exchange moves two assigned targets between two squares
    and never touches the one no square took, so which square is *new* is decided before this runs
    and is unaffected by it.
    """
    order = list(mapping)
    swaps = 0
    while True:
        improved = False
        for i in range(len(order)):
            for j in range(i + 1, len(order)):
                keep = base[i, order[i]] + base[j, order[j]]
                trade = base[i, order[j]] + base[j, order[i]]
                if trade < keep - CROSSING_TOL:
                    order[i], order[j] = order[j], order[i]
                    swaps += 1
                    improved = True
        if not improved:
            return order, swaps


def exclusion_costs(cost: np.ndarray, rows: np.ndarray, cols: np.ndarray) -> np.ndarray:
    """For every column c, the least total cost of an assignment that leaves c out, from the
    optimal one: the cost of the shortest alternating path from c to the free column, found
    by relaxation over the columns (no negative cycles exist at optimality)."""
    n, m = cost.shape
    source_of = np.full(m, -1)
    source_of[cols] = rows
    (free,) = np.flatnonzero(source_of < 0)
    total = float(cost[rows, cols].sum())
    matched = np.flatnonzero(source_of >= 0)
    weights = np.full((m, m), np.inf)
    ia = source_of[matched]
    weights[matched, :] = cost[ia, :] - cost[ia, matched][:, None]
    dist = np.full(m, np.inf)
    dist[free] = 0.0
    for _ in range(m):
        relaxed = np.minimum(dist, (weights + dist[None, :]).min(axis=1))
        if np.array_equal(relaxed, dist):
            break
        dist = relaxed
    return total + dist


def shared_picture_removal(prev: dict, nxt: dict) -> int | None:
    """Index in n+1 whose removal gives n exactly, order preserved; None if not so."""
    a, b = prev["keys"], nxt["keys"]
    if len(b) != len(a) + 1:
        return None
    # Find the first divergence; the rest must line up shifted by one.
    i = 0
    while i < len(a) and a[i] == b[i]:
        i += 1
    if a[i:] == b[i + 1 :]:
        return i
    return None


def static_match(kind: str, n: int, mapping: list[int], new: int, rule: str, **extra) -> dict:
    return {
        "kind": kind, "map": mapping, "new": new, "cost": 0.0, "new_rule": rule, "new_tied": 1,
        "new_hungarian": new, "blocks": [], "block_of": [-1] * n, "clusters": (1, 1), "links": 0,
        **extra,
    }


def match_pair(prev: dict, nxt: dict, prev_render: list[dict], nxt_render: list[dict], manifest_entry_next: dict) -> dict:
    n = prev["n"]
    a_keys, b_keys = prev["keys"], nxt["keys"]
    if b_keys[:n] == a_keys:
        return static_match("prefix", n, list(range(n)), n, "prefix: square n+1 is appended")
    source = manifest_entry_next.get("source", {})
    recorded = source.get("source_n") == n + 1 and n in source.get("listed_n", [])
    removed = shared_picture_removal(prev, nxt)
    if recorded and removed is None:
        raise ValueError(f"pair {n}->{n + 1} is recorded as a shared picture but the poses differ")
    if removed is not None:
        mapping = [i if i < removed else i + 1 for i in range(n)]
        extra = {} if recorded else {"unrecorded": True}
        return static_match("shared-picture", n, mapping, removed, "shared picture: the catalogue's removed square", **extra)

    base, scale, moves = base_cost(prev, nxt)
    # Revision 4's assignment, kept for the comparison the notes report.
    h_rows, h_cols = linear_sum_assignment(base)
    (hungarian_new,) = sorted(set(range(n + 1)) - set(int(c) for c in h_cols))

    links, clusters_a, clusters_b = block_links(prev, nxt, prev_render, nxt_render)
    # Blocks first, then staying put, then moving alone: a square that moves alone pays the
    # penalty on top of its travel; a block member and a square that stays pay nothing extra.
    cost = base + moves * (INDIVIDUAL_PENALTY / scale**2)
    link_of: dict[tuple[int, int], int] = {}
    for k, link in enumerate(links):
        for (i, j), r in zip(link["pairs"], link["residual"], strict=True):
            cost[i, j] = BLOCK_DISCOUNT * base[i, j] + (float(r) / scale) ** 2
            link_of[(i, j)] = k
    # The tie-break, as an infinitesimal bonus on every column: the leftover column pays its own
    # badness, so among exactly tied choices the assignment leaves out the square with the fewest
    # full-side contacts, then the highest, then the rightmost.
    side = nxt["side"]
    badness = np.array([
        CONTACT_BADNESS * row["contacts"] + (side - y) + (side - x) / CONTACT_BADNESS
        for (x, y, _), row in zip(nxt["squares"], nxt_render, strict=True)
    ])
    cost -= NEW_BONUS * badness[None, :]
    rows, cols = linear_sum_assignment(cost)
    mapping = [0] * n
    for r, c in zip(rows, cols, strict=True):
        mapping[int(r)] = int(c)
    (new_index,) = sorted(set(range(n + 1)) - set(mapping))
    # Before anything is derived from it: no two squares may be shorter off in each other's place.
    # The blocks below are built by walking this mapping, so a repaired pairing rebuilds them.
    mapping, crossings_undone = repair_crossings(mapping, base)
    exclusion = exclusion_costs(cost, rows, cols)
    tied = sorted(int(c) for c in np.flatnonzero(exclusion - exclusion[new_index] <= NEW_TIE_TOL))
    if len(tied) == 1:
        rule = "lowest cost"
    else:
        contacts = {c: nxt_render[c]["contacts"] for c in tied}
        fewest = min(contacts.values())
        rule = "lowest cost, fewest contacts" if sum(1 for c in tied if contacts[c] == fewest) == 1 else "lowest cost, fewest contacts, highest position"

    # The blocks that survive the assignment: a link's members that were assigned along it, under
    # the link's own transform (its pivot travels at most BLOCK_SLIDE_MAX and every member lands
    # within BLOCK_RESIDUAL_TOL, both by construction); fewer than BLOCK_MIN members is not a
    # block and moves alone.
    members_of: dict[int, list[int]] = {}
    for i, j in enumerate(mapping):
        k = link_of.get((i, j))
        if k is not None:
            members_of.setdefault(k, []).append(i)
    blocks = []
    block_of = [-1] * n
    for k in sorted(members_of):
        members = members_of[k]
        if len(members) < BLOCK_MIN:
            continue
        link = links[k]
        residual_of = {i: float(r) for (i, _), r in zip(link["pairs"], link["residual"], strict=True)}
        residual = np.array([residual_of[i] for i in members])
        for i in members:
            block_of[i] = len(blocks)
        blocks.append({
            "members": members,
            "riders": [],
            "cluster": link["cluster"],
            "turn": round(float(link["turn"]), 6),
            "from": [round(float(link["from"][0]), 6), round(float(link["from"][1]), 6)],
            "to": [round(float(link["to"][0]), 6), round(float(link["to"][1]), 6)],
            "residual_mean": round(float(residual.mean()), 4),
            "residual_max": round(float(residual.max()), 4),
            "drift_max": 0.0,
        })
    # Riders: a moving square no core carries, whose assigned target lies within BLOCK_DRIFT_TOL
    # of where a core of its own cluster would take it, rides that core and drifts the rest of
    # the way, so a shingled row that shears as it lands still turns with its block.
    cluster_of = {i: k for k, members in enumerate(clusters_a) for i in members}
    drifts: dict[int, list[float]] = {}
    for i in range(n):
        if block_of[i] >= 0 or not moves[i, mapping[i]]:
            continue
        best = None
        for k, block in enumerate(blocks):
            if block["cluster"] != cluster_of[i]:
                continue
            landed = apply_rigid(prev["xy"][[i]], block["turn"], np.array(block["from"]), np.array(block["to"]))[0]
            drift = float(np.hypot(*(nxt["xy"][mapping[i]] - landed)))
            if drift <= BLOCK_DRIFT_TOL and (best is None or drift < best[0]):
                best = (drift, k)
        if best is not None:
            block_of[i] = best[1]
            blocks[best[1]]["riders"].append(i)
            drifts.setdefault(best[1], []).append(best[0])
    for k, block in enumerate(blocks):
        if k in drifts:
            block["drift_max"] = round(max(drifts[k]), 4)
    return {
        "kind": "matched", "map": mapping, "new": new_index, "cost": float(cost[rows, cols].sum()),
        "crossings_undone": crossings_undone,
        "new_rule": rule, "new_tied": len(tied), "new_hungarian": hungarian_new,
        "blocks": blocks, "block_of": block_of, "clusters": (len(clusters_a), len(clusters_b)), "links": len(links),
    }


# --------------------------------------------------------------------------- motion and statistics


def block_pose(a: tuple, b: tuple, block: dict | None, u: float) -> tuple[float, float, float]:
    """Where a square is at progress u of the move, as the page draws it: a block member rides
    its block's rotation about the source pivot while the pivot slides to its target, plus its
    own residual; a square alone slides straight and turns about its own centre."""
    if block is None:
        return a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] + angle_delta(a[2], b[2]) * u
    turn = block["turn"]
    dx, dy = a[0] - block["from"][0], a[1] - block["from"][1]
    ct, st = math.cos(math.radians(turn)), math.sin(math.radians(turn))
    rx = b[0] - (block["to"][0] + ct * dx - st * dy)
    ry = b[1] - (block["to"][1] + st * dx + ct * dy)
    c, s = math.cos(math.radians(turn * u)), math.sin(math.radians(turn * u))
    px = block["from"][0] + (block["to"][0] - block["from"][0]) * u
    py = block["from"][1] + (block["to"][1] - block["from"][1]) * u
    return px + c * dx - s * dy + rx * u, py + s * dx + c * dy + ry * u, a[2] + member_turn(turn, a[2], b[2]) * u


def member_turn(block_turn: float, a: float, b: float) -> float:
    """A block member's own turn, as the page computes it: the block's turn plus the correction
    to its own final tilt, taken the way round that keeps the total smallest (a square riding a
    45 degree block that ends upright is an exact tie, and stays upright rather than going round
    by 90)."""
    d = (b - a - block_turn) % 90.0
    one, other = block_turn + d, block_turn + d - 90.0
    return one if abs(one) <= abs(other) + 1e-9 else other


def crossing_count(prev: dict, nxt: dict, match: dict) -> tuple[int, float]:
    """Square pairs whose centres come within CROSSING_DISTANCE along the page's own paths."""
    n = prev["n"]
    if n < 2:
        return 0, float("inf")
    mapping = match["map"]
    p = prev["xy"]
    q = np.array([nxt["squares"][j][:2] for j in mapping])
    moving = np.linalg.norm(q - p, axis=1) > 1e-6
    if not moving.any():
        return 0, float("inf")
    close = np.zeros((n, n), dtype=bool)
    min_distance = float("inf")
    iu = np.triu_indices(n, 1)
    involved = (moving[:, None] | moving[None, :])[iu]
    blocks = match["blocks"]
    for t in np.linspace(0.0, 1.0, CROSSING_SAMPLES):
        c = np.array([
            block_pose(prev["squares"][i], nxt["squares"][mapping[i]], blocks[match["block_of"][i]] if match["block_of"][i] >= 0 else None, float(t))[:2]
            for i in range(n)
        ])
        d = np.sqrt(((c[:, None, :] - c[None, :, :]) ** 2).sum(-1))[iu]
        # Stationary touching neighbours sit at distance exactly 1; only moving pairs count.
        if involved.any():
            min_distance = min(min_distance, float(d[involved].min()))
        close[iu] |= (d < CROSSING_DISTANCE) & involved
    return int(close[iu].sum()), min_distance


def square_corners(x: float, y: float, angle: float) -> np.ndarray:
    c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    return np.array([(x + c * dx - s * dy, y + s * dx + c * dy) for dx, dy in ((-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5))])


def squares_overlap(a: tuple, b: tuple, depth: float = 1e-6) -> bool:
    """Two unit squares overlap with positive area (separating-axis test; touching does not count)."""
    ca, cb = square_corners(*a), square_corners(*b)
    for angle in (a[2], b[2]):
        for axis_angle in (angle, angle + 90.0):
            axis = np.array([math.cos(math.radians(axis_angle)), math.sin(math.radians(axis_angle))])
            pa, pb = ca @ axis, cb @ axis
            if pa.max() <= pb.min() + depth or pb.max() <= pa.min() + depth:
                return False
    return True


def arrival_overlaps(prev: dict, nxt: dict, new_index: int) -> list[int]:
    """The squares of n that the arriving square covers when it appears at its final pose before
    anything else has moved: the instant the default staging shows."""
    new = nxt["squares"][new_index]
    return [i for i, sq in enumerate(prev["squares"]) if squares_overlap(sq, new)]


def pair_stats(prev: dict, nxt: dict, match: dict) -> dict:
    n = prev["n"]
    mapping = match["map"]
    disp = []
    rot = []
    for i in range(n):
        x0, y0, a0 = prev["squares"][i]
        x1, y1, a1 = nxt["squares"][mapping[i]]
        disp.append(math.hypot(x1 - x0, y1 - y0))
        rot.append(abs(angle_delta(a0, a1)))
    crossings, min_pass = crossing_count(prev, nxt, match)
    scale = max(prev["side"], nxt["side"])
    moving = [i for i in range(n) if disp[i] > MOVE_TOLERANCE or rot[i] > ROTATION_TOLERANCE_DEG]
    in_block = [i for i in range(n) if match["block_of"][i] >= 0]
    moving_in_block = [i for i in moving if match["block_of"][i] >= 0]
    rigid = [i for b in match["blocks"] for i in b["members"]]
    riders = [i for b in match["blocks"] for i in b["riders"]]
    # A hop: a square sliding alone by half a unit or more without turning, the conveyor's step.
    hops = [i for i in moving if match["block_of"][i] < 0 and disp[i] >= 0.5 and rot[i] <= ROTATION_TOLERANCE_DEG]
    overlaps = arrival_overlaps(prev, nxt, match["new"])
    return {
        "n": n,
        "kind": match["kind"],
        "side_from": round(prev["side"], 6),
        "side_to": round(nxt["side"], 6),
        "mean_displacement": round(sum(disp) / n, 4),
        "max_displacement": round(max(disp), 4),
        "max_displacement_normalised": round(max(disp) / scale, 4),
        "moved_over_0_5": sum(1 for d in disp if d > 0.5),
        "moved_over_1_0": sum(1 for d in disp if d > 1.0),
        "rotated": sum(1 for r in rot if r > ROTATION_TOLERANCE_DEG),
        "max_rotation_deg": round(max(rot), 3),
        "crossings": crossings,
        # How many exchanges the repair took on this pair: the number of times two squares were
        # shorter off in each other's place than in the one the assignment gave them.
        "crossings_undone": match.get("crossings_undone", 0),
        "min_pass_distance": None if min_pass == float("inf") else round(min_pass, 3),
        "matching_cost": round(match["cost"], 6),
        "new_index": match["new"],
        "new_rule": match["new_rule"],
        "new_tied": match["new_tied"],
        "new_index_hungarian": match["new_hungarian"],
        "new_choice_differs": match["new"] != match["new_hungarian"],
        "clusters_from": match["clusters"][0],
        "clusters_to": match["clusters"][1],
        "links_found": match["links"],
        "block_count": len(match["blocks"]),
        "in_block": len(in_block),
        "rigid_members": len(rigid),
        "riders": len(riders),
        "individual": n - len(in_block),
        "moving": len(moving),
        "moving_in_block": len(moving_in_block),
        "moving_individually": len(moving) - len(moving_in_block),
        "alone_hops": len(hops),
        "stationary": n - len(moving),
        "block_residual_mean": round(sum(b["residual_mean"] * len(b["members"]) for b in match["blocks"]) / len(rigid), 4) if rigid else 0.0,
        "block_residual_max": max((b["residual_max"] for b in match["blocks"]), default=0.0),
        "rider_drift_max": max((b["drift_max"] for b in match["blocks"]), default=0.0),
        "arrival_overlaps": len(overlaps),
        "arrival_overlap_ids": overlaps,
        "blocks": match["blocks"],
        "block_of": match["block_of"],
        "map": mapping,
    }


def identity_chain(matches: dict[int, dict]) -> dict[int, list[int]]:
    """For each n, the global identity of every positional square: identity k is born as the new
    square of step k and follows the per-pair maps ever after."""
    identities = {1: [1]}
    for n in range(1, N_MAX):
        match = matches[n]
        nxt = [0] * (n + 1)
        for i, j in enumerate(match["map"]):
            nxt[j] = identities[n][i]
        nxt[match["new"]] = n + 1
        if sorted(nxt) != list(range(1, n + 2)):
            raise ValueError(f"identity chain breaks at {n}->{n + 1}")
        identities[n + 1] = nxt
    return identities


# --------------------------------------------------------------------------- facts


FRACTION_RE = re.compile(r"\((\d+)/(\d+)\)")
SQRT_RE = re.compile(r"\s*sqrt\((\d+)\)")
VULGAR = {"1/2": "½", "1/3": "⅓", "2/3": "⅔", "1/4": "¼", "3/4": "¾"}
# `side.display` and `lower.display` as the composite record writes them: s(n), a relation, a value.
SIDE_DISPLAY = re.compile(r"^s\((\d+)\) ([=≤≥]) (.+)$")


def pretty_exact(form: str | None) -> str | None:
    if not form:
        return None
    text = SQRT_RE.sub(lambda m: f"√{m.group(1)}", form)

    def fraction(m: re.Match) -> str:
        key = f"{m.group(1)}/{m.group(2)}"
        return VULGAR.get(key, f"({m.group(1)}⁄{m.group(2)})")

    text = FRACTION_RE.sub(fraction, text)
    text = text.replace(" + ", " + ").replace(" - ", " − ")
    return text


def load_facts(manifest_entries: dict[int, dict]) -> dict[str, dict]:
    figure = json.loads(COMPOSITE.read_text())["figure"]
    facts = {}
    for entry in figure["entries"]:
        n = entry["n"]
        side = entry["side"]
        relation = "=" if side["relation"] == "equality" else "≤"
        match = SIDE_DISPLAY.match(side["display"])
        if match is None or int(match.group(1)) != n or (match.group(2) == "=") != (relation == "="):
            raise ValueError(f"n={n}: side display {side['display']!r} does not read as s({n}) with its relation")
        value_text = match.group(3)
        # The proved lower bound, read as the slideshow reads it: shown for every open n, and the
        # record's own display must read `s(n) ≥ value`. Proved n leave the slot empty.
        lower = entry["lower"]
        lower_value = None
        if lower["shown"]:
            lmatch = SIDE_DISPLAY.match(lower["display"])
            if lmatch is None or lmatch.group(2) != "≥" or int(lmatch.group(1)) != n:
                raise ValueError(f"n={n}: lower display {lower['display']!r} does not read as s({n}) ≥ value")
            lower_value = lmatch.group(3)
        kind = manifest_entries[n]["source"]["kind"]
        badges = []
        for badge in entry["badges"]:
            key = (badge["glyph"], badge["style"])
            if key not in BADGE_VOCABULARY:
                raise ValueError(f"n={n}: badge {key} is not in the poster's vocabulary")
            badges.append({"glyph": badge["glyph"], "style": badge["style"], "meaning": badge["meaning"]})
        # What the record leaves open for this n, in the panel's fixed order.
        open_items = []
        if entry["optimality"]["status"] == "open":
            open_items.append("optimality")
        if entry["exactness"]["state"] not in ("closed-form", "minimal-polynomial"):
            open_items.append("exact value")
        if entry["rigidity"]["state"] == "not-established":
            open_items.append("rigidity")
        facts[str(n)] = {
            "relation": relation,
            # The TeX the panel's three lines are set from, rendered below, once, for every n.
            # The two bounds are the panel's statement and have to carry across a room, so they
            # are set in the bold companions of the same faces rather than in a heavier weight of
            # something else. The closed form stays regular: it annotates the bound rather than
            # competing with it.
            # Only the VALUE takes the bound's colour. `s(n)` names the same quantity
            # in both lines and the relation is what distinguishes them, so colouring
            # either would say that two different things are being talked about.
            "tex_side": BOLD % (
                f"s({n}) {'=' if relation == '=' else LE} "
                + colour(UPPER_INK, value_text)
            ),
            "tex_lower": (
                None
                if lower_value is None
                else BOLD % (f"s({n}) {GE} " + colour(LOWER_INK, lower_value))
            ),
            # The headline under the packing, set as mathematics like everything else.
            "tex_headline": BOLD % f"n = {n}",
            "tex_exact": (
                None
                if not entry["exactness"].get("exact_form")
                else "= " + tex_of_exact(entry["exactness"]["exact_form"])
            ),
            "side": value_text,
            "exact": pretty_exact(entry["exactness"].get("exact_form")),
            "exact_state": entry["exactness"]["state"],
            "degree": entry["exactness"].get("degree"),
            "status": entry["optimality"]["status"],
            "lower": lower_value,
            "kind": kind,
            "badges": badges,
            "star": bool(lower["first_proved_here"]),
            "open": open_items,
        }
    # One call to KaTeX for the whole corpus rather than one per expression: the cost is a node
    # start, and there are about a thousand expressions behind it.
    keys = ("tex_side", "tex_lower", "tex_exact", "tex_headline")
    order = [(n, key) for n in sorted(facts, key=int) for key in keys if facts[n][key] is not None]
    rendered = katex_html([facts[n][key] for n, key in order])
    for (n, key), html in zip(order, rendered, strict=True):
        facts[n][key.replace("tex_", "html_")] = html
    for n in facts:
        for key in keys:
            facts[n].setdefault(key.replace("tex_", "html_"), None)
            del facts[n][key]
    return facts


# --------------------------------------------------------------------------- type metrics


def glyph_bounds(font, char: str) -> tuple[float, float]:
    """(yMin, yMax) of one glyph's ink in font units, from the glyf table."""
    name = font.getBestCmap()[ord(char)]
    glyph = font["glyf"][name]
    if glyph.numberOfContours == 0:
        raise ValueError(f"{char!r} has no outline")
    return float(glyph.yMin), float(glyph.yMax)


def approx_outline() -> dict:
    """KaTeX_Main's U+2248 as an SVG path in font units, with its advance and ink bounds.

    Coordinates are rounded to a tenth of a font unit, so the emitted path is the same
    bytes on every build (the slideshow candidate does the same). The page draws it in
    the badge box with `translate(tx baseline) scale(k -k)`, k = APPROX_FONT_SIZE / 1000,
    centred on its own ink as the atlas centres a math symbol.
    """
    from fontTools.pens.boundsPen import BoundsPen  # noqa: PLC0415
    from fontTools.pens.svgPathPen import SVGPathPen  # noqa: PLC0415
    from fontTools.ttLib import TTFont  # noqa: PLC0415

    katex = TTFont(KATEX_FONTS / "KaTeX_Main-Regular.woff2")
    if katex["head"].unitsPerEm != 1000:
        raise ValueError("KaTeX_Main is not on a 1000-unit em")
    glyph_set = katex.getGlyphSet()
    name = katex.getBestCmap()[ord("≈")]
    pen = SVGPathPen(glyph_set, ntos=lambda v: format(round(v, 1), "g"))
    glyph_set[name].draw(pen)
    bounds = BoundsPen(glyph_set)
    glyph_set[name].draw(bounds)
    _x0, y0, _x1, y1 = bounds.bounds
    return {
        "d": pen.getCommands(),
        "advance": glyph_set[name].width,
        "y0": round(y0, 1),
        "y1": round(y1, 1),
        "font_size": APPROX_FONT_SIZE,
        "stroke_units": APPROX_STROKE_UNITS,
    }


def median(values: list[float]) -> float:
    ordered = sorted(values)
    mid = len(ordered) // 2
    return ordered[mid] if len(ordered) % 2 else (ordered[mid - 1] + ordered[mid]) / 2


def left_bearing(font, char: str) -> float:
    """The glyph's left side bearing in em, from the hmtx table."""
    name = font.getBestCmap()[ord(char)]
    return font["hmtx"][name][1] / font["head"].unitsPerEm


def type_metrics() -> dict:
    """Lengths the page needs to place type and marks, read from the embedded faces.

    A badge glyph is centred in its box the way the atlas does it: letters on their cap
    height, `=` on the middle of its own ink, and `?` likewise; the approximately-equal
    sign is drawn from KaTeX_Main's outline. The numeral's box is offset from the `n =`
    line's so the two align on their ink: the italic n's left bearing at the line's size
    less the median digit's at the numeral's size, in the faces the page sets them in
    (revision 4: the regular face, whose digits carry more side bearing than the bold).
    """
    from fontTools.ttLib import TTFont  # noqa: PLC0415

    sans = TTFont(FONTS / "source-sans-3-latin-wght-normal.woff2")
    serif = TTFont(FONTS / f"pt-serif-latin-{NUMERAL_WEIGHT}-normal.woff2")
    italic = TTFont(FONTS / "pt-serif-latin-400-italic.woff2")

    def centre(font, chars: str) -> float:
        """The middle of the ink, in em; over several glyphs, the median."""
        return median([(lo + hi) / 2 for lo, hi in (glyph_bounds(font, c) for c in chars)]) / font["head"].unitsPerEm

    cap = sans["OS/2"].sCapHeight / sans["head"].unitsPerEm
    letter_baseline = (BADGE_SIZE + BADGE_FONT_SIZE * cap) / 2
    math_baseline = BADGE_SIZE / 2 + BADGE_FONT_SIZE * centre(sans, "=")
    query_baseline = BADGE_SIZE / 2 + BADGE_FONT_SIZE * centre(sans, "?")
    digit_bearing_px = median([left_bearing(serif, d) for d in "0123456789"]) * NUMERAL_PX
    n_bearing_px = left_bearing(italic, "n") * N_LINE_PX
    return {
        "type_scale": TYPE_SCALE,
        "numeral_px": NUMERAL_PX,
        "numeral_weight": NUMERAL_WEIGHT,
        "n_line_px": N_LINE_PX,
        "headline_gap_px": HEADLINE_GAP_PX,
        # The gap bar's two ends, set by the same KaTeX as the panel's lines. They are the same
        # expression at every n, so they are rendered once here rather than per pair.
        "bound_html": dict(
            zip(("area", "grid"), katex_html([r"\sqrt{n}", r"\sqrt{n} + 1"]), strict=True)
        ),
        "digit_bearing_px": round(digit_bearing_px, 2),
        "n_bearing_px": round(n_bearing_px, 2),
        "badge_baseline": {
            "letter": round(letter_baseline, 3),
            "math": round(math_baseline, 3),
            "query": round(query_baseline, 3),
        },
        "approx": approx_outline(),
        "star_inset": STAR_INSET,
        "star_span": STAR_SPAN,
    }


# --------------------------------------------------------------------------- html


# --------------------------------------------------------------------------- the mathematics
KATEX_JS = KATEX_FONTS.parent / "katex.min.js"


def katex_css() -> str:
    """KaTeX's stylesheets, through the explainer's own inliner.

    **Reused rather than rewritten, and the reuse is the point.** `render_explainer.katex_css`
    already does this for the paper: it takes kpress's two stylesheets in kpress's order, inlines
    the faces the page can actually reach and drops the rest (every face is 30-40 kB), and it
    includes `katex-text-face.css` -- the composite that draws the letters and digits of mathematics
    from PT Serif and leaves the rest to the KaTeX faces. That composite is what makes the paper's
    mathematics look like the paper rather than like generic KaTeX, and it is exactly what the owner
    asked this panel to match. A second implementation here would have been a second thing to keep
    in step with kpress, and would have got the visual match wrong by leaving it out.
    """
    from devtools.render_explainer import katex_css as inline_katex, kpress_static  # noqa: PLC0415

    return inline_katex(kpress_static())


def tex_of_exact(form: str) -> str:
    """The recorded closed form as TeX.

    The composite writes these in a plain algebraic notation -- `(7/2) + (3/2)sqrt(2)` -- which is
    readable and is not typeset. This is the one translation between the two: a parenthesised
    quotient becomes a fraction and `sqrt(x)` becomes a radical. Everything else passes through
    because everything else is already TeX-safe: digits, signs and spaces.
    """

    def fraction(match: re.Match[str]) -> str:
        # `\dfrac`, not `\frac`. Inline style compresses a fraction to script size and squeezes it
        # between the lines around it, which on a poster reads as a smudge rather than as a number.
        # Display style gives it its full height, which is what the line has room for.
        return "\\dfrac{" + match.group(1) + "}{" + match.group(2) + "}"

    def radical(match: re.Match[str]) -> str:
        return "\\sqrt{" + match.group(1) + "}"

    out = re.sub(r"\((\d+)/(\d+)\)", fraction, form)
    return re.sub(r"sqrt\(([^()]+)\)", radical, out)


def katex_html(sources: list[str]) -> list[str]:
    """Render every expression once, through the vendored KaTeX, at build time.

    **Build time, not run time, and this is the point of it.** The panel's expressions are a fixed
    set -- three per n -- so there is nothing to render while anyone is watching, and the page does
    not have to carry a 280 kB typesetting engine to show them. It carries the answers.

    It is the same KaTeX the explainer sets its mathematics with, from the same vendored copy, so
    the panel's `s(11) <= 3.877084` is set the way the paper's is rather than approximated with
    hand-placed spans in a face that happens to have a relation glyph.
    """
    if not sources:
        return []
    script = (
        f"import katex from {json.dumps(str(KATEX_JS))};\n"
        "let raw = '';\n"
        "for await (const chunk of process.stdin) raw += chunk;\n"
        "const out = JSON.parse(raw).map((tex) => katex.renderToString(tex,\n"
        "  {throwOnError: true, output: 'html', displayMode: false, strict: 'error'}));\n"
        "process.stdout.write(JSON.stringify(out));\n"
    )
    with tempfile.TemporaryDirectory() as hold:
        entry = Path(hold) / "render.mjs"
        entry.write_text(script, encoding="utf-8")
        done = subprocess.run(
            ["node", str(entry)],
            input=json.dumps(sources),
            capture_output=True,
            text=True,
            check=False,
        )
    if done.returncode != 0:
        raise SystemExit(f"KaTeX rendering failed:\n{done.stderr[-2000:]}")
    return json.loads(done.stdout)


def font_css() -> str:
    """The embedded faces. Each latin face is limited to kpress's latin range and the symbols
    face to the relation code points, and the symbols face is size-adjusted to sit with PT
    Serif, as the slideshow candidate declares them."""
    blocks = []
    for family, weight, style, path in FONT_FACES:
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        symbols = family == "Atlas Symbols"
        unicode_range = SYMBOL_RANGE if symbols else LATIN_RANGE
        extra = f"size-adjust:{SYMBOL_SIZE_ADJUST};" if symbols else ""
        blocks.append(
            f"@font-face{{font-family:'{family}';font-weight:{weight};font-style:{style};"
            f"font-display:block;{extra}src:url(data:font/woff2;base64,{data}) format('woff2');"
            f"unicode-range:{unicode_range};}}"
        )
    return "\n".join(blocks)


def compact_frame(witness: dict, rendering: list[dict], identities: list[int]) -> dict:
    squares = []
    for (x, y, angle), row in zip(witness["squares"], rendering, strict=True):
        squares.append([round(x, 6), round(y, 6), round(angle, 4), row["fill"], row["contacts"]])
    return {"side": round(witness["side"], 9), "squares": squares, "ident": identities}


def asset(name: str) -> str:
    """The text of `assets/<name>`, without its final newline.

    The page's stylesheet and script live beside the template rather than inside it, because
    nothing could read them where they were: 395 lines of CSS and 5,079 of JavaScript sealed in an
    HTML file that is itself composed by Python string operations, so no formatter indented them,
    no linter parsed them and no editor coloured them as code. Each is now a file in the language
    it is written in, and every tool for that language applies to it.

    They are inlined here the way the faces are -- a `__TOKEN__` alone on a line, replaced with
    `str.replace`. **`str.replace` and not `%` or `.format`,** which is not a preference: the
    script is full of `{`, `}` and `%`, and a format string would read every one of them as its
    own punctuation. Interpolating code into a template is the seam that put a doubled backslash
    from an f-string into the rendered page and broke a line of mathematics in two.

    The final newline goes because the token's own line supplies it. The split was required to
    leave the built page byte-for-byte what it was, and the newline is where that is won or lost.
    """
    return (HERE / "assets" / name).read_text(encoding="utf-8").removesuffix("\n")


def build_html(template: str, payload: dict) -> str:
    data = json.dumps(payload, separators=(",", ":"), sort_keys=True, ensure_ascii=False)
    # A closing script tag inside JSON would end the data block early; there is none, but be safe.
    data = data.replace("</", "<\\/")
    html = (
        # The page is assembled before it is filled: the stylesheet and the script go in first, so
        # a face, KaTeX or data token is substituted wherever it ends up standing.
        template.replace("__WORKBENCH_CSS__", asset("workbench.css"))
        .replace("__WORKBENCH_JS__", asset("workbench.js"))
        .replace("__FONT_CSS__", font_css())
        .replace("__KATEX_CSS__", katex_css())
        .replace("__DATA__", data)
    )
    # The explainer's own check, not a substring search for "http". KaTeX draws a radical as an
    # inline SVG, and an SVG carries `xmlns="http://www.w3.org/2000/svg"` -- a namespace name, which
    # is read and never fetched. `EXTERNAL_REFERENCE` matches the four things that do fetch: a
    # script's src, a link's href, an @import, and a url() that is not a data URI.
    from devtools.render_explainer import EXTERNAL_REFERENCE  # noqa: PLC0415

    found = EXTERNAL_REFERENCE.search(html)
    if found is not None:
        raise ValueError(f"index.html must not reference anything outside itself: {found.group(0)!r}")
    return html


NUMBER_ARRAY_RE = re.compile(r"\[\s*((?:(?:-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?|null|true|false)\s*,\s*)*(?:-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?|null|true|false))\s*\]")


def compact_json(document: dict) -> str:
    """Indented JSON whose arrays of scalars sit on one line each, so the maps, the identity
    chain and the block members stay readable without a line per integer."""
    text = json.dumps(document, indent=1, sort_keys=True)
    return NUMBER_ARRAY_RE.sub(lambda m: "[" + re.sub(r"\s+", " ", m.group(1)) + "]", text) + "\n"


# --------------------------------------------------------------------------- summary


HISTOGRAM_BINS = [0.0, 0.001, 0.5, 1.0, 2.0, 3.0, 5.0, 8.0, 12.0, float("inf")]


def summary_text(stats: list[dict]) -> str:
    lines = []
    kinds = {}
    for s in stats:
        kinds.setdefault(s["kind"], []).append(s)
    lines.append("| kind | pairs | mean of max displacement | max of max displacement | pairs with any rotation | mean crossings |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")
    for kind in ("prefix", "shared-picture", "matched"):
        rows = kinds.get(kind, [])
        if not rows:
            continue
        lines.append(
            f"| {kind} | {len(rows)} | {sum(r['max_displacement'] for r in rows) / len(rows):.3f} | "
            f"{max(r['max_displacement'] for r in rows):.3f} | "
            f"{sum(1 for r in rows if r['rotated'] > 0)} | "
            f"{sum(r['crossings'] for r in rows) / len(rows):.1f} |"
        )
    lines.append("")
    total = len(stats)
    under = lambda x: sum(1 for s in stats if s["max_displacement"] < x)
    lines.append(f"Pairs with max displacement under 1 unit: {under(1.0)} of {total}")
    lines.append(f"Pairs with max displacement under 3 units: {under(3.0)} of {total}")
    lines.append(f"Pairs with max displacement over 5 units: {sum(1 for s in stats if s['max_displacement'] > 5.0)} of {total}")
    lines.append(f"Pairs with max displacement over 10 units: {sum(1 for s in stats if s['max_displacement'] > 10.0)} of {total}")
    lines.append("")
    lines.append("Histogram of maximum matched displacement (unit-square units), all 323 pairs:")
    lines.append("")
    lines.append("```")
    labels = ["exactly 0", "(0, 0.5)", "[0.5, 1)", "[1, 2)", "[2, 3)", "[3, 5)", "[5, 8)", "[8, 12)", "12 and over"]
    counts = [0] * len(labels)
    for s in stats:
        d = s["max_displacement"]
        for i in range(len(labels)):
            lo, hi = HISTOGRAM_BINS[i], HISTOGRAM_BINS[i + 1]
            if (lo <= d < hi) if i > 0 else d < hi:
                counts[i] += 1
                break
    width = max(counts) or 1
    for label, count in zip(labels, counts, strict=True):
        bar = "#" * round(40 * count / width)
        lines.append(f"{label:>12} | {count:3d} {bar}")
    lines.append("```")
    lines.append("")
    matched = sorted(kinds.get("matched", []), key=lambda s: -s["max_displacement"])
    lines.append("Most chaotic pairs (by maximum displacement):")
    lines.append("")
    lines.append("| pair | side | max disp | mean disp | moved >1 | rotated | crossings | blocks | moving in blocks | alone |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for s in matched[:15]:
        lines.append(
            f"| {s['n']}→{s['n'] + 1} | {s['side_from']:.3f}→{s['side_to']:.3f} | {s['max_displacement']:.2f} | "
            f"{s['mean_displacement']:.2f} | {s['moved_over_1_0']} | {s['rotated']} | {s['crossings']} | "
            f"{s['block_count']} | {s['moving_in_block']} | {s['moving_individually']} |"
        )
    lines.append("")
    graceful = sorted(kinds.get("matched", []), key=lambda s: s["max_displacement"])
    lines.append("Most graceful matched pairs (by maximum displacement):")
    lines.append("")
    lines.append("| pair | side | max disp | mean disp | moved >1 | rotated | crossings | blocks | moving in blocks | alone |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for s in graceful[:12]:
        lines.append(
            f"| {s['n']}→{s['n'] + 1} | {s['side_from']:.3f}→{s['side_to']:.3f} | {s['max_displacement']:.2f} | "
            f"{s['mean_displacement']:.2f} | {s['moved_over_1_0']} | {s['rotated']} | {s['crossings']} | "
            f"{s['block_count']} | {s['moving_in_block']} | {s['moving_individually']} |"
        )
    lines.append("")
    by_rot = max(stats, key=lambda s: (s["rotated"], s["n"]))
    by_disp = max(stats, key=lambda s: (s["max_displacement"], s["n"]))
    lines.append(f"Largest matched rotation count: {by_rot['n']}→{by_rot['n'] + 1} ({by_rot['rotated']} squares rotate)")
    lines.append(f"Largest maximum displacement: {by_disp['n']}→{by_disp['n'] + 1} ({by_disp['max_displacement']:.2f} units)")
    lines.append("")
    lines.extend(block_summary_lines(kinds.get("matched", []), stats))
    lines.append("")
    per_pair = TIMING["dwell"] + TIMING["move"] + TIMING["settle"]
    total_seconds = per_pair * total + TIMING["dwell"]
    lines.append(
        f"Full 1..324 run at dwell {TIMING['dwell']} s, move {TIMING['move']} s, settle {TIMING['settle']} s: "
        f"{total_seconds:.1f} s = {total_seconds / 60:.1f} min ({total} transitions plus a closing dwell)"
    )
    static = sum(1 for s in stats if s["kind"] != "matched")
    moving = total - static
    for name, timing in STATIC_APPEND_TIMINGS.items():
        static_pair = timing["dwell"] + timing["move"] + timing["settle"]
        seconds = per_pair * moving + static_pair * static + TIMING["dwell"]
        lines.append(
            f"Per-kind schedule, static appends at dwell {timing['dwell']} s, move {timing['move']} s, "
            f"settle {timing['settle']} s ({name}): {moving} × {per_pair:.1f} + {static} × {static_pair:.1f} + "
            f"{TIMING['dwell']} = {seconds:.1f} s = {seconds / 60:.1f} min"
        )
    return "\n".join(lines)


def block_summary_lines(matched: list[dict], stats: list[dict]) -> list[str]:
    """Revision 5's headline numbers: how the 158 assignment pairs move, the residuals, the
    new-square rule and the arrival overlap census."""
    lines = []
    m = len(matched)
    moving = sum(s["moving"] for s in matched)
    in_blocks = sum(s["moving_in_block"] for s in matched)
    lines.append(f"Block matching over the {m} assignment pairs (clusters within {CLUSTER_ANGLE_TOL:g} degrees and a gap of {CLUSTER_GAP_TOL:g}, residual tolerance {BLOCK_RESIDUAL_TOL:g}, discount {BLOCK_DISCOUNT:g}):")
    lines.append("")
    mostly = sum(1 for s in matched if s["moving"] and s["moving_in_block"] >= 0.5 * s["moving"])
    nearly_all = sum(1 for s in matched if s["moving"] and s["moving_in_block"] >= 0.9 * s["moving"])
    entirely = sum(1 for s in matched if s["moving"] and s["moving_individually"] == 0)
    fallback = sum(1 for s in matched if s["moving_individually"] > 0)
    lines.append(f"- Moving squares carried by a block: {in_blocks} of {moving} ({100 * in_blocks / moving:.1f}%)")
    lines.append(f"- Pairs whose moving squares are at least half in blocks: {mostly} of {m}; at least nine in ten: {nearly_all}; all of them: {entirely}")
    lines.append(f"- Pairs where some moving square fell back to a square-level move: {fallback} of {m}")
    lines.append(f"- Blocks per pair: mean {sum(s['block_count'] for s in matched) / m:.1f}, max {max(s['block_count'] for s in matched)}; clusters per frame (from, to): mean {sum(s['clusters_from'] for s in matched) / m:.1f}, {sum(s['clusters_to'] for s in matched) / m:.1f}")
    with_blocks = [s for s in matched if s["block_count"]]
    mean_res = sum(s["block_residual_mean"] * s["in_block"] for s in with_blocks) / max(1, sum(s["in_block"] for s in with_blocks))
    lines.append(f"- Residual after the block transform, over block members: mean {mean_res:.3f} units, max {max((s['block_residual_max'] for s in with_blocks), default=0):.3f}; pairs with a max residual over 0.2: {sum(1 for s in with_blocks if s['block_residual_max'] > 0.2)}")
    lines.append("")
    lines.append(f"New-square rule: {NEW_RULE}.")
    lines.append("")
    by_rule: dict[str, int] = {}
    for s in matched:
        by_rule[s["new_rule"]] = by_rule.get(s["new_rule"], 0) + 1
    for rule, count in sorted(by_rule.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- decided by {rule}: {count} pairs")
    differs = [s["n"] for s in matched if s["new_choice_differs"]]
    lines.append(f"- choice differs from revision 4's leftover: {len(differs)} of {m} pairs")
    lines.append(f"- tie sets larger than one: {sum(1 for s in matched if s['new_tied'] > 1)} pairs, the largest {max(s['new_tied'] for s in matched)} candidates")
    lines.append("")
    overlapping = [s for s in stats if s["arrival_overlaps"]]
    lines.append(f"Arrival overlap census (the new square at its final pose against the squares of n before they move): {len(overlapping)} of {len(stats)} pairs, {sum(s['arrival_overlaps'] for s in overlapping)} squares covered in all; max {max((s['arrival_overlaps'] for s in stats), default=0)} in one pair; mean over the overlapping pairs {sum(s['arrival_overlaps'] for s in overlapping) / max(1, len(overlapping)):.2f}")
    return lines


# --------------------------------------------------------------------------- main


class Stopwatch:
    """Wall time per named stage of the build, so a stage that gets slow says so.

    Every stage here is at least O(n^2) in the number of squares and one of them is a Hungarian
    assignment, which is cubic; the corpus runs them 323 times. A change that makes one of them
    quadratically worse would still finish, just slowly, and would be noticed as "the build feels
    slow" some weeks later. The timings go into the stats record beside the measurements they
    produced, so a regression is a diff rather than a memory.
    """

    def __init__(self) -> None:
        self.totals: dict[str, float] = {}

    @contextmanager
    def stage(self, name: str):
        started = time.perf_counter()
        try:
            yield
        finally:
            self.totals[name] = self.totals.get(name, 0.0) + (time.perf_counter() - started)

    def record(self) -> dict[str, float]:
        return {name: round(seconds, 3) for name, seconds in sorted(self.totals.items())}

    def report(self) -> str:
        rows = sorted(self.totals.items(), key=lambda kv: -kv[1])
        total = sum(self.totals.values())
        body = "\n".join(f"  {seconds:7.2f}s  {name}" for name, seconds in rows)
        return f"Build timings ({total:.1f}s in all):\n{body}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=HERE)
    parser.add_argument("--all", action="store_true", help="also write index-all.html with every pair embedded")
    args = parser.parse_args(argv)
    out: Path = args.out
    out.mkdir(parents=True, exist_ok=True)

    clock = Stopwatch()
    manifest = json.loads(MANIFEST.read_text())["atlas"]["entries"]
    manifest_by_n = {entry["n"]: entry for entry in manifest}
    with clock.stage("read the witnesses and renderings"):
        witnesses = {n: load_witness(n) for n in range(1, N_MAX + 1)}
        renderings = {n: load_rendering(n) for n in range(1, N_MAX + 1)}
    with clock.stage("read the facts"):
        facts = load_facts(manifest_by_n)

    stats = []
    matches = {}
    for n in range(1, N_MAX):
        with clock.stage("match the pairs"):
            match = match_pair(witnesses[n], witnesses[n + 1], renderings[n], renderings[n + 1], manifest_by_n[n + 1])
        matches[n] = match
        with clock.stage("measure the pairs"):
            stats.append(pair_stats(witnesses[n], witnesses[n + 1], match))
    with clock.stage("chain the identities"):
        identities = identity_chain(matches)

    summary = summary_text(stats)
    print(summary)

    by_rot = max(stats, key=lambda s: (s["rotated"], s["n"]))["n"]
    by_disp = max(stats, key=lambda s: (s["max_displacement"], s["n"]))["n"]
    demo = sorted(set(REQUIRED_PAIRS + EXTRA_PAIRS + OPENING_RUN + SEQUENCE_RUN + FINALE + [by_rot, by_disp]))

    stats_doc = {
        "generated_by": "build_candidate.py (spike v2 transitions, revision 5)",
        "angle_weight": ANGLE_WEIGHT,
        "rotation_tolerance_deg": ROTATION_TOLERANCE_DEG,
        "crossing_distance": CROSSING_DISTANCE,
        # The build's own timings are deliberately NOT recorded here. They are a measurement of
        # this machine on this run, and writing them into a tracked artifact made two runs differ
        # in bytes -- against this generator's "two runs give identical bytes" -- and churned a
        # file that `pages.yml` and `build_workbench_site.py` both declare as a render input.
        # They are printed to stdout instead, where a measurement of the run belongs.
        "block_matching": {
            "cluster_angle_tol_deg": CLUSTER_ANGLE_TOL,
            "cluster_gap_tol": CLUSTER_GAP_TOL,
            "residual_tol": BLOCK_RESIDUAL_TOL,
            "block_min": BLOCK_MIN,
            "discount": BLOCK_DISCOUNT,
            "new_square_rule": NEW_RULE,
            "new_tie_tol": NEW_TIE_TOL,
        },
        "timing": TIMING,
        "arrival_fraction": ARRIVAL_FRACTION,
        "motion_phases": MOTION_PHASES,
        "embedded_pairs": demo,
        "largest_max_displacement_pair": by_disp,
        "largest_rotation_count_pair": by_rot,
        "identities": {str(n): identities[n] for n in range(1, N_MAX + 1)},
        "pairs": stats,
    }
    (out / "transition-stats.json").write_text(compact_json(stats_doc))
    # The footer the documentation floor requires on every durable Markdown file. It was being
    # maintained by HAND on a generated file, so every rebuild silently dropped it and the floor
    # only noticed on the next commit. A generated document's footer is the generator's to write.
    (out / "stats-summary.md").write_text(STATS_BANNER + summary + "\n\n" + DOC_FOOTER)

    template = (HERE / "template.html").read_text()
    metrics = type_metrics()

    def payload_for(pair_ns: list[int]) -> dict:
        frame_ns = sorted({n for p in pair_ns for n in (p, p + 1)})
        return {
            "frames": {str(n): compact_frame(witnesses[n], renderings[n], identities[n]) for n in frame_ns},
            "pairs": [
                {
                    "n": n,
                    "kind": matches[n]["kind"],
                    "map": matches[n]["map"],
                    "new": matches[n]["new"],
                    "new_rule": matches[n]["new_rule"],
                    "new_tied": matches[n]["new_tied"],
                    "blocks": [{k: v for k, v in b.items() if k != "residual_mean" and k != "residual_max"} for b in matches[n]["blocks"]],
                    "block_of": matches[n]["block_of"],
                    # The square of frame n that arrived in the pair before: it keeps its scarlet
                    # outline through this pair's dwell. Known for every n from the full matching.
                    "prev_new": matches[n - 1]["new"] if n > 1 else None,
                    "stats": {
                        k: stats[n - 1][k]
                        for k in (
                            "max_displacement", "mean_displacement", "rotated", "moved_over_1_0", "crossings",
                            "block_count", "moving", "moving_in_block", "moving_individually",
                            "block_residual_mean", "block_residual_max", "arrival_overlaps",
                        )
                    },
                }
                for n in pair_ns
            ],
            "facts": {str(n): facts[str(n)] for n in frame_ns},
            "timing": TIMING,
            "arrival_fraction": ARRIVAL_FRACTION,
            "motion_phases": MOTION_PHASES,
            "n_max": N_MAX,
            "metrics": metrics,
            "star_points": STAR_POINTS,
            "sequence_kinds": {str(s["n"]): s["kind"] for s in stats},
        }

    html = build_html(template, payload_for(demo))
    (out / "index.html").write_text(html)
    print(f"\nindex.html: {len(html.encode('utf-8'))} bytes, {len(demo)} pairs embedded: {demo}")
    print()
    print(clock.report())
    if args.all:
        html_all = build_html(template, payload_for(list(range(1, N_MAX))))
        (out / "index-all.html").write_text(html_all)
        print(f"index-all.html: {len(html_all.encode('utf-8'))} bytes, 323 pairs embedded")
        # Revision 8: the workbench is the all-pairs build under the name the owner opens. The
        # sequence tab defaults to 1..100 and the single-step tab to 16 -> 17, and neither exists in
        # the 25-pair demo, so the file with everything in it is the one that should be obvious.
        (out / "workbench.html").write_text(html_all)
        print(f"workbench.html: the same {len(html_all.encode('utf-8'))} bytes, the file to open")
    return 0


if __name__ == "__main__":
    sys.exit(main())
