"""Rebuild normalized, symmetrically widened rectangles using only rational arithmetic."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,gzip
where=Path(__file__).resolve().parent
def verify(v):
    src=where/v['input_file'];assert sha256(src.read_bytes()).hexdigest()==v['input_sha256']
    a=json.load(gzip.open(src));z=json.load(gzip.open(where.parent/'sources'/v['output_file']))
    L=F(v['side']);base=F(a['L']);mass=F(v['n'])-F(1,10**6);fac=F(v['fraction_widened']);w=F(v['minimum_width'])
    assert 0<fac<=1 and 0<w<L and F(z['total_mass'])==mass
    def cut(l,h):
        if h-l>=w:return l,h
        x=min(L-w,max(F(0),(l+h-w)/2));return x,x+w
    out=[]
    for orig in a['rectangles']:
        x,y,X,Y=[F(t)*L/base for t in orig['rectangle']];m=F(orig['mass'])*mass/F(a['total_mass'])
        l,h=cut(x,X);b,t=cut(y,Y)
        if fac<1 and (x,X,y,Y)!=(l,h,b,t):out.append(((x,y,X,Y),m*(1-fac)));m*=fac
        out.append(((l,b,h,t),m))
    assert out==[(tuple(map(F,r['rectangle'])),F(r['mass']))for r in z['rectangles']]
    print(v['n'],len(out),'widened rectangles rebuilt with rational arithmetic',flush=True)
if __name__=='__main__':
    for q in json.load(open(where/'smooth_cases.json')):verify(q)
