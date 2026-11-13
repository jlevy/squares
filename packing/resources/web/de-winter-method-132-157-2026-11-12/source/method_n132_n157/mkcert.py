"""Build an exact rational certificate from a float packing (S, P[x,y,theta]) and verify it exactly."""
import sys,json,math
from fractions import Fraction as F
from itertools import combinations
import numpy as np
HALF=F(1,2)
def rat(x,D): return F(round(x*D),D)
def corners(q):
    cx,cy,c,s=q
    return [(cx+a*c*HALF-b*s*HALF,cy+a*s*HALF+b*c*HALF) for a,b in ((1,1),(-1,1),(-1,-1),(1,-1))]
def separated(qa,ca,qb,cb):
    for (cx,cy,c,s),other in ((qa,cb),(qb,ca)):
        for ax,ay in ((c,s),(-s,c)):
            centre=cx*ax+cy*ay
            proj=[x*ax+y*ay for x,y in other]
            if min(proj)>=centre+HALF or max(proj)<=centre-HALF: return True
    return False
def build(S,P,eps_exp=None,D=10**20):
    sq=[]
    for x,y,th in P:
        t=rat(math.tan(th/2),D); c=(1-t*t)/(1+t*t); s=2*t/(1+t*t)
        sq.append([rat(x,D),rat(y,D),c,s])
    # shift so that the least corner coordinates are 0 and take the side as the greatest corner coordinate
    cs=[corners(q) for q in sq]
    x0=min(x for c in cs for x,_ in c); y0=min(y for c in cs for _,y in c)
    for q in sq: q[0]-=x0; q[1]-=y0
    if eps_exp is not None:
        e=F(1,10**eps_exp)
        for q in sq: q[0]*=(1+e); q[1]*=(1+e)
    cs=[corners(q) for q in sq]
    x0=min(x for c in cs for x,_ in c); y0=min(y for c in cs for _,y in c)
    for q in sq: q[0]-=x0; q[1]-=y0
    cs=[corners(q) for q in sq]
    side=max(max(x for c in cs for x,_ in c),max(y for c in cs for _,y in c))
    return side,[tuple(q) for q in sq]
def verify(side,sq):
    cs=[corners(q) for q in sq]
    for i,q in enumerate(sq):
        if q[2]**2+q[3]**2!=1: return 'square %d: direction is not a unit vector'%i
        if not all(0<=x<=side and 0<=y<=side for x,y in cs[i]): return 'square %d outside'%i
    for i,j in combinations(range(len(sq)),2):
        dx=sq[i][0]-sq[j][0]; dy=sq[i][1]-sq[j][1]
        if dx*dx+dy*dy>=2: continue
        if not separated(sq[i],cs[i],sq[j],cs[j]): return 'squares %d and %d overlap'%(i,j)
    return None
if __name__=='__main__':
    src,out=sys.argv[1],sys.argv[2]
    d=np.load(src); S=float(d['S']); P=d['P']; n=len(P)
    for eps in (None,13,12,11,10,9):
        side,sq=build(S,P,eps)
        err=verify(side,sq)
        print('eps',eps,'side %.15f'%float(side),'->',err or 'VALID',flush=True)
        if err is None: break
    assert err is None
    json.dump({"n":n,"side":str(side),"square_size":"1","format":"each square: [center_x, center_y, cos, sin] as exact rationals; (cos, sin) is the unit direction of one edge","squares":[[str(v) for v in q] for q in sq]},open(out,'w'),indent=0)
    ds=str(side.numerator*10**30//side.denominator); print('side =',ds[:-30]+'.'+ds[-30:],'(truncated; rounded up at 12 places: %s)'%(str(-(-side.numerator*10**12//side.denominator))))
