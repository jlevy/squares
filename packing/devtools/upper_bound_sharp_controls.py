"""Sharp controls on an import's certificate, through both maintained exact routes.

The controls of ``devtools.upper_bound_reports certify`` are gross: a duplicated square,
gap -1, and a square moved the side and 2 outside the box, which a route with a tolerance
of 1e-8 refuses as surely as an exact one. An import's certificate often clears its walls
and pairs by less than the binary64 spacing of its coordinates (5e-21 and about 1e-20 at
#719's 204, a dilation's 6e-13 at #755's 303), so a route rounding at binary64 or
tolerating 1e-15 would pass it as retained. These controls go to exact contact and
`EPSILON` (1e-30) past it, so the receipt shows each route meets the certificate's scale.
Three packets wrote them as programs of their own (mishapolk-n204-2026-10-22's
``receipts/sharp_controls.py``, amundsk-n303-2026-10-23's ``replay/sharp_controls.py``
and evand-kaggle-descents-2026-10-24's), and the T-240 review's clean-room checker
(couzo-issue763-2026-10-23, ``review/review-2026-10-24/check_certificates.py``) added the
enlarged squares; this module is them once (OR-1), and the retained programs stay as
they were written, since their receipts are bound to them.

Each control is built exactly from the certificate and decided by ``sqpack``'s exact
verifier and the independent rational corner checker, through the entry points the
kernel's own jobs use (`kernel.to_witness`, `legacy.exact_verify`,
`legacy.independent.check_squares`):

- ``side-lowered-past-wall-contact`` (`kernel.sharp_input`): the box lowered to the
  packing's extent, its least top or right corner clearance; at contact the box at its
  extent is accepted, and past it, 1e-30 below the extent, refused;
- ``tightest-pair-closed-past-contact`` (`kernel.sharp_input`): the second square of the
  least-gap pair moved along the face normal that closes it, by the gap: exact contact
  accepted, 1e-30 past it refused;
- ``squares-moved-past-near-wall-contact``: every square translated toward the near
  wall, left or bottom, whichever is closer, by the least near-wall clearance, as the 22
  October review of T-229 moved its squares;
- ``square-enlarged-past-pair-contact``: one square of a tight pair enlarged about its
  centre until it touches its partner, and 1e-30 past that (`enlarged_pair`);
- ``square-enlarged-past-wall-contact``: the square nearest a wall enlarged until a
  corner meets the wall, and 1e-30 past it (`enlarged_wall`);
- ``duplicate-square``: square 2 replaced by a copy of square 1 (`kernel.job_input`), the
  one gross control, whose verdict the original certificate's acceptance flips.

At contact both routes must accept with the decisive margin exactly 0, and past it refuse
with it exactly -1e-30, each route naming only the failure the control makes. An enlarged
square is no unit square, so both routes refuse it at contact as well, for its shape
alone, with the margin exactly 0; past contact they also find the overlap or the wall.
The routes measure along each square's edge normals unnormalized, so on the enlarged
square's own normals a pair margin reads the geometric one times its edge: past contact
the pair margin lies between -1e-30 times that edge and -1e-30 (`window`). An enlargement
is chosen to close its one pair or wall alone (``clean``); in a certificate whose squares
touch exactly none can, and the tightest pair's square, or the square nearest a wall, is
enlarged anyway. Its gap is then 0, so at contact it is the certificate itself, accepted,
and past contact the failures it must make are decided exactly beforehand
(`predicted_failures`), the pair margin held to at most -1e-30 (``margin_rule``).

Where the packet's replayed roster is one count the receipt is
``receipts/sharp-controls.json``; otherwise one ``receipts/sharp-controls-nNNN.json`` per
count. The command decides nothing about the certificate itself.

From ``packing/``, with the project interpreter::

    python -m devtools.upper_bound_reports PACKET sharp-controls [--n N ...] [--check]

``--check`` decides every control again and holds the retained receipt to it, every field
but the measured times.
"""

from __future__ import annotations

import json
import time
from collections.abc import Collection, Sequence
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools import upper_bound_reports as reports

FORMAT = "upper-bound-sharp-controls-v1"
EPSILON = kernel.SHARP_EPSILON
ROUTES = kernel.ROUTES
SIDE_LOWERED, TIGHTEST_PAIR = kernel.SHARP_CONTROLS
NEAR_WALL = "squares-moved-past-near-wall-contact"
ENLARGED_PAIR = "square-enlarged-past-pair-contact"
ENLARGED_WALL = "square-enlarged-past-wall-contact"
DUPLICATE = "duplicate-square"
CONTROLS = (SIDE_LOWERED, TIGHTEST_PAIR, NEAR_WALL, ENLARGED_PAIR, ENLARGED_WALL, DUPLICATE)
#: The control each failure is the work of, as the routes name their failures.
SHAPE, CONTAINER, OVERLAP = "shape", "container", "overlap"
#: How many of the tightest pairs, or the squares nearest a wall, an enlargement tries
#: before it refuses: it takes the first whose enlargement closes nothing else.
CANDIDATES = 64
#: How a route's margin is held to the expected one: exactly; within `window`, where an
#: enlarged square's own normals are read; or at most it, where an enlargement that has
#: to close more than its pair (a certificate whose squares touch exactly) may close
#: another by more.
EQUAL, WINDOW, AT_MOST = "equal", "window", "at most"

type Point = tuple[Fraction, Fraction]
type Square = list[Point]
type Verdicts = dict[str, dict[str, Any]]


def receipt_path(packet: Path, roster: Collection[int], n: int) -> Path:
    """``receipts/sharp-controls.json`` for a roster of one count, else one per count."""
    name = "sharp-controls.json" if len(roster) == 1 else f"sharp-controls-n{n:03d}.json"
    return packet / "receipts" / name


# --------------------------------------------------------------------------- the routes


def failure_kinds(route: str, failures: Sequence[Any]) -> list[str]:
    """The kinds of failure a route names: ``shape``, ``container`` or ``overlap``."""
    kinds: set[str] = set()
    for failure in failures:
        if route == "exact_verify":
            kinds.add(str(failure[0]))
        elif str(failure).startswith("square "):
            kinds.add(SHAPE)
        elif str(failure).startswith("container"):
            kinds.add(CONTAINER)
        elif "overlapping pairs" in str(failure):
            kinds.add(OVERLAP)
        else:
            raise reports.ReportError(
                f"an independent route failure of no known kind: {failure}"
            )
    unknown = kinds - {SHAPE, CONTAINER, OVERLAP}
    if unknown:
        raise reports.ReportError(f"route failures of no known kind: {sorted(unknown)}")
    return sorted(kinds)


def _verdicts(first: dict[str, Any], second: dict[str, Any]) -> Verdicts:
    return {
        route: {
            "passed": bool(verdict["verification_passed"]),
            "wall": legacy.literal(Fraction(str(verdict["minimum_containment_clearance"]))),
            "gap": legacy.literal(Fraction(str(verdict["minimum_best_pair_gap"]))),
            "failures": failure_kinds(route, verdict["failures"]),
        }
        for route, verdict in (("exact_verify", first), ("independent", second))
    }


def decide(certificate: legacy.Certificate, profile: dict[str, str]) -> Verdicts:
    """Both routes on a certificate of unit squares, as `kernel.run_sharp` decides one."""
    first, _report = legacy.exact_verify(kernel.to_witness(certificate, **profile))
    second = legacy.independent.check_squares(
        legacy.corner_squares(certificate), certificate.side
    )
    return _verdicts(first, second)


def decide_corners(
    certificate: legacy.Certificate, squares: list[Square], profile: dict[str, str]
) -> Verdicts:
    """Both routes on squares given by their corners, which need not be unit squares."""
    witness = kernel.to_witness(certificate, **profile)
    witness["representation"] = "corners"
    witness["squares"] = [
        {
            "id": index,
            "corners": [[legacy.literal(x), legacy.literal(y)] for x, y in square],
        }
        for index, square in enumerate(squares, start=1)
    ]
    first, _report = legacy.exact_verify(witness)
    second = legacy.independent.check_squares(squares, certificate.side)
    return _verdicts(first, second)


# --------------------------------------------------------------------------- the controls


def near_wall(certificate: legacy.Certificate, *, past: bool) -> legacy.Certificate:
    """Every square moved toward the closer near wall by its least clearance, and past."""
    corners = legacy.corner_squares(certificate)
    left = min(x for square in corners for x, _y in square)
    bottom = min(y for square in corners for _x, y in square)
    step = min(left, bottom) + (EPSILON if past else Fraction(0))
    dx, dy = (step, Fraction(0)) if left <= bottom else (Fraction(0), step)
    poses = tuple(replace(pose, x=pose.x - dx, y=pose.y - dy) for pose in certificate.poses)
    return replace(certificate, poses=poses)


def enlarge(pose: legacy.Pose, delta: Fraction) -> Square:
    """The square of ``pose`` with its half-edge grown by ``delta`` about its centre."""
    scale = 1 + 2 * delta
    return [
        (pose.x + scale * (x - pose.x), pose.y + scale * (y - pose.y))
        for x, y in pose.corners()
    ]


def _dot(point: Point, axis: Point) -> Fraction:
    return point[0] * axis[0] + point[1] * axis[1]


def _normals(pose: legacy.Pose) -> tuple[Point, Point]:
    """The unit normals of the square's edges, its basis and the basis turned."""
    c, s = pose.basis
    return (c, s), (-s, c)


def _wall_clearance(square: Square, side: Fraction) -> Fraction:
    return min(min(x, y, side - x, side - y) for x, y in square)


def contact_enlargement(grown: legacy.Pose, other: legacy.Pose, excess: Fraction) -> Fraction:
    """How far ``grown``'s half-edge grows before the pair's gap is ``-excess``, exactly.

    On a unit normal ``w`` of either square the pair is separated by ``g_w``, and growing
    ``grown``'s half-edge by ``d`` widens its shadow on ``w`` by ``d * r_w``, where
    ``r_w = |w.u| + |w.v|`` over ``grown``'s edge directions, so the gap there is
    ``g_w - d * r_w``. The pair's gap, the largest of these, is ``-excess`` at
    ``d = max_w (g_w + excess) / r_w``.
    """
    mine, theirs = grown.corners(), other.corners()
    u, v = _normals(grown)
    growth = Fraction(0)
    for axis in (*_normals(grown), *_normals(other)):
        lo, hi = min(_dot(p, axis) for p in mine), max(_dot(p, axis) for p in mine)
        other_lo = min(_dot(p, axis) for p in theirs)
        other_hi = max(_dot(p, axis) for p in theirs)
        gap = max(other_lo - hi, lo - other_hi)
        rate = abs(_dot(axis, u)) + abs(_dot(axis, v))
        growth = max(growth, (gap + excess) / rate)
    return growth


def _clear_of_others(
    certificate: legacy.Certificate, squares: list[Square], index: int, exempt: int | None
) -> bool:
    """Whether square ``index`` keeps every other pair it is in apart and stays in the box."""
    square = squares[index]
    return _wall_clearance(square, certificate.side) >= 0 and all(
        legacy.independent.pair_gap(square, other) > 0
        for other_index, other in enumerate(squares)
        if other_index not in {index, exempt}
    )


def tight_pairs(certificate: legacy.Certificate) -> list[tuple[Fraction, int, int]]:
    """Every pair within the circumscribed discs' reach, by gap and then index, as
    `legacy.tightest_pair` reads the pairs."""
    squares = legacy.corner_squares(certificate)
    poses = certificate.poses
    return sorted(
        (legacy.independent.pair_gap(squares[i], squares[j]), i, j)
        for i in range(certificate.n)
        for j in range(i + 1, certificate.n)
        if (poses[i].x - poses[j].x) ** 2 + (poses[i].y - poses[j].y) ** 2 <= 2
    )


def enlarged_pair(certificate: legacy.Certificate) -> dict[str, Any]:
    """A tight pair's square to enlarge past contact, preferring one that closes it alone.

    Over the pairs in `tight_pairs` order, the second square and then the first is grown
    by `contact_enlargement` with ``excess`` `EPSILON`, and the first whose grown square
    keeps every other pair apart and stays in the box is taken (``clean``). Where none of
    the first `CANDIDATES` pairs has one, as in a certificate whose squares touch exactly,
    the tightest pair's second square is taken, as the T-240 review took it. Returned: the
    square, its partner, the pair's gap, the growth at contact and past it, and ``clean``.
    """
    squares = legacy.corner_squares(certificate)
    pairs = tight_pairs(certificate)
    if not pairs:
        raise reports.ReportError("no pair of squares lies within the discs' reach")
    poses = certificate.poses
    chosen: tuple[Fraction, int, int, bool] | None = None
    for gap, i, j in pairs[:CANDIDATES]:
        for grown, other in ((j, i), (i, j)):
            trial = [*squares]
            trial[grown] = enlarge(
                poses[grown], contact_enlargement(poses[grown], poses[other], EPSILON)
            )
            if _clear_of_others(certificate, trial, grown, other):
                chosen = (gap, grown, other, True)
                break
        if chosen is not None:
            break
    if chosen is None:
        gap, i, j = pairs[0]
        chosen = (gap, j, i, False)
    gap, grown, other, clean = chosen
    return {
        "square": grown,
        "partner": other,
        "gap": gap,
        "at": contact_enlargement(poses[grown], poses[other], Fraction(0)),
        "past": contact_enlargement(poses[grown], poses[other], EPSILON),
        "clean": clean,
    }


def enlarged_wall(certificate: legacy.Certificate) -> dict[str, Any]:
    """A square near a wall to enlarge past it, preferring one that closes no pair.

    A square's corners reach out by ``(|c| + |s|) / 2`` from its centre on each axis, so
    growing its half-edge by ``d`` brings each corner ``d * (|c| + |s|)`` nearer the walls:
    its clearance ``w`` is closed at ``d = w / (|c| + |s|)`` and passed by `EPSILON` at
    ``(w + EPSILON) / (|c| + |s|)``. Over the squares by clearance and then index, the
    first whose grown square keeps every pair it is in apart is taken (``clean``); where
    none of the first `CANDIDATES` has one, the square nearest a wall is.
    """
    squares = legacy.corner_squares(certificate)
    order = sorted(
        (_wall_clearance(square, certificate.side), index)
        for index, square in enumerate(squares)
    )

    def growth(clearance: Fraction, index: int, excess: Fraction) -> Fraction:
        c, s = certificate.poses[index].basis
        return (clearance + excess) / (abs(c) + abs(s))

    chosen: tuple[Fraction, int, bool] | None = None
    for clearance, index in order[:CANDIDATES]:
        trial = [*squares]
        trial[index] = enlarge(certificate.poses[index], growth(clearance, index, EPSILON))
        if all(
            legacy.independent.pair_gap(trial[index], other) > 0
            for other_index, other in enumerate(trial)
            if other_index != index
        ):
            chosen = (clearance, index, True)
            break
    if chosen is None:
        clearance, index = order[0]
        chosen = (clearance, index, False)
    clearance, index, clean = chosen
    return {
        "square": index,
        "clearance": clearance,
        "at": growth(clearance, index, Fraction(0)),
        "past": growth(clearance, index, EPSILON),
        "clean": clean,
    }


def predicted_failures(
    squares: list[Square], index: int, growth: Fraction, side: Fraction
) -> list[str]:
    """What the routes must name once square ``index`` has grown by ``growth``, decided
    exactly: its shape where it grew, the wall where it crosses one, an overlap where it
    meets another square. The certificate's other pairs and walls are as it states them."""
    kinds: set[str] = set()
    if growth > 0:
        kinds.add(SHAPE)
    if _wall_clearance(squares[index], side) < 0:
        kinds.add(CONTAINER)
    if any(
        legacy.independent.pair_gap(squares[index], other) < 0
        for other_index, other in enumerate(squares)
        if other_index != index
    ):
        kinds.add(OVERLAP)
    return sorted(kinds)


def window(margin: Fraction, edge: Fraction) -> bool:
    """Whether a pair margin read past contact is -`EPSILON` on a unit normal or on the
    enlarged square's own, whose length is its ``edge``, or a value between them."""
    return -EPSILON * edge <= margin <= -EPSILON


# --------------------------------------------------------------------------- one receipt


def margin_met(margin: Fraction, expected: Fraction, rule: str, edge: Fraction) -> bool:
    """A route's margin held to its control's rule: ``equal``, ``window`` (`window`, with
    the enlarged square's ``edge``) or ``at most``."""
    if rule == EQUAL:
        return margin == expected
    if rule == WINDOW:
        return window(margin, edge)
    if rule == AT_MOST:
        return margin <= expected
    raise reports.ReportError(f"unknown margin rule {rule!r}")


def _row(
    control: str,
    where: str,
    margin: str,
    *,
    verdicts: Verdicts,
    failures: list[str],
    expected_margin: Fraction,
    detail: dict[str, Any],
    started: float,
    rule: str = EQUAL,
    edge: Fraction = Fraction(1),
) -> dict[str, Any]:
    """One control's row. ``as_expected`` holds every route to the verdict the expected
    failures make (accepted where there are none), to those failures, and to the margin
    by its ``rule``."""
    ok = all(
        verdict["passed"] is (not failures)
        and verdict["failures"] == failures
        and margin_met(Fraction(verdict[margin]), expected_margin, rule, edge)
        for verdict in verdicts.values()
    )
    return {
        "control": control,
        "where": where,
        "margin": margin,
        "expected_margin": legacy.literal(expected_margin),
        "margin_rule": rule,
        "expected": "refused" if failures else "accepted",
        "expected_failures": failures,
        "detail": {
            key: legacy.literal(value) if isinstance(value, Fraction) else value
            for key, value in detail.items()
        },
        "routes": verdicts,
        "as_expected": ok,
        "cpu_seconds": round(time.process_time() - started, 3),
    }


def _square(index: int) -> int:
    """The witness's 1-based square number."""
    return index + 1


def control_rows(
    certificate: legacy.Certificate, profile: dict[str, str]
) -> list[dict[str, Any]]:
    """Every control at contact and past it, and the duplicate square, decided."""
    rows: list[dict[str, Any]] = []
    left, right, gap, _normal = legacy.tightest_pair(certificate)
    corners = legacy.corner_squares(certificate)
    near = min(min(x, y) for square in corners for x, y in square)
    clearance = legacy.top_clearance(certificate)
    pair = enlarged_pair(certificate)
    wall = enlarged_wall(certificate)
    for past in (False, True):
        where = "past-contact" if past else "at-contact"
        excess = EPSILON if past else Fraction(0)
        expect = -EPSILON if past else Fraction(0)
        for control, margin, kind, detail in (
            (SIDE_LOWERED, "wall", CONTAINER, {"lowered_by": clearance + excess}),
            (
                TIGHTEST_PAIR,
                "gap",
                OVERLAP,
                {"square": _square(right), "partner": _square(left), "moved_by": gap + excess},
            ),
            (NEAR_WALL, "wall", CONTAINER, {"moved_by": near + excess}),
        ):
            started = time.process_time()
            if control == NEAR_WALL:
                actual = near_wall(certificate, past=past)
            else:
                actual = kernel.sharp_input(certificate, control, past=past)
            rows.append(
                _row(
                    control,
                    where,
                    margin,
                    verdicts=decide(actual, profile),
                    failures=[kind] if past else [],
                    expected_margin=expect,
                    detail=detail,
                    started=started,
                )
            )
        for control, margin, found in (
            (ENLARGED_PAIR, "gap", pair),
            (ENLARGED_WALL, "wall", wall),
        ):
            started = time.process_time()
            growth = found["past" if past else "at"]
            index = found["square"]
            squares = [*corners]
            squares[index] = enlarge(certificate.poses[index], growth)
            failures = predicted_failures(squares, index, growth, certificate.side)
            edge = 1 + 2 * growth
            if control == ENLARGED_WALL:
                rule = EQUAL
                expected_margin = min(
                    _wall_clearance(square, certificate.side) for square in squares
                )
                detail = {"wall_clearance": found["clearance"]}
            else:
                if OVERLAP not in failures:
                    rule = EQUAL
                elif found["clean"]:
                    rule = WINDOW
                else:
                    rule = AT_MOST
                expected_margin = expect
                detail = {"partner": _square(found["partner"]), "pair_gap": found["gap"]}
            rows.append(
                _row(
                    control,
                    where,
                    margin,
                    verdicts=decide_corners(certificate, squares, profile),
                    failures=failures,
                    expected_margin=expected_margin,
                    detail={
                        "square": _square(index),
                        **detail,
                        "half_edge_grown_by": growth,
                        "edge": edge,
                        "clean": found["clean"],
                    },
                    started=started,
                    rule=rule,
                    edge=edge,
                )
            )
    started = time.process_time()
    duplicate = kernel.job_input(certificate, "duplicate-square-overlap")
    rows.append(
        _row(
            DUPLICATE,
            "gross",
            "gap",
            verdicts=decide(duplicate, profile),
            failures=[OVERLAP],
            expected_margin=Fraction(-1),
            detail={"square": _square(1), "copy_of": _square(0)},
            started=started,
        )
    )
    # Each control at contact, then past it, in the order of `CONTROLS`.
    rows.sort(key=lambda row: (CONTROLS.index(row["control"]), row["where"] == "past-contact"))
    return rows


def certificate_path(packet: Path, row: reports.CertificateRow) -> str:
    """The certificate the row names, repository-relative: its derived fact, or its file."""
    if "fact" in row:
        path = packet / row["fact"]
    else:
        path = reports.REPO / reports.acquisition(packet)["archived_path"] / row["path"]
    return path.resolve().relative_to(reports.REPO.resolve()).as_posix()


def sharp_controls(packet: Path, n: int) -> dict[str, Any]:
    """The receipt of every control on the packet's certificate at ``n``."""
    declaration = reports.load_declaration(packet)
    rows = [row for row in declaration["certificates"] if row["n"] == n]
    if len(rows) != 1:
        raise reports.ReportError(f"the packet declares no single certificate at n={n}")
    certificate = reports.read_facts(packet, {n})[n]
    profile = {
        "witness_prefix": declaration["witness_prefix"],
        "claim_limitations": declaration["claim_limitations"],
    }
    controls = control_rows(certificate, profile)
    return {
        "format": FORMAT,
        "packet": packet.name,
        "n": n,
        "certificate": certificate_path(packet, rows[0]),
        "side": legacy.literal(certificate.side),
        "epsilon": legacy.literal(EPSILON),
        "routes": list(ROUTES),
        "controls": controls,
        "all_as_expected": all(row["as_expected"] for row in controls),
    }


def _untimed(record: dict[str, Any]) -> dict[str, Any]:
    return {
        **record,
        "controls": [
            {key: value for key, value in row.items() if key != "cpu_seconds"}
            for row in record["controls"]
        ],
    }


def run(packet: Path, numbers: Collection[int] | None, *, check: bool) -> dict[int, bool]:
    """Write, or with ``check`` hold to its retained copy, each count's receipt."""
    roster = reports.load_declaration(packet)["replayed"]
    chosen = list(roster) if numbers is None else list(numbers)
    if not chosen or not set(chosen) <= set(roster):
        raise reports.ReportError(f"counts outside the replayed roster {roster}: {chosen}")
    results: dict[int, bool] = {}
    for n in chosen:
        path = receipt_path(packet, roster, n)
        reports.ensure_private(path)
        retained = json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
        if retained is not None and retained.get("format") != FORMAT:
            # A packet's own program wrote it, and its receipt stays bound to that program.
            raise reports.ReportError(f"{path.name} is another program's receipt; it stays")
        if check and retained is None:
            raise reports.ReportError(f"no retained {path.name} to check")
        record = sharp_controls(packet, n)
        if check:
            if retained is None or _untimed(retained) != _untimed(record):
                raise reports.ReportError(
                    f"{path.name} differs from the controls decided again"
                )
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
        results[n] = record["all_as_expected"]
    return results
