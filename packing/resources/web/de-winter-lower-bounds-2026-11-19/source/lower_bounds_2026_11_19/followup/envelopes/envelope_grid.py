from fractions import Fraction as F
from collections import defaultdict
from functools import lru_cache
from math import ceil,floor
G=10**7
D=10**9
q=lru_cache(50000)(F)
def grid(z):
    S=q(z['L']);N=S*G;assert N.denominator==1
    allr=defaultdict(int)
    for row in z['rectangles']:
        x,y,X,Y=map(q,row['rectangle']);mass=q(row['mass'])
        upper=ceil(D*mass/(8*(X-x)*(Y-y)))
        for l,v,h,w in ((x,y,X,Y),(y,x,Y,X)):
            for a,b in ((l,h),(S-h,S-l)):
                for c,d in ((v,w),(S-w,S-v)):
                    allr[floor(a*G),floor(c*G),ceil(b*G),ceil(d*G)]+=upper
    s=[f'{int(N)} {len(allr)}']
    for coords,u in sorted(allr.items()):s.append(' '.join(str(v)for v in (*coords,u)))
    return ('\n'.join(s)+'\n').encode()
