"""Lane rR2 (issue 1042 derived bounds), check C3: the four translated regions.

For each region claim (137, 138 and 162 from followup/envelopes/claims.json, and the 161
follow-up of issue comment 7020627554) this program checks the hypotheses of the region
lemma, r^2 >= 1/2 and max(q, T - q) + r <= S, and computes rigorous integer bounds on the
mass of the density g with rr2_envelope.cpp: every image's density rounded up (upper
bound) or down (lower bound) to 2^-E, coordinates exact on the 1e-8 grid, the disk rule
for claims with round_steps. It then compares the bounds with n and with the stated mass.

Usage:
  python -I rr2_envelope.py --source DIR --scratch DIR [--out FILE] [--controls] [--bits E]
Standard library only; the C++ part is compiled here with g++. E (default 40) is the
number of binary places each image density is rounded to; the bracket between the two
bounds narrows with E, and a density of 2^(62 - E) per unit area or more is refused.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from rr2_measure import GRID, Measure, read_json  # noqa: E402
from rr2_strips import strip_masses  # noqa: E402

E = 40
R_SOURCE = F(707107, 10**6)  # the overlap radius stated in followup/envelopes/PROOF.md

# The 161 follow-up, transcribed from issue comment 7020627554 (retained in
# programs/issues-1039-1041-1042.json).
K161F = {
    "n": 161,
    "side": "8036307/625000",
    "seam": "18553/5000",
    "mass": "4024992052429083498016487/25000000000000000000000",
    "anchor_dir": "followup/repeated/161--749858-12.858-100-uniform",
}


def build(scratch: Path) -> Path:
    src = HERE / "rr2_envelope.cpp"
    digest = hashlib.sha256(src.read_bytes()).hexdigest()[:16]
    binary = scratch / f"rr2_envelope-{digest}"
    if not binary.exists():
        subprocess.run(
            ["g++", "-O2", "-std=c++17", "-o", str(binary), str(src)],
            check=True,
        )
    return binary


def rounded_images(measure: Measure) -> list[tuple[int, int, int, int, int, int]]:
    scale = 2**E
    out = []
    for x0, y0, x1, y1, dens in measure.images():
        v = dens * scale
        dn = v.numerator // v.denominator
        up = -((-v.numerator) // v.denominator)
        if up >= 2**62:
            raise ValueError("density too large for the integer sweep")
        out.append((x0, y0, x1, y1, up, dn))
    return out


def hypotheses(S: F, T: F, q: F, r: F) -> dict:
    return {
        "r_squared_at_least_half": r * r >= F(1, 2),
        "regions_fit_in_anchor": max(q, T - q) + r <= S,
        "overlap_inside_board": 0 < q - r and q + r < T,
        "on_grid": all((v * GRID).denominator == 1 for v in (S, T, q, r)),
    }


def integrate(binary: Path, scratch: Path, imgs, S: F, T: F, q: F, r: F, disk: bool) -> dict:
    lines = [
        f"{int(S * GRID)} {int(T * GRID)} {int(q * GRID)} {int(r * GRID)} "
        f"{1 if disk else 0} {E} {len(imgs)}"
    ]
    lines.extend(" ".join(str(v) for v in img) for img in imgs)
    data = ("\n".join(lines) + "\n").encode()
    proc = subprocess.run([str(binary), "sweep"], input=data, capture_output=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode())
    fields = dict(line.split(" ", 1) for line in proc.stdout.decode().splitlines())
    unit = F(1, 2**E * GRID * GRID)
    return {
        "mass_up": int(fields["I_up"]) * unit,
        "mass_dn": int(fields["I_dn"]) * unit,
        "slabs": int(fields["slabs"]),
        "cells": int(fields["cells"]),
        "straddling_cells": int(fields["straddles"]),
    }


def frac(v: F) -> dict:
    return {"exact": str(v), "approx": float(v)}


def envelope_claim(binary, scratch, imgs, S, n, T, q, r, disk, stated) -> dict:
    hyp = hypotheses(S, T, q, r)
    rep: dict = {"n": n, "side": str(T), "seam": str(q), "r": str(r), "disk": disk,
                 "hypotheses": hyp}
    if not all(hyp.values()):
        rep["decided"] = False
        rep["refused_by"] = [k for k, v in hyp.items() if not v]
        return rep
    res = integrate(binary, scratch, imgs, S, T, q, r, disk)
    rep.update({
        "mass_upper": frac(res["mass_up"]),
        "mass_lower": frac(res["mass_dn"]),
        "bracket_width": float(res["mass_up"] - res["mass_dn"]),
        "slack_upper": frac(n - res["mass_up"]),
        "slabs": res["slabs"],
        "cells": res["cells"],
        "straddling_cells": res["straddling_cells"],
    })
    if stated is not None:
        rep["stated_mass"] = frac(stated)
        rep["lower_at_most_stated"] = res["mass_dn"] <= stated
        rep["upper_at_most_stated"] = res["mass_up"] <= stated
        rep["stated_minus_upper"] = float(stated - res["mass_up"])
    rep["decided"] = res["mass_up"] < n
    rep["refused"] = res["mass_dn"] >= n
    return rep


def same_primitives(a: Path, b: Path) -> bool:
    return read_json(a)["rectangles"] == read_json(b)["rectangles"]


def main() -> int:
    global E
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--scratch", required=True, type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--controls", action="store_true")
    ap.add_argument("--only", help="comma-separated claim keys to run")
    ap.add_argument("--bits", type=int, default=40, help="binary places of a density")
    args = ap.parse_args()
    if not 20 <= args.bits <= 60:
        raise SystemExit("--bits must lie in [20, 60]")
    E = args.bits
    args.scratch.mkdir(parents=True, exist_ok=True)
    binary = build(args.scratch)
    src = args.source
    report: dict = {"program": "rr2_envelope.py", "E": E, "claims": {}}
    claims = json.loads((src / "followup/envelopes/claims.json").read_text())
    jobs = []
    for cl in claims:
        anchor = src / "followup/envelopes" / cl["folder"] / "proof/k100.json.gz"
        twin = src / "followup/repeated" / cl["folder"] / "proof/k100.json.gz"
        T = F(cl["side"])
        jobs.append((f"K{cl['n']}e", cl["n"], anchor, twin, T, T / 2, "round_steps" in cl,
                     F(cl["mass"])))
    T = F(K161F["side"])
    jobs.append(("K161f", K161F["n"], src / K161F["anchor_dir"] / "proof/k100.json.gz", None,
                 T, F(K161F["seam"]), False, F(K161F["mass"])))
    only = set(args.only.split(",")) if args.only else None
    cache: dict[Path, tuple] = {}
    for key, n, anchor, twin, T, q, disk, stated in jobs:
        if only and key not in only:
            continue
        if anchor not in cache:
            m = Measure.from_file(anchor)
            cache[anchor] = (m, rounded_images(m))
        m, imgs = cache[anchor]
        rep = envelope_claim(binary, args.scratch, imgs, m.side, n, T, q, R_SOURCE, disk, stated)
        rep["anchor"] = str(anchor.relative_to(src))
        rep["anchor_side"] = str(m.side)
        rep["anchor_mass"] = frac(m.total())
        if twin is not None:
            rep["same_primitives_as_repeated_anchor"] = same_primitives(anchor, twin)
        report["claims"][key] = rep
        print(key, "decided" if rep["decided"] else "NOT decided", flush=True)
    if not only or "cross" in only:
        # plain regions at T = S - 1 on A162a must give the strip mass M(-1)
        anchor = src / "followup/envelopes/162--719881-12.881-100-uniform_finish/proof/k100.json.gz"
        if anchor not in cache:
            m = Measure.from_file(anchor)
            cache[anchor] = (m, rounded_images(m))
        m, imgs = cache[anchor]
        sm = strip_masses(m.images(), m.S, 3)
        m_minus = m.total() - (sm["bx"] + sm["by"]) + sm["c"]
        T = m.side - 1
        res = integrate(binary, args.scratch, imgs, m.side, T, T / 2, R_SOURCE, False)
        report["cross_check_T_equals_S_minus_1"] = {
            "strip_mass_M_minus_1": frac(m_minus),
            "mass_upper": frac(res["mass_up"]),
            "mass_lower": frac(res["mass_dn"]),
            "contains": res["mass_dn"] <= m_minus <= res["mass_up"],
        }
        print("cross-check", report["cross_check_T_equals_S_minus_1"]["contains"], flush=True)
    if args.controls:
        ctl: dict = {}
        m, imgs = next(iter(cache.values()))
        a161 = src / K161F["anchor_dir"] / "proof/k100.json.gz"
        m161 = Measure.from_file(a161)
        T = F(K161F["side"])
        hyp = hypotheses(m161.side, T, F(K161F["seam"]), F(707106, 10**6))
        ctl["r_707106"] = {"refused": not all(hyp.values()), "hypotheses": hyp}
        hyp = hypotheses(m161.side, T, F(1, 2), R_SOURCE)
        ctl["seam_one_half"] = {"refused": not all(hyp.values()), "hypotheses": hyp}
        ctl["all_refused"] = all(v["refused"] for v in ctl.values())
        info = {}
        for key, n, anchor, twin, T, q, disk, stated in jobs:
            if only and key not in only:
                continue
            m, imgs = cache[anchor]
            T2 = T + F(1, 1000)
            q2 = T2 / 2 if key != "K161f" else q
            rep = envelope_claim(binary, args.scratch, imgs, m.side, n, T2, q2, R_SOURCE, disk,
                                 None)
            info[key] = {k: rep.get(k) for k in ("side", "mass_upper", "mass_lower", "refused")}
            print("side+1/1000", key, rep.get("refused"), flush=True)
        ctl["side_plus_one_thousandth"] = info
        report["controls"] = ctl
        report["controls_verdict"] = (
            "ALL_CONTROLS_REFUSED" if ctl["all_refused"] else "CONTROL_ACCEPTED"
        )
    decided = all(c["decided"] for c in report["claims"].values())
    report["verdict"] = "REGION_CLAIMS_DECIDED" if decided else "NOT_DECIDED"
    text = json.dumps(report, indent=1, default=str)
    if args.out:
        args.out.write_text(text + "\n")
    print(report["verdict"], report.get("controls_verdict", ""))
    return 0 if decided else 1


if __name__ == "__main__":
    raise SystemExit(main())
