"""Lane L163 self-test: both methods and the reader against cases with known answers.

Usage: l163_selftest.py OUT.json

Every case's answer is derived by hand or by the closed form of `l163_geom` (corner
projections in fractions), not by either method. The suite is then run twice more
against deliberately broken copies, method A counting a zero margin as apart and
method B clipping with open half-planes; each must fail.
"""

from __future__ import annotations

import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from collections.abc import Callable  # noqa: E402
from fractions import Fraction as F  # noqa: E402

import l163_clip as clip  # noqa: E402
import l163_geom as geom  # noqa: E402
import l163_sat as sat  # noqa: E402
from gmpy2 import mpq  # noqa: E402
from l163_decide import decide  # noqa: E402
from l163_reader import Certificate, Refused, read_cert_text, read_json_text  # noqa: E402

DELTAS = [F(1, 10**30), F(0), F(-1, 10**30)]
Row = geom.Row


class Tally:
    def __init__(self) -> None:
        self.cases = 0
        self.failed: list[str] = []

    def check(self, name: str, ok: bool) -> None:
        self.cases += 1
        if not ok:
            self.failed.append(name)


def q(x: F) -> mpq:
    return mpq(x.numerator, x.denominator)


def equivalents(t: F) -> list[F]:
    """t for the same square at theta, theta + 90, theta + 180 and theta - 90 degrees."""
    out = [t]
    if t != 1:
        out.append((t + 1) / (1 - t))
    if t != 0:
        out.append(-1 / t)
    if t != -1:
        out.append((t - 1) / (1 + t))
    return out


def with_t(r: Row, t: F) -> Row:
    cx, cy, _ = geom.parts(r)
    return geom.row(cx, cy, t)


def expect_pair(tally: Tally, name: str, ri: Row, rj: Row, delta: F, area: F) -> None:
    """Margin exactly delta by A (and by the closed form); B's class and area as derived."""
    for ti in equivalents(geom.parts(ri)[2]):
        for tj in equivalents(geom.parts(rj)[2]):
            a, b = with_t(ri, ti), with_t(rj, tj)
            for x, y, order in ((a, b, "ij"), (b, a, "ji")):
                tag = f"{name} d={geom.sci(delta, 2)} {order}"
                want = "apart" if delta > 0 else ("touch" if delta == 0 else "overlap")
                m = sat.margin(sat.prepare(x), sat.prepare(y))
                tally.check(tag + " A margin", m == delta)
                tally.check(tag + " A class", sat.classify(m) == want)
                cls, ar = clip.pair_class(clip.corners(x), clip.corners(y))
                tally.check(tag + " B class", cls == want)
                tally.check(tag + " B area", ar == q(area))
    tally.check(name + " closed form", geom.margin(ri, rj) == delta)


def pair_cases(tally: Tally) -> None:
    h = F(1, 2)
    t345 = F(1, 2)  # cos 3/5, sin 4/5
    c, s = geom.cos_sin(t345)
    for d in DELTAS:
        ad = -d if d < 0 else F(0)
        # edge to edge, upright, four directions
        for vx, vy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            expect_pair(tally, f"edge upright {vx},{vy}", geom.row(F(0), F(0), F(0)), geom.row((1 + d) * vx, (1 + d) * vy, F(0)), d, ad)
        # edge to edge with an offset of 1/3 along the edge
        expect_pair(tally, "edge upright offset", geom.row(F(0), F(0), F(0)), geom.row(1 + d, F(1, 3), F(0)), d, ad * F(2, 3))
        # edge to edge, both turned by (3/5, 4/5), along u and v
        for ux, uy in ((c, s), (-s, c), (-c, -s), (s, -c)):
            expect_pair(tally, f"edge 3-4-5 {ux},{uy}", geom.row(F(1, 7), F(2, 9), t345), geom.row(F(1, 7) + (1 + d) * ux, F(2, 9) + (1 + d) * uy, t345), d, ad)
        # corner to corner, upright and turned
        for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            expect_pair(tally, f"corner upright {sx},{sy}", geom.row(F(0), F(0), F(0)), geom.row((1 + d) * sx, (1 + d) * sy, F(0)), d, ad * ad)
            off = (sx * c - sy * s, sx * s + sy * c)
            expect_pair(tally, f"corner 3-4-5 {sx},{sy}", geom.row(F(0), F(0), t345), geom.row((1 + d) * off[0], (1 + d) * off[1], t345), d, ad * ad)
        # a corner of a (3/5, 4/5) square on an upright edge, under each quarter turn of the plane
        x0 = h + F(7, 10) + d
        for k in range(4):
            cx, cy = x0, F(0)
            for _ in range(k):
                cx, cy = -cy, cx
            expect_pair(tally, f"vertex on edge turn {k}", geom.row(F(0), F(0), F(0)), geom.row(cx, cy, t345), d, F(25, 24) * ad * ad)
    # duplicates and concentric turns
    for t in (F(0), t345, F(1, 3), F(2, 3)):
        r = geom.row(F(3, 5), F(-1, 4), t)
        expect_pair(tally, f"duplicate t={t}", r, r, F(-1), F(1))
    for t, cs_ in ((t345, (F(3, 5), F(4, 5))), (F(1, 3), (F(4, 5), F(3, 5)))):
        cc, ss = cs_
        want_m = -(1 + cc + ss) / 2
        want_a = 1 - (cc + ss - 1) ** 2 / (2 * cc * ss)
        expect_pair(tally, f"concentric t={t}", geom.row(F(0), F(0), F(0)), geom.row(F(0), F(0), t), want_m, want_a)


def wall_cases(tally: Tally) -> None:
    side = F(10)
    for t in (F(0), F(1, 2), F(2, 3), F(1, 5), F(-3, 7)):
        base = geom.row(F(5), F(5), t)
        for w in range(4):
            for d in DELTAS:  # d > 0 inside by d, 0 contact, d < 0 outside
                r = geom.to_wall(base, w, side, -d)
                tag = f"wall {w} t={t} d={geom.sci(d, 2)}"
                cl = sat.clearances(sat.prepare(r), (10, 1))
                tally.check(tag + " closed form", geom.clearances(r, side)[w] == d)
                tally.check(tag + " A clearance", cl[w] == d)
                tally.check(tag + " A others", all(cl[k] > 1 for k in range(4) if k != w))
                cls, inside = clip.wall_classes(clip.corners(r), mpq(10))
                want = "apart" if d > 0 else ("contact" if d == 0 else "crossing")
                tally.check(tag + " B class", cls[w] == want)
                tally.check(tag + " B others", all(cls[k] == "apart" for k in range(4) if k != w))
                tally.check(tag + " B inside", (inside == 1) == (d >= 0))


def unit_cases(tally: Tally) -> None:
    for t in (F(0), F(1, 2), F(-5, 12), F(113354474907616, 487215704657665), F(1, 10**30)):
        r = geom.row(F(1, 3), F(2, 7), t)
        pts = clip.corners(r)
        tally.check(f"unit A t={t}", sat.is_unit(sat.prepare(r)))
        tally.check(f"unit B t={t}", clip.is_unit_square(pts))
        tally.check(f"ccw B t={t}", clip.twice_signed_area(pts) == 2)
        tally.check(f"cw B reversed t={t}", clip.twice_signed_area(pts[::-1]) == -2)
    # shapes method B must refuse as unit squares
    e = mpq(1, 10**30)
    z, o = mpq(0), mpq(1)
    bad = {
        "rhombus 3-4-5": [(z, z), (o, z), (o + mpq(3, 5), mpq(4, 5)), (mpq(3, 5), mpq(4, 5))],
        "bowtie": [(z, z), (o, o), (o, z), (z, o)],
        "rectangle": [(z, z), (o + e, z), (o + e, o), (z, o)],
        "third corner off": [(z, z), (o, z), (o + e, o), (z, o)],
        "side 2": [(z, z), (mpq(2), z), (mpq(2), mpq(2)), (z, mpq(2))],
        "point": [(z, z)] * 4,
        "three points": [(z, z), (o, z), (o, o)],
    }
    for name, pts in bad.items():
        tally.check(f"B refuses {name}", not clip.is_unit_square(pts))
    tally.check("A refuses (3, 4, 6)", not sat.is_unit(sat.Sq(0, 0, 1, 3, 4, 6)))
    tally.check("A refuses r = 0", not sat.is_unit(sat.Sq(0, 0, 1, 0, 0, 0)))


def random_cases(tally: Tally, rng: random.Random) -> None:
    def rt() -> F:
        return F(rng.randint(-60, 60), rng.randint(1, 60))

    def rc(lo: float, hi: float) -> F:
        den = rng.randint(10**18, 10**20)
        return F(rng.randint(int(lo * den), int(hi * den)), den)

    done = 0
    while done < 300:
        ri = geom.row(rc(-1, 1), rc(-1, 1), rt())
        rj = geom.row(rc(-2.5, 2.5), rc(-2.5, 2.5), rt())
        m = sat.margin(sat.prepare(ri), sat.prepare(rj))
        g = geom.margin(ri, rj)
        cls, _ = clip.pair_class(clip.corners(ri), clip.corners(rj))
        tally.check(f"random {done} A = closed form", m == g)
        tally.check(f"random {done} B class", cls == sat.classify(g))
        done += 1
    done = 0
    while done < 300:
        ri = geom.row(rc(-1, 1), rc(-1, 1), rt())
        rj = geom.row(rc(-3, 3), rc(-3, 3), rt())
        if geom.margin(ri, rj) <= F(1, 10**6):
            continue
        for d in DELTAS:  # -d is the target margin: short, at, past contact
            try:
                moved, _ = geom.close_pair(ri, rj, d)
            except ValueError:
                tally.check(f"close {done} geometry", False)
                continue
            m = sat.margin(sat.prepare(ri), sat.prepare(moved))
            cls, _ = clip.pair_class(clip.corners(ri), clip.corners(moved))
            tally.check(f"close {done} d={geom.sci(d, 2)} A", m == -d)
            tally.check(f"close {done} d={geom.sci(d, 2)} closed form", geom.margin(ri, moved) == -d)
            tally.check(f"close {done} d={geom.sci(d, 2)} B", cls == sat.classify(-d))
        done += 1
    side = F(20)
    for k in range(300):
        base = geom.row(rc(5, 15), rc(5, 15), rt())
        w = k % 4
        for d in DELTAS:
            r = geom.to_wall(base, w, side, d)
            cl = sat.clearances(sat.prepare(r), (20, 1))[w]
            cls, inside = clip.wall_classes(clip.corners(r), mpq(20))
            tally.check(f"random wall {k} A", cl == -d)
            tally.check(f"random wall {k} B", cls[w] == sat.wall_class(-d))
            tally.check(f"random wall {k} B inside", (inside == 1) == (d <= 0))


GOOD_JSON = '{"n": 2, "side": "3/1", "squares": [{"cx": "1/2", "cy": "1/2", "t": "0/1"}, {"cx": "3/2", "cy": "1/2", "t": "0/1"}]}'
GOOD_CERT = "# two squares\n# x y t\n2 3\n1/2 1/2 0\n3/2 1/2 0/1\n"


def reader_cases(tally: Tally) -> None:
    def refused(name: str, fn: Callable[[], Certificate], why: str) -> None:
        try:
            fn()
        except Refused as exc:
            tally.check(f"reader refuses {name}", why in exc.reason)
            return
        tally.check(f"reader refuses {name}", False)

    def j(text: str) -> Callable[[], Certificate]:
        return lambda: read_json_text(text)

    def c(text: str) -> Callable[[], Certificate]:
        return lambda: read_cert_text(text)

    sq = '{"cx": "1/2", "cy": "1/2", "t": "0/1"}'
    cases_json = {
        "float n": ('{"n": 1.0, "side": "3/1", "squares": [' + sq + "]}", "float"),
        "float scalar": ('{"n": 1, "side": 3.5, "squares": [' + sq + "]}", "float"),
        "NaN": ('{"n": 1, "side": NaN, "squares": [' + sq + "]}", "constant"),
        "duplicate top key": ('{"n": 1, "n": 1, "side": "3/1", "squares": [' + sq + "]}", "duplicate"),
        "duplicate square key": ('{"n": 1, "side": "3/1", "squares": [{"cx": "1/2", "cx": "1/2", "cy": "1/2", "t": "0/1"}]}', "duplicate"),
        "unknown key": ('{"n": 1, "side": "3/1", "extra": 1, "squares": [' + sq + "]}", "unknown keys"),
        "missing side": ('{"n": 1, "squares": [' + sq + "]}", "missing keys"),
        "square extra key": ('{"n": 1, "side": "3/1", "squares": [{"cx": "1/2", "cy": "1/2", "t": "0/1", "id": "1/1"}]}', "keys"),
        "square missing t": ('{"n": 1, "side": "3/1", "squares": [{"cx": "1/2", "cy": "1/2"}]}', "keys"),
        "count": ('{"n": 2, "side": "3/1", "squares": [' + sq + "]}", "entries"),
        "n bool": ('{"n": true, "side": "3/1", "squares": [' + sq + "]}", "positive integer"),
        "n string": ('{"n": "1", "side": "3/1", "squares": [' + sq + "]}", "positive integer"),
        "number scalar": ('{"n": 1, "side": 3, "squares": [' + sq + "]}", "not a string"),
        "integer string in JSON": ('{"n": 1, "side": "3", "squares": [' + sq + "]}", "not p/q"),
        "decimal string": ('{"n": 1, "side": "3.5/1", "squares": [' + sq + "]}", "not p/q"),
        "plus sign": ('{"n": 1, "side": "+3/1", "squares": [' + sq + "]}", "not p/q"),
        "leading zero num": ('{"n": 1, "side": "03/1", "squares": [' + sq + "]}", "not p/q"),
        "leading zero den": ('{"n": 1, "side": "3/01", "squares": [' + sq + "]}", "not p/q"),
        "zero den": ('{"n": 1, "side": "3/0", "squares": [' + sq + "]}", "not p/q"),
        "negative den": ('{"n": 1, "side": "3/-1", "squares": [' + sq + "]}", "not p/q"),
        "negative zero": ('{"n": 1, "side": "3/1", "squares": [{"cx": "1/2", "cy": "1/2", "t": "-0/1"}]}', "negative zero"),
        "not lowest": ('{"n": 1, "side": "6/2", "squares": [' + sq + "]}", "lowest terms"),
        "spaces": ('{"n": 1, "side": " 3/1", "squares": [' + sq + "]}", "not p/q"),
        "side zero": ('{"n": 1, "side": "0/1", "squares": [' + sq + "]}", "not positive"),
        "side negative": ('{"n": 1, "side": "-3/1", "squares": [' + sq + "]}", "not positive"),
        "squares not list": ('{"n": 1, "side": "3/1", "squares": ' + sq + "}", "not a list"),
        "top list": ("[1]", "not an object"),
        "not JSON": ('{"n": 1,', "not JSON"),
        "info not string": ('{"n": 1, "side": "3/1", "side_decimal_info_only": 3, "squares": [' + sq + "]}", "not a string"),
        "square not object": ('{"n": 1, "side": "3/1", "squares": [["1/2", "1/2", "0/1"]]}', "not an object"),
    }
    for name, (text, why) in cases_json.items():
        refused(name, j(text), why)
    cases_cert = {
        "no header": ("# only\n", "no header"),
        "header three fields": ("1 3 4\n1/2 1/2 0\n", "header"),
        "count": ("2 3\n1/2 1/2 0\n", "entries"),
        "extra field": ("1 3\n1/2 1/2 0 0\n", "fields"),
        "double space": ("1 3\n1/2  1/2 0\n", "single-space"),
        "tab": ("1 3\n1/2\t1/2 0\n", "single-space"),
        "trailing space": ("1 3\n1/2 1/2 0 \n", "single-space"),
        "comment after header": ("1 3\n# late\n1/2 1/2 0\n", "entries"),
        "negative zero int": ("1 3\n1/2 1/2 -0\n", "negative zero"),
        "zero den": ("1 3\n1/2 1/0 0\n", "not p/q"),
        "not lowest": ("1 3\n2/4 1/2 0\n", "lowest terms"),
        "blank line": ("1 3\n\n1/2 1/2 0\n", "single-space"),
        "n zero": ("0 3\n", "not positive"),
        "decimal": ("1 3\n0.5 1/2 0\n", "not p/q"),
    }
    for name, (text, why) in cases_cert.items():
        refused("cert " + name, c(text), why)
    a = read_json_text(GOOD_JSON)
    b = read_cert_text(GOOD_CERT)
    tally.check("reader accepts good JSON", a.n == 2 and a.side == (3, 1))
    tally.check("reader accepts good cert", b.n == 2 and b.squares[0] == (1, 2, 1, 2, 0, 1))
    tally.check("good twins equal", a.tree() == b.tree())


def file_cases(tally: Tally) -> None:
    def cert(side: F, rows: list[Row]) -> Certificate:
        return Certificate(len(rows), (side.numerator, side.denominator), tuple(rows))

    h = F(1, 2)
    e = F(1, 10**30)
    dup = decide(cert(F(3), [geom.row(h, h, F(0)), geom.row(h, h, F(0))]))
    tally.check("file duplicate refused", not dup.accepted() and dup.overlapping() == [(1, 2)])
    out = decide(cert(F(3), [geom.row(h - e, h, F(0)), geom.row(F(5, 2), h, F(0))]))
    tally.check("file outside refused", not out.accepted() and out.crossings() == [(1, "left")])
    edge = decide(cert(F(2), [geom.row(h, h, F(0)), geom.row(F(3, 2), h, F(0))]))
    tally.check("file edge contact accepted", edge.accepted() and edge.touching() == [(1, 2)])
    tally.check("file edge contact walls", sorted(edge.contacts()) == [(1, "bottom"), (1, "left"), (2, "bottom"), (2, "right")])
    tilt = geom.row(F(7, 10), F(7, 10), F(1, 2))  # half-extent 7/10: touches left and bottom
    corner = decide(cert(F(3), [tilt]))
    tally.check("file tilted corner contacts", corner.accepted() and sorted(corner.contacts()) == [(1, "bottom"), (1, "left")])


def suite(seed: int) -> Tally:
    tally = Tally()
    pair_cases(tally)
    wall_cases(tally)
    unit_cases(tally)
    random_cases(tally, random.Random(seed))
    reader_cases(tally)
    file_cases(tally)
    return tally


def main() -> None:
    out = sys.argv[1]
    t0 = time.process_time()
    good = suite(163)
    # broken method A: a zero margin counted as apart
    keep_a = sat.classify
    sat.classify = lambda m: "apart" if m >= 0 else "overlap"  # type: ignore[assignment]
    broken_a = suite(163)
    sat.classify = keep_a
    # broken method B: clipping with open half-planes
    keep_b = clip.clip

    def open_clip(poly: list[clip.Point], side: Callable[[clip.Point], mpq]) -> list[clip.Point]:
        return keep_b(poly, lambda p: side(p) if side(p) != 0 else mpq(-1))

    clip.clip = open_clip  # type: ignore[assignment]
    broken_b = suite(163)
    clip.clip = keep_b
    verdict = "PASSED" if not good.failed and broken_a.failed and broken_b.failed else "FAILED"
    rec = {
        "lane": "L163",
        "program": "l163_selftest.py",
        "cases": good.cases,
        "failed": len(good.failed),
        "failed_names": good.failed[:20],
        "broken_method_a_failures": len(broken_a.failed),
        "broken_method_b_failures": len(broken_b.failed),
        "verdict": verdict,
        "cpu_seconds": round(time.process_time() - t0, 1),
        "versions": {"python": sys.version.split()[0], **clip.versions()},
    }
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1)
    print(verdict, good.cases, "cases", len(good.failed), "failed; broken A", len(broken_a.failed), "broken B", len(broken_b.failed))


if __name__ == "__main__":
    main()
