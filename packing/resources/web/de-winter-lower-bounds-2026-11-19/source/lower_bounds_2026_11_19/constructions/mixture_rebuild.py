"""Reconstruct sparse rational mixtures from their earlier exclusion measures."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from itertools import product
import json,gzip,hashlib,math
here=Path(__file__).resolve().parent
def axis_bands(B,j,word,cut):
    S=B+j
    if not j:return [(0,B,0,F(1))]
    if word=='middle':
        if j>0:
            c=(B-1)/2
            r=[(0,c,0)]+[(c,c+1,m)for m in range(j+1)]+[(c+1,B,j)]
        else:
            c=S/2;r=[(0,c,0),(c-j,B,j)]
    elif word=='asym':
        if j>0:r=[(0,cut,0)]+[(cut,cut+1,m)for m in range(j+1)]+[(cut+1,B,j)]
        else:r=[(0,cut,0),(cut-j,B,j)]
        first=[(l,h,s,F(1,2))for l,h,s in r if l<h]
        return first+[(B-h,B-l,j-s,w)for l,h,s,w in first]
    elif word=='pair':
        if j>0:
            half=[(0,cut,0)]+[(cut,cut+F(1,2),F(m,2))for m in range(j+1)]+[(cut+F(1,2),B/2,F(j,2))]
        else:
            width=F(-j,2);half=[(0,cut,0),(cut+width,B/2,-width)]
        r=half+[(B-h,B-l,j-s)for l,h,s in reversed(half)]
    else:raise ValueError(word)
    return [(l,h,s,F(1))for l,h,s in r if l<h]
def component(source,term,S):
    L=F(source['L']);j=term['j'];B=S-j
    def warp(x):
        if not term['warp']:return x*B/L
        k=math.floor(L);f=L-k;g=B-k
        if not(0<f<1 and 0<g<1):return x*B/L
        t=math.floor(x);u=x-t
        return t+(u*g/f if u<=f else g+(u-f)*(1-g)/(1-f))
    bands=axis_bands(B,j,term['word'],F(term['loc']))
    def split(l,h):
        for x,X,d,k in bands:
            lo,hi=max(l,x),min(h,X)
            if lo<hi:yield lo+d,hi+d,(hi-lo)*k
    parts=defaultdict(F)
    for row in source['rectangles']:
        x,y,X,Y=(warp(F(t))for t in row['rectangle']);den=F(row['mass'])/((X-x)*(Y-y))
        for (l,h,w),(u,v,t)in product(split(x,X),split(y,Y)):
            parts[l,u,h,v]+=den*w*t
    return parts
def verify(q):
    target=json.load(gzip.open(here.parent/'sources'/q['output_file']));S=F(target['L']);combined=defaultdict(F)
    for term in q['sources']:
        raw=(here/term['input_file']).read_bytes();assert hashlib.sha256(raw).hexdigest()==term['input_sha256']
        parts=component(json.loads(gzip.decompress(raw)),term,S)
        if q['quantized']:
            rounded=defaultdict(int)
            for coords,w in parts.items():
                key=tuple(F(round(v*10**9),10**9)for v in coords)
                if key[0]<key[2]and key[1]<key[3]:rounded[key]+=round(w*10**13)
            parts=rounded
        total=sum(parts.values());unit=term['units']
        for coords,w in parts.items():combined[coords]+=F(unit)*w/total
    scale=F(target['total_mass'])/sum(combined.values());out={k:v*scale for k,v in combined.items()if v>0}
    actual={tuple(map(F,row['rectangle'])):F(row['mass'])for row in target['rectangles']}
    assert out==actual
    print(f"Rebuilt the {len(q['sources'])}-source measure for {q['n']} squares, including all {len(out):,} masses.")
if __name__=='__main__':
    if not __debug__:raise SystemExit('Run with assertions enabled.')
    for q in json.load(open(here/'mix_cases.json')):verify(q)
