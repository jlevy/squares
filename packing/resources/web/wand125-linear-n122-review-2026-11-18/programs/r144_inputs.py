"""Do the 201 checker inputs encode the candidate? Exact enclosure, row by row.

Usage: r144_inputs.py --bundle BUNDLE_DIR --out OUT.json

Each input.txt is read as data: a header of six intervals (expected: L, B, E_j, cos, sin,
gamma), then blocks, each a count line followed by that many rows of hex-float interval
pairs. A block of 2-coordinate rows is points; of 4-coordinate rows, segments or
rectangles (told apart by matching). For every row the program finds an exact D4 image
of a primitive (fractions) whose coordinates the row's intervals enclose, and uses each
image once: the input must be exactly the multiset of the 14,184 images. The weight
field is tested against both readings, the image's mass m/8 and its density (mass over
length or area); the reading that every row encloses is reported.

Verdict INPUTS_ENCODE_CANDIDATE when all 201 headers enclose the recomputed values and
every body encodes the images; INPUTS_FAIL otherwise.
Written for this review; imports nothing from jlevy/squares or the source.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from r144_common import angle_data, expand_images, load_candidate  # noqa: E402


def _ulps(lo: float, hi: float) -> int:
    import math

    n = 0
    x = lo
    while x < hi and n < 64:
        x = math.nextafter(x, math.inf)
        n += 1
    return n


def iv(lo_s: str, hi_s: str):
    lo = float.fromhex(lo_s)
    hi = float.fromhex(hi_s)
    return lo, hi


def split_input(data: bytes):
    lines = data.decode("ascii").split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    header = [ln.split() for ln in lines[:6]]
    body_start = sum(len(ln) + 1 for ln in lines[:6])
    blocks = []
    i = 6
    while i < len(lines):
        f = lines[i].split()
        if len(f) != 1:
            raise ValueError(f"line {i + 1}: expected a count")
        n = int(f[0])
        rows = [lines[k].split() for k in range(i + 1, i + 1 + n)]
        if len(rows) != n:
            raise ValueError("short block")
        blocks.append(rows)
        i += 1 + n
    return header, blocks, data[body_start:]


def enclose(lo: float, hi: float, q: F) -> bool:
    return F(lo) <= q <= F(hi)


def floats_between(lo: float, hi: float, limit: int = 8):
    """Every binary64 value in [lo, hi], or None when there are more than limit."""
    import math

    out = [lo]
    x = lo
    while x < hi:
        x = math.nextafter(x, math.inf)
        out.append(x)
        if len(out) > limit:
            return None
    return out


def check_header(header, ang, L, B):
    names = ["L", "B", "E", "cos", "sin", "gamma"]
    exact = [L, B, ang["E"], ang["cos"], ang["sin"], F(1)]
    res = {}
    ok = True
    for nm, row, q in zip(names, header, exact):
        if len(row) != 2:
            return False, {"error": f"header {nm} arity"}
        lo, hi = iv(*row)
        good = lo <= hi and enclose(lo, hi, q)
        res[nm] = good
        ok &= good
    return ok, res


def check_body(blocks, prims, L):
    imgs = expand_images(prims, L)
    by_kind = {}
    for kind, g, m, i, gi in imgs:
        by_kind.setdefault(kind, []).append((g, m, i, gi))
    report = {"blocks": []}
    used_all = True
    for rows in blocks:
        width = len(rows[0]) if rows else 0
        if any(len(r) != width for r in rows):
            return False, {"error": "ragged block"}
        if width == 6:
            kinds = ["point"]
        elif width == 10:
            kinds = ["rectangle", "segment"]
        else:
            return False, {"error": f"width {width}"}
        done = False
        for kind in kinds:
            pool = by_kind.get(kind, [])
            if len(pool) != len(rows):
                continue
            ncoord = 2 if kind == "point" else 4
            index = {}
            for k, (g, m, i, gi) in enumerate(pool):
                key = tuple(float(v) for v in g)
                index.setdefault(key, []).append(k)
            used = [False] * len(pool)
            readings = {"mass": 0, "density": 0}
            unmatched = 0
            flipped = 0
            widths = []
            for r in rows:
                ivs = [iv(r[2 * q], r[2 * q + 1]) for q in range(ncoord + 1)]
                coords = ivs[:ncoord]
                wlo, whi = ivs[ncoord]
                cands = []
                orders = [list(range(ncoord))]
                if kind == "segment":
                    orders.append([2, 3, 0, 1])
                if kind == "rectangle":
                    orders += [[2, 1, 0, 3], [0, 3, 2, 1], [2, 3, 0, 1]]
                for order in orders:
                    choices = [floats_between(coords[o][0], coords[o][1]) for o in order]
                    if any(ch is None for ch in choices):
                        continue
                    for combo in itertools.product(*choices):
                        for k in index.get(tuple(combo), []):
                            if not used[k]:
                                cands.append((k, order))
                hit = None
                for k, order in cands:
                    g, m, i, gi = pool[k]
                    if all(enclose(coords[order[q]][0], coords[order[q]][1], g[q]) for q in range(ncoord)):
                        if kind == "point":
                            meas = 1
                        elif kind == "segment":
                            meas = max(abs(g[2] - g[0]), abs(g[3] - g[1])) if (g[0] == g[2] or g[1] == g[3]) else None
                        else:
                            meas = (g[2] - g[0]) * (g[3] - g[1])
                        rd = None
                        if enclose(wlo, whi, m):
                            rd = "mass"
                        elif meas is not None and enclose(wlo, whi, m / meas):
                            rd = "density"
                        if rd is not None:
                            hit = (k, order, rd)
                            break
                if hit is None:
                    unmatched += 1
                    continue
                used[hit[0]] = True
                readings[hit[2]] += 1
                if hit[1] != list(range(ncoord)):
                    flipped += 1
                widths.append(max(_ulps(c[0], c[1]) for c in ivs))
            ok = unmatched == 0 and all(used)
            report["blocks"].append({"kind": kind, "rows": len(rows), "unmatched": unmatched, "all_images_used": all(used), "weight_reading": readings, "rows_with_coordinates_reordered": flipped, "widest_interval_ulps": max(widths) if widths else None})
            used_all &= ok
            done = True
            break
        if not done:
            return False, {"error": f"no kind has {len(rows)} images of width {width}"}
    kinds_seen = sorted(b["kind"] for b in report["blocks"])
    return used_all and kinds_seen == ["point", "rectangle", "segment"], report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    t0 = time.process_time()
    cand = load_candidate(open(os.path.join(a.bundle, "candidate.json"), "rb").read())
    L, B, D = cand["L"], cand["B"], cand["step"]
    headers_ok = []
    bodies = {}
    first_blocks = {}
    for j in range(201):
        data = open(os.path.join(a.bundle, f"net{j:03d}", "input.txt"), "rb").read()
        header, blocks, body = split_input(data)
        ok, det = check_header(header, angle_data(j, D, L, B), L, B)
        headers_ok.append((j, ok, det))
        h = hashlib.sha256(body).hexdigest()
        bodies.setdefault(h, []).append(j)
        if h not in first_blocks:
            first_blocks[h] = blocks
    body_reports = {}
    all_body_ok = True
    for h, blocks in first_blocks.items():
        ok, rep = check_body(blocks, cand["primitives"], L)
        body_reports[h] = {"angles": bodies[h], "ok": ok, "report": rep}
        all_body_ok &= ok
    bad_headers = [j for j, ok, _ in headers_ok if not ok]
    verdict = "INPUTS_ENCODE_CANDIDATE" if not bad_headers and all_body_ok else "INPUTS_FAIL"
    res = {
        "program": "r144_inputs.py",
        "verdict": verdict,
        "headers_enclose_L_B_E_cos_sin_gamma": 201 - len(bad_headers),
        "bad_headers": bad_headers,
        "distinct_bodies": len(bodies),
        "bodies": body_reports,
        "cpu_seconds": round(time.process_time() - t0, 2),
    }
    with open(a.out, "w") as f:
        json.dump(res, f, indent=1)
        f.write("\n")
    print(verdict, f"headers ok {201 - len(bad_headers)}/201, distinct bodies {len(bodies)}, cpu {res['cpu_seconds']} s")
    return 0 if verdict == "INPUTS_ENCODE_CANDIDATE" else 1


if __name__ == "__main__":
    sys.exit(main())
