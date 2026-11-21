"""Integrate the rational grid upper bound for a four-patch square-board measure."""
from collections import defaultdict
from fractions import Fraction as F
from math import isqrt
from hashlib import sha256
from envelope_grid import G,D,grid
R=7071070

def piece(rows,T,box,fx,fy,omit_far=False):
    x0,y0,x1,y1=box
    events=defaultdict(list)
    edges={x0,x1}
    flat=0
    for x,y,X,Y,w in rows:
        for i in range(1+fx):
            a,b=max(x0,T-X if i else x),min(x1,T-x if i else X)
            if a>=b:continue
            for j in range(1+fy):
                if omit_far and i and j:continue
                c,e=max(y0,T-Y if j else y),min(y1,T-y if j else Y)
                if c>=e:continue
                if not(fx or fy):
                    flat+=(b-a)*(e-c)*w
                    continue
                k=i+2*j
                events[c].append((a,b,k,w))
                events[e].append((a,b,k,-w))
                edges.update((a,b))
    if not(fx or fy):return flat
    edges=sorted(edges)
    index={x:i for i,x in enumerate(edges)}
    widths=[b-a for a,b in zip(edges,edges[1:])]
    changes=[[0]*len(edges) for _ in range(4)]
    total=0
    levels=sorted(events)
    for y,Y in zip(levels,levels[1:]):
        for a,b,k,w in events[y]:
            changes[k][index[a]]+=w
            changes[k][index[b]]-=w
        col=0
        if fx and fy:
            a=b=c=d=0
            for u,v,t,z,h in zip(*changes,widths):
                a+=u;b+=v;c+=t;d+=z
                col+=max(a,b,c,d)*h
        else:
            a=b=0
            for u,v,h in zip(changes[0],changes[1 if fx else 2],widths):
                a+=u;b+=v
                col+=max(a,b)*h
        total+=(Y-y)*col
    return total

def verify(z,claims):
    data=grid(z)
    lines=data.splitlines();S,k=map(int,lines[0].split())
    rows=[tuple(map(int,l.split()))for l in lines[1:]]
    assert len(rows)==k and qpositive(z)
    for r in claims:
        T=F(r['side'])*G
        assert T.denominator==1 and T%2==0
        T=int(T);m=T//2;a=m-R
        assert 2*R*R>=G*G and 0<a<m and m+R<=S
        assert sha256(data).hexdigest()==r['grid_sha256']
        seam=F(r.get('seam',str(F(m,G))))*G
        assert seam.denominator==1
        seam=int(seam)
        assert min(seam,T-seam)>R and max(seam,T-seam)+R<=S
        if seam==m:
            core=piece(rows,T,(0,0,a,a),False,False)
            edge=piece(rows,T,(a,0,m,a),True,False)
            steps=r.get('round_steps',0)
            assert isinstance(steps,int) and 0<=steps<=128
            if steps:
                center=0
                for k in range(steps):
                    y=a+k*R//steps
                    Y=a+(k+1)*R//steps
                    rad=max(0,G*G//2-(m-Y)**2)
                    root=isqrt(rad)
                    reach=root+(root*root<rad)
                    cut=max(a,m-reach)
                    center+=piece(rows,T,(a,y,cut,Y),True,True,True)
                    center+=piece(rows,T,(cut,y,m,Y),True,True)
            else:
                center=piece(rows,T,(a,a,m,m),True,True)
            integral=4*(core+2*edge+center)
        else:
            assert not r.get('round_steps',0)
            zones=[(0,seam-R,False),(seam-R,seam+R,True),(0,T-seam-R,False)]
            integral=0
            for l,u,fx in zones:
                for b,t,fy in zones:
                    integral+=piece(rows,T,(l,b,u,t),fx,fy)
        upper=F(integral,D*G**2)
        assert F(r['mass'])==upper<r['n'] and F(r['side'])>F(r['previous_upper_endpoint'])
        print(f"{r['n']} squares, lower bound {r['side']} by overlapping four translated regions.",flush=True)
def qpositive(z):
    return not z['points'] and all(F(r['mass'])>=0 for r in z['rectangles'])
