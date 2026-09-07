#!/usr/bin/env python3
"""Exact rational-interval certificates for the uploaded Trump D4 support.

Standard library only. This checks seven positive-area necessary depth rows,
whose rational combination bounds the complete fixed-support a.e. packing LP
by 11. It also refutes the uploaded 56/5 weight vector with a depth-7/5 box.
The geometry is transcribed from file 09, with orbit order from file 11.
This is NOT a verifier of global optimality for eleven squares.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
import json
import sys
from typing import Union

Scalar = Union[int, F]
@dataclass(frozen=True)
class I:
    lo: F
    hi: F
    def __init__(self, lo: Scalar, hi: Scalar | None = None):
        object.__setattr__(self, 'lo', F(lo))
        object.__setattr__(self, 'hi', F(lo if hi is None else hi))
        if self.lo > self.hi: raise ValueError('reversed interval')
    def __add__(self, other):
        o = as_i(other); return I(self.lo+o.lo, self.hi+o.hi)
    __radd__=__add__
    def __neg__(self): return I(-self.hi,-self.lo)
    def __sub__(self, other): return self + (-as_i(other))
    def __rsub__(self, other): return as_i(other) + (-self)
    def __mul__(self, other):
        o=as_i(other); p=[self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi]
        return I(min(p),max(p))
    __rmul__=__mul__
    def __truediv__(self, other):
        o=as_i(other)
        if o.lo<=0<=o.hi: raise ValueError('division by zero-containing interval')
        return self*I(1/o.hi,1/o.lo)
    def __rtruediv__(self, other): return as_i(other)/self

def as_i(x): return x if isinstance(x,I) else I(x)
def poly(coeff,x):
    v=0
    for a in coeff:v=v*x+a
    return v
P=(5,-10,-2,14,12,-6,2,2,-1)
DP=(40,-70,-12,70,48,-18,4,2)

def root_interval():
    a,b=F(36,100),F(37,100)
    if not poly(P,a)<0<poly(P,b):raise ValueError('root existence')
    # A separate interval cover proves strict monotonicity on the whole bracket.
    for j in range(100):
        x=I(a+(b-a)*j/100,a+(b-a)*(j+1)/100)
        if poly(DP,x).lo<=0:raise ValueError('root uniqueness')
    for _ in range(80):
        m=(a+b)/2
        if poly(P,m)<0:a=m
        else:b=m
    return I(a,b)

def geometry():
    u=root_interval(); c=(1-u*u)/(1+u*u); s=2*u/(1+u*u)
    L=(6*u+4)/(1+2*u-u*u)
    r=1-(L-3)*c; a=((1+r)*c-1)/s; v=c-s
    b=(L-1)/s-r-(3+a)*c/s; x=1+2/c-(L-2)*s/c
    def axis(x,y):
        return [(as_i(x)+dx,as_i(y)+dy) for dx,dy in ((0,0),(1,0),(1,1),(0,1))]
    def tilt(x,y):
        return [(1+c*(x+dx)-s*(y+dy-r),1+s*(x+dx)+c*(y+dy-r)) for dx,dy in ((0,0),(1,0),(1,1),(0,1))]
    original=[axis(0,0),axis(L-1,0),axis(x,L-1),axis(0,L-1),axis(1,L-1),axis(0,L-2),tilt(0,0),tilt(a,-1),tilt(1,v),tilt(a+1,v-1),tilt(a+2,-b)]
    seeds=(0,2,4,7,10,8,6,9); out=[]
    for orbit,k in enumerate(seeds):
        for reflect in range(1 if orbit==0 else 2):
            p=original[k]
            if reflect:p=[(L-x,y) for x,y in p]
            for rot in range(4):
                out.append((orbit,k,reflect,rot,p))
                p=[(L-y,x) for x,y in p]
    # Distinct centers suffice here to certify all 60 geometric placements distinct.
    # Fail explicitly if this sufficient distinctness test is ever inadequate.
    centers=[(sum(v[0] for v in p)/4,sum(v[1] for v in p)/4) for *_,p in out]
    for i in range(len(centers)):
        for j in range(i):
            differences=[centers[i][k]-centers[j][k] for k in (0,1)]
            if not any(d.hi<0 or d.lo>0 for d in differences):
                raise ValueError('distinct centers not proved')
    return u,L,out

ROWS=(
 ((F(961,1000),F(752,1000)), (1,1,0,0,1,0,0,0), F(1)),
 ((F(922,1000),F(922,1000)), (1,2,0,0,0,0,0,0), F(3)),
 ((F(2621,1000),F(3017,1000)), (0,1,1,0,1,0,2,2), F(1)),
 ((F(1887,1000),F(2893,1000)), (0,0,2,2,1,0,0,1), F(1)),
 ((F(1939,1000),F(3154,1000)), (0,0,2,2,2,0,0,0), F(5,2)),
 ((F(2025,1000),F(1308,1000)), (0,0,0,1,0,2,3,2), F(1)),
 ((F(1939,1000),F(1489,1000)), (0,0,0,0,0,4,2,2), F(3,2)),
)
SIZES=(4,8,8,8,8,8,8,8)
WEIGHTS=tuple(map(F,('1','0','2/5','1/10','0','1/10','3/10','0')))

def incidence_on_box(point,radius,L,squares):
    if radius<=0:raise ValueError('radius must be positive')
    box=[I(x-radius,x+radius) for x in point]
    if not all(x.lo>0 and x.hi<L.lo for x in box):raise ValueError('box containment')
    counts=[0]*8; members=[]; certified_margins=[]
    for orbit,k,f,r,p in squares:
        gaps=[]
        for j in range(4):
            a,b=p[j],p[(j+1)%4]
            g=((b[0]-a[0])*(box[1]-a[1])-(b[1]-a[1])*(box[0]-a[0]))*((-1)**f)
            gaps.append(g)
        if all(g.lo>0 for g in gaps):
            counts[orbit]+=1; members.append((k,f,r)); certified_margins.append(min(g.lo for g in gaps))
        elif any(g.hi<0 for g in gaps):
            certified_margins.append(max(-g.hi for g in gaps if g.hi<0))
        else:raise ValueError(f'undecided membership for {(k,f,r)}')
    return tuple(counts),members,min(certified_margins)

def check():
    u,L,squares=geometry(); radius=F(1,100000)
    records=[]
    for point,expected,lam in ROWS:
        if lam<0:raise ValueError('negative upper-bound multiplier')
        row,ids,margin=incidence_on_box(point,radius,L,squares)
        if row!=expected:raise ValueError(f'row mismatch: {point}: {row} != {expected}')
        records.append({'point':list(map(str,point)), 'radius':str(radius),'counts':row,'multiplier':str(lam),'margin_positive':margin>0})
    combined=tuple(sum(lam*row[k] for _,row,lam in ROWS) for k in range(8))
    total=sum(lam for _,_,lam in ROWS)
    if combined!=SIZES or total!=11:raise ValueError('upper certificate arithmetic')
    point=(F(97,50),F(71,50))
    row,ids,margin=incidence_on_box(point,radius,L,squares)
    depth=sum(a*b for a,b in zip(row,WEIGHTS))
    if depth!=F(7,5):raise ValueError(f'expected depth 7/5, got {depth}')
    report={'verdict':'EXACT NECESSARY-ROW UPPER BOUND 11; CANDIDATE REFUTED',
     'scope':'Only the D4 support of the supplied Trump construction. Not a global square-packing bound.',
     'method':'Standard-library rational interval arithmetic; no float decisions, no LP solver, no exhaustive arrangement claim.',
     'root_bracket':list(map(str,(u.lo,u.hi))), 'distinct_placements':len(squares),
     'rows':records,'combined_coefficients':list(map(str,combined)),'upper_bound':str(total),
     'candidate_refutation':{'point':list(map(str,point)),'radius':str(radius),'counts':row,'depth':str(depth),'members':ids,'margin_positive':margin>0}}
    return report

if __name__=='__main__':
    try:
        result=check()
        print(json.dumps(result,indent=2))
    except (ValueError,ZeroDivisionError) as e:
        print(f'REFUSED: {e}',file=sys.stderr);sys.exit(1)
