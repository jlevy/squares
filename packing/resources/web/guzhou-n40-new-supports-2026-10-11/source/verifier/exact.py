"""精确密度、输入重建和完整覆盖判定。
Exact density, input regeneration and complete-coverage admission.
"""
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json,math
ROOT=Path(__file__).resolve().parents[1]
ORIGINAL='71011d0356dd179c6e7e6e02c9a064ff30f6f13844016ce3b97463bf7ef53dc0'
SOURCE='984fcd3acc605fe3c50a84912eed77e0192ca5b7253b19b6aa31a4e28e1bf5c2'
POSE='6c64a2d21207e7b65ea011dc7ca7a655418840defbf017340ce44ab7fc7b94fb'
AXIS_INPUT='10dd46b06f14144619bf9de03151c43215e43e34f7e60df440f4e27d6a594396'
KERNEL='da06206b8e83a57b8a710ba62e743c6d3a1959e9160ff32ae89ede583841c73c'
AXIS='f5bc3f60065aaea3d14ffb8465865750fca22cf8bbc6bd8739b5120200b6277d'
P={'n':40,'L':'67/10','B':'3350/3359','X':'3359/500','mass':'3999/100','threshold':'4999/5000',
   'axis_side':'249329659/250000000','epsilon':'1/1000000','last_t':'83/200','denominator':1000000,
   'endpoints':[1,500]+list(range(10000,410001,10000))+[415000],'node_budget':30000000}
L,B,M,TAU,A,EPS,LAST=[Q(P[k]) for k in ('L','B','mass','threshold','axis_side','epsilon','last_t')]
FLAGS=['-O3','-std=c++17','-fno-fast-math','-ffp-contract=off']

def require(x,tag):
    if not x:raise ValueError(tag)

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def digest(raw):return hashlib.sha256(raw).hexdigest()
def pairs(items):
    r={}
    for k,v in items:
        require(k not in r,'DUPLICATE_JSON_KEY');r[k]=v
    return r

def loads(s,exact=False):
    def bad(v):raise ValueError('NONFINITE_JSON')
    return json.loads(s,parse_float=Q if exact else float,parse_constant=bad,object_pairs_hook=pairs)
def load(p,exact=False):return loads(Path(p).read_text(encoding='utf-8'),exact)
def save(p,v):Path(p).write_text(json.dumps(v,sort_keys=True,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def source():
    path=ROOT/'certificate/original_density.json'
    require(sha(path)==ORIGINAL,'ORIGINAL_SOURCE_IDENTITY')
    d=load(path,True)
    require(d['n']==40 and Q(d['L'])==L and len(d['rectangles'])==len(d['weights'])==2526,'ORIGINAL_SCOPE')
    return d

def orbit_key(box):
    a,b,c,e=map(Q,box);out=[]
    for swap in (False,True):
        x0,y0,x1,y1=(b,a,e,c) if swap else (a,b,c,e)
        for fx in (False,True):
            for fy in (False,True):
                xx0,xx1=(L-x1,L-x0) if fx else (x0,x1)
                yy0,yy1=(L-y1,L-y0) if fy else (y0,y1)
                out.append((xx0,yy0,xx1,yy1))
    return min(out)

def source_rows(path):
    require(sha(path)==SOURCE,'DENSITY_IDENTITY');d=load(path,True);original=source()
    require(d['schema']=='n40-expanded-rectangles/v1' and d['source_sha256']==ORIGINAL,'CANDIDATE_SCHEMA')
    for key in ('n','L','B','X','mass','threshold','epsilon','axis_side'):
        require(Q(d[key])==Q(P[key]),'CANDIDATE_PARAMETER:'+key)
    r=[];s=[];total=Q(0);ids=[];orbits=[];inherited=generated=0
    inherited_keys={orbit_key(box) for box in original['rectangles']}
    for site in d['sites']:
        a,b,c,e=map(Q,site['box']);w=Q(site['weight'])
        require(w>0 and 0<=a<c<=L and 0<=b<e<=L,'POSITIVE_LEGAL_SUPPORT')
        if site['kind']=='inherited':
            j=site['source_index'];require(type(j)is int and 0<=j<2526,'SOURCE_INDEX')
            require([a,b,c,e]==list(map(Q,original['rectangles'][j])),'INHERITED_GEOMETRY')
            ids.append(('inherited',j));inherited+=1
        else:
            require(site['kind']=='generated' and isinstance(site['site_id'],str),'GENERATED_KIND')
            require(orbit_key([a,b,c,e]) not in inherited_keys,'GENERATED_GEOMETRY_NOT_NEW')
            ids.append(('generated',site['site_id']));generated+=1
        rho=w/(8*(c-a)*(e-b));total+=w;orbit=[]
        for swap in (False,True):
            x0,y0,x1,y1=(b,a,e,c) if swap else (a,b,c,e)
            for fx in (False,True):
                for fy in (False,True):
                    xx0,xx1=(L-x1,L-x0) if fx else (x0,x1)
                    yy0,yy1=(L-y1,L-y0) if fy else (y0,y1)
                    r.append((xx0,yy0,xx1,yy1,rho));orbit.append((xx0,yy0,xx1,yy1))
        orbits.append(min(orbit))
        for reflection in (False,True):
            x0,y0,x1,y1=(L-c,b,L-a,e) if reflection else (a,b,c,e)
            for _ in range(4):
                s.append((x0,y0,x1,y1,rho));x0,y0,x1,y1=L-y1,x0,L-y0,x1
    require(len(ids)==len(set(ids))==len(set(orbits))==685 and (inherited,generated)==(522,163),'UNIQUE_ORBITS')
    require(len(r)==5480 and Counter(r)==Counter(s),'D4_EXPANSIONS')
    require(total==M and sum((c-a)*(e-b)*rho for a,b,c,e,rho in r)==M,'MASS')
    require(Counter(r)==Counter((L-e,a,L-b,c,rho) for a,b,c,e,rho in r),'QUARTER_TURN')
    return r,s

def enclose(x,hexadecimal=False):
    x=Q(x);v=float(x);f=Q(v)
    lo=v if f<=x else math.nextafter(v,-math.inf);hi=v if f>=x else math.nextafter(v,math.inf)
    require(math.isfinite(lo) and math.isfinite(hi) and Q(lo)<=x<=Q(hi),'OUTWARD_ENCLOSURE')
    return lo.hex()+' '+hi.hex() if hexadecimal else f'{lo:.17g} {hi:.17g}'

def make_inputs(path):
    rows,other=source_rows(path)
    pose=(enclose(L,True)+'\n'+enclose(B,True)+'\n'+str(len(rows))+'\n'+''.join(' '.join(enclose(v,True) for v in row)+'\n' for row in rows)).encode()
    G=10**9;rr=[]
    floor=lambda v:v.numerator//v.denominator
    ceil=lambda v:-((-v.numerator)//v.denominator)
    for a,b,c,e,rho in other:
        aa,bb,cc,ee,w=ceil(a*G),ceil(b*G),floor(c*G),floor(e*G),floor(rho*G)
        if aa<cc and bb<ee and w>0:
            require(Q(aa,G)>=a and Q(bb,G)>=b and Q(cc,G)<=c and Q(ee,G)<=e and Q(w,G)<=rho,'DOMINATED_MEASURE')
            rr.append((aa,bb,cc,ee,w))
    ll=int(L*G);ab=int(A*G)
    require(Q(ll,G)==L and Q(ab,G)==A and ll%2==ab%2==0,'INTEGER_HALVES')
    require(Counter(rr)==Counter((ll-e,a,ll-b,c,w) for a,b,c,e,w in rr),'AXIS_SYMMETRY')
    weights=sum(t[4] for t in rr);bound=16*weights*(ll+ll+ab//2)**2
    require(weights<10**15 and bound<2**125,'INTEGER_OVERFLOW_BOUND')
    axis=(f'{ll} {ab} {G} {G} 4999 5000 {len(rr)}\n'+''.join(' '.join(map(str,t))+'\n' for t in rr)).encode()
    require(digest(pose)==POSE and digest(axis)==AXIS_INPUT,'FROZEN_INPUT_BYTES')
    return pose,axis,{'source_sha256':SOURCE,'pose_input_sha256':POSE,'axis_input_sha256':AXIS_INPUT,
                      'terms':len(rows),'positive_representatives':685,'inherited_representatives':522,'generated_representatives':163,'original_sha256':ORIGINAL,'mass':str(M),'axis_evaluation_bound':str(bound)}

def scalar():
    sqrt2hi=Q(1414213562373096,10**15)
    require(sqrt2hi**2>2 and L>B*sqrt2hi and 0<EPS<LAST<Q(1,2),'GEOMETRIC_RANGE')
    width=(1+2*EPS-EPS*EPS)/(1+EPS*EPS)
    require(0<A<=B and A*width<=B and LAST*LAST+2*LAST-1>0,'NEAR_AXIS_CONTAINMENT')
    require(L/B==Q(3359,500) and 40*TAU-M==Q(1,500),'COUNTING')
    return {'claim':'s(40) > 3359/500','X':str(L/B),'mass':str(M),'threshold':str(TAU),
            'counting_margin':str(40*TAU-M),'axis_containment_margin':str(B-A*width)}

def admit_slabs(rows,binary):
    require(len(rows)==43,'MISSING_SLAB');nodes=leaves=splits=0;minimum=None
    for i,(r,(lo,hi)) in enumerate(zip(rows,zip(P['endpoints'],P['endpoints'][1:]))):
        require(r['index']==i and r['arguments']==[str(lo),str(hi),'1000000','4999','5000','30000000'],'SLAB_DOMAIN')
        require(r['exit_code']==0 and r['timed_out'] is False,'SLAB_EXECUTION')
        require(r['input_sha256']==POSE and r['source_sha256']==KERNEL and r['binary_sha256']==binary,'SLAB_IDENTITY')
        z=loads(r['stdout'])
        require(z['status']=='verified' and (z['pl'],z['ph'],z['den'])==(lo,hi,10**6),'VERDICT')
        require(type(z['nodes']) is int and type(z['leaves']) is int and z['leaves']>0 and z['nodes']==2*z['leaves']-1,'BINARY_COVER')
        require(type(z['lower_bound']) is float and math.isfinite(z['lower_bound']) and Q(z['lower_bound'])>=TAU,'CAPTURE')
        require(type(z['max_depth']) is int and type(z['angle_splits']) is int and 0<=z['max_depth']<=123 and 0<=z['angle_splits']<z['nodes'],'DEPTH')
        nodes+=z['nodes'];leaves+=z['leaves'];splits+=z['angle_splits']
        val=Q(z['lower_bound']);minimum=val if minimum is None else min(minimum,val)
    return {'slabs':43,'nodes':nodes,'leaves':leaves,'angle_bisections':splits,'minimum_capture_lower':str(minimum)}

def admit_axis(r,binary):
    require(r['exit_code']==0 and r['input_sha256']==AXIS_INPUT and r['source_sha256']==AXIS and r['binary_sha256']==binary,'AXIS_IDENTITY')
    z=loads(r['stdout']);require(z['status']=='AXIS_COVERAGE_PROVED' and z['direct_sum_matches'] is True,'AXIS_VERDICT')
    require(z['x_nodes']==z['y_nodes']==3293 and int(z['scale'])==10**27,'AXIS_DOMAIN')
    v=Q(int(z['minimum_numerator']),int(z['scale']))
    require(v>=TAU and 0<int(z['evaluation_abs_bound'])<2**125,'AXIS_CAPTURE')
    _,axis,_=make_inputs(ROOT/'certificate/certified_candidate.json')
    text=axis.decode().splitlines();ll,side,G,W,tn,td,n=map(int,text[0].split());rr=[tuple(map(int,line.split())) for line in text[1:]]
    require(len(rr)==n,'AXIS_ROWS')
    xs={ll//2,ll-side//2};ys=xs.copy()
    for a,b,c,e,w in rr:
        xs.update(x for v in (a,c) for x in (v-side//2,v+side//2) if ll//2<=x<=ll-side//2)
        ys.update(y for v in (b,e) for y in (v-side//2,v+side//2) if ll//2<=y<=ll-side//2)
    require(len(xs)==z['x_nodes'] and len(ys)==z['y_nodes'],'AXIS_COMPLETE_EVENTS')
    cx,cy=z['minimizer_x_integer'],z['minimizer_y_integer'];require(cx in xs and cy in ys,'AXIS_MINIMIZER_DOMAIN')
    direct=sum(w*max(0,min(c,cx+side//2)-max(a,cx-side//2))*max(0,min(e,cy+side//2)-max(b,cy-side//2)) for a,b,c,e,w in rr)
    require(direct==int(z['minimum_numerator']),'AXIS_EXACT_DIRECT_SUM')
    require(int(z['evaluation_abs_bound'])==16*sum(x[4] for x in rr)*(2*ll+side//2)**2,'AXIS_OVERFLOW_IDENTITY')
    return {'vertices':3293**2,'minimum_capture_lower':str(v),'margin':str(v-TAU)}
