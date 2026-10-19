"""Independent exact validator using explicit vertices and interval projections."""
import json,sys
from fractions import Fraction as Q
from itertools import combinations

def check(q):
 L=Q(q['side']);polys=[];boxes=[]
 if q.get('n',len(q['squares']))!=len(q['squares']):raise ValueError('wrongcount')
 for k,s in enumerate(q['squares']):
  x,y=map(Q,s['center']);c,t=map(Q,s['basis']);u=(c/2,t/2);v=(-t/2,c/2)
  P=[(x+u[0]+v[0],y+u[1]+v[1]),(x-u[0]+v[0],y-u[1]+v[1]),(x-u[0]-v[0],y-u[1]-v[1]),(x+u[0]-v[0],y+u[1]-v[1])]
  E=[(P[(i+1)%4][0]-P[i][0],P[(i+1)%4][1]-P[i][1])for i in range(4)]
  for i,e in enumerate(E):
   f=E[(i+1)%4]
   if e[0]*e[0]+e[1]*e[1]!=1 or e[0]*f[0]+e[1]*f[1]!=0:raise ValueError(('nonsquare',k))
  if any(a<0 or b<0 or a>L or b>L for a,b in P):raise ValueError(('wall',k))
  polys.append(P);boxes.append((min(a for a,b in P),max(a for a,b in P),min(b for a,b in P),max(b for a,b in P)))
 count=0;box_count=0
 for i,j in combinations(range(len(polys)),2):
  count+=1;a=boxes[i];b=boxes[j]
  if a[1]<=b[0] or b[1]<=a[0] or a[3]<=b[2] or b[3]<=a[2]:box_count+=1;continue
  P,T=polys[i],polys[j];separated=False
  for V in [P,T]:
   for e in range(4):
    dx=V[(e+1)%4][0]-V[e][0];dy=V[(e+1)%4][1]-V[e][1];axis=(-dy,dx)
    A=[x*axis[0]+y*axis[1]for x,y in P];B=[x*axis[0]+y*axis[1]for x,y in T]
    if max(A)<=min(B) or max(B)<=min(A):separated=True;break
   if separated:break
  if not separated:raise ValueError(('overlap',i,j))
 return {'valid':True,'n':len(polys),'side':str(L),'all_pairs_checked':count,'pairs_separated_by_boxes':box_count,'validator':'exact vertex projections, independent implementation'}
if __name__=='__main__':print(json.dumps(check(json.load(open(sys.argv[1]))),indent=2))
