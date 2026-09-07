import numpy as np,sys,json
from math import comb
src=sys.argv[1];dst=sys.argv[2]
A=np.load(src).astype(np.int64);p,q,L=83,200,12
B=np.zeros((len(A),5),np.int64)
for i in range(5):
 for k in range(i+1):B[:,i]+=A[:,k]*(p**k)*(q**(4-k))*comb(i,k)*(L//comb(4,k))
constant=(((B>=0).all(1))|((B<=0).all(1)))&~((B==0).all(1))
F=A[~constant]
np.save(dst,F.astype(np.int32));np.savetxt(dst.replace('.npy','.tsv'),F,fmt='%d',delimiter='\t')
out={'raw':len(A),'discarded':int(constant.sum()),'filtered':len(F),'max_bernstein':int(np.max(np.abs(B))),'safety_factor':float((2**63-1)/np.max(np.abs(B)))}
open(dst.replace('.npy','.json'),'w').write(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
