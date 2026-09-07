import numpy as np, pathlib
from math import comb
root=pathlib.Path(__file__).resolve().parents[1]
A=np.load(root/'data/event_polys.npy').astype(np.int64)
p,q,L=83,200,12
B=np.zeros((len(A),5),np.int64)
for i in range(5):
 for k in range(i+1):B[:,i]+=A[:,k]*(p**k)*(q**(4-k))*comb(i,k)*(L//comb(4,k))
constant=(((B>=0).all(1))|((B<=0).all(1)))&~((B==0).all(1))
F=A[~constant]
bundled=np.loadtxt(root/'data/event_polys_filtered.tsv',dtype=np.int64,delimiter='\t')
if bundled.ndim==1:bundled=bundled[None,:]
assert F.shape==(150531,5)
assert np.array_equal(F,bundled)
print('raw_polynomials=1344862')
print('exactly_discarded=1194331')
print('filtered_polynomials=150531')
print('EXACT BERNSTEIN FILTER PASS')
