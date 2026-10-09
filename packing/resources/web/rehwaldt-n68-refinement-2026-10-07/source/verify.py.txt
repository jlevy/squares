#!/usr/bin/env python3
"""Standard-library-only audit of a single exact certificate and record gap.

Uses independently written vertex/edge-normal polygon SAT, not the search or
repair code. Fraction computations have no tolerance. File SHA-256 binds the
report to the full rational coordinates. Touching is allowed, overlap is not.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


def verify(data, expected_n, old_side=None):
    assert data['schema']=='packing-n/exact-v1'
    assert data['n']==expected_n==len(data['squares'])
    L=F(data['container_side']); assert L>0
    polys=[]
    for square in data['squares']:
        x,y,t=(F(square[k]) for k in ('x','y','t'))
        c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
        p=[(x+(a*c-b*s)/2,y+(a*s+b*c)/2) for a,b in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        edges=[(p[(k+1)%4][0]-p[k][0],p[(k+1)%4][1]-p[k][1]) for k in range(4)]
        assert all(ex*ex+ey*ey==1 for ex,ey in edges)
        assert edges[0][0]*edges[1][0]+edges[0][1]*edges[1][1]==0
        polys.append(p)
    wall=min(L/2-abs(z) for p in polys for v in p for z in v)
    gap_min=None;witnesses=[]
    for i,p in enumerate(polys):
        for j in range(i):
            q=polys[j];gaps=[]
            for owner,r in ((i,p),(j,q)):
                for k in (0,1):
                    ex=r[k+1][0]-r[k][0];ey=r[k+1][1]-r[k][1]
                    normal=(-ey,ex)
                    a=[x*normal[0]+y*normal[1] for x,y in p]
                    b=[x*normal[0]+y*normal[1] for x,y in q]
                    gaps.append((max(min(a)-max(b),min(b)-max(a)),owner,k))
            best=max(gaps);g=best[0]
            gap_min=g if gap_min is None else min(g,gap_min)
            witnesses.append((i,j,best[1],best[2],str(g)))
    valid=wall>=0 and (gap_min is None or gap_min>=0)
    result=dict(valid_exact=valid,n=expected_n,unit_sides_and_right_angles_exact=True,
                pairs_checked=len(witnesses),minimum_wall_gap=str(wall),minimum_pair_gap=str(gap_min),
                container_side=str(L),method='Independent polygon-edge Fraction SAT; zero tolerance',
                witness_digest=hashlib.sha256(json.dumps(witnesses,separators=(',',':')).encode()).hexdigest())
    if old_side is not None:
        R=F(old_side);delta=R-L
        result.update(reference_side=str(R),improvement_exact=str(delta),strict_improvement=valid and delta>0,
                      improvement_float=float(delta))
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('packing',type=Path)
    ap.add_argument('--n',type=int,required=True);ap.add_argument('--reference-side');ap.add_argument('--output',type=Path)
    args=ap.parse_args();data=json.loads(args.packing.read_text())
    report=verify(data,args.n,args.reference_side)
    report['certificate_sha256']=hashlib.sha256(args.packing.read_bytes()).hexdigest()
    rendered=json.dumps(report,indent=2)+'\n';print(rendered)
    if args.output:args.output.write_text(rendered)
    return 0 if report['valid_exact'] and report.get('strict_improvement',True) else 1


if __name__=='__main__':raise SystemExit(main())
