"""Self-test of lane r1021-1118's programs on hand-derived cases, and broken copies.

Usage: python -I -B r1021_selftest.py OUT.json

Every expected value below was derived by hand (the derivations are in the comments).
The test then breaks the programs in ten ways, one at a time (each a plausible
mistake), and requires every broken copy to fail at least one check; a broken copy
that passes every check means the checks are too weak.  Reads no certificate.
"""

from __future__ import annotations

import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # this packet's programs/, run with -I

import json
from fractions import Fraction as F

import r1021_check as chk
import r1021_clip as clipmod
import r1021_contract as con
import r1021_fmt as fmt
import r1021_geom as geom
import r1021_identity as ident
import r1021_read as rd

H = F(1, 2)
U = (F(1), F(0))  # upright
R34 = (F(3, 5), F(4, 5))  # a Pythagorean direction


def pose(x, y, d=U):
    return (F(x), F(y), d[0], d[1])


def b_class(pi, pj):
    c1, a1, c2, a2 = clipmod.decide_pair(geom.corners_of(pi), geom.corners_of(pj))
    return c1, a1, c2, a2


def checks() -> list:
    out = []

    def ok(name, cond):
        out.append((name, bool(cond)))

    a = pose(H, H)
    # 1. edge contact: centres 1 apart on x, upright: margin |dx| - H = 1 - 1 = 0
    b = pose(F(3, 2), H)
    ok("edge contact margin 0", geom.margin(geom.int_pose(a), geom.int_pose(b)) == 0)
    ok("edge contact B", b_class(a, b)[0::2] == ("contact", "contact"))
    # 2. apart by 1/10
    b = pose(F(8, 5), H)
    ok("apart margin 1/10", geom.margin(geom.int_pose(a), geom.int_pose(b)) == F(1, 10))
    ok("apart B", b_class(a, b)[0::2] == ("apart", "apart"))
    # 3. overlap by 1/10: the strip [9/10, 1] x [0, 1] has area 1/10
    b = pose(F(7, 5), H)
    ok("overlap margin -1/10", geom.margin(geom.int_pose(a), geom.int_pose(b)) == F(-1, 10))
    c1, a1, c2, a2 = b_class(a, b)
    ok("overlap B area 1/10 both ways", (c1, c2) == ("overlap", "overlap") and a1 == a2 == F(1, 10))
    # 4. vertex contact at (1, 1)
    b = pose(F(3, 2), F(3, 2))
    ok("vertex contact margin 0", geom.margin(geom.int_pose(a), geom.int_pose(b)) == 0)
    ok("vertex contact B", b_class(a, b)[0::2] == ("contact", "contact"))
    # 5. the separating axis is the upright square's: i turned (3/5, 4/5), j upright at dx = 13/10.
    #    H = 1/2 + (3/5 + 4/5)/2 = 6/5; on j's axes |dx| = 13/10; margin 1/10.
    i5 = pose(H, H, R34)
    j5 = pose(H + F(13, 10), H)
    ok("j-axis apart margin 1/10", geom.margin(geom.int_pose(i5), geom.int_pose(j5)) == F(1, 10))
    ok("j-axis apart B", b_class(i5, j5)[0::2] == ("apart", "apart"))
    ok("j-axis apart, reversed pair", geom.margin(geom.int_pose(j5), geom.int_pose(i5)) == F(1, 10))
    # 6. vertex of the turned square on the upright square's edge: dx = 6/5
    j6 = pose(H + F(6, 5), H)
    ok("turned vertex contact margin 0", geom.margin(geom.int_pose(i5), geom.int_pose(j6)) == 0)
    ok("turned vertex contact B", b_class(i5, j6)[0::2] == ("contact", "contact"))
    # 7. the vertex 1/10 inside: a triangle of base 3/40 + 2/15 = 5/24 and height 1/10, area 1/96
    j7 = pose(H + F(11, 10), H)
    ok("turned vertex overlap margin -1/10", geom.margin(geom.int_pose(i5), geom.int_pose(j7)) == F(-1, 10))
    c1, a1, c2, a2 = b_class(i5, j7)
    ok("turned vertex overlap area 1/96", (c1, c2) == ("overlap", "overlap") and a1 == a2 == F(1, 96))
    # 8. identical squares: d = 0, margin -H = -1, area 1
    ok("identical margin -1", geom.margin(geom.int_pose(a), geom.int_pose(a)) == -1)
    c1, a1, c2, a2 = b_class(a, a)
    ok("identical area 1", (c1, c2) == ("overlap", "overlap") and a1 == a2 == 1)
    # 9. walls: the unit square in [0, 1]^2 touches all four; in [0, 99/100]^2 it crosses right and top
    ok("clearances in side 1", geom.clearances(a, F(1)) == (0, 0, 0, 0))
    ok("clearances in side 99/100", geom.clearances(a, F(99, 100)) == (0, 0, F(-1, 100), F(-1, 100)))
    bd = clipmod.decide_corners([geom.corners_of(a)], F(99, 100))
    ok("B walls in side 99/100", bd["walls"][0] == ("contact", "contact", "overlap", "overlap")
       and bd["inside_area"][0] == F(9801, 10000))
    # 10. the turned square (3/5, 4/5) has half-extent 7/10; centred at (7/10, 7/10) in side 7/5 it touches all walls
    t = pose(F(7, 10), F(7, 10), R34)
    ok("turned clearances 0", geom.clearances(t, F(7, 5)) == (0, 0, 0, 0))
    bd = clipmod.decide_corners([geom.corners_of(t)], F(7, 5))
    ok("turned B touching, area 1", bd["walls"][0] == ("contact",) * 4 and bd["inside_area"][0] == 1)
    # 11. a non-unit direction
    bad = (H, H, F(3, 5), F(3, 5))
    ok("non-unit direction refused by A", not geom.is_unit(bad))
    ok("non-unit corners refused by B", not clipmod.is_unit_square(clipmod.to_mpq(geom.corners_of(bad))))
    # 12. a unit rhombus: sides 1, diagonals 16/5 and 4/5; and a square listed in crossing order
    rh = ((F(0), F(0)), (F(1), F(0)), (F(8, 5), F(4, 5)), (F(3, 5), F(4, 5)))
    ok("rhombus is not a unit square (A)", not geom.pose_of_corners(rh)[0])
    ok("rhombus is not a unit square (B)", not clipmod.is_unit_square(clipmod.to_mpq(rh)))
    q = geom.corners_of(a)
    crossed = (q[0], q[2], q[1], q[3])
    ok("crossed listing refused (A)", not geom.pose_of_corners(crossed)[0])
    ok("crossed listing refused (B)", not clipmod.is_unit_square(clipmod.to_mpq(crossed)))
    # 13. the twin: offset 2 counterclockwise, the reverse clockwise, a swap none
    e = geom.corners_of(i5)
    ok("twin offset 2 ccw", geom.twin_match((e[2], e[3], e[0], e[1]), i5) == (2, "ccw"))
    ok("twin reversed cw", geom.twin_match((e[2], e[1], e[0], e[3]), i5) == (2, "cw"))
    ok("twin swap is none", geom.twin_match((e[0], e[2], e[1], e[3]), i5) is None)
    u5, p5 = geom.pose_of_corners((e[2], e[3], e[0], e[1]))
    ok("pose of corners", u5 and (p5[0], p5[1]) == (i5[0], i5[1]) and (p5[2], p5[3]) == (i5[2], i5[3]))
    # 14. margins from corners equal A's on cases 1-8
    for name, (pi, pj) in {"c1": (a, pose(F(3, 2), H)), "c3": (a, pose(F(7, 5), H)), "c5": (i5, j5),
                           "c7": (i5, j7), "c8": (a, a)}.items():
        ok(f"C0 {name}", clipmod.margin_from_corners(geom.corners_of(pi), geom.corners_of(pj))
           == geom.margin(geom.int_pose(pi), geom.int_pose(pj)))
    # 15. contraction, three binding pairs: (1/2,1/2), (5/2,1/2), (1/2,5/2) in side 3; lambda* = 1/2, shrunk side 2
    p3 = [pose(H, H), pose(F(5, 2), H), pose(H, F(5, 2))]
    c = con.contraction(p3, F(3))
    ok("contraction lambda 1/2", c["lambda"] == H and c["binding"] == [(0, 1), (0, 2), (1, 2)])
    ok("contraction shrunk side 2, margin 1", c["shrunk_side"] == 2 and c["margin"] == 1)
    # 16. unequal factors: (1/2,1/2), (2,1/2), (1/2,3) in side 7/2: factors 2/3, 2/5, 2/5; shrunk side 8/3
    pu = [pose(H, H), pose(F(2), H), pose(H, F(3))]
    c = con.contraction(pu, F(7, 2))
    ok("unequal factors lambda 2/3", c["lambda"] == F(2, 3) and c["binding"] == [(0, 1)] and c["next_factor"] == F(2, 5))
    ok("unequal factors shrunk 8/3, margin 5/6", c["shrunk_side"] == F(8, 3) and c["margin"] == F(5, 6))
    dk = chk.decide(c["shrunk_poses"], [geom.corners_of(p) for p in c["shrunk_poses"]], c["shrunk_side"])
    ok("shrunk packing accepted, binding pair touching", dk["accept"] and dk["a_classes"] == ["contact", "apart", "apart"])
    # 17. option D on it: a successor at 3 is not new (3 > 8/3); at 5/2 it is, 1/6 below the shrunk side
    od = con.option_d(F(7, 2), c, F(3))
    ok("option D not new", not od["new_under_option_d"] and od["gain"] == H and od["gain_over_margin"] == F(3, 5))
    od = con.option_d(F(7, 2), c, F(5, 2))
    ok("option D new", od["new_under_option_d"] and od["successor_below_shrunk_predecessor_by"] == F(1, 6))
    # 18. identity: a packing against itself, and against its mirror image
    pk = [pose(H, H), pose(F(2), H, R34), pose(H, F(3))]
    m = ident.measure(pk, F(7, 2), pk, F(7, 2))
    row = [r for r in m["rows"] if r["frame"] == "lower-left" and r["symmetry"] == "identity"][0]
    ok("identity against itself", row["nearest_one_to_one"] and row["index_kept"] and row["beyond"]["1e-9"] == 0
       and row["orientation_kept"] == 3)
    mir = [(F(7, 2) - x, y, -cc, ss) for x, y, cc, ss in pk]
    m = ident.measure(pk, F(7, 2), mir, F(7, 2))
    row = [r for r in m["rows"] if r["frame"] == "lower-left" and r["symmetry"] == "mirror-x"][0]
    ok("identity against the mirror", m["nearest_symmetry"]["lower-left"] == "mirror-x" and row["beyond"]["1e-9"] == 0
       and row["orientation_kept"] == 3)
    rq = [(x, y, -ss, cc) for x, y, cc, ss in pk]  # the same squares, each by another edge direction
    m = ident.measure(pk, F(7, 2), rq, F(7, 2))
    row = [r for r in m["rows"] if r["frame"] == "lower-left" and r["symmetry"] == "identity"][0]
    ok("identity orientation modulo quarter turns", row["orientation_kept"] == 3 and row["beyond"]["1e-9"] == 0)
    # 19. the readers on small files, and malformed variants
    fj = make_form_j()
    ok("form J reads", rd.read_form_j(fj)["n"] == 2)
    fc = make_form_c()
    ok("form C reads", rd.read_corners(fc)["n"] == 2)
    for name, raw in [("dup", fj.replace(b'"n": 2,', b'"n": 2,\n "n": 2,')), ("float", fj.replace(b'"n": 2', b'"n": 2.0')),
                      ("plus", fj.replace(b'"1/2"', b'"+1/2"', 1)), ("negzero", fj.replace(b'"1/2"', b'"-0"', 1)),
                      ("lead", fj.replace(b'"1/2"', b'"01/2"', 1)), ("zero-den", fj.replace(b'"1/2"', b'"1/0"', 1))]:
        ok(f"form J refuses {name}", refused(rd.read_form_j, raw))
    for name, raw in [("anchor", fc.replace(b"  n: 2", b"  n: &a 2")), ("tab", fc.replace(b"  n: 2", b"  n:\t2")),
                      ("ids", fc.replace(b"square-1", b"square-X").replace(b"square-2", b"square-1").replace(b"square-X", b"square-2")),
                      ("dquote", fc.replace(b"- - 0\n", b'- - "0"\n', 1)), ("dupkey", fc.replace(b"  n: 2\n", b"  n: 2\n  n: 2\n"))]:
        ok(f"form C refuses {name}", refused(rd.read_corners, raw))
    flags: list = []
    rd.scalar("2/4", "t", flags)
    ok("not lowest terms flagged", flags == [["t", "not-lowest-terms"]])
    # 20. prints
    ok("ceil 12", fmt.ceil_places(F(16870013850404464, 10**15), 12) == "16.870013850405")
    ok("floor 12", fmt.floor_places(F(16870013850404464, 10**15), 12) == "16.870013850404")
    ok("sci", fmt.sci(F(1, 3), 4) == "3.333e-1" and fmt.sci(F(-25, 1000), 2) == "-2.5e-2" and fmt.sci(F(999, 1000), 2) == "1.0e+0")
    # 21. whole decisions: two touching squares accepted; with the second moved 1/10 in, refused
    d2 = chk.decide([pose(H, H), pose(F(3, 2), H)], [geom.corners_of(pose(H, H)), geom.corners_of(pose(F(3, 2), H))], F(2))
    ok("decide accepts touching", d2["accept"] and d2["a_classes"] == ["contact"])
    d3 = chk.decide([pose(H, H), pose(F(7, 5), H)], [geom.corners_of(pose(H, H)), geom.corners_of(pose(F(7, 5), H))], F(2))
    ok("decide refuses overlap", not d3["accept"] and d3["a_overlap"] == [(0, 1)] and d3["b_overlap"] == [(0, 1)])
    i5b, j6b = pose(F(1), F(1), R34), pose(F(1) + F(6, 5), F(1))
    cw = [tuple(reversed(geom.corners_of(p))) for p in (i5b, j6b)]
    d4 = chk.decide([i5b, j6b], cw, F(4))
    ok("decide accepts clockwise listings", d4["accept"] and d4["a_classes"] == ["contact"])
    return out


def refused(fn, raw) -> bool:
    try:
        fn(raw)
    except rd.ReadError:
        return True
    return False


def make_form_j() -> bytes:
    obj = {"n": 2, "side": "2", "square_size": "1", "format": rd.FORMAT_SENTENCE,
           "squares": [["1/2", "1/2", "1", "0"], ["3/2", "1/2", "3/5", "4/5"]]}
    return (json.dumps(obj, indent=1) + "\n").encode()


def make_form_c() -> bytes:
    lines = ["softschema:", "  contract: packing.squares:Witness/v2", "  schema: x", "  envelope: witness", "  status: enforced",
             "witness:", "  id: W-test", "  n: 2", "  side: 2", "  square_size: '1'", "  representation: corners",
             "  scalar:", "    kind: rational", "  coordinates:", "    origin: lower-left", "    axes: x-right-y-up",
             "    angle_unit: not-applicable", "  claim:", "    coordinate_provenance: reported", "    method: exact-algebraic",
             "    limitations: a test", "  squares:"]
    for k, (x, y) in enumerate([(H, H), (F(3, 2), H)], start=1):
        lines += [f"  - id: square-{k}", "    corners:"]
        for cx, cy in geom.corners_of((x, y, F(1), F(0)))[2:] + geom.corners_of((x, y, F(1), F(0)))[:2]:
            lines += [f"    - - {fmt.frac_text(cx)}", f"      - {fmt.frac_text(cy)}"]
    return ("\n".join(lines) + "\n").encode()


def run() -> dict:
    base = checks()
    failed = [n for n, v in base if not v]
    mutants = {}
    for name, apply, undo in MUTANTS:
        saved = apply()
        try:
            res = checks()
            fails = [n for n, v in res if not v]
        except Exception as exc:  # a broken copy that crashes is caught too
            fails = [f"raised {type(exc).__name__}"]
        finally:
            undo(saved)
        mutants[name] = {"caught": bool(fails), "checks_failed": len(fails), "first": fails[:3]}
    return {"checks": len(base), "failed": failed, "mutants": mutants,
            "verdict": "PASSED" if not failed and all(m["caught"] for m in mutants.values()) else "FAILED"}


def _patch(mod, attr, new):
    def apply():
        old = getattr(mod, attr)
        setattr(mod, attr, new)
        return old

    def undo(old):
        setattr(mod, attr, old)

    return apply, undo


def _m1_pair_terms(pi, pj):  # only square i's axes
    xi, yi, ei, ai, bi, ri = pi
    xj, yj, ej, aj, bj, rj = pj
    dx, dy = xj * ei - xi * ej, yj * ei - yi * ej
    p = max(rj * abs(dx * ai + dy * bi), rj * abs(dy * ai - dx * bi))
    hn = ei * ej * (ri * rj + abs(ai * aj + bi * bj) + abs(ai * bj - bi * aj))
    return p, hn, 2 * ei * ej * ri * rj


def _m2_pair_terms(pi, pj):  # H without the |sin D| term
    xi, yi, ei, ai, bi, ri = pi
    xj, yj, ej, aj, bj, rj = pj
    dx, dy = xj * ei - xi * ej, yj * ei - yi * ej
    p = max(rj * abs(dx * ai + dy * bi), rj * abs(dy * ai - dx * bi), ri * abs(dx * aj + dy * bj), ri * abs(dy * aj - dx * bj))
    hn = ei * ej * (ri * rj + abs(ai * aj + bi * bj))
    return p, hn, 2 * ei * ej * ri * rj


def _m4_clip_linear(poly, a, b, c):  # open half-planes
    vals = [a * x + b * y + c for x, y in poly]
    out = []
    n = len(poly)
    for k in range(n):
        fp, fc = vals[k - 1], vals[k]
        pp, pc = poly[k - 1], poly[k]
        if fc > 0:
            if fp <= 0 and fp != fc:
                t = fp / (fp - fc)
                out.append((pp[0] + t * (pc[0] - pp[0]), pp[1] + t * (pc[1] - pp[1])))
            out.append(pc)
        elif fp > 0:
            t = fp / (fp - fc)
            out.append((pp[0] + t * (pc[0] - pp[0]), pp[1] + t * (pc[1] - pp[1])))
    return out


def _m5_edge_halfplanes(q):  # ignores the listing sense
    out = []
    for k in range(len(q)):
        (px, py), (qx, qy) = q[k], q[(k + 1) % len(q)]
        a, b = -(qy - py), (qx - px)
        out.append((a, b, -(a * px + b * py)))
    return out


_REAL_CONTRACTION = con.contraction


def _m6_contraction(poses, side):  # takes the least contact factor
    ints = [geom.int_pose(p) for p in poses]
    fs = [f for f in geom.contact_factors(ints)]
    lo = min(F(f[0], f[1]) for f in fs)
    real = _REAL_CONTRACTION(poses, side)
    e = [geom.half_extent(p) for p in poses]
    xlo = min(lo * p[0] - h for p, h in zip(poses, e, strict=True))
    xhi = max(lo * p[0] + h for p, h in zip(poses, e, strict=True))
    ylo = min(lo * p[1] - h for p, h in zip(poses, e, strict=True))
    yhi = max(lo * p[1] + h for p, h in zip(poses, e, strict=True))
    shrunk = max(xhi - xlo, yhi - ylo)
    real.update({"lambda": lo, "shrunk_side": shrunk, "margin": side - shrunk,
                 "shrunk_poses": [(lo * p[0] - xlo, lo * p[1] - ylo, p[2], p[3]) for p in poses]})
    return real


def _m8_twin(q, p):  # accepts any order of the right four corners
    return (0, "ccw") if sorted(q) == sorted(geom.corners_of(p)) else None


_REAL_SCALAR = rd.scalar


def _m10_scalar(text, where, flags):  # accepts a plus sign
    if isinstance(text, str) and text.startswith("+"):
        text = text[1:]
    return _REAL_SCALAR(text, where, flags)


def _m9_canonical(c, d):  # compares raw directions
    return (c, d)


MUTANTS = [
    ("M1 method A on square i's axes only", *_patch(geom, "pair_terms", _m1_pair_terms)),
    ("M2 method A's H without |sin D|", *_patch(geom, "pair_terms", _m2_pair_terms)),
    ("M3 margin 0 classed as overlap", *_patch(chk, "a_class", lambda m: "apart" if m > 0 else "overlap")),
    ("M4 method B with open half-planes", *_patch(clipmod, "clip_linear", _m4_clip_linear)),
    ("M5 method B ignoring the listing sense", *_patch(clipmod, "edge_halfplanes", _m5_edge_halfplanes)),
    ("M6 contraction at the least factor", *_patch(con, "contraction", _m6_contraction)),
    ("M7 half-extent 1/2 at every angle", *_patch(geom, "half_extent", lambda p: F(1, 2))),
    ("M8 twin accepting any corner order", *_patch(geom, "twin_match", _m8_twin)),
    ("M9 identity orientation on raw directions", *_patch(ident, "canonical", _m9_canonical)),
    ("M10 scalar accepting a plus sign", *_patch(rd, "scalar", _m10_scalar)),
]


def main(argv: list[str]) -> int:
    res = run()
    with open(argv[0], "w") as f:
        json.dump(res, f, indent=1)
        f.write("\n")
    print(res["verdict"], res["checks"], "checks;", sum(m["caught"] for m in res["mutants"].values()), "of",
          len(res["mutants"]), "broken copies caught;", "failed:", res["failed"])
    return 0 if res["verdict"] == "PASSED" else 1


if __name__ == "__main__":
    _sys.exit(main(_sys.argv[1:]))
