#!/usr/bin/env python3
"""Decide PR #622's s(29) certificate over Q, apart from the routes that replayed it.

A stage 4 review program (packing/campaign/result-import.md, "The review"). It reads the
release asset by member name with ``zipfile`` and extracts nothing. It reads the
certificate, the native corners witness and the baseline certificates as data, and never
imports or runs a program of the source's, of this repository's or of the replay's. It was
written from the geometry statement in the asset's ``README.txt`` and the JSON layout of
the certificate. Standard library only; every decision is made in ``fractions.Fraction``.
Run it with ``python3.14 -I``.

The mathematics. A pose ``(x, y, t)`` is the closed unit square with centre ``(x, y)`` and
unit axes ``u = (c, s)`` and ``v = (-s, c)``, where ``c = (1 - t^2)/(1 + t^2)`` and
``s = 2t/(1 + t^2)``, so that ``c^2 + s^2 = 1`` over Q; its corners are
``(x, y) + (a u + b v)/2`` for ``a, b`` in ``{-1, 1}``. The square lies in ``[0, S]^2``
exactly when its four corners do, since both are convex. Two such squares have disjoint
interiors exactly when one of the four axes ``u_i, v_i, u_j, v_j`` weakly separates them,
that is when the projections of their corners onto it overlap in at most a point: the
difference body ``Q_i - Q_j`` is a polygon whose edge normals are those axes, and the
interiors meet exactly when 0 lies in its interior. A projection's extremes are at
corners. So the checks below are both sound and complete for this certificate's claim:
29 closed unit squares with pairwise disjoint interiors inside a square of side ``S``,
hence ``s(29) <= S``.

Subcommands, each printing one JSON object:

``certificate ASSET [--member M]``
    the asset's and the member's digests, a strict parse, and every wall and every pair
    decided exactly, with the exact contacts and the least positive clearances.
``controls ASSET``
    mutated copies of the certificate, each decided in full, with the violations that
    refuse it held to the violations its mutation should cause and no others: the two
    gross mutations the replay ran (a duplicated square, a square moved out of the box)
    and tight ones at the exact contacts (a touching pair pushed together, and the box
    shrunk, each by 10^-3000).
``fact ASSET FACT``
    the replay's derived fact (``facts/n-029.yaml.gz``) equal to the certificate, side,
    centre and axis, square for square, read by a strict line reader of its layout.
``native ASSET``
    the source's corners witness equal to the corners computed here, as sets per square.
``sides ASSET REPO``
    the side against the record's comparators at 29 and the source's baselines, exactly,
    and against T-009's Krawczyk enclosure of the catalogue's own contact system.
``identity ASSET REPO``
    the certificate measured against T-009's witness, T-155's view and the house witness:
    the register's identity measurement (one to one by nearest centres under the box's
    eight symmetries, squares moved beyond 1e-3, the largest move and turn), in floats of
    exact differences. It measures and decides nothing.
``receipt ASSET RECEIPT``
    each job the replay retained (``receipts/exact-certification.json.xz``) decided again
    from its own checker input: the positive held to the certificate, each control held
    to the mutation it should be and the reason it should be refused for, and each
    route's least gap and clearance held to this program's.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import lzma
import math
import re
import sys
import time
import zipfile
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

ASSET_NAME = "pingyou-n29-certificate-2026-10-15.zip"
ASSET_BYTES = 430075
ASSET_SHA256 = "0dc9bcd1cf5f2806a4d2e0c4c1c07e4903d91bbea611b8b938bda770b9782537"
CERT_MEMBER = "n29-certificate/certificates/n029.cert.json"
CERT_SHA256 = "a01428c51875679fbe78c11a803742b8d99f44b916a660ab6801bb0fcf76951b"
NATIVE_MEMBER = "n29-certificate/native/pingyou-20261015-n29-rational.yaml"
NATIVE_SHA256 = "0eff5b4d2a9701e30fe8912fd634c5a7124384366197533c18a5bcc26dfe4a39"
BASELINES = {
    "pr574-v2": "n29-certificate/baselines/pr574-v2-n029.cert.json",
    "pr549": "n29-certificate/baselines/pr549-n029.cert.json",
    "evan": "n29-certificate/baselines/evan-n029.cert.json",
}
N = 29
# One unit of a scale far below the certificate's own: its coordinates have denominators
# of about 2,400 digits, so a move of 10^-3000 is invisible at any precision short of exact.
TIGHT = Fraction(1, 10**3000)
#: The move thresholds the identity counts squares beyond.
THRESHOLDS = ("1e-3", "1e-9", "1e-30")
RATIONAL = re.compile(r"-?[0-9]+(?:/[0-9]+)?")
DECIMAL = re.compile(r"-?[0-9]+(?:\.[0-9]+)?")

type Point = tuple[Fraction, Fraction]


class ReviewError(Exception):
    """A premise failed: a digest, the layout, or a value's lexical form."""


@dataclass(frozen=True)
class Pose:
    x: Fraction
    y: Fraction
    t: Fraction


@dataclass(frozen=True)
class Square:
    centre: Point
    u: Point
    v: Point
    corners: tuple[Point, Point, Point, Point]


@dataclass(frozen=True)
class Decision:
    walls: list[tuple[int, str, Fraction]]
    pairs: list[tuple[int, int, Fraction, str]]
    cpu_s: float

    @property
    def violations(self) -> list[str]:
        out = [f"wall {k} {w}" for k, w, c in self.walls if c < 0]
        out += [f"pair {i} {j}" for i, j, g, _ in self.pairs if g < 0]
        return out


def rational(text: object, what: str) -> Fraction:
    """A value written as an integer or a fraction of integers, and nothing else."""
    if not isinstance(text, str) or not RATIONAL.fullmatch(text):
        raise ReviewError(f"{what}: not an integer or a fraction of integers")
    num, _, den = text.partition("/")
    if den and int(den) == 0:
        raise ReviewError(f"{what}: zero denominator")
    return Fraction(int(num), int(den) if den else 1)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def open_asset(path: Path) -> zipfile.ZipFile:
    data = path.read_bytes()
    if len(data) != ASSET_BYTES or sha256(data) != ASSET_SHA256:
        raise ReviewError(f"{path}: not the pinned asset ({len(data)} bytes, {sha256(data)})")
    return zipfile.ZipFile(path)


def member(asset: zipfile.ZipFile, name: str, digest: str | None = None) -> bytes:
    data = asset.read(name)
    if digest is not None and sha256(data) != digest:
        raise ReviewError(f"{name}: SHA-256 {sha256(data)}, not {digest}")
    return data


def read_certificate(data: bytes, what: str) -> tuple[Fraction, list[Pose]]:
    """The side and the poses of a certificate, held to its layout strictly."""
    record = json.loads(data)
    if not isinstance(record, dict) or record.get("n") != N:
        raise ReviewError(f"{what}: n is not {N}")
    squares = record.get("squares")
    if not isinstance(squares, list) or len(squares) != N:
        raise ReviewError(f"{what}: not {N} squares")
    side = rational(record.get("s_exact"), f"{what} s_exact")
    poses = []
    for k, row in enumerate(squares):
        if not isinstance(row, list) or len(row) != 3:
            raise ReviewError(f"{what} square {k}: not [x, y, t]")
        x, y, t = (rational(v, f"{what} square {k}") for v in row)
        poses.append(Pose(x, y, t))
    return side, poses


def axes(t: Fraction) -> tuple[Point, Point]:
    d = 1 + t * t
    c, s = (1 - t * t) / d, 2 * t / d
    if c * c + s * s != 1:
        raise ReviewError("an axis is not a unit vector")
    return (c, s), (-s, c)


def square(pose: Pose) -> Square:
    u, v = axes(pose.t)
    corners = tuple(
        (pose.x + (a * u[0] + b * v[0]) / 2, pose.y + (a * u[1] + b * v[1]) / 2)
        for a in (-1, 1)
        for b in (-1, 1)
    )
    assert len(corners) == 4
    return Square((pose.x, pose.y), u, v, (corners[0], corners[1], corners[2], corners[3]))


def clearances(q: Square, side: Fraction) -> dict[str, Fraction]:
    xs = [x for x, _ in q.corners]
    ys = [y for _, y in q.corners]
    return {"left": min(xs), "bottom": min(ys), "right": side - max(xs), "top": side - max(ys)}


def gap(p: Square, q: Square) -> tuple[Fraction, str]:
    """The widest weak separation of two squares along their four axes, and its axis.

    Non-negative exactly when the interiors are disjoint; zero when they touch.
    """
    best: tuple[Fraction, str] | None = None
    for name, (a, b) in (("i.u", p.u), ("i.v", p.v), ("j.u", q.u), ("j.v", q.v)):
        pi = [a * x + b * y for x, y in p.corners]
        pj = [a * x + b * y for x, y in q.corners]
        g = max(min(pj) - max(pi), min(pi) - max(pj))
        if best is None or g > best[0]:
            best = (g, name)
    assert best is not None
    return best


def decide(side: Fraction, poses: list[Pose]) -> Decision:
    start = time.process_time()
    squares = [square(p) for p in poses]
    walls = [(k, w, c) for k, q in enumerate(squares) for w, c in clearances(q, side).items()]
    pairs = []
    for i in range(len(squares)):
        for j in range(i + 1, len(squares)):
            g, axis = gap(squares[i], squares[j])
            pairs.append((i, j, g, axis))
    return Decision(walls, pairs, time.process_time() - start)


def sci(r: Fraction, digits: int = 16) -> str:
    """``r`` in scientific notation, truncated (not rounded) to ``digits`` digits."""
    if r == 0:
        return "0"
    sign, r = ("-" if r < 0 else ""), abs(r)
    e = len(str(r.numerator)) - len(str(r.denominator))
    scale = Fraction(10) ** e
    if r < scale:
        e, scale = e - 1, scale / 10
    mantissa = str(int(r / scale * 10 ** (digits - 1)))
    return f"{sign}{mantissa[0]}.{mantissa[1:]}e{e:+03d}"


def summary(d: Decision) -> dict[str, object]:
    pos_walls = [c for _, _, c in d.walls if c > 0]
    pos_pairs = [g for _, _, g, _ in d.pairs if g > 0]
    return {
        "accepted": not d.violations,
        "walls_decided": len(d.walls),
        "pairs_decided": len(d.pairs),
        "violations": d.violations,
        "touching_walls": [f"{k} {w}" for k, w, c in d.walls if c == 0],
        "touching_pairs": [f"{i} {j} along {a}" for i, j, g, a in d.pairs if g == 0],
        "least_positive_wall_clearance": sci(min(pos_walls)) if pos_walls else None,
        "least_positive_pair_gap": sci(min(pos_pairs)) if pos_pairs else None,
        "cpu_s": round(d.cpu_s, 2),
    }


def cmd_certificate(args: argparse.Namespace) -> dict[str, object]:
    asset = open_asset(args.asset)
    name = args.member
    digest = CERT_SHA256 if name == CERT_MEMBER else None
    data = member(asset, name, digest)
    side, poses = read_certificate(data, name)
    d = decide(side, poses)
    return {
        "asset_sha256": ASSET_SHA256,
        "member": name,
        "member_sha256": sha256(data),
        "n": len(poses),
        "side_digits": [len(str(side.numerator)), len(str(side.denominator))],
        "side_sci": sci(side, 40),
        "axis_aligned": [k for k, p in enumerate(poses) if p.t == 0],
        **summary(d),
    }


def toward(p: Square, q: Square, axis: str) -> Point:
    """The unit axis named by ``gap``, oriented from ``p`` towards ``q``."""
    a, b = {"i.u": p.u, "i.v": p.v, "j.u": q.u, "j.v": q.v}[axis]
    if a * q.centre[0] + b * q.centre[1] < a * p.centre[0] + b * p.centre[1]:
        a, b = -a, -b
    return a, b


def cmd_controls(args: argparse.Namespace) -> dict[str, object]:
    asset = open_asset(args.asset)
    side, poses = read_certificate(member(asset, CERT_MEMBER, CERT_SHA256), CERT_MEMBER)
    base = decide(side, poses)
    if base.violations:
        raise ReviewError("the certificate itself is refused")
    squares = [square(p) for p in poses]
    touching = [(i, j, a) for i, j, g, a in base.pairs if g == 0]
    top_right = sorted({k for k, w, c in base.walls if c == 0 and w in {"top", "right"}})
    controls: list[tuple[str, str, Fraction, list[Pose], list[str]]] = []

    dup = list(poses)
    dup[1] = poses[0]
    controls.append(("duplicate-square", "square 1 := square 0", side, dup, ["pair 0 1"]))

    out = list(poses)
    out[0] = Pose(poses[0].x - 1, poses[0].y, poses[0].t)
    controls.append(
        ("outside-container", "square 0 moved by (-1, 0)", side, out, ["wall 0 left"])
    )

    for i, j, a in touching[:2]:
        da, db = toward(squares[i], squares[j], a)
        pushed = list(poses)
        pushed[j] = Pose(poses[j].x - TIGHT * da, poses[j].y - TIGHT * db, poses[j].t)
        controls.append(
            (
                f"tight-pair-{i}-{j}",
                f"square {j} moved 10^-3000 towards square {i} along their touching axis {a}",
                side,
                pushed,
                [f"pair {i} {j}"],
            )
        )

    expected = [f"wall {k} {w}" for k, w, c in base.walls if c == 0 and w in {"top", "right"}]
    controls.append(
        (
            "tight-box",
            "side reduced by 10^-3000",
            side - TIGHT,
            list(poses),
            expected,
        )
    )

    rows = []
    for name, mutation, s, ps, want in controls:
        d = decide(s, ps)
        got = d.violations
        rows.append(
            {
                "control": name,
                "mutation": mutation,
                "refused": bool(got),
                "violations": got,
                "expected": want,
                "for_the_right_reason": got == want,
                "cpu_s": round(d.cpu_s, 2),
            }
        )
    return {
        "certificate_touching_pairs": [f"{i} {j} along {a}" for i, j, a in touching],
        "certificate_top_right_contacts": top_right,
        "controls": rows,
    }


FACT_SIDE = re.compile(r"  side: (\S+)")


def fact_value(line: str, indent: str) -> str:
    prefix = f"{indent}- "
    if not line.startswith(prefix):
        raise ReviewError(f"fact: expected a list item, found {line[:40]!r}")
    value = line[len(prefix) :]
    if len(value) >= 2 and value[0] == value[-1] == "'":
        value = value[1:-1]
    return value


def read_fact(path: Path) -> tuple[Fraction, list[tuple[int, Point, Point]]]:
    """The side and the squares of the derived fact, by its layout and nothing looser."""
    lines = gzip.decompress(path.read_bytes()).decode().splitlines()
    sides = [m.group(1) for line in lines if (m := FACT_SIDE.fullmatch(line))]
    if len(sides) != 1:
        raise ReviewError("fact: not exactly one side")
    side = rational(sides[0], "fact side")
    start = lines.index("  squares:") + 1
    rows = []
    for k in range(N):
        block = lines[start + 7 * k : start + 7 * k + 7]
        head = f"  - id: {k + 1}"
        if block[0] != head or block[1] != "    center:" or block[4] != "    basis:":
            raise ReviewError(f"fact: block {k} is not the layout read here")
        x, y, b0, b1 = (rational(fact_value(block[i], "    "), "fact") for i in (2, 3, 5, 6))
        rows.append((k + 1, (x, y), (b0, b1)))
    after = lines[start + 7 * N]
    if after.startswith(("  - ", "   ")) or not after.startswith("  "):
        raise ReviewError(f"fact: more than {N} squares, or a layout not read here")
    return side, rows


def cmd_fact(args: argparse.Namespace) -> dict[str, object]:
    asset = open_asset(args.asset)
    side, poses = read_certificate(member(asset, CERT_MEMBER, CERT_SHA256), CERT_MEMBER)
    fside, rows = read_fact(args.fact)
    mismatches = []
    for (ident, centre, basis), pose in zip(rows, poses, strict=True):
        u, _ = axes(pose.t)
        if centre != (pose.x, pose.y):
            mismatches.append(f"id {ident}: centre")
        if basis != u:
            mismatches.append(f"id {ident}: basis")
    return {
        "fact": "packing/resources/web/pingyou-pr622-certificate-2026-10-15/facts/"
        "n-029.yaml.gz",
        "side_equal": fside == side,
        "squares": len(rows),
        "ids": "1 to 29, id k the certificate's square k - 1 (the reader refuses any other)",
        "mismatches": mismatches,
        "equal": fside == side and not mismatches,
    }


def cmd_native(args: argparse.Namespace) -> dict[str, object]:
    asset = open_asset(args.asset)
    side, poses = read_certificate(member(asset, CERT_MEMBER, CERT_SHA256), CERT_MEMBER)
    record = json.loads(member(asset, NATIVE_MEMBER, NATIVE_SHA256))
    witness = record["witness"]
    nside = rational(witness["side"], "native side")
    mismatches = []
    rows = witness["squares"]
    if len(rows) != N:
        raise ReviewError("native: not 29 squares")
    for k, (row, pose) in enumerate(zip(rows, poses, strict=True)):
        if row["id"] != k + 1:
            mismatches.append(f"square {k}: id {row['id']}")
        native = sorted(
            (rational(x, "native"), rational(y, "native")) for x, y in row["corners"]
        )
        if native != sorted(square(pose).corners):
            mismatches.append(f"square {k}: corners")
    return {
        "member": NATIVE_MEMBER,
        "representation": witness.get("representation"),
        "side_equal": nside == side,
        "mismatches": mismatches,
        "equal": nside == side and not mismatches,
    }


SCIENTIFIC = re.compile(r"'(-?[0-9]+(?:\.[0-9]+)?(?:[eE][-+]?[0-9]+)?)'")
# The eight symmetries of the box [0, L]^2, each with whether it reverses orientation.
SYMMETRIES: tuple[tuple[str, bool], ...] = (
    ("identity", False),
    ("x -> L - x", True),
    ("y -> L - y", True),
    ("half turn", False),
    ("swap x, y", True),
    ("quarter turn", False),
    ("three-quarter turn", False),
    ("anti-diagonal", True),
)


def symmetry(name: str, side: Fraction, p: Point) -> Point:
    x, y = p
    return {
        "identity": (x, y),
        "x -> L - x": (side - x, y),
        "y -> L - y": (x, side - y),
        "half turn": (side - x, side - y),
        "swap x, y": (y, x),
        "quarter turn": (side - y, x),
        "three-quarter turn": (y, side - x),
        "anti-diagonal": (side - y, side - x),
    }[name]


def linear(name: str, v: Point) -> Point:
    """The linear part of a symmetry, acting on a direction."""
    x, y = v
    return {
        "identity": (x, y),
        "x -> L - x": (-x, y),
        "y -> L - y": (x, -y),
        "half turn": (-x, -y),
        "swap x, y": (y, x),
        "quarter turn": (-y, x),
        "three-quarter turn": (y, -x),
        "anti-diagonal": (-y, -x),
    }[name]


def turn_sine(u: Point, w: Point) -> float:
    """The sine of the angle between unit ``u`` and ``w``, modulo a quarter turn.

    For an angle d in [0, 45] degrees modulo 90, sin d = min(|u x w|, |u . w|) / |w|;
    the cross and dot products are exact, so a turn far below binary64 is still seen.
    """
    cross = abs(u[0] * w[1] - u[1] * w[0])
    dot = abs(u[0] * w[0] + u[1] * w[1])
    small = min(cross, dot)
    if small == 0:
        return 0.0
    # |w| from its exact square, so a tiny ratio keeps its digits.
    return float(small / Fraction(math.sqrt(float(w[0] * w[0] + w[1] * w[1]))))


type Direction = Point | float


def blocks(text: str) -> list[str]:
    """The text of each square's entry under ``  squares:``, in order of id."""
    body = text.split("\n  squares:\n", 1)[1]
    parts = re.split(r"\n?  - id: ([0-9]+)\n", "\n" + body)
    ids, chunks = parts[1::2], parts[2::2]
    if [int(i) for i in ids] != list(range(1, N + 1)):
        raise ReviewError("a reference witness does not list ids 1 to 29 in order")
    # The last entry ends where the next key of the witness (two spaces, then text) begins.
    last = re.split(r"\n  (?=\S)", chunks[-1], maxsplit=1)[0]
    return [*chunks[:-1], last]


def angle_mod_90(a: float, b: float) -> float:
    return math.degrees(math.atan2(b, a)) % 90.0


def interval_reference(path: Path) -> tuple[Fraction, list[tuple[Point, Direction]]]:
    """T-009's corners witness: each coordinate an enclosure, read at its midpoint."""
    text = path.read_text()
    side = decimal(find_one(r"\n  side:\n  - '([0-9.]+)'\n", text, "T-009 side"), "side")
    rows: list[tuple[Point, Direction]] = []
    for chunk in blocks(text):
        values = [Fraction(v) for v in SCIENTIFIC.findall(chunk.split("corners:", 1)[1])]
        if len(values) != 16:
            raise ReviewError("T-009's witness: a square without 4 corners of 2 enclosures")
        mids = [(values[i] + values[i + 1]) / 2 for i in range(0, 16, 2)]
        corners = [(mids[i], mids[i + 1]) for i in range(0, 8, 2)]
        cx = sum((c[0] for c in corners), Fraction(0)) / 4
        cy = sum((c[1] for c in corners), Fraction(0)) / 4
        edge = (corners[1][0] - corners[0][0], corners[1][1] - corners[0][1])
        rows.append(((cx, cy), edge))
    return side, rows


def basis_reference(path: Path) -> tuple[Fraction, list[tuple[Point, Direction]]]:
    """A rational centre-basis witness, as the replay's fact is written."""
    side, squares = read_fact(path)
    return side, [((c[0], c[1]), (b[0], b[1])) for _, c, b in squares]


def angle_reference(path: Path) -> tuple[Fraction, list[tuple[Point, Direction]]]:
    """A decimal centre-angle witness in degrees, as the house at 29 is written."""
    text = path.read_text()
    side = decimal(find_one(r"\n  side: '([0-9.]+)'\n", text, "house side"), "side")
    rows: list[tuple[Point, Direction]] = []
    for chunk in blocks(text):
        values = SCIENTIFIC.findall(chunk)
        if len(values) != 3:
            raise ReviewError("the house witness: a square without a centre and an angle")
        x, y, a = (Fraction(v) for v in values)
        rows.append(((x, y), float(a) % 90.0))
    return side, rows


def turn_deg(name: str, u: Point, direction: Direction, *, reverses: bool) -> float:
    """The turn between a certificate square and its partner, modulo 90 degrees."""
    if isinstance(direction, tuple):
        return math.degrees(math.asin(min(1.0, turn_sine(linear(name, u), direction))))
    ours = angle_mod_90(float(u[0]), float(u[1]))
    ours = (-ours) % 90.0 if reverses else ours
    turn = abs(ours - direction) % 90.0
    return min(turn, 90.0 - turn)


def measure(
    side: Fraction,
    poses: list[Pose],
    reference: tuple[Fraction, list[tuple[Point, Direction]]],
) -> dict[str, object]:
    """The certificate against a reference packing, as the register's identity reads it.

    Under each symmetry of the box, each reference square is paired with the nearest
    certificate centre; a pairing that is one to one is measured by the largest centre
    move, the squares moved beyond 1e-3, and the largest turn modulo 90 degrees.
    Differences are taken exactly and only then made floats, and a turn against a
    rational direction is taken from exact cross and dot products; a turn against an
    angle in degrees is a float difference, good to about 1e-13 degrees. This measures; it
    decides nothing.
    """
    ref_side, ref = reference
    ours = [((p.x, p.y), axes(p.t)[0]) for p in poses]
    exact_turns = all(isinstance(d, tuple) for _, d in ref)
    best: dict[str, object] | None = None
    best_move = math.inf
    for name, reverses in SYMMETRIES:
        mapped = [symmetry(name, side, c) for c, _ in ours]
        pairs = []
        for centre, direction in ref:
            dists = [
                math.hypot(float(m[0] - centre[0]), float(m[1] - centre[1])) for m in mapped
            ]
            k = min(range(N), key=dists.__getitem__)
            turn = turn_deg(name, ours[k][1], direction, reverses=reverses)
            pairs.append((k, dists[k], turn))
        one_to_one = len({k for k, _, _ in pairs}) == N
        moves = [d for _, d, _ in pairs]
        row: dict[str, object] = {
            "symmetry": name,
            "one_to_one": one_to_one,
            "paired_by_index": [k for k, _, _ in pairs] == list(range(N)),
            "moved": sum(d > 1e-3 for d in moves),
            "moved_beyond": {t: sum(d > float(t) for d in moves) for t in THRESHOLDS},
            "max_move": f"{max(moves):.4g}",
            "max_turn_deg": f"{max(t for _, _, t in pairs):.4g}",
            "turns": "exact cross and dot products" if exact_turns else "float angles",
            "side_difference": sci(side - ref_side),
        }
        if one_to_one and max(moves) < best_move:
            best, best_move = row, max(moves)
    if best is None:
        return {"one_to_one": False}
    return best


def cmd_identity(args: argparse.Namespace) -> dict[str, object]:
    asset = open_asset(args.asset)
    side, poses = read_certificate(member(asset, CERT_MEMBER, CERT_SHA256), CERT_MEMBER)
    repo = args.repo
    t009 = "packing/witnesses/kingbird-n029-2026-interval.yaml"
    t155 = "packing/cases/regularized_bounds/views/n-029.yaml.gz"
    house = "packing/witnesses/known-best/n-029.yaml"
    return {
        "T-009's witness (the packing the regularization names)": {
            "path": t009,
            **measure(side, poses, interval_reference(repo / t009)),
        },
        "T-155's view (the verified lane)": {
            "path": t155,
            **measure(side, poses, basis_reference(repo / t155)),
        },
        "the house witness (Kingbird derived numerical facts)": {
            "path": house,
            **measure(side, poses, angle_reference(repo / house)),
        },
    }


def find_one(pattern: str, text: str, what: str) -> str:
    found = re.findall(pattern, text, flags=re.DOTALL)
    if len(found) != 1:
        raise ReviewError(f"{what}: {len(found)} matches, not one")
    return found[0]


def decimal(text: str, what: str) -> Fraction:
    if not DECIMAL.fullmatch(text):
        raise ReviewError(f"{what}: not a terminating decimal")
    return Fraction(text)


def cmd_sides(args: argparse.Namespace) -> dict[str, object]:
    asset = open_asset(args.asset)
    side, _ = read_certificate(member(asset, CERT_MEMBER, CERT_SHA256), CERT_MEMBER)
    repo = args.repo
    case_path = "packing/frontier/n-029.md"
    case = (repo / case_path).read_text()
    kingbird_text = find_one(
        r"reported_upper_bound:\n    value: '([0-9.]+)'\n    exact_form: null", case, "print"
    )
    verified_print = find_one(
        r"verified_upper_bound:\n    value: '([0-9.]+)'\n    exact_form: ", case, "print"
    )
    t155_case = find_one(
        r"verified_upper_bound:\n    value: '[0-9.]+'\n    exact_form: ([0-9]+/[0-9]+)\n",
        case,
        "exact form",
    )
    results_path = "packing/frontier/results.yaml"
    results = (repo / results_path).read_text()
    t155_entry = find_one(r"\n  - id: T-155\n(.*?)\n  - id: T-", results, "T-155")
    t155_claim = find_one(r"s\(29\) <=\s+([0-9.]+),", t155_entry, "T-155's s(29)")
    ledger_path = "packing/campaign/issue-intake/upper-bounds-20261014/sources.yaml"
    ledger = (repo / ledger_path).read_text()
    pr574_text = find_one(
        r"\n  - n: 29\n    printed: '5\.9338334626769291896894606163520191384339'\n"
        r"    rounding: up\n    exact: ([0-9]+/[0-9]+)\n",
        ledger,
        "PR #574's N29 row",
    )
    t155 = rational(t155_case, "T-155")
    pr574 = rational(pr574_text, "PR #574 N29")
    kingbird = decimal(kingbird_text, "Kingbird print")
    baselines = {
        key: read_certificate(member(asset, name), name)[0] for key, name in BASELINES.items()
    }
    comparisons = {
        "T-155 exact side (n-029.md verified_upper_bound.exact_form)": t155,
        "PR #574 N29 exact side (14 October ledger sources.yaml)": pr574,
        "asset baseline pr574-v2-n029.cert.json s_exact": baselines["pr574-v2"],
        "asset baseline pr549-n029.cert.json s_exact": baselines["pr549"],
        "asset baseline evan-n029.cert.json s_exact": baselines["evan"],
        "Kingbird print (n-029.md reported_upper_bound.value)": kingbird,
    }
    rows = {}
    for label, value in comparisons.items():
        diff = value - side
        rows[label] = {
            "value_sci": sci(value, 40),
            "minus_S": sci(diff),
            "S_is": "below" if diff > 0 else ("equal" if diff == 0 else "above"),
        }
    ulp = Fraction(1, 10 ** len(kingbird_text.split(".")[1]))
    t009_path = "packing/witnesses/kingbird-n029-2026-interval.yaml"
    t009 = (repo / t009_path).read_text()
    box = find_one(
        r"pose_box:\n        names:\n        - s\n.*?        lo:\n        - '([0-9.]+)'\n"
        r".*?        hi:\n        - '([0-9.]+)'\n",
        t009,
        "T-009's pose box",
    )
    box_lo, box_hi = decimal(box[0], "box lo"), decimal(box[1], "box hi")
    house_path = "packing/witnesses/known-best/n-029.yaml"
    house = (repo / house_path).read_text()
    house_side = decimal(find_one(r"\n  side: '([0-9.]+)'\n", house, "house side"), "house")
    # The source's own comparison, read only after the differences above were computed.
    stated = json.loads(member(asset, "n29-certificate/COMPARISON.json"))
    files = {"previous_public_pr574_v2": "pr574-v2", "external_pr549": "pr549"}
    files["external_evan"] = "evan"
    source_rows = {}
    for row in stated["comparisons"]:
        key = files[row["label"]]
        theirs = baselines[key]
        source_rows[row["label"]] = {
            "side_exact equals the baseline's s_exact": rational(row["side_exact"], "side")
            == theirs,
            "gain_exact equals the baseline minus S, computed here": rational(
                row["gain_exact"], "gain"
            )
            == theirs - side,
            "strictly_smaller": row["strictly_smaller"],
        }
    return {
        "S_sci": sci(side, 60),
        "read_from": [case_path, results_path, ledger_path, t009_path, house_path, ASSET_NAME],
        "T-155 claim's s(29) decimal equals n-029.md's exact form": decimal(
            t155_claim, "T-155 claim"
        )
        == t155,
        "asset pr574-v2 baseline equals the ledger's PR #574 side": baselines["pr574-v2"]
        == pr574,
        "asset pr549 baseline equals T-155": baselines["pr549"] == t155,
        "n-029.md verified print minus its exact form": sci(
            decimal(verified_print, "p") - t155
        ),
        "comparisons": rows,
        "Kingbird print spans": {
            "cut [p, p + ulp)": "S inside"
            if kingbird <= side < kingbird + ulp
            else "S outside",
            "nearest [p - ulp/2, p + ulp/2]": "S inside"
            if kingbird - ulp / 2 <= side <= kingbird + ulp / 2
            else "S above"
            if side > kingbird + ulp / 2
            else "S below",
            "up (p - ulp, p]": "S inside" if kingbird - ulp < side <= kingbird else "S above",
            "S - p in units of the last place": sci((side - kingbird) / ulp),
        },
        "T-009's Krawczyk pose box for s": {
            "path": t009_path,
            "lo": box[0],
            "hi": box[1],
            "S - lo": sci(side - box_lo),
            "hi - S": sci(box_hi - side),
            "S in the box": box_lo <= side <= box_hi,
            "lo - p in units of the print's last place": sci((box_lo - kingbird) / ulp),
            "the print is the box truncated, not rounded": kingbird + ulp / 2 < box_lo
            and box_hi < kingbird + ulp,
            "T-155 - hi": sci(t155 - box_hi),
        },
        "the house witness's numerical side": {
            "path": house_path,
            "value_sci": sci(house_side, 40),
            "S - house": sci(side - house_side),
            "PR #574 - house": sci(pr574 - house_side),
        },
        "the source's COMPARISON.json against this program": {
            "candidate side_exact equals S": rational(stated["candidate"]["side_exact"], "S")
            == side,
            **source_rows,
        },
    }


EXPECTED_RECEIPT = {
    "positive": [],
    "duplicate-square-overlap": ["pair 0 1"],
    "square-translated-outside-container": ["wall 0 right"],
}


def cmd_receipt(args: argparse.Namespace) -> dict[str, object]:
    """Each job the replay retained, decided again here from its own checker input."""
    asset = open_asset(args.asset)
    side, poses = read_certificate(member(asset, CERT_MEMBER, CERT_SHA256), CERT_MEMBER)
    receipt = json.loads(lzma.decompress(args.receipt.read_bytes()))
    rows = []
    for case in receipt["cases"]:
        given = case["checker_input"]
        if given["n"] != N or len(given["poses"]) != N:
            raise ReviewError("a receipt job is not 29 squares")
        jside = rational(given["side"], "receipt side")
        jposes = [Pose(*(rational(v, "receipt pose") for v in row)) for row in given["poses"]]
        d = decide(jside, jposes)
        changed = [k for k in range(N) if jposes[k] != poses[k]]
        least_gap = min(g for _, _, g, _ in d.pairs)
        least_wall = min(c for _, _, c in d.walls)
        routes = {}
        for route in receipt["routes"]:
            r = case[route]
            routes[route] = {
                "verification_passed": r["verification_passed"],
                "failures": r["failures"],
                "least_pair_gap_equals_this_program's": rational(
                    r["minimum_best_pair_gap"], "gap"
                )
                == least_gap,
                "least_wall_clearance_equals_this_program's": rational(
                    r["minimum_containment_clearance"], "clearance"
                )
                == least_wall,
            }
        rows.append(
            {
                "control": case["control"],
                "side_is_the_certificate's": jside == side,
                "squares_changed_from_the_certificate": changed,
                "this_program": {
                    "violations": d.violations,
                    "least_pair_gap": sci(least_gap) if least_gap else "0",
                    "least_wall_clearance": sci(least_wall) if least_wall else "0",
                    "expected": EXPECTED_RECEIPT[case["control"]],
                    "for_the_right_reason": d.violations == EXPECTED_RECEIPT[case["control"]],
                },
                "routes": routes,
                "cpu_s": round(d.cpu_s, 2),
            }
        )
    return {
        "receipt": "packing/resources/web/pingyou-pr622-certificate-2026-10-15/receipts/"
        "exact-certification.json.xz",
        "format": receipt["format"],
        "jobs": rows,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("certificate")
    p.add_argument("asset", type=Path)
    p.add_argument("--member", default=CERT_MEMBER)
    p = sub.add_parser("controls")
    p.add_argument("asset", type=Path)
    p = sub.add_parser("fact")
    p.add_argument("asset", type=Path)
    p.add_argument("fact", type=Path)
    p = sub.add_parser("native")
    p.add_argument("asset", type=Path)
    p = sub.add_parser("sides")
    p.add_argument("asset", type=Path)
    p.add_argument("repo", type=Path)
    p = sub.add_parser("identity")
    p.add_argument("asset", type=Path)
    p.add_argument("repo", type=Path)
    p = sub.add_parser("receipt")
    p.add_argument("asset", type=Path)
    p.add_argument("receipt", type=Path)
    args = parser.parse_args(argv)
    commands = {
        "certificate": cmd_certificate,
        "controls": cmd_controls,
        "fact": cmd_fact,
        "native": cmd_native,
        "sides": cmd_sides,
        "identity": cmd_identity,
        "receipt": cmd_receipt,
    }
    try:
        out = commands[args.command](args)
    except ReviewError as error:
        sys.stderr.write(json.dumps({"error": str(error)}) + "\n")
        return 2
    sys.stdout.write(json.dumps(out, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
