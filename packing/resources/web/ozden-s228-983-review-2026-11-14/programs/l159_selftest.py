"""Lane L159's self-test: hold both methods and the reader to hand-derived cases.

Clean-room code written for the stage 4 review of issue #983. It imports nothing from
this repository or from the source, and reuses no code of any earlier review.

Every exact expectation below is derived by hand in the comments beside it. The suite
then runs twice more with a deliberately broken copy of each method (method A counting
a zero margin as apart, method B clipping with open half-planes); both must fail it.

Usage: l159_selftest.py OUT.json
"""

from __future__ import annotations

import json
import random
import sys
import time
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml  # noqa: E402

import l159_clip as clip  # noqa: E402
import l159_geom as geom  # noqa: E402
import l159_sat as sat  # noqa: E402
from l159_check import decide  # noqa: E402
from l159_reader import Refused, parse_yaml, read_texts  # noqa: E402

EPS = Fraction(1, 10**30)
DELTAS = (EPS, Fraction(0), -EPS)
UP = (Fraction(1), Fraction(0))
U345 = (Fraction(3, 5), Fraction(4, 5))
U435 = (Fraction(4, 5), Fraction(3, 5))
WALLS = ("left", "bottom", "right", "top")


class Suite:
    """Counts cases and keeps the labels of failures."""

    def __init__(self) -> None:
        self.cases = 0
        self.failures: list[str] = []

    def expect(self, ok: bool, label: str) -> None:
        self.cases += 1
        if not ok:
            self.failures.append(label)


def cls_of(delta: Fraction) -> str:
    return "apart" if delta > 0 else "contact" if delta == 0 else "overlap"


def b_area(p: tuple, q: tuple) -> tuple[str, Fraction]:
    pp, qq = clip.to_points(p), clip.to_points(q)
    cls, area = clip.pair(pp, clip.edge_half_planes(qq))
    return cls, Fraction(int(area.numerator), int(area.denominator))


def check_pair(s: Suite, p: tuple, q: tuple, margin: Fraction, area: Fraction, label: str) -> None:
    """Both methods, both orders: A's margin and class, B's class and area."""
    a, b = sat.prepare(p), sat.prepare(q)
    s.expect(a is not None and b is not None, f"{label}: A unit")
    s.expect(clip.is_unit_square(clip.to_points(p)), f"{label}: B unit p")
    s.expect(clip.is_unit_square(clip.to_points(q)), f"{label}: B unit q")
    if a is None or b is None:
        return
    want = cls_of(margin)
    for x, y, tag in ((a, b, "pq"), (b, a, "qp")):
        m = sat.margin(x, y)
        s.expect(sat.margin_fraction(m) == margin, f"{label} {tag}: A margin")
        s.expect(sat.margin_class(m[0]) == want, f"{label} {tag}: A class")
    for x, y, tag in ((p, q, "pq"), (q, p, "qp")):
        cls, got = b_area(x, y)
        s.expect(cls == want, f"{label} {tag}: B class {cls}")
        s.expect(got == area, f"{label} {tag}: B area {got}")


def listings(centre: tuple, u: tuple) -> list[tuple]:
    """The square in both senses from two starting corners."""
    return [geom.square(centre, u, sense, start) for sense in (1, -1) for start in (0, 2)]


def quarter(corners: tuple, k: int) -> tuple:
    """Turn the corners k quarter turns about the origin."""
    pts = geom.as_fraction_points(corners)
    for _ in range(k):
        pts = [(-y, x) for x, y in pts]
    return tuple(geom.as_int_point(p) for p in pts)


def contact_cases(s: Suite) -> None:
    # Edge to edge: two squares with the same frame, centres 1 + d apart along a normal.
    # The gap on that normal is d; the other normal overlaps fully, gap -1. Margin d.
    # Overlap: a 1 x |d| rectangle, area |d|.
    for u in (UP, U345):
        w = (-u[1], u[0])
        for direction in (u, w, (-u[0], -u[1]), (-w[0], -w[1])):
            for d in DELTAS:
                ca = (Fraction(5), Fraction(5))
                cb = (ca[0] + (1 + d) * direction[0], ca[1] + (1 + d) * direction[1])
                area = -d if d < 0 else Fraction(0)
                for p in listings(ca, u):
                    for q in listings(cb, u):
                        check_pair(s, p, q, d, area, f"edge {u} {direction} {d}")
    # Corner to corner: upright squares, centres offset (1 + d, 1 + d) diagonally.
    # Both normals give gap d. Overlap: a |d| x |d| square, area d^2.
    for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        for d in DELTAS:
            ca = (Fraction(5), Fraction(5))
            cb = (ca[0] + sx * (1 + d), ca[1] + sy * (1 + d))
            area = d * d if d < 0 else Fraction(0)
            for p in listings(ca, UP):
                for q in listings(cb, UP):
                    check_pair(s, p, q, d, area, f"corner {sx},{sy} {d}")
    # Vertex on edge: square i = [0,1]^2; square j turned by (3/5, 4/5) with its lowest
    # vertex V = (1/2, 1 + d). With u = (3/5, 4/5), w = (-4/5, 3/5), j's centre is
    # V + (u + w)/2 = V + (-1/10, 7/10). i's vertical normal gives gap d; the others are
    # far below (about -0.3 and -0.4). Overlap: a right triangle at V with legs
    # |d|/(4/5) and |d|/(3/5), area d^2 / (2 * 12/25) = 25 d^2 / 24.
    # The whole configuration is also turned by each quarter turn.
    for k in range(4):
        for d in DELTAS:
            ci = (Fraction(1, 2), Fraction(1, 2))
            cj = (Fraction(1, 2) - Fraction(1, 10), 1 + d + Fraction(7, 10))
            area = Fraction(25, 24) * d * d if d < 0 else Fraction(0)
            for p in listings(ci, UP):
                for q in listings(cj, U345):
                    check_pair(s, quarter(p, k), quarter(q, k), d, area, f"vertex q{k} {d}")
    # A duplicate: every gap is -1; the intersection is the square, area 1.
    c = (Fraction(7, 3), Fraction(11, 4))
    for p in listings(c, U345):
        for q in listings(c, U345):
            check_pair(s, p, q, Fraction(-1), Fraction(1), "duplicate")
    # Concentric, one turned by (c, s) = (3/5, 4/5) or (4/5, 3/5): on every normal the
    # gap is 0 - 1/2 - (c + s)/2 = -6/5. The upright square loses four congruent corner
    # triangles with legs 1/4 and 1/3 (the turned edge u.X = 1/2 meets x = 1/2 at
    # y = (1 - c)/(2s) and y = 1/2 at x = (1 - s)/(2c)), area 1 - 4/24 = 5/6, and the
    # same for (4/5, 3/5) by symmetry.
    for u in (U345, U435):
        for p in listings(c, UP):
            for q in listings(c, u):
                check_pair(s, p, q, Fraction(-6, 5), Fraction(5, 6), f"concentric {u}")


def wall_case(s: Suite, corners: tuple, side: tuple[int, int], wall: int, value: Fraction, label: str) -> None:
    """A's clearance at the wall, A's and B's classes, B's containment."""
    a = sat.prepare(corners)
    s.expect(a is not None, f"{label}: A unit")
    if a is None:
        return
    got = sat.clearances(a, side)[wall]
    s.expect(got == value, f"{label}: A clearance {got}")
    want = "apart" if value > 0 else "contact" if value == 0 else "cross"
    s.expect(sat.clearance_class(got) == want, f"{label}: A class")
    pts = clip.to_points(corners)
    s.expect(clip.walls(pts, side)[wall] == want, f"{label}: B class")
    s.expect(clip.contained(pts, side) == (value >= 0), f"{label}: B containment")


def wall_cases(s: Suite) -> None:
    side = (3, 1)
    big = Fraction(3)
    # An upright square at each wall: centre half a unit plus d from it.
    for d in DELTAS:
        h = Fraction(1, 2) + d
        centres = [(h, Fraction(3, 2)), (Fraction(3, 2), h), (big - h, Fraction(3, 2)), (Fraction(3, 2), big - h)]
        for k, ctr in enumerate(centres):
            for p in listings(ctr, UP):
                wall_case(s, p, side, k, d, f"upright {WALLS[k]} {d}")
    # A 3-4-5 square with its top vertex d below the top: the top vertex is
    # centre + (u + w)/2 = centre + (-1/10, 7/10).
    for d in DELTAS:
        ctr = (Fraction(3, 2), big - Fraction(7, 10) - d)
        for p in listings(ctr, U345):
            wall_case(s, p, side, 3, d, f"345 top {d}")


def sense_cases(s: Suite) -> None:
    for u in (UP, U345, geom.pythagorean(7, 2)):
        for sense in (1, -1):
            for start in range(4):
                p = geom.square((Fraction(2), Fraction(2)), u, sense, start)
                a = sat.prepare(p)
                s.expect(a is not None and a.sense == sense, f"sense A {u} {sense} {start}")
                s.expect(clip.sense(clip.to_points(p)) == sense, f"sense B {u} {sense} {start}")


def refusal_cases(s: Suite) -> None:
    def pts(*xy: tuple[Fraction, Fraction]) -> tuple:
        return tuple(geom.as_int_point(p) for p in xy)

    f = Fraction
    good = geom.square((f(2), f(2)), U345, 1, 0)
    gp = geom.as_fraction_points(good)
    shapes = {
        # unit sides, angles not right: a rhombus from (3/5, 4/5)
        "rhombus": pts((f(0), f(0)), (f(1), f(0)), (f(8, 5), f(4, 5)), (f(3, 5), f(4, 5))),
        "bowtie": pts((f(0), f(0)), (f(1), f(1)), (f(1), f(0)), (f(0), f(1))),
        "rectangle": pts((f(0), f(0)), (f(1), f(0)), (f(1), 1 + EPS), (f(0), 1 + EPS)),
        "third corner off": pts((f(0), f(0)), (f(1), f(0)), (1 + EPS, f(1)), (f(0), f(1))),
        "fourth corner off": pts((f(0), f(0)), (f(1), f(0)), (f(1), f(1)), (EPS, f(1))),
        "side 2": pts((f(0), f(0)), (f(2), f(0)), (f(2), f(2)), (f(0), f(2))),
        "point": pts((f(1), f(1)), (f(1), f(1)), (f(1), f(1)), (f(1), f(1))),
        # unit sides, one diagonal sqrt 2, and P3 = P1
        "folded": pts((f(0), f(0)), (f(1), f(0)), (f(1), f(1)), (f(1), f(0))),
        "tilted corner off": pts(gp[0], gp[1], (gp[2][0], gp[2][1] + EPS), gp[3]),
    }
    for name, corners in shapes.items():
        s.expect(sat.prepare(corners) is None, f"refuse A {name}")
        s.expect(not clip.is_unit_square(clip.to_points(corners)), f"refuse B {name}")


def random_frame(rng: random.Random) -> tuple[Fraction, Fraction]:
    m = rng.randrange(2, 60)
    k = rng.randrange(1, m)
    u = geom.pythagorean(m, k)
    if rng.random() < 0.5:
        u = (u[1], u[0])
    sx, sy = rng.choice((1, -1)), rng.choice((1, -1))
    return (sx * u[0], sy * u[1])


def random_point(rng: random.Random, lo: int, hi: int) -> tuple[Fraction, Fraction]:
    def r() -> Fraction:
        return Fraction(rng.randrange(lo * 997, hi * 997), rng.choice((997, 991, 983)))

    return (r(), r())


def random_cases(s: Suite, rng: random.Random) -> None:
    # Closing along the centre line: the closed form from centres and half-widths gives
    # the time at which the margin is +eps, 0 and -eps; method A must equal it exactly.
    done = 0
    while done < 400:
        ca, cb = random_point(rng, 2, 8), random_point(rng, 2, 8)
        ua, ub = random_frame(rng), random_frame(rng)
        wa, wb = (-ua[1], ua[0]), (-ub[1], ub[0])
        if geom.closed_margin(ca, ua, wa, cb, ub, wb) <= EPS:
            continue
        try:
            t0, t1, _ = geom.closing(ca, ua, wa, cb, ub, wb, EPS)
        except ValueError:
            continue
        # eps short of contact: the margin max(g - t r) is +eps at max (g - eps) / r.
        tshort = max((g - EPS) / r for g, r in geom.axis_terms(ca, ua, wa, cb, ub, wb) if r > 0)
        done += 1
        sa, sb = rng.choice((1, -1)), rng.choice((1, -1))
        p = geom.square(ca, ua, sa, rng.randrange(4))
        for t, want in ((tshort, EPS), (t0, Fraction(0)), (t1, -EPS)):
            c2 = (cb[0] + t * (ca[0] - cb[0]), cb[1] + t * (ca[1] - cb[1]))
            q = geom.square(c2, ub, sb, rng.randrange(4))
            closed = geom.closed_margin(ca, ua, wa, c2, ub, wb)
            a, b = sat.prepare(p), sat.prepare(q)
            m = sat.margin_fraction(sat.margin(a, b))  # type: ignore[arg-type]
            s.expect(closed == want, f"random closing closed form {want}")
            s.expect(m == want, f"random closing A margin {want}")
            s.expect(sat.margin_class(sat.margin(a, b)[0]) == cls_of(want), "random closing A class")  # type: ignore[arg-type]
            s.expect(b_area(q, p)[0] == cls_of(want), f"random closing B class {want}")
    # Random pairs, near or overlapping: A's margin equals the closed form, and A's and
    # B's classes agree with its sign.
    for _ in range(300):
        ca, cb = random_point(rng, 2, 4), random_point(rng, 2, 4)
        ua, ub = random_frame(rng), random_frame(rng)
        wa, wb = (-ua[1], ua[0]), (-ub[1], ub[0])
        p = geom.square(ca, ua, rng.choice((1, -1)), rng.randrange(4))
        q = geom.square(cb, ub, rng.choice((1, -1)), rng.randrange(4))
        closed = geom.closed_margin(ca, ua, wa, cb, ub, wb)
        a, b = sat.prepare(p), sat.prepare(q)
        m = sat.margin_fraction(sat.margin(a, b))  # type: ignore[arg-type]
        s.expect(m == closed, "random pair A margin = closed form")
        s.expect(b_area(p, q)[0] == cls_of(closed), "random pair B class")
    # Random tilted squares taken to each wall: short of it, at it, past it.
    side = (20, 1)
    big = Fraction(20)
    for _ in range(300):
        ctr = random_point(rng, 3, 17)
        u = random_frame(rng)
        w = (-u[1], u[0])
        hx = geom.half_width((Fraction(1), Fraction(0)), u, w)
        hy = geom.half_width((Fraction(0), Fraction(1)), u, w)
        sense, start = rng.choice((1, -1)), rng.randrange(4)
        for k in range(4):
            for target in DELTAS:
                if k == 0:
                    c2 = (target + hx, ctr[1])
                elif k == 1:
                    c2 = (ctr[0], target + hy)
                elif k == 2:
                    c2 = (big - target - hx, ctr[1])
                else:
                    c2 = (ctr[0], big - target - hy)
                wall_case(s, geom.square(c2, u, sense, start), side, k, target, f"random wall {WALLS[k]}")


VALID = """softschema:
  contract: packing.squares:Witness/v2
  schema: witness.schema.yaml
  envelope: witness
  status: enforced
witness:
  id: W-test-n2
  n: 2
  side: 5/2
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
      - 1/3
    - - '1'
      - 1/3
    - - '1'
      - 4/3
    - - '0'
      - 4/3
  - id: 2
    corners:
    - - 3/2
      - 1/2
    - - 5/2
      - 1/2
    - - 5/2
      - 3/2
    - - 3/2
      - 3/2
  claim:
    coordinate_provenance: verified
    method: exact-algebraic
    limitations: test
  source:
    path: test.yaml
  certificate:
    kind: test
    pairs_tested: 1
"""


def twin_of(text: str) -> str:
    return json.dumps(parse_yaml(text), indent=1)


def dump(tree: object) -> str:
    return yaml.safe_dump(tree, sort_keys=False, width=10**6)


def reader_cases(s: Suite) -> None:
    def refused(yaml_text: str, json_text: str, reason: str, label: str) -> None:
        """The reader must refuse, and for the stated reason."""
        try:
            read_texts(yaml_text, json_text)
        except Refused as exc:
            message = str(exc)
        except json.JSONDecodeError:
            message = "JSON syntax"
        except yaml.YAMLError:
            message = "YAML syntax"
        else:
            s.expect(False, f"reader accepted: {label}")
            return
        s.expect(reason in message, f"{label}: refused for {message!r}, not {reason!r}")

    def own_twin(text: str) -> str:
        try:
            return twin_of(text)
        except (Refused, ValueError, yaml.YAMLError):
            return twin_of(VALID)

    def both(old: str, new: str, reason: str, label: str) -> None:
        """Change the YAML, and the twin alike where the change still parses."""
        assert VALID.count(old) >= 1, label
        changed = VALID.replace(old, new, 1)
        refused(changed, own_twin(changed), reason, label)

    # Accepted: the valid file, and the file without the optional source and certificate.
    for text, label in ((VALID, "valid"), (VALID.split("  source:")[0], "no optional keys")):
        try:
            w = read_texts(text, twin_of(text))
            s.expect(w.n == 2 and w.side == (5, 2) and w.squares[0][1] == ((1, 1), (1, 3)), f"accept {label}")
            s.expect(decide(w.side, w.squares).verdict == "ACCEPT", f"decide {label}")
        except (Refused, ValueError, yaml.YAMLError) as exc:
            s.expect(False, f"refused {label}: {exc}")
    tag = "resolved type tag:yaml.org,2002:"
    yaml_only = [
        ("    path: test.yaml\n", "    path: &a test.yaml\n", "YAML anchor", "anchor"),
        ("    kind: test\n", "    kind: *x\n", "YAML alias", "alias"),
        ("  side: 5/2\n", "  side: !!str 5/2\n", "explicit YAML tag", "explicit tag"),
        ("  side: 5/2\n", "  side: ! 5/2\n", "explicit YAML tag", "non-specific tag"),
        ("  n: 2\n", "  n: 2\n  n: 2\n", "duplicate key", "duplicate key"),
        ("    pairs_tested: 1\n", "    pairs_tested: 1\n---\nfoo: bar\n", "2 YAML documents", "two documents"),
        ("softschema:\n", "%YAML 1.1\n---\nsoftschema:\n", "YAML directive", "directive"),
        ("  n: 2\n", "  n: 2.0\n", tag + "float", "float"),
        ("  status: enforced\n", "  status: true\n", tag + "bool", "bool"),
        ("    limitations: test\n", "    limitations: ~\n", tag + "null", "null"),
        ("  n: 2\n", "  n: 0x2\n", "integer not in plain decimal", "hex integer"),
        ("  n: 2\n", "  n: 02\n", "integer not in plain decimal", "octal integer"),
        ("  n: 2\n", "  n: +2\n", "integer not in plain decimal", "signed integer"),
        ("  n: 2\n", "  n: 0_2\n", "integer not in plain decimal", "underscore integer"),
        ("    limitations: test\n", "    limitations: 2026-11-14\n", tag + "timestamp", "timestamp"),
        ("  n: 2\n", "  n: [2\n", "YAML syntax", "YAML syntax"),
        ("    kind: test\n", "    ? [a]\n    : b\n", "non-string mapping key", "non-string key"),
        ("    kind: test\n", "    <<: {a: b}\n", "non-string mapping key", "merge key"),
    ]
    for old, new, reason, label in yaml_only:
        both(old, new, reason, f"yaml {label}")
    # YAML 1.1 reads 0o2 as a string, which the twin then carries; n must be an integer.
    both("  n: 2\n", "  n: 0o2\n", "n is not a positive integer", "yaml 0o2")
    for bad in ("10/4", "5/1", "-0", "05/2", "5/02", "+5/2", "5/-2", "5 /2", "5e0/2", "1/0", "0/1", "-0/1", " 5/2", "5/2 ", "", "5//2", "0x5/2"):
        both("  side: 5/2\n", f"  side: '{bad}'\n", "side: ", f"side {bad!r}")
    both("    - - '0'\n      - 1/3\n", "    - - '-0'\n      - 1/3\n", "square 1 corner 0 x: not a canonical", "coordinate -0")
    both("    - - '0'\n      - 1/3\n", "    - - 0\n      - 1/3\n", "square 1 corner 0 x: not a string", "coordinate int")
    both("    - - '0'\n      - 1/3\n", "    - - '0'\n      - 2/6\n", "square 1 corner 0 y: not in lowest terms", "coordinate not reduced")
    both("  side: 5/2\n", "  side: '0'\n", "side is not positive", "side zero")
    both("  side: 5/2\n", "  side: -5/2\n", "side is not positive", "side negative")
    structural = [
        ("softschema:\n", "extra: 1\nsoftschema:\n", "top level: unexpected", "extra top key"),
        ("  status: enforced\n", "  status: enforced\n  extra: x\n", "softschema: unexpected", "extra envelope key"),
        ("  status: enforced\n", "", "softschema: missing", "missing envelope key"),
        ("  n: 2\n", "  n: 2\n  extra: x\n", "witness: unexpected", "extra witness key"),
        ("  square_size: '1'\n", "", "witness: missing", "missing square_size"),
        ("  claim:\n    coordinate_provenance: verified\n    method: exact-algebraic\n    limitations: test\n", "", "witness: missing", "missing claim"),
        ("    limitations: test\n", "    limitations: test\n    extra: x\n", "claim: unexpected", "extra claim key"),
        ("    path: test.yaml\n", "    path: test.yaml\n    extra: x\n", "source: unexpected", "extra source key"),
        ("  - id: 2\n    corners:\n", "  - id: 2\n    angle: '0'\n    corners:\n", "square 2: unexpected", "extra square key"),
        ("Witness/v2", "Witness/v1", "contract is not", "contract"),
        ("  envelope: witness\n", "  envelope: other\n", "envelope is not", "envelope"),
        ("  representation: corners\n", "  representation: center-angle\n", "representation is not", "representation"),
        ("    kind: rational\n", "    kind: decimal\n", "scalar is not", "scalar kind"),
        ("    kind: rational\n", "    kind: rational\n    extra: x\n", "scalar is not", "scalar extra"),
        ("    origin: lower-left\n", "    origin: container-center\n", "coordinates are not", "origin"),
        ("    angle_unit: not-applicable\n", "    angle_unit: degrees\n", "coordinates are not", "angle unit"),
        ("  square_size: '1'\n", "  square_size: '2'\n", "square_size is not", "square size 2"),
        ("  square_size: '1'\n", "  square_size: 1\n", "square_size is not", "square size int"),
        ("  n: 2\n", "  n: 3\n", "2 entries for n = 3", "n mismatch"),
        ("  n: 2\n", "  n: 0\n", "n is not a positive integer", "n zero"),
        ("  - id: 2\n", "  - id: 3\n", "square 2: id", "id out of order"),
        ("  - id: 1\n", "  - id: '1'\n", "square 1: id", "id string"),
        ("  id: W-test-n2\n", "  id: w-test-n2\n", "witness id", "witness id"),
        ("    method: exact-algebraic\n", "    method: guess\n", "claim.method", "claim method"),
        ("    coordinate_provenance: verified\n", "    coordinate_provenance: proved\n", "claim.coordinate_provenance", "claim provenance"),
        ("    - - '0'\n      - 4/3\n", "", "square 1: not four corners", "three corners"),
        ("    - - '0'\n      - 1/3\n", "    - - '0'\n      - 1/3\n      - 1/3\n", "square 1 corner 0: not a point", "three coordinates"),
        ("  certificate:\n    kind: test\n    pairs_tested: 1\n", "  certificate: []\n", "certificate is not a mapping", "certificate not a mapping"),
    ]
    for old, new, reason, label in structural:
        both(old, new, reason, label)
    tree = parse_yaml(VALID)
    tree["witness"]["squares"] = {"a": "b"}  # type: ignore[index]
    refused(dump(tree), json.dumps(tree), "squares is not a sequence", "squares not a sequence")
    twin = twin_of(VALID)
    differs = "twin differs at "
    twin_cases = [
        (twin.replace('"5/2"', '"5/3"', 1), differs + "$.witness.side", "twin side differs"),
        (twin.replace('"n": 2', '"n": 2.0', 1), "twin float", "twin float"),
        (twin.replace('"pairs_tested": 1', '"pairs_tested": NaN', 1), "twin constant", "twin NaN"),
        (twin.replace('"pairs_tested": 1', '"pairs_tested": Infinity', 1), "twin constant", "twin Infinity"),
        (twin.replace('"n": 2', '"n": 2, "n": 2', 1), "twin duplicate key", "twin duplicate key"),
        (twin.replace('"n": 2', '"n": "2"', 1), differs + "$.witness.n: int vs str", "twin type str"),
        (twin.replace('"n": 2', '"n": true', 1), differs + "$.witness.n: int vs bool", "twin type bool"),
        (twin.replace('"pairs_tested": 1', '"pairs_tested": -0', 1), "twin integer not canonical", "twin -0"),
        (twin.replace('"n": 2', '"n": 2, "extra": 1', 1), differs + "$.witness: keys", "twin extra key"),
        (twin.replace('"limitations": "test"', '"limitations": "test "', 1), differs + "$.witness.claim.limitations", "twin string differs"),
        (twin.replace('"pairs_tested": 1', '"pairs_tested": 1e0', 1), "twin float", "twin exponent"),
        (twin[:-3], "JSON syntax", "twin syntax"),
        (json.dumps({"softschema": {}, "witness": {}}), differs + "$.softschema: keys", "twin other tree"),
    ]
    for text, reason, label in twin_cases:
        refused(VALID, text, reason, label)
    # A whole-file decision on small files: an overlap, a square outside, a non-square,
    # and an edge-to-edge contact (square 2 moved to [1, 2] x [1/3, 4/3]).
    w = read_texts(VALID, twin_of(VALID))
    sq = list(w.squares)
    d = decide(w.side, [sq[0], sq[0]])
    s.expect(d.verdict == "REFUSE" and d.class_a.get((1, 2)) == "overlap", "decide duplicate")
    moved = geom.translate(sq[1], (Fraction(1, 10**30), Fraction(0)))
    d = decide(w.side, [sq[0], moved])
    s.expect(d.verdict == "REFUSE" and d.wall_a[1][2] == "cross", "decide outside")
    d = decide(w.side, [sq[0], (sq[1][0], sq[1][1], ((5, 2), (8, 5)), sq[1][3])])
    s.expect(d.verdict == "REFUSE" and d.stopped is not None, "decide not unit")
    d = decide(w.side, [sq[0], geom.translate(sq[1], (Fraction(-1, 2), Fraction(-1, 6)))])
    s.expect(d.verdict == "ACCEPT" and d.class_a[(1, 2)] == "contact", "decide contact")


def run_suite() -> Suite:
    s = Suite()
    contact_cases(s)
    wall_cases(s)
    sense_cases(s)
    refusal_cases(s)
    random_cases(s, random.Random(20261114))
    reader_cases(s)
    return s


def with_patch(module: object, name: str, replacement: Callable[..., object]) -> Suite:
    original = getattr(module, name)
    setattr(module, name, replacement)
    try:
        return run_suite()
    finally:
        setattr(module, name, original)


def main(argv: list[str]) -> int:
    out_path = Path(argv[1])
    started = time.process_time()
    s = run_suite()
    broken_a = with_patch(sat, "margin_class", lambda g: "apart" if g >= 0 else "overlap")
    broken_b = with_patch(clip, "inside", lambda v: v > 0)
    passed = not s.failures and broken_a.failures and broken_b.failures
    receipt = {
        "program": "l159_selftest.py",
        "verdict": "PASSED" if passed else "FAILED",
        "cases": s.cases,
        "failed": len(s.failures),
        "failures": s.failures[:50],
        "broken_method_a_zero_margin_apart": {"cases": broken_a.cases, "failed": len(broken_a.failures)},
        "broken_method_b_open_half_planes": {"cases": broken_b.cases, "failed": len(broken_b.failures)},
        "cpu_seconds": round(time.process_time() - started, 1),
    }
    out_path.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    print(receipt["verdict"], s.cases, "cases", len(s.failures), "failed;", "broken A fails", len(broken_a.failures), "; broken B fails", len(broken_b.failures))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
