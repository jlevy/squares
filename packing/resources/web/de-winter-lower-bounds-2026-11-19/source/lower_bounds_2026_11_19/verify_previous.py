"""Recompute exact bounds, input hashes and complete interval coverage."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,sys,csv,gzip,argparse,subprocess,math
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'proof'))
import check
def verify(folder,comparison):
 m=check.verify(folder);n=m['n'];side=F(m['side']);anchors=json.loads(comparison.read_text());assert n==anchors['n']
 for r in anchors['protected']:
  prev=F(r['value'])
  if r['kind']=='sqrt':assert side*side>prev
  else:assert side>prev
 source=(HERE/'sources'/anchors['source_file']).read_bytes();assert hashlib.sha256(source).hexdigest()==m['source_sha256'];orig=json.loads(gzip.decompress(source));a,_=check.read_level(folder,m['levels'][0]);S=F(a['L']);L=F(orig['L']);w=m['warp'];scale=F(a['total_mass'])/F(orig['total_mass'])
 for r,z in zip(orig['rectangles'],a['rectangles'],strict=True):
  for t,x in zip(r['rectangle'],z['rectangle'],strict=True):
   v=F(t)/L
   if w>=100:
    original=F(t);k=math.floor(L);fr=L-k;sf=S-k;u=original-math.floor(original);mix=F(w-100,100);yy=math.floor(original)+(u*sf/fr if u<=fr else sf+(u-fr)*(1-sf)/(1-fr));value=(1-mix)*S*v+mix*yy
   else:value=S*v+F(w,1000)*4*v*(1-v)*(2*v-1)
   assert F(x)==value
  assert F(z['mass'])==F(r['mass'])*scale
 assert F(a['total_mass'])==F(m.get('target_total_mass',str(F(n)-F(1,10**6))))<n
 return n,side,m
if __name__=='__main__':
 if not __debug__:raise SystemExit('Run with Python assertions enabled.')
 p=argparse.ArgumentParser();p.add_argument('--n',type=int,help='Replay a single direct lower-bound certificate.');p.add_argument('--replay',action='store_true');p.add_argument('--workers',type=int,default=2);opt=p.parse_args()
 for line in (HERE/'SHA256SUMS').read_text().splitlines():
  dig,name=line.split('  ',1);assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==dig
 rows=list(csv.DictReader((HERE/'lower_bounds.csv').open()));fs=sorted((HERE/'proof').glob('n*/manifest.json'))
 assert len(rows)==len(fs)and {int(r['n'])for r in rows}=={int(f.parent.name[1:])for f in fs}
 if opt.n is not None:
  rows=[r for r in rows if int(r['n'])==opt.n]
  if not rows:raise SystemExit('No direct lower-bound certificate for this count.')
 for r in rows:
  folder=HERE/'proof'/('n'+r['n']);n,side,m=verify(folder,folder/'comparison.json');assert side==F(r['new_exact']);print(f"{n} squares, lower bound {side}, {m['directions']} angle intervals, {m['nodes']:,} center boxes.",flush=True)
  if opt.replay:subprocess.run([sys.executable,HERE/'proof/replay.py',folder,'--workers',str(opt.workers),'--controls'],check=True)

if __name__=='__main__' and opt.n is None and (HERE/'corners/verify.py').exists():
 subprocess.run([sys.executable,HERE/'corners/verify.py'],check=True)

if __name__=='__main__' and opt.n is None and (HERE/'upper/improvements.csv').exists():
 subprocess.run([sys.executable,HERE/'upper/verify.py'],check=True)

if __name__=='__main__' and opt.n in (None,114) and (HERE/'constructions/cases.json').exists():
 subprocess.run([sys.executable,HERE/'constructions/verify.py'],check=True)
 subprocess.run([sys.executable,HERE/'constructions/mixture_rebuild.py'],check=True)
 anchor=HERE/'constructions/strip_n114';verify(anchor,anchor/'comparison.json')

if __name__=='__main__' and (HERE/'constructions/smooth_cases.json').exists():
 subprocess.run([sys.executable,HERE/'constructions/smooth_check.py'],check=True)
