"""Audit the measure, every direction receipt, and the rational extension of the bound."""
import argparse
import gzip
import hashlib
import json
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path
from stretch_measure import make

ROOT = Path(__file__).resolve().parent
SOURCE_SHA = "4d72da64052667a3ebf057f7e78ea9d40f1521a0b86ddef210a2be319d27042a"
VERIFIER_SHA = "d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88"


def check(condition, message):
    if not condition:
        raise ValueError(message)


def axis_capture(rectangles, L, B, center):
    """Integrate the density exactly at one stored axis-direction center."""
    cx,cy = center
    def overlap(a, b, c):
        return max(F(0), min(b,c+B/2)-max(a,c-B/2))
    capture = F(0)
    for row in rectangles:
        x0,y0,x1,y1=map(F,row["rectangle"])
        density=F(row["mass"])/(8*(x1-x0)*(y1-y0))
        for xa,xb in ((x0,x1),(L-x1,L-x0)):
            for ya,yb in ((y0,y1),(L-y1,L-y0)):
                capture+=density*(overlap(xa,xb,cx)*overlap(ya,yb,cy)
                                   +overlap(ya,yb,cx)*overlap(xa,xb,cy))
    return capture


def audit(receipts):
    source = ROOT / "evidence/Hosono_n108.json.gz"
    candidate_file = ROOT / "evidence/n108_measure.json.gz"
    check(hashlib.sha256(gzip.decompress(source.read_bytes())).hexdigest()==SOURCE_SHA,
          "Unexpected source certificate")
    with gzip.open(candidate_file, "rt") as f:
        candidate = json.load(f)
    L, B, D = F(candidate["L"]), F(candidate["B"]), F(candidate["proof_net"]["step"])
    last = candidate["proof_net"]["last"]
    check((L,B,D,last)==(F("10.63"),F("0.99896"), F(83,80000),400), "Incorrect grid")
    check(candidate == make(source, L, B, D, last), "Candidate differs from the specified rescaling")
    check(candidate["n"] == 108 and candidate["points"] == [], "Unexpected measure format")
    total = F(0)
    for row in candidate["rectangles"]:
        x0,y0,x1,y1 = map(F,row["rectangle"])
        mass = F(row["mass"])
        check(0<=x0<x1<=L and 0<=y0<y1<=L and mass>0,"Invalid rectangle or mass")
        total += mass
    check(len(candidate["rectangles"])==823 and total==F(10799999,100000) and total<108,
          "Incorrect measure mass")
    files=sorted(receipts.glob("*.jsonl.gz")) if receipts.is_dir() else [receipts]
    check(bool(files), "Missing direction receipts")
    compressed=candidate_file.read_bytes()
    expected_digests={hashlib.sha256(data).hexdigest() for data in (compressed,gzip.decompress(compressed))}
    all_rows=[]
    all_nodes=0
    for receipt_file in files:
        opener=gzip.open if receipt_file.suffix==".gz" else open
        with opener(receipt_file,"rt") as f:
            rows=[json.loads(line) for line in f if line.strip()]
        summary=rows.pop()
        expected_status = "VERIFIED" if len(rows)==last+1 else "PARTIAL"
        check(summary["kind"]=="sqverify-fast-summary/v1" and summary["status"]==expected_status,
              "A native run had a refusal or an unexpected completion status")
        check(summary["directions"]==len(rows) and summary["refused_directions"]==[]
              and summary["fault_injected_at_box"] is None and F(summary["threshold"])==1,"Incomplete or faulted run")
        check(summary["build"]["source_sha256"]==VERIFIER_SHA,"Unexpected verifier source")
        premises=summary["premises"]
        check(premises["input_sha256"] in expected_digests,"Input digest mismatch")
        for k,expected in (("n",108),("L",L),("B",B),("D",D),("angle_count",last+1),
                           ("mass_exact",total),("source_rectangles",823),("expanded_segments",0),
                           ("expanded_points",0)):
            check(F(premises[k])==expected,f"Receipt disagrees on {k}")
        check(premises["format"]=="M" and premises["centre_domain"]=="per-bin","Wrong domain")
        all_rows.extend(rows)
        all_nodes+=summary["nodes"]
    lines=all_rows
    check(len(lines)==last+1 and {r["r"] for r in lines}==set(range(last+1)),
          "Incomplete list of directions")
    for row in lines:
        check(row['verdict']=='verified' and F(row['threshold'])==1 and
              F(str(row['min_certified_lower_bound']))>=1,"Unverified direction")
    axis_row = next(r for r in lines if r["r"]==0)
    capture = axis_capture(candidate["rectangles"],L,B,tuple(map(F,axis_row["argmin"])))
    check(capture>=F(str(axis_row["min_certified_lower_bound"])) and capture*F(99,100)<1,
          "Independent axis integration or 99 percent mass control failed")
    t_end = last*D
    check(t_end*t_end+2*t_end>1 and t_end<=F(1,2),"Net misses the diagonal")
    z = D/2
    u = B*(1+2*z-z*z)/(1+z*z)
    h = F(707107,1000000)
    check(0<u<1 and 1-2*z-z*z>0 and 2*h*h>1,"Invalid containment constants")
    S = (L-2*h)/u+2*h
    check(u*S+2*h*(1-u)==L and S==F(1700799526134255846599,159999384348528500000),
          "Incorrect rational bound")
    print(f"PASS. {len(lines)} directions verified, {all_nodes:,} branch-and-bound nodes.")
    print(f"Independent axis integration = {float(capture):.12f}. Scaling all masses by 99/100 gives {float(capture*F(99,100)):.12f}, below 1.")
    print(f"Mass {total} in {len(candidate['rectangles'])} rectangle orbits. Base side {L}.")
    with localcontext() as ctx:
        ctx.prec=60
        print(f"Lower bound for 108 and 109 = {S} = {Decimal(S.numerator)/Decimal(S.denominator)}...")


if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('receipt',nargs='?',type=Path,default=ROOT/'evidence/direction_runs')
    audit(p.parse_args().receipt)
