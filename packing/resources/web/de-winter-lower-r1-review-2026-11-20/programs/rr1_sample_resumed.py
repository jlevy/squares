"""Lane rR1-lower, resumed: the whole-certificate sample with a wall cap and a checkpoint.

Written after the checker freeze by the agent that resumed the lane (amendment A2 of
frozen/checker-amendments.txt), because the frozen `rr1_runs.py sample` writes a
certificate's receipt only when all of its bins are done, and the first run of it was lost
with the session.  It changes no decision: every bin is decided by the frozen
`rr1_decide.decide` with the frozen limits, threshold 1, the true masses and bin splitting
in three at most twice.  What it adds is orchestration:

  * the certificates in the frozen order, each one computation under a wall cap (the
    resumed lane's rule: 30 minutes, then the certificate is recorded as not completed);
  * a certificate's bins in a seeded order, `random.Random(int(SHA, 16) + i).shuffle` for
    the certificate at index i of the frozen order, so that the bins decided before a cap
    are a uniform sample of its partition and not its first angles;
  * batches of 2 * procs bins, with the results appended to a checkpoint after each batch;
    no batch starts after the cap, and a run killed inside a batch keeps the batches before.

Usage: rr1_sample_resumed.py --root SRC_FOLDER --scratch DIR --out-dir DIR
       [--procs 3] [--wall-cap 1800] [--labels a,b] [--finalize]
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
import rr1_runs as R  # noqa: E402
import rr1_search as S  # noqa: E402


def child_cpu() -> float:
    ch = resource.getrusage(resource.RUSAGE_CHILDREN)
    return ch.ru_utime + ch.ru_stime


def receipt(label: str, order: list[tuple[int, int]], gaps: list, ck: dict, cap: float) -> dict:
    res = ck["results"]
    done = {(r["K"], r["r"]) for r in res if r["depth"] == 0}
    verdicts = {r["verdict"] for r in res if r["verdict"] != "SPLIT"}
    complete = len(done) == len(order)
    if "REFUSED_EXACT" in verdicts:
        verdict = "REFUSED_EXACT"
    elif gaps and complete:
        verdict = "PARTITION_GAP"
    elif "UNDECIDED" in verdicts:
        verdict = "UNDECIDED"
    elif complete:
        verdict = "DECIDED"
    else:
        verdict = "NOT_COMPLETED_WALL_CAP"
    return {
        "program": "rr1_sample_resumed.py", "label": label, "verdict": verdict, "complete": complete,
        "bins": len(order), "bins_run": len(done),
        "bins_accepted_unsplit": sum(1 for r in res if r["depth"] == 0 and r["verdict"] == "ACCEPT"),
        "bins_split": sum(1 for r in res if r["verdict"] == "SPLIT"),
        "bins_not_run": [list(b) for b in order if b not in done],
        "partition_gaps": [[str(x), str(y)] for x, y in gaps],
        "wall_cap_seconds": cap, "nodes": sum(r["nodes"] for r in res),
        "c_seconds": round(sum(r["seconds"] for r in res), 3), "cpu_seconds": round(ck["cpu_seconds"], 3),
        "wall_seconds": round(ck["wall_seconds"], 1), "killed_inside_a_batch": ck.get("killed", False),
        "lattice_Q": ck["lattice_Q"], "lattice_rounded": ck["lattice_rounded"], "G": ck["G"],
        "bin_order_seed": ck["seed"], "results": res,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--procs", type=int, default=3)
    ap.add_argument("--wall-cap", type=float, default=1800.0)
    ap.add_argument("--labels", default="")
    ap.add_argument("--finalize", action="store_true", help="write the receipt of a killed run from its checkpoint")
    a = ap.parse_args()
    root = Path(a.root)
    scratch = Path(a.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    od = Path(a.out_dir)
    od.mkdir(parents=True, exist_ok=True)
    labels_all = S.all_labels(root)
    if len(labels_all) != 77 or R.seeded_picks(labels_all) != [R.SAMPLE[2], R.SAMPLE[4], R.SAMPLE[6], R.SAMPLE[8]]:
        raise SystemExit("the sample is not the frozen rule's")
    todo = a.labels.split(",") if a.labels else R.SAMPLE
    exe = None if a.finalize else C.build_c(scratch)
    for lab in todo:
        i = R.SAMPLE.index(lab)
        name = lab.replace("/", "-")
        ckf = od / f"checkpoint-{name}.json"
        outf = od / f"sample-{name}.json"
        cert = C.load_certificate(S.folder_of(root, lab))
        allb = C.bins_of(cert)
        gaps = C.coverage_gaps(allb)
        seed = int(R.SHA, 16) + i
        order = list(allb)
        random.Random(seed).shuffle(order)
        keys = [(K, r) for K, r, _, _ in order]
        if a.finalize:
            ck = json.loads(ckf.read_text())
            ck["killed"] = True
            outf.write_text(json.dumps(receipt(lab, keys, gaps, ck, a.wall_cap), indent=1) + "\n")
            print(lab, "finalized from the checkpoint", flush=True)
            continue
        if outf.exists():
            print(lab, "already has a receipt; not run again", flush=True)
            continue
        w0 = time.time()
        t0 = time.process_time()
        c0 = child_cpu()
        prep = D.prepare(root, lab, F(1), F(1))
        ck = {"label": lab, "seed": str(seed), "results": [], "cpu_seconds": 0.0, "wall_seconds": 0.0,
              "lattice_Q": prep["lat"]["Q"], "lattice_rounded": prep["lat"]["rounded"], "G": prep["lat"]["G"]}
        step = 2 * a.procs
        for j in range(0, len(order), step):
            if time.time() - w0 >= a.wall_cap:
                break
            ck["results"] += D.decide(exe, prep, order[j:j + step], F(1), scratch, a.procs, 2)
            ck["cpu_seconds"] = time.process_time() - t0 + child_cpu() - c0
            ck["wall_seconds"] = time.time() - w0
            ckf.write_text(json.dumps(ck) + "\n")
        out = receipt(lab, keys, gaps, ck, a.wall_cap)
        outf.write_text(json.dumps(out, indent=1) + "\n")
        ckf.unlink(missing_ok=True)
        print(lab, out["verdict"], out["bins_run"], "of", out["bins"], "nodes", out["nodes"], "cpu", out["cpu_seconds"],
              "wall", out["wall_seconds"], flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
