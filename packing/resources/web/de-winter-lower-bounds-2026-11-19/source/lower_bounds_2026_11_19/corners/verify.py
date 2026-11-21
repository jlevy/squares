"""Verify the change to each published corner measure and replay its continuous local cover."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache,reduce
from math import comb,ceil,floor,lcm,gcd,isqrt
from itertools import combinations
import argparse,csv,gzip,hashlib,json,sys,subprocess,tempfile
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import family_structure as fs
G=2**28;DS=2**30;M=2**40
def require(ok,what):
    if not ok:raise ValueError(what)
def shape(ix,table):
    rec=table[ix-1];p=H/'families'/f'family_{ix}.json'
    require(hashlib.sha256(p.read_bytes()).hexdigest()==rec['family_sha256'],'source family hash')
    fam=fs.load(p);per,fixed,translating=fs.decompose(fam)
    require((fam['d0'],fam['d1'])==(F(rec['d0']),F(rec['d1'])),'source endpoints')
    return fam,per,fixed,translating
def cut(case,fixed):
    x,y,pct=map(F,(case['X'],case['Y'],case['pct']));mode=case['mode'];reduced=[];taken=[];sub=F(0)
    require(0<pct<=1 and mode in ('h','v','both') and 0<x<=2 and 0<y<=2,'cut specification')
    for typ,axis,lo,hi,dens in fixed:
        require(dens>=0,'negative fixed-corner density')
        if not dens:continue
        edge,along=(x,y) if typ=='v' else(y,x)
        if axis<=edge and lo<along and mode in (typ,'both'):
            z=min(hi,along);sub+=(z-lo)*dens*pct
            for val in (lo,z):taken.append((axis,val) if typ=='v' else (val,axis))
            reduced.append((typ,axis,lo,z,dens*(1-pct)))
            if z<hi:reduced.append((typ,axis,z,hi,dens))
        else:reduced.append((typ,axis,lo,hi,dens))
    box=tuple(f(v[k] for v in taken)for f in (min,max)for k in range(2))
    require(box==tuple(map(F,case['affected_bounds'])),'affected support bounds')
    require(sub==F(case['subtraction_per_corner']) and sub>0,'corner saving')
    pieces=[(t=='v',l,h,a,a,w*(h-l))for t,a,l,h,w in reduced if w>0 and h<=F(12,5)]
    return box[2:],pieces
def bands(case,fam,profile,fixed,moving):
    X,Y=F(case['X']),F(case['Y']);flavor=case['flavor'];frees=[];known=[];orig=F(0);bound=F(3)
    require(0<X<=F(3,2) and 0<Y<=F(3,2) and flavor in range(5),'replacement domain')
    def add(typ,coord,lo,hi,rho,free=False,top=None):
        nonlocal orig
        hi=min(hi,bound)
        if hi<=lo or coord>bound:return
        geom=(typ=='v',lo,hi,coord,coord if top is None else top)
        if free:frees.append(geom);orig+=(hi-lo)*rho
        elif rho>0:known.append((*geom,rho*(hi-lo)))
    for t,c,lo,hi,w in fixed:
        if not w:continue
        e,z=(X,Y) if t=='v' else(Y,X)
        if c<=e and lo<z:
            mid=min(z,hi);add(t,c,lo,mid,w,True);add(t,c,mid,hi,w)
        else:add(t,c,lo,hi,w)
    for t,c,lo,hi,w in fs.repeated(fs.reflect_profile(profile),2,True):add(t,c,lo,hi,w)
    for t,c,lo,hi,w in moving+fs.repeated(profile,2):
        if t=='v':add(t,c+fam['d0'],lo,hi,w,top=c+fam['d1'])
        else:add(t,c,lo+fam['d1'],hi+fam['d0'],w)
    for xl,cy,w in fam['V']:add('h',cy,xl,2+fam['d0'],w)
    lo=F(9,5)
    while lo<bound:
        hi=min(bound,lo+F(1,40));add('h',lo,F(9,5),bound,hi-lo,top=hi);lo=hi
    grid=[F(i,10)for i in range(4,16)];grid=grid[::2]if flavor%2==0 else grid
    for x in grid:
        for y in grid:
            if (x-F('0.78'))**2+(y-F('0.78'))**2>F('0.40'):continue
            for length in ([F(1,8)]if flavor<3 else[F(1,16),F(1,4)]):
                for typ in ('v','h'):
                    c,mid=(x,y)if typ=='v'else(y,x);add(typ,c,mid-length/2,mid+length/2,F(0),True)
    weights=list(map(F,case['weights']));require(len(weights)==len(frees)and min(weights)>=0,'replacement weights')
    require(orig-sum(weights)==F(case['subtraction_per_corner'])>0,'replacement saving')
    return (X,Y),[(*g,w)for g,w in zip(frees,weights)]+known
def geometry_rows(pieces,flip):
    rows=[]
    for vert,l,h,a,z,w in pieces:
        if w:
            require(0<=a<=z and 0<=l<h and w>0,'nonnegative primitive')
            rows.append((int(bool(vert)^bool(flip)),ceil(G*l),floor(G*h),floor(G*a),ceil(G*z),floor(DS*w/(h-l))))
    return rows
def wire(rows):return (str(len(rows))+'\n'+''.join(' '.join(map(str,r))+'\n'for r in rows)).encode()
@lru_cache(None)
def inverse():
    a=[]
    for i in range(5):
        x=F(i,4);a.append([comb(4,j)*x**j*(1-x)**(4-j)for j in range(5)]+[F(i==j)for j in range(5)])
    for k in range(5):
        pivot=next(i for i in range(k,5)if a[i][k]);a[k],a[pivot]=a[pivot],a[k];a[k]=[v/a[k][k]for v in a[k]]
        for i in range(5):
            if i!=k:
                w=a[i][k];a[i]=[x-w*y for x,y in zip(a[i],a[k])]
    return [r[5:]for r in a]
@lru_cache(12000)
def faces(k,r,grouped=False):
    values=[[]for _ in range(4)]
    for i in range(5):
        t=F(4*r+i,4*k);den=1+t*t;c=(1-t*t)/den;s=2*t/den
        poly=[(s,F(0)),(c+s,s),(c,c+s),(F(0),c)]
        for j,(x,y)in enumerate(poly):
            X,Y=poly[(j+1)%4];u=Y-y;v=x-X;values[j].append((u*den**2,v*den**2,(u*x+v*y)*den**2))
    out=[]
    for vv in values:
        for ww in inverse():
            rr=[sum(v[j]*w for v,w in zip(vv,ww))for j in range(3)];l=lcm(*(v.denominator for v in rr));v=tuple(int(q*l)for q in rr);g=reduce(gcd,(abs(q)for q in v));row=tuple(q//g for q in v)
            if grouped or row not in out:out.append(row)
    require(all(max(map(abs,r))<2**61 for r in out),'face exceeds native range')
    return out
def hdr(k,r,xy,flip):
    x,y=xy[::-1]if flip else xy;q=faces(k,r);return [r,len(q),0,0,ceil(G*x),ceil(G*y)]+[v for row in q for v in row]
def ceildiv(a,b):return -((-a)//b)
def python_direction(lines,planes,xmax,ymax):
    @lru_cache(10000)
    def point(x,y):
        scores=[]
        for vert,lo,hi,fl,fh,rho in lines:
            L,U=lo,hi
            for a,b,c in planes:
                u,v=(b,a)if vert else(a,b);ox,oy=(y,x)if vert else(x,y);z=c*G+v*oy-v*(fh if v>0 else fl)
                if u>0:U=min(U,ox+z//u)
                elif u<0:L=max(L,ox+ceildiv(z,u))
                elif z<0:U=L
                if U<=L:break
            scores.append(max(0,U-L)*rho*M//(G*DS))
        return scores
    stack=[(0,0,xmax,ymax)];nodes=0
    while stack:
        x,y,X,Y=stack.pop();nodes+=1;vals=list(zip(point(x,y),point(X,y),point(x,Y),point(X,Y)));sums=[0]*4
        for row in vals:
            if min(row)>0:sums=[a+z for a,z in zip(sums,row)]
        if min(sums)>=M:continue
        require(max(X-x,Y-y)>4 and nodes<1600000,'unresolved independent cover')
        if X-x>=Y-y:
            mid=(x+X)//2;stack.extend([(x,y,mid,Y),(mid,y,X,Y)])
        else:
            mid=(y+Y)//2;stack.extend([(x,y,X,mid),(x,mid,X,Y)])
    return nodes
def coverage(rows):
    for flip in (0,1):
        rr=sorted((F(q['r'],q['k']),F(q['r']+1,q['k']))for q in rows if q['flip']==flip)
        require(rr and rr[0][0]==0,'missing zero direction');end=F(0)
        for l,h in rr:
            require(l==end and h>l,'angle gap or duplicate');end=h
        require(end*end+2*end>=1,'missing the diagonal angle')
def case(path,table,exe,tmp,extra=False):
    q=json.loads(gzip.decompress(path.read_bytes()));i=q['interval'];f,profile,fixed,trans=shape(i,table);require(q['family_sha256']==table[i-1]['family_sha256'],'unmatched family')
    if 'segments'in q:
        import altered
        coverage(q['rows']);which='proportional'if q.get('proportional')else 'balance'if 'points'in q else 'swept';return altered.replay(sys.modules[__name__],q,f,profile,fixed,trans,tmp/which,tmp,extra)
    box,pieces=cut(q,fixed)if 'pct'in q else bands(q,f,profile,fixed,trans);coverage(q['rows'])
    count=0;controls=0
    for flip in (0,1):
        rows=[z for z in q['rows']if z['flip']==flip];lines=geometry_rows(pieces,flip)
        ff=tmp/f'{i}_{flip}.txt';ff.write_bytes(wire(lines));headers=[hdr(z['k'],z['r'],box,flip)for z in rows];args=''.join(' '.join(map(str,h))+'\n'for h in headers)
        pr=subprocess.run([exe,ff],input=args,text=True,capture_output=True,check=True);out=pr.stdout.splitlines();require(len(out)==len(rows),'short native replay')
        for s,row in zip(out,rows):
            tok=s.split();require(tok[1]=='PASS'and list(map(int,tok[2:]))==[row['nodes'],row['leaves'],row['depth'],row['minimum']]and int(tok[5])>=M,'native replay mismatch');count+=1
        neg=tmp/'negative.txt';neg.write_bytes(wire([(*zz[:-1],0)for zz in lines]));rr=subprocess.run([exe,neg],input=' '.join(map(str,headers[0]))+'\n',text=True,capture_output=True,check=True);require(rr.stdout.split()[1]=='OPEN','negative control');controls+=1
        if extra:
            idx=max(range(len(rows)),key=lambda j:rows[j]['nodes']);h=headers[idx];z=rows[idx];require(python_direction(lines,faces(z['k'],z['r']),h[4],h[5])==z['nodes'],'independent exact check')
    return i,F(q['subtraction_per_corner']),count,controls
def root_above(x):
    t=10**19;a=isqrt(x.numerator*t*t//x.denominator);return F(a if a*a*x.denominator==x.numerator*t*t else a+1,t)
def old_family_upper(n,table):
    k=isqrt(n);vals=[F(0)]
    for rec in table:
        a,b=map(F,(rec['certified_line']['alpha'],rec['certified_line']['beta']));disc=4*a*a+n+4*b-4*a*k
        if disc<0:continue
        root=2*a+root_above(disc)
        if root>k+F(rec['d0']):vals.append(min(root,k+F(rec['d1'])))
    return max(vals)
def main(extra=False):
    table=json.load(open(H/'intervals.json'))['intervals'];cases={}
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td);exe=tmp/'local';subprocess.run(['c++','-O3','-std=c++17',H/'anchored.cpp','-o',exe],check=True)
        for name in ('swept','balance','proportional'):
            if (H/(name+'.cpp')).exists():subprocess.run(['c++','-O3','-std=c++17',H/(name+'.cpp'),'-o',tmp/name],check=True)
        for path in sorted((H/'claims').glob('*.json.gz')):
            i,sub,count,controls=case(path,table,exe,tmp,extra);require(i not in cases,'duplicate family');cases[i]=sub
            print(f'Interval {i} verified at {count} angle intervals with {controls} negative controls.',flush=True)
    refs=json.load(open(H/'comparisons.json'));rows=list(csv.DictReader(open(H/'bounds.csv')))
    require(len({r['n']for r in rows})==len(rows),'duplicate count')
    for r in rows:
        n=int(r['n']);i=int(r['interval']);L=F(r['new_side']);k=isqrt(n);d=L-k;iv=table[i-1]
        require(F(iv['d0'])<d<=F(iv['d1']),'family does not apply')
        a,b=map(F,(iv['certified_line']['alpha'],iv['certified_line']['beta']));mass=L*L-4*(a*d+b+cases[i]);require(mass<n and mass==F(r['total_mass_upper']),'unverified mass budget')
        require(L>old_family_upper(n,table),'fails to improve unrounded original formula')
        for q in refs[str(n)]:
            val=F(q['value']);require(L*L>val if q['kind']=='sqrt'else L>val,'comparison failed')
    print(f'{len(rows)} improved lower bounds checked.',flush=True)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--independent',action='store_true',help='Also check the hardest center cover in each reflection with Python integer arithmetic.');main(ap.parse_args().independent)
