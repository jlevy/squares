"""Measure two packings of one count pose by pose: how far apart they lie, for credit.

Every upper-bound import that asks whether a packing is another's, a refinement of it or
a new arrangement wrote its own ``measure/identity.py``: the evand-regularized-2026-10-20
packet's holds the measures, and the mishapolk-n204-2026-10-22, evand-n303-2026-10-22 and
amundsk-n303-2026-10-23 packets load them from its file. This module is those measures
once (OR-1). A measurement for credit; it decides nothing. The retained programs stay as
they were written, since their receipts are bound to them, and later packets call this.
It is not ``devtools.register_regularized_bounds.measure_identity``, the regularization
driver's own check of a view against the checkout witness it was regularized from
(`regularize_evand.identity`): that one decides a regularization's custody, and this one
measures any two packings of a count for credit and lineage.

**Inputs.** Each packing is named by a spec, ``[LABEL=]KIND:TARGET``:

- ``packet:NAME``, an import packet's admitted certificate at the count, read by
  `devtools.upper_bound_reports.read_facts`, which holds custody to the digest the packet
  pins;
- ``FORMAT:PATH``, a file read by the adapter of that name in
  `devtools.upper_bound_reports.ADAPTERS` (``evand-cert``, ``sqcert``,
  ``witness-center-basis`` and the rest), exactly; a path ending ``.gz`` is decompressed
  first, and any other is read as stored or as its retained ``.gz``
  (`devtools.retained_data.read_retained_bytes`);
- ``binary64-xyd:PATH``, a binary64 text packing, ``n side`` and then ``n`` rows
  ``x y degrees``, as Evan Daniel's ``.input.txt`` and ``.predescent.txt`` files state
  them; blank lines and lines starting ``#`` are comments. Each number is read as the
  binary64 value its decimal names, and each angle, reduced modulo a quarter turn, as the
  exact rotation whose half-angle tangent is the binary64 tangent of half of it.

The receipt names each file by its repository-relative path, or by its name alone where
it lies outside the repository, with the SHA-256 of the bytes read after any
decompression.

Anything else is refused (`MeasureError`, and by the command with exit status 2): an
unknown kind, a count other than ``n`` or above `MAX_COUNT`, a row with other than three
numbers, a token that is not a decimal number, a number that is not finite, a side that
is not positive, a file over `MAX_INPUT_BYTES` as stored or four times that read, and a
``.gz`` that is truncated or not a deflate stream.

**The count.** Each symmetry's assignment holds an ``n`` by ``n`` matrix of binary64
distances and solves it in ``O(n^3)``, so the counts are bounded by `MAX_COUNT`. Measured
on 24 October 2026 at 2,263, the largest count of any retained certificate (Francisco
Couzo's ``n2263.cert``, couzo-issue763-2026-10-23), against itself under ``nice`` on a
shared four-core host: 22 s of CPU and a peak of 573 MB resident, both growing with
``n^2`` or faster.

**The measures**, each of the first packing against the second, exactly as the retained
programs computed them, so a receipt they wrote is reproduced key for key:

- ``nearest_centre``: `devtools.check_half_angle_area.arrangement_gap`, exact: under each
  of the box's eight symmetries applied to the second packing, every square of the first
  is matched to the nearest centre of the second, a symmetry counting only where that is
  one to one (``one_to_one``); for the best, the largest displacement and turn and how
  many squares moved beyond each of `BOUNDS`;
- ``assignment``: the optimal assignment, least total squared centre displacement under
  each symmetry (``scipy.optimize.linear_sum_assignment``, the Hungarian method, in
  binary64), the least total kept, with the same counts;
- ``tilts`` of each packing and ``bands`` of each pair: the evand-n303-2026-10-22
  program's tilt classes, and how the first packing's tilted squares pair by the sign of
  their tilt under the assignment without a symmetry;
- ``centred``: the T-240 review's primary measure (couzo-issue763-2026-10-23,
  ``review/review-2026-10-24/identity.py``), the same assignment with the two boxes
  sharing their centre rather than their lower-left corner, which reads a refinement
  whose side moved as one: the best and the runner-up symmetry with their totals, since a
  packing near to symmetric under a reflection gives two of nearly equal cost; the
  largest and RMS move, the counts beyond `BOUNDS`, the bottleneck (the least largest
  move over all assignments), whether nearest centres pair the squares one to one, and
  how many squares turn by more than a degree or have their tilt beyond a degree
  reversed.

Exact sides and their differences are exact. What a binary64 step reads is printed as the
retained programs printed it, which is what lets their receipts reproduce: moves, totals
and the bottleneck at six significant digits, the side difference at seven (``.6e``),
turns at four, and the tilt range in full.

From ``packing/``, with the project interpreter::

    python -m devtools.measure_identity --n 303 \\
        "#755=packet:amundsk-n303-2026-10-23" \\
        "T-230=packet:evand-n303-2026-10-22" \\
        "T-239=witness-center-basis:witnesses/known-best/n-303.yaml" \\
        --out resources/web/PACKET/measure/identity.json

The first spec is the view, and each one after it is measured against it. The JSON
written is the receipt a packet keeps under ``measure/``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import zlib
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_bipartite_matching

from devtools import check_half_angle_area as area
from devtools import evand_exact_certificates as legacy
from devtools import retained_data
from devtools import upper_bound_reports as reports

FORMAT = "measure-identity-v1"
#: The displacements the counts are taken beyond, as every retained receipt names them.
BOUNDS = ("1e-9", "1e-6", "1e-3", "1e-2", "1e-1")
PACKET = "packet"
BINARY64 = "binary64-xyd"
MAX_INPUT_BYTES = reports.MAX_SOURCE_BYTES
SYMMETRIES = 8
_DECIMAL = re.compile(r"[-+]?(?:[0-9]+\.?[0-9]*|\.[0-9]+)(?:[eE][-+]?[0-9]+)?")
_COUNT = re.compile(r"[1-9][0-9]{0,8}")
#: The largest count measured: the largest of any retained certificate, 2,263, with room;
#: the module docstring gives what 2,263 cost.
MAX_COUNT = 2500

type Placed = tuple[Fraction, Fraction, Fraction, Fraction]
type Measured = tuple[Fraction, list[Placed]]


class MeasureError(ValueError):
    """An input this module refuses to measure."""


@dataclass(frozen=True)
class Packing:
    """One packing as the measures read it, with where it was read from."""

    label: str
    source: dict[str, Any]
    side: Fraction
    squares: tuple[Placed, ...]

    @property
    def measured(self) -> Measured:
        return self.side, list(self.squares)


# --------------------------------------------------------------------------- inputs


def _decimal(token: str, where: str) -> float:
    if _DECIMAL.fullmatch(token) is None:
        raise MeasureError(f"{where}: {token!r} is not a decimal number")
    value = float(token)
    if not math.isfinite(value):
        raise MeasureError(f"{where}: {token!r} is not finite")
    return value


def rotation_from_degrees(degrees: float) -> tuple[Fraction, Fraction]:
    """An exact rotation for a binary64 angle in degrees, read modulo a quarter turn.

    The angle is reduced into ``[-45, 45)``, which draws the same square, and the rotation
    is the one whose half-angle tangent is the binary64 tangent of half of it: not the
    exact rotation nearest the angle, but one within a few units in the last place of it
    that lies exactly on the unit circle, as `check_half_angle_area.rotation` requires.
    """
    folded = (degrees + 45.0) % 90.0 - 45.0
    return area.rotation(Fraction(math.tan(math.radians(folded) / 2)))


def read_binary64(raw: bytes, n: int) -> Measured:
    """A binary64 ``n side`` / ``x y degrees`` text packing of exactly ``n`` squares."""
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as error:
        raise MeasureError("a binary64 packing is ASCII text") from error
    rows = [
        line.split()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not rows or len(rows[0]) != 2 or _COUNT.fullmatch(rows[0][0]) is None:
        raise MeasureError("the header is not 'n side'")
    if int(rows[0][0]) != n:
        raise MeasureError(f"the header states {rows[0][0]} squares, not {n}")
    side = _decimal(rows[0][1], "side")
    if side <= 0:
        raise MeasureError("the side must be positive")
    body = rows[1:]
    if len(body) != n:
        raise MeasureError(f"{len(body)} square rows for n = {n}")
    squares: list[Placed] = []
    for index, row in enumerate(body, start=1):
        where = f"square {index}"
        if len(row) != 3:
            raise MeasureError(f"{where}: {len(row)} numbers, not x y degrees")
        x, y, degrees = (_decimal(token, where) for token in row)
        squares.append((Fraction(x), Fraction(y), *rotation_from_degrees(degrees)))
    return Fraction(side), squares


def _from_certificate(certificate: legacy.Certificate) -> Measured:
    return certificate.side, area.placed([(p.x, p.y, p.t) for p in certificate.poses])


def _file_bytes(path: Path) -> bytes:
    try:
        if path.suffix == retained_data.GZIP_SUFFIX:
            with path.open("rb") as stream:
                stored = stream.read(MAX_INPUT_BYTES + 1)
            if len(stored) > MAX_INPUT_BYTES:
                raise MeasureError(f"{path} exceeds {MAX_INPUT_BYTES} bytes")
            return retained_data.gunzip_bytes(stored, limit=4 * MAX_INPUT_BYTES, name=str(path))
        return retained_data.read_retained_bytes(path, limit=4 * MAX_INPUT_BYTES)
    except (OSError, ValueError, EOFError, zlib.error) as error:
        if isinstance(error, MeasureError):
            raise
        raise MeasureError(f"{path}: {error}") from error


def _where(path: Path) -> dict[str, Any]:
    """The path repository-relative where it lies in the repository; else its name alone."""
    try:
        return {"path": path.resolve().relative_to(reports.REPO.resolve()).as_posix()}
    except ValueError:
        return {"path": path.name, "outside_repository": True}


def split_spec(spec: str) -> tuple[str | None, str, str]:
    """``[LABEL=]KIND:TARGET`` as its label, kind and target."""
    label: str | None = None
    head, equals, tail = spec.partition("=")
    if equals and ":" not in head:
        label, spec = head, tail
    kind, colon, target = spec.partition(":")
    if not colon or not kind or not target:
        raise MeasureError(f"{spec!r} is not KIND:TARGET")
    if label is not None and not label.strip():
        raise MeasureError("an empty label")
    return label, kind, target


def read_packing(spec: str, n: int) -> Packing:
    """One packing of ``n`` squares, from its spec (see the module docstring)."""
    if type(n) is not int or n < 1:
        raise MeasureError("the count must be a positive integer")
    if n > MAX_COUNT:
        raise MeasureError(f"{n} squares is above the {MAX_COUNT} this tool measures")
    label, kind, target = split_spec(spec)
    plain = spec if label is None else spec.partition("=")[2]
    if kind == PACKET:
        try:
            facts = reports.read_facts(reports.packet_path(target), {n})
        except reports.ReportError as error:
            raise MeasureError(f"{plain}: {error}") from error
        if n not in facts:
            raise MeasureError(f"{plain}: the packet declares no certificate at {n}")
        side, squares = _from_certificate(facts[n])
        source: dict[str, Any] = {"input": PACKET, "packet": target}
    elif kind == BINARY64 or kind in reports.ADAPTERS:
        path = Path(target)
        raw = _file_bytes(path)
        if kind == BINARY64:
            side, squares = read_binary64(raw, n)
        else:
            try:
                side, squares = _from_certificate(reports.parse_certificate(raw, n, kind))
            except reports.ReportError as error:
                raise MeasureError(f"{plain}: {error}") from error
        source = {"input": kind, **_where(path), "sha256": hashlib.sha256(raw).hexdigest()}
    else:
        raise MeasureError(f"{plain}: unknown kind {kind!r}")
    if len(squares) != n:
        raise MeasureError(f"{plain}: {len(squares)} squares, not {n}")
    return Packing(label or plain, source, side, tuple(squares))


# --------------------------------------------------------------------------- measures


def nearest_centre(first: Measured, second: Measured) -> dict[str, Any]:
    """`check_half_angle_area.arrangement_gap`, or its refusal where no symmetry is one to
    one, as the retained programs report it."""
    try:
        found = area.arrangement_gap(first, second)
    except area.AreaRouteError as error:
        return {"one_to_one": False, "refusal": str(error)}
    return {
        "one_to_one": True,
        "symmetry": found["symmetry"],
        "largest_displacement": found["largest_displacement"],
        "largest_turn_degrees": (
            f"{math.degrees(math.asin(min(1.0, float(found['largest_orientation_sine'])))):.4g}"
        ),
        "moved_beyond": found["moved_beyond"],
        "turned_beyond_1e-6": found["turned_beyond_1e-6"],
    }


def _centres(squares: list[Placed]) -> np.ndarray:
    return np.array([[float(x), float(y)] for x, y, _c, _s in squares])


def _turn_sine(left: Placed, right: Placed) -> Fraction:
    """The sine of the least angle between the two squares' edges."""
    _x, _y, c, s = left
    _u, _v, p, q = right
    return min(abs(c * q - s * p), abs(c * p + s * q))


def assignment(first: Measured, second: Measured) -> dict[str, Any]:
    """The optimal assignment under the symmetry whose total squared move is least."""
    _side, left = first
    other_side, right = second
    a = _centres(left)
    best: tuple[float, int, list[Placed], np.ndarray, np.ndarray, np.ndarray] | None = None
    for k in range(SYMMETRIES):
        mapped = [area.symmetric(other_side, square, k) for square in right]
        b = _centres(mapped)
        cost = ((a[:, None, :] - b[None, :, :]) ** 2).sum(axis=2)
        rows, cols = linear_sum_assignment(cost)
        total = float(cost[rows, cols].sum())
        if best is None or total < best[0]:
            best = (total, k, mapped, cost, rows, cols)
    if best is None:
        raise MeasureError("no symmetry was measured")
    _total, k, mapped, cost, rows, cols = best
    moves = np.sqrt(cost[rows, cols])
    turns = [float(_turn_sine(left[i], mapped[j])) for i, j in zip(rows, cols, strict=True)]
    return {
        "symmetry": k,
        "largest_move": f"{float(moves.max()):.6g}",
        "moved_beyond": {bound: int((moves > float(bound)).sum()) for bound in BOUNDS},
        "largest_turn_degrees": f"{math.degrees(math.asin(min(1.0, max(turns)))):.4g}",
        "turned_beyond_1e-6": sum(1 for turn in turns if turn > 1e-6),
    }


def measure(first: Measured, second: Measured) -> dict[str, Any]:
    """The side difference, exact, and both pairings."""
    difference = first[0] - second[0]
    return {
        "side_difference": f"{float(difference):.6e}",
        "side_difference_exact": str(difference),
        "nearest_centre": nearest_centre(first, second),
        "assignment": assignment(first, second),
    }


def signed_tilt(c: Fraction, s: Fraction) -> float:
    """The square's turn in degrees, folded to (-45, 45]."""
    angle = math.degrees(math.atan2(float(s), float(c))) % 90.0
    return angle if angle <= 45.0 else angle - 90.0


def tilt_class(c: Fraction, s: Fraction) -> str:
    """``upright`` where ``c*s = 0`` exactly; else tilted beyond a degree, or near upright."""
    if c * s == 0:
        return "upright"
    return "tilted" if abs(signed_tilt(c, s)) >= 1.0 else "near-upright"


def tilts(packing: Measured) -> dict[str, Any]:
    """How many squares turn, by class and by the sign of their tilt."""
    squares = packing[1]
    tilted = [signed_tilt(c, s) for _x, _y, c, s in squares if tilt_class(c, s) == "tilted"]
    near = sorted(
        signed_tilt(c, s) for _x, _y, c, s in squares if tilt_class(c, s) == "near-upright"
    )
    return {
        "exactly_turned": sum(1 for _x, _y, c, s in squares if c * s != 0),
        "tilted_beyond_1_degree": len(tilted),
        "tilted_positive": sum(1 for t in tilted if t > 0),
        "tilted_negative": sum(1 for t in tilted if t < 0),
        "tilt_range_degrees": [min(map(abs, tilted)), max(map(abs, tilted))] if tilted else [],
        "near_upright": len(near),
        "near_upright_beyond_1e-3_degrees": [t for t in near if abs(t) > 1e-3],
    }


def bands(first: Measured, second: Measured) -> dict[str, Any]:
    """How the first packing's tilted squares pair, by sign, under the identity assignment."""
    a = _centres(first[1])
    b = _centres(second[1])
    cost = ((a[:, None, :] - b[None, :, :]) ** 2).sum(axis=2)
    rows, cols = linear_sum_assignment(cost)
    moves = np.sqrt(cost[rows, cols])
    same = flipped = to_other = same_within = flipped_beyond = 0
    for i, j, move in zip(rows, cols, moves, strict=True):
        c, s = first[1][i][2], first[1][i][3]
        if tilt_class(c, s) != "tilted":
            continue
        cc, ss = second[1][j][2], second[1][j][3]
        if tilt_class(cc, ss) != "tilted":
            to_other += 1
            continue
        if signed_tilt(c, s) * signed_tilt(cc, ss) > 0:
            same += 1
            same_within += int(move <= 0.1)
        else:
            flipped += 1
            flipped_beyond += int(move > 0.1)
    ours = [signed_tilt(c, s) for _x, _y, c, s in first[1] if tilt_class(c, s) == "tilted"]
    theirs = [signed_tilt(c, s) for _x, _y, c, s in second[1] if tilt_class(c, s) == "tilted"]
    shared = sum(1 for t in ours if any(abs(t - u) < 1e-4 for u in theirs))
    return {
        "assignment": "identity, least total squared centre displacement",
        "tilted_paired_same_sign": same,
        "tilted_paired_same_sign_within_1e-1": same_within,
        "tilted_paired_opposite_sign": flipped,
        "tilted_paired_opposite_sign_beyond_1e-1": flipped_beyond,
        "tilted_paired_with_untilted": to_other,
        "tilt_angles_shared_within_1e-4_degrees": shared,
    }


def bottleneck(distances: np.ndarray) -> float:
    """The least largest move over all assignments: the least distance level at which a
    perfect matching uses only pairs at most that far apart, by binary search."""
    levels = np.unique(distances)
    low, high = 0, len(levels) - 1
    while low < high:
        middle = (low + high) // 2
        matching = maximum_bipartite_matching(
            csr_matrix(distances <= levels[middle]), perm_type="column"
        )
        if bool((matching >= 0).all()):
            high = middle
        else:
            low = middle + 1
    return float(levels[low])


def centred(first: Measured, second: Measured) -> dict[str, Any]:
    """The assignment with the second box centred on the first, as the T-240 review read it."""
    side, left = first
    other_side, right = second
    shift = (side - other_side) / 2
    a = _centres(left)
    trials: list[tuple[float, int, list[Placed], np.ndarray, np.ndarray]] = []
    for k in range(SYMMETRIES):
        mapped = [
            (u + shift, v + shift, p, q)
            for u, v, p, q in (area.symmetric(other_side, square, k) for square in right)
        ]
        b = _centres(mapped)
        cost = ((a[:, None, :] - b[None, :, :]) ** 2).sum(axis=2)
        rows, cols = linear_sum_assignment(cost)
        order = np.empty(len(rows), dtype=int)
        order[rows] = cols
        trials.append((float(cost[rows, cols].sum()), k, mapped, cost, order))
    trials.sort(key=lambda trial: (trial[0], trial[1]))
    total, k, mapped, cost, order = trials[0]
    distances = np.sqrt(cost)
    moves = distances[np.arange(len(left)), order]
    turned = reversed_tilts = 0
    for i, j in enumerate(order.tolist()):
        mine, theirs = left[i], mapped[j]
        sine = float(_turn_sine(mine, theirs))
        turned += int(math.degrees(math.asin(min(1.0, sine))) > 1.0)
        here, there = signed_tilt(mine[2], mine[3]), signed_tilt(theirs[2], theirs[3])
        reversed_tilts += int(
            abs(here) > 1.0 and abs(there) > 1.0 and (here > 0) != (there > 0)
        )
    nearest = distances.argmin(axis=1)
    return {
        "alignment": "box centres",
        "symmetry": k,
        "total_squared": f"{total:.6g}",
        "runner_up_symmetry": trials[1][1],
        "runner_up_total_squared": f"{trials[1][0]:.6g}",
        "largest_move": f"{float(moves.max()):.6g}",
        "rms_move": f"{float(np.sqrt((moves**2).mean())):.6g}",
        "bottleneck": f"{bottleneck(distances):.6g}",
        "moved_beyond": {bound: int((moves > float(bound)).sum()) for bound in BOUNDS},
        "nearest_one_to_one": len(set(nearest.tolist())) == len(left),
        "turned_beyond_1_degree": turned,
        "tilts_reversed_beyond_1_degree": reversed_tilts,
    }


def compare(view: Packing, against: Packing) -> dict[str, Any]:
    """Every measure of one pair, the view first."""
    if len(view.squares) != len(against.squares):
        raise MeasureError(
            f"{view.label} has {len(view.squares)} squares, {against.label} "
            f"{len(against.squares)}"
        )
    first, second = view.measured, against.measured
    return {
        "view": view.label,
        "against": against.label,
        **measure(first, second),
        "bands": bands(first, second),
        "centred": centred(first, second),
    }


def receipt(n: int, view: Packing, others: list[Packing]) -> dict[str, Any]:
    """The receipt of one view measured against each other packing."""
    labels = [view.label, *(other.label for other in others)]
    if len(set(labels)) != len(labels):
        raise MeasureError("two inputs share a label")
    if not others:
        raise MeasureError("nothing to measure the view against")
    return {
        "format": FORMAT,
        "n": n,
        "inputs": {
            packing.label: {**packing.source, "side": str(packing.side)}
            for packing in (view, *others)
        },
        "tilts": {packing.label: tilts(packing.measured) for packing in (view, *others)},
        "pairs": [compare(view, other) for other in others],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--n", type=int, required=True, help="the count of both packings")
    parser.add_argument("view", help="the packing measured, [LABEL=]KIND:TARGET")
    parser.add_argument("against", nargs="+", help="the packings it is measured against")
    parser.add_argument("--out", type=Path, help="where to write the receipt as well")
    args = parser.parse_args(argv)
    try:
        view = read_packing(args.view, args.n)
        others = [read_packing(spec, args.n) for spec in args.against]
        result = receipt(args.n, view, others)
    except MeasureError as error:
        sys.stderr.write(f"measure_identity: {error}\n")
        return 2
    text = json.dumps(result, indent=1) + "\n"
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
