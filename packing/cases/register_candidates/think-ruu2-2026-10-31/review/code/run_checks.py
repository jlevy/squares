"""Decide the three candidates (and, for comparison, the three houses) on both routes.

Usage: python3.14 -I run_checks.py INPUTS_DIR OUT_DIR [labels...]
Writes OUT_DIR/check-<label>.json and prints one line per route.
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path

import qio
import route_area
import route_sat


def jsonable(v: object) -> object:
    if isinstance(v, Fraction):
        return {"exact": str(v), "approx": f"{float(v):.6e}" if v else "0"}
    if isinstance(v, dict):
        return {k: jsonable(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [jsonable(x) for x in v]
    return v


def subjects(inp: Path) -> dict[str, tuple[Fraction, list[qio.Square], str]]:
    out: dict[str, tuple[Fraction, list[qio.Square], str]] = {}
    for n in (130, 307):
        _, side, sq, _ = qio.read_view(inp / f"n{n}-view-solved.yaml")
        out[f"cand{n}"] = (side, sq, f"n{n}-view-solved.yaml")
        _, side, sq, _ = qio.read_tcert(inp / f"n{n}-solve-witness.cert")
        out[f"solve{n}"] = (side, sq, f"n{n}-solve-witness.cert")
    _, s260, sq260, _ = qio.read_tcert(inp / "s260_1028.cert")
    out["s260"] = (s260, sq260, "s260_1028.cert")
    for variant in ("16+16+1", "17+16", "17top+16"):
        out[f"cand293-{variant}"] = (s260 + 1, sq260 + qio.l_strip(s260, variant), f"s260_1028.cert + L {variant}")
    for n in (130, 293, 307):
        _, side, sq, _ = qio.read_view(inp / f"house-n{n}.yaml")
        out[f"house{n}"] = (side, sq, f"house-n{n}.yaml")
    return out


def main() -> None:
    inp, outdir = Path(sys.argv[1]), Path(sys.argv[2])
    labels = sys.argv[3:]
    outdir.mkdir(parents=True, exist_ok=True)
    subj = subjects(inp)
    for label in labels or list(subj):
        side, sq, src = subj[label]
        rec: dict[str, object] = {"label": label, "source": src, "n": len(sq), "side": side}
        for name, mod in (("A", route_sat), ("B", route_area)):
            t0 = time.process_time()
            res = mod.check(side, sq)
            res["cpu_seconds"] = round(time.process_time() - t0, 2)
            rec[name] = res
            extra = ""
            if name == "A":
                lp = res["least_pair_slack"]
                lw = res["least_wall_clearance"]
                extra = (
                    f" least pair slack {float(lp[0]):.6e} (squares {lp[1] + 1},{lp[2] + 1})"
                    f" least wall {float(lw[0]):.6e} (square {lw[1] + 1} {lw[2]})"
                    f" side-extent {float(side - res['extent_hi']):.6e}"
                )
            else:
                extra = f" clipped {res['pairs_clipped']}"
            print(
                f"{label:22s} route {name}: accepted={res['accepted']} n={res['n']} pairs={res['pairs_decided']}"
                f"{extra} cpu={res['cpu_seconds']}s",
                flush=True,
            )
        (outdir / f"check-{label}.json").write_text(json.dumps(jsonable(rec), indent=1) + "\n")


if __name__ == "__main__":
    main()
