from collections import defaultdict
from fractions import Fraction as F
from itertools import product

def split_groups(T,side,p):
    A=(side-p*10**8)//2
    B=A+p*10**8
    def cuts(lo,hi):
        for a,b,flag in ((lo,min(A,hi),0),(max(A,lo),min(B,hi),1),(max(B,lo),hi,0)):
            if a<b:yield a,b,flag
    out=[defaultdict(F) for i in range(3)]
    for (x,y,X,Y),w in T.items():
        for (a,b,i),(c,d,j) in product(cuts(x,X),cuts(y,Y)):
            out[i+j][a,c,b,d]+=F(w*(b-a)*(d-c),(X-x)*(Y-y))
    return out

def uniform_groups(side,p):
    """Partition a uniform board into exterior corners, edge bands and interior cells."""
    U=10**8
    a=(side-p*U)//2
    b=a+p*U
    outer={0,a,b,side}
    # Span every central period by one unit. Exterior pieces have width at most one.
    outer.update(range(0,a,U));outer.update(range(a,b+1,U));outer.update(side-i for i in range(0,a,U))
    bounds=sorted(outer);out=[{}, {}, {}]
    for l,h in zip(bounds,bounds[1:]):
        for v,w in zip(bounds,bounds[1:]):
            k=int(a<=l<h<=b)+int(a<=v<w<=b)
            out[k][l,v,h,w]=(h-l)*(w-v)
    return out
