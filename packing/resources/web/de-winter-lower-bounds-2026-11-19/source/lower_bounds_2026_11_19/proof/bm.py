from pathlib import Path
from fractions import Fraction as Q
import json,gzip,sys,subprocess,math,time,os,argparse,concurrent.futures,hashlib
root=Path(__file__).resolve().parent
G=2**30;DS=2**32;U=2**24;M=U**2
fl=math.floor;ce=math.ceil
def rows(meas):
 L=Q(meas['L']);acc={}
 assert not meas['points']
 for row in meas['rectangles']:
  x,y,X,Y=map(Q,row['rectangle']);wt=Q(row['mass'])/8
  assert 0<=x<X<=L and 0<=y<Y<=L and wt>=0
  for a,b,c,d in [(x,y,X,Y),(y,x,Y,X)]:
   for l,h in [(a,c),(L-c,L-a)]:
    for j,k in [(b,d),(L-d,L-b)]:
     g=l,j,h,k;acc[g]=acc.get(g,Q(0))+wt
 assert sum(acc.values())==Q(meas['total_mass'])<meas['n']
 for (x,y,X,Y),w in acc.items():
  den=w/((X-x)*(Y-y));r=(ce(x*G),ce(y*G),fl(X*G),fl(Y*G),fl(x*G),fl(y*G),ce(X*G),ce(Y*G),fl(den*DS),fl(w*M))
  assert 0<=r[-2]<2**63 and (r[6]-r[4])*(r[7]-r[5])*2*r[-2]<2**126
  yield r
def worker(r):
 T=r*delta;a,b=T.numerator,T.denominator;C=b*b-a*a;H=2*a*b;E=a*a+b*b
 xx=max(Q(0),T-delta/2);v=(1+2*xx-xx**2)/(2*(1+xx**2));lo=fl(G*L/2);hi=ce(G*(L-v))
 t=fl(E*G*B/2);rep=[C,H,E,t//E,t%E,lo,lo,hi,hi];dpath=od/f'header-{os.getpid()}.txt';dpath.write_text(' '.join(map(str,rep))+'\n')
 t0=time.monotonic();pr=subprocess.run([str(root/'bmcheck'),str(datafile),str(dpath),str(nodecap)],capture_output=True,text=True)
 rs=pr.stdout.strip().split();return dict(r=r,verdict=(rs[0] if rs else f'ERROR_{pr.returncode}'),nodes=int(rs[1]) if len(rs)>1 else 0,leaves=int(rs[2]) if len(rs)>1 else 0,clips=int(rs[3]) if len(rs)>1 else 0,depth=int(rs[4]) if len(rs)>1 else 0,lower_units=int(rs[5]) if len(rs)>1 else 0,seconds=round(time.monotonic()-t0,4),detail=pr.stderr.strip()[:150])
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('file');p.add_argument('spec');p.add_argument('workers',type=int);p.add_argument('--cap',type=int,default=350000);args=p.parse_args();nodecap=args.cap
 f=Path(args.file);d=json.load(gzip.open(f));L=Q(d['L']);B=Q(d['B']);delta=Q(d['proof_net']['step']);last=d['proof_net']['last']
 od=f.parent/'independent';od.mkdir(exist_ok=True);datafile=od/'rectangles.txt';rr=list(rows(d));datafile.write_text(str(len(rr))+'\n'+''.join(' '.join(map(str,r))+'\n' for r in rr));raw=f.read_bytes()
 (od/'meta.json').write_text(json.dumps(dict(measure_sha256=hashlib.sha256(raw).hexdigest(),rects_sha256=hashlib.sha256(datafile.read_bytes()).hexdigest(),source_sha256=hashlib.sha256((root/'bmcheck.cpp').read_bytes()).hexdigest(),G=G,DS=DS,M=M,rectangles=len(rr)),indent=1))
 log=od/'directions.jsonl';done={j['r']for x in log.read_text().splitlines()for j in[json.loads(x)]if j['verdict']=='PASS'} if log.exists() else set()
 if args.spec=='all':dr=range(last+1)
 elif args.spec=='odd':dr=range(1,last+1,2)
 else:dr=list(map(int,args.spec.split(',')))
 dr=[r for r in dr if r not in done]
 with concurrent.futures.ProcessPoolExecutor(args.workers) as ex,open(log,'a',buffering=1) as out:
  for x in concurrent.futures.as_completed([ex.submit(worker,r) for r in dr]):out.write(json.dumps(x.result())+'\n')
