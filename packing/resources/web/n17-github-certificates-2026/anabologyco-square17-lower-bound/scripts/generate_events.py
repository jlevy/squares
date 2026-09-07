import csv,numpy as np,time,sys
from math import gcd
atom_path=sys.argv[1] if len(sys.argv)>1 else '/mnt/data/square17_4p5705_candidate/atoms.csv'
out_path=sys.argv[2] if len(sys.argv)>2 else '/mnt/data/square17_4p5705_candidate/event_polys.npy'
G=4000;K=18282;C=9141;Q=G//4;H=G//2
pts=np.array([(int(r['X']),int(r['Y'])) for r in csv.DictReader(open(atom_path))],dtype=np.int64)
def pp(A0,Ac,As,Ac2=0,As2=0):
 co=(A0+Ac+Ac2,2*As+4*As2,2*A0-6*Ac2,2*As-4*As2,A0-Ac+Ac2);g=0
 for v in co:g=gcd(g,abs(int(v)))
 if g==0:return None
 co=tuple(int(v)//g for v in co)
 for v in reversed(co):
  if v:
   if v<0:co=tuple(-q for q in co)
   break
 return co
N=len(pts);t=time.time();A=set();D={(int(p[0]-q[0]),int(p[1]-q[1])) for p in pts for q in pts}
for dx,dy in D:
 for z in (-G,0,G):A.add(pp(z,dx,dy));A.add(pp(z,dy,-dx))
A.discard(None);print('A',len(A),'diffs',len(D),'sec',time.time()-t,flush=True)
B=set()
for x,y in pts:
 x=int(x);y=int(y)
 for a in (-1,1):
  for b in (-1,1):
   for sig in (-1,1):
    B.add(pp(-Q*(a+b)-H*sig,C*(1+a)-x,C*(1+b)-y,-Q*(a-b),-Q*(a+b)))
    B.add(pp(Q*(a-b)-H*sig,C*(1+b)-y,-C*(1+a)+x,-Q*(a+b),Q*(a-b)))
B.discard(None);print('B',len(B),'sec',time.time()-t,flush=True)
CC=set()
for ii,p in enumerate(pts):
 px,py=map(int,p)
 for q in pts:
  qx,qy=map(int,q)
  for a in (-1,1):
   for sig in (-1,1):
    for tau in (-1,1):
     CC.add(pp(px+qx-K*(1+a),G*(sig+a),G*(a-tau),px-qx,py-qy))
     CC.add(pp(py+qy-K*(1+a),G*(tau+a),G*(sig+a),qy-py,px-qx))
 if ii%100==0:print('C progress',ii,len(CC),'sec',time.time()-t,flush=True)
CC.discard(None);print('C',len(CC),'sec',time.time()-t,flush=True)
U=np.array(sorted(A|B|CC),dtype=np.int64)
if np.max(np.abs(U))<2**31:U=U.astype(np.int32)
np.save(out_path,U);np.savetxt(out_path.replace('.npy','.tsv'),U,fmt='%d',delimiter='\t')
print('union',len(U),'dtype',U.dtype,'max',np.max(np.abs(U)),'sec',time.time()-t)
