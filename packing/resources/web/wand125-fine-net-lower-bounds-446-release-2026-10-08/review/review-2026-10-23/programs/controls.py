"""Controls on this review's own checkers: inputs and conventions they must refuse.

Each control mutates an in-memory copy (the retained files are only read) and records
the outcome a correct checker must give:

- the strict reader refuses a duplicate key, a float token, a negative mass, and a gzip
  stream with a second member;
- the premises refuse a total mass raised by 1/100000 (so M = n), a step of 1/4999
  (B(1 + D) = 1) and a last index of 2071 (the net stops short of tan(pi/8));
- the axis decision does not decide the 99/100 mutant of each certificate;
- at the source's 31 rotated control witnesses of n = 19, four wrong conventions each
  fail to reproduce the source's exact fractions: the other rectangle field order, the
  standard net's step 83/40000 in place of the declared one (the failure mode of DR-1 of
  the 6 October soundness review), half the declared step (close to reading the angle as
  arctan(t) rather than 2 arctan(t)), and the listed rows without their D4 images;
- at the least value the direction sample found at each sampled direction of n = 19,
  the 99/100 mutant's exact capture is below 1, so the sample would find a too-light
  measure.

    OPENBLAS_NUM_THREADS=1 python3 -I controls.py --packet PACKET \
        --sample outputs/direction-sample.json --out outputs/controls.json
"""

from __future__ import annotations

import argparse
import dataclasses
import gzip
import json
import resource
import sys
import zlib
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import axis_decide  # noqa: E402
import premises  # noqa: E402
from t233lib import (  # noqa: E402
    CERTS,
    Measure,
    StrictError,
    as_rect,
    cos_sin,
    exact_capture,
    expand,
    loose_json,
    read_candidate,
    read_gzip_single,
    strict_json,
)


def reader_controls(packet: Path, scratch: Path) -> list[dict]:
    out = []
    for label, text in (
        ("duplicate key", b'{"n": 19, "n": 19}'),
        ("float token", b'{"n": 19, "L": 4.8275}'),
    ):
        try:
            strict_json(text)
            out.append({"control": label, "refused": False})
        except StrictError as exc:
            out.append({"control": label, "refused": True, "message": str(exc)})
    from t233lib import rat  # noqa: PLC0415

    try:
        rat("-1/2")
        out.append({"control": "negative mass", "refused": False})
    except StrictError as exc:
        out.append({"control": "negative mass", "refused": True, "message": str(exc)})
    stored = (packet / "release" / "certificates" / CERTS[19][0] / "candidate.json.gz").read_bytes()
    two = scratch / "two-members.json.gz"
    two.write_bytes(stored + gzip.compress(b"{}"))
    try:
        read_gzip_single(two)
        out.append({"control": "second gzip member", "refused": False})
    except (StrictError, zlib.error) as exc:
        out.append({"control": "second gzip member", "refused": True, "message": str(exc)})
    two.unlink()
    return out


def premise_controls(packet: Path) -> list[dict]:
    cand = read_candidate(packet, 19)
    out = []
    heavy = dataclasses.replace(cand, total_mass=cand.total_mass + Fraction(1, 100000))
    rep = premises.measure_report(heavy, "x1y1x2y2")
    out.append({"control": "total mass n", "refused": not rep["all_hold"],
                "failed": [k for k, v in rep["checks"].items() if not v]})
    for label, change in (("step 1/4999", {"step": Fraction(1, 4999)}), ("last 2071", {"last": 2071})):
        rep = premises.net_report(dataclasses.replace(cand, **change))
        out.append({"control": label, "refused": not rep["all_hold"],
                    "failed": [k for k, v in rep["checks"].items() if not v]})
    return out


def axis_controls(packet: Path) -> list[dict]:
    out = []
    for n in CERTS:
        res = axis_decide.decide(packet, n, scale=Fraction(99, 100))
        out.append({"control": f"axis decision of the 99/100 mutant, n = {n}",
                    "refused": not res["decided_at_least_1"],
                    "rigorous_lower_bound": res["rigorous_lower_bound"],
                    "exact_min": res["exact_min_over_64_smallest"]})
    return out


def wrong_measure(cand, how: str) -> Measure:
    if how == "other field order":
        # rows that are not rectangles in the other order are dropped: the measure is
        # then wrong in two ways, and must still not reproduce the source's values
        keep = []
        for row in cand.rows:
            r = as_rect(row, "x1x2y1y2")
            if r.x1 < r.x2 and r.y1 < r.y2:
                keep.append(dataclasses.replace(row, fields=(r.x1, r.y1, r.x2, r.y2)))
        return expand(dataclasses.replace(cand, rows=keep))
    if how == "no D4 images":
        meas = expand(cand)
        listed = {}
        for row in cand.rows:
            r = as_rect(row, "x1y1x2y2")
            listed[r] = listed.get(r, Fraction(0)) + row.mass / ((r.x2 - r.x1) * (r.y2 - r.y1))
        keep = [k for k, rect in enumerate(meas.rects) if rect in listed]
        meas.rects = [meas.rects[k] for k in keep]
        meas.density = [listed[meas.rects[i]] for i in range(len(keep))]
        meas.mass = [d * (r.x2 - r.x1) * (r.y2 - r.y1) for d, r in zip(meas.density, meas.rects, strict=True)]
        for attr in ("mx", "my", "wx", "wy", "fx1", "fy1", "fx2", "fy2"):
            setattr(meas, attr, getattr(meas, attr)[keep])
        import numpy as np  # noqa: PLC0415

        meas.frho = np.array([float(d) for d in meas.density])
        meas.fmass = np.array([float(m) for m in meas.mass])
        return meas
    return expand(cand)


def convention_controls(packet: Path) -> list[dict]:
    cand = read_candidate(packet, 19)
    name = CERTS[19][0]
    path = packet / "release" / "certificates" / name / "check2" / "control-197_200.jsonl.gz"
    with gzip.open(path, "rb") as fh:
        rows = [loose_json(line) for line in fh.read().splitlines() if line.strip()]
    wit = [r for r in rows if r.get("r", 0) >= 1 and r.get("witness")]
    h = cand.B / 2
    factor = Fraction(197, 200)
    out = []
    steps = {
        "standard step 83/40000": Fraction(83, 40000),  # DR-1's failure mode
        "half the declared step": cand.step / 2,  # roughly arctan(t) for 2 arctan(t)
    }
    hows = ("right conventions", "other field order", *steps, "no D4 images")
    for how in hows:
        meas = wrong_measure(cand, how)
        equal = 0
        for row in wit:
            r = row["r"]
            c, s = cos_sin(steps.get(how, cand.step), r)
            px, py = (Fraction(v) for v in row["witness"]["exact_pose"])
            cap, _i, _b = exact_capture(meas, px, py, c, s, h)
            if factor * cap == Fraction(row["witness"]["exact_coverage"]):
                equal += 1
        out.append({"control": how, "witnesses": len(wit), "equal_to_source_fraction": equal,
                    "refused": equal == 0 if how != "right conventions" else None})
    return out


def sample_controls(packet: Path, sample: Path) -> list[dict]:
    doc = json.loads(sample.read_text())
    cand = read_candidate(packet, 19)
    meas = expand(cand)
    h = cand.B / 2
    below = 0
    total = 0
    for d in doc["cases"]["19"]["directions"]:
        best = min(d["points"], key=lambda p: p["exact"])
        c, s = cos_sin(cand.step, d["r"])
        cap, _i, _b = exact_capture(meas, Fraction(best["x"]), Fraction(best["y"]), c, s, h)
        total += 1
        if cap * Fraction(99, 100) < 1:
            below += 1
    return [{"control": "99/100 mutant at the sample's least points, n = 19",
             "directions": total, "below_1": below, "refused": below == total}]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--packet", type=Path, required=True)
    ap.add_argument("--sample", type=Path, required=True)
    ap.add_argument("--scratch", type=Path, default=Path.cwd())
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    results = {
        "reader": reader_controls(args.packet, args.scratch),
        "premises": premise_controls(args.packet),
        "axis": axis_controls(args.packet),
        "conventions": convention_controls(args.packet),
        "sample": sample_controls(args.packet, args.sample),
    }
    flat = [r for group in results.values() for r in group if r.get("refused") is not None]
    ok = all(r["refused"] for r in flat)
    right = results["conventions"][0]
    ok = ok and right["equal_to_source_fraction"] == right["witnesses"]
    usage = resource.getrusage(resource.RUSAGE_SELF)
    out = {
        "kind": "t233-review-controls/v1",
        "results": results,
        "verdict": "EVERY_CONTROL_REFUSED" if ok else "A_CONTROL_PASSED",
        "cpu_seconds": round(usage.ru_utime + usage.ru_stime, 3),
    }
    args.out.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    for group, rows in results.items():
        for r in rows:
            print(group, r["control"], "refused" if r.get("refused") else r)
    print(out["verdict"], "cpu", out["cpu_seconds"])
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
