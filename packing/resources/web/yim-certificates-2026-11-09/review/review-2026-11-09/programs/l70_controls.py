"""Run the frozen L70 controls plan on one certificate and compare with what it stated.

Written after the plan was frozen (frozen/controls-plan-digests.txt). Every mutated
packing is built exactly here and decided by the frozen checker's two methods, at the
level the plan names:

* whole-file: l70_check.decide (every square, wall and pair, both methods);
* wall-level: every square's shape, containment and wall contacts by both methods,
  through the frozen modules' own functions (the pairs are unchanged by construction);
* pair-level / square-level: l70_check.decide on the two squares / the one square;
* reader: the frozen reader on the mutated bytes.

Usage: python -I l70_controls.py --src SRC --plan controls-plan.json --label LABEL --checks OUTDIR --out RECEIPT
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import l70_check as C  # noqa: E402
import l70_clip as B  # noqa: E402
import l70_reader as R  # noqa: E402
import l70_sat as A  # noqa: E402
from gmpy2 import mpq  # noqa: E402

EPS = F(1, 10**30)


def ints(x: F) -> tuple[int, int]:
    return x.numerator, x.denominator


def with_side(pk: R.Packing, side: F) -> R.Packing:
    return R.Packing(n=pk.n, side=ints(side), kind=pk.kind, squares=pk.squares, ids=pk.ids)


def with_rows(pk: R.Packing, rows: list[tuple[int, ...]]) -> R.Packing:
    return R.Packing(n=pk.n, side=pk.side, kind=pk.kind, squares=tuple(rows), ids=pk.ids)


def row_xyt(row: tuple[int, ...]) -> tuple[F, F, F]:
    return F(row[0], row[1]), F(row[2], row[3]), F(row[4], row[5])


def make_row(x: F, y: F, t: F) -> tuple[int, ...]:
    return ints(x) + ints(y) + ints(t)


def basis(t: F) -> tuple[F, F]:
    d = 1 + t * t
    return (1 - t * t) / d, 2 * t / d


def contact_factor(ri: tuple[F, F, F], rj: tuple[F, F, F]) -> F:
    """lambda with max_w |w.(lambda d)| = T over the pair's four edge normals."""
    c1, s1 = basis(ri[2])
    c2, s2 = basis(rj[2])
    dx, dy = rj[0] - ri[0], rj[1] - ri[1]
    t_half = (1 + abs(c1 * c2 + s1 * s2) + abs(c1 * s2 - s1 * c2)) / 2
    m = max(abs(c1 * dx + s1 * dy), abs(-s1 * dx + c1 * dy), abs(c2 * dx + s2 * dy), abs(-s2 * dx + c2 * dy))
    return t_half / m


def closed_row(ri: tuple[F, F, F], rj: tuple[F, F, F], lam: F) -> tuple[int, ...]:
    return make_row(ri[0] + lam * (rj[0] - ri[0]), ri[1] + lam * (rj[1] - ri[1]), rj[2])


def wall_level(pk: R.Packing) -> dict[str, Any]:
    """Every square's shape, containment and wall contacts, by both methods."""
    side_f = F(pk.side[0], pk.side[1])
    side_q = mpq(pk.side[0], pk.side[1])
    sa = A.build(pk)
    sb = B.build(pk)
    a_unit = [pk.ids[i] for i, s in enumerate(sa) if not s.unit]
    b_unit = [pk.ids[i] for i, s in enumerate(sb) if not s.unit]
    a_out = [pk.ids[i] for i, s in enumerate(sa) if min(A.wall_clearances(s, side_f)) < 0]
    b_out = [pk.ids[i] for i, s in enumerate(sb) if not B.inside_box(s, side_q)]
    a_con: dict[str, list[str]] = {w: [] for w in C.WALLS}
    b_con: dict[str, list[str]] = {w: [] for w in C.WALLS}
    for i, s in enumerate(sa):
        for w, v in zip(C.WALLS, A.wall_clearances(s, side_f), strict=True):
            if v == 0:
                a_con[w].append(pk.ids[i])
    for i, s in enumerate(sb):
        for w, hit in zip(C.WALLS, B.wall_touches(s, side_q), strict=True):
            if hit:
                b_con[w].append(pk.ids[i])
    agree = a_unit == b_unit and a_out == b_out and a_con == b_con
    ok = not a_unit and not b_unit and not a_out and not b_out
    return {
        "verdict": "ACCEPT" if ok and agree else "REFUSE",
        "agree": agree,
        "outside_A": a_out,
        "outside_B": b_out,
        "not_unit_A": a_unit,
        "not_unit_B": b_unit,
        "contacts_A": a_con,
        "contacts_B": b_con,
    }


def summarize(res: dict[str, Any]) -> dict[str, Any]:
    return {
        "verdict": res["verdict"],
        "agree": res["agree"],
        "outside_A": res["A"]["outside"],
        "outside_B": res["B"]["outside"],
        "not_unit_A": res["A"]["not_unit"],
        "not_unit_B": res["B"]["not_unit"],
        "touching_A": res["A"]["touching_pairs"],
        "touching_B": res["B"]["touching_pairs"],
        "overlapping_A": res["A"]["overlapping_pairs"],
        "overlapping_B": res["B"]["overlapping_pairs"],
        "overlap_counts": [res["A"]["classes"]["overlap"], res["B"]["classes"]["overlap"]],
        "A_least_margin": res["A"]["least_margin"],
        "B_largest_overlap_area": C.frac_str(F(res["B"]["largest_overlap_area_float"]).limit_denominator(10**12)),
        "contacts_A": {w: res["A"]["walls"][w]["contacts"] for w in C.WALLS},
        "contacts_B": res["B"]["wall_contacts"],
        "cpu_seconds": res["cpu_seconds_total"],
    }


def same_both(got: dict[str, Any], key: str, want: list[Any]) -> bool:
    return got[f"{key}_A"] == want and got[f"{key}_B"] == want


def judge(cid: str, exp: dict[str, Any], got: dict[str, Any]) -> bool:
    if "reader" in exp:
        return got.get("reader") == "refuse" and exp["reason_contains"] in got.get("reason", "")
    if got["verdict"] != exp["verdict"]:
        return False
    if not got.get("agree", True):
        return False
    ok = True
    if "outside" in exp:
        ok &= same_both(got, "outside", exp["outside"])
    if "not_unit" in exp:
        ok &= same_both(got, "not_unit", exp["not_unit"])
    if "overlapping_pairs" in exp:
        if isinstance(exp["overlapping_pairs"], str):  # "at least one, equal sets"
            ok &= got["overlap_counts"][0] >= 1 and got["overlap_counts"][0] == got["overlap_counts"][1] and got["overlapping_A"] == got["overlapping_B"]
        else:
            ok &= same_both(got, "overlapping", exp["overlapping_pairs"]) and got["overlap_counts"] == [len(exp["overlapping_pairs"])] * 2
    if "touching_pairs" in exp:
        ok &= same_both(got, "touching", exp["touching_pairs"])
    if "A_least_margin" in exp:
        ok &= got["A_least_margin"] == exp["A_least_margin"]
    if "B_largest_overlap_area" in exp:
        ok &= got["B_largest_overlap_area"] == exp["B_largest_overlap_area"]
    if "far_wall_contacts" in exp:
        want: dict[str, list[str]] = {"right": [], "top": []}
        for e in exp["far_wall_contacts"]:
            w, s = e.split(":")
            want[w].append(s)
        for w in ("right", "top"):
            ok &= got["contacts_A"][w] == want[w] and got["contacts_B"][w] == want[w]
    for key, wall in (("left_contacts", "left"), ("bottom_contacts", "bottom")):
        if key in exp:
            ok &= got["contacts_A"][wall] == exp[key] and got["contacts_B"][wall] == exp[key]
    return bool(ok)


def run(label: str, path: Path, plan: dict[str, Any], receipt: dict[str, Any]) -> dict[str, Any]:
    raw = path.read_bytes()
    pk = R.parse_cert_bytes(raw)
    side = F(pk.side[0], pk.side[1])
    rows = list(pk.squares)
    idx = {s: k for k, s in enumerate(pk.ids)}
    sa = A.build(pk)
    cl = [A.wall_clearances(s, side) for s in sa]
    least = {w: min(c[k] for c in cl) for k, w in enumerate(C.WALLS)}
    far = min(least["right"], least["top"])
    results = []
    for ctl in plan["controls"]:
        cid = ctl["id"]
        exp = ctl["expect"]
        t0 = time.process_time()
        got: dict[str, Any]
        if cid in ("G3", "G4", "G5"):
            lines = raw.decode("utf-8").split("\n")
            if cid == "G3":
                mutated = "\n".join(lines[:-2] + [""])
            elif cid == "G4":
                h = 1 if lines[0].startswith("#") else 0
                n_tok, s_tok = lines[h].split(" ")
                lines[h] = f"{int(n_tok) + 1} {s_tok}"
                mutated = "\n".join(lines)
            else:
                h = 1 if lines[0].startswith("#") else 0
                toks = lines[h + 1].split(" ")
                toks[2] = "1.5"
                lines[h + 1] = " ".join(toks)
                mutated = "\n".join(lines)
            try:
                R.parse_cert_bytes(mutated.encode("utf-8"))
                got = {"reader": "accept"}
            except R.ReadError as exc:
                got = {"reader": "refuse", "reason": str(exc)}
        elif cid == "G1":
            got = summarize(C.decide(with_rows(pk, rows[:-1] + [rows[0]]), keep_near=False))
        elif cid == "G2":
            x, y, t = row_xyt(rows[0])
            got = summarize(C.decide(with_rows(pk, [make_row(x + side, y, t)] + rows[1:]), keep_near=False))
        elif cid == "G6":
            got = summarize(C.decide(R.parse_cert_bytes(raw, sense="cw"), keep_near=False))
        elif cid in ("S1a", "S1b", "S1c", "S1d", "S1e"):
            new_side = {
                "S1a": side - F(1, pk.side[1]),
                "S1b": side - far,
                "S1c": side - far - EPS,
                "S1d": F(C.ceil_places(side, 12)),
                "S1e": F(C.floor_places(side, 12)),
            }[cid]
            got = wall_level(with_side(pk, new_side))
        elif cid in ("S3a", "S3b", "S3c", "S3d"):
            d = least["left"] if cid in ("S3a", "S3b") else least["bottom"]
            if cid in ("S3b", "S3d"):
                d += EPS
            new_rows = []
            for r in rows:
                x, y, t = row_xyt(r)
                new_rows.append(make_row(x - d, y, t) if cid in ("S3a", "S3b") else make_row(x, y - d, t))
            got = wall_level(with_rows(pk, new_rows))
        elif cid in ("S4c", "S4p"):
            i, j = (str(v) for v in ctl["what"].split("(")[1].split(")")[0].split(", "))
            ri, rj = row_xyt(rows[idx[i]]), row_xyt(rows[idx[j]])
            lam = contact_factor(ri, rj)
            if cid == "S4p":
                lam *= 1 - EPS
            new_rows = list(rows)
            new_rows[idx[j]] = closed_row(ri, rj, lam)
            got = summarize(C.decide(with_rows(pk, new_rows), keep_near=False))
        elif cid == "S5":
            pairs = [(a, b) for a, b, _e, f, _k in receipt["near_pairs_below_1e-9"] if f < 1e-12]
            stated = 0
            misses = []
            for a, b in pairs:
                ri, rj = row_xyt(rows[idx[a]]), row_xyt(rows[idx[b]])
                lam = contact_factor(ri, rj)
                classes = []
                for f in (lam, lam * (1 - EPS)):
                    two = R.Packing(n=2, side=pk.side, kind="cert", squares=(rows[idx[a]], closed_row(ri, rj, f)), ids=(a, b))
                    res = C.decide(two, keep_near=False)
                    ca = "overlap" if res["A"]["classes"]["overlap"] else ("touch" if res["A"]["classes"]["touch"] else "apart")
                    cb = "overlap" if res["B"]["classes"]["overlap"] else ("touch" if res["B"]["classes"]["touch"] else "apart")
                    classes.append((ca, cb))
                if classes == [("touch", "touch"), ("overlap", "overlap")]:
                    stated += 1
                else:
                    misses.append([a, b, classes])
            got = {"pairs": len(pairs), "as_stated": stated, "misses": misses[:20]}
        elif cid == "S6":
            stated = 0
            misses = []
            for k, r in enumerate(rows):
                x, y, t = row_xyt(r)
                c = cl[k]
                w = min(range(4), key=lambda q: c[q])
                outs = []
                for d in (c[w], c[w] + EPS):
                    nx, ny = x, y
                    if w == 0:
                        nx = x - d
                    elif w == 1:
                        ny = y - d
                    elif w == 2:
                        nx = x + d
                    else:
                        ny = y + d
                    one = R.Packing(n=1, side=pk.side, kind="cert", squares=(make_row(nx, ny, t),), ids=(pk.ids[k],))
                    wl = wall_level(one)
                    outs.append(wl)
                at, past = outs
                wall = C.WALLS[w]
                ok = at["verdict"] == "ACCEPT" and at["contacts_A"][wall] == [pk.ids[k]] and at["contacts_B"][wall] == [pk.ids[k]]
                ok = ok and past["outside_A"] == [pk.ids[k]] and past["outside_B"] == [pk.ids[k]]
                if ok:
                    stated += 1
                else:
                    misses.append([pk.ids[k], wall])
            got = {"squares": len(rows), "as_stated": stated, "misses": misses[:20]}
        elif cid == "S7":
            i = ctl["what"].split("square ")[1].split(" ")[0]
            corners_rows = []
            for k, r in enumerate(rows):
                x, y, t = row_xyt(r)
                c, s = basis(t)
                pts = [(x - c / 2 + s / 2, y - s / 2 - c / 2), (x + c / 2 + s / 2, y + s / 2 - c / 2), (x + c / 2 - s / 2, y + s / 2 + c / 2), (x - c / 2 - s / 2, y - s / 2 + c / 2)]
                if pk.ids[k] == i:
                    g = 1 + EPS
                    pts = [(x + g * (px - x), y + g * (py - y)) for px, py in pts]
                v: list[int] = []
                for px, py in pts:
                    v.extend(ints(px) + ints(py))
                corners_rows.append(tuple(v))
            cpk = R.Packing(n=pk.n, side=pk.side, kind="corners", squares=tuple(corners_rows), ids=pk.ids)
            got = summarize(C.decide(cpk, keep_near=False))
        else:
            raise SystemExit(f"unknown control {cid}")
        if cid in ("S5", "S6"):
            total = got.get("pairs", got.get("squares"))
            as_stated = got["as_stated"] == total and total == exp.get("pairs", exp.get("squares"))
        else:
            as_stated = judge(cid, exp, got)
        results.append({"id": cid, "level": ctl["level"], "what": ctl["what"], "expect": exp, "got": got, "as_stated": as_stated, "cpu_seconds": round(time.process_time() - t0, 3)})
        print(label, cid, "AS STATED" if as_stated else "MISSED", f"{time.process_time() - t0:.1f}s", flush=True)
    return {
        "label": label,
        "input_sha256": pk.meta["sha256"],
        "controls": results,
        "every_control_as_stated": all(r["as_stated"] for r in results),
        "missed": [r["id"] for r in results if not r["as_stated"]],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--checks", required=True)
    ap.add_argument("--out", required=True)
    ns = ap.parse_args()
    t0 = time.process_time()
    plan = json.loads(Path(ns.plan).read_text())
    entry = plan["files"][ns.label]
    path = Path(ns.src) / entry["input"]
    receipt = json.loads((Path(ns.checks) / f"check-{ns.label}.json").read_text())
    res = run(ns.label, path, entry, receipt)
    if res["input_sha256"] != entry["input_sha256"]:
        raise SystemExit("input differs from the plan's")
    out = {
        "program": "l70_controls.py",
        "program_digests": C.file_digests(C.CHECKER_FILES + ("l70_controls.py", "controls-plan.json")),
        **res,
        "cpu_seconds": round(time.process_time() - t0, 3),
    }
    Path(ns.out).write_text(json.dumps(out, indent=1) + "\n")
    print(ns.label, "EVERY_CONTROL_AS_STATED" if res["every_control_as_stated"] else f"MISSED {res['missed']}", "cpu", out["cpu_seconds"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
