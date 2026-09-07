#!/usr/bin/env python3
"""Known-answer and mutation checks for the review's fixed-support certificate."""
from fractions import Fraction as F
import json
import check_support_ceiling as c

def must_refuse(fn):
    try:
        fn()
    except ValueError:
        return
    raise RuntimeError('mutation was not refused')

def main():
    u,L,squares=c.geometry()
    checks=[]
    # A second membership assembly: project the entire test box onto each edge
    # direction and compare with a +/-1/2 center-based support interval. The
    # root enclosure and corner formulas are shared with the main checker.
    for point,row,lam in c.ROWS:
        counts=[0]*8
        box=[c.I(x-F(1,100000),x+F(1,100000)) for x in point]
        for orbit,k,f,r,p in squares:
            center=[sum(v[d] for v in p)/4 for d in (0,1)]
            axes=[(p[j][0]-p[0][0],p[j][1]-p[0][1]) for j in (1,3)]
            projs=[a[0]*(box[0]-center[0])+a[1]*(box[1]-center[1]) for a in axes]
            if all(-F(1,2)<v.lo and v.hi<F(1,2) for v in projs):
                counts[orbit]+=1
            elif any(v.lo>F(1,2) or v.hi<-F(1,2) for v in projs):
                pass
            else:
                raise RuntimeError('projection assembly unresolved')
        if tuple(counts)!=row:raise RuntimeError('projection assembly mismatch')
    checks.append('all seven rows reproduced by center/edge projection assembly')
    # Simple exact square fixtures, with touching boundaries and oversized boxes.
    square=[(c.I(0),c.I(0)),(c.I(1),c.I(0)),(c.I(1),c.I(1)),(c.I(0),c.I(1))]
    fixture=[(0,0,0,0,square)]
    row,_,_=c.incidence_on_box((F(1,2),F(1,2)),F(1,10),c.I(3),fixture)
    if row[0]!=1:raise RuntimeError('interior fixture')
    row,_,_=c.incidence_on_box((F(3,2),F(1,2)),F(1,10),c.I(3),fixture)
    if row[0]!=0:raise RuntimeError('exterior fixture')
    must_refuse(lambda:c.incidence_on_box((F(1),F(1,2)),F(1,100),c.I(3),fixture))
    must_refuse(lambda:c.incidence_on_box((F(1,2),F(1,2)),F(1),c.I(3),fixture))
    checks.extend(['interior and exterior fixtures accepted with correct incidence',
                   'boundary-straddling and out-of-container boxes refused'])
    original=c.ROWS
    try:
        point,row,lam=original[0]
        changed=(row[0]+1,)+row[1:]
        c.ROWS=((point,changed,lam),)+original[1:]
        must_refuse(c.check)
        checks.append('altered incidence row refused')
        c.ROWS=((point,row,lam+1),)+original[1:]
        must_refuse(c.check)
        checks.append('altered multiplier refused')
        c.ROWS=original[:-1]
        must_refuse(c.check)
        checks.append('omitted certificate row refused')
    finally:
        c.ROWS=original
    result=c.check()
    if result['upper_bound']!='11':raise RuntimeError('restored certificate')
    print(json.dumps({'status':'PASS','checks':checks,
      'independence_boundary':'Projection assembly differs; interval arithmetic, root enclosure, and source geometry are shared. This is not an independent external review.'},indent=2))
if __name__=='__main__':main()
