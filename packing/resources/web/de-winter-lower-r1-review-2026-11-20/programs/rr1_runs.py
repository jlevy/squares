"""Lane rR1-lower: the planned runs of the decider.

  tier1     two bins of each of the 77 certificates: the bin holding the least exact
            capture the seeded search found, and one seeded random bin
  controls  A1 to A4 of the frozen plan at the least-capture bin of each sampled certificate
  sample    whole certificates in the frozen order, under the frozen CPU rule

Usage: rr1_runs.py MODE --root SRC_FOLDER --search out/search.json --scratch DIR --out-dir DIR
"""

from __future__ import annotations

import argparse
import json
import random
import resource
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rr1_common as C  # noqa: E402
import rr1_decide as D  # noqa: E402
import rr1_search as S  # noqa: E402

SHA = "7a3b186a2e65c7f277c20770eb6727420f895862"
SAMPLE = ["1042/n136", "1041/n114", "1042/n129", "1042/n132", "1042/n115", "1041/n115", "1041/n107", "1042/n135",
          "1041/n111"]
CAP_CPU_SECONDS = 24 * 3600


def seeded_picks(labels: list[str]) -> list[str]:
    """Recompute the plan's seeded picks, so the list above is checked against the rule."""
    det = ["1042/n136", "1041/n114", "1042/n132", "1041/n115", "1042/n135"]
    rest = sorted(set(labels) - set(det))
    return random.Random(int(SHA, 16)).sample(rest, 4)


def child_cpu() -> float:
    ch = resource.getrusage(resource.RUSAGE_CHILDREN)
    return ch.ru_utime + ch.ru_stime


def least_bin(search: dict, label: str) -> tuple[int, int]:
    rec = next(r for r in search["results"] if r["label"] == label)
    return tuple(rec["bins_holding_least_t"][0])


def run(exe: Path, root: Path, label: str, sel: list[tuple[int, int]] | None, scratch: Path, procs: int,
        factor: F = F(1), stretch: F = F(1), threshold: F = F(1), widen: int = 0, split: int = 2) -> dict:
    t0 = time.process_time()
    c0 = child_cpu()
    w0 = time.time()
    prep = D.prepare(root, label, factor, stretch)
    allb = C.bins_of(prep["cert"])
    bins = allb if sel is None else [b for b in allb if (b[0], b[1]) in set(sel)]
    if sel is not None and len(bins) != len(set(sel)):
        raise SystemExit(f"{label}: unknown bin")
    if widen:
        bins = [(K, r, l - widen * (h - l), h + widen * (h - l)) for K, r, l, h in bins]
    res = D.decide(exe, prep, bins, threshold, scratch, procs, split)
    return {
        "label": label, "n": prep["n"], "L": str(prep["L"]), "factor": str(factor), "stretch": str(stretch),
        "threshold": str(threshold), "widen": widen, "bins": len(bins), "verdict": D.summarize(res),
        "nodes": sum(r["nodes"] for r in res), "c_seconds": round(sum(r["seconds"] for r in res), 3),
        "cpu_seconds": round(time.process_time() - t0 + child_cpu() - c0, 3), "wall_seconds": round(time.time() - w0, 1),
        "lattice_Q": prep["lat"]["Q"], "lattice_rounded": prep["lat"]["rounded"], "G": prep["lat"]["G"],
        "results": res,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["tier1", "controls", "sample"])
    ap.add_argument("--root", required=True)
    ap.add_argument("--search", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--procs", type=int, default=2)
    ap.add_argument("--labels", default="")
    a = ap.parse_args()
    root = Path(a.root)
    scratch = Path(a.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    od = Path(a.out_dir)
    od.mkdir(parents=True, exist_ok=True)
    exe = C.build_c(scratch)
    search = json.loads(Path(a.search).read_text())
    labels_all = S.all_labels(root)
    if len(labels_all) != 77 or seeded_picks(labels_all) != [SAMPLE[2], SAMPLE[4], SAMPLE[6], SAMPLE[8]]:
        raise SystemExit("the sample is not the frozen rule's")
    if a.mode == "tier1":
        todo = a.labels.split(",") if a.labels else labels_all
        for lab in todo:
            i = labels_all.index(lab)
            cert = C.load_certificate(S.folder_of(root, lab))
            allb = [(K, r) for K, r, _, _ in C.bins_of(cert)]
            rnd = random.Random(int(SHA, 16) + i).choice(allb)
            sel = sorted({least_bin(search, lab), rnd})
            out = run(exe, root, lab, sel, scratch, min(a.procs, len(sel)))
            out["least_bin"] = list(least_bin(search, lab))
            out["seeded_bin"] = list(rnd)
            (od / f"tier1-{lab.replace('/', '-')}.json").write_text(json.dumps(out, indent=1) + "\n")
            print(lab, out["verdict"], out["nodes"], out["cpu_seconds"], flush=True)
    elif a.mode == "controls":
        todo = a.labels.split(",") if a.labels else SAMPLE
        for lab in todo:
            lb = least_bin(search, lab)
            rec = next(r for r in search["results"] if r["label"] == lab)
            least = F(rec["least"]["capture"])
            for cid, kw, expect in (
                ("A1", {"factor": F(99, 100)}, {"REFUSED_EXACT"}),
                ("A2", {"threshold": least + F(1, 10**4)}, {"REFUSED_EXACT"}),
                ("A3", {"stretch": F(1001, 1000)}, {"REFUSED_EXACT"}),
                ("A4", {"widen": 2, "split": 0}, {"UNDECIDED", "REFUSED_EXACT"}),
            ):
                out = run(exe, root, lab, [lb], scratch, 1, **kw)
                out["control"] = cid
                out["expected"] = sorted(expect)
                out["as_planned"] = out["verdict"] in expect
                (od / f"control-{cid}-{lab.replace('/', '-')}.json").write_text(json.dumps(out, indent=1) + "\n")
                print(lab, cid, out["verdict"], "as planned" if out["as_planned"] else "NOT AS PLANNED", flush=True)
    else:
        spent = 0.0
        per_bin = []
        for lab in SAMPLE:
            cert = C.load_certificate(S.folder_of(root, lab))
            nb = len(C.bins_of(cert))
            if per_bin:
                proj = nb * (sum(c for c, _ in per_bin) / sum(b for _, b in per_bin))
                if spent + proj > CAP_CPU_SECONDS:
                    print(lab, "SKIPPED by the CPU rule, projected", round(proj), flush=True)
                    (od / f"sample-{lab.replace('/', '-')}.json").write_text(
                        json.dumps({"label": lab, "verdict": "NOT_RUN_CPU_RULE", "projected": proj}) + "\n")
                    continue
            out = run(exe, root, lab, None, scratch, a.procs)
            gaps = C.coverage_gaps(C.bins_of(cert))
            out["partition_gaps"] = [[str(x), str(y)] for x, y in gaps]
            if gaps:
                out["verdict"] = "PARTITION_GAP"
            spent += out["cpu_seconds"]
            per_bin.append((out["cpu_seconds"], nb))
            (od / f"sample-{lab.replace('/', '-')}.json").write_text(json.dumps(out, indent=1) + "\n")
            print(lab, out["verdict"], out["bins"], out["nodes"], out["cpu_seconds"], flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
