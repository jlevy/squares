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
    the side against the record's comparators at 29 and the source's baselines, exactly.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
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
    walls = [
        (k, w, c) for k, q in enumerate(squares) for w, c in clearances(q, side).items()
    ]
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
    controls.append(("outside-container", "square 0 moved by (-1, 0)", side, out, ["wall 0 left"]))

    for i, j, a in touching[:2]:
        da, db = toward(squares[i], squares[j], a)
        pushed = list(poses)
        pushed[j] = Pose(poses[j].x - TIGHT * da, poses[j].y - TIGHT * db, poses[j].t)
        controls.append((
            f"tight-pair-{i}-{j}",
            f"square {j} moved 10^-3000 towards square {i} along their touching axis {a}",
            side,
            pushed,
            [f"pair {i} {j}"],
        ))

    expected = [f"wall {k} {w}" for k, w, c in base.walls if c == 0 and w in {"top", "right"}]
    controls.append((
        "tight-box",
        "side reduced by 10^-3000",
        side - TIGHT,
        list(poses),
        expected,
    ))

    rows = []
    for name, mutation, s, ps, want in controls:
        d = decide(s, ps)
        got = d.violations
        rows.append({
            "control": name,
            "mutation": mutation,
            "refused": bool(got),
            "violations": got,
            "expected": want,
            "for_the_right_reason": got == want,
            "cpu_s": round(d.cpu_s, 2),
        })
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
    if after.startswith("  - ") or not after.startswith("  ") or after.startswith("   "):
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
        "fact": "packing/resources/web/pingyou-pr622-certificate-2026-10-15/facts/n-029.yaml.gz",
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
        native = sorted((rational(x, "native"), rational(y, "native")) for x, y in row["corners"])
        if native != sorted(square(pose).corners):
            mismatches.append(f"square {k}: corners")
    return {
        "member": NATIVE_MEMBER,
        "representation": witness.get("representation"),
        "side_equal": nside == side,
        "mismatches": mismatches,
        "equal": nside == side and not mismatches,
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
    return {
        "S_sci": sci(side, 60),
        "read_from": [case_path, results_path, ledger_path, ASSET_NAME],
        "T-155 claim's s(29) decimal equals n-029.md's exact form": decimal(
            t155_claim, "T-155 claim"
        )
        == t155,
        "asset pr574-v2 baseline equals the ledger's PR #574 side": baselines["pr574-v2"]
        == pr574,
        "asset pr549 baseline equals T-155": baselines["pr549"] == t155,
        "n-029.md verified print minus its exact form": sci(decimal(verified_print, "p") - t155),
        "comparisons": rows,
        "Kingbird print spans": {
            "cut [p, p + ulp)": "S inside" if kingbird <= side < kingbird + ulp else "S outside",
            "nearest [p - ulp/2, p + ulp/2]": "S inside"
            if kingbird - ulp / 2 <= side <= kingbird + ulp / 2
            else "S above"
            if side > kingbird + ulp / 2
            else "S below",
            "up (p - ulp, p]": "S inside" if kingbird - ulp < side <= kingbird else "S above",
            "S - p in units of the last place": sci((side - kingbird) / ulp),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
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
    args = parser.parse_args(argv)
    commands = {
        "certificate": cmd_certificate,
        "controls": cmd_controls,
        "fact": cmd_fact,
        "native": cmd_native,
        "sides": cmd_sides,
    }
    try:
        out = commands[args.command](args)
    except ReviewError as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 2
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
