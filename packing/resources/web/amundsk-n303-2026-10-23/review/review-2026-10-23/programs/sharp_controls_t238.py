#!/usr/bin/env python3
"""Sharp, gross and reader controls for the issue 755 certificate, on four deciders.

Written for the stage 4 review of T-238 (bead think-jdz0) after its checker had decided.
A premise check: it builds mutants of the certificate exactly and records what each
decider says of each; the deciders decide.

Each mutant is written as certificate text in the certificate's own format, rows the
mutant does not change keeping their original literals, and every decider reads that text
with its own reader:

- routes Z and E of `review_t238_check.py`, loaded from its path;
- the two maintained routes, `exact_verify` and `independent`, reached as
  `upper_bound_reports certify`'s child reaches them: the `evand-cert` adapter, then
  `devtools.evand_arrangement_reports.run_case` on the `positive` job.

The mutants (eps = 1e-30, exact):

- F0, F1: the side lowered by the least top-or-right clearance, and by eps more.
- N0, N1: every square moved left by the least left clearance, and by eps more.
- B0, B1: every square moved down by the least bottom clearance, and by eps more.
- P0, P1: the second square of the least-gap pair moved along the pair's closing normal
  by the gap, and by eps more.
- Q0, Q1: the same for the tightest pair of a square tilted beyond 1 degree and an
  exactly aligned one.
- T0, T1: the same for the tightest pair of two squares tilted beyond 1 degree at one angle.
- U0, U1: the same for the tightest pair of two squares tilted beyond 1 degree at angles
  more than 0.5 degree apart.
- D0, D1: the tightest pair whose centres are more than sqrt(2) apart, a corner-to-corner
  near-contact: the second square moved by the vector between their nearest corners, and
  by eps more along each axis, toward the first.
- G1: square 1 replaced by a copy of square 0. G2: square 0 moved right by S + 2.
- M1: every tangent negated, the mirrored reading of the format.
- R1: the last row dropped. R2: square 0's x written as its exact decimal.

Usage:
  python3 -I -B sharp_controls_t238.py CERT --checker review_t238_check.py \
      --packing /home/user/squares/packing --declaration report.json --out OUT.json
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
import math
import platform
import sys
import time
from fractions import Fraction as Q
from pathlib import Path

EPS = Q(1, 10**30)


def load_checker(path: str):
    spec = importlib.util.spec_from_file_location("review_t238_check", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def lit(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def basis(t: Q) -> tuple[Q, Q]:
    w = 1 + t * t
    return (1 - t * t) / w, 2 * t / w


def corners(x: Q, y: Q, t: Q) -> list[tuple[Q, Q]]:
    c, s = basis(t)
    u, v = (c, s), (-s, c)
    h = Q(1, 2)
    return [
        (x + su * h * u[0] + sv * h * v[0], y + su * h * u[1] + sv * h * v[1])
        for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    ]


def aligned(t: Q) -> bool:
    """Exactly aligned: t in {0, 1, -1}."""
    return t in (0, 1, -1)


def tilt_degrees(t: Q) -> float:
    """The rotation modulo 90 degrees, in (-45, 45], for choosing pairs only."""
    deg = math.degrees(2 * math.atan(float(t)))
    return ((deg + 45.0) % 90.0) - 45.0


def tilted(t: Q) -> bool:
    """Tilted by more than 1 degree modulo 90."""
    return abs(tilt_degrees(t)) > 1.0


class Cert:
    def __init__(self, data: bytes):
        lines = data.decode("ascii").split("\n")
        if lines[-1] == "":
            lines.pop()
        k = 0
        while lines[k].startswith("#"):
            k += 1
        self.comments = lines[:k]
        n_text, s_text = lines[k].split(" ")
        self.n = int(n_text)
        self.side_text = s_text
        self.row_text = [line.split(" ") for line in lines[k + 1 :]]
        self.side = Q(s_text)
        self.rows = [[Q(tok) for tok in row] for row in self.row_text]

    def text(self, side: Q | None = None, changes: dict | None = None, drop_last: bool = False, raw: dict | None = None) -> bytes:
        changes = changes or {}
        raw = raw or {}
        out = list(self.comments)
        out.append(f"{self.n} {self.side_text if side is None else lit(side)}")
        rows = range(self.n - 1) if drop_last else range(self.n)
        for k in rows:
            if k in raw:
                out.append(raw[k])
            elif k in changes:
                out.append(" ".join(lit(v) for v in changes[k]))
            else:
                out.append(" ".join(self.row_text[k]))
        return ("\n".join(out) + "\n").encode("ascii")


def pair_table(checker, data: bytes):
    """Route Z's per-pair gaps and axes for the original certificate."""
    cert = checker.read_certificate(data)
    buf = io.StringIO()
    checker.route_z(cert, buf)
    table = {}
    for line in buf.getvalue().splitlines():
        i, j, gap, axis = line.split("\t")
        table[(int(i), int(j))] = (Q(gap), int(axis))
    return table


def build(data: bytes, checker) -> tuple[list[dict], dict]:
    c = Cert(data)
    xs = [r[0] for r in c.rows]
    ys = [r[1] for r in c.rows]
    ts = [r[2] for r in c.rows]
    half = []
    for t in ts:
        cc, ss = basis(t)
        half.append((abs(cc) + abs(ss)) / 2)
    left = min(xs[k] - half[k] for k in range(c.n))
    right = min(c.side - xs[k] - half[k] for k in range(c.n))
    bottom = min(ys[k] - half[k] for k in range(c.n))
    top = min(c.side - ys[k] - half[k] for k in range(c.n))
    top_right = min(right, top)
    table = pair_table(checker, data)
    info = {
        "least_clearances": {"left": lit(left), "right": lit(right), "bottom": lit(bottom), "top": lit(top)},
    }
    mutants = []

    def add(name, text, expect, note):
        mutants.append({"name": name, "text": text, "expect": expect, "note": note})

    add("F0", c.text(side=c.side - top_right), "accept", "side lowered by the least top-or-right clearance")
    add("F1", c.text(side=c.side - top_right - EPS), "refuse", "and by 1e-30 more")
    add("N0", c.text(changes={k: (xs[k] - left, ys[k], ts[k]) for k in range(c.n)}), "accept", "every square left by the least left clearance")
    add("N1", c.text(changes={k: (xs[k] - left - EPS, ys[k], ts[k]) for k in range(c.n)}), "refuse", "and by 1e-30 more")
    add("B0", c.text(changes={k: (xs[k], ys[k] - bottom, ts[k]) for k in range(c.n)}), "accept", "every square down by the least bottom clearance")
    add("B1", c.text(changes={k: (xs[k], ys[k] - bottom - EPS, ts[k]) for k in range(c.n)}), "refuse", "and by 1e-30 more")

    def axis_vector(i, j, k):
        ci, si = basis(ts[i])
        cj, sj = basis(ts[j])
        return [(ci, si), (-si, ci), (cj, sj), (-sj, cj)][k]

    def closing(i, j):
        gap, k = table[(i, j)]
        w = axis_vector(i, j, k)
        dot = (xs[j] - xs[i]) * w[0] + (ys[j] - ys[i]) * w[1]
        sign = 1 if dot > 0 else -1
        return gap, (-sign * w[0], -sign * w[1]), k

    def far(i, j):
        return (xs[j] - xs[i]) ** 2 + (ys[j] - ys[i]) ** 2 > 2

    def tightest(pred):
        best = None
        for key, (gap, _k) in table.items():
            if pred(*key) and (best is None or gap < table[best][0]):
                best = key
        return best

    picks = {
        "P": tightest(lambda i, j: not far(i, j)),
        "Q": tightest(
            lambda i, j: not far(i, j)
            and ((tilted(ts[i]) and aligned(ts[j])) or (aligned(ts[i]) and tilted(ts[j])))
        ),
        "T": tightest(lambda i, j: not far(i, j) and tilted(ts[i]) and tilted(ts[j]) and ts[i] == ts[j]),
        "U": tightest(
            lambda i, j: not far(i, j)
            and tilted(ts[i])
            and tilted(ts[j])
            and abs(tilt_degrees(ts[i]) - tilt_degrees(ts[j])) > 0.5
        ),
    }
    names = ("u_i", "v_i", "u_j", "v_j")
    for label, (i, j) in picks.items():
        gap, d, k = closing(i, j)
        kind = {
            "P": "the least gap",
            "Q": "one tilted beyond 1 degree, one exactly aligned",
            "T": "two tilted beyond 1 degree, at one angle",
            "U": "two tilted beyond 1 degree, at angles more than 0.5 degree apart",
        }[label]
        info[label] = {
            "pair": [i, j],
            "gap": lit(gap),
            "axis": names[k],
            "kind": kind,
            "tilts": [lit(ts[i]), lit(ts[j])],
            "tilt_degrees": [round(tilt_degrees(ts[i]), 4), round(tilt_degrees(ts[j]), 4)],
        }
        for suffix, step in (("0", gap), ("1", gap + EPS)):
            moved = (xs[j] + step * d[0], ys[j] + step * d[1], ts[j])
            add(
                label + suffix,
                c.text(changes={j: moved}),
                "accept" if suffix == "0" else "refuse",
                f"square {j} moved toward square {i} along {names[k]} by the gap" + ("" if suffix == "0" else " + 1e-30"),
            )
    # the diagonal near-contact
    i, j = tightest(far)
    gap, k = table[(i, j)]
    ki, kj = corners(xs[i], ys[i], ts[i]), corners(xs[j], ys[j], ts[j])
    best = None
    for a in ki:
        for b in kj:
            d2 = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
            if best is None or d2 < best[0]:
                best = (d2, a, b)
    d2, a, b = best
    vec = (a[0] - b[0], a[1] - b[1])
    sx = 1 if vec[0] > 0 else -1
    sy = 1 if vec[1] > 0 else -1
    info["D"] = {
        "pair": [i, j],
        "gap": lit(gap),
        "axis": names[k],
        "centre_distance_squared_minus_2": lit((xs[j] - xs[i]) ** 2 + (ys[j] - ys[i]) ** 2 - 2),
        "corner_distance_squared": lit(d2),
        "corner_vector": [lit(vec[0]), lit(vec[1])],
        "tilts": [lit(ts[i]), lit(ts[j])],
    }
    add("D0", c.text(changes={j: (xs[j] + vec[0], ys[j] + vec[1], ts[j])}), "accept", f"square {j} moved onto square {i}'s nearest corner")
    add(
        "D1",
        c.text(changes={j: (xs[j] + vec[0] + sx * EPS, ys[j] + vec[1] + sy * EPS, ts[j])}),
        "refuse",
        "and 1e-30 further on each axis",
    )
    add("G1", c.text(changes={1: tuple(c.rows[0])}), "refuse", "square 1 replaced by a copy of square 0")
    add("G2", c.text(changes={0: (xs[0] + c.side + 2, ys[0], ts[0])}), "refuse", "square 0 moved right by S + 2")
    add("M1", c.text(changes={k: (xs[k], ys[k], -ts[k]) for k in range(c.n)}), "refuse", "every tangent negated: the mirrored reading")
    add("R1", c.text(drop_last=True), "unreadable", "the last row dropped")
    x0 = xs[0]
    den = x0.denominator
    places = 0
    while den % 10 == 0 or den % 2 == 0 or den % 5 == 0:
        if den % 10 == 0:
            den //= 10
        elif den % 2 == 0:
            den //= 2
        else:
            den //= 5
        places += 1
    places = max(places, 1)
    scaled = x0 * 10**places
    assert scaled.denominator == 1 and den == 1
    digits = str(scaled.numerator).rjust(places + 1, "0")
    decimal = digits[:-places] + "." + digits[-places:]
    assert Q(decimal) == x0
    add("R2", c.text(raw={0: " ".join([decimal] + c.row_text[0][1:])}), "reader difference", "square 0's x as its exact decimal")
    return mutants, info


def decide_mine(checker, text: bytes) -> dict:
    out = {}
    try:
        cert = checker.read_certificate(text)
    except checker.ReadError as exc:
        return {"Z": {"verdict": "unreadable", "reason": str(exc)}, "E": {"verdict": "unreadable", "reason": str(exc)}}
    for route, fn in (("Z", checker.route_z), ("E", checker.route_e)):
        res = fn(cert)
        walls = res["least_wall"]
        least_wall = min((Q(v["clearance"]) for v in walls.values()))
        row = {
            "verdict": "accept" if res["accepted"] else "refuse",
            "least_wall": lit(least_wall),
            "walls_at_zero": {w: v["squares"] for w, v in walls.items() if Q(v["clearance"]) == 0},
            "walls_failing": [list(x) for x in res["wall_failures"][:10]],
            "touching": [list(p[:2]) for p in res["touching_pairs"][:10]],
            "touching_count": res["touching_count"],
            "overlapping": [list(p[:3]) if route == "E" else list(p[:3]) for p in res["overlapping_pairs"][:10]],
            "overlapping_count": res["overlapping_count"],
        }
        if route == "Z" and res["least_gap"] is not None:
            row["least_gap"] = res["least_gap"]["gap"]
            row["least_gap_pairs"] = [[p["i"], p["j"]] for p in res["least_gap"]["pairs"][:6]]
        out[route] = row
    return out


def decide_maintained(reports, kernel, profile, text: bytes) -> dict:
    try:
        cert = reports.evand_cert(text, 303, {})
    except reports.ReportError as exc:
        return {r: {"verdict": "unreadable", "reason": str(exc)} for r in kernel.ROUTES}
    row = kernel.run_case(cert, "positive", **profile)
    return {
        route: {
            "verdict": "accept" if row[route]["verification_passed"] else "refuse",
            "least_wall": row[route]["minimum_containment_clearance"],
            "least_gap": row[route]["minimum_best_pair_gap"],
            "failures": len(row[route]["failures"]),
        }
        for route in kernel.ROUTES
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cert")
    ap.add_argument("--checker", required=True)
    ap.add_argument("--packing", required=True)
    ap.add_argument("--declaration", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", nargs="*")
    args = ap.parse_args()
    checker = load_checker(args.checker)
    sys.path.insert(0, str(Path(args.packing).resolve()))
    from devtools import evand_arrangement_reports as kernel  # noqa: PLC0415
    from devtools import upper_bound_reports as reports  # noqa: PLC0415

    declaration = json.loads(Path(args.declaration).read_text())
    profile = {"witness_prefix": declaration["witness_prefix"], "claim_limitations": declaration["claim_limitations"]}
    data = Path(args.cert).read_bytes()
    mutants, info = build(data, checker)
    results = []
    for m in mutants:
        if args.only and m["name"] not in args.only:
            continue
        started = time.perf_counter()
        mine = decide_mine(checker, m["text"])
        theirs = decide_maintained(reports, kernel, profile, m["text"])
        verdicts = {"Z": mine["Z"]["verdict"], "E": mine["E"]["verdict"]} | {r: theirs[r]["verdict"] for r in theirs}
        if m["expect"] == "reader difference":
            as_expected = verdicts["Z"] == verdicts["E"] == "unreadable" and all(theirs[r]["verdict"] == "accept" for r in theirs)
        else:
            as_expected = all(v == m["expect"] for v in verdicts.values())
        results.append(
            {
                "name": m["name"],
                "note": m["note"],
                "expect": m["expect"],
                "text_sha256": hashlib.sha256(m["text"]).hexdigest(),
                "verdicts": verdicts,
                "as_expected": as_expected,
                "review_routes": mine,
                "maintained_routes": theirs,
                "wall_seconds": round(time.perf_counter() - started, 2),
            }
        )
        print(m["name"], verdicts, "as expected" if as_expected else "NOT AS EXPECTED", flush=True)
    receipt = {
        "program": "sharp_controls_t238.py",
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(args.checker).read_bytes()).hexdigest(),
        "input_sha256": hashlib.sha256(data).hexdigest(),
        "python": platform.python_version(),
        "epsilon": "1/10^30",
        "pairs": info,
        "mutants": results,
        "all_as_expected": all(r["as_expected"] for r in results),
    }
    Path(args.out).write_text(json.dumps(receipt, indent=2) + "\n")
    return 0 if receipt["all_as_expected"] else 1


if __name__ == "__main__":
    sys.exit(main())
