#!/usr/bin/env python3
"""Exact rational replay of finite packing bounds (Python standard library).

The geometry follows Evan Daniel's MIT verifier at commit
622cd2e21407700fe8d5ac5943af820725107921 (search/exact/verify_cert.py).
This version accepts closed containers and disjoint interiors by default;
--strict uses his open-container/disjoint-closed-squares contract. It adds a
conservative pair prefilter: centres in non-neighbouring cells of side 2
are more than 2 apart on some coordinate, hence have squared distance > 2.
Their unit-square circumscribed discs are disjoint. No pair that could
overlap is omitted, and all decisions use fractions.Fraction.

Copyright (c) 2026 Evan Daniel; modifications by Francisco Couzo with Codex.
Distributed under the MIT license in BOUND_VERIFIER_LICENSE.txt.
"""
import argparse
from collections import defaultdict
from fractions import Fraction as F
import json
from pathlib import Path


def parse(path):
    rows=[line.split() for line in Path(path).read_text().splitlines()
          if line.strip() and not line.lstrip().startswith('#')]
    if not rows or len(rows[0])!=2:raise ValueError('expected n S header')
    n,S=int(rows[0][0]),F(rows[0][1])
    if n<1 or S<=0 or len(rows)!=n+1:raise ValueError('count/side mismatch')
    squares=[]
    for row in rows[1:]:
        if len(row)!=3:raise ValueError('expected x y t')
        x,y,t=map(F,row);d=1+t*t
        squares.append((x,y,(1-t*t)/d,2*t/d))
    return n,S,squares


def candidate_pairs(squares):
    cells=defaultdict(list)
    for j,(x,y,c,s) in enumerate(squares):
        cell=(x//2,y//2)
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                for i in cells[(cell[0]+dx,cell[1]+dy)]:yield i,j
        cells[cell].append(j)


def verify(n,S,squares):
    if n!=len(squares):raise ValueError('count mismatch')
    half=F(1,2);wall=None;pair=None;near=0;tested=0
    for x,y,c,s in squares:
        if c*c+s*s!=1:raise ValueError('rotation is not orthonormal')
        extent=half*(abs(c)+abs(s))
        margin=min(x-extent,S-x-extent,y-extent,S-y-extent)
        if wall is None or margin<wall:wall=margin
    for i,j in candidate_pairs(squares):
        tested+=1
        xi,yi,ci,si=squares[i];xj,yj,cj,sj=squares[j]
        dx,dy=xj-xi,yj-yi
        if dx*dx+dy*dy>2:continue
        near+=1;separation=None
        for nx,ny in ((ci,si),(-si,ci),(cj,sj),(-sj,cj)):
            hi=half*(abs(nx*ci+ny*si)+abs(-nx*si+ny*ci))
            hj=half*(abs(nx*cj+ny*sj)+abs(-nx*sj+ny*cj))
            margin=abs(nx*dx+ny*dy)-hi-hj
            if separation is None or margin>separation:separation=margin
        if pair is None or separation<pair:pair=separation
    return {'n':n,'side':str(S),'valid':wall>=0 and (pair is None or pair>=0),
            'strict_valid':wall>0 and (pair is None or pair>0),
            'wall_margin_sign':(wall>0)-(wall<0),
            'pair_margin_sign':None if pair is None else (pair>0)-(pair<0),
            'candidate_pairs':tested,'near_pairs':near}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificates',nargs='+',type=Path)
    parser.add_argument('--strict',action='store_true')
    args=parser.parse_args();ok=True
    for path in args.certificates:
        result=verify(*parse(path));result['certificate']=str(path)
        result['accepted']=result['strict_valid'] if args.strict else result['valid']
        ok=ok and result['accepted'];print(json.dumps(result))
    raise SystemExit(0 if ok else 1)


if __name__=='__main__':main()
