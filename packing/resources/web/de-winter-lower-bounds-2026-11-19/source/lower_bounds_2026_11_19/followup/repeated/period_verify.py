"""Exact period checks and mass of a repeated central strip."""
from fractions import Fraction as F
from collections import defaultdict
def inspect(z,repetitions):
 S=F(z['L']);start=(S-repetitions)/2;unit=(S-1)/2;M=F(z['total_mass']);bx=F(0);c=F(0)
 assert repetitions>=3 and start>=0
 maps=[[defaultdict(F)for i in range(repetitions)]for ax in (0,1)]
 def frac(x,X):return max(F(0),min(X,unit+1)-max(x,unit))/(X-x)
 for row in z['rectangles']:
  x,y,X,Y=map(F,row['rectangle']);m=F(row['mass']);den=m/((X-x)*(Y-y));fx=frac(x,X);fy=frac(y,Y);bx+=m*(fx+fy)/2;c+=m*fx*fy
  for axis,(l,h,v,w)in enumerate(((x,X,y,Y),(y,Y,x,X))):
   for i in range(repetitions):
    left=start+i;right=left+1;low=max(l,left);high=min(h,right)
    if low>=high:continue
    # Signed corner events determine the piecewise-constant rectangular density almost everywhere.
    t=maps[axis][i];a=low-left;b=high-left
    t[a,v]+=den;t[a,w]-=den;t[b,v]-=den;t[b,w]+=den
 for parts in maps:
  first={k:v for k,v in parts[0].items()if v}
  for t in parts[1:]:assert {k:v for k,v in t.items()if v}==first,'The chosen strip does not repeat exactly.'
 return M,bx,c
def verify(z,p):
 M,b,c=inspect(z,p['periods']);S=F(z['L'])
 assert all(F(p[k])==v for k,v in [('base_mass',M),('strip_mass',b),('cell_mass',c)])
 for r in p['claims']:
  d=r['offset'];assert isinstance(d,int) and p['periods']+d>=2
  mass=M+2*d*b+d*d*c
  assert mass==F(r['mass'])<r['n'] and int(mass)+1==r['n'] and F(r['side'])==S+d>F(r['previous_upper_endpoint'])
 return len(p['claims'])
