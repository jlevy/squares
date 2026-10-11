"""精确密度、输入重建和完整覆盖判定。
Exact density, input regeneration and complete-coverage admission.
"""
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json,math
ROOT=Path(__file__).resolve().parents[1]
SOURCE='71011d0356dd179c6e7e6e02c9a064ff30f6f13844016ce3b97463bf7ef53dc0'
POSE='ccf7b68aa89fdcfcf0d78ac135cfa24e4a73b822eb412b2aac46e9c49e2b9925'
AXIS_INPUT='d57e8bb267dc1a17d57fa0f17f662bf552b6aef46427a0eb9308ae16539ed1cb'
KERNEL='da06206b8e83a57b8a710ba62e743c6d3a1959e9160ff32ae89ede583841c73c'
AXIS='f5bc3f60065aaea3d14ffb8465865750fca22cf8bbc6bd8739b5120200b6277d'
P={'n':40,'L':'67/10','B':'199529/200000','X':'1340000/199529','mass':'3999/100','threshold':'4999/5000',
   'axis_side':'997643/1000000','epsilon':'1/1000000','last_t':'83/200','denominator':1000000,
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

def source_rows(path):
    require(sha(path)==SOURCE,'DENSITY_IDENTITY');d=load(path,True)
    require(d['n']==40 and Q(d['L'])==L and Q(d['B'])==Q(9977,10000),'SOURCE_PARAMETERS')
    require(len(d['rectangles'])==len(d['weights']),'SOURCE_LENGTH')
    r=[];s=[];total=Q(0);count=0
    for coords,wt in zip(d['rectangles'],d['weights']):
        w=Q(wt);require(w>=0,'NEGATIVE_WEIGHT')
        if not w:continue
        a,b,c,e=map(Q,coords);require(0<=a<c<=L and 0<=b<e<=L,'SUPPORT')
        rho=w/(8*(c-a)*(e-b));count+=1;total+=w
        for swap in (False,True):
            x0,y0,x1,y1=(b,a,e,c) if swap else (a,b,c,e)
            for fx in (False,True):
                for fy in (False,True):
                    xx0,xx1=(L-x1,L-x0) if fx else (x0,x1)
                    yy0,yy1=(L-y1,L-y0) if fy else (y0,y1)
                    r.append((xx0,yy0,xx1,yy1,rho))
        for reflection in (False,True):
            x0,y0,x1,y1=(L-c,b,L-a,e) if reflection else (a,b,c,e)
            for _ in range(4):
                s.append((x0,y0,x1,y1,rho));x0,y0,x1,y1=L-y1,x0,L-y0,x1
    require(count==480 and len(r)==3840 and Counter(r)==Counter(s),'D4_EXPANSIONS')
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
    pose=(enclose(L,True)+'\n'+enclose(B)+'\n3840\n'+''.join(' '.join(enclose(v,True) for v in row)+'\n' for row in rows)).encode()
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
                      'terms':len(rows),'positive_representatives':480,'mass':str(M),'axis_evaluation_bound':str(bound)}

def scalar():
    sqrt2hi=Q(1414213562373096,10**15)
    require(sqrt2hi**2>2 and L>B*sqrt2hi and 0<EPS<LAST<Q(1,2),'GEOMETRIC_RANGE')
    width=(1+2*EPS-EPS*EPS)/(1+EPS*EPS)
    require(0<A<=B and A*width<=B and LAST*LAST+2*LAST-1>0,'NEAR_AXIS_CONTAINMENT')
    require(L/B==Q(1340000,199529) and 40*TAU-M==Q(1,500),'COUNTING')
    return {'claim':'s(40) > 1340000/199529','X':str(L/B),'mass':str(M),'threshold':str(TAU),
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
        require(0<=z['max_depth']<=123 and 0<=z['angle_splits']<z['nodes'],'DEPTH')
        nodes+=z['nodes'];leaves+=z['leaves'];splits+=z['angle_splits']
        val=Q(z['lower_bound']);minimum=val if minimum is None else min(minimum,val)
    return {'slabs':43,'nodes':nodes,'leaves':leaves,'angle_bisections':splits,'minimum_capture_lower':str(minimum)}

def admit_axis(r,binary):
    require(r['exit_code']==0 and r['input_sha256']==AXIS_INPUT and r['source_sha256']==AXIS and r['binary_sha256']==binary,'AXIS_IDENTITY')
    z=loads(r['stdout']);require(z['status']=='AXIS_COVERAGE_PROVED' and z['direct_sum_matches'] is True,'AXIS_VERDICT')
    require(z['x_nodes']==z['y_nodes']==2213 and int(z['scale'])==10**27,'AXIS_DOMAIN')
    v=Q(int(z['minimum_numerator']),int(z['scale']))
    require(v>=TAU and 0<int(z['evaluation_abs_bound'])<2**125,'AXIS_CAPTURE')
    return {'vertices':2213**2,'minimum_capture_lower':str(v),'margin':str(v-TAU)}
