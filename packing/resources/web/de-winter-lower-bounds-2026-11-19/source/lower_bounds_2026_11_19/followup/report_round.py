"""Compare certified claims against the preceding, immutable 40-count report."""
from fractions import Fraction as F
from pathlib import Path
import csv,hashlib
def rows(p):
 with p.open() as f:return list(csv.DictReader(f))
def derive(new,old,history):
 prev={int(r['n']):F(r['exact'])for r in old}
 assert set(prev)<={int(r['n'])for r in new}
 out=[]
 for r in new:
  n=int(r['n']);lower=max([history.prior(n)[0]]+[v for k,v in prev.items()if k<=n]);side=F(r['exact'])
  assert side>=lower and (n not in prev or prev[n]<=side)
  if side>lower:
   out.append(dict(n=n,previous_exact=str(lower),previous_approx=f'{float(lower):.12f}',new_exact=str(side),new_side=r['side'],gain_exact=str(side-lower),gain_approx=f'{float(side-lower):.12g}',status='stronger bound'if n in prev else 'new square count',method=r['method']))
 return sorted(out,key=lambda z:z['n'])
def verify(h,history):
 baseline=h/'comparisons/preceding_40.csv'
 assert hashlib.sha256(baseline.read_bytes()).hexdigest()==BASE_HASH
 data=derive(rows(h/'best_by_count.csv'),rows(baseline),history)
 table=rows(h/'since_previous_report.csv')
 assert [{k:str(v)for k,v in r.items()}for r in data]==table
 return data
BASE_HASH='7a81ac49bc4ae68f94956a6a22cb19bd5f47c4a6516048c63e220236f5f48617'
