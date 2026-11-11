"""Tests of this review's own evaluators and readers; it decides nothing about the claims.

Usage: python -I selftest.py --release DIR --out FILE

1. The two exact methods (polygon clipping, and vertical chords integrated exactly) agree
   as fractions at random and adversarial poses at directions 1, 2, 7, 296, 1036, 1777,
   2071 and 2072 of both certificates, and the binary64 estimate used by the search
   agrees with them to 1e-9.
2. Conventions: at the 31 oblique 197/200 control witnesses of each certificate, the
   reading used here reproduces every logged fraction, and each wrong reading reproduces
   none: the other field order, the standard net's step 83/40000, half the declared step,
   and the rows without their D4 images.
3. The strict reader and premises refuse mutated copies: a duplicate key, a float token,
   a second gzip member, a nonpositive mass, a total mass of n, a step of 1/4999 (so
   B(1 + D) = 1) and a last index of 2071 (the net stops short of tan(pi/8)).
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import random
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fnlib as F  # noqa: E402
import premises as P  # noqa: E402

NAMES = ("mixed_n28_L57425", "mixed_n30_L58925")
DIRS = (1, 2, 7, 296, 1036, 1777, 2071, 2072)


def agreement(cert: F.Cert, m: F.Measure, rng: random.Random, per_dir: int) -> dict:
    fm = F.FloatMeasure(m)
    L, b = cert.L, cert.B / 2
    worst_float = 0.0
    n = 0
    for j in DIRS:
        u = F.upper_end(j, L)
        c, s = F.cos_sin(j)
        pts = []
        for _ in range(per_dir):
            pts.append((L / 2 + (u - L / 2) * Fraction(rng.randrange(10**6), 10**6),
                        L / 2 + (u - L / 2) * Fraction(rng.randrange(10**6), 10**6)))
        # Adversarial: put a core vertex exactly on an image corner near the pose.
        for k in rng.sample(range(len(m.keys)), 4):
            X0, Y0, X1, Y1 = m.keys[k]
            cx, cy = X0 + b * (c - s), Y0 + b * (s + c)  # p4 (the bottom vertex) at (X0, Y0)
            if L / 2 <= cx <= u and L / 2 <= cy <= u:
                pts.append((cx, cy))
        for cx, cy in pts:
            e1 = F.capture(m, j, cx, cy)
            e2 = F.chord_capture(m, j, cx, cy)
            if e1 != e2:
                raise AssertionError(f"exact methods differ at {j}, {cx}, {cy}")
            f = F.fcapture(fm, float(c), float(s), float(b), float(cx), float(cy))
            worst_float = max(worst_float, abs(f - float(e1)))
            n += 1
    return {"poses": n, "exact_methods_equal": True, "largest_float_error": worst_float}


def conventions(rel: Path, name: str) -> dict:
    cdir = rel / name
    ctl = [json.loads(x) for x in gzip.open(cdir / "check2" / "control-197_200.jsonl.gz", "rt")][:-1]
    wits = [(r["r"], r["witness"]) for r in ctl if r["r"] != 0]
    good = F.read_candidate(cdir / "candidate.json.gz")
    swapped = F.read_candidate(cdir / "candidate.json.gz", field_order="x0x1y0y1")
    bad_rows = sum(1 for r in swapped.rows if not (r[2] > r[0] and r[3] > r[1]))
    readings = {
        "this review's reading": (F.Measure(F.expand(good.rows, good.L)), F.STEP),
        "standard step 83/40000": (F.Measure(F.expand(good.rows, good.L)), Fraction(83, 40000)),
        "half the declared step": (F.Measure(F.expand(good.rows, good.L)), F.STEP / 2),
        "rows without D4 images": (F.Measure(F.expand(good.rows, good.L, d4=False)), F.STEP),
    }
    if bad_rows == 0:
        readings["other field order"] = (F.Measure(F.expand(swapped.rows, swapped.L)), F.STEP)
    # A witness is angle-sensitive when, under this review's reading, the capture at its
    # centre differs between its own angle and the axis; elsewhere the core lies where the
    # density is constant and no reading of the angle can be told apart.
    m0 = readings["this review's reading"][0]
    sensitive = set()
    for j, w in wits:
        cx, cy = Fraction(w["exact_pose"][0]), Fraction(w["exact_pose"][1])
        if F.capture(m0, j, cx, cy) != F.capture(m0, 0, cx, cy):
            sensitive.add(j)
    out: dict = {"angle_sensitive_witnesses": len(sensitive)}
    for label, (m, step) in readings.items():
        hits, hits_sensitive = 0, 0
        for j, w in wits:
            cx, cy = Fraction(w["exact_pose"][0]), Fraction(w["exact_pose"][1])
            if Fraction(197, 200) * F.capture(m, j, cx, cy, step=step) == F.rat(w["exact_coverage"]):
                hits += 1
                hits_sensitive += j in sensitive
        out[label] = f"{hits} of {len(wits)} ({hits_sensitive} of {len(sensitive)} angle-sensitive)"
    out["other field order"] = out.get("other field order", f"refused: {bad_rows} rows of no positive area")
    return out


def refusals(rel: Path) -> dict:
    raw = (rel / NAMES[0] / "candidate.json.gz").read_bytes()
    text = F.gunzip_one(raw).decode()
    out = {}

    def reader(label: str, data: bytes) -> None:
        try:
            F.parse_candidate(data)
            out[label] = "ACCEPTED"
        except F.StrictError as exc:
            out[label] = f"refused: {str(exc)[:60]}"

    reader("duplicate key", text.replace('"n": 28,', '"n": 28, "n": 28,', 1).encode())
    reader("float token", text.replace('"total_mass": "2799999/100000"', '"total_mass": 27.99999', 1).encode())
    reader("second gzip member", raw + gzip.compress(b"{}"))

    def premise(label: str, new_text: str) -> None:
        tmp = Path(out_dir) / "mutant.json.gz"
        tmp.write_bytes(gzip.compress(new_text.encode()))
        try:
            cert = F.read_candidate(tmp)
            fails = []
            if not all(r[4] > 0 for r in cert.rows):
                fails.append("nonpositive mass")
            if sum((r[4] for r in cert.rows), Fraction(0)) != cert.total_mass or not cert.total_mass < cert.n:
                fails.append("mass")
            n0 = P.net_premises(cert.B, cert.step, cert.last)
            fails += [k for k in ("b_holds", "c_holds", "e_holds") if not n0[k]]
            out[label] = f"refused: {fails}" if fails else "ACCEPTED"
        except F.StrictError as exc:
            out[label] = f"refused: {str(exc)[:60]}"
        finally:
            tmp.unlink()

    first_mass = text.split('"mass": "', 1)[1].split('"', 1)[0]
    premise("nonpositive mass", text.replace(f'"mass": "{first_mass}"', f'"mass": "-{first_mass}"', 1))
    premise("total mass n", text.replace('"total_mass": "2799999/100000"', '"total_mass": "28"', 1))
    premise("step 1/4999", text.replace('"step": "1/5002"', '"step": "1/4999"', 1))
    premise("last 2071", text.replace('"last": 2072', '"last": 2071', 1))
    return out


out_dir = "."


def main() -> int:
    global out_dir
    ap = argparse.ArgumentParser()
    ap.add_argument("--release", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--per-dir", type=int, default=10)
    args = ap.parse_args()
    out_dir = str(Path(args.out).parent)
    rel = Path(args.release)
    t0 = time.process_time()
    res: dict = {"agreement": {}, "conventions": {}}
    for name in NAMES:
        cert = F.read_candidate(rel / name / "candidate.json.gz")
        m = F.Measure(F.expand(cert.rows, cert.L))
        seed = int(hashlib.sha256(cert.sha256.encode()).hexdigest()[:16], 16)
        res["agreement"][name] = agreement(cert, m, random.Random(seed), args.per_dir)
        res["conventions"][name] = conventions(rel, name)
        print(name, res["agreement"][name], res["conventions"][name])
    res["refusals"] = refusals(rel)
    print(res["refusals"])
    ok = (all(a["exact_methods_equal"] and a["largest_float_error"] < 1e-9 for a in res["agreement"].values())
          and all(c["this review's reading"].startswith("31 of 31")
                  and c["rows without D4 images"].startswith("0 of")
                  and all(v.startswith("refused") or v.endswith(f"(0 of {c['angle_sensitive_witnesses']} angle-sensitive)")
                          for k, v in c.items() if k not in ("this review's reading", "angle_sensitive_witnesses"))
                  for c in res["conventions"].values())
          and all(v.startswith("refused") for v in res["refusals"].values()))
    res["status"] = "PASS" if ok else "FAIL"
    res["cpu_seconds"] = round(time.process_time() - t0, 1)
    F.write_json(args.out, {"program": "selftest.py", **res})
    print(res["status"])
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
