#!/usr/bin/env python3
"""Sharp controls for the #728 certificate: mutants at exact contact and 1e-30 past it.

A premise check for the review of #728 (lane c-review-728-math). It builds eight
mutants of the certificate from review_728_check.py's own reading of it, decides each
with both routes of review_728_check.py, and, given --packing, with both maintained
routes through maintained_routes_728.py (one child process per mutant, at most two at
a time). It writes the mutants to --mutants (not retained; their SHA-256 are) and a
receipt to --out.

    F0  the side lowered by the least top-or-right clearance        contact: accept
    F1  ... and by 1e-30 more                                         refuse
    N0  every square moved toward the least-clearance near wall      contact: accept
        by that clearance
    N1  ... by the clearance + 1e-30                                  refuse
    P0  the second square of the least-gap pair moved along the       contact: accept
        pair's best separating axis toward the first, by the gap
    P1  ... by the gap + 1e-30                                        refuse
    R1  the last row dropped (the header still says n)               both readers refuse
    R2  square 0's x written as its exact decimal                    a reader difference

Usage:
    python3 -I sharp_controls_728.py CERT --mutants DIR --out FILE.json \
        [--packing PACKING --python PY]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import review_728_check as chk  # noqa: E402  (this lane's own checker)

EPS = F(1, 10**30)


def lit(x: F) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def write_cert(comment: str, side: F, poses: list[tuple[F, F, F]]) -> bytes:
    body = "".join(f"{lit(x)} {lit(y)} {lit(t)}\n" for x, y, t in poses)
    return f"# {comment}\n{len(poses)} {lit(side)}\n{body}".encode()


def build(data: bytes) -> dict[str, tuple[bytes, str]]:
    cert = chk.read_certificate(data)
    z = chk.route_z(cert)
    side = F(*cert["side"])
    poses = [(F(*x), F(*y), F(*t)) for x, y, t in cert["rows"]]
    walls = z["least_clearance_by_wall"]
    far = min(("x<=S", "y<=S"), key=lambda w: F(walls[w]["clearance"]))
    near = min(("x>=0", "y>=0"), key=lambda w: F(walls[w]["clearance"]))
    c_far, c_near = F(walls[far]["clearance"]), F(walls[near]["clearance"])
    i, j = z["least_gap_pair"]
    gap = F(z["least_gap"])
    axis = z["least_gap_axis"]

    def basis(t: F) -> tuple[F, F]:
        return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)

    ui, uj = basis(poses[i][2]), basis(poses[j][2])
    w = {"u_i": ui, "v_i": (-ui[1], ui[0]), "u_j": uj, "v_j": (-uj[1], uj[0])}[axis]
    delta = (poses[j][0] - poses[i][0], poses[j][1] - poses[i][1])
    sgn = 1 if delta[0] * w[0] + delta[1] * w[1] > 0 else -1

    def shifted(amount: F) -> list[tuple[F, F, F]]:
        if near == "x>=0":
            return [(x - amount, y, t) for x, y, t in poses]
        return [(x, y - amount, t) for x, y, t in poses]

    def moved(step: F) -> list[tuple[F, F, F]]:
        out = list(poses)
        x, y, t = out[j]
        out[j] = (x - sgn * step * w[0], y - sgn * step * w[1], t)
        return out

    m: dict[str, tuple[bytes, str]] = {}
    m["F0"] = (write_cert(f"F0: side lowered by the least {far} clearance", side - c_far, poses), "accept")
    m["F1"] = (write_cert("F1: and by 1e-30 more", side - c_far - EPS, poses), "refuse")
    m["N0"] = (write_cert(f"N0: all squares moved to the {near} wall by its least clearance", side, shifted(c_near)), "accept")
    m["N1"] = (write_cert("N1: and by 1e-30 more", side, shifted(c_near + EPS)), "refuse")
    m["P0"] = (write_cert(f"P0: square {j} moved along {axis} toward square {i} by the gap", side, moved(gap)), "accept")
    m["P1"] = (write_cert("P1: by the gap + 1e-30", side, moved(gap + EPS)), "refuse")
    lines = data.decode().split("\n")
    m["R1"] = ("\n".join(lines[:-2]).encode() + b"\n", "reader-refuse")
    x0 = poses[0][0]
    assert 10**40 % x0.denominator == 0
    places = 40
    dec = x0.numerator * (10**places // x0.denominator)
    dec_text = f"{dec // 10**places}.{dec % 10**places:0{places}d}".rstrip("0")
    row = lines[2].split(" ")
    lines2 = list(lines)
    lines2[2] = " ".join([dec_text, row[1], row[2]])
    m["R2"] = ("\n".join(lines2).encode(), "reader-difference")
    meta = {
        "far_wall": far,
        "far_clearance": lit(c_far),
        "near_wall": near,
        "near_clearance": lit(c_near),
        "pair": [i, j],
        "axis": axis,
        "gap": lit(gap),
        "moved_square": j,
        "direction_sign": sgn,
        "r2_decimal": dec_text,
    }
    return m, meta


def decide_mine(data: bytes) -> dict:
    try:
        cert = chk.read_certificate(data)
    except chk.CertificateError as exc:
        return {"reader": f"refused: {exc}"}
    out = {}
    for name, route in (("Z", chk.route_z), ("C", chk.route_c)):
        r = route(cert)
        out[name] = {
            "accepted": r["accepted"],
            "least_wall_clearance": r["least_wall_clearance"],
            "wall_contacts": r["wall_contacts"],
            "wall_violations": r["wall_violation_count"],
            "touching_pairs": r["touching_pairs"],
            "overlapping_pairs": r["overlapping_pairs"],
        }
        if name == "Z":
            out[name]["least_gap"] = r["least_gap"]
            out[name]["least_gap_pair"] = r["least_gap_pair"]
        else:
            out[name]["least_squared_distance"] = r["least_squared_distance"]
    return out


def decide_maintained(path: str, packing: str, python: str, here: str) -> dict:
    out_json = path + ".maintained.json"
    cmd = [python, "-I", os.path.join(here, "maintained_routes_728.py"), path, "--packing", packing]
    cmd += ["--n", "303", "--control", "positive", "--out", out_json]
    done = subprocess.run(["nice", "-n", "10", *cmd], capture_output=True, cwd=packing, check=False)
    res = json.load(open(out_json))
    res["exit"] = done.returncode
    return res


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cert")
    ap.add_argument("--mutants", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--packing")
    ap.add_argument("--python", default=sys.executable)
    args = ap.parse_args(argv)
    here = os.path.dirname(os.path.abspath(__file__))
    data = open(args.cert, "rb").read()
    mutants, meta = build(data)
    os.makedirs(args.mutants, exist_ok=True)
    paths = {}
    for name, (text, _) in mutants.items():
        p = os.path.join(args.mutants, f"{name}.cert")
        open(p, "wb").write(text)
        paths[name] = p
    receipt = {"certificate_sha256": hashlib.sha256(data).hexdigest(), "construction": meta, "mutants": {}}
    for name, (text, expected) in mutants.items():
        receipt["mutants"][name] = {
            "expected": expected,
            "sha256": hashlib.sha256(text).hexdigest(),
            "this_review": decide_mine(text),
        }
    if args.packing:
        with ThreadPoolExecutor(max_workers=2) as pool:
            futs = {n: pool.submit(decide_maintained, p, args.packing, args.python, here) for n, p in paths.items()}
            for n, f in futs.items():
                receipt["mutants"][n]["maintained"] = f.result()
    open(args.out, "w").write(json.dumps(receipt, indent=1) + "\n")
    # summary table
    print(json.dumps(meta, indent=1))
    for name, rec in receipt["mutants"].items():
        mine = rec["this_review"]
        if "reader" in mine:
            mine_s = mine["reader"]
        else:
            mine_s = " | ".join(
                f"{r}: {'accept' if mine[r]['accepted'] else 'refuse'} wall {chk.sci(F(mine[r]['least_wall_clearance']).numerator, F(mine[r]['least_wall_clearance']).denominator, 4)}"
                + (f" gap {chk.sci(F(mine['Z']['least_gap']).numerator, F(mine['Z']['least_gap']).denominator, 4)}" if r == "Z" else "")
                + f" touch {len(mine[r]['touching_pairs'])} over {len(mine[r]['overlapping_pairs'])}"
                for r in ("Z", "C")
            )
        print(f"{name} expected {rec['expected']}: this review: {mine_s}")
        if "maintained" in rec:
            mm = rec["maintained"]
            if mm.get("adapter") != "read":
                print(f"    maintained: adapter {mm.get('adapter')}")
            else:
                for r in ("exact_verify", "independent"):
                    v = mm[r]
                    print(
                        f"    {r}: {'accept' if v['verification_passed'] else 'refuse'} wall {v['minimum_containment_clearance'][:60]} "
                        f"gap {v['minimum_best_pair_gap'][:60]} failures {v['failures'][:2]}"
                    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
