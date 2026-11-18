"""Scale Hosono's 108-square measure to a specified side and declare the indicated grid."""
from pathlib import Path
from fractions import Fraction as F
import json, gzip, argparse

def make(source, side, core, step, last):
    with gzip.open(source, 'rt') as f:
        candidate = json.load(f)
    scale = F(side) / F(candidate["L"])
    for row in candidate["rectangles"]:
        row["rectangle"] = [str(F(x)*scale) for x in row["rectangle"]]
    candidate.update(L=str(F(side)), B=str(F(core)), proof_net={"step":str(F(step)), "last":last})
    return candidate

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    for k in ["source","side","core","step","output"]:p.add_argument(k)
    p.add_argument("--last", type=int, required=True)
    a=p.parse_args()
    Path(a.output).write_text(json.dumps(make(a.source,a.side,a.core,a.step,a.last),separators=(",",":"))+"\n")
