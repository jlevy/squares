"""Decide a two-strip L-packing exactly from its parameters (#799, think-clgp).

Mohsen Karimi's issue #799 reports 683 upper bounds at n = 1184 to 3775, published as
Zenodo record 10.5281/zenodo.23624433, V1.0. No row has a certificate file: each states
a side S, the integer K just above it, and the parameters of one packing. A box of side S
holds two strips of unit squares tilted by small angles, mH rows on the bottom wall and
mV rows standing on the right wall, and the rest is an axis-parallel grid. This is
Sungjoon Ryu's L-shaped packing (his Theorem 1.3, `cases.asymptotic.ryu_upper_l_packing`)
with the two strips' widths, angles and phases chosen independently. By the owner's D2
answer (think-f2io) such a row is a row once "decided exactly from the recipe by a
checker this project maintains"; this module is that checker for the two-strip kind.
`devtools.construction_checker` decides the recipes that build on a replayed parent, and
a two-strip packing has no parent.

**The construction.** For a strip tilted by a with t = tan(a/2), 0 < t < 1, let
c = (1 - t^2)/(1 + t^2), s = 2t/(1 + t^2), e = (c + s)/2 and p = 1/c. A strip of m rows
and length W holds, in row j = 0 .. m - 1, unit squares turned by -a with centres
(x0_j + k p, e + j c) for k = 0, 1, ... while x0_j + k p + e <= W, where
x0_j = e + ((ph p + j s) mod p) and ph in [0, 1) is the strip's phase.

- The H strip: mH rows of tilt tH and phase phH, length S - wV, on the bottom wall.
- The V strip: mV rows of tilt tV and phase phV, length S, the same construction turned
  by 90 degrees, (x, y) -> (S - y, x), on the right wall; wV = mV cV + sV.
- The grid: K - mV columns and K - mH rows of axis-parallel unit squares, centres
  (i + 1/2, S - j - 1/2), in [0, K - mV] x [S - (K - mH), S].

**The lemma** (`LEMMA`).

- *Within a strip.* Two of its squares have centres differing by dj (s, c) + N (p, 0)
  for integers dj and N, since the rows' first centres differ by dj s modulo p. Along
  the squares' own axes (c, -s) and (s, c) that difference is (N, dj + N s/c), so two
  distinct squares are interior-disjoint: |N| >= 1 when N != 0, and |dj| >= 1 when
  N = 0. A unit square turned by a has half-width e in x and in y, so every square lies
  in [0, W] x [0, m c + s]: x0_j - e >= 0, the last centre plus e is at most W, and row
  j spans heights j c to (j + 1) c + s.
- *Between regions.* The H strip lies in [0, S - wV] x [0, hH], hH = mH cH + sH; the V
  strip in [S - wV, S] x [0, S]; the grid in [0, K - mV] x [S - (K - mH), S]. Their
  interiors are disjoint, and all three lie in [0, S]^2, when hH <= S - (K - mH) and
  K - mV <= S - wV (the fit inequalities), with 1 <= mH, mV <= K - 1.
- *Capacity.* Row j of a strip holds floor((W - e - x0_j) c) + 1 squares when
  W - e - x0_j >= 0 and none otherwise; the grid holds (K - mV)(K - mH). Deleting
  squares from a packing leaves a packing, so every n up to the capacity is packed.

`decide` holds a row to the lemma in `Fraction`s and returns the capacity, each part's
count, the two slacks of the fit inequalities and the verdict, or raises
`TwoStripRefusedError` saying why not. It refuses any other kind; a K above `MAX_K`; a
tilt outside (0, 1); a strip of no rows or of K or more; a phase outside [0, 1); a side
that fails either fit inequality; and a count above the capacity. Whether S < K and
whether K is the ceiling of sqrt(n) are reported, not required: they say whether the
bound beats the grid, not whether the packing is one. A checker of a lemma is sound, not
complete: it refuses some genuine packings the lemma does not state, and must.

`mutants` are a row's negative controls (`CONTROLS`), each of which `decide` must
refuse, and `controls` decides them: the count one above the capacity; the side
10^-15 below the binding fit inequality (W7's "one unit below" carries no meaning here,
since #799's sides sit at least 1.13e-8 above the fit, and a side 10^-12 lower is still
a packing); both strips one row deeper around the same grid (K, mH and mV each one
more, at the original capacity), refused whenever a strip's fit slack is below its c;
no tilt (tH = 0); a right angle (tV = 1); the grid one column and row larger at the same
side, refused whenever a slack is below 1; and an unknown kind. #799's largest slack is
0.025, and c is about 0.98. The H strip one row deeper alone is no control: it is a
genuine two-strip packing by the same lemma, whose capacity falls only when the
parameters were locally better, which is a property of the data. A control `decide`
accepts is reported, ``refused`` False, so a check fails rather than passing it over.

`write_out` builds the packing the lemma states, as a certificate in Evan Daniel's
``n S`` / ``x y t`` format with t = tan(theta/2): the H strip's squares row by row, the V
strip's, then the grid's column by column, the surplus over n dropped from the end of
the grid, as the source's README says its program does. The record does not run the
source's ``regenerate.py``; `write_out` is this module's own builder, written from the
README and the issue.

**#799's packet.** ``karimi-two-strip-2026-10-24`` retains the record's three zip
members, which ``devtools.capture_web_source zenodo`` wrote after holding the archive to
the MD5 Zenodo states, and its ``issue_text-1.md``, which the tool checks by its MD5 but
does not write, so it was fetched alone and placed beside them. From then on Git keeps
them (OR-16), so `custody` compares no digest: it checks that the capture is record
23624433 and that the packet keeps exactly the files the capture names.

**The ingest.** ``records.csv`` is another party's file, read as untrusted data by
`parse_records`, which any deposit of the family can use (version 2's 2,824 rows are
the next). The header must be the eleven columns exactly, each row exactly eleven
fields, each literal matched whole with at most `MAX_DIGITS` digits in each part, K at
most `MAX_K` and equal to ceil(sqrt(n)), and each count once. Every refusal is a
`CustodyError`. `records` reads the packet's 683 rows through it. The receipts are:

- ``receipts/two-strip-decisions.json`` (``decide-all``): every row decided, every
  control refused, and the SHA-256 and size of each written-out certificate, which the
  record does not retain (OR-18: they are derived, and `write_out` writes them again
  byte for byte). It records no row of the coverage register.
- ``receipts/replay-sample.json`` (``replay-sample``): the cross-check. At five counts,
  1184, 1193, 1813, 2363 and 3775, the written-out certificate is decided on both exact
  routes of `devtools.couzo_678_replay` with its six controls, as
  `beyond_horizon_replay.decide_row` decides a row, so the lemma's verdict and the
  routes' agree where both are run.

``check`` reads both receipts back: every decision and control derived again, the
digests at the sample written out again (every count's with ``--digests``), and with
``--replay`` the sample decided again on both routes.

From ``packing/``, with the project interpreter::

    python -m devtools.two_strip_checker decide-all
    python -m devtools.two_strip_checker replay-sample [--n 1184 ...] [--workers 2]
    python -m devtools.two_strip_checker check [--digests] [--replay]

A finite packing certifies an upper bound and nothing more. Whether a row is below every
earlier report at its count is the walk's to decide, not this module's.
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
from collections.abc import Callable, Iterator, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from fractions import Fraction
from itertools import islice
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import evand_exact_certificates as legacy
from devtools.retained_data import read_retained_bytes
from sqpack.retained_json import dumps as retained_dumps

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent

KIND = "two-strip"
DECIDED = "decided"
#: The lemma a decision rests on, as a receipt states it.
LEMMA = (
    "Two squares of one strip, turned by -a with t = tan(a/2), c = (1 - t^2)/(1 + t^2), "
    "s = 2t/(1 + t^2), have centres differing by dj (s, c) + N (1/c, 0), which along "
    "their axes is (N, dj + N s/c), so distinct squares are interior-disjoint; a strip of "
    "m rows of length W lies in [0, W] x [0, m c + s] when each centre is at least "
    "e = (c + s)/2 from both ends; the H strip in [0, S - wV] x [0, hH], the V strip in "
    "[S - wV, S] x [0, S] and the (K - mV) x (K - mH) grid in [0, K - mV] x "
    "[S - (K - mH), S] have disjoint interiors inside [0, S]^2 when hH <= S - (K - mH) and "
    "K - mV <= S - wV; row j holds floor((W - e - x0_j) c) + 1 squares, and deleting "
    "squares leaves a packing"
)
#: The controls every row carries (`mutants`), in order.
CONTROLS = (
    "count above the capacity",
    "side below the binding fit",
    "both strips one row deeper",
    "no tilt",
    "a right angle",
    "grid one larger",
    "unknown kind",
)
#: How far below the binding fit inequality the side control puts the side.
FIT_MARGIN = Fraction(1, 10**15)
#: The largest K the checker decides. The family's deposits reach K = 100 (version 2,
#: n <= 9944); ten times that bounds the work a hostile row can ask for, since a strip
#: has fewer than K rows and the grid at most K^2 squares.
MAX_K = 1000

# --------------------------------------------------------------------------- #799's packet

PACKET = ROOT / "resources/web/karimi-two-strip-2026-10-24"
RECORD = 23624433
DOI = "10.5281/zenodo.23624433"
ISSUE = "https://github.com/jlevy/squares/issues/799"
CAPTURE = PACKET / f"zenodo/zenodo-{RECORD}-receipt.json"
EXTRACTED = PACKET / f"zenodo/zenodo-{RECORD}"
RECORDS = EXTRACTED / "records.csv"
#: The deposit's one archive, whose members the packet keeps.
ARCHIVE = "karimi_two_strip_records_v1_lite.zip"
#: The deposit's issue text, kept beside the members (not an archive member).
ISSUE_TEXT = "issue_text-1.md"
ROWS = 683
DECISIONS = PACKET / "receipts/two-strip-decisions.json"
REPLAY = PACKET / "receipts/replay-sample.json"
DECISIONS_FORMAT = "two-strip-decisions-v1"
REPLAY_FORMAT = "two-strip-replay-sample-v1"
#: The counts the stage 1 triage replayed, from 1184 to 3775: the cross-check's sample.
SAMPLE = (1184, 1193, 1813, 2363, 3775)

#: The columns of a deposit's ``records.csv``, exactly and in order.
COLUMNS = (
    "n",
    "new_side_exact",
    "new_side",
    "previous_best_side",
    "K",
    "mH",
    "tH",
    "phH",
    "mV",
    "tV",
    "phV",
)
#: The most digits in any one part of a literal (a numerator, a denominator, either side
#: of a decimal point). The deposits' longest run is 12 digits, in the comparison column.
MAX_DIGITS = 30

_RATIONAL = re.compile(rf"[0-9]{{1,{MAX_DIGITS}}}(/[1-9][0-9]{{0,{MAX_DIGITS - 1}}})?")
_INTEGER = re.compile(rf"[1-9][0-9]{{0,{MAX_DIGITS - 1}}}")
_DECIMAL = re.compile(rf"[0-9]{{1,{MAX_DIGITS}}}\.[0-9]{{1,{MAX_DIGITS}}}")


class TwoStripRefusedError(ValueError):
    """A row the checker does not decide, with the reason."""


class CustodyError(ValueError):
    """The packet's files are not the ones the capture pinned."""


def _refuse(condition: object, message: str) -> None:
    if not condition:
        raise TwoStripRefusedError(message)


@dataclass(frozen=True, slots=True)
class TwoStrip:
    """One two-strip packing as a row states it: the count, the side, the integer K, and
    each strip's rows, tilt t = tan(a/2) and phase (``h`` the bottom strip, ``v`` the
    right-hand one). ``k`` is the record's K."""

    n: int
    side: Fraction
    k: int
    rows_h: int
    tilt_h: Fraction
    phase_h: Fraction
    rows_v: int
    tilt_v: Fraction
    phase_v: Fraction
    kind: str = KIND


@dataclass(frozen=True, slots=True)
class StripRow:
    """One row of a strip, in the strip's own frame: the first centre along the strip,
    the centres' height across it, and how many squares the row holds."""

    first: Fraction
    height: Fraction
    count: int


def basis(tilt: Fraction) -> tuple[Fraction, Fraction]:
    """``(cos a, sin a)`` for ``tilt = tan(a/2)``, exactly."""
    square = tilt * tilt
    return (1 - square) / (1 + square), 2 * tilt / (1 + square)


def thickness(tilt: Fraction, rows: int) -> Fraction:
    """How far a strip of ``rows`` rows reaches from its wall: m c + s."""
    cos, sin = basis(tilt)
    return rows * cos + sin


def strip(tilt: Fraction, rows: int, length: Fraction, phase: Fraction) -> tuple[StripRow, ...]:
    """A strip's rows by the construction: row j's first centre is
    e + ((ph p + j s) mod p) along the strip, at height e + j c, and the row holds every
    square whose centre is at most ``length`` - e along."""
    cos, sin = basis(tilt)
    half, pitch = (cos + sin) / 2, 1 / cos
    found = []
    for row in range(rows):
        first = half + (phase * pitch + row * sin) % pitch
        room = length - half - first
        count = math.floor(room * cos) + 1 if room >= 0 else 0
        found.append(StripRow(first, half + row * cos, count))
    return tuple(found)


def binding_side(row: TwoStrip) -> Fraction:
    """The least side at which both fit inequalities hold, for the row's K and strips."""
    return max(
        row.k - row.rows_h + thickness(row.tilt_h, row.rows_h),
        row.k - row.rows_v + thickness(row.tilt_v, row.rows_v),
    )


def decide(row: TwoStrip) -> dict[str, Any]:
    """The row decided exactly by the lemma; `TwoStripRefusedError` says why not."""
    _refuse(row.kind == KIND, f"kind {row.kind!r}: not a two-strip packing")
    _refuse(row.n >= 1, f"n = {row.n}: no squares to pack")
    _refuse(row.side > 0, f"the side {row.side} is not positive")
    _refuse(1 < row.k <= MAX_K, f"K = {row.k}: the checker decides 2 <= K <= {MAX_K}")
    for name, tilt in (("tH", row.tilt_h), ("tV", row.tilt_v)):
        _refuse(0 < tilt < 1, f"{name} = {tilt}: a strip's tan(a/2) must lie in (0, 1)")
    for name, rows in (("mH", row.rows_h), ("mV", row.rows_v)):
        _refuse(0 < rows < row.k, f"{name} = {rows}: a strip has 1 to K - 1 = {row.k - 1} rows")
    for name, phase in (("phH", row.phase_h), ("phV", row.phase_v)):
        _refuse(0 <= phase < 1, f"{name} = {phase}: a phase lies in [0, 1)")
    high = thickness(row.tilt_h, row.rows_h)
    wide = thickness(row.tilt_v, row.rows_v)
    slack_h = row.side - (row.k - row.rows_h) - high
    slack_v = row.side - wide - (row.k - row.rows_v)
    _refuse(
        slack_h >= 0,
        f"the H strip, {float(high):.12g} high, overlaps the grid by {float(-slack_h):.3e}: "
        "mH cH + sH > S - (K - mH)",
    )
    _refuse(
        slack_v >= 0,
        f"the V strip, {float(wide):.12g} wide, overlaps the grid by {float(-slack_v):.3e}: "
        "K - mV > S - (mV cV + sV)",
    )
    held_h = sum(
        item.count for item in strip(row.tilt_h, row.rows_h, row.side - wide, row.phase_h)
    )
    held_v = sum(item.count for item in strip(row.tilt_v, row.rows_v, row.side, row.phase_v))
    grid = (row.k - row.rows_v) * (row.k - row.rows_h)
    held = held_h + held_v + grid
    _refuse(row.n <= held, f"n = {row.n} is above the capacity {held}")
    return {
        "n": row.n,
        "kind": row.kind,
        "side": legacy.literal(row.side),
        "k": row.k,
        "capacity": held,
        "h_strip": held_h,
        "v_strip": held_v,
        "grid": grid,
        "surplus": held - row.n,
        "h_slack": legacy.literal(slack_h),
        "v_slack": legacy.literal(slack_v),
        "side_below_k": row.side < row.k,
        "k_is_ceil_sqrt_n": row.k == math.isqrt(row.n - 1) + 1,
        "verdict": DECIDED,
    }


def capacity(row: TwoStrip) -> int:
    """The row's capacity, by `decide` at its own count."""
    return int(decide(replace(row, n=1))["capacity"])


def mutants(row: TwoStrip) -> list[tuple[str, TwoStrip]]:
    """A row's negative controls, each a change `decide` must refuse (`CONTROLS`)."""
    held = capacity(row)
    changed = [
        replace(row, n=held + 1),
        replace(row, side=binding_side(row) - FIT_MARGIN),
        replace(row, k=row.k + 1, rows_h=row.rows_h + 1, rows_v=row.rows_v + 1, n=held),
        replace(row, tilt_h=Fraction(0)),
        replace(row, tilt_v=Fraction(1)),
        replace(row, k=row.k + 1),
        replace(row, kind="three-strip"),
    ]
    return list(zip(CONTROLS, changed, strict=True))


def controls(row: TwoStrip) -> list[dict[str, Any]]:
    """Each control (`mutants`) and the reason `decide` refused it; ``refused`` False
    marks one it accepted, which a check refuses."""
    found = []
    for name, changed in mutants(row):
        try:
            decide(changed)
        except TwoStripRefusedError as error:
            found.append({"control": name, "refused": True, "reason": str(error)})
        else:
            found.append({"control": name, "refused": False, "reason": ""})
    return found


def poses(row: TwoStrip) -> Iterator[legacy.Pose]:
    """Every square the construction places, decided or not, one at a time: the H strip
    row by row, the V strip turned onto the right wall, then the grid column by column."""
    wide = thickness(row.tilt_v, row.rows_v)
    pitch_h = 1 / basis(row.tilt_h)[0]
    for item in strip(row.tilt_h, row.rows_h, row.side - wide, row.phase_h):
        for k in range(item.count):
            yield legacy.Pose(item.first + k * pitch_h, item.height, -row.tilt_h)
    pitch_v = 1 / basis(row.tilt_v)[0]
    for item in strip(row.tilt_v, row.rows_v, row.side, row.phase_v):
        for k in range(item.count):
            yield legacy.Pose(row.side - item.height, item.first + k * pitch_v, -row.tilt_v)
    half = Fraction(1, 2)
    for i in range(row.k - row.rows_v):
        for j in range(row.k - row.rows_h):
            yield legacy.Pose(half + i, row.side - half - j, Fraction(0))


def write_out(row: TwoStrip) -> legacy.Certificate:
    """The packing the lemma states for a row it decides: the first n squares `poses`
    places, so the surplus is dropped from the end of the grid and never built."""
    decide(row)
    return legacy.Certificate(row.n, row.side, tuple(islice(poses(row), row.n)))


def certificate_text(row: TwoStrip) -> str:
    """A decided row's written-out certificate, ``n S`` then ``x y t`` rows."""
    return legacy.serialize(write_out(row))


# --------------------------------------------------------------------------- the packet


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def custody() -> None:
    """Hold the packet to the capture by name: the capture is record 23624433, its files
    are the archive and the issue text, and the packet keeps exactly the archive's
    members the capture extracted, with the issue text. Git keeps the bytes (OR-16)."""
    capture = _read(CAPTURE)
    if (capture.get("record"), capture.get("doi")) != (RECORD, DOI):
        raise CustodyError(f"the capture is not record {RECORD}")
    files = sorted(item["key"] for item in capture["files"])
    if files != sorted((ARCHIVE, ISSUE_TEXT)):
        raise CustodyError(f"the capture's files are {files}")
    kept = sorted([*(item["member"] for item in capture["extracted"]), ISSUE_TEXT])
    present = sorted(path.name for path in EXTRACTED.iterdir())
    if present != kept or RECORDS.name not in present:
        raise CustodyError(f"the packet keeps {present}, the capture {kept}")


def _literal(text: str, pattern: re.Pattern[str], where: str) -> str:
    if pattern.fullmatch(text) is None:
        raise CustodyError(f"{where}: {text!r} is not the literal the format states")
    return text


def row_from_record(item: Mapping[str, object]) -> TwoStrip:
    """A row of a deposit's ``records.csv`` as `COLUMNS` names its fields, each a string
    matched whole before it is read: ``n``, ``K``, ``mH`` and ``mV`` integers,
    ``new_side_exact``, ``tH``, ``phH``, ``tV`` and ``phV`` rationals, and ``new_side``
    and the author's ``previous_best_side`` decimals. The decimal side must be the exact
    side, so the table states one side; K must be at most `MAX_K` and ceil(sqrt(n)), as
    every deposit's row is. Anything else is a `CustodyError`."""
    shown = repr(item.get("n"))[:40] if isinstance(item, Mapping) else "?"
    where = f"records.csv n={shown}"
    if not isinstance(item, Mapping) or sorted(map(str, item)) != sorted(COLUMNS):
        raise CustodyError(f"{where}: the fields are not the columns {list(COLUMNS)}")
    if not all(isinstance(value, str) for value in item.values()):
        raise CustodyError(f"{where}: a field is missing or not text")
    text = {str(key): str(value) for key, value in item.items()}

    def whole(name: str) -> int:
        return int(_literal(text[name], _INTEGER, where))

    def rational(name: str) -> Fraction:
        return Fraction(_literal(text[name], _RATIONAL, where))

    side = rational("new_side_exact")
    if Fraction(_literal(text["new_side"], _DECIMAL, where)) != side:
        raise CustodyError(f"{where}: the decimal side is not the exact side")
    _literal(text["previous_best_side"], _DECIMAL, where)
    n, k = whole("n"), whole("K")
    if k > MAX_K:
        raise CustodyError(f"{where}: K = {k} is above the checker's bound {MAX_K}")
    if k != math.isqrt(n - 1) + 1:
        raise CustodyError(f"{where}: K = {k} is not ceil(sqrt(n))")
    return TwoStrip(
        n=n,
        side=side,
        k=k,
        rows_h=whole("mH"),
        tilt_h=rational("tH"),
        phase_h=rational("phH"),
        rows_v=whole("mV"),
        tilt_v=rational("tV"),
        phase_v=rational("phV"),
    )


def parse_records(text: str) -> list[TwoStrip]:
    """A deposit's rows from its ``records.csv`` text, read as untrusted data: the header
    exactly `COLUMNS`, so no column is missing, extra or given twice; each row exactly
    that many fields; each row by `row_from_record`; and each count once. Every refusal
    is a `CustodyError`, including the csv module's own, as for a field past its size
    limit."""
    try:
        table = list(csv.reader(io.StringIO(text, newline=""), strict=True))
    except csv.Error as error:
        raise CustodyError(f"records.csv: {error}") from error
    if not table or tuple(table[0]) != COLUMNS:
        header = repr(table[0] if table else [])[:200]
        raise CustodyError(f"records.csv: the header is {header}, not {list(COLUMNS)}")
    rows = []
    for number, fields in enumerate(table[1:], start=1):
        if len(fields) != len(COLUMNS):
            raise CustodyError(
                f"records.csv row {number}: {len(fields)} fields, not {len(COLUMNS)}"
            )
        rows.append(row_from_record(dict(zip(COLUMNS, fields, strict=True))))
    counts = [row.n for row in rows]
    if len(set(counts)) != len(counts):
        raise CustodyError("records.csv: a count appears in more than one row")
    return rows


def records() -> list[TwoStrip]:
    """#799's rows, from the retained ``records.csv`` once `custody` holds."""
    custody()
    try:
        text = read_retained_bytes(RECORDS).decode("utf-8")
    except UnicodeDecodeError as error:
        raise CustodyError(f"records.csv is not UTF-8: {error}") from error
    rows = parse_records(text)
    if len(rows) != ROWS:
        raise CustodyError(f"records.csv holds {len(rows)} rows, not {ROWS}")
    return rows


# --------------------------------------------------------------------------- the receipts


def _write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_text(retained_dumps(value, sort_keys=True), encoding="utf-8")


def _environment() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "machine": platform.machine(),
    }


def _now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def decision_row(
    row: TwoStrip, *, digest: bool = True
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """One row of the decisions receipt, with its controls decided once: the decision,
    how many controls were refused and, with ``digest``, the written-out certificate's
    SHA-256 and size; and the controls themselves, for the summary."""
    found = decide(row)
    checked = controls(row)
    found["controls_refused"] = sum(1 for item in checked if item["refused"])
    if digest:
        text = certificate_text(row).encode("utf-8")
        found["certificate_sha256"] = _sha256(text)
        found["certificate_bytes"] = len(text)
    return found, checked


def decisions_summary(
    found: Sequence[dict[str, Any]], checked: Sequence[Sequence[dict[str, Any]]]
) -> dict[str, Any]:
    """Counts over the decisions, and each control's refusals over the rows' controls
    (``checked``, as `decision_row` decided them) with its reason at the first row."""
    tallies: dict[str, int] = dict.fromkeys(CONTROLS, 0)
    for row in checked:
        for item in row:
            tallies[item["control"]] += item["refused"]
    return {
        "rows": len(found),
        "decided": sum(1 for item in found if item["verdict"] == DECIDED),
        "squares": sum(item["n"] for item in found),
        "surplus_zero": sum(1 for item in found if item["surplus"] == 0),
        "surplus_most": max(item["surplus"] for item in found),
        "side_below_k": sum(1 for item in found if item["side_below_k"]),
        "k_is_ceil_sqrt_n": sum(1 for item in found if item["k_is_ceil_sqrt_n"]),
        "least_h_slack": f"{min(Fraction(item['h_slack']) for item in found):.6e}",
        "least_v_slack": f"{min(Fraction(item['v_slack']) for item in found):.6e}",
        "controls": {
            item["control"]: {
                "refused": tallies[item["control"]],
                "first_reason": item["reason"],
            }
            for item in checked[0]
        },
    }


def decide_all() -> dict[str, Any]:
    """Decide every row of #799 with its controls and write the decisions receipt."""
    rows = records()
    started, cpu = _now(), time.process_time()
    decided = [decision_row(row) for row in rows]
    found = [item for item, _ in decided]
    receipt = {
        "format": DECISIONS_FORMAT,
        "issue": ISSUE,
        "doi": DOI,
        "packet": PACKET.relative_to(REPO).as_posix(),
        "records": RECORDS.relative_to(REPO).as_posix(),
        "checker": "packing/devtools/two_strip_checker.py",
        "lemma": LEMMA,
        "controls": list(CONTROLS),
        "certificates": (
            "written out by write_out and serialized in the n S / x y t format; not "
            "retained, each pinned here by its SHA-256 and size"
        ),
        "environment": _environment(),
        "started_utc": started,
        "cpu_seconds": round(time.process_time() - cpu, 1),
        "rows": found,
        "summary": decisions_summary(found, [checked for _, checked in decided]),
    }
    _write(DECISIONS, receipt)
    return receipt


def replay_row(n: int) -> dict[str, Any]:
    """One count of the sample: the row decided by the lemma, its certificate written out
    and decided on both routes of `devtools.couzo_678_replay`, and the six controls."""
    # The replay module costs about two seconds to import; the checker needs none of it.
    from devtools import couzo_678_replay as base  # noqa: PLC0415

    row = next(row for row in records() if row.n == n)
    found = decide(row)
    cert = write_out(row)
    text = legacy.serialize(cert).encode("utf-8")
    started = time.process_time()
    result = base.decide(base.geometry(cert))
    positive = time.process_time()
    checked = base.decide_controls(cert)
    ended = time.process_time()
    return {
        "n": n,
        "capacity": found["capacity"],
        "certificate_sha256": _sha256(text),
        "certificate_bytes": len(text),
        "exact_side": legacy.literal(cert.side),
        "verified": result["passed"],
        "decision": result,
        "controls": checked,
        "cpu_seconds": {
            "positive": round(positive - started, 2),
            "controls": round(ended - positive, 2),
        },
    }


def replay_sample(counts: Sequence[int], workers: int) -> dict[str, Any]:
    """Replay the sample's certificates on both routes and write the replay receipt."""
    from devtools import couzo_678_replay as base  # noqa: PLC0415

    started, wall = _now(), time.monotonic()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(replay_row, counts))
    receipt = {
        "format": REPLAY_FORMAT,
        "issue": ISSUE,
        "doi": DOI,
        "packet": PACKET.relative_to(REPO).as_posix(),
        "checker": "packing/devtools/two_strip_checker.py",
        "routes": "packing/devtools/couzo_678_replay.py (decide and decide_controls)",
        "filter_lemma": base.FILTER_LEMMA,
        "controls": list(base.CONTROLS),
        "environment": _environment(),
        "started_utc": started,
        "wall_seconds": round(time.monotonic() - wall, 1),
        "workers": workers,
        "rows": rows,
    }
    _write(REPLAY, receipt)
    return receipt


def stable(row: Mapping[str, Any]) -> dict[str, Any]:
    """A replay row without its timings."""
    copy = json.loads(json.dumps(row))
    copy.pop("cpu_seconds", None)
    copy["decision"].pop("cpu_seconds", None)
    return copy


def check(*, digests: bool = False, replay: bool = False) -> list[str]:
    """Problems with the two receipts against the packet; empty when they hold."""
    from devtools import couzo_678_replay as base  # noqa: PLC0415

    rows = records()
    receipt = _read(DECISIONS)
    problems = []
    if (receipt["format"], receipt["records"], receipt["lemma"]) != (
        DECISIONS_FORMAT,
        RECORDS.relative_to(REPO).as_posix(),
        LEMMA,
    ) or receipt["controls"] != list(CONTROLS):
        problems.append("the decisions receipt's header is not this checker's")
    stored = receipt["rows"]
    if [item["n"] for item in stored] != [row.n for row in rows]:
        return [*problems, "the decisions receipt's rows are not the records'"]
    every: list[list[dict[str, Any]]] = []
    for row, kept in zip(rows, stored, strict=True):
        wanted, checked = decision_row(row, digest=digests or row.n in SAMPLE)
        every.append(checked)
        if {key: kept.get(key) for key in wanted} != wanted:
            problems.append(f"n={row.n}: the decision differs from the receipt")
        if kept["controls_refused"] != len(CONTROLS):
            problems.append(f"n={row.n}: a control was accepted")
    if receipt["summary"] != decisions_summary(stored, every):
        problems.append("the decisions summary does not match the rows")
    sample = _read(REPLAY)
    if [item["n"] for item in sample["rows"]] != list(SAMPLE):
        return [*problems, "the replay receipt's counts are not the sample"]
    if sample["controls"] != list(base.CONTROLS):
        problems.append("the replay receipt's controls are not the routes' six")
    by_n = {item["n"]: item for item in stored}
    for kept in sample["rows"]:
        n = kept["n"]
        if not kept["verified"]:
            problems.append(f"n={n}: the written-out certificate failed a route")
        if [item["control"] for item in kept["controls"]] != list(base.CONTROLS) or not all(
            item["refused_by_sqpack"] and item["refused_by_independent"]
            for item in kept["controls"]
        ):
            problems.append(f"n={n}: a route accepted a control")
        # The certificate is written out and never retained, so its digest is its name
        # (a generated artifact under OR-16): the replayed one must be the decided one.
        decided = by_n[n]
        if (kept["certificate_sha256"], kept["capacity"]) != (
            decided["certificate_sha256"],
            decided["capacity"],
        ):
            problems.append(f"n={n}: the replayed certificate is not the decided one")
        if replay and stable(replay_row(n)) != stable(kept):
            problems.append(f"n={n}: the replay differs from the receipt")
    return problems


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n", 1)[0])
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("decide-all")
    sample = commands.add_parser("replay-sample")
    sample.add_argument("--n", type=int, nargs="+", default=list(SAMPLE))
    sample.add_argument("--workers", type=int, default=2)
    audit = commands.add_parser("check")
    audit.add_argument("--digests", action="store_true")
    audit.add_argument("--replay", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "check":
        problems = check(digests=args.digests, replay=args.replay)
        for problem in problems:
            print(problem)
        print("FAILED" if problems else f"OK: {ROWS} rows decided, every control refused")
        return 1 if problems else 0
    actions: dict[str, Callable[[], Any]] = {
        "decide-all": lambda: decide_all()["summary"],
        "replay-sample": lambda: [
            {key: row[key] for key in ("n", "verified", "certificate_sha256", "cpu_seconds")}
            for row in replay_sample(args.n, args.workers)["rows"]
        ],
    }
    print(json.dumps(actions[args.command](), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
