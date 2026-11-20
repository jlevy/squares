from pathlib import Path
import json,gzip,math,sys,subprocess,hashlib,time,csv
from concurrent.futures import ThreadPoolExecutor,as_completed
from fractions import Fraction as F
import os
root=Path(os.environ['SQUAREMATH_SEARCH_OUTPUT']).resolve()
proof=Path(__file__).resolve().parents[2]/'proof'
sys.path.insert(0,str(proof))
import check,bm
sha=lambda x:hashlib.sha256(x).hexdigest()
def dump(p,a):
 p.write_bytes(gzip.compress(a,mtime=0));return sha(p.read_bytes())
def search(n,source,L,K,mode,workers):
 old=proof/f'n{source}'
 if source<0:
  srcfile=root/'mix'/f'{-source}'/'measure.json.gz';srcname=f'mix/{-source}/measure.json.gz'
 else:
  m=json.load(open(old/'manifest.json'));srcfile=old/m['levels'][0]['measure'];srcname=old.name+'/'+m['levels'][0]['measure']
 raw=srcfile.read_bytes();a=json.loads(gzip.decompress(raw));S=F(L);B=F(a['L']);tag=f'{n}-{source}-{L}-{K}-{mode}';folder=root/tag;folder.mkdir(exist_ok=True)
 if (folder/'manifest.json').is_file():return
 target=F(a.get('fixed_mass',str(n-F(1,10**6))));assert 0<target<n;scale=target/F(a['total_mass']);k=int(B)
 def warp(s):
  x=F(s)
  if mode=='phase' and S//1==k and B!=k:
   u=x-int(x);f=B-k;g=S-k
   return str(int(x)+(u*g/f if u<=f else g+(u-f)*(1-g)/(1-f)))
  return str(x*S/B)
 a.update(n=n,L=str(S),total_mass=str(target))
 for p in a['rectangles']:
  p['rectangle']=[warp(c)for c in p['rectangle']];p['mass']=str(F(p['mass'])*scale)
 rect=folder/'grid.txt';rc=list(bm.rows(a));rect.write_bytes(check.input_bytes(rc));rd=sha(rect.read_bytes())
 def level(k):
  return dict(a,B=str(F(1,1)/(1+F(83,200*k)/(1-F(83,200*k)**2/4))-F(1,10**12)),proof_net=dict(last=k,step=str(F(83,200*k))))
 def legal(k,r):
  t=(r-F(1,2))*F(83,200*k);return r>=0 and r<=k and(t<0 or t*t+2*t<1)
 def trial(kr):
  k,r=kr;hdr=check.header(level(k),r,'octagon-gram');p=folder/f'h-{k}-{r}';p.write_text(' '.join(map(str,hdr)));q=subprocess.run([root/'gram',rect,p,'600000'],capture_output=True,text=True);p.unlink();v=q.stdout.split();assert len(v)==6 and v[0]in('UNDECIDED','PASS'),(v,q.stderr)
  return dict(K=k,r=r,header=hdr,verdict=v[0],nodes=int(v[1]),leaves=int(v[2]),clips=int(v[3]),depth=int(v[4]),lower_units=int(v[5]),detail=q.stderr.strip()[:200])
 memo={};log=folder/'checked.jsonl'
 if log.exists():
  for line in log.read_text().splitlines():
   q=json.loads(line);memo[q['K'],q['r']]=q
 def finish(k,r,depth,jobs,picks):
  if not legal(k,r):return
  q=memo.get((k,r))
  if q is None:jobs.append((k,r));return
  if q['verdict']=='PASS':picks.append(q);return
  if depth>=6:raise ValueError('unresolved '+str((k,r)))
  for i in [-1,0,1]:finish(3*k,3*r+i,depth+1,jobs,picks)
 with ThreadPoolExecutor(workers)as pool:
  while True:
   jobs=[];picked=[]
   for r in range(K+1):finish(K,r,0,jobs,picked)
   if not jobs:break
   jobs.sort(key=lambda kr:(-kr[0],min(kr[1],abs(kr[1]-kr[0]),abs(kr[1]-kr[0]//2)),kr[1]))
   for fut in as_completed([pool.submit(trial,kr)for kr in jobs[:2*workers]]):
    q=fut.result();memo[q['K'],q['r']]=q
    with log.open('a')as h:h.write(json.dumps(q)+'\n')
 levels=[]
 for k in sorted({q['K']for q in picked}):
  z=level(k);f=f'k{k}.json.gz';r=f'k{k}_receipts.jsonl.gz';ls=[q for q in picked if q['K']==k];levels.append(dict(K=k,measure=f,receipts=r,rectangles=len(rc),rects_sha256=rd,measure_sha256=dump(folder/f,json.dumps(z,separators=(',',':')).encode()),receipts_sha256=dump(folder/r,b'\n'.join(json.dumps(q,separators=(',',':')).encode()for q in ls))))
 m=dict(n=n,side=str(S),kernel='octagon-gram',native_sha256=sha((proof/'gram.cpp').read_bytes()),wrapper_sha256=sha((proof/'bm.py').read_bytes()),levels=levels,directions=len(picked),nodes=sum(q['nodes']for q in picked),target_total_mass=str(target),source_n=source,source_sha256=sha(raw),source_measure=srcname,mode=mode)
 (folder/'verification.json').write_text(json.dumps(dict(n=n,side=str(S),verified_bins=len(picked),nodes=m['nodes'])));(folder/'manifest.json').write_text(json.dumps(m,indent=1));check.verify(folder);print('verified',tag,m['directions'],m['nodes'],flush=True)
if __name__=='__main__':search(int(sys.argv[1]),int(sys.argv[2]),sys.argv[3],int(sys.argv[4]),sys.argv[5],int(sys.argv[6]))
