"""Self-test of the L64 checker: known answers, random pairs at exact contact, bad files.

Usage: python -I -B l64_selftest.py OUT.json SCRATCH_DIR [SEED]

Written clean room on 2026-11-09, before the checker was frozen. Every expectation is
derived here by hand or by a construction independent of both methods:

- known answers for edge, corner and vertex-edge contacts and their 1e-30 overlaps, a
  duplicate, a square and its own rotation about its centre, and walls;
- shapes both methods must refuse;
- random rational pairs, each taken to exact contact along its centre line by the
  contact parameter of the Minkowski difference (computed here, not by either method),
  then 1e-30 past it and 1e-30 short of it;
- malformed variants of a small valid file, each of which the reader must refuse.
"""

from __future__ import annotations

import json
import random
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # see l64_check.py

import l64_clip as B
import l64_sat as A
from l64_check import CHECKER, HERE, decide
from l64_reader import ReadError, read_twin_json, read_witness
from l64_util import Clock, environment, frac_str, program_digests, write_receipt

EPS = F(1, 10**30)
FAILURES: list[str] = []
COUNTS = {"known": 0, "random_pairs": 0, "random_walls": 0, "reader_refusals": 0}


def check(cond: bool, what: str) -> None:
    if not cond:
        FAILURES.append(what)


def ints(pts: list[tuple[F, F]]) -> list[tuple[int, int, int, int]]:
    return [(x.numerator, x.denominator, y.numerator, y.denominator) for x, y in pts]


def square(p0: tuple[F, F], u: tuple[F, F], ccw: bool = True) -> list[tuple[F, F]]:
    w = (-u[1], u[0]) if ccw else (u[1], -u[0])
    return [
        p0,
        (p0[0] + u[0], p0[1] + u[1]),
        (p0[0] + u[0] + w[0], p0[1] + u[1] + w[1]),
        (p0[0] + w[0], p0[1] + w[1]),
    ]


def centred(c: tuple[F, F], u: tuple[F, F], ccw: bool = True) -> list[tuple[F, F]]:
    w = (-u[1], u[0]) if ccw else (u[1], -u[0])
    p0 = (c[0] - (u[0] + w[0]) / 2, c[1] - (u[1] + w[1]) / 2)
    return square(p0, u, ccw)


def moved(pts: list[tuple[F, F]], dx: F, dy: F) -> list[tuple[F, F]]:
    return [(x + dx, y + dy) for x, y in pts]


def classes(p: list[tuple[F, F]], q: list[tuple[F, F]]) -> tuple[str, F, str, F]:
    a1, a2 = A.SquareA(1, ints(p)), A.SquareA(2, ints(q))
    m, _ = A.pair_margin(a1, a2)
    b1, b2 = B.SquareB(1, ints(p)), B.SquareB(2, ints(q))
    cb, area = B.pair_class(b1, b2)
    return A.classify(m), m, cb, F(int(area.numerator), int(area.denominator))


def known(name: str, p, q, cls: str, margin: F | None, area: F | None) -> None:
    COUNTS["known"] += 1
    ca, m, cb, ar = classes(p, q)
    check(ca == cls, f"{name}: A class {ca}, expected {cls}")
    check(cb == cls, f"{name}: B class {cb}, expected {cls}")
    if margin is not None:
        check(m == margin, f"{name}: margin {m}, expected {margin}")
    if area is not None:
        check(ar == area, f"{name}: area {ar}, expected {area}")


def known_answers() -> None:
    z, one, half = F(0), F(1), F(1, 2)
    unit = square((z, z), (one, z))
    known("edge contact", unit, moved(unit, one, z), "touching", z, z)
    known("edge apart", unit, moved(unit, one + EPS, z), "separated", EPS, z)
    known("edge overlap", unit, moved(unit, one - EPS, z), "overlapping", -EPS, EPS)
    known("corner contact", unit, moved(unit, one, one), "touching", z, z)
    known("corner apart", unit, moved(unit, one + EPS, one + EPS), "separated", EPS, z)
    known("corner overlap", unit, moved(unit, one - EPS, one - EPS), "overlapping", -EPS, EPS * EPS)
    for label, u in (("3-4-5", (F(3, 5), F(4, 5))), ("4-3-5", (F(4, 5), F(3, 5)))):
        v = square((half, one), u)
        known(f"{label} vertex on edge", unit, v, "touching", z, z)
        known(f"{label} vertex apart", unit, moved(v, z, EPS), "separated", EPS, z)
        known(
            f"{label} vertex overlap",
            unit,
            moved(v, z, -EPS),
            "overlapping",
            -EPS,
            F(25, 24) * EPS * EPS,
        )
        rev = v[::-1]
        known(f"{label} vertex on edge, clockwise list", unit, rev, "touching", z, z)
        known(
            f"{label} vertex overlap, clockwise list",
            unit,
            moved(rev, z, -EPS),
            "overlapping",
            -EPS,
            F(25, 24) * EPS * EPS,
        )
    known("duplicate", unit, unit, "overlapping", -one, one)
    turned = centred((half, half), (F(3, 5), F(4, 5)))
    known("own rotation by (3/5, 4/5)", unit, turned, "overlapping", F(-6, 5), F(5, 6))
    turned_t3 = centred((half, half), (F(4, 5), F(3, 5)))
    known("own rotation by (4/5, 3/5)", unit, turned_t3, "overlapping", F(-6, 5), F(5, 6))

    # Walls.
    for side, inside, clear in ((one, True, z), (one - EPS, False, -EPS), (one + EPS, True, z)):
        COUNTS["known"] += 1
        a = A.SquareA(1, ints(unit))
        b = B.SquareB(1, ints(unit))
        m = min(A.wall_clearances(a, side).values())
        ok_b, kept = B.contained(b, B.mpq(side.numerator, side.denominator))
        check((m >= 0) == inside and m == clear, f"wall at side {side}: A clearance {m}")
        check(ok_b == inside, f"wall at side {side}: B {ok_b}")
        if not inside:
            check(kept == B.mpq(((one - EPS) ** 2).numerator, ((one - EPS) ** 2).denominator), f"wall at side {side}: kept {kept}")

    # Shapes both methods must refuse.
    bad = {
        "edge 1 + 1e-30": square((z, z), (one + EPS, z)),
        "parallelogram": [(z, z), (one, z), (F(3, 2), one), (half, one)],
        "unit rhombus": [(z, z), (one, z), (F(8, 5), F(4, 5)), (F(3, 5), F(4, 5))],
        "corners out of order": [unit[0], unit[2], unit[1], unit[3]],
        "fourth corner off by 1e-30": [unit[0], unit[1], (one, one + EPS), unit[3]],
        "degenerate": [(z, z)] * 4,
    }
    for name, pts in bad.items():
        COUNTS["known"] += 1
        try:
            A.SquareA(1, ints(pts))
            check(False, f"shape {name}: A accepted")
        except A.ShapeError:
            pass
        try:
            B.SquareB(1, ints(pts))
            check(False, f"shape {name}: B accepted")
        except B.ShapeErrorB:
            pass


def contact_lambda(p: list[tuple[F, F]], q: list[tuple[F, F]], v: tuple[F, F]) -> F:
    """Least lambda at which q moved by -lambda*v first touches p (Minkowski difference)."""
    axes = []
    for pts in (p, q):
        ux, uy = pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]
        axes += [(ux, uy), (-uy, ux), (-ux, -uy), (uy, -ux)]
    best: F | None = None
    for ax in axes:
        k = ax[0] * v[0] + ax[1] * v[1]
        if k <= 0:
            continue
        h = max(ax[0] * x + ax[1] * y for x, y in p) - min(ax[0] * x + ax[1] * y for x, y in q)
        cand = -h / k
        if best is None or cand > best:
            best = cand
    assert best is not None
    return best


def random_unit(rng: random.Random) -> tuple[F, F]:
    t = F(rng.randint(-10**6, 10**6), rng.randint(1, 10**6))
    c = (1 - t * t) / (1 + t * t)
    s = 2 * t / (1 + t * t)
    return c, s


def random_pairs(rng: random.Random, count: int) -> None:
    for _ in range(count):
        COUNTS["random_pairs"] += 1
        ci = (F(rng.randint(0, 10**6), 10**6), F(rng.randint(0, 10**6), 10**6))
        cj = (ci[0] + F(rng.randint(-2 * 10**6, 2 * 10**6), 10**6), ci[1] + F(rng.randint(-2 * 10**6, 2 * 10**6), 10**6))
        if cj == ci:
            continue
        p = centred(ci, random_unit(rng), rng.random() < 0.5)
        q = centred(cj, random_unit(rng), rng.random() < 0.5)
        ca, m, cb, _ = classes(p, q)
        check(ca == cb, f"random pair: A {ca} B {cb}")
        v = (cj[0] - ci[0], cj[1] - ci[1])
        lam = contact_lambda(p, q, v)
        for delta, want in ((F(0), "touching"), (EPS, "overlapping"), (-EPS, "separated")):
            lt = lam + delta
            q2 = moved(q, -lt * v[0], -lt * v[1])
            ca2, m2, cb2, ar2 = classes(p, q2)
            check(ca2 == want, f"random contact {delta}: A {ca2}, expected {want}")
            check(cb2 == want, f"random contact {delta}: B {cb2}, expected {want}")
            if want == "touching":
                check(m2 == 0 and ar2 == 0, "random contact: margin or area not zero")


def random_walls(rng: random.Random, count: int) -> None:
    side = F(10)
    sq = B.mpq(10)
    for _ in range(count):
        COUNTS["random_walls"] += 1
        c = (F(rng.randint(2 * 10**6, 8 * 10**6), 10**6), F(rng.randint(2 * 10**6, 8 * 10**6), 10**6))
        p = centred(c, random_unit(rng), rng.random() < 0.5)
        wall = rng.choice(("left", "bottom", "right", "top"))
        xs, ys = [x for x, _ in p], [y for _, y in p]
        shift = {
            "left": (-min(xs), F(0)),
            "bottom": (F(0), -min(ys)),
            "right": (side - max(xs), F(0)),
            "top": (F(0), side - max(ys)),
        }[wall]
        unit_dir = {"left": (-1, 0), "bottom": (0, -1), "right": (1, 0), "top": (0, 1)}[wall]
        for delta, inside in ((F(0), True), (EPS, False), (-EPS, True)):
            dx = shift[0] + delta * unit_dir[0]
            dy = shift[1] + delta * unit_dir[1]
            pts = moved(p, dx, dy)
            a = A.SquareA(1, ints(pts))
            b = B.SquareB(1, ints(pts))
            m = min(A.wall_clearances(a, side).values())
            ok_b, _ = B.contained(b, sq)
            check((m >= 0) == inside, f"random wall {wall} {delta}: A {m}")
            check(ok_b == inside, f"random wall {wall} {delta}: B {ok_b}")
            if delta == 0:
                check(m == 0, f"random wall {wall}: clearance {m} at contact")


VALID_YAML = """softschema:
  contract: packing.squares:Witness/v2
  schema: witness.schema.yaml
  envelope: witness
  status: enforced
witness:
  id: W-l64-selftest
  n: 2
  side: '3'
  square_size: '1'
  representation: corners
  scalar:
    kind: rational
  coordinates:
    origin: lower-left
    axes: x-right-y-up
    angle_unit: not-applicable
  squares:
  - id: 1
    corners:
    - - '0'
      - '0'
    - - '1'
      - '0'
    - - '1'
      - '1'
    - - '0'
      - '1'
  - id: 2
    corners:
    - - 23/10
      - 1/10
    - - 29/10
      - 9/10
    - - 21/10
      - 3/2
    - - 3/2
      - 7/10
  claim:
    coordinate_provenance: verified
    method: exact-algebraic
    limitations: A self-test file.
"""


def _json_of(yaml_text: str) -> str:
    import yaml

    doc = yaml.load(yaml_text, Loader=yaml.BaseLoader)  # noqa: S506 - strings only
    doc["witness"]["n"] = int(doc["witness"]["n"])
    for sq in doc["witness"]["squares"]:
        sq["id"] = int(sq["id"])
    return json.dumps(doc) + "\n"


def reader_tests(scratch: Path) -> dict:
    scratch.mkdir(parents=True, exist_ok=True)
    good_y = scratch / "good.yaml"
    good_j = scratch / "good.json"
    good_y.write_text(VALID_YAML, encoding="ascii")
    good_j.write_text(_json_of(VALID_YAML), encoding="ascii")
    w = read_witness(good_y, expected_n=2)
    read_twin_json(good_j, w)
    res = decide(w["squares"], F(*w["side"]))
    check(res["verdict"] == "ACCEPT", f"valid self-test file: {res['verdict']}")
    check(w["final_newline"], "valid self-test file: final newline not recorded")
    # A final newline is recorded and decides nothing: the same file without one reads.
    bare = scratch / "no-final-newline.yaml"
    bare.write_text(VALID_YAML.rstrip("\n"), encoding="ascii")
    w_bare = read_witness(bare, expected_n=2)
    check(not w_bare["final_newline"], "file without a final newline: not recorded")
    check(w_bare["raw_squares"] == w["raw_squares"], "file without a final newline: squares differ")
    bare_j = scratch / "no-final-newline.json"
    bare_j.write_text(_json_of(VALID_YAML).rstrip("\n"), encoding="ascii")
    check(not read_twin_json(bare_j, w)["final_newline"], "JSON without a final newline")
    check(res["pairs"]["classes"]["separated"] == 1, "valid self-test file: pair class")
    yaml_mutants = {
        "CRLF": VALID_YAML.replace("\n", "\r\n"),
        "tab": VALID_YAML.replace("  n: 2", "\tn: 2"),
        "non-ASCII digit": VALID_YAML.replace("23/10", "13/1０"),
        "duplicate key": VALID_YAML.replace("  n: 2\n", "  n: 2\n  n: 2\n"),
        "decimal": VALID_YAML.replace("23/10", "2.3"),
        "exponent": VALID_YAML.replace("23/10", "23e-1"),
        "plus sign": VALID_YAML.replace("23/10", "+23/10"),
        "leading zero": VALID_YAML.replace("23/10", "023/10"),
        "zero denominator": VALID_YAML.replace("23/10", "23/0"),
        "negative denominator": VALID_YAML.replace("23/10", "23/-10"),
        "negative zero": VALID_YAML.replace("- - '0'\n      - '0'", "- - '-0'\n      - '0'", 1),
        "space in scalar": VALID_YAML.replace("23/10", "23 /10"),
        "underscore": VALID_YAML.replace("23/10", "2_3/10"),
        "extra square key": VALID_YAML.replace("  - id: 2\n", "  - id: 2\n    angle: '0'\n"),
        "three corners": VALID_YAML.replace("    - - 3/2\n      - 7/10\n", ""),
        "count mismatch": VALID_YAML.replace("  n: 2", "  n: 3"),
        "repeated id": VALID_YAML.replace("  - id: 2", "  - id: 1"),
        "center-basis": VALID_YAML.replace("representation: corners", "representation: center-basis"),
        "decimal kind": VALID_YAML.replace("kind: rational", "kind: decimal"),
        "container-center": VALID_YAML.replace("origin: lower-left", "origin: container-center"),
        "square size 2": VALID_YAML.replace("square_size: '1'", "square_size: '2'"),
        "anchor and alias": VALID_YAML.replace("side: '3'", "side: &s '3'\n  extra: *s"),
        "tag": VALID_YAML.replace("side: '3'", "side: !!str '3'"),
        "flow sequence": VALID_YAML.replace("    - - 3/2\n      - 7/10\n", "    - [3/2, 7/10]\n"),
        "unknown witness key": VALID_YAML.replace("  n: 2\n", "  n: 2\n  extra: x\n"),
        "zero side": VALID_YAML.replace("side: '3'", "side: '0'"),
    }
    refused: dict[str, str] = {}
    for name, text in yaml_mutants.items():
        COUNTS["reader_refusals"] += 1
        path = scratch / "mutant.yaml"
        path.write_bytes(text.encode("utf-8"))
        try:
            read_witness(path, expected_n=2)
            check(False, f"reader accepted the mutant: {name}")
            refused[name] = "ACCEPTED"
        except ReadError as exc:
            refused[name] = str(exc)[:100]
    good_json = _json_of(VALID_YAML)
    json_mutants = {
        "JSON digit differs": good_json.replace("23/10", "23/11"),
        "JSON float": good_json.replace('"n": 2', '"n": 2.0'),
        "JSON duplicate key": good_json.replace('"n": 2', '"n": 2, "n": 2'),
        "JSON n as string": good_json.replace('"n": 2', '"n": "2"'),
        "JSON NaN": good_json.replace('"n": 2', '"n": NaN'),
        "JSON id as string": good_json.replace('"id": 2', '"id": "2"'),
    }
    for name, text in json_mutants.items():
        COUNTS["reader_refusals"] += 1
        path = scratch / "mutant.json"
        path.write_text(text, encoding="ascii")
        try:
            read_twin_json(path, w)
            check(False, f"reader accepted the mutant: {name}")
            refused[name] = "ACCEPTED"
        except ReadError as exc:
            refused[name] = str(exc)[:100]
    return refused


def main(argv: list[str]) -> int:
    if len(argv) not in (3, 4):
        print(__doc__)
        return 2
    out, scratch = argv[1], Path(argv[2])
    seed = int(argv[3]) if len(argv) == 4 else 20261109
    clock = Clock()
    rng = random.Random(seed)
    known_answers()
    random_pairs(rng, 3000)
    random_walls(rng, 1000)
    refused = reader_tests(scratch)
    receipt = {
        "program": "l64_selftest.py",
        "programs_sha256": program_digests([HERE / f for f in [*CHECKER, "l64_selftest.py"]]),
        "environment": environment(),
        "seed": seed,
        "epsilon": frac_str(EPS),
        "counts": COUNTS,
        "reader_refusals": refused,
        "failures": FAILURES,
        "verdict": "PASSED" if not FAILURES else "FAILED",
        "clock": clock.report(),
    }
    write_receipt(out, receipt)
    print(f"self-test {receipt['verdict']}: {COUNTS}; failures {len(FAILURES)}")
    for f in FAILURES[:20]:
        print("  ", f)
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
