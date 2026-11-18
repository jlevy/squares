"""Do #1018's archived direction runs cover every direction its argument needs?

Lane r108-1118, blind review of jlevy/squares#1018. Reads the source's twelve
`evidence/direction_runs/directions_AAA_BBB.jsonl.gz` files as data (it runs nothing) and
checks, against values this program recomputes from the measure file itself:

- every file: one JSON object per line, no duplicate key, the last line the run's summary,
  the others one record per direction, the file name's range the records' range;
- every record: verdict `verified` at threshold 1 with a least certified bound of at least
  1; the axis sweep at r = 0 only, with vertices = x events * y events and its argmin in
  the quadrant [L/2, L - 1/2]^2; branch and bound elsewhere, with a complete tree
  (nodes = 2 leaves - 1) and its least-bound box centred in the quadrant [L/2, U_r]^2;
- every summary: the premises this program recomputes (format M, per-bin domain, the
  declared net's D, last tangent and count, B, L, n, the exact and missing mass, B(1 + D),
  the row and merged image counts, no points or segments, and the SHA-256 of the
  decompressed measure), the reviewed crate source, no refusal, no injected fault, and
  node, direction and CPU totals equal to the records';
- the union: every index 0 to last exactly once.

Usage: python -I rv1018_runs.py --runs DIR --measure M.json.gz --reviewed-source SHA
         --out OUT.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rv1018_common as cm  # noqa: E402

NAME = re.compile(r"^directions_(\d{3})_(\d{3})\.jsonl\.gz$")


class Dec(str):
    """A JSON float token, kept as its text."""


def load_lines(path: Path) -> list[dict]:
    _raw, payload = cm.read_one_member(path)
    out = []
    for line in payload.decode().splitlines():
        if line.strip():
            out.append(json.loads(line, object_pairs_hook=cm._pairs, parse_float=Dec))
    return out


def expected_premises(meas: dict) -> dict:
    rects = cm.expand(meas["rows"], meas["L"])
    return {
        "B": str(meas["B"]),
        "D": str(meas["step"]),
        "L": str(meas["L"]),
        "angle_count": meas["last"] + 1,
        "centre_domain": "per-bin",
        "expanded_points": 0,
        "expanded_rectangles": len(rects),
        "expanded_segments": 0,
        "format": "M",
        "input_sha256": meas["json_sha256"],
        "mass_below_n": str(meas["n"] - meas["total_mass"]),
        "mass_exact": str(meas["total_mass"]),
        "n": meas["n"],
        "net_last_tangent": str(meas["last"] * meas["step"]),
        "net_origin": "proof_net",
        "shrink_bound": str(meas["B"] * (1 + meas["step"])),
        "source_rectangles": len(meas["rows"]),
    }


def fr(v: object) -> Fraction:
    return Fraction(str(v))


def check_runs(files: dict[str, list[dict]], meas: dict, reviewed: str) -> dict:
    fails: list[str] = []
    exp = expected_premises(meas)
    side, step, last = meas["L"], meas["step"], meas["last"]
    seen: dict[int, str] = {}
    table = []
    totals = {"nodes": 0, "cpu_seconds": Fraction(0), "direction_seconds": Fraction(0)}
    summaries = []
    for name in sorted(files):
        lines = files[name]
        m = NAME.match(name)
        if not m:
            fails.append(f"{name}: unexpected file name")
            continue
        lo, hi = int(m.group(1)), int(m.group(2))
        if not lines or lines[-1].get("kind") != "sqverify-fast-summary/v1":
            fails.append(f"{name}: last line is not a summary")
            continue
        summ, recs = lines[-1], lines[:-1]
        if any("kind" in x or "r" not in x for x in recs):
            fails.append(f"{name}: a line that is neither record nor final summary")
        rs = sorted(x.get("r") for x in recs)
        if rs != list(range(lo, hi + 1)):
            fails.append(f"{name}: records are not exactly r = {lo}..{hi}")
        fnodes = 0
        fcpu = Fraction(0)
        fsec = Fraction(0)
        for x in recs:
            r = x.get("r")
            if not isinstance(r, int):
                fails.append(f"{name}: a record without an integer r")
                continue
            if r in seen:
                fails.append(f"r = {r} appears in {seen[r]} and {name}")
            seen[r] = name
            if x.get("verdict") != "verified":
                fails.append(f"r = {r}: verdict {x.get('verdict')!r}")
            if x.get("threshold") != "1":
                fails.append(f"r = {r}: threshold {x.get('threshold')!r}")
            bound = fr(x.get("min_certified_lower_bound", "0"))
            if not bound >= 1:
                fails.append(f"r = {r}: least certified bound below 1")
            fcpu += fr(x.get("cpu_seconds", 0))
            fsec += fr(x.get("seconds", 0))
            row = {"r": r, "method": x.get("method"), "bound": str(x.get("min_certified_lower_bound"))}
            upper = cm.domain_upper(r, step, side)
            if r == 0:
                if x.get("method") != "axis-vertex-sweep":
                    fails.append("r = 0: not the axis sweep")
                if x.get("vertices") != x.get("x_events", -1) * x.get("y_events", -1):
                    fails.append("r = 0: vertices are not x events times y events")
                ax, ay = (Fraction(v) for v in x.get("argmin", ["-1", "-1"]))
                if not (side / 2 <= ax <= upper and side / 2 <= ay <= upper):
                    fails.append("r = 0: argmin outside the quadrant")
                row.update(
                    x_events=x.get("x_events"),
                    y_events=x.get("y_events"),
                    vertices=x.get("vertices"),
                    argmin=x.get("argmin"),
                )
            else:
                if x.get("method") != "interval-branch-and-bound":
                    fails.append(f"r = {r}: not branch and bound")
                nodes, leaves = x.get("nodes", -1), x.get("leaves", -1)
                if nodes != 2 * leaves - 1:
                    fails.append(f"r = {r}: tree not complete (nodes != 2 leaves - 1)")
                fnodes += nodes
                box = x.get("least_bound_box") or {}
                bx, by = fr(box.get("x", -1)), fr(box.get("y", -1))
                if not (side / 2 <= bx <= upper and side / 2 <= by <= upper):
                    fails.append(f"r = {r}: least-bound box centre outside the quadrant")
                row.update(
                    nodes=nodes,
                    leaves=leaves,
                    max_depth=x.get("max_depth"),
                    box=[str(box.get(k)) for k in ("x", "y", "dx", "dy")],
                    cpu=str(x.get("cpu_seconds")),
                )
            table.append(row)
        prem = summ.get("premises", {})
        for k, v in exp.items():
            if prem.get(k) != v:
                fails.append(f"{name}: premise {k} is {prem.get(k)!r}, expected {v!r}")
        extra = sorted(set(prem) - set(exp))
        if extra:
            fails.append(f"{name}: unexpected premises {extra}")
        if (summ.get("build") or {}).get("source_sha256") != reviewed:
            fails.append(f"{name}: crate source is not the reviewed one")
        if summ.get("refused_directions") != []:
            fails.append(f"{name}: refused directions {summ.get('refused_directions')}")
        if summ.get("fault_injected_at_box") is not None:
            fails.append(f"{name}: a fault was injected")
        if summ.get("threshold") != "1":
            fails.append(f"{name}: summary threshold {summ.get('threshold')!r}")
        if summ.get("directions") != len(recs):
            fails.append(f"{name}: summary counts {summ.get('directions')} directions")
        if summ.get("nodes") != fnodes:
            fails.append(f"{name}: summary nodes {summ.get('nodes')} != records' {fnodes}")
        if abs(fr(summ.get("direction_cpu_seconds", 0)) - fcpu) > Fraction(1, 10**6):
            fails.append(f"{name}: summary direction CPU differs from the records'")
        if abs(fr(summ.get("direction_seconds", 0)) - fsec) > Fraction(1, 10**6):
            fails.append(f"{name}: summary direction seconds differ from the records'")
        totals["nodes"] += fnodes
        totals["cpu_seconds"] += fcpu
        totals["direction_seconds"] += fsec
        summaries.append(
            {
                "file": name,
                "status": summ.get("status"),
                "threads": summ.get("threads"),
                "directions": summ.get("directions"),
                "nodes": summ.get("nodes"),
                "direction_cpu_seconds": str(summ.get("direction_cpu_seconds")),
                "wall_seconds": str(summ.get("wall_seconds")),
                "build": summ.get("build"),
            }
        )
    missing = sorted(set(range(last + 1)) - set(seen))
    if missing:
        fails.append(f"directions missing: {missing[:20]}{'...' if len(missing) > 20 else ''}")
    stray = sorted(set(seen) - set(range(last + 1)))
    if stray:
        fails.append(f"directions outside the net: {stray}")
    table.sort(key=lambda t: t["r"])
    rot = [t for t in table if t["r"] >= 1]
    least = min(rot, key=lambda t: fr(t["bound"])) if rot else None
    return {
        "verdict": "RUNS_COVER_THE_NET" if not fails else "RUNS_DO_NOT_COVER_THE_NET",
        "failures": fails,
        "expected_premises": exp,
        "reviewed_source": reviewed,
        "directions_seen": len(seen),
        "total_rotated_nodes": totals["nodes"],
        "total_direction_cpu_seconds": float(totals["cpu_seconds"]),
        "total_direction_seconds": float(totals["direction_seconds"]),
        "least_rotated_certified_bound": least,
        "summaries": summaries,
        "directions": table,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True)
    ap.add_argument("--measure", required=True)
    ap.add_argument("--reviewed-source", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    meas = cm.read_measure(args.measure)
    files = {p.name: load_lines(p) for p in sorted(Path(args.runs).glob("*"))}
    res = check_runs(files, meas, args.reviewed_source)
    res["program"] = "rv1018_runs.py"
    res["files"] = sorted(files)
    Path(args.out).write_text(json.dumps(res, separators=(",", ":")) + "\n")
    print(res["verdict"], res["failures"][:10])
    print("directions", res["directions_seen"], "rotated nodes", res["total_rotated_nodes"])
    return 0 if not res["failures"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
