"""精确多边形对照及 IEEE 取整测试。\nExact polygon comparisons and IEEE rounding tests."""
from pathlib import Path
from fractions import Fraction as Q
import argparse,hashlib,json,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'verifier'))
from exact import enclose,sha,FLAGS,B
from oracle import cs, area, capture
import random,itertools

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 out=args.output;out.mkdir(parents=True,exist_ok=False)
 p=ROOT/'tests/kernel_harness.cpp';exe=out/'kernel-oracle'
 cmd=['g++',*FLAGS,'-I',str(ROOT/'verifier'),str(p),'-o',str(exe)]
 z=subprocess.run(cmd,capture_output=True);assert z.returncode==0,z.stderr
 seed=40004261010;rng=random.Random(seed);cases=[];text=['160']
 L=Q(67,10)
 for j in range(160):
  t0=Q(rng.randrange(1,400001),10**6);dt=Q(rng.choice([0,1,10,100,500,2000]),10**6);t1=min(Q(83,200),t0+dt)
  if j<16:t0=Q(1+j,10**6);t1=t0+Q(1,10**6)
  u=Q(rng.randrange(2,30),32);v=Q(rng.randrange(2,30),32);du=Q(1,rng.choice([32,64,1024,2**20]));dv=Q(1,rng.choice([32,64,1024,2**20]));
  c,s=cs((t0+t1)/2);E=L/2-B*(c+s)/2;cx=L/2+u*E;cy=L/2+v*E;rs=[]
  for k in range(8):
   dx=Q(rng.randrange(-700,701),1000);dy=Q(rng.randrange(-700,701),1000);a=cx+dx;b=cy+dy
   w=Q(rng.choice([1,10,100,500]),rng.choice([1000,10**6]));h=Q(rng.choice([1,10,100,500]),rng.choice([1000,10**6]));rho=Q(rng.randrange(1,1000),7)
   rs.append((a,b,a+w,b+h,rho))
  if j%3==0:rs[0]=(Q(0),Q(0),L,L,Q(2))
  cases.append((t0,t1,u,v,du,dv,rs))
  text += [enclose(L),enclose(B),enclose(t0).split()[0]+' '+enclose(t1).split()[1],f'{float(u)} {float(v)} {float(du)} {float(dv)} {len(rs)}']
  text += [' '.join(enclose(x) for x in row) for row in rs]
 st=time.monotonic();z=subprocess.run([str(exe)],input='\n'.join(text)+'\n',capture_output=True,text=True);assert z.returncode==0,z.stderr
 results=[json.loads(line) for line in z.stdout.splitlines()];assert len(results)==len(cases)
 checked=0;area_checks=0;cls_inside=cls_outside=0
 for i,(t0,t1,u,v,du,dv,rs) in enumerate(cases):
  result=results[i];assert result['case']==i;cls_inside+=result['inside'];cls_outside+=result['outside']
  for t in set([t0,t1,(t0+t1)/2]):
   c,s=cs(t);E=L/2-B*(c+s)/2;cx=L/2+u*E;cy=L/2+v*E
   for k,row in enumerate(rs):
    exact=area(row[:4],cx,cy,t,B);assert Q(result['areas'][k])<=exact,(i,k,'area');area_checks+=1
   exact=capture(rs,cx,cy,t,B);assert Q(result['center'])<=exact,(i,'center')
   for a,b in itertools.product((u-du,u,u+du),(v-dv,v,v+dv)):
    val=capture(rs,L/2+a*E,L/2+b*E,t,B);assert Q(result['lower'])<=val,(i,'box',a,b);checked+=1
 receipt={'status':'PASSED_FINITE_ORACLE_TESTS','cases':len(cases),'exact_pose_checks':checked,'exact_area_checks':area_checks,'classified_inside':cls_inside,'classified_outside':cls_outside,'seed':seed,'seconds':time.monotonic()-st,'scope':'Finite regression only; continuous coverage uses interval proof, not these samples','kernel_sha256':sha(ROOT/'verifier/continuous_pose.cpp'),'driver_sha256':sha(Path(__file__)),'oracle_sha256':sha(ROOT/'tests/oracle.py'),'compile_flags':FLAGS,'compile_exit':0,'run_exit':0,'stdout_sha256':hashlib.sha256(z.stdout.encode()).hexdigest()}
 (out/'oracle.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':
 if not __debug__:raise RuntimeError('PYTHON_OPTIMIZATION_FORBIDDEN')
 main()
