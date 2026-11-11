"""Run the stated controls with the frozen checker and compare with the plan.

Lane L108, blind stage 4 review of jlevy/squares#959. Written after the plan was stated
and hashed (frozen/controls-plan-digest.txt). Builds each modified certificate with
l108_geom or by editing the parsed tree, and decides it with the frozen reader and
methods through l108_check.decide.

Usage: python -I -B l108_controls.py CERT.yaml CERT.json PLAN.json FACTS.json CHECK.json OUT.json
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import l108_check as check  # noqa: E402
import l108_clip as clipm  # noqa: E402
import l108_geom as geom  # noqa: E402
import l108_reader as reader  # noqa: E402
import l108_sat as satm  # noqa: E402

EPS = Fraction(1, 10**30)
WALLS = ("left", "bottom", "right", "top")


def raw_of(v: Fraction) -> tuple[int, int]:
    return (v.numerator, v.denominator)


def replace(cert: reader.Certificate, squares: list[Any] | None = None, side: Fraction | None = None) -> reader.Certificate:
    return reader.Certificate(
        n=cert.n,
        side=cert.side if side is None else raw_of(side),
        squares=cert.squares if squares is None else tuple(squares),
        tree=cert.tree,
    )


def pair_exact(cert: reader.Certificate, i: int, j: int) -> tuple[Fraction, Fraction]:
    """Method A's margin and method B's clipped area for one pair (1-based ids)."""
    a1, a2 = satm.build(cert.squares[i - 1]), satm.build(cert.squares[j - 1])
    b1, b2 = clipm.build(cert.squares[i - 1]), clipm.build(cert.squares[j - 1])
    assert a1 is not None and a2 is not None and b1 is not None and b2 is not None
    return check.as_fraction(satm.margin(a1, a2)), clipm.pair(b1, clipm.inner_half_planes(b2))[1]


def compare(expect: dict[str, Any], res: dict[str, Any], cert: reader.Certificate) -> tuple[bool, dict[str, Any]]:
    seen: dict[str, Any] = {"verdict": res["verdict"]}
    ok = res["verdict"] == expect["verdict"]
    for key in ("not_unit_a", "not_unit_b"):
        if key in expect:
            seen[key] = res[key]
            ok &= res[key] == expect[key]
    if res["verdict"] == "REFUSE" and (res["not_unit_a"] or res["not_unit_b"]):
        return ok, seen
    if "overlapping_pairs" in expect:
        got = sorted(o["pair"] for o in res["overlapping_pairs"])
        seen["overlapping_pair_count"] = len(got)
        seen["overlapping_pairs_first"] = got[:5]
        if expect["overlapping_pairs"] == "at least one":
            ok &= len(got) >= 1
        else:
            ok &= got == sorted(expect["overlapping_pairs"])
        ok &= all(o["a"] == o["b"] for o in res["overlapping_pairs"])
    if "touching_pairs" in expect:
        seen["touching_pairs"] = res["touching_pairs"]
        ok &= sorted(res["touching_pairs"]) == sorted(expect["touching_pairs"])
    if "walls_outside" in expect:
        got_w = [list(x) for x in res["walls_outside"]]
        seen["walls_outside"] = got_w
        ok &= sorted(got_w) == sorted(expect["walls_outside"])
    if "wall_contacts" in expect:
        seen["wall_contacts"] = res["wall_contacts"]
        ok &= res["wall_contacts"] == expect["wall_contacts"]
    if "wall_contacts_set" in expect:
        seen["wall_contacts"] = res["wall_contacts"]
        ok &= sorted(res["wall_contacts"]) == sorted(expect["wall_contacts_set"])
    if "margin_list_sha256" in expect:
        seen["margin_list_sha256"] = res["margin_list_sha256"]
        ok &= res["margin_list_sha256"] == expect["margin_list_sha256"]
    for key in ("counterclockwise", "clockwise"):
        if key in expect:
            seen[key] = res[key]
            ok &= res[key] == expect[key]
    ok &= not res.get("wall_disagreements") and not res.get("pair_disagreements")
    for name, want in expect.get("pair_margins", {}).items():
        i, j = (int(x) for x in name.split())
        m, area = pair_exact(cert, i, j)
        seen[f"margin {name}"] = check.exact(m) if m.denominator < 10**40 else check.dec(m)
        ok &= m == Fraction(want)
        if name in expect.get("pair_areas", {}):
            seen[f"area {name}"] = check.exact(area)
            ok &= area == Fraction(expect["pair_areas"][name])
    return ok, seen


def reader_control(yaml_text: str, json_text: str, want: str) -> tuple[bool, dict[str, Any]]:
    try:
        reader.read_texts(yaml_text, json_text)
    except reader.Refused as exc:
        return (want in str(exc), {"refused": str(exc)[:120]})
    return (False, {"refused": None})


def dump_pair(tree: dict[str, Any]) -> tuple[str, str]:
    return yaml.safe_dump(tree, sort_keys=False, width=10**9), json.dumps(tree)


def main(argv: list[str]) -> int:
    sys.set_int_max_str_digits(0)  # summed overlap areas in G6 are long exact integers
    t0 = time.process_time()
    yaml_path, json_path = Path(argv[1]), Path(argv[2])
    plan = json.loads(Path(argv[3]).read_text(encoding="utf-8"))
    facts = json.loads(Path(argv[4]).read_text(encoding="utf-8"))
    base_receipt = json.loads(Path(argv[5]).read_text(encoding="utf-8"))
    yaml_text = yaml_path.read_text(encoding="utf-8")
    json_text = json_path.read_text(encoding="utf-8")
    cert = reader.read_texts(yaml_text, json_text)
    side = Fraction(*cert.side)
    corners = [geom.from_raw(r) for r in cert.squares]
    n = cert.n
    out: list[dict[str, Any]] = []

    def record(cid: str, ok: bool, seen: dict[str, Any]) -> None:
        out.append({"id": cid, "as_stated": ok, "came_out": seen})
        print(cid, "as stated" if ok else "NOT AS STATED", flush=True)

    by_id = {c["id"]: c for c in plan["controls"]}

    def run_decide(cid: str, mod: reader.Certificate, only: set[int] | None = None) -> None:
        res = check.decide(mod, only=only)
        ok, seen = compare(by_id[cid]["expect"], res, mod)
        record(cid, ok, seen)

    # G1
    sq = list(cert.squares)
    sq[178] = sq[0]
    run_decide("G1", replace(cert, squares=sq))
    # G2
    sq = list(cert.squares)
    sq[0] = geom.to_raw(geom.translate(corners[0], (side, Fraction(0))))
    run_decide("G2", replace(cert, squares=sq))
    # G3, G4, G9: the tree edited, YAML and twin alike
    tree = json.loads(json_text)
    t3 = json.loads(json_text)
    del t3["witness"]["squares"][178]
    ok, seen = reader_control(*dump_pair(t3), by_id["G3"]["expect"]["reader_refuses"])
    record("G3", ok, seen)
    t4 = json.loads(json_text)
    t4["witness"]["squares"][178]["id"] = 1
    ok, seen = reader_control(*dump_pair(t4), by_id["G4"]["expect"]["reader_refuses"])
    record("G4", ok, seen)
    # G5
    sq = list(cert.squares)
    c = list(corners[0])
    c[2] = (c[2][0] + EPS, c[2][1])
    sq[0] = geom.to_raw((c[0], c[1], c[2], c[3]))
    run_decide("G5", replace(cert, squares=sq))
    # G6
    sq = []
    for cs in corners:
        cy = (cs[0][1] + cs[2][1]) / 2
        sq.append(geom.to_raw(tuple((x, 2 * cy - y) for x, y in cs)))  # type: ignore[arg-type]
    run_decide("G6", replace(cert, squares=sq))
    # G7: the twin alone
    t7 = json.loads(json_text)
    s7 = t7["witness"]["side"]
    t7["witness"]["side"] = s7[:-1] + ("1" if s7[-1] != "1" else "3")
    ok, seen = reader_control(yaml_text, json.dumps(t7), by_id["G7"]["expect"]["reader_refuses"])
    record("G7", ok, seen)
    # G8
    sq = [geom.to_raw(tuple((y, x) for x, y in cs)) for cs in corners]  # type: ignore[misc]
    run_decide("G8", replace(cert, squares=sq))
    # G9
    t9 = json.loads(json_text)
    p, q = cert.side
    t9["witness"]["side"] = f"{2 * p}/{2 * q}"
    ok, seen = reader_control(*dump_pair(t9), by_id["G9"]["expect"]["reader_refuses"])
    record("G9", ok, seen)
    # G10, G11
    sq = [(r[1], r[2], r[3], r[0]) for r in cert.squares]
    run_decide("G10", replace(cert, squares=sq))
    sq = [(r[0], r[3], r[2], r[1]) for r in cert.squares]
    run_decide("G11", replace(cert, squares=sq))
    del tree
    # S1: the side changed; walls only (no pair depends on the side)
    floor12 = Fraction(side.numerator * 10**12 // side.denominator, 10**12)
    ceil12 = Fraction(-((-side.numerator * 10**12) // side.denominator), 10**12)
    assert f"{floor12.numerator}/{floor12.denominator}" == facts["side_floor_12"]
    assert f"{ceil12.numerator}/{ceil12.denominator}" == facts["side_ceil_12"]
    for cid, new_side in (("S1a", side - Fraction(1, cert.side[1])), ("S1b", side - EPS), ("S1c", floor12), ("S1d", ceil12)):
        run_decide(cid, replace(cert, side=new_side), only=set())
    # S4: the least pair closed along its centre line; the mover's pairs and every wall
    a, b = facts["s4"]["pair"]
    mover = plan["s4_mover"]
    fixed = a if mover == b else b
    info = geom.closing(corners[fixed - 1], corners[mover - 1])
    tau = info["tau"]
    assert isinstance(tau, Fraction)
    for cid, tt in (("S4c", tau), ("S4p", geom.past_tau(info, EPS))):
        sq = list(cert.squares)
        sq[mover - 1] = geom.to_raw(geom.moved(corners[mover - 1], info, tt))
        run_decide(cid, replace(cert, squares=sq), only={mover})
    # S5: every pair below 1e-12, pair by pair
    near = [r["pair"] for r in base_receipt["result"]["pairs_below_1e-3"] if _approx(r["margin"]) < Fraction(1, 10**12)]
    good = 0
    bad: list[list[int]] = []
    for i, j in near:
        info = geom.closing(corners[i - 1], corners[j - 1])
        tau = info["tau"]
        assert isinstance(tau, Fraction)
        fine = True
        for tt, want_m, want_c in ((tau, Fraction(0), "contact"), (geom.past_tau(info, EPS), -EPS, "overlap")):
            moved = geom.to_raw(geom.moved(corners[j - 1], info, tt))
            a1, a2 = satm.build(cert.squares[i - 1]), satm.build(moved)
            b1, b2 = clipm.build(cert.squares[i - 1]), clipm.build(moved)
            assert a1 is not None and a2 is not None and b1 is not None and b2 is not None
            m = check.as_fraction(satm.margin(a1, a2))
            cb, _area = clipm.pair(b1, clipm.inner_half_planes(b2))
            fine &= m == want_m and satm.classify(satm.margin(a1, a2)) == want_c and cb == want_c
        if fine:
            good += 1
        else:
            bad.append([i, j])
    want5 = by_id["S5"]["expect"]
    record("S5", good == want5["as_stated"] == len(near), {"pairs": len(near), "as_stated": good, "not": bad[:10]})
    # S6: every square to its nearest wall, at and past
    good = 0
    bad6: list[list[Any]] = []
    for k in range(n):
        cl = geom.clearances(corners[k], side)
        w = min(WALLS, key=lambda name: cl[name])
        fine = True
        for move, want in ((cl[w], "contact"), (cl[w] + EPS, "overlap")):
            raw = geom.to_raw(geom.to_wall(corners[k], w, move))
            sa, sb = satm.build(raw), clipm.build(raw)
            assert sa is not None and sb is not None
            ca = satm.classify(satm.walls(sa, satm.side_q(cert.side))[w])
            cb = clipm.wall(sb, clipm.wall_planes(side)[w])[0]
            fine &= ca == want and cb == want
        if fine:
            good += 1
        else:
            bad6.append([k + 1, w])
    record("S6", good == by_id["S6"]["expect"]["as_stated"], {"squares": n, "as_stated": good, "not": bad6[:10]})

    every = all(r["as_stated"] for r in out) and len(out) == len(plan["controls"])
    receipt = {
        "program": "l108_controls.py",
        "lane": "L108",
        "python": sys.version.split()[0],
        "programs_sha256": {**check.program_digests(), "l108_geom.py": check.sha256_file(HERE / "l108_geom.py"), "l108_controls.py": check.sha256_file(HERE / "l108_controls.py")},
        "plan_sha256": hashlib.sha256(Path(argv[3]).read_bytes()).hexdigest(),
        "controls": out,
        "verdict": "EVERY_CONTROL_AS_STATED" if every else "SOME_CONTROL_NOT_AS_STATED",
        "cpu_seconds": round(time.process_time() - t0, 1),
    }
    Path(argv[6]).write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    print(receipt["verdict"])
    return 0 if every else 1


def _approx(text: str) -> Fraction:
    mant, exp = text.split("e")
    return Fraction(mant) * Fraction(10) ** int(exp)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
