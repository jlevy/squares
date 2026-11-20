"""Verify the new bounds, exact comparisons, source geometry and certificates."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from functools import lru_cache
from importlib.util import spec_from_file_location,module_from_spec
import argparse,csv,hashlib,gzip,json,subprocess,sys
here=Path(__file__).resolve().parent;project=here.parent
sys.path.insert(0,str(project/'proof'));import check
def load_module(fn,name):
 s=spec_from_file_location(name,fn);m=module_from_spec(s);s.loader.exec_module(m);return m
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def readz(p):return json.loads(gzip.decompress(p.read_bytes()))
def base(n):
 folder=project/'proof'/f'n{n}';m=json.loads((folder/'manifest.json').read_text());return folder/m['levels'][0]['measure']
def warp(x,B,S,mode):
 k=int(B);a=x*S/B
 if int(S)!=k or B==k:return a
 t=x-int(x);f=B-k;g=S-k;b=int(x)+(t*g/f if t<=f else g+(t-f)*(1-g)/(1-f));return a+(b-a)*F(mode,100)
def group(xy,B):
 x,y,X,Y=xy;d1=min(x,B-X);d2=min(y,B-Y);return (0 if min(d1,d2)<55000000 else 1 if min(d1,d2)<155000000 else 2,max(d1,d2)<160000000,max(X-x,Y-y)>65000000)
@lru_cache(100)
def transported(n,mode,S):
 data=readz(base(n));B=F(data['L']);T=defaultdict(int)
 if mode>=200:
  module=load_module(project/'constructions/mixture_rebuild.py','strip_transform')
  parts=module.component(data,dict(j=int(S)-int(B),word='middle' if mode<210 else 'asym',loc='5/4',warp=mode%2),S)
 else:
  fast=lru_cache(None)(lambda x:warp(F(x),B,S,mode))
  parts=[(tuple(fast(x)for x in r['rectangle']),F(r['mass']))for r in data['rectangles']]
 for xy,w in (parts.items()if mode>=200 else parts):
  key=tuple(round(y*10**8)for y in xy)
  if key[0]<key[2] and key[1]<key[3]:T[key]+=round(w*10**12)
 return T
def verify_recipe(folder):
 z=readz(folder/'measure.json.gz');p=json.loads((folder/'recipe.json').read_text());S=F(p['side']);total=F(z['total_mass'])
 if p.get('kind')=='archived rectangle measure':
  record=here/'comparisons/issue1039_sha256.txt';assert digest(record)=='2659c81ff57758ddcf8ac52c26953b110a8cdbf4cd18030daab9d4ebebb0a0aa'
  hashes={name:sha for l in record.read_text().splitlines() for sha,name in [l.split(None,1)]}
  assert p['archive']=='lower-bounds-56.zip' and hashes[p['source_path']]==p['source_sha256']==digest(folder/'measure.json.gz')
  assert not z['points'] and F(z['L'])==S
  return
 assert (p['coordinate_grid'],p['mass_grid'])==(10**8,10**12)
 combined=defaultdict(F)
 for term in p['components']:
  n,t,u=term['n'],term['warp_percent'],term['units'];assert digest(base(n))==term['source_sha256'] and u>0;T=transported(n,t,S)
  if 'period_group' in term:
   sub=load_module(here/'period_groups.py','period_groups');parts=(sub.uniform_groups(round(S*10**8),term['period_count']) if term.get('uniform_regions') else sub.split_groups(T,round(S*10**8),term['period_count']));T=parts[term['period_group']]
  if 'group'in term:T={k:v for k,v in T.items()if group(k,round(S*10**8))==tuple(term['group'])}
  divisor=sum(T.values());assert divisor>0
  for xy,w in T.items():combined[xy]+=F(w*u,divisor)
 scale=total/sum(combined.values());expected={tuple(F(v,10**8)for v in k):w*scale for k,w in combined.items()}
 assert {tuple(map(F,r['rectangle'])):F(r['mass'])for r in z['rectangles']}==expected
def check_case(row,replay=False,workers=4,folder=None):
 n=int(row['n']);folder=folder or here/'lower'/f'n{n}';m=check.verify(folder);assert n==m['n'] and F(row['exact'])==F(m['side'])>F(row['previous_upper_endpoint'])
 source=(here/m['source_measure'])if m['source_n']<0 else (project/'proof'/m['source_measure']);assert digest(source)==m['source_sha256']
 if m['source_n']<0:verify_recipe(source.parent)
 old=readz(source);a,_=check.read_level(folder,m['levels'][0]);B=F(old['L']);S=F(m['side']);mass=F(m.get('target_total_mass',str(F(n)-F(1,10**6))));assert 0<mass<n and F(a['total_mass'])==mass and not a['points'];factor=mass/F(old['total_mass'])
 for r,v in zip(old['rectangles'],a['rectangles'],strict=True):
  assert F(v['mass'])==F(r['mass'])*factor and tuple(F(x)for x in v['rectangle'])==tuple(warp(F(x),B,S,100 if m['mode']=='phase' else 0)for x in r['rectangle'])
 print(f"{n} squares, lower bound {m['side']}, {m['directions']} angular intervals, {m['nodes']:,} center boxes.",flush=True)
 if replay:subprocess.run([sys.executable,project/'proof/replay.py',folder,'--controls','--workers',str(workers)],check=True)
def verify_best_table():
 rows=list(csv.DictReader((here/'lower_bounds.csv').open()))
 best={}
 def take(n,side,previous):
  if n not in best or side>best[n][0]:best[n]=(side,previous)
 for row in rows:take(int(row['n']),F(row['exact']),F(row['previous_upper_endpoint']))
 for loc in ('inherited.json','repeated/claims.json','envelopes/claims.json','corner_trim/claims.json'):
  file=here/loc
  if file.exists():
   for row in json.loads(file.read_text()):take(row['n'],F(row['side']),F(row['previous_upper_endpoint']))
 table=here/'best_by_count.csv'
 if table.exists():
  summary=list(csv.DictReader(table.open()))
  assert len(summary)==len(best) and len(set(int(r['n'])for r in summary))==len(best)
  history=load_module(here/'comparisons/benchmark.py','history')
  for r in summary:
   side,previous=best[int(r['n'])]
   assert history.prior(int(r['n']))==(previous,r['previous_source'])
   assert F(r['exact'])==F(r['side'])==side and F(r['previous_exact_upper_endpoint'])==previous<side

  audit_round=here/'report_round.py'
  if audit_round.is_file():load_module(audit_round,'round_comparison').verify(here,history)

def main():
 if not __debug__:raise SystemExit('Run with assertions enabled.')
 ap=argparse.ArgumentParser();ap.add_argument('--n',type=int);ap.add_argument('--replay',action='store_true');ap.add_argument('--workers',type=int,default=4);o=ap.parse_args();seen=False
 for line in (project/'SHA256SUMS').read_text().splitlines():
  h,p=line.split('  ',1);assert digest(project/p)==h,p
 verify_best_table()
 rows=list(csv.DictReader((here/'lower_bounds.csv').open()));direct={int(r['n']):r for r in rows}
 primary={(int(r['n']),F(r['exact']))for r in rows}
 for name in ('repeated/claims.json','envelopes/claims.json','corner_trim/claims.json'):
  f=here/name
  if f.exists():primary.update((r['n'],F(r['side']))for r in json.loads(f.read_text()))
 wanted={o.n}
 for r in json.loads((here/'inherited.json').read_text()):
  if o.n is None or r['n']==o.n:
   assert r['source_n']<=r['n'] and (r['source_n'],F(r['side'])) in primary and F(r['side'])>F(r['previous_upper_endpoint'])
   wanted.add(r['source_n']);seen=True
 for row in rows:
  if o.n is None or int(row['n']) in wanted:check_case(row,o.replay,o.workers);seen=True
 period=here/'repeated'
 if (period/'claims.json').exists():
  mod=load_module(period/'period_verify.py','period_check')
  for path in sorted(period.glob('*/family.json')):
   law=json.loads(path.read_text());claims=[r for r in law['claims']if o.n is None or r['n'] in wanted]
   if not claims:continue
   seen=True;anchor=path.parent/'proof';m=json.loads((anchor/'manifest.json').read_text());check_case(dict(n=m['n'],exact=m['side'],previous_upper_endpoint='0'),o.replay,o.workers,anchor)
   z,_=check.read_level(anchor,m['levels'][0]);assert law['side']==m['side'] and law['anchor_n']==m['n'] and law['source_sha256']==m['source_sha256'];mod.verify(z,law)
   for r in claims:print(f"{r['n']} squares, lower bound {r['side']} by repeating the certified central strips.",flush=True)
 env=here/'envelopes'
 if (env/'claims.json').is_file():
  sys.path.insert(0,str(env));mod=load_module(env/'envelope_exact.py','four_regions')
  for path in env.glob('*/claims.json'):
   desc=json.loads(path.read_text());claims=[r for r in desc['claims'] if o.n is None or r['n'] in wanted]
   if not claims:continue
   seen=True
   if desc['previous_anchor']:
    anchor=project/'proof'/f"n{desc['source_n']}";m=check.verify(anchor)
    if o.replay:subprocess.run([sys.executable,project/'proof/replay.py',anchor,'--controls','--workers',str(o.workers)],check=True)
   else:
    anchor=path.parent/'proof';m=json.loads((anchor/'manifest.json').read_text());check_case(dict(n=m['n'],exact=m['side'],previous_upper_endpoint='0'),o.replay,o.workers,anchor)
   assert m['n']==desc['source_n'] and F(m['side'])==F(desc['anchor_side']);z,_=check.read_level(anchor,m['levels'][0]);mod.verify(z,claims)
 for p in sorted((here/'upper').glob('n*/summary.json')):
  q=json.loads(p.read_text())
  if o.n in(None,int(q['n'])):
   if (p.parent/'scaling_bound.json').is_file():load_module(here/'shape_bound.py','scale_checker').verify(p.parent)
   ver=load_module(project/'upper/verify.py','upper_checker');a=ver.case(p.parent);assert a==json.loads((p.parent/'audit.json').read_text());assert a['pairs_per_predicate']==q['pairs'] and F(q['previous_exact'])>F(q['new_exact'])
   print(f"{q['n']} squares, all {q['pairs']:,} pairs checked with three geometric predicates.",flush=True);seen=True
 trim=here/'corner_trim'
 if (trim/'claims.json').exists():
  import types
  context=types.SimpleNamespace(check=check,check_case=check_case,load_module=load_module,project=project)
  checker=load_module(trim/'verify.py','verify_corners')
  for p in trim.glob('*/bounds.json'):
   points=[r['n'] for r in json.loads(p.read_text()) if o.n is None or r['n'] in wanted]
   if points:
    count=checker.verify(p.parent,context,o.replay,o.workers);seen=True
    print('Verified',count,'local angular intervals and periodic bounds for',points,flush=True)
 addon=here/'mass_reserve'
 if (addon/'claims.json').is_file():
  selected=[r for r in json.loads((addon/'claims.json').read_text()) if o.n is None or r['n']==o.n]
  if selected:
   load_module(addon/'verify.py','edge_strip_check').verify(addon)
   print('Verified the edge-strip enlargement for square counts', [r['n'] for r in selected],flush=True);seen=True
 if not seen:raise SystemExit('No matching case in this continuation.')
if __name__=='__main__':main()
