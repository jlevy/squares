from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import csv,json
here=Path(__file__).resolve().parent
def source(name):
 return here.parents[1]/name[5:] if name.startswith('prev/') else here/'inputs'/name
def records(name):
 with source(name).open() as f:return list(csv.DictReader(f))
def data(name):
 with source(name).open() as f:return json.load(f)
reg=data('prior56/attribution/registry_lower_intervals.json')
priv=data('prior56/attribution/strongest_prior_lower.json')
table=data('prev/corners/intervals.json')['intervals']
refs={}
def add(n,v,label):
 n=int(n);refs.setdefault(n,[]).append((F(v),label))
def ceilroot(x):
 t=10**25;a=isqrt(x.numerator*t*t//x.denominator);return F(a if a*a*x.denominator==x.numerator*t*t else a+1,t)
for n in range(1,325):
 for name,r in reg.get(str(n),{}).items():
  if r:add(n,r['upper'],'SquareMath '+name)
 if str(n)in priv:add(n,priv[str(n)],'Earlier strongest enclosure')
 if n>=49:
  k=isqrt(n)
  for j,r in enumerate(table,1):
   a,b=map(F,(r['certified_line']['alpha'],r['certified_line']['beta']));disc=4*a*a+n+4*b-4*a*k
   if disc<0:continue
   R=2*a+ceilroot(disc)
   if R>k+F(r['d0']):add(n,min(R,k+F(r['d1'])),'Original Hosono family '+str(j))
for q in records('prior56/attribution/prior_lower_comparisons.csv'):
 try:add(q['n'],q['exact'],q['source'])
 except ValueError:pass
for q in records('prior56/exact_claims.csv'):
 x=F(q['rational_value_or_radicand']);add(q['n'],ceilroot(x) if q['exact_kind']=='sqrt'else x,'Issue 1039')
for q in records('earlier/results.csv'):
 if q['kind']=='lower':
  try:add(q['n'],q['exact'],'Earlier four-hour search')
  except ValueError:add(q['n'],F(q['bound'])+F(1,10**12),'Earlier four-hour search (rounded outwards)')
for q in records('earlier/companion_comparison.csv'):
 if q['companion_exact']:add(q['n'],q['companion_exact'],'Companion direct certificate')
 elif q['companion_exact_squared']:add(q['n'],ceilroot(F(q['companion_exact_squared'])),'Companion squared certificate')
 elif q['companion_lower_down_12']:add(q['n'],F(q['companion_lower_down_12'])+F(1,10**12),'Companion ceiling')
for q in records('prev/lower_bounds.csv'):add(q['n'],q['new_exact'],'Previous search, standalone proof')
for q in records('prev/corners/bounds.csv'):add(q['n'],q['new_side'],'Previous search, corner modification')
from functools import lru_cache
@lru_cache(None)
def prior(n):return max((v,(s if k==n else s+' via monotonicity from '+str(k)))for k,items in refs.items() if k<=n for v,s in items)
if __name__=='__main__':
 with (here.parent/'best_by_count.csv').open() as f:claims=list(csv.DictReader(f))
 for row in claims:
  value,label=prior(int(row['n']))
  assert value==F(row['previous_exact_upper_endpoint']) and label==row['previous_source'] and value<F(row['exact'])
 print(f'Checked every preceding bound and source for {len(claims)} square counts.')
