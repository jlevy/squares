"""Replay a rigorous lower bound on the side under uniform scaling of all centers."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import gzip,json


def axes(t):
    c=(1-t*t)/(1+t*t)
    s=2*t/(1+t*t)
    return (c,s),(-s,c)


def dot(a,b):
    return a[0]*b[0]+a[1]*b[1]


def minimum_scale(a,b):
    x,y,A=a
    X,Y,B=b
    delta=(X-x,Y-y)
    ratios=[]
    for axis in A+B:
        projection=abs(dot(axis,delta))
        if projection:
            width=sum(abs(dot(axis,v)) for v in A+B)/2
            ratios.append(width/projection)
    return min(ratios)


def read(z):
    return [(F(s['cx']),F(s['cy']),axes(F(s['t']))) for s in z['squares']]


def lower(side_rows,scale):
    w=[sum(abs(z[0]) for z in a)/2 for x,y,a in side_rows]
    return max(max(r[j]*scale+v for r,v in zip(side_rows,w))-
               min(r[j]*scale-v for r,v in zip(side_rows,w)) for j in (0,1))


def select(z):
    a=read(z)
    close=[(i,j) for i,j in combinations(range(len(a)),2)
           if max(abs(float(a[i][k]-a[j][k])) for k in (0,1))<1.43]
    g,pair=max((minimum_scale(a[i],a[j]),(i,j)) for i,j in close)
    return dict(pair=list(pair),necessary_scale=str(g),lower_endpoint=str(lower(a,g)))


def verify(folder):
    z=json.load(gzip.open(folder/'previous_for_scaling.json.gz'))
    p=json.loads((folder/'scaling_bound.json').read_text())
    a=read(z)
    i,j=p['pair']
    assert 0<=i<j<len(a)==z['n']
    scale=minimum_scale(a[i],a[j])
    assert 0<scale==F(p['necessary_scale'])
    # The extent at scale g is max_ij(g |x_i-x_j| + w_i + w_j), in either axis.
    # It is nondecreasing. The indicated pair forces at least this scale by SAT.
    cap=lower(a,scale)
    assert cap==F(p['lower_endpoint'])>F(json.load(gzip.open(folder/'packing.json.gz'))['side'])
    return cap
