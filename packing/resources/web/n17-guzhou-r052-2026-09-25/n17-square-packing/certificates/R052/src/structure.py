"""Exact structure, additive budget and angular containment for new resources.

This does not establish centre-space minima or a packing lower bound.
"""
from fractions import Fraction as Q
from hashlib import sha256
from collections import Counter
from pathlib import Path
from copy import deepcopy
from time import monotonic
import json
import argparse


def check(cert):
    L,A=Q(cert['L']),Q(cert['A']);D=cert['coordinate_denominator']
    assert type(D) is int and D>0 and (L*D).denominator==1 and 0<A<L
    assert Q(cert['bound'])==L/A==Q(231001,50000)
    LD=int(L*D);sites=[];owners=[];budget=0
    for j,(x,y,w) in enumerate(cert['point_orbits']):
        assert all(type(v) is int for v in (x,y,w)) and w>=0 and 0<=x<=LD and 0<=y<=LD
        orb=sorted({(u,v) for a,b in [(x,y),(y,x)] for u in (a,LD-a) for v in (b,LD-b)})
        sites.extend(orb);owners.extend([j]*len(orb));budget+=len(orb)*w
    assert len(sites)==len(set(sites));lookup={p:i for i,p in enumerate(sites)}
    group_count=0
    for family,gkey,kfixed in [('threshold_orbits','triples',2),('generic_trigger_orbits','groups',None)]:
        for orbit in cert[family]:
            w=orbit['weight'];k=kfixed if kfixed else orbit['k'];groups=orbit[gkey]
            assert type(w) is int and w>=0 and groups and type(k) is int
            m=len(groups[0]);assert 1<=k<=m and (kfixed is None or m==3)
            for group in groups:
                assert len(group)==len(set(group))==m and all(type(i) is int and 0<=i<len(sites) for i in group)
            given={tuple(sorted(g)) for g in groups};assert len(given)==len(groups)
            transformed=set()
            for swap in (False,True):
                for fx in (False,True):
                    for fy in (False,True):
                        image=[]
                        for i in groups[0]:
                            x,y=sites[i]
                            if swap:x,y=y,x
                            image.append(lookup[(LD-x if fx else x,LD-y if fy else y)])
                        transformed.add(tuple(sorted(image)))
            assert given==transformed
            budget+=len(groups)*(m//k)*w;group_count+=len(groups)
    assert budget==cert['budget_units']
    assert type(cert['weight_denominator']) is int and cert['weight_denominator']>0
    assert cert['minimum_units']==budget//17+1 and 17*cert['minimum_units']>budget
    def cs(t):return (1-t*t)/(1+t*t),2*t/(1+t*t)
    last=Q(0);lowest=None;inequalities=0
    for entry in cert['entries']:
        a,b,t,B=map(Q,entry)
        assert a==last and 0<=a<b<1 and a<=t<=b and 0<B<A
        c,s=cs(t);ca,sa=cs(a);cb,sb=cs(b)
        assert c*c+s*s==1 and c>=0 and s>=0
        assert B*(c+s)<=A*min(ca+sa,cb+sb)
        for pc,ps in [(ca,sa),(cb,sb)]:
            dot=c*pc+s*ps;cross=c*ps-s*pc
            assert dot>0 and dot>=abs(cross)
            for ax,ay in [(pc,ps),(-ps,pc)]:
                extent=B*(abs(ax*c+ay*s)+abs(-ax*s+ay*c))/2
                margin=A/2-extent;assert margin>0
                inequalities+=1;lowest=margin if lowest is None else min(lowest,margin)
        last=b
    # tan(pi/8)=sqrt(2)-1. The final rational endpoint must cover it.
    assert last*last+2*last>=1 and cert['entries']
    return dict(physical_sites=len(sites),point_orbits=len(cert['point_orbits']),threshold_orbits=len(cert['threshold_orbits']),generic_orbits=len(cert['generic_trigger_orbits']),
        physical_trigger_groups=group_count,budget_units=budget,required_minimum_units=cert['minimum_units'],
        angular_rows=len(cert['entries']),strict_containment_inequalities=inequalities,minimum_containment_margin=str(lowest))


def main():
    if not __debug__:raise RuntimeError('Optimization-disabled assertions are not a verification mode')
    ap=argparse.ArgumentParser();ap.add_argument('--candidate',required=True);ap.add_argument('--output',required=True);args=ap.parse_args()
    root=Path(__file__).resolve().parents[2];source=root/args.candidate;out=root/args.output;assert not out.exists()
    start=monotonic();raw=source.read_bytes();cert=json.loads(raw);report=check(cert)
    faults={
        'negative_point_weight':lambda c:c['point_orbits'][0].__setitem__(2,-1),
        'incomplete_D4_trigger':lambda c:c['threshold_orbits'][0]['triples'].pop(),
        'bad_trigger_site':lambda c:c['threshold_orbits'][0]['triples'][0].__setitem__(0,-1),
        'wrong_budget':lambda c:c.__setitem__('budget_units',c['budget_units']+1),
        'wrong_target':lambda c:c.__setitem__('bound','462001/100000'),
        'angular_gap':lambda c:c['entries'][1].__setitem__(0,str((Q(c['entries'][1][0])+Q(c['entries'][1][1]))/2)),
        'lost_strict_containment':lambda c:c['entries'][0].__setitem__(3,str(Q(c['A'])-Q(1,10**100))),
    }
    controls={}
    for name,mutate in faults.items():
        bad=deepcopy(cert);mutate(bad)
        try:check(bad)
        except (AssertionError,KeyError,ValueError):controls[name]='REJECTED'
        else:raise AssertionError('Fault passed: '+name)
    assert source.read_bytes()==raw
    report.update(status='PASS_STRUCTURE_AND_CONTAINMENT_ONLY',candidate_sha256=sha256(raw).hexdigest(),auditor_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        negative_controls=controls,seconds=monotonic()-start,scope='No centre minimum or numerical lower bound is asserted; source-distinct acceptance review remains separate')
    with out.open('x',encoding='utf-8') as f:json.dump(report,f,indent=2);f.write('\n')
    print(json.dumps(report),flush=True)


if __name__=='__main__':main()
