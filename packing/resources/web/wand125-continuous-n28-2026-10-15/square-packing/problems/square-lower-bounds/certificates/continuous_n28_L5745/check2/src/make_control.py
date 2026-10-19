"""Generate the exact 197/200-mass n40 negative control."""
from fractions import Fraction as Q
from generator import ROOT,load,save

def strings(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,list):return [strings(v) for v in x]
    if isinstance(x,dict):return {k:strings(v) for k,v in x.items()}
    return x

if __name__=='__main__':
    d=load(ROOT/'upstream/certificate/certified_candidate.json')
    d['weights']=[str(Q(w)*Q(197,200)) for w in d['weights']]
    d['mass']=str(Q(d['mass'])*Q(197,200))
    save(ROOT/'inputs/n40.mass0985.json',strings(d))
