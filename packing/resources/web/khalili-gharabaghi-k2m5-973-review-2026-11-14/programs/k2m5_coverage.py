"""Clean-room re-implementation of the coverage step (paper Proposition 12) for the review of #973 (L144).

usage: python -I k2m5_coverage.py COVDIR TTDIR OUT_JSON [MUTATE]
  COVDIR  the zmx2 dumps r<id>.out of the 75 tight-tile roots (all uncertified boxes printed)
  TTDIR   the source's tight_tile/ folder (job outputs in out/, out_u2000/, out_fix/, out_u2000_fix/)
  MUTATE  optional "M-4": widen the first box of the first dump to u1 = U0 + 2^-40 (the control)

Written from the paper's statement of the Tight-Tile Lemma (Theorem 11) and its chart table (section 6.3),
not from cov_check.py.  Checks, in exact rationals:
  1. every leftover box, with its u = 0 face removed, lies in the lemma's domain for one (d0, sign):
     |x - d0| <= 1/1000, y in I(d0), u <= 1/4000 (sign +1, left wall), or the same with x and y exchanged
     (sign -1, bottom wall by the diagonal reflection); or in one of the five ranges with u0 = 1/2000,
     delta_max = 1/500, the range extended by 1/500;
  2. the jobs needed for that domain exist: for every (d0, sign) and every range of I(d0), a line job at every
     base line y_b in (1/10)Z within the range and a strip job between consecutive base lines; for the five
     further ranges, both end lines and the strip between them at u0 = 1/2000;
  3. every needed job's final output reports, for every chart of the chart table (C_u, W_t +-, W_d +-, four
     W_td pairs a/b; S_u, S_d +- for strips), zero refused cells at h0 = u0 and K = 4, a rerun in the *_fix
     folder overriding exactly the charts it reports.
"""
import glob
import json
import os
import re
import sys
from fractions import Fraction as F

U0, DM = F(1, 4000), F(1, 1000)
U0b, DMb = F(1, 2000), F(1, 500)
I = {F(3, 2): [("1.4", "1.7"), ("2.4", "2.7"), ("3.3", "5.5")],
     F(5, 2): [("1.4", "1.7"), ("2.3", "2.7"), ("3.3", "3.7"), ("3.8", "5.5")],
     F(7, 2): [("1.4", "1.7"), ("2.3", "2.7"), ("3.3", "3.7"), ("4.1", "4.5")]}
I = {d: [(F(a), F(b)) for a, b in rs] for d, rs in I.items()}
EXTRA = [(F(3, 2), 1, F("4.2"), F("4.3")), (F(3, 2), 1, F("4.5"), F("4.6")), (F(3, 2), -1, F("3.8"), F("3.9")),
         (F(3, 2), -1, F("5.4"), F("5.5")), (F(5, 2), -1, F("4.4"), F("4.5"))]
LINE_CHARTS = ["C_u", "W_t t+1", "W_t t-1", "W_d d+1", "W_d d-1"] + \
    [f"W_td t{a} d{b} {c}" for a in ("+1", "-1") for b in ("+1", "-1") for c in ("a", "b")]
STRIP_CHARTS = ["S_u", "S_d d+1", "S_d d-1"]


def in_domain(box):
    x0, x1, y0, y1, u0, u1 = box
    for d0, rs in I.items():
        for (d_lo, d_hi, h_lo, h_hi, sg) in ((x0, x1, y0, y1, 1), (y0, y1, x0, x1, -1)):
            if u1 <= U0 and d0 - DM <= d_lo and d_hi <= d0 + DM and any(a <= h_lo and h_hi <= b for a, b in rs):
                return ("main", str(d0), sg)
    for d0, sg, a, b in EXTRA:
        d_lo, d_hi, h_lo, h_hi = (x0, x1, y0, y1) if sg == 1 else (y0, y1, x0, x1)
        if u1 <= U0b and d0 - DMb <= d_lo and d_hi <= d0 + DMb and a - DMb <= h_lo and h_hi <= b + DMb:
            return ("extra", str(d0), sg)
    return None


def tenth(v):
    return f"{float(v):.1f}"


def needed_jobs():
    main, extra = [], []
    for d0, rs in I.items():
        for sg in (1, -1):
            lines = sorted({F(j, 10) for a, b in rs for j in range(int(a * 10), int(b * 10) + 1)})
            for y in lines:
                main.append((d0, sg, "line", tenth(y)))
                if y + F(1, 10) in lines:
                    main.append((d0, sg, "strip", tenth(y) + "+", tenth(y + F(1, 10)) + "-"))
    for d0, sg, a, b in EXTRA:
        extra += [(d0, sg, "line", tenth(a)), (d0, sg, "strip", tenth(a) + "+", tenth(b) + "-"), (d0, sg, "line", tenth(b))]
    return main, extra


def read_out(path):
    lines = [ln for ln in open(path).read().split("\n") if ln.strip()]
    charts = {}
    for ln in lines:
        if ln.startswith("{"):
            d = json.loads(ln)
            if "fails" in d:
                charts[d["chart"]] = d
    return (lines[-1] if lines else ""), charts


NO_K = set()     # jobs whose chart lines do not record K (the published run_tt.py prints it)


def check_job(ttd, job, u0, folder, fix_folder):
    d0, sg, kind = job[0], job[1], job[2]
    args = job[3:]
    name = f"d{float(d0)}_s{sg}_{kind}_{'_'.join(args)}"
    cands = [p for p in [os.path.join(ttd, folder, name + ".out")] + glob.glob(os.path.join(ttd, folder, glob.escape(name) + "_*.out")) if os.path.exists(p)]
    if len(cands) != 1:
        return name, f"{len(cands)} outputs"
    last, charts = read_out(cands[0])
    if last not in ("ALL-OK", "NOT-OK"):
        return name, "unfinished"
    fx = os.path.join(ttd, fix_folder, name + ".out")
    if os.path.exists(fx):
        flast, fch = read_out(fx)
        if not flast.startswith(("ALL-OK", "NOT-OK", "PARTIAL-")):
            return name, "fix unfinished"
        charts.update(fch)
    expect = LINE_CHARTS if kind == "line" else STRIP_CHARTS
    tile = f"d0={d0} sign={sg} {kind} {' '.join(args)}"
    for c in expect:
        d = charts.get(c)
        if d is None:
            return name, f"chart {c} missing"
        if "K" not in d:
            NO_K.add(name)
        if d["fails"] != 0 or F(d["h0"]) != u0 or F(d.get("K", 4)) != 4:
            return name, f"chart {c}: fails {d['fails']} h0 {d['h0']} K {d.get('K')}"
        if not (d["tile"] == tile or (kind == "line" and d["tile"].startswith(tile + " "))):
            return name, f"chart {c}: tile {d['tile']!r}"
    extra = sorted(set(charts) - set(expect))
    if extra:
        return name, f"unexpected charts {extra}"
    return name, "ok"


def main():
    covd, ttd, out = sys.argv[1:4]
    mutate = len(sys.argv) > 4 and sys.argv[4] == "M-4"
    pat = re.compile(r"^UNCERT (\d+) pass \d+ box (\S+) ")
    n = 0
    outside = []
    kinds = {}
    files = sorted(glob.glob(os.path.join(covd, "r*.out")))
    finished = 0
    for fi, f in enumerate(files):
        txt = open(f).read()
        finished += "\ndone in" in txt
        first = True
        for line in txt.split("\n"):
            m = pat.match(line)
            if not m:
                continue
            box = [F(t) for t in m.group(2).split(",")]
            if mutate and fi == 0 and first:
                box[5] = U0 + F(1, 2 ** 40)
            first = False
            n += 1
            if box[4] < 0:
                outside.append((m.group(1), "u0 < 0"))
                continue
            r = in_domain(box)
            if r is None:
                outside.append((m.group(1), [str(v) for v in box]))
            else:
                kinds[r] = kinds.get(r, 0) + 1
    main_jobs, extra_jobs = needed_jobs()
    bad_main = [r for r in (check_job(ttd, j, U0, "out", "out_fix") for j in main_jobs) if r[1] != "ok"]
    bad_extra = [r for r in (check_job(ttd, j, U0b, "out_u2000", "out_u2000_fix") for j in extra_jobs) if r[1] != "ok"]
    res = dict(files=len(files), finished=finished, boxes=n, outside=len(outside), outside_first=outside[:5],
               by_domain={f"{k[0]} d0={k[1]} sign={k[2]}": v for k, v in sorted(kinds.items(), key=str)},
               main_jobs_needed=len(main_jobs), main_jobs_not_ok=bad_main[:10], extra_jobs_needed=len(extra_jobs),
               extra_jobs_not_ok=bad_extra[:10], jobs_without_K_recorded=len(NO_K), mutated="M-4" if mutate else None)
    res["verdict"] = "COVERED" if (not outside and not bad_main and not bad_extra and len(files) == 75 and finished == 75) else "NOT-COVERED"
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
