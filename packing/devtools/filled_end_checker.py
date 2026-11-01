"""Decide a filled-end two-band L packing exactly from its parameters (#847, think-fuwd).

Mohsen Karimi's filled-end set V2.0 (#847; Zenodo 10.5281/zenodo.23819397) states 5,134
upper bounds at n = 1182 to 9946, and V1.0 (Zenodo 10.5281/zenodo.23681705, reported on
#836 on 27 October) states 4,571 at 1184 to 9946. No row has a certificate file: each
states an exact side S, K = ceil(sqrt(n)), and six parameters bV, tV, yV, bH, tH and yH of
one packing. It is Sungjoon Ryu's L-shaped packing (his Theorem 1.3) with two tilted bands
of independent width, tilt and lift, and each band's two ends filled with axis-parallel
layers, Evan Daniel's idea as Kevin Fang's note writes it. By the owner's D2 answer
(think-f2io) such a row is a row once a checker this project maintains decides it exactly
from its recipe; this module is that checker for the filled-end kind.
`devtools.two_strip_checker` decides the two-strip rows of #799 and #836 and does not read
these.

**The construction.** The author's ``filled_ends.py`` states it; this module was written
from that file read as data, and shares no code with it. For a tilt t = tan(theta/2),
0 < t < 1, let c = (1 - t^2)/(1 + t^2) and s = 2t/(1 + t^2): both positive and rational,
with c^2 + s^2 = 1. A *band* of width b (a positive integer), tilt t, length L and lift y
has its own frame, X across in [0, W] and Y along in [0, L], where W = b c + s,
h = b s + c and p = 1/c.

- *Rows.* R = floor((L - h)/p) + 1 rows, leaving the free length F = L - (R - 1) p - h,
  which lies in [0, p); the lift is 0 <= y <= F. Row j, 0 <= j < R, is b unit squares
  turned by theta: square i is {P_j + u (c, s) + v (-s, c) : i <= u <= i + 1,
  0 <= v <= 1}, with P_j = (s, y + j p).
- *Near-end layers.* At level i = 0, 1, ..., let a_i = max(0, s + (i + 1 - y) c/s). The
  level holds m_i = floor(W - a_i) axis-parallel unit squares
  [W - m_i + q, W - m_i + q + 1] x [i, i + 1], q = 0 .. m_i - 1, when m_i > 0.
- *Far-end layers.* The near-end layers of lift y' = F - y, turned by 180 degrees about
  (W/2, L/2): (X, Y) -> (W - X, L - Y).

The box is [0, S]^2. The grid is (K - bV)(K - bH) axis-parallel unit squares filling
[0, K - bV] x [0, K - bH]. The V band (width bV, tilt tV, length S, lift yV) is placed by
(X, Y) -> (K - bV + X, Y). The H band (width bH, tilt tH, length K - bV, lift yH) is
placed by the reflection (X, Y) -> (Y, K - bH + X), which turns each of its squares by
-theta, so its tilt is written -tH.

**The lemma** (`LEMMA`). Let 2 <= K, 1 <= bV, bH <= K - 1, 0 < tV, tH < 1, and let S
satisfy the fit inequalities K - bV + WV <= S and K - bH + WH <= S. Let each band have
h <= L and 0 <= y <= F, and let each end of each band hold, at each level i, any number
m_i of layer squares with 0 <= m_i <= W - a_i, placed as above (the construction takes
the floor, the most). Then the grid, both bands' rows and all their layer squares are
unit squares with pairwise disjoint interiors inside [0, S]^2. So s(n) <= S for every n
up to their number, the capacity (K - bV)(K - bH) + bV RV + bH RH + every layer's m_i.

*Proof.* In a band, take coordinates relative to its row 0: u and v are the components
of (X, Y) - P_0 along (c, s) and (-s, c), so v = c (Y - y) - s (X - s).

1. *Rows.* P_j - P_0 = (0, j p) has (u, v) = (j s/c, j), so square i of row j is
   {j s/c + i <= u <= j s/c + i + 1, j <= v <= j + 1}. Two squares of one row are
   separated by their u-intervals and two of different rows by their v-intervals. Row
   j's corners have X = s, s + b c, 0 and b c, so its X-extent is [0, W], and its
   Y-extent is [y + j p, y + j p + h]. Since y >= 0 and y + (R - 1) p + h = L - F + y
   <= L, every row lies in [0, W] x [0, L], and every row lies in the half-plane
   v >= 0.
2. *Near-end layers.* A level-i square is [X0, X0 + 1] x [i, i + 1] with
   W - m_i <= X0 <= W - 1. On it v grows with Y and falls with X, so its largest v is at
   the corner (X0, i + 1): c (i + 1 - y) - s (X0 - s) <= c (i + 1 - y) - s (W - m_i - s)
   <= 0, the last because W - m_i >= a_i >= s + (i + 1 - y) c/s and s > 0. So every
   layer square lies in v <= 0 and meets no row's interior. Two layer squares of
   different levels are separated by their Y-intervals, of one level by their
   X-intervals. Each lies in [0, W] x [0, L]: X0 >= W - m_i >= a_i >= 0, X0 + 1 <= W,
   i >= 0, and from v <= 0 and X <= W, Y <= y + (W - s) s/c = y + b s < y + h <= L.
3. *Far-end layers.* The point reflection r(X, Y) = (W - X, L - Y) maps the band of lift
   y' = F - y (also in [0, F], with the same R and F) onto the band of lift y: it sends
   row j's corner P'_j + b (c, s) + (-s, c) = (b c, y' + j p + h) to
   (s, L - h - y' - j p) = (s, y + (R - 1 - j) p) = P_{R - 1 - j}, and keeps edge
   directions, so it maps row j onto row R - 1 - j and the edge v' = 0 of the former's
   row 0 onto the edge v = R of row R - 1. The lift-y' band's near-end layers lie in
   v' <= 0 (step 2), so the far-end layers lie in v >= R, away from every row, and in
   [0, W] x [0, L], which r maps onto itself. As R >= 1, they meet no near-end layer's
   interior, which lies in v < 0.
4. *The box.* A translation and the reflection in y = x are isometries, so each placed
   band keeps its squares interior-disjoint. The V band lies in
   [K - bV, K - bV + WV] x [0, S], the H band in [0, K - bV] x [K - bH, K - bH + WH] and
   the grid in [0, K - bV] x [0, K - bH]: the V band is right of x = K - bV and the other
   two left of it, and the H band is above y = K - bH and the grid below it. The fit
   inequalities put all three inside [0, S]^2 (they give K - bV < S and K - bH < S).
5. *Count.* Deleting squares from a packing leaves a packing. QED

`decide` holds a row to the lemma in `Fraction`s and returns its capacity, each part's
count, each band's rows and layers, both fit slacks, each band's free length and the least
layer slack, or raises `FilledEndRefusedError` saying why not. It refuses any other kind; a
K above `MAX_K`; a side above K, which bounds nothing the K x K grid does not and keeps the
work a hostile row can ask for to about K levels a band end; a tilt outside (0, 1); a band
of no rows or of K or more across; a side that fails either fit inequality; a band shorter
than h; a lift outside [0, F]; a stated layer count outside [0, W - a_i]; and a count above
the capacity. Whether S < K and whether K is ceil(sqrt(n)) are reported, not required: they
say whether the bound beats the grid, not whether the packing is one. A checker of a lemma
is sound, not complete: it refuses some genuine packings the lemma does not state, and
must.

`mutants` are a row's negative controls (`CONTROLS`), each a change `decide` must refuse,
and `controls` decides them: the count one above the capacity; the side 10^-15 below the
binding fit inequality (the V fit, which every row of both deposits meets with equality);
each band's lift 10^-15 past its free length, so its last row passes the band's far end;
each of the four band ends with one layer one square over, at every level in turn and at
the level after its last; no tilt (tH = 0); a right angle (tV = 1); and an unknown kind. A
layer one over always breaks the bound, since the construction's m_i is the floor of
W - a_i. A control `decide` accepts is reported, ``refused`` False, so a check fails rather
than passing it over.

`write_out` builds the packing the lemma states as a certificate in the ``n S`` / ``x y t``
format with t = tan(theta/2): the grid column by column, then the V band (its rows, its
near-end layers, its far-end layers), then the H band reflected, with the surplus over n
dropped from the start of the grid. That is the order of the author's ``build``, so at the
five counts of the author-built sample (``receipts/filled-end-replay-sample.json``) the
certificate is the author's byte for byte, which `check` holds by its SHA-256 without
running his code.

**The packet.** ``karimi-records-2026-10-31`` keeps both deposits (`DEPOSITS`) from the
author's GitHub copy at ad8b094: V2.0's ``filled_records.csv`` beside its programs, and
V1.0's archive ``karimi_filled_end_v2.zip``, whose ``filled_records.csv`` is read from the
archive. Their bytes had the SHA-256s the author stated when the packet was written; from
then on Git keeps them and ``acquire_source --check`` holds them to the packet's manifest
(OR-16), so this module compares no digest.

**The ingest.** ``filled_records.csv`` is another party's file, read as untrusted data by
`parse_table`: the header exactly `COLUMNS`, each row exactly that many fields, each literal
matched whole with at most `MAX_DIGITS` digits in each part, the decimal side within one
unit of its last place of the exact side, K at most `MAX_K` and equal to ceil(sqrt(n)), the
author's ``previous_source`` one of `SOURCES`, and each count once. Every refusal is a
`CustodyError`. The author's comparison columns are counted in the receipt and decide
nothing.

**The receipts**, in the packet:

- ``receipts/filled-end-decisions-v2.json.gz`` and ``filled-end-decisions-v1.json.gz``
  (``decide-all``): every row of each deposit decided by the lemma, every control
  refused, and the SHA-256 and size of each written-out certificate, which the record
  does not keep (OR-18: they are derived, and `write_out` writes them again byte for
  byte). Over 1,000 lines each, they are stored as deterministic gzip and read through
  `devtools.retained_data`. V1.0's is decided and labelled apart: whether V1.0 counts as
  a report at all is the owner's question Q-847a (think-r94q), and neither receipt
  records a row of the coverage register.
- ``receipts/filled-end-checker-replay-sample.json`` (``replay-sample``): the
  cross-check. At five V2.0 counts nearest the lemma's edges (`SAMPLE`), the certificate
  `write_out` writes is decided on both exact routes of `devtools.couzo_678_replay` with
  their six controls, as `two_strip_checker.replay_row` decides a two-strip row, so the
  lemma's verdict and the routes' agree where both are run. A row the lemma refuses would
  be decided this way instead (``replay-sample --n``), and `check` accepts a refused row
  only where the replay sample passes it on both routes; no row of either deposit needs it.

``check`` reads the receipts back: every decision and control derived again, the author's
columns counted again, the certificates at each deposit's quick sample written again
(every count's with ``--digests``), the author-built sample's five certificates written
again to its digests, and with ``--replay`` each count of the replay sample decided again
on both routes.

From ``packing/``, with the project interpreter::

    python -m devtools.filled_end_checker decide-all [--version 2] [--version 1]
    python -m devtools.filled_end_checker replay-sample [--n N ...] [--workers 2]
    python -m devtools.filled_end_checker check [--digests] [--replay]

A finite packing certifies an upper bound and nothing more. Whether a row is below every
earlier report at its count is the walk's to decide (think-llit), not this module's.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import platform
import re
import time
import zipfile
import zlib
from collections.abc import Iterator, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from fractions import Fraction
from functools import lru_cache, partial
from itertools import islice
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import evand_exact_certificates as legacy
from devtools import retained_data
from devtools.retained_data import read_retained_bytes
from sqpack.retained_json import dumps as retained_dumps

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent

KIND = "filled-end"
DECIDED = "decided"
REFUSED = "refused"
#: The lemma a decision rests on, as a receipt states it.
LEMMA = (
    "For t = tan(theta/2) in (0, 1), c = (1 - t^2)/(1 + t^2), s = 2t/(1 + t^2), a band of "
    "width b, length L >= h and lift 0 <= y <= F, with W = b c + s, h = b s + c, p = 1/c, "
    "R = floor((L - h)/p) + 1 and F = L - (R - 1) p - h, has rows j < R of b unit squares "
    "turned by theta at P_j = (s, y + j p), which lie in [0, W] x [0, L] and in v >= 0 "
    "for v = c (Y - y) - s (X - s); a near-end layer at level i of m_i <= W - a_i axis "
    "squares [W - m_i + q, W - m_i + q + 1] x [i, i + 1], a_i = max(0, s + (i + 1 - y) "
    "c/s), lies in v <= 0 and in [0, W] x [0, L]; the far-end layers, the near-end "
    "layers of lift F - y turned by 180 degrees about (W/2, L/2), lie in v >= R; the "
    "grid [0, K - bV] x [0, K - bH], the V band at x = K - bV of length S and the H band "
    "reflected in y = x at y = K - bH of length K - bV have disjoint interiors inside "
    "[0, S]^2 when K - bV + WV <= S and K - bH + WH <= S; deleting squares leaves a "
    "packing"
)
#: The controls every row carries (`mutants`), in order.
CONTROLS = (
    "count above the capacity",
    "side below the binding fit",
    "V lift past its free length",
    "H lift past its free length",
    "a V near-end layer one over",
    "a V far-end layer one over",
    "an H near-end layer one over",
    "an H far-end layer one over",
    "no tilt",
    "a right angle",
    "unknown kind",
)
#: The four band ends whose layers a row may state, in `FilledEnd.layers` order.
ENDS = ("V near", "V far", "H near", "H far")
#: How far below the binding fit inequality the side control puts the side, and how far
#: past a band's free length the lift controls put its lift.
FIT_MARGIN = Fraction(1, 10**15)
#: The largest K the checker decides. The deposits reach K = 100 (n <= 9946); ten times
#: that bounds the work a hostile row can ask for, with the side at most K.
MAX_K = 1000

#: The packet, as the receipts name it from the repository root, and on disk.
PACKET_PATH = "packing/resources/web/karimi-records-2026-10-31"
PACKET = REPO / PACKET_PATH
ISSUE = "https://github.com/jlevy/squares/issues/847"
ISSUE_836 = "https://github.com/jlevy/squares/issues/836"
CHECKER = "packing/devtools/filled_end_checker.py"
ROUTES = "packing/devtools/couzo_678_replay.py (decide and decide_controls)"
DECISIONS_FORMAT = "filled-end-decisions-v1"
REPLAY_FORMAT = "filled-end-checker-replay-sample-v1"
#: The replay sample: five V2.0 counts nearest the lemma's edges, each the smallest count
#: attaining its extreme over V2.0's rows (`edge_counts`).
SAMPLE = (1188, 5265, 7439, 8524, 9517)
#: What each count of `SAMPLE` is the extreme of, in `edge_counts` order.
EDGES = (
    "a lift of zero",
    "the least layer slack",
    "the least H lift room",
    "the least V lift room",
    "the least H fit slack",
)
#: The author-built sample of `devtools.filled_end_sample`, whose certificates
#: `write_out` must write byte for byte.
AUTHOR_SAMPLE = "receipts/filled-end-replay-sample.json"


@dataclass(frozen=True, slots=True)
class Deposit:
    """One version of the filled-end deposit the packet keeps: its label and record, the
    comment or issue that reported it, where its ``filled_records.csv`` is (``table``, a
    path in the packet, or a member of the archive at ``archived``), how many rows it
    holds, its decisions receipt, and the counts whose written-out certificates the quick
    check writes again (``sample``). ``replay`` names its replay sample, when it has one,
    and ``note`` says how its receipt is to be read."""

    label: str
    record: int
    reported: str
    rows: int
    receipt: str
    sample: tuple[int, ...]
    table: str = ""
    archived: str = ""
    replay: str = ""
    note: str = ""

    @property
    def doi(self) -> str:
        return f"10.5281/zenodo.{self.record}"

    @property
    def records_name(self) -> str:
        """The rows' file as the receipts name it, from the repository root."""
        if self.archived:
            return f"{PACKET_PATH}/{self.archived}:filled_records.csv"
        return f"{PACKET_PATH}/{self.table}"

    @property
    def decisions(self) -> Path:
        return PACKET / "receipts" / self.receipt

    @property
    def replay_receipt(self) -> Path:
        return PACKET / "receipts" / self.replay


#: V2.0, reported by #847 (2026-10-30T21:56:32Z): 5,134 rows at 1182 to 9946.
V2 = Deposit(
    label="V2.0",
    record=23819397,
    reported=ISSUE,
    rows=5134,
    receipt="filled-end-decisions-v2.json",
    sample=(1182, 9946),
    table="source/filled_records.csv",
    replay="filled-end-checker-replay-sample.json",
    note=(
        "every row decided by the lemma; whether a row is below every earlier report at "
        "its count is the walk's (think-llit), and this receipt records no row"
    ),
)
#: V1.0, reported on #836 (2026-10-27T04:16:22Z): 4,571 rows at 1184 to 9946, kept as
#: its archive. Decided apart and labelled: Q-847a is the owner's.
V1 = Deposit(
    label="V1.0",
    record=23681705,
    reported=f"{ISSUE_836}#issuecomment-6433611255",
    rows=4571,
    receipt="filled-end-decisions-v1.json",
    sample=(1184, 9946),
    archived="source/karimi_filled_end_v2.zip",
    note=(
        "decided apart from V2.0 and labelled: #847 asks that V1.0 be ignored, and whether "
        "it counts as a report in report order is the owner's question Q-847a "
        "(think-r94q); this receipt says only which of its packings the lemma decides, "
        "and records no row"
    ),
)
DEPOSITS = (V2, V1)
#: The deposits by the label the command line takes.
VERSIONS = {"2": V2, "1": V1}

#: The columns of both deposits' ``filled_records.csv``, exactly and in order.
COLUMNS = (
    "n",
    "K",
    "side_exact",
    "side",
    "previous_best_side",
    "previous_source",
    "bV",
    "tV",
    "yV",
    "bH",
    "tH",
    "yH",
)
#: The author's ``previous_source`` labels, read, counted and deciding nothing.
SOURCES = frozenset({"Karimi v5", "Couzo 712c6a6", "Mishapolk ab8e833"})
#: The most bytes the archive's ``filled_records.csv`` may decompress to; V1.0's is
#: 598,761.
MAX_RECORDS_BYTES = 8 * 1024 * 1024
#: The most digits in any one part of a literal. The deposits' longest run is 22 digits,
#: in a lift.
MAX_DIGITS = 30

_RATIONAL = re.compile(rf"[0-9]{{1,{MAX_DIGITS}}}(/[1-9][0-9]{{0,{MAX_DIGITS - 1}}})?")
_INTEGER = re.compile(rf"[1-9][0-9]{{0,{MAX_DIGITS - 1}}}")
_DECIMAL = re.compile(rf"[0-9]{{1,{MAX_DIGITS}}}\.([0-9]{{1,{MAX_DIGITS}}})")


class FilledEndRefusedError(ValueError):
    """A row the checker does not decide, with the reason."""


class CustodyError(ValueError):
    """The packet's files, or a row read from them, are not what the format states."""


def _refuse(condition: object, message: str) -> None:
    if not condition:
        raise FilledEndRefusedError(message)


@dataclass(frozen=True, slots=True)
class FilledEnd:
    """One filled-end packing as a row states it: the count, the side, K, and each band's
    width b, tilt t = tan(theta/2) and lift (``v`` the band on the right wall, ``h`` the
    one reflected onto the top). ``layers`` states each band end's layer counts by level,
    in `ENDS` order; None, as every row of a deposit has, takes the construction's own,
    the most the lemma allows."""

    n: int
    side: Fraction
    k: int
    width_v: int
    tilt_v: Fraction
    lift_v: Fraction
    width_h: int
    tilt_h: Fraction
    lift_h: Fraction
    layers: tuple[tuple[int, ...], ...] | None = None
    kind: str = KIND


@dataclass(frozen=True, slots=True)
class Band:
    """One band decided in its own frame: its width, tilt, length and lift, the basis,
    W, h and the pitch p = 1/c, its rows R and free length F, and each end's layer
    counts by level (``near`` at lift y, ``far`` at lift F - y)."""

    width: int
    tilt: Fraction
    length: Fraction
    lift: Fraction
    cos: Fraction
    sin: Fraction
    across: Fraction
    deep: Fraction
    pitch: Fraction
    rows: int
    free: Fraction
    near: tuple[int, ...]
    far: tuple[int, ...]

    @property
    def count(self) -> int:
        return self.width * self.rows + sum(self.near) + sum(self.far)


#: How many band frames and layer computations each cache keeps. A row's controls decide
#: it about twenty times with the same few frames; the caches only save that arithmetic.
CACHE = 4096


@lru_cache(maxsize=CACHE)
def basis(tilt: Fraction) -> tuple[Fraction, Fraction]:
    """``(cos theta, sin theta)`` for ``tilt = tan(theta/2)``, exactly."""
    square = tilt * tilt
    return (1 - square) / (1 + square), 2 * tilt / (1 + square)


def across(width: int, tilt: Fraction) -> Fraction:
    """A band's width across, W = b c + s."""
    cos, sin = basis(tilt)
    return width * cos + sin


@lru_cache(maxsize=CACHE)
def edge(cos: Fraction, sin: Fraction, lift: Fraction, level: int) -> Fraction:
    """a_i: the least X at which a level-i layer square stays below row 0's edge."""
    return max(Fraction(0), sin + (level + 1 - lift) * cos / sin)


@lru_cache(maxsize=CACHE)
def floor_layers(width: int, cos: Fraction, sin: Fraction, lift: Fraction) -> tuple[int, ...]:
    """The construction's layer counts at one end, m_i = floor(W - a_i) while positive.
    a_i grows with i, so the counts fall and the positive ones come first; a level at or
    past y + b s holds none, since there a_i >= W, so no more levels are looked at."""
    wide = width * cos + sin
    found = []
    for level in range(math.floor(lift + width * sin) + 1):
        held = math.floor(wide - edge(cos, sin, lift, level))
        if held <= 0:
            break
        found.append(held)
    return tuple(found)


def _stated(
    name: str,
    counts: Sequence[int],
    *,
    width: int,
    cos: Fraction,
    sin: Fraction,
    lift: Fraction,
) -> tuple[int, ...]:
    """A band end's stated layer counts, each held to 0 <= m_i <= W - a_i."""
    wide = width * cos + sin
    for level, held in enumerate(counts):
        _refuse(held >= 0, f"the {name}-end layer {level} holds {held} squares")
        if held:
            over = edge(cos, sin, lift, level) - (wide - held)
            _refuse(
                over <= 0,
                f"the {name}-end layer {level}, {held} squares, crosses the band's end row "
                f"by {float(over):.3e}: W - m_{level} < a_{level}",
            )
    return tuple(counts)


@lru_cache(maxsize=CACHE)
def frame(
    width: int, tilt: Fraction, length: Fraction
) -> tuple[Fraction, Fraction, Fraction, Fraction, Fraction, int, Fraction]:
    """A band's c, s, W, h and p, and the rows R and free length F its length gives,
    exactly; meaningful only when h <= L, which `band` requires."""
    cos, sin = basis(tilt)
    wide, deep, pitch = width * cos + sin, width * sin + cos, 1 / cos
    rows = math.floor((length - deep) * cos) + 1
    return cos, sin, wide, deep, pitch, rows, length - (rows - 1) * pitch - deep


def band(
    name: str,
    width: int,
    tilt: Fraction,
    length: Fraction,
    lift: Fraction,
    *,
    stated: tuple[Sequence[int], Sequence[int]] | None = None,
) -> Band:
    """A band decided in its own frame (`LEMMA`): at least h long, its lift in [0, F],
    and each end's layers the floor or, when ``stated``, held to W - a_i."""
    cos, sin, wide, deep, pitch, rows, free = frame(width, tilt, length)
    _refuse(
        deep <= length,
        f"the {name} band, {float(deep):.12g} deep, is longer than its length "
        f"{float(length):.12g}",
    )
    _refuse(lift >= 0, f"the {name} lift {lift} is negative")
    _refuse(
        lift <= free,
        f"the {name} lift passes its free length by {float(lift - free):.3e}: the last "
        "row passes the band's far end",
    )
    after = free - lift
    if stated is None:
        near = floor_layers(width, cos, sin, lift)
        far = floor_layers(width, cos, sin, after)
    else:
        near = _stated(f"{name} near", stated[0], width=width, cos=cos, sin=sin, lift=lift)
        far = _stated(f"{name} far", stated[1], width=width, cos=cos, sin=sin, lift=after)
    return Band(width, tilt, length, lift, cos, sin, wide, deep, pitch, rows, free, near, far)


def layer_slack(item: Band) -> Fraction | None:
    """The least W - m_i - a_i over a band's layers, how near a layer is to holding one
    more square; None for a band with no layer."""
    found = [
        item.across - held - edge(item.cos, item.sin, lift, level)
        for counts, lift in ((item.near, item.lift), (item.far, item.free - item.lift))
        for level, held in enumerate(counts)
        if held
    ]
    return min(found) if found else None


def binding_side(row: FilledEnd) -> Fraction:
    """The least side at which both fit inequalities hold, for the row's K and bands."""
    return max(
        row.k - row.width_v + across(row.width_v, row.tilt_v),
        row.k - row.width_h + across(row.width_h, row.tilt_h),
    )


def bands(row: FilledEnd) -> tuple[Band, Band]:
    """The row's two bands decided (`band`), V then H, once its ranges and fits hold."""
    stated = row.layers
    v = band(
        "V",
        row.width_v,
        row.tilt_v,
        row.side,
        row.lift_v,
        stated=None if stated is None else (stated[0], stated[1]),
    )
    h = band(
        "H",
        row.width_h,
        row.tilt_h,
        Fraction(row.k - row.width_v),
        row.lift_h,
        stated=None if stated is None else (stated[2], stated[3]),
    )
    return v, h


def decide(row: FilledEnd) -> dict[str, Any]:
    """The row decided exactly by the lemma; `FilledEndRefusedError` says why not."""
    _refuse(row.kind == KIND, f"kind {row.kind!r}: not a filled-end packing")
    _refuse(row.n >= 1, f"n = {row.n}: no squares to pack")
    _refuse(row.side > 0, f"the side {row.side} is not positive")
    _refuse(1 < row.k <= MAX_K, f"K = {row.k}: the checker decides 2 <= K <= {MAX_K}")
    _refuse(row.side <= row.k, f"the side {float(row.side):.12g} is above K = {row.k}")
    for name, tilt in (("tH", row.tilt_h), ("tV", row.tilt_v)):
        _refuse(0 < tilt < 1, f"{name} = {tilt}: a band's tan(theta/2) must lie in (0, 1)")
    for name, width in (("bV", row.width_v), ("bH", row.width_h)):
        _refuse(0 < width < row.k, f"{name} = {width}: a band is 1 to K - 1 = {row.k - 1} wide")
    _refuse(
        row.layers is None or len(row.layers) == len(ENDS),
        "a row states the layers of all four band ends or of none",
    )
    wide_v = across(row.width_v, row.tilt_v)
    wide_h = across(row.width_h, row.tilt_h)
    slack_v = row.side - (row.k - row.width_v) - wide_v
    slack_h = row.side - (row.k - row.width_h) - wide_h
    _refuse(
        slack_v >= 0,
        f"the V band, {float(wide_v):.12g} wide from x = K - bV, passes the right wall by "
        f"{float(-slack_v):.3e}: K - bV + WV > S",
    )
    _refuse(
        slack_h >= 0,
        f"the H band, {float(wide_h):.12g} high from y = K - bH, passes the top wall by "
        f"{float(-slack_h):.3e}: K - bH + WH > S",
    )
    v, h = bands(row)
    grid = (row.k - row.width_v) * (row.k - row.width_h)
    held = grid + v.count + h.count
    _refuse(row.n <= held, f"n = {row.n} is above the capacity {held}")
    slacks = [found for found in (layer_slack(v), layer_slack(h)) if found is not None]
    return {
        "n": row.n,
        "kind": row.kind,
        "side": legacy.literal(row.side),
        "k": row.k,
        "capacity": held,
        "grid": grid,
        "v_band": v.count,
        "h_band": h.count,
        "v_rows": v.rows,
        "h_rows": h.rows,
        "v_layers": [list(v.near), list(v.far)],
        "h_layers": [list(h.near), list(h.far)],
        "surplus": held - row.n,
        "v_slack": legacy.literal(slack_v),
        "h_slack": legacy.literal(slack_h),
        "v_free": legacy.literal(v.free),
        "h_free": legacy.literal(h.free),
        "layer_slack": legacy.literal(min(slacks)) if slacks else None,
        "side_below_k": row.side < row.k,
        "k_is_ceil_sqrt_n": row.k == math.isqrt(row.n - 1) + 1,
        "verdict": DECIDED,
    }


def capacity(row: FilledEnd) -> int:
    """The row's capacity, by `decide` at a count of one."""
    return int(decide(replace(row, n=1))["capacity"])


def own_layers(row: FilledEnd) -> tuple[tuple[int, ...], ...]:
    """The layer counts the construction takes at the row's four band ends."""
    v, h = bands(row)
    return (v.near, v.far, h.near, h.far)


def _one_over(row: FilledEnd, end: int, layers: tuple[tuple[int, ...], ...]) -> list[FilledEnd]:
    """One band end (``layers`` the row's own) with each of its layers one square over in
    turn, and the level after its last given one square: one mutant per level."""
    counts = layers[end]
    changed = []
    for level in range(len(counts) + 1):
        grown = [*counts, 0]
        grown[level] += 1
        stated = tuple(tuple(grown) if index == end else layers[index] for index in range(4))
        changed.append(replace(row, layers=stated))
    return changed


def mutants(row: FilledEnd) -> list[tuple[str, list[FilledEnd]]]:
    """A row's negative controls, each one change or a few (`CONTROLS`), every one of
    which `decide` must refuse."""
    held = capacity(row)
    v, h = bands(row)
    layers = (v.near, v.far, h.near, h.far)
    changed = [
        [replace(row, n=held + 1)],
        [replace(row, side=binding_side(row) - FIT_MARGIN)],
        [replace(row, lift_v=v.free + FIT_MARGIN)],
        [replace(row, lift_h=h.free + FIT_MARGIN)],
        *(_one_over(row, end, layers) for end in range(len(ENDS))),
        [replace(row, tilt_h=Fraction(0))],
        [replace(row, tilt_v=Fraction(1))],
        [replace(row, kind="two-strip")],
    ]
    return list(zip(CONTROLS, changed, strict=True))


def controls(row: FilledEnd) -> list[dict[str, Any]]:
    """Each control (`mutants`): refused when `decide` refuses every one of its changes,
    with the first change's reason and how many changes it made; ``refused`` False marks
    one with a change `decide` accepted, which a check refuses."""
    found = []
    for name, changes in mutants(row):
        reasons = []
        for changed in changes:
            try:
                decide(changed)
            except FilledEndRefusedError as error:
                reasons.append(str(error))
            else:
                break
        refused = len(reasons) == len(changes)
        found.append(
            {
                "control": name,
                "refused": refused,
                "reason": reasons[0] if refused else "",
                "changes": len(changes),
            }
        )
    return found


# --------------------------------------------------------------------------- the write-out


def _band_poses(item: Band) -> Iterator[tuple[Fraction, Fraction, Fraction]]:
    """A band's squares in its own frame, ``(X, Y, t)`` centres: its rows, then its
    near-end layers, then its far-end layers turned by 180 degrees."""
    half = Fraction(1, 2)
    cos, sin = item.cos, item.sin
    for row in range(item.rows):
        for square in range(item.width):
            yield (
                sin + (square + half) * cos - half * sin,
                item.lift + row * item.pitch + (square + half) * sin + half * cos,
                item.tilt,
            )
    for level, held in enumerate(item.near):
        for q in range(held):
            yield item.across - held + q + half, level + half, Fraction(0)
    for level, held in enumerate(item.far):
        for q in range(held):
            yield held - q - half, item.length - level - half, Fraction(0)


def poses(row: FilledEnd) -> Iterator[legacy.Pose]:
    """Every square the construction places, one at a time: the grid column by column,
    the V band placed at x = K - bV, then the H band reflected in y = x onto y = K - bH."""
    half = Fraction(1, 2)
    for i in range(row.k - row.width_v):
        for j in range(row.k - row.width_h):
            yield legacy.Pose(half + i, half + j, Fraction(0))
    v, h = bands(row)
    for x, y, tilt in _band_poses(v):
        yield legacy.Pose(row.k - row.width_v + x, y, tilt)
    for x, y, tilt in _band_poses(h):
        yield legacy.Pose(y, row.k - row.width_h + x, -tilt)


def write_out(row: FilledEnd) -> legacy.Certificate:
    """The packing the lemma states for a row it decides: its last n squares as `poses`
    places them, so the surplus is dropped from the start of the grid."""
    surplus = int(decide(row)["surplus"])
    return legacy.Certificate(row.n, row.side, tuple(islice(poses(row), surplus, None)))


def construction(row: FilledEnd) -> legacy.Certificate:
    """The construction's last n squares written out whether or not the lemma decides the
    row, for the routes to decide; a construction of fewer squares is refused."""
    placed = tuple(poses(row))
    _refuse(len(placed) >= row.n, f"the construction places {len(placed)} squares")
    return legacy.Certificate(row.n, row.side, placed[len(placed) - row.n :])


def certificate_text(row: FilledEnd) -> str:
    """A decided row's written-out certificate, ``n S`` then ``x y t`` rows."""
    return legacy.serialize(write_out(row))


# --------------------------------------------------------------------------- the ingest


def archived_records(deposit: Deposit) -> str:
    """The text of ``filled_records.csv`` inside a deposit kept as its archive, read from
    Git as untrusted data: the archive must open and hold exactly one member of that name,
    at most `MAX_RECORDS_BYTES`, readable without a password by a method `zipfile` knows,
    and UTF-8. Any refusal is a `CustodyError`."""
    data = read_retained_bytes(PACKET / deposit.archived)
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            found = [
                item for item in archive.infolist() if item.filename == "filled_records.csv"
            ]
            if len(found) != 1:
                raise CustodyError(f"{deposit.archived} holds {len(found)} filled_records.csv")
            if found[0].file_size > MAX_RECORDS_BYTES:
                raise CustodyError(f"{deposit.archived}'s filled_records.csv is too large")
            with archive.open(found[0]) as member:
                text = member.read(MAX_RECORDS_BYTES + 1)
    except (
        zipfile.BadZipFile,
        zipfile.LargeZipFile,
        OSError,
        EOFError,
        RuntimeError,
        NotImplementedError,
        zlib.error,
    ) as error:
        raise CustodyError(f"{deposit.archived}: {error}") from error
    if len(text) > MAX_RECORDS_BYTES:
        raise CustodyError(f"{deposit.archived}'s filled_records.csv is too large")
    try:
        return text.decode("utf-8")
    except UnicodeDecodeError as error:
        raise CustodyError(f"filled_records.csv is not UTF-8: {error}") from error


def _records_text(deposit: Deposit) -> str:
    if deposit.archived:
        return archived_records(deposit)
    data = read_retained_bytes(PACKET / deposit.table, limit=MAX_RECORDS_BYTES)
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise CustodyError(f"filled_records.csv is not UTF-8: {error}") from error


def _literal(text: str, pattern: re.Pattern[str], where: str) -> str:
    if pattern.fullmatch(text) is None:
        raise CustodyError(f"{where}: {text[:60]!r} is not the literal the format states")
    return text


def row_from_record(item: Mapping[str, object]) -> FilledEnd:
    """A row of ``filled_records.csv`` as `COLUMNS` names its fields, each a string
    matched whole before it is read: ``n``, ``K``, ``bV`` and ``bH`` integers,
    ``side_exact``, ``tV``, ``yV``, ``tH`` and ``yH`` rationals, ``side`` and the
    author's ``previous_best_side`` decimals, and ``previous_source`` one of `SOURCES`.
    The decimal side must be the exact side to within one unit of its last place, K at
    most `MAX_K` and ceil(sqrt(n)). Anything else is a `CustodyError`."""
    shown = repr(item.get("n"))[:40] if isinstance(item, Mapping) else "?"
    where = f"filled_records.csv n={shown}"
    if not isinstance(item, Mapping) or sorted(map(str, item)) != sorted(COLUMNS):
        raise CustodyError(f"{where}: the fields are not the columns {list(COLUMNS)}")
    if not all(isinstance(value, str) for value in item.values()):
        raise CustodyError(f"{where}: a field is missing or not text")
    text = {str(key): str(value) for key, value in item.items()}

    def whole(name: str) -> int:
        return int(_literal(text[name], _INTEGER, where))

    def rational(name: str) -> Fraction:
        return Fraction(_literal(text[name], _RATIONAL, where))

    side = rational("side_exact")
    shown_side = _literal(text["side"], _DECIMAL, where)
    places = len(shown_side.split(".")[1])
    if abs(Fraction(shown_side) - side) >= Fraction(1, 10**places):
        raise CustodyError(f"{where}: the decimal side is not the exact side")
    _literal(text["previous_best_side"], _DECIMAL, where)
    if text["previous_source"] not in SOURCES:
        raise CustodyError(
            f"{where}: previous_source {text['previous_source'][:40]!r} is not one of "
            f"{sorted(SOURCES)}"
        )
    n, k = whole("n"), whole("K")
    if k > MAX_K:
        raise CustodyError(f"{where}: K = {k} is above the checker's bound {MAX_K}")
    if k != math.isqrt(n - 1) + 1:
        raise CustodyError(f"{where}: K = {k} is not ceil(sqrt(n))")
    return FilledEnd(
        n=n,
        side=side,
        k=k,
        width_v=whole("bV"),
        tilt_v=rational("tV"),
        lift_v=rational("yV"),
        width_h=whole("bH"),
        tilt_h=rational("tH"),
        lift_h=rational("yH"),
    )


def parse_table(text: str) -> list[tuple[FilledEnd, str]]:
    """A deposit's rows from its ``filled_records.csv`` text, read as untrusted data, each
    with the author's ``previous_source``: the header exactly `COLUMNS`, each row exactly
    that many fields, each row by `row_from_record`, and each count once. Every refusal
    is a `CustodyError`, including the csv module's own."""
    try:
        lines = list(csv.reader(io.StringIO(text, newline=""), strict=True))
    except csv.Error as error:
        raise CustodyError(f"filled_records.csv: {error}") from error
    if not lines or tuple(lines[0]) != COLUMNS:
        shown = repr(lines[0] if lines else [])[:200]
        raise CustodyError(f"filled_records.csv: the header is {shown}, not {list(COLUMNS)}")
    rows = []
    for number, fields in enumerate(lines[1:], start=1):
        if len(fields) != len(COLUMNS):
            raise CustodyError(
                f"filled_records.csv row {number}: {len(fields)} fields, not {len(COLUMNS)}"
            )
        named: dict[str, str] = dict(zip(COLUMNS, fields, strict=True))
        rows.append((row_from_record(named), named["previous_source"]))
    counts = [row.n for row, _ in rows]
    if len(set(counts)) != len(counts):
        raise CustodyError("filled_records.csv: a count appears in more than one row")
    return rows


def table(deposit: Deposit = V2) -> list[tuple[FilledEnd, str]]:
    """A deposit's rows with their ``previous_source``, at the deposit's row count."""
    rows = parse_table(_records_text(deposit))
    if len(rows) != deposit.rows:
        raise CustodyError(f"filled_records.csv holds {len(rows)} rows, not {deposit.rows}")
    return rows


def records(deposit: Deposit = V2) -> list[FilledEnd]:
    """A deposit's rows, from its retained ``filled_records.csv``."""
    return [row for row, _ in table(deposit)]


def sources(rows: Sequence[tuple[FilledEnd, str]]) -> dict[str, int]:
    """How many rows name each ``previous_source``."""
    counted: dict[str, int] = {}
    for _, source in rows:
        counted[source] = counted.get(source, 0) + 1
    return dict(sorted(counted.items()))


# --------------------------------------------------------------------------- the receipts


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_receipt(path: Path) -> Any:
    """A receipt, plain or stored as ``X.gz`` (`devtools.retained_data`)."""
    return json.loads(read_retained_bytes(path).decode("utf-8"))


def _write(path: Path, value: Any) -> Path:
    """Write a receipt; one of more than `retained_data.LINE_THRESHOLD` lines is stored as
    deterministic gzip, ``X.gz``, by `retained_data.compress`. Returns the stored path."""
    text = retained_dumps(value, sort_keys=True)
    packed = retained_data.compressed_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    packed.unlink(missing_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_text(text, encoding="utf-8")
    if text.count("\n") > retained_data.LINE_THRESHOLD:
        return retained_data.compress(path)
    return path


def _environment() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "machine": platform.machine(),
    }


def _now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def decision_row(
    row: FilledEnd, *, digest: bool = True
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """One row of the decisions receipt, with its controls decided once: the decision,
    how many controls were refused and, with ``digest``, the written-out certificate's
    SHA-256 and size; and the controls themselves, for the summary. A row the lemma
    refuses is kept with its reason and no controls."""
    try:
        found = decide(row)
    except FilledEndRefusedError as error:
        return {"n": row.n, "verdict": REFUSED, "reason": str(error)}, []
    checked = controls(row)
    found["controls_refused"] = sum(1 for item in checked if item["refused"])
    if digest:
        text = certificate_text(row).encode("utf-8")
        found["certificate_sha256"] = _sha256(text)
        found["certificate_bytes"] = len(text)
    return found, checked


def _least(found: Sequence[Mapping[str, Any]], key: str) -> str | None:
    values = [Fraction(item[key]) for item in found if item.get(key) is not None]
    return f"{min(values):.6e}" if values else None


def decisions_summary(
    found: Sequence[Mapping[str, Any]], checked: Sequence[Sequence[Mapping[str, Any]]]
) -> dict[str, Any]:
    """Counts over the decisions, and each control's refusals over the decided rows'
    controls (``checked``, as `decision_row` decided them) with its reason at the first."""
    decided = [item for item in found if item["verdict"] == DECIDED]
    tallies: dict[str, int] = dict.fromkeys(CONTROLS, 0)
    changes: dict[str, int] = dict.fromkeys(CONTROLS, 0)
    for row in checked:
        for item in row:
            tallies[item["control"]] += item["refused"]
            changes[item["control"]] += item["changes"]
    first = next((row for row in checked if row), [])
    return {
        "rows": len(found),
        "decided": len(decided),
        "refused": [item["n"] for item in found if item["verdict"] != DECIDED],
        "squares": sum(item["n"] for item in decided),
        "surplus_zero": sum(1 for item in decided if item["surplus"] == 0),
        "surplus_most": max((item["surplus"] for item in decided), default=0),
        "side_below_k": sum(1 for item in decided if item["side_below_k"]),
        "k_is_ceil_sqrt_n": sum(1 for item in decided if item["k_is_ceil_sqrt_n"]),
        "least_v_slack": _least(decided, "v_slack"),
        "least_h_slack": _least(decided, "h_slack"),
        "least_layer_slack": _least(decided, "layer_slack"),
        "most_layers": max(
            (
                len(counts)
                for item in decided
                for key in ("v_layers", "h_layers")
                for counts in item[key]
            ),
            default=0,
        ),
        "controls": {
            item["control"]: {
                "refused": tallies[item["control"]],
                "changes": changes[item["control"]],
                "first_reason": item["reason"],
            }
            for item in first
        },
    }


def decide_all(deposit: Deposit = V2) -> dict[str, Any]:
    """Decide every row of a deposit with its controls and write its decisions receipt."""
    parsed = table(deposit)
    started, cpu = _now(), time.process_time()
    decided = [decision_row(row) for row, _ in parsed]
    found = [item for item, _ in decided]
    receipt = {
        "format": DECISIONS_FORMAT,
        "issue": ISSUE,
        "reported": deposit.reported,
        "version": deposit.label,
        "doi": deposit.doi,
        "packet": PACKET_PATH,
        "records": deposit.records_name,
        "checker": CHECKER,
        "lemma": LEMMA,
        "controls": list(CONTROLS),
        "note": deposit.note,
        "certificates": (
            "written out by write_out and serialized in the n S / x y t format; not "
            "retained, each pinned here by its SHA-256 and size"
        ),
        "author_columns": {
            "previous_source": sources(parsed),
            "note": (
                "the author's own comparison columns, read and counted; the checker "
                "decides nothing by them, and whether a row is below every earlier report "
                "is the walk's"
            ),
        },
        "environment": _environment(),
        "started_utc": started,
        "cpu_seconds": round(time.process_time() - cpu, 1),
        "rows": found,
        "summary": decisions_summary(found, [checked for _, checked in decided]),
    }
    _write(deposit.decisions, receipt)
    return receipt


def edge_counts(rows: Sequence[FilledEnd]) -> tuple[int, ...]:
    """The replay sample's rule (`EDGES`): the smallest count with a lift of zero, then
    the smallest count attaining each least slack, in `EDGES` order."""
    found = {row.n: decide(row) for row in rows}
    by_n = {row.n: row for row in rows}

    def least(value: Any) -> int:
        return min(found, key=lambda n: (value(n), n))

    zero = min(n for n, row in by_n.items() if row.lift_v == 0 or row.lift_h == 0)
    return (
        zero,
        least(lambda n: Fraction(found[n]["layer_slack"])),
        least(lambda n: Fraction(found[n]["h_free"]) - by_n[n].lift_h),
        least(lambda n: Fraction(found[n]["v_free"]) - by_n[n].lift_v),
        least(lambda n: Fraction(found[n]["h_slack"])),
    )


def replay_row(n: int, deposit: Deposit = V2) -> dict[str, Any]:
    """One count of the replay sample: the row decided by the lemma (or its refusal), its
    certificate written out and decided on both routes of `devtools.couzo_678_replay`,
    and the six controls."""
    # The replay module costs about two seconds to import; the checker needs none of it.
    from devtools import couzo_678_replay as base  # noqa: PLC0415

    row = next(row for row in records(deposit) if row.n == n)
    try:
        lemma: dict[str, Any] = {"verdict": DECIDED, "capacity": decide(row)["capacity"]}
    except FilledEndRefusedError as error:
        lemma = {"verdict": REFUSED, "reason": str(error)}
    began = time.process_time()
    cert = construction(row)
    text = legacy.serialize(cert).encode("utf-8")
    started = time.process_time()
    result = base.decide(base.geometry(cert))
    positive = time.process_time()
    checked = base.decide_controls(cert)
    ended = time.process_time()
    return {
        "n": n,
        "lemma": lemma,
        "certificate_sha256": _sha256(text),
        "certificate_bytes": len(text),
        "exact_side": legacy.literal(cert.side),
        "verified": result["passed"],
        "decision": result,
        "controls": checked,
        "cpu_seconds": {
            "write_out": round(started - began, 2),
            "positive": round(positive - started, 2),
            "controls": round(ended - positive, 2),
        },
    }


def replay_sample(counts: Sequence[int], workers: int, deposit: Deposit = V2) -> dict[str, Any]:
    """Replay the sample's certificates on both routes and write the replay receipt."""
    from devtools import couzo_678_replay as base  # noqa: PLC0415

    if not deposit.replay:
        raise ValueError(f"{deposit.label} has no replay sample")
    started, wall = _now(), time.monotonic()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(partial(replay_row, deposit=deposit), counts))
    receipt = {
        "format": REPLAY_FORMAT,
        "issue": ISSUE,
        "doi": deposit.doi,
        "packet": PACKET_PATH,
        "records": deposit.records_name,
        "checker": CHECKER,
        "routes": ROUTES,
        "filter_lemma": base.FILTER_LEMMA,
        "controls": list(base.CONTROLS),
        "sample_rule": dict(zip(EDGES, SAMPLE, strict=True)),
        "environment": _environment(),
        "started_utc": started,
        "wall_seconds": round(time.monotonic() - wall, 1),
        "workers": workers,
        "rows": rows,
    }
    _write(deposit.replay_receipt, receipt)
    return receipt


def stable(row: Mapping[str, Any]) -> dict[str, Any]:
    """A replay row without its timings."""
    copy = json.loads(json.dumps(row))
    copy.pop("cpu_seconds", None)
    copy["decision"].pop("cpu_seconds", None)
    return copy


# --------------------------------------------------------------------------- the check


def decisions_problems(
    deposit: Deposit, *, digests: bool = False
) -> tuple[list[str], list[dict[str, Any]]]:
    """Problems with a deposit's decisions receipt, every decision and control derived
    again, the author's column counted again and the written-out certificates at its
    sample (at every count with ``digests``) written again; and the receipt's rows."""
    parsed = table(deposit)
    receipt = read_receipt(deposit.decisions)
    label = deposit.label
    problems = []
    header = (receipt["format"], receipt["doi"], receipt["records"], receipt["lemma"])
    if header != (DECISIONS_FORMAT, deposit.doi, deposit.records_name, LEMMA) or receipt[
        "controls"
    ] != list(CONTROLS):
        problems.append(f"{label}: the decisions receipt's header is not this checker's")
    if receipt["author_columns"]["previous_source"] != sources(parsed):
        problems.append(f"{label}: the author's column is not counted as the rows")
    stored: list[dict[str, Any]] = receipt["rows"]
    if [item["n"] for item in stored] != [row.n for row, _ in parsed]:
        return [*problems, f"{label}: the receipt's rows are not the records'"], stored
    every: list[list[dict[str, Any]]] = []
    for (row, _), kept in zip(parsed, stored, strict=True):
        wanted, checked = decision_row(row, digest=digests or row.n in deposit.sample)
        every.append(checked)
        if {key: kept.get(key) for key in wanted} != wanted:
            problems.append(f"{label} n={row.n}: the decision differs from the receipt")
        if wanted["verdict"] == DECIDED and kept.get("controls_refused") != len(CONTROLS):
            problems.append(f"{label} n={row.n}: a control was accepted")
    if receipt["summary"] != decisions_summary(stored, every):
        problems.append(f"{label}: the decisions summary does not match the rows")
    return problems, stored


def replay_problems(
    deposit: Deposit, stored: Sequence[Mapping[str, Any]], *, replay: bool = False
) -> list[str]:
    """Problems with the replay sample against the decisions receipt's rows (``stored``):
    its counts, a pass on both routes with all six controls refused by both at each, the
    certificate the decided one (or, for a row the lemma refused, the construction's);
    and each count replayed again with ``replay``."""
    from devtools import couzo_678_replay as base  # noqa: PLC0415

    label = deposit.label
    sample = read_receipt(deposit.replay_receipt)
    problems = []
    if [item["n"] for item in sample["rows"]] != list(SAMPLE) or sample["sample_rule"] != dict(
        zip(EDGES, SAMPLE, strict=True)
    ):
        problems.append(f"{label}: the replay receipt's counts are not the sample's")
    if sample["controls"] != list(base.CONTROLS):
        problems.append(f"{label}: the replay receipt's controls are not the routes' six")
    by_n = {item["n"]: item for item in stored}
    for kept in sample["rows"]:
        n = kept["n"]
        if not kept["verified"]:
            problems.append(f"{label} n={n}: the written-out certificate failed a route")
        if [item["control"] for item in kept["controls"]] != list(base.CONTROLS) or not all(
            item["refused_by_sqpack"] and item["refused_by_independent"]
            for item in kept["controls"]
        ):
            problems.append(f"{label} n={n}: a route accepted a control")
        decided = by_n.get(n, {})
        if decided.get("verdict") == DECIDED and (
            kept["certificate_sha256"],
            kept["lemma"].get("capacity"),
        ) != (decided.get("certificate_sha256"), decided.get("capacity")):
            problems.append(f"{label} n={n}: the replayed certificate is not the decided one")
        if replay and stable(replay_row(n, deposit)) != stable(kept):
            problems.append(f"{label} n={n}: the replay differs from the receipt")
    return problems


def refused_problems(deposit: Deposit, stored: Sequence[Mapping[str, Any]]) -> list[str]:
    """A row the lemma refuses is decided only where the replay sample passes its
    written-out construction on both routes, all six controls refused by both."""
    refused = [item["n"] for item in stored if item["verdict"] != DECIDED]
    if not refused:
        return []
    routed = {}
    if deposit.replay and retained_data.retained_exists(deposit.replay_receipt):
        routed = {item["n"]: item for item in read_receipt(deposit.replay_receipt)["rows"]}
    problems = []
    for n in refused:
        item = routed.get(n)
        if (
            item is None
            or not item["verified"]
            or not all(
                control["refused_by_sqpack"] and control["refused_by_independent"]
                for control in item["controls"]
            )
        ):
            problems.append(
                f"{deposit.label} n={n}: refused by the lemma and not decided on both routes"
            )
    return problems


def author_sample_problems() -> list[str]:
    """`write_out` must write the author-built sample's five certificates byte for byte:
    the SHA-256, size and side `devtools.filled_end_sample`'s receipt names."""
    receipt = read_receipt(PACKET / AUTHOR_SAMPLE)
    rows = {row.n: row for row in records(V2)}
    problems = []
    for kept in receipt["rows"]:
        n = kept["n"]
        text = certificate_text(rows[n]).encode("utf-8")
        written = (_sha256(text), len(text), legacy.literal(rows[n].side))
        if written != (
            kept["certificate_sha256"],
            kept["certificate_bytes"],
            kept["exact_side"],
        ):
            problems.append(f"V2.0 n={n}: write_out is not the author's build")
    return problems


def check(
    *,
    digests: bool = False,
    replay: bool = False,
    deposits: Sequence[Deposit] | None = None,
) -> list[str]:
    """Problems with the receipts against the packet: each deposit's decisions, any row
    the lemma refused, and the replay sample; and, with V2.0, the author-built sample's
    certificates. Empty when they hold. A deposit whose files fail custody is one
    problem, and the rest are still checked."""
    problems: list[str] = []
    chosen = DEPOSITS if deposits is None else deposits
    for deposit in chosen:
        try:
            found, stored = decisions_problems(deposit, digests=digests)
        except CustodyError as error:
            problems.append(f"{deposit.label}: custody: {error}")
            continue
        problems += found
        problems += refused_problems(deposit, stored)
        if deposit.replay:
            problems += replay_problems(deposit, stored, replay=replay)
    if V2 in chosen:
        problems += author_sample_problems()
    return problems


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n", 1)[0])
    commands = parser.add_subparsers(dest="command", required=True)
    every = commands.add_parser("decide-all")
    every.add_argument("--version", choices=tuple(VERSIONS), action="append")
    sample = commands.add_parser("replay-sample")
    sample.add_argument("--n", type=int, nargs="+")
    sample.add_argument("--workers", type=int, default=2)
    audit = commands.add_parser("check")
    audit.add_argument("--digests", action="store_true")
    audit.add_argument("--replay", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "check":
        problems = check(digests=args.digests, replay=args.replay)
        for problem in problems:
            print(problem)
        if problems:
            print("FAILED")
            return 1
        decided = ", ".join(f"{deposit.rows} {deposit.label} rows" for deposit in DEPOSITS)
        print(
            f"OK: {decided} decided by the lemma, every control refused; {len(SAMPLE)} V2.0 "
            "counts written out and passed by both routes, their controls refused; the "
            "author-built sample written out byte for byte"
        )
        return 0
    if args.command == "decide-all":
        chosen = [VERSIONS[version] for version in args.version] if args.version else DEPOSITS
        print(
            json.dumps(
                {deposit.label: decide_all(deposit)["summary"] for deposit in chosen}, indent=1
            )
        )
        return 0
    receipt = replay_sample(args.n or list(SAMPLE), args.workers)
    print(
        json.dumps(
            [
                {
                    key: row[key]
                    for key in ("n", "verified", "certificate_sha256", "cpu_seconds")
                }
                for row in receipt["rows"]
            ],
            indent=1,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
