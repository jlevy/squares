"""Known-answer self-test for the L70 checker (both methods and the reader).

Every case states its answer before it is decided. Exits 0 and writes PASSED only if
every case comes out as stated by both methods.

Usage: python -I l70_selftest.py --out selftest.json
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from fractions import Fraction as F
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import l70_check as C  # noqa: E402
import l70_reader as R  # noqa: E402

EPS = F(1, 10**30)
results: list[dict[str, Any]] = []


def ratint(x: F) -> tuple[int, int]:
    return x.numerator, x.denominator


def cert_pk(side: F, rows: list[tuple[F, F, F]]) -> R.Packing:
    sq = tuple(ratint(x) + ratint(y) + ratint(t) for (x, y, t) in rows)
    return R.Packing(n=len(rows), side=ratint(side), kind="cert", squares=sq, ids=tuple(str(i + 1) for i in range(len(rows))))


def corner_pk(side: F, sqs: list[list[tuple[F, F]]]) -> R.Packing:
    out = []
    for c in sqs:
        v: list[int] = []
        for x, y in c:
            v.extend(ratint(x) + ratint(y))
        out.append(tuple(v))
    return R.Packing(n=len(sqs), side=ratint(side), kind="corners", squares=tuple(out), ids=tuple(str(i + 1) for i in range(len(sqs))))


def expect(name: str, ok: bool, detail: Any = None) -> None:
    results.append({"case": name, "ok": bool(ok), "detail": detail})


def pair_case(name: str, side: F, rows: list[tuple[F, F, F]], cls: str, margin: F | None = None, area: F | None = None) -> None:
    pk = cert_pk(side, rows)
    r = C.decide(pk)
    a_cls = "overlap" if r["A"]["classes"]["overlap"] else ("touch" if r["A"]["classes"]["touch"] else "apart")
    b_cls = "overlap" if r["B"]["classes"]["overlap"] else ("touch" if r["B"]["classes"]["touch"] else "apart")
    ok = a_cls == cls and b_cls == cls and r["agree"]["pair_touch"] and r["agree"]["pair_overlap"]
    detail: dict[str, Any] = {"A": a_cls, "B": b_cls, "margin": r["A"]["least_margin"]}
    if margin is not None:
        ok = ok and F(r["A"]["least_margin"]) == margin
    if area is not None:
        # recompute the exact area with method B directly
        import l70_clip as B

        sb = B.build(pk)
        _, ar = B.pair_class(sb[0], sb[1])
        got = C.mpq_to_fraction(ar)
        detail["area"] = C.frac_str(got)
        ok = ok and got == area
    expect(name, ok, detail)


def axis(x: F, y: F) -> tuple[F, F, F]:
    return (x, y, F(0))


def t_of(c: F, s: F) -> F:
    """tan(theta/2) for an exact rational unit vector (c, s), c != -1."""
    return s / (1 + c)


def unit_from_t(t: F) -> tuple[F, F]:
    d = 1 + t * t
    return (1 - t * t) / d, 2 * t / d


def half_extents(t: F) -> tuple[F, F]:
    c, s = unit_from_t(t)
    h = (abs(c) + abs(s)) / 2
    return h, h


def contact_scale(r1: tuple[F, F, F], r2: tuple[F, F, F]) -> F:
    """Independent third computation: lambda with max_k |w_k.(lambda d)| = T."""
    c1, s1 = unit_from_t(r1[2])
    c2, s2 = unit_from_t(r2[2])
    dx, dy = r2[0] - r1[0], r2[1] - r1[1]
    cosd = c1 * c2 + s1 * s2
    sind = c1 * s2 - s1 * c2
    t_half = (1 + abs(cosd) + abs(sind)) / 2
    normals = [(c1, s1), (-s1, c1), (c2, s2), (-s2, c2)]
    m = max(abs(wx * dx + wy * dy) for wx, wy in normals)
    return t_half / m


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ns = ap.parse_args()
    t0 = time.process_time()
    h = F(1, 2)
    S = F(10)
    # --- edge contact, past, apart
    pair_case("edge contact", S, [axis(h + 1, h + 1), axis(h + 2, h + 1)], "touch", F(0), F(0))
    pair_case("edge past 1e-30", S, [axis(h + 1, h + 1), axis(h + 2 - EPS, h + 1)], "overlap", -EPS, EPS)
    pair_case("edge apart 1e-30", S, [axis(h + 1, h + 1), axis(h + 2 + EPS, h + 1)], "apart", EPS)
    # --- corner contact and past along the diagonal
    pair_case("corner contact", S, [axis(h + 1, h + 1), axis(h + 2, h + 2)], "touch", F(0), F(0))
    pair_case("corner past", S, [axis(h + 1, h + 1), axis(h + 2 - EPS, h + 2 - EPS)], "overlap", -EPS, EPS * EPS)
    # --- 3-4-5 vertex on an edge: u = (4/5, 3/5), t = 1/3; lowest corner offset (-1/10, -7/10)
    t345 = F(1, 3)
    base = axis(F(3), F(3))
    top = F(3) + h
    vtx = (F(3) + F(1, 10), top + F(7, 10), t345)
    pair_case("3-4-5 vertex on edge, contact", S, [base, vtx], "touch", F(0), F(0))
    pair_case("3-4-5 vertex on edge, past", S, [base, (vtx[0], vtx[1] - EPS, t345)], "overlap", -EPS, F(25, 24) * EPS * EPS)
    # mirror listing sense: the same contact built from the reflected square
    pair_case("3-4-5 vertex on edge, contact, reflected", S, [base, (F(3) - F(1, 10), top + F(7, 10), -t345)], "touch", F(0), F(0))
    # --- duplicate and rotated copies
    pair_case("duplicate", S, [axis(F(2), F(2)), axis(F(2), F(2))], "overlap", F(-1), F(1))
    pair_case("rotated copy (3/5, 4/5)", S, [axis(F(2), F(2)), (F(2), F(2), t_of(F(3, 5), F(4, 5)))], "overlap", F(-6, 5), F(5, 6))
    pair_case("rotated copy (4/5, 3/5)", S, [axis(F(2), F(2)), (F(2), F(2), t_of(F(4, 5), F(3, 5)))], "overlap", F(-6, 5), F(5, 6))
    # --- walls
    for name, row, out in (
        ("left wall contact", axis(h, F(5)), False),
        ("left wall past", axis(h - EPS, F(5)), True),
        ("top wall contact", axis(F(5), S - h), False),
        ("top wall past", axis(F(5), S - h + EPS), True),
    ):
        r = C.decide(cert_pk(S, [row]))
        ok = (bool(r["A"]["outside"]) == out) and (bool(r["B"]["outside"]) == out) and r["agree"]["inside"] and r["agree"]["wall_contacts"]
        expect(name, ok, {"A_outside": r["A"]["outside"], "B_outside": r["B"]["outside"], "A_contacts": {w: r["A"]["walls"][w]["contacts"] for w in C.WALLS}})
    r = C.decide(cert_pk(S, [axis(h, F(5))]))
    expect("left contact class", r["A"]["walls"]["left"]["contacts"] == ["1"] and r["B"]["wall_contacts"]["left"] == ["1"])
    # --- shapes both methods must refuse (corner format)
    z = F(0)
    one = F(1)
    good = [(z + 2, z + 2), (one + 2, z + 2), (one + 2, one + 2), (z + 2, one + 2)]
    shapes = {
        "rectangle 1 x (1+e)": [(F(2), F(2)), (F(3), F(2)), (F(3), F(3) + EPS), (F(2), F(3) + EPS)],
        "square of side 1+e": [(F(2), F(2)), (F(3) + EPS, F(2)), (F(3) + EPS, F(3) + EPS), (F(2), F(3) + EPS)],
        "unit rhombus (3/5, 4/5)": [(F(2), F(2)), (F(3), F(2)), (F(3) + F(3, 5), F(2) + F(4, 5)), (F(2) + F(3, 5), F(2) + F(4, 5))],
        "bowtie order": [good[0], good[2], good[1], good[3]],
        "repeated corner": [good[0], good[1], good[1], good[3]],
        "third corner off by e": [good[0], good[1], (good[2][0] + EPS, good[2][1]), good[3]],
    }
    r = C.decide(corner_pk(S, [good]))
    expect("good corner square accepted", r["verdict"] == "ACCEPT" and not r["A"]["not_unit"] and not r["B"]["not_unit"])
    for name, sq in shapes.items():
        r = C.decide(corner_pk(S, [sq]))
        expect(f"shape refused: {name}", r["A"]["not_unit"] == ["1"] and r["B"]["not_unit"] == ["1"] and r["verdict"] == "REFUSE")
    # clockwise listing of a unit square is still a unit square
    r = C.decide(corner_pk(S, [list(reversed(good))]))
    expect("clockwise listing accepted", r["verdict"] == "ACCEPT" and r["A"]["listing_sense"]["cw"] == 1)
    # --- random rational pairs to contact along the centre line, and 1e-30 either side
    rng = random.Random(20261109)
    n_pairs = 0
    bad_pairs: list[Any] = []
    for _ in range(600):
        t1 = F(rng.randint(-999, 999), rng.randint(1, 999))
        t2 = F(rng.randint(-999, 999), rng.randint(1, 999))
        r1 = (F(rng.randint(3000, 7000), 1000), F(rng.randint(3000, 7000), 1000), t1)
        r2 = (F(rng.randint(3000, 7000), 1000), F(rng.randint(3000, 7000), 1000), t2)
        if r1[:2] == r2[:2]:
            continue
        lam = contact_scale(r1, r2)
        for scale, want in ((lam, "touch"), (lam * (1 - EPS), "overlap"), (lam * (1 + EPS), "apart")):
            q = (r1[0] + scale * (r2[0] - r1[0]), r1[1] + scale * (r2[1] - r1[1]), t2)
            pk = cert_pk(F(20), [r1, q])
            rr = C.decide(pk)
            a_cls = "overlap" if rr["A"]["classes"]["overlap"] else ("touch" if rr["A"]["classes"]["touch"] else "apart")
            b_cls = "overlap" if rr["B"]["classes"]["overlap"] else ("touch" if rr["B"]["classes"]["touch"] else "apart")
            n_pairs += 1
            if not (a_cls == want and b_cls == want):
                bad_pairs.append([str(r1), str(q), want, a_cls, b_cls])
    expect("random pairs at contact and 1e-30 either side", not bad_pairs, {"probes": n_pairs, "failures": bad_pairs[:5]})
    # --- random squares to a wall and past it
    bad_walls: list[Any] = []
    n_walls = 0
    for _ in range(400):
        t = F(rng.randint(-999, 999), rng.randint(1, 999))
        hx, hy = half_extents(t)
        x = F(rng.randint(3000, 7000), 1000)
        for row, out in (((x, hy, t), False), ((x, hy - EPS, t), True), ((S - hx, F(5), t), False), ((S - hx + EPS, F(5), t), True)):
            rr = C.decide(cert_pk(S, [row]))
            n_walls += 1
            if (bool(rr["A"]["outside"]) != out) or (bool(rr["B"]["outside"]) != out) or not rr["agree"]["wall_contacts"]:
                bad_walls.append([str(row), out])
    expect("random squares at a wall and 1e-30 past", not bad_walls, {"probes": n_walls, "failures": bad_walls[:5]})
    # --- the reversed sense is the reflection in the horizontal centre line
    t = F(2, 7)
    pk_ccw = R.parse_cert_bytes(b"# x\n1 10\n5 5 2/7\n")
    pk_cw = R.parse_cert_bytes(b"# x\n1 10\n5 5 2/7\n", sense="cw")
    import l70_sat as A

    pa = A.build(pk_ccw)[0].p
    pb = A.build(pk_cw)[0].p
    refl = sorted((x, 10 - y) for (x, y) in pa)
    expect("cw reading is the horizontal reflection", sorted(pb) == refl and pk_cw.squares[0][4] == -2 and t == F(2, 7))
    # --- the reader refuses malformed files, each for its own reason
    good_file = b"# c\n2 5/2\n1/2 1/2 0\n3/2 1/2 0\n"
    pk = R.parse_cert_bytes(good_file)
    expect("reader accepts a good file", pk.n == 2 and pk.side == (5, 2) and pk.meta["row_tokens_not_lowest_terms"] == 0)
    pk = R.parse_cert_bytes(b"2 5/2\n2/4 1/2 0\n3/2 1/2 0\n")
    expect("reader flags a token not in lowest terms", pk.meta["row_tokens_not_lowest_terms"] == 1)
    malformed = {
        "no final newline": good_file[:-1],
        "carriage return": good_file.replace(b"\n", b"\r\n"),
        "tab": good_file.replace(b" 0\n", b"\t0\n", 1),
        "blank line": good_file + b"\n",
        "double space": good_file.replace(b"1/2 1/2", b"1/2  1/2", 1),
        "leading space": good_file.replace(b"\n1/2", b"\n 1/2", 1),
        "header three tokens": good_file.replace(b"2 5/2", b"2 5/2 1"),
        "header n zero": good_file.replace(b"2 5/2", b"0 5/2"),
        "header n leading zero": good_file.replace(b"2 5/2", b"02 5/2"),
        "too few rows": b"# c\n3 5/2\n1/2 1/2 0\n3/2 1/2 0\n",
        "too many rows": b"# c\n1 5/2\n1/2 1/2 0\n3/2 1/2 0\n",
        "row with two tokens": good_file.replace(b"3/2 1/2 0", b"3/2 1/2"),
        "row with four tokens": good_file.replace(b"3/2 1/2 0", b"3/2 1/2 0 0"),
        "zero denominator": good_file.replace(b"3/2 1/2 0", b"3/0 1/2 0"),
        "leading zero": good_file.replace(b"3/2 1/2 0", b"03/2 1/2 0"),
        "plus sign": good_file.replace(b"3/2 1/2 0", b"+3/2 1/2 0"),
        "decimal point": good_file.replace(b"3/2 1/2 0", b"1.5 1/2 0"),
        "negative denominator": good_file.replace(b"3/2 1/2 0", b"3/-2 1/2 0"),
        "letter": good_file.replace(b"3/2 1/2 0", b"3/2 a 0"),
        "negative zero": good_file.replace(b"3/2 1/2 0", b"3/2 1/2 -0"),
        "double slash": good_file.replace(b"3/2 1/2 0", b"3//2 1/2 0"),
        "comment after header": b"# c\n2 5/2\n# x\n1/2 1/2 0\n3/2 1/2 0\n",
        "non-ASCII data": good_file.replace(b"3/2 1/2 0", "3/2 1/2 ½".encode()),
        "negative side": good_file.replace(b"2 5/2", b"2 -5/2"),
        "zero side": good_file.replace(b"2 5/2", b"2 0"),
        "not UTF-8": b"# \xff\n" + good_file[4:],
        "empty": b"\n",
    }
    refused = {}
    for name, data in malformed.items():
        try:
            R.parse_cert_bytes(data)
            refused[name] = None
        except R.ReadError as exc:
            refused[name] = str(exc)
    expect("reader refuses every malformed cert", all(v is not None for v in refused.values()), refused)
    # corners YAML refusals
    import tempfile

    ytmpl = (
        "softschema:\n  contract: packing.squares:Witness/v2\n  schema: witness.schema.yaml\n"
        "witness:\n  id: W-test\n  n: {n}\n  side: '{side}'\n  square_size: '1'\n  representation: {rep}\n"
        "  scalar:\n    kind: {kind}\n  coordinates:\n    origin: {origin}\n    axes: x-right-y-up\n    angle_unit: not-applicable\n"
        "  squares:\n{squares}"
    )

    def sqy(sid: str, corners: list[tuple[str, str]]) -> str:
        s = f"  - id: {sid}\n    corners:\n"
        for x, y in corners:
            s += f"    - - '{x}'\n      - '{y}'\n"
        return s

    c1 = [("0", "0"), ("1", "0"), ("1", "1"), ("0", "1")]
    c2 = [("2", "0"), ("3", "0"), ("3", "1"), ("2", "1")]
    base_kw = {"n": 2, "side": "3", "rep": "corners", "kind": "rational", "origin": "lower-left", "squares": sqy("1", c1) + sqy("2", c2)}
    variants = {
        "good": base_kw,
        "wrong representation": {**base_kw, "rep": "center-basis"},
        "decimal scalars": {**base_kw, "kind": "decimal"},
        "centre origin": {**base_kw, "origin": "container-center"},
        "n mismatch": {**base_kw, "n": 3},
        "three corners": {**base_kw, "squares": sqy("1", c1[:3]) + sqy("2", c2)},
        "repeated id": {**base_kw, "squares": sqy("1", c1) + sqy("1", c2)},
        "bad scalar": {**base_kw, "squares": sqy("1", [("0.5", "0")] + c1[1:]) + sqy("2", c2)},
    }
    yres = {}
    with tempfile.TemporaryDirectory() as td:
        for name, kw in variants.items():
            p = Path(td) / "w.yaml"
            p.write_text(ytmpl.format(**kw))
            try:
                pk = R.read_corners_yaml(p)
                yres[name] = ("accepted", C.decide(pk)["verdict"])
            except R.ReadError as exc:
                yres[name] = ("refused", str(exc))
        p = Path(td) / "dup.yaml"
        p.write_text(ytmpl.format(**base_kw).replace("  square_size: '1'\n", "  square_size: '1'\n  square_size: '1'\n"))
        try:
            R.read_corners_yaml(p)
            yres["duplicate key"] = ("accepted", None)
        except R.ReadError as exc:
            yres["duplicate key"] = ("refused", str(exc))
    ok = yres["good"] == ("accepted", "ACCEPT") and all(v[0] == "refused" for k, v in yres.items() if k != "good")
    expect("corner reader: good accepted, every variant refused", ok, yres)
    # --- decimal helpers
    expect("ceil and floor at 12 places", C.ceil_places(F(1, 3), 12) == "0.333333333334" and C.floor_places(F(1, 3), 12) == "0.333333333333" and C.ceil_places(F(1, 4), 2) == "0.25")
    passed = all(r["ok"] for r in results)
    out = {
        "program": "l70_selftest.py",
        "program_digests": C.file_digests(C.CHECKER_FILES + ("l70_selftest.py",)),
        "python": sys.version.split()[0],
        "verdict": "PASSED" if passed else "FAILED",
        "cases": results,
        "cpu_seconds": round(time.process_time() - t0, 3),
    }
    Path(ns.out).write_text(json.dumps(out, indent=1) + "\n")
    print(out["verdict"], sum(r["ok"] for r in results), "of", len(results), "cpu", out["cpu_seconds"])
    for r in results:
        if not r["ok"]:
            print("FAIL", r["case"], json.dumps(r["detail"])[:400])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
