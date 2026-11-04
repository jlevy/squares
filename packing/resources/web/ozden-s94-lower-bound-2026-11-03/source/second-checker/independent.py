#!/usr/bin/env python3
"""Independent exact admission, fixed-point preparation, and rational clipping oracle."""
import json, gzip, sys, hashlib
from fractions import Fraction as F
from pathlib import Path
S=1<<42

def load(path):
    with (gzip.open(path,'rt') if str(path).endswith('.gz') else open(path)) as f:
        return json.load(f,parse_float=str)
def floor(q): return q.numerator//q.denominator
def ceil(q): return -floor(-q)
def images(v,L):
    x,y,X,Y=v
    # Four rotations followed by the four rotated diagonal reflections.
    out=[]
    for a,b,c,d in ((x,y,X,Y),(y,x,Y,X)):
        for _ in range(4):
            out.append((a,b,c,d)); a,b,c,d=L-d,a,L-b,c
    return out

def prepare(d,out,rs):
    L,B=F(d['L']),F(d['B']); D=F(d.get('proof_net',{}).get('step','83/40000')); m=int(d.get('proof_net',{}).get('last',200))
    rows=[(tuple(map(F,r['rectangle'])),F(r['mass'])) for r in d['rectangles']]
    M=sum((w for _,w in rows),F(0));t=m*D
    ck={'n_is_94':int(d['n'])==94,'mass':0<M<94,'mass_declared':M==F(d['total_mass']), 'core':0<B<1,'step':D>0,'last':m>=1,'endpoint':t*t+2*t-1>0,'tmax_cap':t<=F(1,2),'shrink':B*(1+D)<1,'tangent':B*(1+D/(1-D*D/4))<1,'nonempty_domains':L*L>=2*B*B,'rectangles':all(w>=0 and 0<=v[0]<v[2]<=L and 0<=v[1]<v[3]<=L for v,w in rows),'no_points':not d.get('points'),'no_segments':not d.get('segments')}
    info={'checks':ck,'L':str(L),'B':str(B),'D':str(D),'last':m,'M':str(M),'mass_gap':str(94-M),'shrink':str(B*(1+D)),'tangent':str(B*(1+D/(1-D*D/4))),'endpoint_polynomial':str(t*t+2*t-1)}
    if not all(ck.values()): return info
    # Bounds used in the integer implementation's overflow and reciprocal-division proof.
    assert 0<L<10 and D==F(83,120000) and m==599
    edge_sum=sum((w*(1/(v[2]-v[0])+1/(v[3]-v[1]))/2 for v,w in rows),F(0))
    assert edge_sum<2**14
    info['integer_limits']={'scale':S,'L_lt_10':True,'max_expanded_density_lt_65536':True,'sum_density_times_vertical_edge_length_upper':str(F(ceil(edge_sum*10**9),10**9)),'sum_density_times_vertical_edge_length_lt_16384':True}
    expanded=[]
    for v,w in rows:
        if not w:continue
        rho=w/8/((v[2]-v[0])*(v[3]-v[1]))
        assert rho<2**16
        for a,b,c,e in images(v,L):
            z=(ceil(a*S),ceil(b*S),floor(c*S),floor(e*S),floor(rho*S))
            assert z[0]<z[2] and z[1]<z[3] and 0<=z[4]<1<<60
            expanded.append(z)
    with open(out,'w') as f:
        print(S,floor(L*S/2),floor(B*S/2),len(expanded),len(rs),file=f)
        for z in expanded:print(*z,file=f)
        domains={}
        for r in rs:
            t=r*D; den=1+t*t;c=(1-t*t)/den;s=2*t/den
            a=max(F(0),t-D/2);rho=(1+2*a-a*a)/(2*(1+a*a));margin=max(rho,B*(c+s)/2); U=L-margin
            cn,sn,den=D.denominator**2-r*r*D.numerator**2,2*r*D.numerator*D.denominator,D.denominator**2+r*r*D.numerator**2
            assert cn*cn+sn*sn==den*den and 0<=sn and 0<cn and den<1<<35
            print(r,cn,sn,den,ceil(U*S),file=f); domains[str(r)]={'lower':str(L/2),'upper':str(U),'margin':str(margin)}
    info['domains']=domains;info['expanded']=len(expanded)
    return info

def clip(poly,A,B,C):
    if not poly:return []
    out=[]
    for p,q in zip(poly,poly[1:]+poly[:1]):
        fp=A*p[0]+B*p[1]-C;fq=A*q[0]+B*q[1]-C
        if fp<=0:out.append(p)
        if (fp<0<fq) or (fq<0<fp):
            z=fp/(fp-fq);out.append((p[0]+z*(q[0]-p[0]),p[1]+z*(q[1]-p[1])))
    return out

def capture(d,r,x,y):
    L,B=F(d['L']),F(d['B']);D=F(d.get('proof_net',{}).get('step','83/40000'));t=r*D;c=(1-t*t)/(1+t*t);s=2*t/(1+t*t);h=B/2;ext=h*(c+s);tot=F(0)
    for row in d['rectangles']:
        v=tuple(map(F,row['rectangle']));w=F(row['mass'])
        if not w:continue
        rho=w/8/((v[2]-v[0])*(v[3]-v[1]))
        for a,b,A,Bb in images(v,L):
            if A<=x-ext or a>=x+ext or Bb<=y-ext or b>=y+ext:continue
            p=[(a-x,b-y),(A-x,b-y),(A-x,Bb-y),(a-x,Bb-y)]
            for u,vv in ((c,s),(-c,-s),(-s,c),(s,-c)):
                p=clip(p,u,vv,h)
                if len(p)<3:break
            if len(p)<3:continue
            area=abs(sum((p[i][0]*p[(i+1)%len(p)][1]-p[i][1]*p[(i+1)%len(p)][0] for i in range(len(p))),F(0)))/2
            tot+=rho*area
    return tot

if __name__=='__main__':
    d=load(sys.argv[1]);rs=list(map(int,sys.argv[3].split(',')))
    info=prepare(d,sys.argv[2],rs);print(json.dumps(info,indent=2))
