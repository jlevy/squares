"""Independent rational unit-square packing certification via separating axes.

Input JSON: side (rational string), squares [{center:[x,y],basis:[c,s]}].
All numbers interpreted exactly; basis vectors must have unit squared norm.
"""
from fractions import Fraction as F
from itertools import combinations
import json,sys,math

def certify(q):
 if q.get('n',len(q['squares']))!=len(q['squares']):raise ValueError('wrongcount')
 S=F(str(q['side']));a=[];wall_min=S;pair_min=S
 for k,p in enumerate(q['squares']):
  x,y=map(lambda z:F(str(z)),p['center']);c,s=map(lambda z:F(str(z)),p['basis'])
  if c*c+s*s!=1:raise ValueError(f'nonunit basis at{k}')
  h=(abs(c)+abs(s))/2;g=min(x-h,y-h,S-x-h,S-y-h)
  if g<0:raise ValueError(f'wall violation{k}')
  wall_min=min(wall_min,g);a.append((x,y,c,s,h))
 for i,j in combinations(range(len(a)),2):
  x,y,c,s,h=a[i];X,Y,C,T,H=a[j];dx=X-x;dy=Y-y
  # Disjoint exact coordinate projections already prove disjoint interiors.
  box_gap=max(abs(dx)-h-H,abs(dy)-h-H)
  if box_gap>=0:
   pair_min=min(pair_min,box_gap);continue
  gaps=[]
  for u,v in [(c,s),(-s,c),(C,T),(-T,C)]:
   rad=(abs(u*c+v*s)+abs(-u*s+v*c)+abs(u*C+v*T)+abs(-u*T+v*C))/2
   gaps.append(abs(u*dx+v*dy)-rad)
  g=max(gaps)
  if g<0:raise ValueError(f'overlap{i},{j}')
  pair_min=min(pair_min,g)
 return {'n':len(a),'side':str(S),'all_pairs_checked':len(a)*(len(a)-1)//2,'wall_margin':str(wall_min),'pair_margin':str(pair_min),'valid':True}

def rationalize(q,safety='0.000000001'):
 # Inflating center distances creates slack without changing unit square sizes.
 scale=1+F(safety);squares=[]
 for x,y,angle in q['poses']:
  t=F(format(math.tan(float(angle)/2),'.17g'));c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
  squares.append({'center':[F(format(float(x),'.17g'))*scale,F(format(float(y),'.17g'))*scale],'basis':[c,s]})
 lo=[min(a['center'][d]-(abs(a['basis'][0])+abs(a['basis'][1]))/2 for a in squares) for d in range(2)]
 for a in squares:a['center']=[a['center'][d]-lo[d]+F(safety) for d in range(2)]
 S=max(max(a['center'][d]+(abs(a['basis'][0])+abs(a['basis'][1]))/2 for a in squares) for d in range(2))+F(safety)
 return {'n':len(squares),'side':str(S),'squares':[{'center':list(map(str,a['center'])),'basis':list(map(str,a['basis']))} for a in squares]}
if __name__=='__main__':
 q=json.load(open(sys.argv[1]))
 if 'poses' in q:
  q=rationalize(q);json.dump(q,open(sys.argv[2],'w'),indent=2)
 print(json.dumps(certify(q),indent=2))
